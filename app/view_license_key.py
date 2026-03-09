import tkinter as tk
from tkinter import messagebox
from Admin_Interface import AdminInterfaceFrame
from startup_page import StartPageFrame
from db_connection import get_db_connection
from session_context import verify_admin, enforce_plan, exit_session


class ViewLicenseKeyFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.username_var = tk.StringVar()
        self.build_ui()

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

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def build_ui(self):
        tk.Label(
            self,
            text="Enter Username:",
            font=("Arial", 14, "bold")
        ).pack(pady=20)

        tk.Entry(
            self,
            textvariable=self.username_var,
            width=40
        ).pack(pady=10)

        tk.Button(
            self,
            text="Get License Key",
            font=("Arial", 12, "bold"),
            command=self.show_license_key,
            bg="green"
        ).pack(pady=20)

        tk.Button(
            self,
            text="Return to Admin Interface",
            font=("Arial", 12),
            command=lambda: self.controller.show_frame(AdminInterfaceFrame),
            bg="gold"
        ).pack(pady=10)

    # ---------------------------------------------------------
    # FETCH LICENSE KEY
    # ---------------------------------------------------------
    def fetch_license_key(self, username):
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("SELECT username, salt, license_key FROM users")
        rows = cursor.fetchall()
        conn.close()

        for stored_username, stored_salt, user_license in rows:
            if username == stored_username:
                try:
                    return user_license
                except Exception as e:
                    messagebox.showerror("Error", f"Failed to decrypt license key: {e}")
                    return None

        messagebox.showerror("Error", "Username not found.")
        return None

    # ---------------------------------------------------------
    # DISPLAY LICENSE KEY
    # ---------------------------------------------------------
    def show_license_key(self):
        username = self.username_var.get().strip()
        if not username:
            messagebox.showwarning("Input Required", "Please enter a username.")
            return

        license_key = self.fetch_license_key(username)
        if not license_key:
            return

        display = tk.Toplevel(self)
        display.title("License Key Viewer")
        display.attributes("-fullscreen", True)

        tk.Label(
            display,
            text="Decrypted License Key:",
            font=("Arial", 16, "bold")
        ).pack(pady=20)

        tk.Label(
            display,
            text=license_key,
            font=("Arial", 14),
            wraplength=600
        ).pack(pady=20)

        tk.Button(
            display,
            text="Return to Admin Interface",
            font=("Arial", 12, "bold"),
            command=lambda: [
                display.destroy(),
                self.controller.show_frame(AdminInterfaceFrame)    
            ],
             bg="gold"
        ).pack(pady=30)


def main():
    pass