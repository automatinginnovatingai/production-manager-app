import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


INSTRUCTIONS_TEXT = """
Production Manager App - User Guide

Welcome to the Automating Innovating AI Production Manager App — a streamlined, secure, and intuitive tool 
for managing production workflows, employee payroll, and data exports.

Key Features:
--------------
• Secure Login:
  Encrypted password protection with industry-standard hashing.

• Payroll Management:
  - Input and calculate weekly payroll.
  - Material usage calculations:
      • Sqft/Bags Installed × Pay Per Tube/Piece Rate
      • Bag method: 5 bags × $4.50 = $22.50
      • Square footage: 2000 ft² × $0.045 = $90.00
      • Hourly wage: 10 hours × $17.45 = $174.50
      • Enter 0 in unused fields
  - Add up to four employees per job.
  - Automatic pay splitting.

• Employee Job Entry:
  Requires:
    - First/Last Name
    - Employee ID
    - Hours worked
    - Job role
    - Builder
    - Job site
    - Model name
    - Lot/Block
    - Optional insulation product details

• Pay Week Entry & Auto Export:
  - Set start and end day of payroll period.
  - Payroll auto-exports 2 days after end day.
  - Requires verified session.
  - Exports grouped payroll to Excel:
      Documents/AIAI_PM_App/Payroll_Excels/YYYY-MM/Payroll_YYYY-MM.xlsx
  - Each employee gets a sheet labeled by week number.
  - Totals auto-calculated.

• Data Protection:
  - Automatic de-duplication.
  - Smart cleanup of older records.

• Reporting:
  - Clean CSV exports.
  - Customizable filenames.

• Auto-Updating:
  - App checks for updates.

• Friendly Interface:
  - Simple and fast.

System Requirements:
---------------------
• Microsoft Excel required.
• 70 MB disk space.
• 4–8 GB RAM recommended.
• Local payroll data storage.
• Monthly Excel files with daily worksheets.

Getting Started:
----------------
1. Launch the app.
2. Register admin.
3. Login as admin.
4. Access Admin Interface.
5. Begin entering job/payroll data.

Navigation & Exiting:
---------------------
• Use dashboard to access modules.
• Exit button available on all screens.

Tips:
-----
• Export data regularly.
• Use strong admin credentials.
• Keep Excel updated.

Support:
--------
automatinginnovatingai@outlook.com

Thank you for using Production Manager App!
"""


class UserGuideFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.build_ui()

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def build_ui(self):
        title = tk.Label(
            self,
            text="Production Manager App - User Guide",
            font=("Helvetica", 24, "bold")
        )
        title.pack(pady=20)

        frame = ttk.Frame(self, padding="10")
        frame.pack(fill=tk.BOTH, expand=True)

        text_frame = ttk.Frame(frame)
        text_frame.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(text_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        text_widget = tk.Text(
            text_frame,
            wrap=tk.WORD,
            yscrollcommand=scrollbar.set,
            font=("Segoe UI", 11)
        )
        text_widget.insert(tk.END, INSTRUCTIONS_TEXT)
        text_widget.config(state=tk.DISABLED)
        text_widget.pack(fill=tk.BOTH, expand=True)

        scrollbar.config(command=text_widget.yview)

        button_frame = ttk.Frame(frame, padding="10")
        button_frame.pack(fill=tk.X, side=tk.BOTTOM)

        ttk.Button(
            button_frame,
            text="Return to Main Menu",
            command=self.go_to_start_page
        ).pack(side=tk.RIGHT, padx=5)

    def go_to_start_page(self):
        from startup_page import StartPageFrame
        self.controller.show_frame(StartPageFrame) 

def main():
    pass