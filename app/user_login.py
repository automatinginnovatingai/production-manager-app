import tkinter as tk
from tkinter import messagebox, BooleanVar
import time
from password_reset import PasswordResetFrame
from db_connection import get_db_connection
from session_context import set_user, normalize_flag
from path_utils import verify_password

class UserLoginFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.username_var = tk.StringVar()
        self.password_var = tk.StringVar()

        self.build_home()

    # ---------------------------------------------------------
    # HOME SCREEN
    # ---------------------------------------------------------
    def build_home(self):
        for w in self.winfo_children():
            w.destroy()

        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")

        tk.Label(
            frame,
            text="Automating Innovating AI Production Manager App",
            font=("Helvetica", 32, "bold")
        ).grid(row=0, column=0, columnspan=3, pady=10)

        tk.Button(
            frame,
            text="Sign In",
            font=("Helvetica", 12, "bold"),
            bg="green",
            command=self.build_signin
        ).grid(row=5, column=0, columnspan=3, pady=10)

        tk.Button(
            frame,
            text="Exit",
            font=("Helvetica", 12, "bold"),
            bg="red",
            command=self.exit_app
        ).grid(row=6, column=0, columnspan=3, pady=10)

    # ---------------------------------------------------------
    # SIGN-IN SCREEN
    # ---------------------------------------------------------
    def build_signin(self):
        for w in self.winfo_children():
            w.destroy()

        frame = tk.Frame(self)
        frame.pack()

        tk.Label(
            frame,
            text="Automating Innovating AI Production Manager App",
            font="bold, 32"
        ).grid(row=0, column=0, columnspan=3, pady=10)

        tk.Label(frame, text="Username", font="bold").grid(row=1, column=0, sticky="e")
        tk.Entry(frame, textvariable=self.username_var).grid(row=1, column=1, padx=5)

        tk.Label(frame, text="Password", font="bold").grid(row=2, column=0, sticky="e")

        pw_entry = tk.Entry(frame, textvariable=self.password_var, show="*")
        pw_entry.grid(row=2, column=1, padx=5)

        show_pw_var = BooleanVar()
        tk.Checkbutton(
            frame,
            text="Show Password",
            variable=show_pw_var,
            command=lambda: self.toggle_visibility(pw_entry, show_pw_var)
        ).grid(row=3, column=1, sticky="w")

        tk.Button(
            frame,
            text="Login",
            font="bold",
            bg="green",
            command=self.login_user
        ).grid(row=5, column=0, columnspan=3, pady=10)

        tk.Button(
            frame,
            text="Forgot Password?",
            font="bold",
            bg="red",
            command=lambda: self.controller.show_frame(PasswordResetFrame)
        ).grid(row=6, column=0, columnspan=3, pady=10)

        tk.Button(
            frame,
            text="Exit",
            font="bold",
            bg="red",
            command=self.exit_app
        ).grid(row=8, column=0, columnspan=3, pady=10)

    # ---------------------------------------------------------
    # TOGGLE VISIBILITY
    # ---------------------------------------------------------
    def toggle_visibility(self, entry, var):
        entry.config(show="" if var.get() else "*")

    # ---------------------------------------------------------
    # LOGIN LOGIC
    # ---------------------------------------------------------
    def login_user(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        cnxn = get_db_connection()
        cursor = cnxn.cursor()

        cursor.execute("""
            SELECT username, password, agreed, failed_attempts, time_hashed,
                   user_key, company_name, is_admin, mac_id_check
            FROM users
        """)

        found = None
        for row in cursor.fetchall():
            db_user, db_pw, agreed, fails, time_hash, user_key, company_name, is_admin, mac_id = row
            if username == db_user:
                found = row
                break

        if not found:
            cnxn.close()
            messagebox.showerror("Error", "Username not found.")
            return

        db_user, stored_pw, agreed, fails, time_hash, user_key, company_name, is_admin, mac_id = found
        now = int(time.time())

        # ---------------------------------------------------------
        # LOCKOUT CHECK
        # ---------------------------------------------------------
        if time_hash and now - int(time_hash) < 300:
            messagebox.showwarning("Locked Out", "Too many failed attempts. Wait 5 minutes.")
            cnxn.close()
            return

        # ---------------------------------------------------------
        # PASSWORD VERIFICATION
        # ---------------------------------------------------------
        if not verify_password(password, stored_pw):
            fails = (fails or 0) + 1

            if fails >= 3:
                cursor.execute(
                    "UPDATE users SET failed_attempts=?, time_hashed=? WHERE username=?",
                    (fails, str(now), db_user)
                )
                messagebox.showwarning("Locked Out", "Too many failed attempts. Wait 5 minutes.")
            else:
                cursor.execute(
                    "UPDATE users SET failed_attempts=? WHERE username=?",
                    (fails, db_user)
                )
                messagebox.showwarning("Failed Login", f"Incorrect password. Attempts left: {3 - fails}")

            cnxn.commit()
            cursor.close()
            cnxn.close()
            return

        # Reset failed attempts
        cursor.execute(
            "UPDATE users SET failed_attempts=0, time_hashed=NULL WHERE username=?",
            (db_user,)
        )
        cnxn.commit()

        # ---------------------------------------------------------
        # ADMIN LICENSE ENFORCEMENT (AFTER PASSWORD VERIFIED)
        # ---------------------------------------------------------
        cursor.execute("SELECT is_main_admin FROM admin_licenses WHERE admin_id = ?", (user_key,))
        admin_license_row = cursor.fetchone()

        if normalize_flag(is_admin) == "Yes":
            if admin_license_row is None:
                # Additional admin with no license → must activate
                from admin_license_activation import AdminLicenseActivationFrame
                messagebox.showinfo(
                    "Admin License Required",
                    "You must activate your Admin Add-on Gumroad license before using the app."
                )
                self.controller.pending_admin_id = user_key
                self.controller.show_frame(AdminLicenseActivationFrame)
                cursor.close()
                cnxn.close()
                return

        # ---------------------------------------------------------
        # STORE SESSION
        # ---------------------------------------------------------
        set_user(
            username,
            user_key,
            company_name,
            "Yes" if normalize_flag(is_admin) else "No",
            None,
            None
        )

        # ---------------------------------------------------------
        # AGREED CHECK
        # ---------------------------------------------------------
        if agreed != "Agreed":
            messagebox.showerror("User did not agree to terms. Goodbye.")
            self.exit_app()
            return

        cursor.close()
        cnxn.close()

        # ---------------------------------------------------------
        # REDIRECTION
        # ---------------------------------------------------------
        self.redirection()

    # ---------------------------------------------------------
    # REDIRECTION
    # ---------------------------------------------------------
    def redirection(self):
        from Admin_Interface import AdminInterfaceFrame
        self.controller.show_frame(AdminInterfaceFrame)

    def exit_app(self):
        self.controller.destroy()


def main():
    pass