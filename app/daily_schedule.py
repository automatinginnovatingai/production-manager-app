import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
import datetime
import calendar
from session_context import exit_session, verify_admin, enforce_plan
from db_connection import get_db_connection
from Admin_Interface import AdminInterfaceFrame
from startup_page import StartPageFrame


class EmployeeTicketFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        controller.title("Automating Innovating AI - Employee Work Schedule")

        # --------------------------------------------------------------
        # MAIN FRAME
        # --------------------------------------------------------------
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(2, weight=1)
        for col in range(7):
            frame.grid_columnconfigure(col, weight=1)

        # --------------------------------------------------------------
        # DATE SELECTION AREA
        # --------------------------------------------------------------
        date_frame = tk.Frame(frame)
        date_frame.grid(row=0, column=0, columnspan=7, pady=10)

        tk.Label(date_frame, text="Select Date:", font=("Arial", 12, "bold")).grid(row=0, column=0, padx=5)

        self.date_entry = DateEntry(
            date_frame,
            width=12,
            background="darkblue",
            foreground="white",
            borderwidth=2,
            date_pattern="mm/dd/yyyy"
        )
        self.date_entry.grid(row=0, column=1, padx=5)

        ttk.Button(date_frame, text="Load Daily", command=self.load_daily_schedule).grid(row=0, column=2, padx=10)
        ttk.Button(date_frame, text="◀ Prev", command=self.previous_day).grid(row=0, column=3, padx=5)
        ttk.Button(date_frame, text="Next ▶", command=self.next_day).grid(row=0, column=4, padx=5)

        # --------------------------------------------------------------
        # FILTERS & REPORT BUTTONS
        # --------------------------------------------------------------
        filter_frame = tk.Frame(frame)
        filter_frame.grid(row=1, column=0, columnspan=7, pady=5)

        ttk.Button(filter_frame, text="Weekly View", command=self.load_weekly_schedule).grid(row=0, column=0, padx=10)
        ttk.Button(filter_frame, text="Monthly View", command=self.load_monthly_schedule).grid(row=0, column=1, padx=10)

        # Employee filter
        tk.Label(filter_frame, text="Employee ID:", font=("Arial", 10)).grid(row=0, column=2, padx=5)
        self.emp_filter_var = tk.StringVar()
        ttk.Entry(filter_frame, textvariable=self.emp_filter_var, width=10).grid(row=0, column=3, padx=5)
        ttk.Button(filter_frame, text="Filter", command=self.filter_by_employee).grid(row=0, column=4, padx=10)

        # Reports button (PDF / Excel / Print handled in separate file)
        ttk.Button(filter_frame, text="Reports", command=self.open_reports_window).grid(row=0, column=5, padx=20)

        # --------------------------------------------------------------
        # RESULTS AREA (SCROLLABLE)
        # --------------------------------------------------------------
        results_frame = tk.Frame(frame)
        results_frame.grid(row=2, column=0, columnspan=7, sticky="nsew")

        self.canvas = tk.Canvas(results_frame)
        self.scrollbar = ttk.Scrollbar(results_frame, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all"))
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scrollbar.pack(side="right", fill="y")

    # ----------------------------------------------------------------------
    # ADMIN INTERFACE
    # ----------------------------------------------------------------------
    def admin_interface(self):
        self.controller.show_frame(AdminInterfaceFrame)

    # ----------------------------------------------------------------------
    # EXIT
    # ----------------------------------------------------------------------
    def exit_button(self):
        self.controller.destroy()

    # ----------------------------------------------------------------------
    # PAGE SHOW LOGIC
    # ----------------------------------------------------------------------
    def on_show(self):
        if not verify_admin():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        if not enforce_plan("basic", "pro", "enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            self.controller.show_frame(StartPageFrame)
            return False

        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

    # ----------------------------------------------------------------------
    # DATE NAVIGATION
    # ----------------------------------------------------------------------
    def previous_day(self):
        current = datetime.datetime.strptime(self.date_entry.get(), "%m/%d/%Y")
        new_date = current - datetime.timedelta(days=1)
        self.date_entry.set_date(new_date)
        self.load_daily_schedule()

    def next_day(self):
        current = datetime.datetime.strptime(self.date_entry.get(), "%m/%d/%Y")
        new_date = current + datetime.timedelta(days=1)
        self.date_entry.set_date(new_date)
        self.load_daily_schedule()

    # ----------------------------------------------------------------------
    # DAILY SCHEDULE
    # ----------------------------------------------------------------------
    def load_daily_schedule(self):
        date = self.date_entry.get()
        query = """
            SELECT First_Name, Last_Name, Employee_ID,
                   Employee_Hours, Employee_Job_Title,
                   Builder, Jobsite, Model_Name, Lot_Number, Block_Number,
                   Material_Used, Material_Used_2, Material_Used_3, Material_Used_4,
                   Material_Used_5, Material_Used_6, Material_Used_7,
                   Pay_Per_Employee
            FROM AIAI_Employee_Work_Ticket
            WHERE MM_DD_YYYY = ?
        """
        self.run_query_and_display(query, (date,), f"No work tickets found for {date}.")
        self.last_report_title = f"Daily Schedule - {date}"

    # ----------------------------------------------------------------------
    # WEEKLY SCHEDULE
    # ----------------------------------------------------------------------
    def load_weekly_schedule(self):
        selected = datetime.datetime.strptime(self.date_entry.get(), "%m/%d/%Y")
        week_start = selected - datetime.timedelta(days=selected.weekday())
        week_end = week_start + datetime.timedelta(days=6)

        query = """
            SELECT *
            FROM AIAI_Employee_Work_Ticket
            WHERE MM_DD_YYYY BETWEEN ? AND ?
        """
        self.run_query_and_display(
            query,
            (week_start.strftime("%m/%d/%Y"), week_end.strftime("%m/%d/%Y")),
            "No work tickets found for this week."
        )
        self.last_report_title = f"Weekly Schedule ({week_start.strftime('%m/%d/%Y')} - {week_end.strftime('%m/%d/%Y')})"

    # ----------------------------------------------------------------------
    # MONTHLY SCHEDULE
    # ----------------------------------------------------------------------
    def load_monthly_schedule(self):
        selected = datetime.datetime.strptime(self.date_entry.get(), "%m/%d/%Y")
        month = selected.month
        year = selected.year

        query = """
            SELECT *
            FROM AIAI_Employee_Work_Ticket
            WHERE MONTH(CONVERT(date, MM_DD_YYYY, 101)) = ?
              AND YEAR(CONVERT(date, MM_DD_YYYY, 101)) = ?
        """
        self.run_query_and_display(query, (month, year), "No work tickets found for this month.")
        self.last_report_title = f"Monthly Schedule ({month}/{year})"

    # ----------------------------------------------------------------------
    # FILTER BY EMPLOYEE
    # ----------------------------------------------------------------------
    def filter_by_employee(self):
        emp_id = self.emp_filter_var.get().strip()
        if not emp_id:
            messagebox.showerror("Error", "Enter an Employee ID.")
            return

        query = """
            SELECT *
            FROM AIAI_Employee_Work_Ticket
            WHERE Employee_ID = ?
        """
        self.run_query_and_display(query, (emp_id,), f"No records found for Employee ID {emp_id}.")
        self.last_report_title = f"Employee ID {emp_id}"    
    # ----------------------------------------------------------------------
    # REPORTS BUTTON (PDF / Excel / Print handled separately)
    # ----------------------------------------------------------------------
    def open_reports_window(self):
        from reports_window import ReportsWindow
        if not hasattr(self, "last_loaded_rows") or not self.last_loaded_rows:
            messagebox.showerror("No Data", "Load a schedule before opening reports.")
            return

        ReportsWindow(self.controller, self.last_loaded_rows, self.last_report_title)    

    # ----------------------------------------------------------------------
    # QUERY EXECUTION + DISPLAY
    # ----------------------------------------------------------------------
    def run_query_and_display(self, query, params, no_data_message):
        for widget in self.scrollable_frame.winfo_children():
            widget.destroy()

        try:
            conn, cursor = get_db_connection()
        except Exception:
            messagebox.showerror("Database Error", "Could not connect to database.")
            return

        try:
            cursor.execute(query, params)
            rows = cursor.fetchall()

            if not rows:
                messagebox.showinfo("No Data", no_data_message)
                return

            self.display_results(rows)
            self.last_loaded_rows = rows   # <-- keep this
            # self.last_report_title = "Daily Schedule"  <-- REMOVE THIS LINE

        except Exception as e:
            messagebox.showerror("Query Error", f"Error loading schedule:\n{e}")
        finally:
            conn.close()

    # ----------------------------------------------------------------------
    # DISPLAY RESULTS (USED BY ALL VIEWS)
    # ----------------------------------------------------------------------
    def display_results(self, rows):
        row_index = 0

        for row in rows:
            (
                first, last, emp_id,
                hours, title,
                builder, jobsite, model, lot, block,
                mat1, mat2, mat3, mat4, mat5, mat6, mat7,
                pay
            ) = row

            tk.Label(self.scrollable_frame, text=f"{first} {last} (ID: {emp_id})",
                     font=("Arial", 12, "bold")).grid(row=row_index, column=0, sticky="w", pady=5)
            row_index += 1

            tk.Label(self.scrollable_frame, text=f"Job Title: {title}").grid(row=row_index, column=0, sticky="w")
            row_index += 1

            tk.Label(self.scrollable_frame, text=f"Hours Worked: {hours}").grid(row=row_index, column=0, sticky="w")
            row_index += 1

            tk.Label(self.scrollable_frame, text=f"Builder: {builder} | Jobsite: {jobsite}").grid(row=row_index, column=0, sticky="w")
            row_index += 1

            tk.Label(self.scrollable_frame, text=f"Model: {model} | Lot: {lot} | Block: {block}").grid(row=row_index, column=0, sticky="w")
            row_index += 1

            materials = ", ".join([m for m in [mat1, mat2, mat3, mat4, mat5, mat6, mat7] if m])
            tk.Label(self.scrollable_frame, text=f"Materials Used: {materials}").grid(row=row_index, column=0, sticky="w")
            row_index += 1

            tk.Label(self.scrollable_frame, text=f"Pay: ${pay:.2f}", fg="green").grid(row=row_index, column=0, sticky="w", pady=(0, 10))
            row_index += 1