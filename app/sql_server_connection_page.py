import tkinter as tk
from tkinter import messagebox
import pyodbc

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

        tk.Button(self, text="Connect", command=self.connect).pack(pady=10)

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

        # Step 1 — Test connection
        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
        except Exception as e:
            messagebox.showerror("Connection Failed", str(e))
            return

        # Step 2 — Save SQL creds locally (activation_id still None)
        save_local_activation(
            activation_id=None,
            sql_host=host,
            sql_db=db,
            sql_user=user,
            sql_pwd=pwd
        )

        # Step 3 — Ensure schema exists
        try:
            ensure_schema(cursor, conn)
            conn.commit()
        except Exception as e:
            messagebox.showerror("Schema Error", str(e))
            return

        # Step 4 — Register activation in SQL Server
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

        # Step 5 — Save activation_id + SQL creds via DPAPI
        save_local_activation(
            activation_id,
            host,
            db,
            user,
            pwd
        )

        self.controller.activation_id = activation_id

        messagebox.showinfo("Success", "Activation complete. Launching application.")
        self.go_to_start_page()

    def go_to_start_page(self):
        from startup_page import StartPageFrame
        self.controller.show_frame(StartPageFrame)