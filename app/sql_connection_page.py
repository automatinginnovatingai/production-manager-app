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

        # Automatically attempt connection when this frame loads
        self.after(100, self.auto_connect)

    def auto_connect(self):
        host = socket.gethostname()
        instance = "MYAPP"      # Your SQL Express instance name
        db = "YourDB"           # Your database name

        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={host}\\{instance};"
            f"DATABASE={db};"
            f"Trusted_Connection=yes;"
            "Encrypt=no;"
        )

        # Step 1 — Connect to SQL Server Express
        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
        except Exception as e:
            messagebox.showerror("SQL Error", f"Could not connect to SQL Server:\n{e}")
            return

        # Step 2 — Save SQL info locally (no username/password)
        save_local_activation(
            activation_id=None,
            sql_host=f"{host}\\{instance}",
            sql_db=db,
            sql_user=None,
            sql_pwd=None
        )

        # Step 3 — Ensure schema exists
        try:
            ensure_schema(cursor, conn)
            conn.commit()
        except Exception as e:
            messagebox.showerror("Schema Error", str(e))
            return

        # Step 4 — Register activation
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

        # Step 5 — Save activation_id
        save_local_activation(
            activation_id,
            f"{host}\\{instance}",
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