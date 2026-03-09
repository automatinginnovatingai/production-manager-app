import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import hmac
import hashlib
import os

from Admin_Interface import AdminInterfaceFrame
from startup_page import StartPageFrame
from session_context import verify_admin, exit_session, enforce_plan
from db_connection import get_db_connection


class InstallerActivationFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.build_ui()

    def on_show(self):
        if not verify_admin():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        if not enforce_plan("enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            self.controller.show_frame(StartPageFrame)
            return False

        return True

    # ---------------------------------------------------------
    # UI BUILD
    # ---------------------------------------------------------
    def build_ui(self):
        title = tk.Label(
            self,
            text="Automating Innovating AI Production Manager App",
            font=("Helvetica", 24, "bold")
        )
        title.pack(pady=10)

        content_frame = tk.Frame(self)
        content_frame.pack(padx=20, pady=10, fill="both", expand=True)

        employee_frame = tk.LabelFrame(
            content_frame,
            text="Installer Activation",
            font=("Helvetica", 16, "bold")
        )
        employee_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # ENTRY WIDGETS
        self.employee_username_entry = tk.Entry(employee_frame)
        self.gumroad_license_entry = tk.Entry(employee_frame)

        labels = [
            ("Enter employee username:", self.employee_username_entry),
            ("Enter employee Gumroad license:", self.gumroad_license_entry),
        ]

        for i, (text, entry) in enumerate(labels):
            tk.Label(employee_frame, text=text, anchor="w").grid(
                row=i, column=0, sticky="w", padx=10, pady=5
            )
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

        # Calendar
        calendar_frame = tk.LabelFrame(content_frame, text="Calendar", font=("Arial", 12, "bold"))
        calendar_frame.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        now = datetime.datetime.now()
        tk.Label(calendar_frame, text="Time", font=("Arial", 10)).pack(padx=10, pady=5)
        self.time_frame = tk.Label(calendar_frame, text=now.strftime("%H:%M:%S"), font=("Arial", 10))
        self.time_frame.pack(padx=10, pady=5)

        self.date_frame = tk.Label(calendar_frame, text=now.strftime("%m/%d/%Y"), font=("Arial", 10))
        self.date_frame.pack(padx=10, pady=5)

        content_frame.grid_columnconfigure(0, weight=3)
        content_frame.grid_columnconfigure(1, weight=1)

        # Buttons
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=20, fill="x")

        buttons = [
            ("Exit", exit_session, "red"),
            ("Admin Interface", self.back_to_menu, "blue"),
            ("Save", self.update_data, "green"),
            ("Clear Form", self.clear_user_input, "yellow")
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            tk.Button(
                buttons_frame,
                text=text,
                command=cmd,
                font=("Helvetica", 12, "bold"),
                bg=color
            ).grid(row=0, column=i, padx=10, pady=10, sticky="ew")

        for i in range(len(buttons)):
            buttons_frame.grid_columnconfigure(i, weight=1)

    # ---------------------------------------------------------
    # UPDATE DATA (ACTIVATION)
    # ---------------------------------------------------------
    def update_data(self):
        username = self.employee_username_entry.get().strip()
        gumroad_key = self.gumroad_license_entry.get().strip()

        if not (username and gumroad_key):
            messagebox.showerror("Missing Data", "All fields are required.")
            return

        try:
            conn, cursor = get_db_connection()

            # Look up installer
            cursor.execute("""
                SELECT user_key
                FROM AIAI_Employee_Info
                WHERE Employee_Username = ?
            """, (username,))
            row = cursor.fetchone()

            if not row:
                messagebox.showerror("Error", "Installer not found.")
                return

            user_key = row[0]

            # Create salt
            salt = os.urandom(32)

            # Hash Gumroad key using HMAC-SHA256
            gumroad_hash = hmac.new(
                salt,
                gumroad_key.encode("utf-8"),
                hashlib.sha256
            ).digest()

            # Update installer record
            cursor.execute("""
                UPDATE AIAI_Employee_Info
                SET gumroad_key_hash = ?, salt = ?, plan = ?, created_at = SYSUTCDATETIME()
                WHERE user_key = ?
            """, (gumroad_hash, salt, "installer", user_key))

            conn.commit()
            messagebox.showinfo("Success", "Installer activation updated.")
            self.back_to_menu()

        except Exception as e:
            messagebox.showerror("Database Error", str(e))

    def back_to_menu(self):
        self.controller.show_frame(AdminInterfaceFrame)

    def clear_user_input(self):
        for entry in [
            self.employee_username_entry,
            self.gumroad_license_entry
        ]:
            entry.delete(0, tk.END)