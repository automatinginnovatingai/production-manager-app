# app/admin_interface.py

import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import datetime
from session_context import (
    verify_admin,
    exit_session,
    enforce_plan,
    get_subscription_plan_from_session

)
from startup_page import StartPageFrame


class AdminInterfaceFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        controller.title("Automating Innovating AI Production Manager App")

        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")

        production_info_frame = tk.Label(
            frame,
            text="Automating Innovating AI, LLC - Production Manager Dashboard",
            font=("Arial", 16, "bold")
        )
        production_info_frame.pack(padx=20, pady=10)

        buttons_frame = tk.Frame(frame)
        buttons_frame.pack()

        self.button_widgets = {}

        buttons = [
            ("Builder's Portal", self.get_builders_info, "brown", "pro"),
            ("Employee Portal", self.get_installer_info, "purple", "pro"),
            ("Production Portal", self.get_production_info, "blue", "basic"),
            ("Database Portal", self.get_database, "green", "pro"),
            ("Material Portal", self.get_material_info, "cyan", "pro"),
            ("Alerts", self.get_alert_check, "gold", "enterprise"),
            ("Schedule Pay Week", self.get_pay_week_schedule, "white", "pro"),
            ("License Key", self.get_license_key, "yellow", "basic"),
            ("Upgrade Plan", self.get_upgrade_license_key, "gray", "basic_or_pro"),
            ("Activate Installer", self.get_activate_installer, "orange", "enterprise"),
            ("Transfer Data", self.get_transfer_data, "silver" , "basic"),
            ("Work Ticket", self.get_work_ticket, "coral", "basic"),
            ("Exit", self.exit_button, "red", "basic")
        ]

        for text, cmd, color, required_plan in buttons:
            btn = tk.Button(
                buttons_frame,
                text=text,
                command=cmd,
                font=("Arial", 12, "bold"),
                bg=color,
                width=20
            )
            btn.pack(padx=20, pady=10)

            self.button_widgets[text] = {
                "widget": btn,
                "required_plan": required_plan
            }
        
        calendar_frame = tk.LabelFrame(frame, text="Calendar", font=("Arial", 12, "bold"))
        calendar_frame.pack(padx=20, pady=10)

        now = datetime.datetime.now()

        tk.Label(calendar_frame, text="Time", font=("Arial", 10)).pack(padx=10, pady=5)
        tk.Label(calendar_frame, text=now.strftime("%H:%M:%S"), font=("Arial", 10)).pack(padx=10, pady=5)
        tk.Label(calendar_frame, text=now.strftime("%m/%d/%Y"), font=("Arial", 10)).pack(padx=10, pady=5)

    # ---------------------------------------------------------
    # PLAN VISIBILITY HOOK
    # ---------------------------------------------------------
    def on_show(self):
        if not verify_admin():
            messagebox.showerror("User not authorized")
            exit_session()
            return False
        

        # 2. USER MUST HAVE ANY PLAN
        if not enforce_plan("basic", "pro", "enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            self.controller.show_frame(StartPageFrame)
            return False

        # 3. GET ACTUAL PLAN STRING FROM DB
        user_plan = get_subscription_plan_from_session()

        if user_plan not in ("basic", "pro", "enterprise"):
            user_plan = "basic"  # fallback safety
        
        # 4. APPLY BUTTON VISIBILITY
        self.apply_plan_visibility(user_plan)

        return True

    def apply_plan_visibility(self, plan):
        plan_order = ["basic", "pro", "enterprise"]

        for name, info in self.button_widgets.items():
            widget = info["widget"]
            required = info["required_plan"]

            # Special rule: Upgrade Plan visible only for basic + pro
            if required == "basic_or_pro":
                if plan in ("basic", "pro"):
                    widget.pack(padx=20, pady=10)
                else:
                    widget.pack_forget()
                continue
            # Normal rule (min required plan)
            if plan_order.index(plan) >= plan_order.index(required):
                widget.pack(padx=20, pady=10)
            else:
                widget.pack_forget()

    # ---------------------------------------------------------
    # Navigation Methods
    # ---------------------------------------------------------
    def get_installer_info(self):
        from installer_info import InstallerInfoFrame
        self.controller.show_frame(InstallerInfoFrame)

    def get_builders_info(self):
        from builders_info import BuildersInfoFrame
        self.controller.show_frame(BuildersInfoFrame)

    def get_database(self):
        from database import DatabasePortalFrame
        self.controller.show_frame(DatabasePortalFrame)

    def get_alert_check(self):
        from alert_checks import AlertChecksFrame
        self.controller.show_frame(AlertChecksFrame)

    def get_production_info(self):
        from Automating_Innovating_AI_Production_Manager_App import EmployeeDailyWorkFrame
        self.controller.show_frame(EmployeeDailyWorkFrame)

    def get_material_info(self):
        from material_info import MaterialInfoFrame
        self.controller.show_frame(MaterialInfoFrame)

    def get_license_key(self):
        from view_license_key import ViewLicenseKeyFrame
        self.controller.show_frame(ViewLicenseKeyFrame)

    def get_pay_week_schedule(self):
        from pay_week_schedule import PayWeekScheduleFrame
        self.controller.show_frame(PayWeekScheduleFrame)

    def get_upgrade_license_key(self):
        from upgrade_license_page import UpgradeLicenseFrame
        self.controller.show_frame(UpgradeLicenseFrame)

    def get_activate_installer(self):
        from installer_activation import InstallerActivationFrame
        self.controller.show_frame(InstallerActivationFrame)

    def get_transfer_data(self):
        from transfer_data import TransferFrame
        self.controller.show_frame(TransferFrame)

    def get_work_ticket(self):
        from work_ticket import EmployeeTicketFrame
        self.controll.show_frame(EmployeeTicketFrame)    

    def exit_button(self):
        self.controller.destroy()
