# license_validator.py
import tkinter as tk
from tkinter import messagebox
import requests
import webbrowser

PRODUCT_ID = "VyL6eH6uzltRd1VdYG90xQ=="


def gumroad_verify(license_key: str) -> dict | None:
    url = "https://api.gumroad.com/v2/licenses/verify"
    payload = {
        "product_id": PRODUCT_ID,
        "license_key": license_key
    }

    try:
        return requests.post(url, data=payload).json()
    except Exception as e:
        messagebox.showerror("Validation Error", str(e))
        return None


def normalize_gumroad_variant(raw_variant, fallback_plan):
    if not raw_variant:
        return fallback_plan

    if isinstance(raw_variant, list) and raw_variant:
        raw_variant = raw_variant[0]

    raw = str(raw_variant).strip().lower()

    if "installer" in raw:
        return None  # installer cannot be standalone

    if "admin" in raw:
        return fallback_plan  # admin add-on requires base plan

    if "enterprise" in raw:
        return "enterprise"
    if "pro" in raw:
        return "pro"
    if "basic" in raw:
        return "basic"

    return fallback_plan


class LicensePageFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.build_activation_ui()
        
    # -----------------------------
    # UI
    # -----------------------------
    def build_activation_ui(self):
        tk.Label(self, text="Enter your Gumroad license key:").pack(pady=5)

        self.entry = tk.Entry(self, width=40)
        self.entry.pack(pady=5)

        welcome_text = (
            "Welcome to the Automating Innovating AI Production Manager App Pro Version!\n\n"
            "Please enter the Gumroad license key you received after purchase.\n"
            "You’ll find it on the Gumroad receipt and confirmation email.\n\n"
            "If you do not have a license key, click the button below to purchase one.\n\n"
            "Need help? Contact automatinginnovatingai@outlook.com"
        )
        tk.Label(self, text=welcome_text, justify="left", wraplength=400).pack(padx=10, pady=10)

        btn_frame = tk.Frame(self)
        btn_frame.pack(pady=10)

        tk.Button(btn_frame, text="Submit", command=self.submit, bg="green").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Retry", command=self.retry, bg="yellow").pack(side=tk.LEFT, padx=5)
        tk.Button(btn_frame, text="Cancel", command=self.cancel, bg="red").pack(side=tk.LEFT, padx=5)

        tk.Button(
            self,
            text="Purchase License on Gumroad",
            fg="blue",
            bg="gold",
            cursor="hand2",
            command=lambda: webbrowser.open("https://automateai56.gumroad.com/l/koxupw")
        ).pack(pady=5)

    # -----------------------------
    # Submit License
    # -----------------------------
    def submit(self):
        license_key = self.entry.get().strip()

        if not license_key:
            messagebox.showerror("Error", "Please enter a license key.")
            return

        response = gumroad_verify(license_key)
        if not response or not response.get("success"):
            messagebox.showerror("Invalid License", "License key is invalid or revoked.")
            return

        purchase = response.get("purchase", {})
        raw_variant = purchase.get("variants")

        subscription_plan = normalize_gumroad_variant(raw_variant, fallback_plan="basic")
        if subscription_plan is None:
            messagebox.showerror(
                "Invalid License",
                "The Installer Add-on cannot be used as a standalone license. "
                "You must have an Enterprise plan first."
            )
            return

        # Store temporarily in controller memory
        self.controller.license_key = license_key
        self.controller.subscription_plan = subscription_plan
        self.controller.last_verified = purchase.get("updated_at")

        messagebox.showinfo("License Verified", "Now configure your SQL Server connection.")
        self._go_to_sql_connection()

    # -----------------------------
    # Navigation Helpers
    # -----------------------------
    def _go_to_sql_connection(self):
        from sql_connection_page import SQLConnectionFrame
        self.controller.show_frame(SQLConnectionFrame)

    def _go_to_start_page(self):
        from startup_page import StartPageFrame
        self.controller.show_frame(StartPageFrame)

    def _go_to_license_page(self):
        from license_validator import LicensePageFrame
        self.controller.show_frame(LicensePageFrame)

    # -----------------------------
    # Buttons
    # -----------------------------
    def retry(self):
        self.entry.delete(0, tk.END)

    def cancel(self):
        self.controller.destroy()