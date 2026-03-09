import tkinter as tk
from tkinter import messagebox, BooleanVar
import time
from Installer_Interface import InstallerInterfaceFrame
from db_connection import get_db_connection
from session_context import set_installer, exit_session
from path_utils import verify_password

class InstallerLoginFrame(tk.Frame):
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
        ).grid(row=4, column=2)

        tk.Button(
            frame,
            text="Sign In",
            font=("Helvetica", 12, "bold"),
            bg="green",
            command=self.build_signin
        ).grid(row=0, column=2, padx=20, pady=20)

        tk.Button(
            frame,
            text="Exit",
            font=("Helvetica", 12, "bold"),
            bg="red",
            command=exit_session
        ).grid(row=2, column=2, padx=20, pady=20)

        tk.Label(
            frame,
            text="Installer Login Page",
            font=("Helvetica", 32, "bold")
        ).grid(row=5, column=2)

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

        password_entry = tk.Entry(frame, textvariable=self.password_var, show="*")
        password_entry.grid(row=2, column=1, padx=5)

        show_pw_var = BooleanVar()
        tk.Checkbutton(
            frame,
            text="Show Password",
            variable=show_pw_var,
            command=lambda: self.toggle_password(password_entry, show_pw_var)
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
            command=self.reset_password
        ).grid(row=6, column=0, columnspan=3, pady=10)

        tk.Button(
            frame,
            text="Exit",
            font="bold",
            bg="red",
            command=exit_session
        ).grid(row=8, column=0, columnspan=3, pady=10)

    # ---------------------------------------------------------
    # PASSWORD VISIBILITY
    # ---------------------------------------------------------
    def toggle_password(self, entry, var):
        entry.config(show="" if var.get() else "*")

    # ---------------------------------------------------------
    # RESET PASSWORD SCREEN
    # ---------------------------------------------------------
    def reset_password(self):
        win = tk.Toplevel(self)
        win.title("Reset Password")
        win.attributes("-fullscreen", True)

        frame = tk.Frame(win)
        frame.pack(expand=True, fill="both")

        for i in range(20):
            frame.grid_rowconfigure(i, weight=1)
            frame.grid_columnconfigure(i, weight=1)

        tk.Label(
            frame,
            text="See authorized user to reset password. Goodbye.",
            font=("Helvetica", 32, "bold")
        ).grid(row=10, column=10, sticky="nsew")

        win.after(2000, exit_session)

    # ---------------------------------------------------------
    # LOGIN LOGIC
    # ---------------------------------------------------------
    def login_user(self):
        username = self.username_var.get().strip()
        password = self.password_var.get().strip()

        cnxn = get_db_connection()
        cursor = cnxn.cursor()

        cursor.execute("""
            SELECT user_key, Employee_Username, Employee_Password,
                is_installer, salt, failed_attempts, time_hashed,
                gumroad_license_key
            FROM AIAI_Employee_Info
        """)

        found = None
        for user_key, db_user, db_pw, is_installer, salt, fails, time_hash, gumroad_key in cursor.fetchall():
            if username == db_user:
                found = (db_user, db_pw, fails, time_hash, user_key, is_installer, salt, gumroad_key)
                break

        if not found:
            cnxn.close()
            messagebox.showerror("Error", "Username not found.")
            return

        db_user, stored_pw, fails, time_hash, user_key, is_installer, salt, gumroad_key = found        
        now = int(time.time())

         # ---------------------------------------------------------
        # FETCH LICENSE INFO FOR THIS USER
        # ---------------------------------------------------------
        cursor.execute("""
            SELECT id, plan
            FROM license_store
           
        """)

        row = cursor.fetchone()

        if not row:
            cnxn.close()
            messagebox.showerror("Error", "No license found for this user.")
            return

        license_id, subscription_plan = row

        if time_hash and now - int(time_hash) < 300:
            messagebox.showwarning("Locked Out", "Too many failed attempts. Wait 5 minutes.")
            cursor.execute(
                "UPDATE AIAI_Employee_Info SET failed_attempts=0, time_hashed=NULL WHERE Employee_Username=?",
                (db_user,)
            )
            cnxn.commit()
            cnxn.close()
            return

        if verify_password(password, stored_pw):

            # -----------------------------------------
            # REQUIRE INSTALLER TO HAVE A LICENSE
            # -----------------------------------------
            if not gumroad_key:
                messagebox.showerror("License Missing", "No Gumroad license found for this installer.")
                cnxn.close()
                return

            # -----------------------------------------
            # FETCH GUMROAD LICENSE KEY
            # -----------------------------------------
            try:
                license_key = gumroad_key
            except Exception:
                messagebox.showerror("Error", "Installer license key is corrupted.")
                cnxn.close()
                return

            # -----------------------------------------
            # VERIFY LICENSE WITH GUMROAD
            # -----------------------------------------
            import license_validator  # safe import

            response = license_validator.gumroad_verify(license_key)
            
            if not response or not response.get("success"):
                messagebox.showerror("Invalid License", "Installer Gumroad license is invalid or revoked.")
                cnxn.close()
                return

            # -----------------------------------------
            # LOGIN SUCCESSFUL
            # -----------------------------------------
            messagebox.showinfo("Login Successful", "Login successful.")
            set_installer(username, user_key, salt, is_installer, license_id, subscription_plan)
            self.controller.show_frame(InstallerInterfaceFrame)

            self.username_var.set("")
            self.password_var.set("")
        else:
            fails = (fails or 0) + 1

            if fails >= 3:
                cursor.execute(
                    "UPDATE AIAI_Employee_Info SET failed_attempts=?, time_hashed=? WHERE Employee_Username=?",
                    (fails, str(now), db_user)
                )
                messagebox.showwarning("Locked Out", "Too many failed attempts. Wait 5 minutes.")
                exit_session()
            else:
                cursor.execute(
                    "UPDATE AIAI_Employee_Info SET failed_attempts=? WHERE Employee_Username=?",
                    (fails, db_user)
                )
                messagebox.showwarning("Failed Login", f"Incorrect password. Attempts left: {3 - fails}")

            cnxn.commit()

        cursor.close()
        cnxn.close()



def main():
    pass