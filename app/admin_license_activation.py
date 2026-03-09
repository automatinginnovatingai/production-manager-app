import tkinter as tk
from tkinter import messagebox
import requests
import hmac
import hashlib

from db_connection import get_db_connection
from license_validator import gumroad_verify, normalize_gumroad_variant


class AdminLicenseActivationFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.build_ui()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def build_ui(self):
        tk.Label(
            self,
            text="Admin License Activation",
            font=("Arial", 22, "bold")
        ).pack(pady=20)

        tk.Label(
            self,
            text="Enter your Admin Add‑on Gumroad license key:",
            font=("Arial", 12)
        ).pack(pady=5)

        self.license_entry = tk.Entry(self, width=45)
        self.license_entry.pack(pady=5)

        tk.Button(
            self,
            text="Activate",
            bg="green",
            fg="white",
            command=self.activate_license
        ).pack(pady=10)

        tk.Button(
            self,
            text="Cancel",
            bg="red",
            fg="white",
            command=self.cancel
        ).pack(pady=5)

    # ---------------------------------------------------------
    # LICENSE ACTIVATION LOGIC
    # ---------------------------------------------------------
    def activate_license(self):
        license_key = self.license_entry.get().strip()

        if not license_key:
            messagebox.showerror("Error", "Please enter a license key.")
            return

        # Verify with Gumroad
        response = gumroad_verify(license_key)
        if not response or not response.get("success"):
            messagebox.showerror("Invalid License", "License key is invalid or revoked.")
            return

        purchase = response.get("purchase", {})
        raw_variant = purchase.get("variants")

        # Admin Add‑on must not be used alone
        subscription_plan = normalize_gumroad_variant(raw_variant, fallback_plan="basic")
        if subscription_plan is None:
            messagebox.showerror(
                "Invalid License",
                "The Admin Add‑on cannot be used as a standalone license.\n"
                "A Basic, Pro, or Enterprise plan is required first."
            )
            return

        # Hash the license key for secure storage
        license_hash = hmac.new(
            key=b"ADMIN_LICENSE_SECRET_KEY",  # Replace with your real secret
            msg=license_key.encode(),
            digestmod=hashlib.sha256
        ).digest()

        admin_id = self.controller.pending_admin_id
        if not admin_id:
            messagebox.showerror("Error", "No admin account found for activation.")
            return

        # Insert into admin_licenses table
        conn = get_db_connection()
        cursor = conn.cursor()

        cursor.execute("""
            INSERT INTO admin_licenses (admin_id, license_hash, plan_type, is_main_admin)
            VALUES (?, ?, ?, 0)
        """, (
            admin_id,
            license_hash,
            subscription_plan
        ))

        conn.commit()
        conn.close()

        messagebox.showinfo("Success", "Admin license activated successfully!")

        # Redirect to admin interface
        from Admin_Interface import AdminInterfaceFrame
        self.controller.show_frame(AdminInterfaceFrame)

    # ---------------------------------------------------------
    # CANCEL
    # ---------------------------------------------------------
    def cancel(self):
        messagebox.showinfo("Cancelled", "Admin license activation cancelled.")
        from user_login import UserLoginFrame
        self.controller.show_frame(UserLoginFrame)