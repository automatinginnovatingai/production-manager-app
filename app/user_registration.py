import os
import re
import uuid
import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime, date
import sys

from session_context import set_user, clear_user, normalize_flag
from db_connection import get_db_connection
from path_utils import (
    hash_password,
    hash_pin,
)

# ------------------ VALIDATION HELPERS ------------------

def check_username(username):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT 1 FROM users WHERE username = ?", (username,))
    result = cursor.fetchone()
    conn.close()
    return result is not None


def is_first_admin():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM users WHERE is_admin = 'Yes'")
    count = cursor.fetchone()[0]
    conn.close()
    return count == 0


def validate_phone_number(phone_number):
    pattern = re.compile(r"^\D*(\d\D*){10,}$")
    return bool(pattern.match(phone_number))


def validate_password(password):
    if len(password) <= 8:
        return "Password must be more than 8 characters long."
    if not re.search("[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search("[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search("[0-9]", password):
        return "Password must contain at least one number."
    if not re.search(r"[\W_]", password):
        return "Password must contain at least one special character."
    if re.search(r"\s", password):
        return "Password cannot contain any whitespace."
    return None


def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ------------------ MAIN FRAME ------------------

class UserRegistrationFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.register_username_entry = None
        self.register_password_entry = None
        self.register_first_name_entry = None
        self.register_last_name_entry = None
        self.register_phone_entry = None
        self.register_company_entry = None
        self.register_pin_entry = None

        self.show_password_var = tk.BooleanVar()
        self.show_pin_var = tk.BooleanVar()
        self.is_admin_var = tk.StringVar()

        self.build_ui()

    # ------------------ UI ------------------

    def build_ui(self):
        title_label = tk.Label(
            self,
            text="Automating Innovating AI Production Manager",
            font=("Arial", 24, "bold"),
        )
        title_label.pack(pady=20)

        frame = tk.Frame(self)
        frame.pack()

        # --- Fields ---
        tk.Label(frame, text="Username:").grid(row=0, column=0, pady=5)
        self.register_username_entry = tk.Entry(frame)
        self.register_username_entry.grid(row=0, column=1, pady=5)

        tk.Label(frame, text="Password:").grid(row=1, column=0, pady=5)
        self.register_password_entry = tk.Entry(frame, show="*")
        self.register_password_entry.grid(row=1, column=1, pady=5)

        tk.Label(frame, text="First Name:").grid(row=2, column=0, pady=5)
        self.register_first_name_entry = tk.Entry(frame)
        self.register_first_name_entry.grid(row=2, column=1, pady=5)

        tk.Label(frame, text="Last Name:").grid(row=3, column=0, pady=5)
        self.register_last_name_entry = tk.Entry(frame)
        self.register_last_name_entry.grid(row=3, column=1, pady=5)

        tk.Label(frame, text="Mobile Number:").grid(row=4, column=0, pady=5)
        self.register_phone_entry = tk.Entry(frame)
        self.register_phone_entry.grid(row=4, column=1, pady=5)

        tk.Label(frame, text="Company Name:").grid(row=5, column=0, pady=5)
        self.register_company_entry = tk.Entry(frame)
        self.register_company_entry.grid(row=5, column=1, pady=5)

        tk.Label(frame, text="Pin:").grid(row=6, column=0, pady=5)
        self.register_pin_entry = tk.Entry(frame, show="*")
        self.register_pin_entry.grid(row=6, column=1, pady=5)

        # --- Admin selection ---
        tk.Label(frame, text="Admin Authorization:", font=("Arial", 14)).grid(row=8, column=0, pady=5)

        self.is_admin_combo = ttk.Combobox(
            frame,
            textvariable=self.is_admin_var,
            values=["Yes", "No"],
            state="readonly",
            width=10
        )
        self.is_admin_combo.grid(row=8, column=1, pady=5)
        self.is_admin_combo.bind("<<ComboboxSelected>>", self.on_admin_selection)
        self.is_admin_combo.set("No")

        # --- Buttons ---
        tk.Button(frame, text="Register", command=self.register_user, bg="green").grid(row=9, column=1, pady=10)
        tk.Button(frame, text="Back", command=self.back, bg="yellow").grid(row=10, column=1, pady=10)
        tk.Button(frame, text="Exit", command=self.exit, bg="red").grid(row=11, column=1, pady=10)

    # ------------------ UI Helpers ------------------

    def toggle_password(self):
        self.register_password_entry.config(show="" if self.show_password_var.get() else "*")

    def toggle_pin(self):
        self.register_pin_entry.config(show="" if self.show_pin_var.get() else "*")

    def on_admin_selection(self, event=None):
        if self.is_admin_var.get() == "No":
            messagebox.showerror("Admin Required", "You must be an Admin to move forward.")
            self.is_admin_combo.set("Yes")

    def clear_inputs(self):
        self.register_username_entry.delete(0, tk.END)
        self.register_password_entry.delete(0, tk.END)
        self.register_first_name_entry.delete(0, tk.END)
        self.register_last_name_entry.delete(0, tk.END)
        self.register_phone_entry.delete(0, tk.END)
        self.register_company_entry.delete(0, tk.END)
        self.register_pin_entry.delete(0, tk.END)
        self.is_admin_var.set("No")

    def run_next_file(self):
        from terms_conditions import TermsConditionsFrame
        self.controller.show_frame(TermsConditionsFrame)

    def back(self):
        from startup_page import StartPageFrame
        self.controller.show_frame(StartPageFrame)

    def exit(self):
        self.controller.exit_session()

    # ------------------ REGISTRATION LOGIC ------------------

    def register_user(self):
        username = self.register_username_entry.get()
        password = self.register_password_entry.get()
        first_name = self.register_first_name_entry.get()
        last_name = self.register_last_name_entry.get()
        phone_number = self.register_phone_entry.get()
        company_name = self.register_company_entry.get()
        pin = self.register_pin_entry.get()
        is_admin = self.is_admin_var.get()

        # --- Validation ---
        if check_username(username):
            messagebox.showerror("Error", "Username already in use.\nPlease try again.")
            return

        if not (6 <= len(pin) <= 8):
            messagebox.showwarning("Invalid PIN", "PIN must be 6 to 8 digits long.")
            return

        if not validate_phone_number(phone_number):
            messagebox.showerror("Invalid Input", "Please enter a valid phone number with at least 10 digits.")
            return

        password_error = validate_password(password)
        if password_error:
            messagebox.showerror("Error", password_error)
            return

        # --- Prepare data ---
        user_key = str(uuid.uuid4())
        hashed_password = hash_password(password)
        hashed_pin_value = hash_pin(pin)

        conn = None
        try:
            conn = get_db_connection()
            cursor = conn.cursor()

            # ------------------ INSERT USER ------------------
            cursor.execute("""
                INSERT INTO users (
                    user_key, username, password, first_name, last_name,
                    phone_number, company_name, pin, is_admin
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                user_key,
                username,
                hashed_password,
                first_name,
                last_name,
                phone_number,
                company_name,
                hashed_pin_value,
                is_admin
            ))
            conn.commit()

            # ------------------ MAIN ADMIN LICENSE ------------------
            first_admin = is_first_admin()
            if is_admin == "Yes" and first_admin:
                license_hash = self.controller.company_license_hash
                plan_type = self.controller.company_plan_type

                cursor.execute("""
                    INSERT INTO admin_licenses (admin_id, license_hash, plan_type, is_main_admin)
                    VALUES (?, ?, ?, 1)
                """, (
                    user_key,
                    license_hash,
                    plan_type
                ))
                conn.commit()

            # ------------------ SUCCESS ------------------
            messagebox.showinfo("User Sign up", "Sign up successful.")
            self.clear_inputs()

            # Determine if this is the first admin BEFORE inserting license
            first_admin = (is_admin == "Yes" and is_first_admin())

            # MAIN ADMIN → create session + continue to Terms
            if first_admin:
                set_user(
                    username,
                    user_key,
                    company_name,
                    "Yes",
                    None,
                    None
                )
                self.run_next_file()
                return

            # ADDITIONAL ADMIN → NO SESSION, redirect to login
            messagebox.showinfo(
                "Registration Complete",
                "Your admin account has been created.\n\n"
                "Please log in to activate your Admin Add‑on license."
            )

            from user_login import UserLoginFrame
            self.controller.show_frame(UserLoginFrame)
            return

        except Exception as e:
            messagebox.showerror("Error", f"Unexpected error during registration:\n{str(e)}")
            clear_user()

        finally:
            if conn:
                conn.close()