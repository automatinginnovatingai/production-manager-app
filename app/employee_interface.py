import pandas as pd
import tkinter
from tkinter import ttk
from tkinter import messagebox, END
import sqlite3
from openpyxl import Workbook
from cryptography.fernet import Fernet
import calendar
import time
import datetime
import csv
import os
import tkinter as tk
from tkinter import messagebox
from session_context import exit_session, verify_installer, enforce_installer_plan
from db_connection import get_db_connection
from CSV_View import CSV_ViewFrame

class InstallerDailyWorkFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        controller.title("Automating Innovating AI - Employee Daily Work Schedule")

        # --------------------------------------------------------------
        # MAIN FRAME
        # --------------------------------------------------------------
        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        for col in range(7):
            frame.grid_columnconfigure(col, weight=1)

        # --------------------------------------------------------------
        # EMPLOYEE INFO SECTION
        # --------------------------------------------------------------
        user_info_frame = tk.LabelFrame(frame, text="Employee Daily Work Schedule", font="bold")
        user_info_frame.grid(row=0, column=0, padx=40, pady=20, sticky="nsew")
        for c in range(5):
            user_info_frame.grid_columnconfigure(c, weight=1)

        tk.Label(user_info_frame, text="Employee First Name").grid(row=0, column=0)
        tk.Label(user_info_frame, text="Employee Last Name").grid(row=0, column=1)
        tk.Label(user_info_frame, text="Employee ID").grid(row=0, column=2)
        tk.Label(user_info_frame, text="Employee Hours").grid(row=0, column=3)

        # EMPTY LISTS — will be filled in on_show()
        self.first_names_list = []
        self.last_names_list = []
        self.employee_ids_list = []

        # --------------------------------------------------------------
        # EMPLOYEE COMBOBOXES
        # --------------------------------------------------------------
        self.first_name_boxes = []
        self.last_name_boxes = []
        self.id_boxes = []
        self.hour_boxes = []

        for i in range(1, 5):
            fn = ttk.Combobox(user_info_frame, values=[])
            ln = ttk.Combobox(user_info_frame, values=[])
            ei = ttk.Combobox(user_info_frame, values=[])
            hr = tk.Entry(user_info_frame)

            fn.grid(row=i, column=0)
            ln.grid(row=i, column=1)
            ei.grid(row=i, column=2)
            hr.grid(row=i, column=3)

            self.first_name_boxes.append(fn)
            self.last_name_boxes.append(ln)
            self.id_boxes.append(ei)
            self.hour_boxes.append(hr)

        # --------------------------------------------------------------
        # JOB TITLES (STATIC)
        # --------------------------------------------------------------
        tk.Label(user_info_frame, text="Employee Job Title").grid(row=0, column=4)
        titles = [
            "Fiberglass Insulation", "Foam Insulation", "Blow Insulation", "Gutters",
            "Warehouse", "Office", "Fiberglass Insulation-Repair", "Foam Insulation-Repair",
            "Blow Insulation-Repair", "Gutter-Repair", "N/A"
        ]

        self.title_boxes = []
        for i in range(1, 5):
            cb = ttk.Combobox(user_info_frame, values=titles)
            cb.grid(row=i, column=4)
            self.title_boxes.append(cb)

        # --------------------------------------------------------------
        # BUILDER FIELDS (EMPTY VALUES — filled in on_show)
        # --------------------------------------------------------------
        tk.Label(user_info_frame, text="Name of Builder").grid(row=13, column=0)
        tk.Label(user_info_frame, text="Name of Jobsite").grid(row=13, column=1)
        tk.Label(user_info_frame, text="Model Name").grid(row=13, column=2)
        tk.Label(user_info_frame, text="Lot Number").grid(row=13, column=3)
        tk.Label(user_info_frame, text="Block Number").grid(row=13, column=4)

        self.builder_name_list = []
        self.jobsite_name_list = []
        self.model_name_list = []
        self.jobsite_lot_number_list = []
        self.builder_block_number_list = []

        self.builder_name_entry = ttk.Combobox(user_info_frame, values=[])
        self.builder_jobsite_entry = ttk.Combobox(user_info_frame, values=[])
        self.builder_model_entry = ttk.Combobox(user_info_frame, values=[])
        self.builder_lot_number_entry = ttk.Combobox(user_info_frame, values=[])
        self.builder_block_number_entry = ttk.Combobox(user_info_frame, values=[])

        self.builder_name_entry.grid(row=14, column=0)
        self.builder_jobsite_entry.grid(row=14, column=1)
        self.builder_model_entry.grid(row=14, column=2)
        self.builder_lot_number_entry.grid(row=14, column=3)
        self.builder_block_number_entry.grid(row=14, column=4)

        # --------------------------------------------------------------
        # MATERIAL SECTION (EMPTY VALUES — filled in on_show)
        # --------------------------------------------------------------
        tk.Label(user_info_frame, text="Material used").grid(row=19, column=0)
        tk.Label(user_info_frame, text="R-Value").grid(row=19, column=1)
        tk.Label(user_info_frame, text="Material Width").grid(row=19, column=2)
        tk.Label(user_info_frame, text="Sqft/Bags Installed").grid(row=19, column=3)
        tk.Label(user_info_frame, text="Pay Per Tube/Piece Rate").grid(row=19, column=4)

        self.material_comboboxes = []
        self.material_r_values = []
        self.material_widths = []
        self.square_footage_entries = []
        self.pay_rate_entries = []

        for i in range(20, 27):
            m_cb = ttk.Combobox(user_info_frame, values=[])
            r_cb = ttk.Combobox(user_info_frame, values=[])
            w_cb = ttk.Combobox(user_info_frame, values=[])
            sqft_cb = ttk.Combobox(user_info_frame, values=[])
            rate_cb = ttk.Combobox(user_info_frame, values=[])

            m_cb.grid(row=i, column=0)
            r_cb.grid(row=i, column=1)
            w_cb.grid(row=i, column=2)
            sqft_cb.grid(row=i, column=3)
            rate_cb.grid(row=i, column=4)

            self.material_comboboxes.append(m_cb)
            self.material_r_values.append(r_cb)
            self.material_widths.append(w_cb)
            self.square_footage_entries.append(sqft_cb)
            self.pay_rate_entries.append(rate_cb)
        # ------------------------------------------------------------------
        # CALENDAR
        # ------------------------------------------------------------------
        calendar_frame = tk.LabelFrame(frame, text="Calendar", font="bold")
        calendar_frame.grid(row=0, column=6, padx=10, pady=5, sticky="nsew")
        frame.grid_columnconfigure(6, weight=1)

        now = datetime.datetime.now()
        tk.Label(calendar_frame, text="Time").grid(row=1, column=0)
        tk.Label(calendar_frame, text=now.strftime("%H:%M:%S")).grid(row=2, column=0)

        tk.Label(calendar_frame, text="MM/DD/YYYY").grid(row=3, column=0)
        tk.Label(calendar_frame, text=now.strftime("%m/%d/%Y")).grid(row=4, column=0)

        tk.Label(calendar_frame, text="Day of the Week").grid(row=5, column=0)
        tk.Label(calendar_frame, text=calendar.day_name[now.weekday()]).grid(row=6, column=0)

        # ------------------------------------------------------------------
        # BUTTONS
        # ------------------------------------------------------------------
        tk.Button(frame, text="Save", command=self.save_data, bg="green", font="bold").grid(row=28, column=0, padx=20, pady=10)
        tk.Button(frame, text="Exit", command=self.exit_button, bg="red", font="bold").grid(row=28, column=1, padx=20, pady=10)
        tk.Button(frame, text="Clear", command=self.clear_form, bg="blue", font="bold").grid(row=28, column=2, padx=20, pady=10)


        tk.Button(
            frame,
            text="Enter 0 for sqft/bags installed and pay per tube/piece rate if there is no pay information.",
            bg="yellow",
            command=self.no_info
        ).grid(row=27, column=0, padx=20, pady=10)

        tk.Button(
            frame,
            text="Installer Interface",
            command=self.installer_interface,
            bg="orange",
            font="bold"
        ).grid(row=27, column=1, padx=20, pady=10)

    # ----------------------------------------------------------------------
    # SAVE DATA
    # ----------------------------------------------------------------------
    def save_data(self):
        # Employee data
        first_names = [box.get() for box in self.first_name_boxes]
        last_names = [box.get() for box in self.last_name_boxes]
        employee_ids = [box.get() for box in self.id_boxes]
        hours = [box.get() for box in self.hour_boxes]
        titles = [box.get() for box in self.title_boxes]

        if not first_names[0] or not last_names[0]:
            messagebox.showwarning("Error", "First employee must have a first and last name.")
            return

        # Builder info
        builder_name = self.builder_name_entry.get()
        builder_jobsite = self.builder_jobsite_entry.get()
        builder_model = self.builder_model_entry.get()
        builder_lot = self.builder_lot_number_entry.get()
        builder_block = self.builder_block_number_entry.get()

        if not (builder_name and builder_jobsite and builder_lot and builder_block):
            messagebox.showwarning("Error", "Builder, jobsite, lot, and block are required.")
            return

        # Material / sqft / rate
        materials = [cb.get() for cb in self.material_comboboxes]
        r_values = [cb.get() for cb in self.material_r_values]
        widths = [cb.get() for cb in self.material_widths]
        sqft_vals = [cb.get() for cb in self.square_footage_entries]
        rate_vals = [cb.get() for cb in self.pay_rate_entries]

        # Pay calculations
        pay_values = []
        for s, r in zip(sqft_vals, rate_vals):
            try:
                s_f = float(s or 0)
                r_f = float(r or 0)
                pay_values.append(s_f * r_f)
            except ValueError:
                pay_values.append(0.0)

        total_pay = sum(pay_values)
        active_employees = [fn for fn in first_names if fn]
        num_employees = len(active_employees)
        pay_per_employee = total_pay / num_employees if num_employees else 0.0

        # DB insert
       
        cnxn = get_db_connection()
        cursor = cnxn.cursor()

        insert_query = """
            INSERT INTO AIAI_Weekly_Payroll (
                Time, MM_DD_YYYY, Day_of_Week,
                First_Name, Last_Name, Employee_ID, Salt,
                Employee_Hours, Employee_Job_Title,
                Builder, Jobsite, Model_Name, Lot_Number, Block_Number,
                Material_Used, Material_Used_2, Material_Used_3, Material_Used_4,
                Material_Used_5, Material_Used_6, Material_Used_7,
                R_Value, R_Value_2, R_Value_3, R_Value_4, R_Value_5, R_Value_6, R_Value_7,
                Material_Width, Material_Width_2, Material_Width_3, Material_Width_4,
                Material_Width_5, Material_Width_6, Material_Width_7,
                Sqft_Bags_Installed, Sqft_Bags_Installed_2, Sqft_Bags_Installed_3,
                Sqft_Bags_Installed_4, Sqft_Bags_Installed_5, Sqft_Bags_Installed_6,
                Sqft_Bags_Installed_7,
                Pay_Per_Tube_Piece_Rate, Pay_Per_Tube_Piece_Rate_2, Pay_Per_Tube_Piece_Rate_3,
                Pay_Per_Tube_Piece_Rate_4, Pay_Per_Tube_Piece_Rate_5, Pay_Per_Tube_Piece_Rate_6,
                Pay_Per_Tube_Piece_Rate_7,
                Pay, Pay_2, Pay_3, Pay_4, Pay_5, Pay_6, Pay_7,
                total_pay, Pay_Per_Employee, Split_Pay_Per_Employee
            ) VALUES (
                ?,?,?,?,?,?,?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,
                ?,?,?,?,?,?,?,?,
                ?,?,?,?,?
            )
        """

        now = datetime.datetime.now()
        time_str = now.strftime("%H:%M:%S")
        date_str = now.strftime("%m/%d/%Y")
        day_str = calendar.day_name[now.weekday()]

        try:
            for i in range(4):
                if not first_names[i]:
                    continue

                row = [
                    time_str, date_str, day_str,
                    first_names[i], last_names[i], employee_ids[i], 
                    hours[i], titles[i],
                    builder_name, builder_jobsite, builder_model, builder_lot, builder_block,
                    *materials,
                    *r_values,
                    *widths,
                    *sqft_vals,
                    *rate_vals,
                    *pay_values,
                    total_pay,
                    pay_per_employee,
                    pay_per_employee
                ]

                cursor.execute(insert_query, row)

            cnxn.commit()
        except Exception as e:
            cnxn.rollback()
            messagebox.showerror("Insert Error", f"Error inserting data: {e}")
            return
        finally:
            cnxn.close()

        # ------------------------------------------------------------------
        # PRINT PREVIEW
        # ------------------------------------------------------------------
        preview = tk.Toplevel(self)
        preview.title("Employee Daily Work Schedule Printout")

        frame = tk.Frame(preview)
        frame.pack(padx=20, pady=20)

        tk.Label(frame, text="Employee Daily Work Schedule Printout", font=("Arial", 14, "bold")).grid(row=0, column=0, columnspan=4, pady=10)

        row_idx = 1
        for i in range(4):
            if not first_names[i]:
                continue
            tk.Label(frame, text=f"{first_names[i]} {last_names[i]}", font=("Arial", 10, "bold")).grid(row=row_idx, column=0, sticky="w")
            tk.Label(frame, text=f"ID: {employee_ids[i]}").grid(row=row_idx, column=1, sticky="w")
            tk.Label(frame, text=f"Hours: {hours[i]}").grid(row=row_idx, column=2, sticky="w")
            tk.Label(frame, text=f"Pay: ${pay_values[i]:.2f}").grid(row=row_idx, column=3, sticky="w")
            row_idx += 1

        tk.Label(frame, text=f"Total Pay: ${total_pay:.2f}", font=("Arial", 10, "bold")).grid(row=row_idx+1, column=0, sticky="w")
        tk.Label(frame, text=f"Pay Per Employee: ${pay_per_employee:.2f}", font=("Arial", 10, "bold")).grid(row=row_idx+2, column=0, sticky="w")

        # ------------------------------------------------------------------
        # CLEAR FORM
        # ------------------------------------------------------------------
        def on_preview_close():
            messagebox.showinfo("Success", "Data saved and payroll recorded.")
            preview.destroy()

        preview.protocol("WM_DELETE_WINDOW", on_preview_close)

    # ----------------------------------------------------------------------
    # NO INFO
    # ----------------------------------------------------------------------
    def no_info(self):
        messagebox.showinfo("Info", "Enter 0 where no pay info exists.")

    # ----------------------------------------------------------------------
    # Installer INTERFACE
    # ----------------------------------------------------------------------
    def installer_interface(self):
        from Installer_Interface import InstallerInterfaceFrame
        self.controller.show_frame(InstallerInterfaceFrame)


    # ----------------------------------------------------------------------
    # EXIT
    # ----------------------------------------------------------------------
    def exit_button(self):
        exit_session()

    # ----------------------------------------------------------------------
    # CLEAR FORM
    # ----------------------------------------------------------------------
    def clear_form(self):
        for group in [
            self.first_name_boxes,
            self.last_name_boxes,
            self.id_boxes,
            self.hour_boxes,
            self.material_comboboxes,
            self.material_r_values,
            self.material_widths,
            self.square_footage_entries,
            self.pay_rate_entries,
        ]:
            for widget in group:
                widget.delete(0, "end")

        self.builder_name_entry.delete(0, "end")
        self.builder_jobsite_entry.delete(0, "end")
        self.builder_model_entry.delete(0, "end")
        self.builder_lot_number_entry.delete(0, "end")
        self.builder_block_number_entry.delete(0, "end")

    def _load_employee_data(self, cursor):
        try:
            cursor.execute("SELECT First_Name, Last_Name, ID FROM AIAI_Employee_Info")
            rows = cursor.fetchall()
        except Exception:
            rows = []

        self.first_names_list = []
        self.last_names_list = []
        self.employee_ids_list = []

        seen_first, seen_last, seen_ids = set(), set(), set()

        for f, l, i in rows:
            if f not in seen_first:
                self.first_names_list.append(f)
                seen_first.add(f)
            if l not in seen_last:
                self.last_names_list.append(l)
                seen_last.add(l)
            if i not in seen_ids:
                self.employee_ids_list.append(i)
                seen_ids.add(i)

        # Update comboboxes
        for fn in self.first_name_boxes:
            fn["values"] = self.first_names_list
        for ln in self.last_name_boxes:
            ln["values"] = self.last_names_list
        for ei in self.id_boxes:
            ei["values"] = self.employee_ids_list

    def _load_material_data(self, cursor):
        hardcoded_materials = [
            "Owens Corning", "Johns Manville", "Knauf", "Certainteed", "Guardian", "Rockwool",
            "Fi-Foil", "Mineral Wool", "Foam - Open Cell", "Foam - Close Cell",
            "Baffles and Rulers", "Tape", "Lo Gloss White", "Hi Gloss White", "Brown", "Cream",
            "Musket Brown", "Wicker", "Eggshell", "Light Gray", "Dark Gray", "Linen", "Clay",
            "Bronze", "Black", "Other", "N/A"
        ]

        hardcoded_r_values = [
            "R-49", "R-38", "R-30", "R-20", "R-21", "R-19", "R13", "R11", "R-8", "R-3",
            "AA-2", "VR Plus", "Rigid Board", "Radiant Barrier", "Removal", "k-style",
            "half-round", "gutter-guard", "downspout", "elbows", "endcaps", "connectors",
            "fascia board", "Other", "N/A"
        ]

        hardcoded_material_width = [
            "24 inch", "23 inch", "16 inch", "15 inch",
            "Removal-Blow", "Removal-Batts", "Removal-Both", "N/A"
        ]

        try:
            cursor.execute("""
                SELECT material_name, material_r_value, material_width, square_footage, pay_rate
                FROM AIAI_Material_Info
            """)
            rows = cursor.fetchall()
        except Exception:
            rows = []

        material_name, material_r_value, material_width = [], [], []
        square_footage_list, pay_rate_list = [], []
        seen_name, seen_r, seen_w, seen_sqft, seen_rate = set(), set(), set(), set(), set()

        for name, r_val, width, sqft, rate in rows:
            if name and name not in seen_name:
                material_name.append(name); seen_name.add(name)
            if r_val and r_val not in seen_r:
                material_r_value.append(r_val); seen_r.add(r_val)
            if width and width not in seen_w:
                material_width.append(width); seen_w.add(width)
            if sqft and sqft not in seen_sqft:
                square_footage_list.append(sqft); seen_sqft.add(sqft)
            if rate and rate not in seen_rate:
                pay_rate_list.append(rate); seen_rate.add(rate)

        self.final_material_list = hardcoded_materials + [m for m in material_name if m not in hardcoded_materials]
        self.final_r_values_list = hardcoded_r_values + [r for r in material_r_value if r not in hardcoded_r_values]
        self.final_material_width_list = hardcoded_material_width + [w for w in material_width if w not in hardcoded_material_width]

        # Update comboboxes
        for cb in self.material_comboboxes:
            cb["values"] = self.final_material_list
        for cb in self.material_r_values:
            cb["values"] = self.final_r_values_list
        for cb in self.material_widths:
            cb["values"] = self.final_material_width_list
        for cb in self.square_footage_entries:
            cb["values"] = square_footage_list
        for cb in self.pay_rate_entries:
            cb["values"] = pay_rate_list

    def _load_builder_data(self, cursor):
        try:
            cursor.execute("""
                SELECT builder_name, jobsite_name, model_name, jobsite_lot_number, builder_block_number
                FROM AIAI_Builders_Info
            """)
            rows = cursor.fetchall()
        except Exception:
            rows = []

        self.builder_name_list = []
        self.jobsite_name_list = []
        self.model_name_list = []
        self.jobsite_lot_number_list = []
        self.builder_block_number_list = []

        seen_b, seen_j, seen_m, seen_l, seen_bl = set(), set(), set(), set(), set()

        for b, j, m, l, bl in rows:
            if b not in seen_b:
                self.builder_name_list.append(b); seen_b.add(b)
            if j not in seen_j:
                self.jobsite_name_list.append(j); seen_j.add(j)
            if m not in seen_m:
                self.model_name_list.append(m); seen_m.add(m)
            if l not in seen_l:
                self.jobsite_lot_number_list.append(l); seen_l.add(l)
            if bl not in seen_bl:
                self.builder_block_number_list.append(bl); seen_bl.add(bl)

        # Update comboboxes
        self.builder_name_entry["values"] = self.builder_name_list
        self.builder_jobsite_entry["values"] = self.jobsite_name_list
        self.builder_model_entry["values"] = self.model_name_list
        self.builder_lot_number_entry["values"] = self.jobsite_lot_number_list
        self.builder_block_number_entry["values"] = self.builder_block_number_list                    

    def on_show(self):
        # ADMIN CHECK
        if not verify_installer():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        # PLAN CHECK
        if not enforce_installer_plan("enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            from startup_page import StartPageFrame
            self.controller.show_frame(StartPageFrame)
            return False

        try:
            conn, cursor = get_db_connection()
        except Exception:
            messagebox.showerror("Database Error", "Could not connect to database.")
            return False

        # CALL HELPERS THAT CONTAIN THE SQL YOU CURRENTLY HAVE IN __init__
        self._load_employee_data(cursor)
        self._load_material_data(cursor)
        self._load_builder_data(cursor)

        conn.close()
        return True     