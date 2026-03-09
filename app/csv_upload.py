import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd

from db_connection import get_db_connection
from session_context import verify_admin, exit_session, get_user, enforce_plan, get_is_admin
from startup_page import StartPageFrame


class CSVUploadFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.build_ui()

    def on_show(self):
        if not verify_admin():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        if not enforce_plan("pro", "enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            self.controller.show_frame(StartPageFrame)
            return False

        return True

    # ---------------------------------------------------------
    # UI BUILD
    # ---------------------------------------------------------
    def build_ui(self):
        title_label = tk.Label(
            self,
            text="Automating Innovating AI Production Manager App",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=20)

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(pady=20, fill="x")

        buttons = [
            ("Exit", exit_session, "red"),
            ("CSV Instructions", self.show_csv_instructions, "blue"),
            ("Upload Employee CSV", self.open_csv_upload, "brown"),
            ("Admin Interface", self.go_back, "gold"),
        ]

        for text, cmd, color in buttons:
            tk.Button(
                buttons_frame,
                text=text,
                command=cmd,
                font=("Helvetica", 12, "bold"),
                bg=color
            ).pack(side=tk.LEFT, padx=10, pady=10, expand=True, fill="x")

    # ---------------------------------------------------------
    # CSV UPLOAD (PLAIN TEXT — NO ENCRYPTION)
    # ---------------------------------------------------------
    def open_csv_upload(self):
        username = get_user()
        is_admin = get_is_admin()

        if not verify_admin():
            messagebox.showerror("User not authorized.")
            exit_session()
            return

        try:
            filepath = filedialog.askopenfilename(filetypes=[("CSV files", "*.csv")])
            if not filepath:
                return

            df = pd.read_csv(filepath)

            required_columns = [
                "First_Name", "Last_Name", "ID", "Email", "Address", "Apt_Number",
                "City", "State", "Country", "Phone_Number", "Employee_Username",
                "Title", "Is_Admin"
            ]

            missing = set(required_columns) - set(df.columns)
            if missing:
                messagebox.showerror(
                    "Missing Columns",
                    f"The following columns are missing from the CSV: {', '.join(missing)}"
                )
                return

            cnxn = get_db_connection()
            cursor = cnxn.cursor()

            for index, row in df.iterrows():
                values = []

                for column in required_columns:
                    value = row.get(column, "")

                    # Store everything as plain text
                    if value is None:
                        value = ""
                    else:
                        value = str(value)

                    values.append(value)

                cursor.execute(
                    '''
                    INSERT INTO AIAI_Employee_Info (
                        First_Name, Last_Name, ID, Email, Address, Apt_Number, City,
                        State, Country, Phone_Number, Employee_Username, Title, Is_Admin
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    values
                )

            cnxn.commit()
            messagebox.showinfo("CSV Upload Success", "The CSV file has been successfully uploaded.")

        except Exception as e:
            messagebox.showerror("CSV Upload Error", f"An error occurred while uploading the CSV:\n{e}")

    # ---------------------------------------------------------
    # CSV INSTRUCTIONS
    # ---------------------------------------------------------
    def show_csv_instructions(self):
        instructions = (
            "Please prepare your CSV file with the following columns:\n"
            "First_Name, Last_Name, ID, Email, Address, Apt_Number, City, State, Country, "
            "Phone_Number, Employee_Username, Title, Is_Admin\n\n"
            "Example:\n"
            "John, Doe, 12345, john.doe@example.com, 123 Main St, 1A, New York, NY, USA, "
            "555-5555, johndoe, Manager, 1\n"
        )

        instruction_window = tk.Toplevel(self)
        instruction_window.title("CSV Preparation Instructions")

        tk.Label(
            instruction_window,
            text=instructions,
            justify=tk.LEFT,
            padx=10,
            pady=10
        ).pack()

    def go_back(self):
        from Admin_Interface import AdminInterfaceFrame
        self.controller.show_frame(AdminInterfaceFrame)


def main():
    pass