import tkinter as tk
from tkinter import ttk, messagebox
import socket
import pyodbc
import threading

from license_storage import save_local_activation
from schema_manager import ensure_schema


class SQLConnectionFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

        self.progress = ttk.Progressbar(
            self, orient="horizontal", length=300, mode="determinate"
        )
        self.progress.pack(pady=10)

        self.total_steps = 6
        self.current_step = 0

    def update_progress(self, text):
        self.current_step += 1
        percent = int((self.current_step / self.total_steps) * 100)

        def update():
            self.status_label.config(text=text)
            self.progress["value"] = percent

        self.after(0, update)

    def on_show(self):
        self.status_label.config(text="Please wait… preparing SQL Server connection.")
        self.progress["value"] = 0
        self.current_step = 0

        threading.Thread(target=self.auto_connect, daemon=True).start()

    def get_express_server_candidates(self):
        machine = socket.gethostname()
        return [
            f"{machine}\\SQLEXPRESS",
            r"(local)\SQLEXPRESS",
            r".\SQLEXPRESS",
            r"localhost\SQLEXPRESS",
        ]

    def find_working_server(self):
        for candidate in self.get_express_server_candidates():
            test_str = (
                "DRIVER={ODBC Driver 18 for SQL Server};"
                f"SERVER={candidate};"
                "DATABASE=master;"
                "Trusted_Connection=yes;"
                "Encrypt=no;"
                "TrustServerCertificate=yes;"
            )
            try:
                pyodbc.connect(test_str, timeout=3)
                return candidate
            except Exception:
                continue

        return None

    def auto_connect(self):
        db = "Production_Manager_App_DB"

        # STEP 1 — Find SQL Express
        self.update_progress("Searching for SQL Server Express…")
        host = self.find_working_server()
        if host is None:
            messagebox.showerror("ERROR", "Could not find SQL Server Express.")
            self.after(0, self.go_to_start_page)
            return

        # STEP 2 — Connect to master
        self.update_progress("Connecting to master database…")
        master_conn_str = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={host};"
            "DATABASE=master;"
            "Trusted_Connection=yes;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )

        try:
            master_conn = pyodbc.connect(master_conn_str, autocommit=True, timeout=5)
            master_cursor = master_conn.cursor()
        except Exception:
            messagebox.showerror("ERROR", "Could not connect to SQL Server master DB.")
            self.after(0, self.go_to_start_page)
            return

        # STEP 3 — Create DB if needed
        self.update_progress("Ensuring database exists…")
        try:
            master_cursor.execute(f"""
                IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{db}')
                BEGIN
                    CREATE DATABASE {db};
                END
            """)
            master_conn.commit()
        except Exception:
            pass
        finally:
            master_conn.close()

        # STEP 4 — Connect to app DB
        self.update_progress("Connecting to application database…")
        conn_str = (
            "DRIVER={ODBC Driver 18 for SQL Server};"
            f"SERVER={host};"
            f"DATABASE={db};"
            "Trusted_Connection=yes;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )

        try:
            conn = pyodbc.connect(conn_str, timeout=5)
            cursor = conn.cursor()
        except Exception:
            messagebox.showerror("ERROR", "Could not connect to application database.")
            self.after(0, self.go_to_start_page)
            return

        # SUCCESS — DB CONNECTED
        messagebox.showinfo("Database Connected", "Database connection successful. Redirecting…")

        save_local_activation(None, host, db, None, None)

        # STEP 5 — Schema creation
        self.update_progress("Creating tables and stored procedures…")
        try:
            ensure_schema(cursor, conn)
            conn.commit()
        except Exception:
            pass

        # STEP 6 — Activation
        self.update_progress("Registering activation…")
        try:
            cursor.execute(
                "{CALL register_activation (?, ?, ?, ?)}",
                self.controller.license_key,
                1,
                self.controller.subscription_plan,
                None
            )
            row = cursor.fetchone()
            if row:
                activation_id = row[0]
                conn.commit()
                save_local_activation(activation_id, host, db, None, None)
                self.controller.activation_id = activation_id
        except Exception:
            pass

        # Redirect — ALWAYS
        self.after(0, self.go_to_start_page)

    def go_to_start_page(self):
        from startup_page import StartPageFrame
        self.controller.show_frame(StartPageFrame)