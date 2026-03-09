import tkinter as tk
from tkinter import messagebox

class UserUpgradeFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.build_ui()  # UI only — no logic

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def build_ui(self):
        pass

    def on_show(self):
        self.after(100, self.show_upgrade_message)

    # ---------------------------------------------------------
    # UPGRADE MESSAGE
    # ---------------------------------------------------------
    def show_upgrade_message(self):
        messagebox.showinfo(
            "Upgrade to Automating Innovating AI Production Manager Pro! or Enterprise Edition.",
            "Upgrade to access premium features and improve your productivity!"
        )