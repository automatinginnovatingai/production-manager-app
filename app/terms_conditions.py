import tkinter as tk
from tkinter import messagebox
from tkinter.scrolledtext import ScrolledText
from db_connection import get_db_connection
from session_context import exit_session, get_user_key, enforce_plan, get_user
from startup_page import StartPageFrame


TERMS_TEXT = """Terms and Conditions, User Agreement, and Licensing Document
Automating and Innovating AI, LLC
Effective Date: November 5, 2024
1. Introduction
Welcome to Automating and Innovating AI, LLC. By accessing or using our proprietary software ("Software"), you agree to be bound by these Terms and Conditions, User Agreement, and Licensing Document (collectively, the "Agreement"). If you do not agree to these terms, you must not use the Software.
2. License Grant
Automating and Innovating AI, LLC grants you a non-exclusive, non-transferable, revocable license to use the Software strictly in accordance with this Agreement.
3. Restrictions
You agree not to, and you will not permit others to:
• Alteration: Modify, alter, translate, or create derivative works of the Software.
• Manipulation: Reverse engineer, decompile, disassemble, or attempt to derive the source code of the Software.
• Stealing: Use the Software in any manner that could damage, disable, overburden, or impair the Software.
• Illegal Sharing: Distribute, share, lease, rent, loan, or sublicense the Software.
• Copying: Copy the Software, except as expressly permitted under this Agreement.
• Unauthorized Access: Gain unauthorized access to any part of the Software or its related systems or networks. This is a one computer use. No refunds.
4. Intellectual Property
The Software and all intellectual property rights therein are and shall remain the exclusive property of Automating and Innovating AI, LLC.
5. Confidentiality
You acknowledge that the Software contains proprietary and confidential information of Automating and Innovating AI, LLC.
6. Termination
This Agreement is effective until terminated. Your rights terminate automatically if you fail to comply.
7. Indemnification
You agree to indemnify and hold harmless Automating and Innovating AI, LLC.
8. Limitation of Liability
Automating and Innovating AI, LLC is not liable for damages.
9. Governing Law
This Agreement is governed by U.S. law.
10. Entire Agreement
This Agreement supersedes all prior agreements.
11. Amendments
Automating and Innovating AI, LLC may modify this Agreement at any time.
12. Data Usage
User agrees that all user and company data may be used indefinitely.
"""


class TermsConditionsFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.build_ui()

    def on_show(self):

        # PLAN CHECK
        if not enforce_plan("basic", "pro", "enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            self.controller.show_frame(StartPageFrame)
            return False

        return True  

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def build_ui(self):
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        canvas.pack(side="left", fill="both", expand=True)

        scrollbar = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        scrollbar.pack(side="right", fill="y")

        scroll_frame = tk.Frame(canvas)
        scroll_frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        title = tk.Label(
            scroll_frame,
            text="Automating Innovating AI - Production Manager App",
            font=("Segoe UI", 35, "bold")
        )
        title.pack(pady=20)

        text_box = ScrolledText(scroll_frame, wrap="word", width=150, height=30)
        text_box.insert(tk.END, TERMS_TEXT)
        text_box.config(state=tk.DISABLED)
        text_box.pack(fill="both", expand=True, padx=20, pady=20)

        btn_frame = tk.Frame(scroll_frame)
        btn_frame.pack(pady=20)

        tk.Button(btn_frame, text="I Agree", width=20, command=self.on_agree).pack(side="left", padx=20)
        tk.Button(btn_frame, text="I Disagree", width=20, command=self.on_disagree).pack(side="right", padx=20)

    # ---------------------------------------------------------
    # AGREE
    # ---------------------------------------------------------
    def on_agree(self):
        user_key = get_user_key()
        username = get_user()

        if not username:
            messagebox.showerror("Session error", "Missing username.")
            return

        agreed_value = "Agreed"
        agreed = agreed_value

        try:
            cnxn = get_db_connection()
            with cnxn as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "UPDATE users SET agreed=? WHERE username=?",
                    (agreed, username)
                )
                conn.commit()

            messagebox.showinfo("Success", "Agreement status updated.")
            from Admin_Interface import AdminInterfaceFrame
            self.controller.show_frame(AdminInterfaceFrame)

        except Exception as e:
            messagebox.showerror("Database Error", f"{e}")

    # ---------------------------------------------------------
    # DISAGREE
    # ---------------------------------------------------------
    def on_disagree(self):
        messagebox.showerror("Access Denied", "You must agree to continue.")
        exit_session()

def main(self):
    pass