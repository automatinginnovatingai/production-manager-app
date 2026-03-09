import tkinter as tk
from tkinter import messagebox
from session_context import verify_admin, exit_session, clear_user
from sync_subscription import upgrade_license
from startup_page import StartPageFrame
from Admin_Interface import AdminInterfaceFrame

class UpgradeLicenseFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.build_ui()

    def on_show(self):
        if not verify_admin():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        current_plan = self.controller.subscription_plan
        if not current_plan:
            messagebox.showerror("Error", "No subscription plan found in session.")
            self.controller.show_frame(StartPageFrame)
            return False

        current_plan = current_plan.lower()

        if current_plan not in ("basic", "pro"):
            messagebox.showerror("Access Denied", "Your plan cannot be upgraded.")
            self.controller.show_frame(StartPageFrame)
            return False

        return True

    def build_ui(self):
        tk.Label(self, text="Upgrade Your Subscription").pack(pady=10)

        instructions = (
            "Enter your NEW Gumroad license key to upgrade your plan.\n\n"
            "After verification, your subscription plan will be updated\n"
            "and stored securely in your encrypted license database."
        )
        tk.Label(self, text=instructions, justify="left", wraplength=450).pack(pady=10)

        self.entry = tk.Entry(self, width=45)
        self.entry.pack(pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=15)

        tk.Button(btn_frame, text="Submit", command=self.submit).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Clear", command=self.clear).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.cancel).pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Admin Interface", command=self.admin).pack(side=tk.LEFT, padx=5)

    def submit(self):
        new_key = self.entry.get().strip()

        if not new_key:
            messagebox.showerror("Error", "Please enter a license key.")
            return

        # This calls your Gumroad verification + DB update logic
        new_plan = upgrade_license(new_key)

        if not new_plan:
            messagebox.showerror("Invalid License", "The license key is invalid or revoked.")
            return

        messagebox.showinfo(
            "Upgrade Successful",
            f"Your subscription has been upgraded to: {new_plan.capitalize()}"
        )

        clear_user()
        self.controller.show_frame(StartPageFrame)

    def clear(self):
        self.entry.delete(0, tk.END)

    def cancel(self):
        self.controller.show_frame(StartPageFrame)

    def admin(self):
        self.controller.show_frame(AdminInterfaceFrame)