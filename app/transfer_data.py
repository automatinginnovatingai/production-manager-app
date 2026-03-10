import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import pyodbc
import re
from session_context import verify_admin, enforce_plan, exit_session
from startup_page import StartPageFrame

class TransferFrame(tk.Frame):
    def __init__(self, parent, controller):
        super().__init__(parent)
        self.controller = controller

        # Try to get connection string + DB name up front
        try:
            self.conn_str = self.controller.get_sql_connection_string()
            self.db_name = self._extract_database_name(self.conn_str)
        except Exception as e:
            self.conn_str = None
            self.db_name = None
            messagebox.showerror("Error", f"Failed to load SQL connection info:\n{e}")

        self._build_ui()

    # ---------------- UI ----------------

    def _build_ui(self):
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        container = ttk.Frame(self)
        container.grid(row=0, column=0, sticky="nsew", padx=20, pady=20)

        title = ttk.Label(
            container,
            text="Transfer Data Between Computers",
            font=("Segoe UI", 14, "bold")
        )
        title.grid(row=0, column=0, columnspan=2, pady=(0, 10))

        db_label_text = f"Database: {self.db_name}" if self.db_name else "Database: (unknown)"
        self.db_label = ttk.Label(container, text=db_label_text, font=("Segoe UI", 9))
        self.db_label.grid(row=1, column=0, columnspan=2, pady=(0, 15))

        # Backup section (old computer)
        backup_frame = ttk.LabelFrame(container, text="On the OLD Computer")
        backup_frame.grid(row=2, column=0, sticky="nsew", padx=(0, 10), pady=(0, 10))

        backup_desc = ttk.Label(
            backup_frame,
            text=(
                "Create a transfer file (.bak) from this computer.\n"
                "Copy it to a USB drive and take it to the new computer."
            ),
            justify="left"
        )
        backup_desc.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        backup_btn = ttk.Button(
            backup_frame,
            text="Create Transfer File",
            command=self._on_backup_clicked
        )
        backup_btn.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        # Restore section (new computer)
        restore_frame = ttk.LabelFrame(container, text="On the NEW Computer")
        restore_frame.grid(row=2, column=1, sticky="nsew", padx=(10, 0), pady=(0, 10))

        restore_desc = ttk.Label(
            restore_frame,
            text=(
                "Restore a transfer file (.bak) from your old computer.\n"
                "This will replace the empty database on this machine."
            ),
            justify="left"
        )
        restore_desc.grid(row=0, column=0, padx=10, pady=(10, 5), sticky="w")

        restore_btn = ttk.Button(
            restore_frame,
            text="Restore Transfer File",
            command=self._on_restore_clicked
        )
        restore_btn.grid(row=1, column=0, padx=10, pady=(0, 10), sticky="w")

        container.columnconfigure(0, weight=1)
        container.columnconfigure(1, weight=1)

        self.status_label = ttk.Label(self, text="", foreground="gray")
        self.status_label.grid(row=1, column=0, pady=(5, 0))

    # ---------------- Events ----------------

    def _on_backup_clicked(self):
        if not self._ensure_connection_info():
            return

        default_name = f"{self.db_name or 'database'}_transfer.bak"
        backup_path = filedialog.asksaveasfilename(
            title="Save Transfer File",
            defaultextension=".bak",
            filetypes=[("SQL Server Backup", "*.bak")],
            initialfile=default_name
        )
        if not backup_path:
            return

        try:
            self._set_status("Creating transfer file, please wait...")
            self.update_idletasks()
            self._backup_database(self.conn_str, backup_path)
            self._set_status("Transfer file created successfully.")
            messagebox.showinfo("Success", f"Transfer file created:\n{backup_path}")
        except Exception as e:
            self._set_status("Backup failed.")
            messagebox.showerror("Backup Failed", f"An error occurred while creating the transfer file:\n\n{e}")

    def _on_restore_clicked(self):
        if not self._ensure_connection_info():
            return

        backup_path = filedialog.askopenfilename(
            title="Select Transfer File",
            filetypes=[("SQL Server Backup", "*.bak")]
        )
        if not backup_path:
            return

        confirm = messagebox.askyesno(
            "Confirm Restore",
            "This will replace the current database on this machine with the data from the transfer file.\n\n"
            "Are you sure you want to continue?"
        )
        if not confirm:
            return

        try:
            self._set_status("Restoring transfer file, please wait...")
            self.update_idletasks()
            self._restore_database(self.conn_str, backup_path)
            self._set_status("Database restored successfully.")
            messagebox.showinfo(
                "Success",
                "Database restored successfully.\n"
                "This computer now has the data from the old machine."
            )
        except Exception as e:
            self._set_status("Restore failed.")
            messagebox.showerror("Restore Failed", f"An error occurred while restoring the transfer file:\n\n{e}")

    # ---------------- Helpers ----------------

    def _set_status(self, text: str):
        self.status_label.config(text=text)

    def _ensure_connection_info(self) -> bool:
        if not self.conn_str or not self.db_name:
            try:
                self.conn_str = self.controller.get_sql_connection_string()
                self.db_name = self._extract_database_name(self.conn_str)
                self.db_label.config(text=f"Database: {self.db_name}")
                return True
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load SQL connection info:\n{e}")
                return False
        return True

    @staticmethod
    def _extract_database_name(conn_str: str) -> str:
        match = re.search(r"Database\s*=\s*([^;]+)", conn_str, re.IGNORECASE)
        if not match:
            raise ValueError("Could not find Database=... in connection string")
        return match.group(1).strip()

    # ---------------- SQL Server backup / restore ----------------

    def _backup_database(self, conn_str: str, backup_path: str):
        db_name = self._extract_database_name(conn_str)
        master_conn_str = re.sub(
            r"Database\s*=\s*[^;]+",
            "Database=master",
            conn_str,
            flags=re.IGNORECASE
        )

        with pyodbc.connect(master_conn_str, autocommit=True) as conn:
            cursor = conn.cursor()
            # Force single user to avoid locks
            cursor.execute(f"ALTER DATABASE [{db_name}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;")
            cursor.execute("BACKUP DATABASE [{0}] TO DISK = ? WITH INIT;".format(db_name), backup_path)
            cursor.execute(f"ALTER DATABASE [{db_name}] SET MULTI_USER;")

    def _restore_database(self, conn_str: str, backup_path: str):
        db_name = self._extract_database_name(conn_str)
        master_conn_str = re.sub(
            r"Database\s*=\s*[^;]+",
            "Database=master",
            conn_str,
            flags=re.IGNORECASE
        )

        with pyodbc.connect(master_conn_str, autocommit=True) as conn:
            cursor = conn.cursor()
            # Force single user to restore
            cursor.execute(f"ALTER DATABASE [{db_name}] SET SINGLE_USER WITH ROLLBACK IMMEDIATE;")
            cursor.execute("RESTORE DATABASE [{0}] FROM DISK = ? WITH REPLACE;".format(db_name), backup_path)
            cursor.execute(f"ALTER DATABASE [{db_name}] SET MULTI_USER;")

    def on_show(self):
        # ADMIN CHECK
        if not verify_admin():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        # PLAN CHECK
        if not enforce_plan("basic", "pro", "enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            self.controller.show_frame(StartPageFrame)
            return False

        return True 