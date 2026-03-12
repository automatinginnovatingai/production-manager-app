import tkinter as tk
from tkinter import ttk, messagebox
import datetime
import re
import uuid
import base64
import os
from Admin_Interface import AdminInterfaceFrame
from startup_page import StartPageFrame
from csv_upload import CSVUploadFrame
from session_context import verify_admin, exit_session, enforce_plan
from db_connection import  get_db_connection
from path_utils import hash_password



# ---------------------------------------------------------
# Utility functions
# ---------------------------------------------------------

def generate_user_key():
    return base64.b64encode(uuid.uuid4().bytes).decode()


states = {
    'Alabama': 'AL', 'Alaska': 'AK', 'Arizona': 'AZ', 'Arkansas': 'AR', 'California': 'CA',
    'Colorado': 'CO', 'Connecticut': 'CT', 'Delaware': 'DE', 'Florida': 'FL', 'Georgia': 'GA',
    'Hawaii': 'HI', 'Idaho': 'ID', 'Illinois': 'IL', 'Indiana': 'IN', 'Iowa': 'IA', 'Kansas': 'KS',
    'Kentucky': 'KY', 'Louisiana': 'LA', 'Maine': 'ME', 'Maryland': 'MD', 'Massachusetts': 'MA',
    'Michigan': 'MI', 'Minnesota': 'MN', 'Mississippi': 'MS', 'Missouri': 'MO', 'Montana': 'MT',
    'Nebraska': 'NE', 'Nevada': 'NV', 'New Hampshire': 'NH', 'New Jersey': 'NJ', 'New Mexico': 'NM',
    'New York': 'NY', 'North Carolina': 'NC', 'North Dakota': 'ND', 'Ohio': 'OH', 'Oklahoma': 'OK',
    'Oregon': 'OR', 'Pennsylvania': 'PA', 'Rhode Island': 'RI', 'South Carolina': 'SC',
    'South Dakota': 'SD', 'Tennessee': 'TN', 'Texas': 'TX', 'Utah': 'UT', 'Vermont': 'VT',
    'Virginia': 'VA', 'Washington': 'WA', 'West Virginia': 'WV', 'Wisconsin': 'WI', 'Wyoming': 'WY'
}

abbrev_to_state = {abbr: state for state, abbr in states.items()}


def validate_zip_code(zip_code):
    return bool(re.match(r"^\d{5}(-\d{4})?$", zip_code))


def validate_phone_number(phone_number):
    return bool(re.match(r"^\D*(\d\D*){10,}$", phone_number))


