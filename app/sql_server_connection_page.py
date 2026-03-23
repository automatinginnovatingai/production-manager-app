import tkinter as tk
from tkinter import ttk
import pyodbc
import threading

from license_storage import save_local_activation, load_local_activation
from schema_manager import ensure_schema


class SQLServerConnectionFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        tk.Label(self, text="SQL Server Host:").pack()
        self.host_entry = tk.Entry(self, width=40)
        self.host_entry.pack()

        tk.Label(self, text="Database Name:").pack()
        self.db_entry = tk.Entry(self, width=40)
        self.db_entry.insert(0, "Production_Manager_App_DB")
        self.db_entry.pack()

        tk.Label(self, text="SQL Username:").pack()
        self.user_entry = tk.Entry(self, width=40)
        self.user_entry.pack()

        tk.Label(self, text="SQL Password:").pack()
        self.pwd_entry = tk.Entry(self, width=40, show="*")
        self.pwd_entry.pack()

        tk.Button(self, text="Connect", command=self.start_connect_thread).pack(pady=10)

        # Progress bar
        self.progress = ttk.Progressbar(self, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

        self.total_steps = 4
        self.current_step = 0

        self.status_label = tk.Label(self, text="", font=("Arial", 12))
        self.status_label.pack(pady=10)

    def update_progress(self, text):
        self.current_step += 1
        percent = int((self.current_step / self.total_steps) * 100)

        def update():
            self.status_label.config(text=text)
            self.progress["value"] = percent

        self.after(0, update)

    def on_show(self):
        saved = load_local_activation()
        if saved:
            if saved.get("sql_host"):
                self.host_entry.delete(0, tk.END)
                self.host_entry.insert(0, saved["sql_host"])

            if saved.get("sql_db"):
                self.db_entry.delete(0, tk.END)
                self.db_entry.insert(0, saved["sql_db"])

            if saved.get("sql_user"):
                self.user_entry.delete(0, tk.END)
                self.user_entry.insert(0, saved["sql_user"])

        self.progress["value"] = 0
        self.current_step = 0
        self.status_label.config(text="Ready to connect.")

    def start_connect_thread(self):
        threading.Thread(target=self.connect, daemon=True).start()

    def connect(self):
        host = self.host_entry.get().strip()
        db = self.db_entry.get().strip()
        user = self.user_entry.get().strip()
        pwd = self.pwd_entry.get().strip()

        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={host},1433;"
            f"DATABASE={db};"
            f"UID={user};"
            f"PWD={pwd};"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;"
        )

        # STEP 1 — Test connection
        self.update_progress("Testing SQL Server connection…")
        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
        except:
            self.after(0, self.go_to_start_page)
            return

        # STEP 2 — Save SQL creds
        self.update_progress("Saving SQL credentials…")
        save_local_activation(
            activation_id=None,
            sql_host=host,
            sql_db=db,
            sql_user=user,
            sql_pwd=pwd
        )

        # STEP 3 — Ensure schema
        self.update_progress("Ensuring database schema…")
        try:
            ensure_schema(cursor, conn)
            conn.commit()
        except:
            pass

        # STEP 4 — Register activation
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
                save_local_activation(activation_id, host, db, user, pwd)
                self.controller.activation_id = activation_id
        except:
            pass

        # ALWAYS redirect
        self.after(0, self.go_to_start_page)

    def go_to_start_page(self):
        from startup_page import StartPageFrame
        self.controller.show_frame(StartPageFrame)