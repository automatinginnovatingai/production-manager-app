# start_page.py
import tkinter as tk
import sys
from datetime import datetime, date
import calendar

from installer_login import InstallerLoginFrame
from Production_Manager_App import PMMHomeFrame

# REQUIRED imports for activation check
from license_storage import load_local_activation
from db_connection import get_db_connection
from tkinter import messagebox
from license_validator import LicensePageFrame


class StartPageFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        canvas = tk.Canvas(self, width=controller.winfo_screenwidth(),
                           height=controller.winfo_screenheight())
        canvas.pack(fill="both", expand=True)

        frame = tk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        home_portal_label = tk.Label(frame, text="Home", font=("Helvetica", 16, "bold"))
        title_label = tk.Label(frame, text="Automating Innovating AI Production Manager App Welcome Page",
                               font=("Helvetica", 18, "bold"))
        home_portal_label.grid(row=0, column=0)
        title_label.grid(row=1, column=0, pady=(0, 20))

        tk.Button(frame, text="Admin Page",
                  command=self.admin_page,
                  font=("Helvetica", 14, "bold"), bg="green", fg="white").grid(row=2, column=0, pady=10)

        tk.Button(frame, text="Installer Page",
                  command=self.installer_page,
                  font=("Helvetica", 14, "bold"), bg="gold").grid(row=3, column=0, pady=10)

        tk.Button(frame, text="Exit",
                  command=self.exit_app,
                  font=("Helvetica", 14, "bold"), bg="red", fg="white").grid(row=4, column=0, pady=10)

        # Calendar Section
        calendar_frame = tk.LabelFrame(frame, text="Calendar", font=("Helvetica", 14, "bold"))
        calendar_frame.grid(row=0, column=1, rowspan=5, padx=40, pady=10, sticky="n")

        now = datetime.now()
        s1 = now.strftime("%m/%d/%Y")
        my_date = date.today()
        day_name = calendar.day_name[my_date.weekday()]

        tk.Label(calendar_frame, text="Time", font=("Helvetica", 12)).grid(row=0, column=0, sticky="w")
        self.time_frame = tk.Label(calendar_frame, text=now.strftime("%H:%M:%S"), font=("Helvetica", 12))
        self.time_frame.grid(row=1, column=0, sticky="w")

        tk.Label(calendar_frame, text="MM/DD/YYYY", font=("Helvetica", 12)).grid(row=2, column=0, sticky="w")
        tk.Label(calendar_frame, text=s1, font=("Helvetica", 12)).grid(row=3, column=0, sticky="w")

        tk.Label(calendar_frame, text="Day of the Week", font=("Helvetica", 12)).grid(row=4, column=0, sticky="w")
        tk.Label(calendar_frame, text=day_name, font=("Helvetica", 12)).grid(row=5, column=0, sticky="w")

    def on_show(self):
        """Runs every time this frame becomes visible."""
        # 1. Load activation_id from DPAPI
        try:
            cfg = load_local_activation()
            activation_id = cfg["activation_id"]
        except Exception:
            messagebox.showerror("License Error", "This machine is not activated.")
            self.controller.show_frame(LicensePageFrame)
            return

        # 2. Validate activation_id in SQL Server
        try:
            conn, cursor = get_db_connection()
            cursor.execute("SELECT COUNT(*) FROM activations WHERE activation_id = ?", activation_id)
            exists = cursor.fetchone()[0]
        except Exception as e:
            messagebox.showerror("Database Error", str(e))
            return

        # 3. If activation missing → force reactivation
        if exists == 0:
            messagebox.showerror("License Error", "This machine is not activated.")
            self.controller.show_frame(LicensePageFrame)
            return

    def admin_page(self):
        self.controller.show_frame(PMMHomeFrame)

    def installer_page(self):
        self.controller.show_frame(InstallerLoginFrame)

    def exit_app(self):
        sys.exit()