def validate_email(email):
    return bool(re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", email))


def validate_password(password):
    if len(password) <= 8:
        return "Password must be more than 8 characters long."
    if not re.search("[a-z]", password):
        return "Password must contain at least one lowercase letter."
    if not re.search("[A-Z]", password):
        return "Password must contain at least one uppercase letter."
    if not re.search("[0-9]", password):
        return "Password must contain at least one number."
    if not re.search(r'[\W_]', password):
        return "Password must contain at least one special character."
    if re.search(r"\s", password):
        return "Password cannot contain whitespace."
    return None


# ---------------------------------------------------------
# MAIN FRAME CLASS
# ---------------------------------------------------------

class InstallerInfoFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.build_ui()
        self.update_time()

    def on_show(self):
        # ADMIN CHECK
        if not verify_admin():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        # PLAN CHECK
        if not enforce_plan("pro", "enterprise"):
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
            text="Employee Portal",
            font=("Helvetica", 16, "bold")
        )
        employee_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # ---------------------------------------------------------
        # ENTRY WIDGETS (all self.*)
        # ---------------------------------------------------------
        self.employee_first_name_entry = tk.Entry(employee_frame)
        self.employee_middle_name_entry = tk.Entry(employee_frame)
        self.employee_last_name_entry = tk.Entry(employee_frame)
        self.employee_id_entry = tk.Entry(employee_frame)
        self.employee_email_entry = tk.Entry(employee_frame)
        self.employee_password_entry = tk.Entry(employee_frame, show="*")
        self.employee_address_entry = tk.Entry(employee_frame)
        self.employee_apt_number_entry = tk.Entry(employee_frame)
        self.employee_city_entry = tk.Entry(employee_frame)
        self.employee_state_entry = tk.Entry(employee_frame)
        self.employee_zip_code_entry = tk.Entry(employee_frame)
        self.employee_phone_number_entry = tk.Entry(employee_frame)
        self.employee_username_entry = tk.Entry(employee_frame)
        self.employee_title_combobox_entry = ttk.Combobox(
            employee_frame,
            values=[
                "Fiberglass Insulation", "Foam Insulation", "Blow Insulation",
                "Warehouse", "Office", "N/A"
            ]
        )

        self.is_installer_var = tk.BooleanVar()
        self.show_password_var = tk.BooleanVar()

        labels = [
            ("Enter employee's first name:", self.employee_first_name_entry),
            ("Enter employee's middle name:", self.employee_middle_name_entry),
            ("Enter employee's last name:", self.employee_last_name_entry),
            ("Enter employee's ID:", self.employee_id_entry),
            ("Enter employee's email address:", self.employee_email_entry),
            ("Enter employee's password:", self.employee_password_entry),
            ("Enter employee's home address:", self.employee_address_entry),
            ("Enter apt number:", self.employee_apt_number_entry),
            ("Enter city:", self.employee_city_entry),
            ("Enter state:", self.employee_state_entry),
            ("Enter zip code:", self.employee_zip_code_entry),
            ("Enter employee's phone number:", self.employee_phone_number_entry),
            ("Enter employee's username:", self.employee_username_entry),
            ("Select Employee Job Title:", self.employee_title_combobox_entry)
        ]

        for i, (text, entry) in enumerate(labels):
            tk.Label(employee_frame, text=text, anchor="w").grid(
                row=i, column=0, sticky="w", padx=10, pady=5
            )
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

        # Show password checkbox
        tk.Checkbutton(
            employee_frame,
            text="Show Password",
            variable=self.show_password_var,
            command=self.toggle_password
        ).grid(row=5, column=8, pady=5)

        # Installer checkbox
        tk.Checkbutton(
            employee_frame,
            text="Installer",
            variable=self.is_installer_var,
            font=("Arial", 14)
        ).grid(row=len(labels), column=1, padx=10, pady=10, sticky="w")

        # ---------------------------------------------------------
        # Calendar
        # ---------------------------------------------------------
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

        # ---------------------------------------------------------
        # Buttons
        # ---------------------------------------------------------
        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=20, fill="x")

        buttons = [
            ("Exit", exit_session, "red"),
            ("Admin Interface", lambda: self.controller.show_frame(AdminInterfaceFrame), "blue"),
            ("Upload Employee CSV", lambda: self.controller.show_frame(CSVUploadFrame), "brown"),
            ("Save", self.installer_data, "green"),
            ("Clear Form", self.clear_inputs, "yellow")
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
    # TIME UPDATE
    # ---------------------------------------------------------
    def update_time(self):
        now = datetime.datetime.now()
        self.time_frame.config(text=now.strftime("%H:%M:%S"))
        self.date_frame.config(text=now.strftime("%m/%d/%Y"))
        self.after(1000, self.update_time)

    # ---------------------------------------------------------
    # PASSWORD VISIBILITY
    # ---------------------------------------------------------
    def toggle_password(self):
        if self.show_password_var.get():
            self.employee_password_entry.config(show="")
        else:
            self.employee_password_entry.config(show="*")

    # ---------------------------------------------------------
    # CLEAR INPUTS
    # ---------------------------------------------------------
    def clear_inputs(self):
        for entry in [
            self.employee_first_name_entry,
            self.employee_middle_name_entry,
            self.employee_last_name_entry,
            self.employee_id_entry,
            self.employee_email_entry,
            self.employee_password_entry,
            self.employee_address_entry,
            self.employee_apt_number_entry,
            self.employee_city_entry,
            self.employee_state_entry,
            self.employee_zip_code_entry,
            self.employee_phone_number_entry,
            self.employee_username_entry,
            self.employee_title_combobox_entry
        ]:
            entry.delete(0, tk.END)

        self.is_installer_var.set(0)

    # ---------------------------------------------------------
    # VALIDATE ENTRIES
    # ---------------------------------------------------------
    def validate_entries(self):
        entries = [
            self.employee_first_name_entry.get(),
            self.employee_middle_name_entry.get(),
            self.employee_last_name_entry.get(),
            self.employee_id_entry.get(),
            self.employee_email_entry.get(),
            self.employee_password_entry.get(),
            self.employee_address_entry.get(),
            self.employee_apt_number_entry.get(),
            self.employee_city_entry.get(),
            self.employee_state_entry.get(),
            self.employee_zip_code_entry.get(),
            self.employee_phone_number_entry.get(),
            self.employee_username_entry.get(),
            self.employee_title_combobox_entry.get()
        ]

        for entry in entries:
            if not entry:
                messagebox.showerror("Input Error", "All fields must be filled out.")
                return False

        return True

    # ---------------------------------------------------------
    # INSERT INSTALLER DATA
    # ---------------------------------------------------------
    def insert_installer_data(self, data):

        password = data["password"]
        state = data["State"]
        zip_code = data["Zip_Code"]
        phone = data["Phone_Number"]
        email = data["Email"]

        # Validate password
        pw_error = validate_password(password)
        if pw_error:
            messagebox.showerror("Error", pw_error)
            return

        # Validate state
        if state not in states and state not in abbrev_to_state:
            messagebox.showerror("Invalid Input", "Invalid state name or abbreviation.")
            return

        # Validate ZIP
        if not validate_zip_code(zip_code):
            messagebox.showerror("Invalid Input", "Invalid ZIP code.")
            return

        # Validate phone
        if not validate_phone_number(phone):
            messagebox.showerror("Invalid Input", "Invalid phone number.")
            return

        # Validate email
        if not validate_email(email):
            messagebox.showerror("Invalid Input", "Invalid email address.")
            return

        # Generate keys
        license_key = str(uuid.uuid4())
        verification_key = str(uuid.uuid4())
        user_key = str(uuid.uuid4())

        is_installer = str(bool(self.is_installer_var.get()))
        stored_is_installer = "Yes" if self.is_installer_var.get() else "No"


        try:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute(
                '''
                INSERT INTO AIAI_Employee_Info
                (user_key, First_Name, Middle_Name, Last_Name, ID, Email, Employee_Password,
                 Address, Apt_Number, City, State, Zip_Code, Phone_Number, Employee_Username,
                 Title, is_installer, license_key, verification_key)
                VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                ''',
                (
                    user_key,
                    data["First_Name"],
                    data["Middle_Name"],
                    data["Last_Name"],
                    data["ID"],
                    data["Email"],
                    hash_password(data["password"]),
                    data["Address"],
                    data["Apt_Number"],
                    data["City"],
                    data["State"],
                    data["Zip_Code"],
                    data["Phone_Number"],
                    data["Employee_Username"],
                    data["Title"],
                    stored_is_installer,
                    license_key,
                    verification_key
                )
            )
            conn.commit()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")       

    # ---------------------------------------------------------
    # SAVE INSTALLER DATA
    # ---------------------------------------------------------
    def installer_data(self):
        if not self.validate_entries():
            return

        data = {
            "First_Name": self.employee_first_name_entry.get(),
            "Middle_Name": self.employee_middle_name_entry.get(),
            "Last_Name": self.employee_last_name_entry.get(),
            "ID": self.employee_id_entry.get(),
            "Email": self.employee_email_entry.get(),
            "Address": self.employee_address_entry.get(),
            "Apt_Number": self.employee_apt_number_entry.get(),
            "City": self.employee_city_entry.get(),
            "State": self.employee_state_entry.get(),
            "Zip_Code": self.employee_zip_code_entry.get(),
            "Phone_Number": self.employee_phone_number_entry.get(),
            "Employee_Username": self.employee_username_entry.get(),
            "password": self.employee_password_entry.get(),
            "Title": self.employee_title_combobox_entry.get(),
            "is_installer": "1" if self.is_installer_var.get() else "0"
        }

        self.insert_installer_data(data)
        messagebox.showinfo("Registration", "Installer Data Entered and Encrypted Successfully!")
        self.clear_inputs()

def main():
    pass