# app/alert_checks.py

import os
import pandas as pd
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.fernet import Fernet
from startup_page import StartPageFrame
from db_connection import get_db_connection
from session_context import verify_admin, exit_session, enforce_plan

import tkinter as tk
from tkinter import messagebox
import pandas as pd

class AlertChecksFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller    

        tk.Label(self, text="Payroll Table Comparison", font=("Arial", 16, "bold")).pack(pady=10)

        tk.Button(
            self,
            text="Load Payroll Tables",
            command=self.load_tables,
            bg="lightblue",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        tk.Button(
            self,
            text="Compare Tables",
            command=self.compare_tables,
            bg="green",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        tk.Button(
            self,
            text="Admin Interface",
            command=self.back,
            bg="gold",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        tk.Button(
            self,
            text="Exit",
            command=self.compare_tables,
            bg="red",
            fg="white",
            font=("Arial", 12, "bold")
        ).pack(pady=5)

        self.df1 = None
        self.df2 = None

        # --------------------------------------------------------------
        # REQUIRED COLUMNS TO COMPARE (YOUR ORIGINAL LIST)
        # --------------------------------------------------------------
        self.columns_to_compare = [
            'Time', 'MM_DD_YYYY', 'Day_of_Week', 'First_Name', 'Last_Name', 'Employee_ID',
            'Employee_Hours', 'Employee_Job_Title', 'Builder', 'Jobsite', 'Model_Name',
            'Lot_Number', 'Block_Number', 'Material_Used', 'Material_Used_2', 'Material_Used_3',
            'Material_Used_4', 'Material_Used_5', 'Material_Used_6', 'Material_Used_7', 'R_Value',
            'R_Value_2', 'R_Value_3', 'R_Value_4', 'R_Value_5', 'R_Value_6', 'R_Value_7',
            'Material_Width', 'Material_Width_2', 'Material_Width_3', 'Material_Width_4',
            'Material_Width_5', 'Material_Width_6', 'Material_Width_7', 'Sqft_Bags_Installed',
            'Sqft_Bags_Installed_2', 'Sqft_Bags_Installed_3', 'Sqft_Bags_Installed_4',
            'Sqft_Bags_Installed_5', 'Sqft_Bags_Installed_6', 'Sqft_Bags_Installed_7',
            'Pay_Per_Tube_Piece_Rate', 'Pay_Per_Tube_Piece_Rate_2', 'Pay_Per_Tube_Piece_Rate_3',
            'Pay_Per_Tube_Piece_Rate_4', 'Pay_Per_Tube_Piece_Rate_5', 'Pay_Per_Tube_Piece_Rate_6',
            'Pay_Per_Tube_Piece_Rate_7', 'Pay', 'Pay_2', 'Pay_3', 'Pay_4', 'Pay_5', 'Pay_6', 'Pay_7',
            'total_pay', 'Pay_Per_Employee', 'Split_Pay_Per_Employee'
        ]
    def on_show(self):
        # ADMIN CHECK
        if not verify_admin():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        # PLAN CHECK
        if not enforce_plan("enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            self.controller.show_frame(StartPageFrame)
            return False

        return True    
    # ----------------------------------------------------------------------
    # LOAD TABLES + DECRYPT
    # ----------------------------------------------------------------------
    def load_tables(self):
        try:
            conn = get_db_connection()

            raw_df1 = pd.read_sql_query("SELECT * FROM AIAI_Weekly_Payroll", conn)
            raw_df2 = pd.read_sql_query("SELECT * FROM AIAI_Employee_Weekly_Payroll", conn)

            conn.close()

            # decrypt every cell
            self.df1 = raw_df1
            self.df2 = raw_df2
            messagebox.showinfo("Success", "Both payroll tables loaded.")

        except Exception as e:
            messagebox.showerror("Load Error", f"Could not load tables:\n{e}")

    # ----------------------------------------------------------------------
    # VALIDATE STRUCTURE
    # ----------------------------------------------------------------------
    def tables_match(self, df1, df2):
        if df1 is None or df2 is None:
            return False

        # ensure both tables contain the required columns
        if not all(col in df1.columns for col in self.columns_to_compare):
            return False
        if not all(col in df2.columns for col in self.columns_to_compare):
            return False

        # restrict to required columns only
        df1 = df1[self.columns_to_compare]
        df2 = df2[self.columns_to_compare]

        # index must match
        if list(df1.index) != list(df2.index):
            return False

        return True

    # ----------------------------------------------------------------------
    # COMPARE TABLES
    # ----------------------------------------------------------------------
    def compare_tables(self):
        if self.df1 is None or self.df2 is None:
            messagebox.showwarning("Missing Data", "Load both tables before comparing.")
            return

        if not self.tables_match(self.df1, self.df2):
            messagebox.showerror(
                "Structure Mismatch",
                "The two payroll tables do not match the required structure."
            )
            return

        df1 = self.df1[self.columns_to_compare]
        df2 = self.df2[self.columns_to_compare]

        try:
            comparison = df1.compare(df2, keep_shape=True, keep_equal=True)
        except Exception as e:
            messagebox.showerror("Comparison Error", f"Could not compare tables:\n{e}")
            return

        self.show_results(comparison)

    # ----------------------------------------------------------------------
    # DISPLAY RESULTS
    # ----------------------------------------------------------------------
    def show_results(self, comparison_df):
        win = tk.Toplevel(self)
        win.title("Payroll Table Comparison Results")

        tk.Label(win, text="Differences Between Tables", font=("Arial", 14, "bold")).pack(pady=10)

        text_box = tk.Text(win, width=140, height=40)
        text_box.pack(padx=10, pady=10)

        if comparison_df.empty:
            text_box.insert("end", "No differences found.\n")
        else:
            text_box.insert("end", comparison_df.to_string())

        text_box.config(state="disabled")

    def exit_button(self):
        self.controller.destroy()

    def back(self):    
        from Admin_Interface import AdminInterfaceFrame
        self.controller.show_frame(AdminInterfaceFrame)    