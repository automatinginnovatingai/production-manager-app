import tkinter as tk
from tkinter import messagebox
import socket
import pyodbc

from license_storage import save_local_activation
from schema_manager import ensure_schema


class SQLConnectionFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=20)

    def on_show(self):
        self.status_label.config(
            text="Please be patient… the database is being created.\nThis may take up to a minute."
        )
        self.after(200, self.auto_connect)

    def get_express_server_candidates(self):
        machine = socket.gethostname()
        return [
            f"{machine}\\SQLEXPRESS",   # primary, most correct
            r"(local)\SQLEXPRESS",
            r".\SQLEXPRESS",
            r"localhost\SQLEXPRESS",
        ]

    def find_working_server(self):
        for candidate in self.get_express_server_candidates():
            test_str = (
                f"DRIVER={{ODBC Driver 18 for SQL Server}};"
                f"SERVER={candidate};"
                f"DATABASE=master;"
                f"Trusted_Connection=yes;"
                "Encrypt=no;"
                "TrustServerCertificate=yes;"
            )
            try:
                pyodbc.connect(test_str, timeout=3)
                return candidate
            except Exception as e:
                print(f"FAILED: {candidate} → {e}")
                continue

        return None

    def auto_connect(self):
        db = "Production_Manager_App_DB"

        # Find a working SQL Express server
        host = self.find_working_server()
        if host is None:
            messagebox.showerror(
                "SQL Error",
                "Could not connect to SQL Server Express.\n"
                "Ensure SQL Server Express is installed and running."
            )
            return

        # Connect to master to create DB if needed
        master_conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={host};"
            f"DATABASE=master;"
            f"Trusted_Connection=yes;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )

        try:
            master_conn = pyodbc.connect(master_conn_str, autocommit=True)
            master_cursor = master_conn.cursor()
        except Exception as e:
            messagebox.showerror("SQL Error", f"Could not connect to SQL Server master DB:\n{e}")
            return

        try:
            master_cursor.execute(f"""
                IF NOT EXISTS (SELECT name FROM sys.databases WHERE name = '{db}')
                BEGIN
                    CREATE DATABASE {db};
                END
            """)
            master_conn.commit()
        except Exception as e:
            messagebox.showerror("Database Creation Error", str(e))
            return
        finally:
            master_conn.close()

        # Connect to the actual app DB
        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={host};"
            f"DATABASE={db};"
            f"Trusted_Connection=yes;"
            "Encrypt=no;"
            "TrustServerCertificate=yes;"
        )

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
        except Exception as e:
            messagebox.showerror("SQL Error", f"Could not connect to {db}:\n{e}")
            return

        # Save activation with Windows Auth
        save_local_activation(
            activation_id=None,
            sql_host=host,
            sql_db=db,
            sql_user=None,
            sql_pwd=None
        )

        # Ensure schema exists
        try:
            ensure_schema(cursor, conn)
            conn.commit()
        except Exception as e:
            messagebox.showerror("Schema Error", str(e))
            return

        # Register activation
        try:
            cursor.execute(
                "{CALL register_activation (?, ?, ?, ?)}",
                self.controller.license_key,
                1,
                self.controller.subscription_plan,
                None
            )
            row = cursor.fetchone()
            if row is None:
                raise Exception("register_activation returned no activation_id")

            activation_id = row[0]
            conn.commit()

        except Exception as e:
            messagebox.showerror("Activation Error", str(e))
            return

        # Save final activation
        save_local_activation(
            activation_id,
            host,
            db,
            None,
            None
        )

        self.controller.activation_id = activation_id

        messagebox.showinfo("Success", "Activation complete. Launching application.")
        self.go_to_start_page()

    def go_to_start_page(self):
        from startup_page import StartPageFrame
        self.controller.show_frame(StartPageFrame)