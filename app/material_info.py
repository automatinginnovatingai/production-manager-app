import tkinter as tk
from tkinter import ttk, messagebox
import uuid
import datetime
from Admin_Interface import AdminInterfaceFrame
from startup_page import StartPageFrame
from session_context import verify_admin, exit_session, enforce_plan
from db_connection import get_db_connection


class MaterialInfoFrame(tk.Frame):
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
    # UI
    # ---------------------------------------------------------
    def build_ui(self):
        title = tk.Label(
            self,
            text="Material's Information Portal",
            font=("Helvetica", 24, "bold")
        )
        title.pack(pady=10)

        frame = tk.Frame(self)
        frame.pack(expand=True, fill="both")

        form_frame = tk.LabelFrame(frame, text="Material Portal", font="bold")
        form_frame.grid(row=0, column=0, padx=20, pady=10)

        self.material_name = tk.Entry(form_frame)
        self.material_r_value = tk.Entry(form_frame)
        self.material_width = tk.Entry(form_frame)
        self.square_footage = tk.Entry(form_frame)
        self.pay_rate = tk.Entry(form_frame)

        fields = [
            ("Material Name", self.material_name),
            ("Material R Value", self.material_r_value),
            ("Material Width", self.material_width),
            ("Square Footage", self.square_footage),
            ("Pay Rate", self.pay_rate)
        ]

        for i, (text, entry) in enumerate(fields):
            tk.Label(form_frame, text=text, anchor="w").grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry.grid(row=i, column=1, padx=10, pady=5, sticky="ew")

        form_frame.grid_columnconfigure(1, weight=1)

        title_label = tk.Label(
            form_frame,
            text="Automating Innovating AI Production Manager App",
            font=("Helvetica", 16, "bold"),
            wraplength=300
        )
        title_label.grid(row=0, column=2, rowspan=len(fields), padx=20, pady=10, sticky="nsew")

        calendar_frame = tk.LabelFrame(frame, text="Calendar", font=("Arial", 12, "bold"))
        calendar_frame.grid(row=1, column=0, padx=20, pady=10, sticky="ew")

        self.time_label = tk.Label(calendar_frame, text="", font=("Arial", 10))
        self.time_label.pack(padx=10, pady=5)

        self.date_label = tk.Label(calendar_frame, text="", font=("Arial", 10))
        self.date_label.pack(padx=10, pady=5)

        buttons = [
            ("Save", self.material_info_data, "green"),
            ("Exit", exit_session, "red"),
            ("Admin Interface", lambda: self.controller.show_frame(AdminInterfaceFrame), "blue")
        ]

        for i, (text, cmd, color) in enumerate(buttons):
            tk.Button(
                frame,
                text=text,
                command=cmd,
                font="bold",
                bg=color
            ).grid(row=i + 2, column=0, sticky="news", padx=20, pady=10)

    # ---------------------------------------------------------
    # TIME UPDATE
    # ---------------------------------------------------------
    def update_time(self):
        now = datetime.datetime.now()
        self.time_label.config(text=now.strftime("%H:%M:%S"))
        self.date_label.config(text=now.strftime("%m/%d/%Y"))
        self.after(1000, self.update_time)

    # ---------------------------------------------------------
    # CLEAR
    # ---------------------------------------------------------
    def clear_entries(self):
        self.material_name.delete(0, tk.END)
        self.material_r_value.delete(0, tk.END)
        self.material_width.delete(0, tk.END)
        self.square_footage.delete(0, tk.END)
        self.pay_rate.delete(0, tk.END)

    # ---------------------------------------------------------
    # INSERT MATERIAL
    # ---------------------------------------------------------
    def insert_material_data(self, data):
        try:
            cnxn = get_db_connection()
            with cnxn as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO AIAI_Material_Info (
                        material_id, material_name, material_r_value,
                        material_width, square_footage, pay_rate
                    ) VALUES (?, ?, ?, ?, ?, ?)
                ''', data)
                conn.commit()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    # ---------------------------------------------------------
    # SAVE MATERIAL
    # ---------------------------------------------------------
    def material_info_data(self):
        material_id = str(uuid.uuid4())
        data = (
            material_id,
            self.material_name.get(),
            self.material_r_value.get(),
            self.material_width.get(),
            self.square_footage.get(),
            self.pay_rate.get()
        )

        try:
            self.insert_material_data(data)
            messagebox.showinfo("Success", "Material data entered and saved successfully!")
            self.clear_entries()
        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")


def main():
    pass