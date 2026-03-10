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
        self.after(100, self.auto_connect)

    def auto_connect(self):
        host = socket.gethostname()
        instance = "ProductionManagerApp"
        db = "Production_Manager_App_DB"

        master_conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={host}\\{instance};"
            f"DATABASE=master;"
            f"Trusted_Connection=yes;"
            "Encrypt=no;"
        )

        try:
            master_conn = pyodbc.connect(master_conn_str)
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

        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={host}\\{instance};"
            f"DATABASE={db};"
            f"Trusted_Connection=yes;"
            "Encrypt=no;"
        )

        try:
            conn = pyodbc.connect(conn_str)
            cursor = conn.cursor()
        except Exception as e:
            messagebox.showerror("SQL Error", f"Could not connect to YourDB:\n{e}")
            return

        save_local_activation(
            activation_id=None,
            sql_host=f"{host}\\{instance}",
            sql_db=db,
            sql_user=None,
            sql_pwd=None
        )

        try:
            ensure_schema(cursor, conn)
            conn.commit()
        except Exception as e:
            messagebox.showerror("Schema Error", str(e))
            return

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