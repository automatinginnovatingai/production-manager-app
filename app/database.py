import tkinter as tk
from tkinter import messagebox
from session_context import exit_session, verify_admin, enforce_plan
from startup_page import StartPageFrame


class DatabasePortalFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        title_label = tk.Label(
            self,
            text="AIAI Production Manager App",
            font=("Helvetica", 24, "bold")
        )
        title_label.pack(pady=(30, 10))

        buttons_frame = tk.Frame(self)
        buttons_frame.pack(expand=True)

        buttons = [
            ("Builder Info Database", self.goto_builders_db, "brown"),
            ("Installer Info Database", self.goto_installers_db, "purple"),
            ("Material Info Database", self.goto_material_db, "blue"),
            ("Weekly Production Info", self.goto_weekly_production_info, "cyan"),
            ("Admin Interface", self.goto_admin_interface, "green"),
            ("Exit", exit_session, "red")
        ]

        for text, cmd, color in buttons:
            tk.Button(
                buttons_frame,
                text=text,
                command=cmd,
                font=("Arial", 12, "bold"),
                bg=color,
                width=25
            ).pack(padx=20, pady=10)

    # ---------------------------------------------------------
    # SHOW HOOK (must be OUTSIDE __init__)
    # ---------------------------------------------------------
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
    # Navigation Methods (must be inside the class)
    # ---------------------------------------------------------
    def goto_builders_db(self):
        from builders_db import BuildersDBFrame
        self.controller.show_frame(BuildersDBFrame)

    def goto_installers_db(self):
        from installer_db import InstallerDBFrame
        self.controller.show_frame(InstallerDBFrame)

    def goto_material_db(self):
        from material_info_db import MaterialInfoDBFrame
        self.controller.show_frame(MaterialInfoDBFrame)

    def goto_weekly_production_info(self):
        from weekly_production_sheet import WeeklyProductionSheetFrame
        self.controller.show_frame(WeeklyProductionSheetFrame)

    def goto_admin_interface(self):
        from Admin_Interface import AdminInterfaceFrame
        self.controller.show_frame(AdminInterfaceFrame)


def main():
    if verify_admin():
        print("This module is now a Frame. Load it through the App controller.")
    else:
        messagebox.showerror("User not authorized")
        exit_session()


if __name__ == "__main__":
    main()