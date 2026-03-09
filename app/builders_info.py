import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import calendar
import datetime
import pandas as pd

from db_connection import get_db_connection
from session_context import verify_admin, exit_session, enforce_plan
from Admin_Interface import AdminInterfaceFrame
from startup_page import StartPageFrame


class BuildersInfoFrame(tk.Frame):
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

    # ----------------------------------------------------------------------
    # UI Layout
    # ----------------------------------------------------------------------
    def build_ui(self):
        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")

        builder_info_frame = tk.LabelFrame(frame, text="Builder's Portal", font="bold")
        builder_info_frame.grid(row=0, column=0, padx=20, pady=10)

        # Entry fields
        self.builder_name_entry = tk.Entry(builder_info_frame)
        self.jobsite_name_entry = tk.Entry(builder_info_frame)
        self.jobsite_address_entry = tk.Entry(builder_info_frame)
        self.jobsite_city_entry = tk.Entry(builder_info_frame)
        self.jobsite_state_entry = tk.Entry(builder_info_frame)
        self.jobsite_zip_code_entry = tk.Entry(builder_info_frame)
        self.model_name_entry = tk.Entry(builder_info_frame)
        self.jobsite_lot_number_entry = tk.Entry(builder_info_frame)
        self.builder_block_number_entry = tk.Entry(builder_info_frame)
        self.job_total_sq_ft_entry = tk.Entry(builder_info_frame)
        self.ext_block_sq_footage_entry = tk.Entry(builder_info_frame)
        self.ceiling_area_sq_footage_entry = tk.Entry(builder_info_frame)
        self.garage_ceiling_sq_footage_entry = tk.Entry(builder_info_frame)
        self.garage_wall_sq_footage_entry = tk.Entry(builder_info_frame)
        self.int_wall_sq_footage_entry = tk.Entry(builder_info_frame)
        self.miscellaneous_info_entry = tk.Entry(builder_info_frame)

        labels = [
            ("Builder's name:", self.builder_name_entry),
            ("Name of jobsite:", self.jobsite_name_entry),
            ("Jobsite Address", self.jobsite_address_entry),
            ("City", self.jobsite_city_entry),
            ("State", self.jobsite_state_entry),
            ("Zip Code", self.jobsite_zip_code_entry),
            ("Model name:", self.model_name_entry),
            ("Lot number:", self.jobsite_lot_number_entry),
            ("Block number:", self.builder_block_number_entry),
            ("Total square footage:", self.job_total_sq_ft_entry),
            ("Exterior block square footage:", self.ext_block_sq_footage_entry),
            ("Ceiling area square footage:", self.ceiling_area_sq_footage_entry),
            ("Garage ceiling square footage:", self.garage_ceiling_sq_footage_entry),
            ("Garage wall square footage:", self.garage_wall_sq_footage_entry),
            ("Interior wall square footage:", self.int_wall_sq_footage_entry),
            ("Miscellaneous information:", self.miscellaneous_info_entry),
        ]

        for i, (text, entry) in enumerate(labels):
            tk.Label(builder_info_frame, text=text, anchor="w").grid(
                row=i, column=0, sticky="w", padx=10, pady=5
            )
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

        builder_info_frame.grid_columnconfigure(1, weight=1)

        # Title
        title_label = tk.Label(
            builder_info_frame,
            text="Automating Innovating AI Production Manager App",
            font=("Helvetica", 16, "bold"),
            wraplength=300,
        )
        title_label.grid(
            row=0, column=2, rowspan=len(labels), padx=20, pady=10, sticky="nsew"
        )

        # Buttons
        button_frame = tk.Frame(frame)
        button_frame.grid(row=1, column=0, pady=20, sticky="ew")

        buttons = [
            ("Save", self.builder_info_data, "green"),
            ("Exit", exit_session, "red"),
            ("Admin Interface", lambda: self.controller.show_frame(AdminInterfaceFrame), "blue"),
            ("Clear Entry Forms", self.clear_entries, "yellow"),
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            tk.Button(
                button_frame, text=text, command=cmd, font="bold", bg=color
            ).grid(row=0, column=i, padx=10, pady=10, sticky="ew")

        for i in range(len(buttons)):
            button_frame.grid_columnconfigure(i, weight=1)

    # ----------------------------------------------------------------------
    # Clear Form
    # ----------------------------------------------------------------------
    def clear_entries(self):
        for entry in [
            self.builder_name_entry,
            self.jobsite_name_entry,
            self.jobsite_address_entry,
            self.jobsite_city_entry,
            self.jobsite_state_entry,
            self.jobsite_zip_code_entry,
            self.model_name_entry,
            self.jobsite_lot_number_entry,
            self.builder_block_number_entry,
            self.job_total_sq_ft_entry,
            self.ext_block_sq_footage_entry,
            self.ceiling_area_sq_footage_entry,
            self.garage_ceiling_sq_footage_entry,
            self.garage_wall_sq_footage_entry,
            self.int_wall_sq_footage_entry,
            self.miscellaneous_info_entry,
        ]:
            entry.delete(0, tk.END)

    # ----------------------------------------------------------------------
    # Save Builder Info (Plain Text)
    # ----------------------------------------------------------------------
    def builder_info_data(self):

        data = (
            self.builder_name_entry.get(),
            self.jobsite_name_entry.get(),
            self.jobsite_address_entry.get(),
            self.jobsite_city_entry.get(),
            self.jobsite_state_entry.get(),
            self.jobsite_zip_code_entry.get(),
            self.model_name_entry.get(),
            self.jobsite_lot_number_entry.get(),
            self.builder_block_number_entry.get(),
            self.job_total_sq_ft_entry.get(),
            self.ext_block_sq_footage_entry.get(),
            self.ceiling_area_sq_footage_entry.get(),
            self.garage_ceiling_sq_footage_entry.get(),
            self.garage_wall_sq_footage_entry.get(),
            self.int_wall_sq_footage_entry.get(),
            self.miscellaneous_info_entry.get(),
        )

        try:
            self.insert_builder_data(data)
            messagebox.showinfo("Success", "Builder data saved successfully!")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    # ----------------------------------------------------------------------
    # Insert Into SQL Server (Plain Text)
    # ----------------------------------------------------------------------
    def insert_builder_data(self, data):
        try:
            cnxn = get_db_connection()
            with cnxn as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    INSERT INTO AIAI_Builders_Info (
                        builder_name, jobsite_name, jobsite_address, city, state, zip_code,
                        model_name, jobsite_lot_number, builder_block_number, job_total_sq_ft,
                        ext_block_sq_footage, ceiling_area_sq_footage, garage_ceiling_sq_footage,
                        garage_wall_sq_footage, int_wall_sq_footage, miscellaneous_info
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                    ''',
                    data,
                )
                conn.commit()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


def main():
    pass