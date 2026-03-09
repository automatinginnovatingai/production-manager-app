import os
import tkinter as tk
from tkinter import messagebox
from cryptography.fernet import Fernet
from openpyxl import Workbook, load_workbook
from datetime import datetime
from db_connection import get_db_connection
from session_context import (
    verify_installer,
    enforce_installer_plan,
    get_user_key,
    get_user,
    exit_session
)

class CSV_ViewFrame(tk.Frame):

    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

    def on_show(self, event=None):
        # 1 — Verify installer integrity
        if not verify_installer():
            messagebox.showerror("Security Error", "Installer verification failed.")
            exit_session()
            return

        # 2 — Enforce plan (Pro or Enterprise only)
        if not enforce_installer_plan("enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            from startup_page import StartPageFrame
            self.controller.show_frame(StartPageFrame)

        # Scrollable text widget
        self.text_widget = tk.Text(
            self,
            wrap="word",
            font=("Segoe UI", 10),
            padx=10,
            pady=10
        )
        self.scrollbar = tk.Scrollbar(self, command=self.text_widget.yview)
        self.text_widget.configure(yscrollcommand=self.scrollbar.set)

        self.text_widget.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

        # Load data immediately when frame is shown
        self.bind("<Visibility>", self.on_show)

        # Exit button
        exit_btn = tk.Button(
            self,
            text="Exit",
            font=("Segoe UI", 10, "bold"),
            command=exit_session,
            bg="#cc0000",
            fg="white",
            padx=10,
            pady=5
        )
        exit_btn.pack(side="bottom", anchor="e", pady=10, padx=10)

    # ----------------------------------------------------------------------
    # LOAD DATA WHEN FRAME BECOMES VISIBLE
    # ----------------------------------------------------------------------
   

        # 3 — Continue with normal behavior
        self.text_widget.delete("1.0", "end")
        self.display_report()

    # ----------------------------------------------------------------------
    # MAIN LOGIC
    # ----------------------------------------------------------------------
    def display_report(self):
        username = get_user()

        cnxn = get_db_connection()
        with cnxn as conn:
            cursor = conn.cursor()

            # STEP 1 — Identify logged-in user via AIAI_Employee_Info (plain text)
            cursor.execute("""
                SELECT ID
                FROM AIAI_Employee_Info
                WHERE Employee_Username = ?
            """, (username,))

            user_info = cursor.fetchone()
            if not user_info:
                messagebox.showerror("Access Denied", "User profile not found.")
                return

            employee_id = user_info[0]  # plain text ID

            # STEP 2 — Fetch payroll rows for this employee only (plain text)
            cursor.execute("""
                SELECT *
                FROM AIAI_Employee_Weekly_Payroll
                WHERE Employee_ID = ?
            """, (employee_id,))
            data = cursor.fetchall()

            if not data:
                messagebox.showerror("Access Denied", "No records found for this user.")
                return

            # STEP 3 — Fetch column metadata
            cursor.execute("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = 'AIAI_Employee_Weekly_Payroll'
            """)
            columns = [col[0] for col in cursor.fetchall()]
            column_indices = {column: index for index, column in enumerate(columns)}

            # STEP 4 — Fetch pay week ranges
            cursor.execute("SELECT start_date, end_date FROM pay_week")
            pay_weeks_raw = cursor.fetchall()

        # Convert pay week ranges to Python date objects
        pay_weeks = []
        for start, end in pay_weeks_raw:
            try:
                s = datetime.strptime(start, "%m/%d/%Y").date()
                e = datetime.strptime(end, "%m/%d/%Y").date()
                pay_weeks.append((s, e))
            except:
                continue

        # ------------------------------------------------------------------
        # REQUIRED: Your exact original column order
        # ------------------------------------------------------------------
        column_order = [
            "First_Name", "Last_Name", "ID",
            "MM_DD_YYYY", "Day_of_Week",
            "Employee_Job_Title", "Builder", "Jobsite", "Model_Name",
            "Employee_Hours", "total_pay",
            "Pay_Per_Employee", "Split_Pay_Per_Employee",

            "Material_Used_1", "R_Value_1", "Material_Width_1", "Sqft_Bags_Installed_1",
            "Pay_Per_Tube_Piece_Rate_1", "Pay_1",

            "Material_Used_2", "R_Value_2", "Material_Width_2", "Sqft_Bags_Installed_2",
            "Pay_Per_Tube_Piece_Rate_2", "Pay_2",

            "Material_Used_3", "R_Value_3", "Material_Width_3", "Sqft_Bags_Installed_3",
            "Pay_Per_Tube_Piece_Rate_3", "Pay_3",

            "Material_Used_4", "R_Value_4", "Material_Width_4", "Sqft_Bags_Installed_4",
            "Pay_Per_Tube_Piece_Rate_4", "Pay_4",

            "Material_Used_5", "R_Value_5", "Material_Width_5", "Sqft_Bags_Installed_5",
            "Pay_Per_Tube_Piece_Rate_5", "Pay_5",

            "Material_Used_6", "R_Value_6", "Material_Width_6", "Sqft_Bags_Installed_6",
            "Pay_Per_Tube_Piece_Rate_6", "Pay_6",

            "Material_Used_7", "R_Value_7", "Material_Width_7", "Sqft_Bags_Installed_7",
            "Pay_Per_Tube_Piece_Rate_7", "Pay_7",
        ]

        # ------------------------------------------------------------------
        # GROUPING LOGIC (plain text)
        # ------------------------------------------------------------------
        groups = {}

        for row in data:
            # Build a plain-text dictionary for the row
            decrypted = {}
            for col in column_order:
                if col not in columns:
                    decrypted[col] = ""
                    continue

                raw_value = row[column_indices[col]]
                decrypted[col] = raw_value if raw_value is not None else ""

            # Determine row date
            date_str = decrypted.get("MM_DD_YYYY", "")
            try:
                row_date = datetime.strptime(date_str, "%m/%d/%Y").date()
            except:
                row_date = None

            # Determine group label
            if row_date:
                group_label = None

                # Check pay week ranges
                for s, e in pay_weeks:
                    if s <= row_date <= e:
                        group_label = f"Pay Week: {s.strftime('%m/%d/%Y')} – {e.strftime('%m/%d/%Y')}"
                        break

                # Fallback to month grouping
                if not group_label:
                    group_label = row_date.strftime("%B %Y")
            else:
                group_label = "Unknown Date"

            # Add to group
            groups.setdefault(group_label, []).append(decrypted)

        # At this point, `groups` is ready for rendering in your UI
        self.render_grouped_report(groups)
        # ------------------------------------------------------------------
        # SORT GROUPS BY DATE
        # ------------------------------------------------------------------
        def group_sort_key(label):
            if label.startswith("Pay Week:"):
                dates = label.replace("Pay Week: ", "").split(" – ")
                return datetime.strptime(dates[0], "%m/%d/%Y")
            else:
                return datetime.strptime(label, "%B %Y")

        # ------------------------------------------------------------------
        # DISPLAY GROUPED REPORT
        # ------------------------------------------------------------------
        self.text_widget.insert("end", f"{'='*40} Payroll Report {'='*40}\n\n")

        for group_label in sorted(groups.keys(), key=group_sort_key):

            self.text_widget.insert("end", f"\n=== {group_label} ===\n\n")

            # DAILY + WEEKLY + MONTHLY totals
            weekly_hours = 0.0
            weekly_pay = 0.0

            monthly_hours = 0.0
            monthly_pay = 0.0

            # Group entries by date inside this group
            date_groups = {}

            for decrypted in groups[group_label]:
                date_str = decrypted.get("MM_DD_YYYY", "")
                try:
                    d = datetime.strptime(date_str, "%m/%d/%Y").date()
                except:
                    d = "Unknown"

                date_groups.setdefault(d, []).append(decrypted)

            # Sort dates inside group
            sorted_dates = sorted(
                date_groups.keys(),
                key=lambda d: d if isinstance(d, datetime.date) else datetime.min.date()
            )

            for d in sorted_dates:
                entries = date_groups[d]

                if isinstance(d, datetime.date):
                    date_label = f"{d.strftime('%m/%d/%Y')} ({entries[0].get('Day_of_Week', '')})"
                else:
                    date_label = "Unknown Date"

                self.text_widget.insert("end", f"{date_label}\n")

                daily_hours = 0.0
                daily_pay = 0.0

                for decrypted in entries:

                    # Convert numeric fields
                    hours = float(decrypted.get("Employee_Hours", 0))
                    pay = float(decrypted.get("Pay_Per_Employee", 0))

                    daily_hours += hours
                    daily_pay += pay

                    weekly_hours += hours
                    weekly_pay += pay

                    monthly_hours += hours
                    monthly_pay += pay

                    # Display entry
                    self.text_widget.insert("end",
                        f"   👷 {decrypted.get('First_Name', '')} {decrypted.get('Last_Name', '')} "
                        f"(ID: {decrypted.get('ID', '')})\n"
                    )
                    self.text_widget.insert("end",
                        f"      Job: {decrypted.get('Employee_Job_Title', '')} | "
                        f"Builder: {decrypted.get('Builder', '')} | "
                        f"Jobsite: {decrypted.get('Jobsite', '')} | "
                        f"Model: {decrypted.get('Model_Name', '')}\n"
                    )
                    self.text_widget.insert("end",
                        f"      Hours: {hours} | Pay (Employee): ${pay}\n"
                    )

                # DAILY TOTALS
                self.text_widget.insert("end",
                    f"   ➤ Daily Total Hours: {daily_hours}\n"
                )
                self.text_widget.insert("end",
                    f"   ➤ Daily Total Pay: ${daily_pay}\n\n"
                )

            # WEEKLY TOTALS (only for pay-week groups)
            if group_label.startswith("Pay Week:"):
                self.text_widget.insert("end",
                    f"➤ WEEKLY TOTAL HOURS: {weekly_hours}\n"
                )
                self.text_widget.insert("end",
                    f"➤ WEEKLY TOTAL PAY: ${weekly_pay}\n\n"
                )

            # MONTHLY TOTALS (only for month groups)
            if not group_label.startswith("Pay Week:"):
                self.text_widget.insert("end",
                    f"➤ MONTHLY TOTAL HOURS: {monthly_hours}\n"
                )
                self.text_widget.insert("end",
                    f"➤ MONTHLY TOTAL PAY: ${monthly_pay}\n\n"
                )

        self.text_widget.insert("end", f"{'='*40} End of Report {'='*40}\n")
        cnxn.close()