import tkinter as tk
from tkinter import messagebox, BooleanVar
from contextlib import closing
from dashboard_return import DashboardReturnFrame
from session_context import clear_user, exit_session
from db_connection import get_db_connection
from path_utils import hash_password, verify_pin


class PasswordResetFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()
        self.first_name_var = tk.StringVar()
        self.last_name_var = tk.StringVar()
        self.phone_var = tk.StringVar()
        self.pin_var = tk.StringVar()

        self.build_ui()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def build_ui(self):
        title = tk.Label(
            self,
            text="Automating Innovating AI Production Manager App",
            font=("Helvetica", 20, "bold")
        )
        title.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")

        tk.Label(frame, text="Enter Username:").pack(pady=5)
        tk.Entry(frame, textvariable=self.username_var).pack(pady=5)

        tk.Label(frame, text="Enter First Name:").pack(pady=5)
        tk.Entry(frame, textvariable=self.first_name_var).pack(pady=5)

        tk.Label(frame, text="Enter Last Name:").pack(pady=5)
        tk.Entry(frame, textvariable=self.last_name_var).pack(pady=5)

        tk.Label(frame, text="Enter Phone Number:").pack(pady=5)
        tk.Entry(frame, textvariable=self.phone_var).pack(pady=5)

        tk.Label(frame, text="Enter Pin:").pack(pady=5)
        pin_entry = tk.Entry(frame, textvariable=self.pin_var, show="*")
        pin_entry.pack(pady=5)

        show_pin_var = BooleanVar()
        tk.Checkbutton(
            frame,
            text="Show Pin",
            variable=show_pin_var,
            command=lambda: self.toggle_visibility(pin_entry, show_pin_var)
        ).pack(pady=5)

        tk.Label(frame, text="Enter New Password:").pack(pady=5)
        pw_entry = tk.Entry(frame, textvariable=self.password_var, show="*")
        pw_entry.pack(pady=5)

        show_pw_var = BooleanVar()
        tk.Checkbutton(
            frame,
            text="Show Password",
            variable=show_pw_var,
            command=lambda: self.toggle_visibility(pw_entry, show_pw_var)
        ).pack(pady=5)

        tk.Button(frame, text="Reset Password", command=self.reset_password).pack(pady=10)
        tk.Button(frame, text="Exit", command=self.exit_session_app).pack(pady=10)

    # ---------------------------------------------------------
    # TOGGLE VISIBILITY
    # ---------------------------------------------------------
    def toggle_visibility(self, entry, var):
        entry.config(show="" if var.get() else "*")

    # ---------------------------------------------------------
    # CLEAR
    # ---------------------------------------------------------
    def clear_fields(self):
        self.username_var.set("")
        self.password_var.set("")
        self.first_name_var.set("")
        self.last_name_var.set("")
        self.phone_var.set("")
        self.pin_var.set("")

    # ---------------------------------------------------------
    # EXIT
    # ---------------------------------------------------------
    def exit_session_app(self):
        self.clear_fields()
        clear_user()
        exit_session()

    # ---------------------------------------------------------
    # RESET PASSWORD
    # ---------------------------------------------------------
    def reset_password(self):
        username = self.username_var.get()
        new_password = self.password_var.get()
        first_name = self.first_name_var.get()
        last_name = self.last_name_var.get()
        phone_number = self.phone_var.get()
        pin = self.pin_var.get()

        cnxn = get_db_connection()
        cursor = cnxn.cursor()

        with cnxn as conn:
            with closing(conn.cursor()) as cursor:
                cursor.execute("SELECT username, salt FROM users")
                rows = cursor.fetchall()

                stored_salt = None
                stored_pin_hash = None

                for stored_username, salt in rows:
                    if username == stored_username:
                        stored_salt = salt
                        cursor.execute("SELECT pin FROM users WHERE username=?", (username,))
                        pin_row = cursor.fetchone()
                        if not pin_row:
                            messagebox.showerror("Error", "PIN not found.")
                            return
                        stored_pin_hash = pin_row[0]
                        break

                if not stored_salt:
                    messagebox.showerror("Error", "User not found.")
                    return

                if not verify_pin(pin, stored_pin_hash):
                    messagebox.showerror("Error", "Invalid PIN.")
                    self.exit_session_app()
                    return

                cursor.execute(
                    "SELECT first_name, last_name, phone_number FROM users WHERE username=?",
                    (username,)
                )
                row = cursor.fetchone()
                if not row:
                    messagebox.showerror("Error", "User not found.")
                    return

                db_first, db_last, db_phone = row

                stored_first = db_first
                stored_last = db_last
                stored_phone = db_phone

                if first_name != stored_first:
                    messagebox.showerror("Incorrect first name.")
                    return
                if last_name != stored_last:
                    messagebox.showerror("Incorrect last name.")
                    return
                if phone_number != stored_phone:
                    messagebox.showerror("Incorrect phone number.")
                    return

                cursor.execute(
                    """SELECT username FROM users
                       WHERE username=? AND first_name=? AND last_name=?
                       AND phone_number=? AND pin=? AND salt=?""",
                    (username, db_first, db_last, db_phone, stored_pin_hash, stored_salt)
                )
                result = cursor.fetchone()

                if result:
                    hashed_pw = hash_password(new_password)
                    cursor.execute(
                        "UPDATE users SET password=?, salt=? WHERE username=?",
                        (hashed_pw, stored_salt, username)
                    )
                    conn.commit()

                    if messagebox.askyesno("Continue", "Password reset successfully. Return to Dashboard?"):
                        self.controller.show_frame(DashboardReturnFrame)
                else:
                    messagebox.showerror("Error", "User info mismatch.")
                    self.exit_session_app()


def main():
    pass