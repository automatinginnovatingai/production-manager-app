import tkinter as tk
from tkinter import messagebox
import datetime
from CSV_View import CSV_ViewFrame
from employee_interface import InstallerDailyWorkFrame
from session_context import exit_session, verify_installer, enforce_installer_plan


class InstallerInterfaceFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.build_ui()
        self.update_time()
        
    def on_show(self):
        # ADMIN CHECK
        if not verify_installer():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        # PLAN CHECK
        if not enforce_installer_plan("enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            from startup_page import StartPageFrame
            self.controller.show_frame(StartPageFrame)
            return False

        return True
    # ---------------------------------------------------------
    # UI BUILD
    # ---------------------------------------------------------
    def build_ui(self):
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(0, weight=1)

        frame = tk.Frame(self)
        frame.grid(row=0, column=0, sticky="nsew")
        frame.grid_rowconfigure(0, weight=1)
        frame.grid_columnconfigure(0, weight=1)

        title = tk.Label(
            frame,
            text="Automating Innovating AI, LLC - Production Manager Dashboard",
            font=("Arial", 16, "bold")
        )
        title.pack(padx=20, pady=10)

        # ---------------------------------------------------------
        # Buttons
        # ---------------------------------------------------------
        buttons_frame = tk.Frame(frame)
        buttons_frame.pack()

        buttons = [
            ("Production Portal", lambda: self.controller.show_frame(InstallerDailyWorkFrame), "brown"),
            ("Production Sheet", lambda: self.controller.show_frame(CSV_ViewFrame), "purple"),
            ("Exit", exit_session, "red")
        ]

        for text, cmd, color in buttons:
            tk.Button(
                buttons_frame,
                text=text,
                command=cmd,
                font=("Arial", 12, "bold"),
                bg=color,
                width=20
            ).pack(padx=20, pady=10)

        # ---------------------------------------------------------
        # Calendar
        # ---------------------------------------------------------
        calendar_frame = tk.LabelFrame(frame, text="Calendar", font=("Arial", 12, "bold"))
        calendar_frame.pack(padx=20, pady=10)

        tk.Label(calendar_frame, text="Time", font=("Arial", 10)).pack(padx=10, pady=5)

        self.time_frame = tk.Label(calendar_frame, text="", font=("Arial", 10))
        self.time_frame.pack(padx=10, pady=5)

        self.date_frame = tk.Label(calendar_frame, text="", font=("Arial", 10))
        self.date_frame.pack(padx=10, pady=5)

    # ---------------------------------------------------------
    # TIME UPDATE
    # ---------------------------------------------------------
    def update_time(self):
        now = datetime.datetime.now()
        self.time_frame.config(text=now.strftime("%H:%M:%S"))
        self.date_frame.config(text=now.strftime("%m/%d/%Y"))
        self.after(1000, self.update_time)


def main():
    pass