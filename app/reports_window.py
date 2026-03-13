import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from fpdf import FPDF
from openpyxl import Workbook
import win32print
import win32api
import tempfile
import os


class ReportsWindow(tk.Toplevel):
    def __init__(self, parent, data_rows, report_title="Report"):
        super().__init__(parent)

        self.data_rows = data_rows
        self.report_title = report_title

        self.title(f"Reports - {report_title}")
        self.geometry("420x260")
        self.resizable(False, False)

        main_frame = tk.Frame(self)
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        tk.Label(
            main_frame,
            text="Select a report action:",
            font=("Arial", 12, "bold")
        ).pack(pady=(0, 15))

        # -----------------------------
        # PDF BUTTON (RED)
        # -----------------------------
        pdf_btn = tk.Button(
            main_frame,
            text="Export to PDF",
            width=25,
            bg="#B22222",
            fg="white",
            activebackground="#8B1A1A",
            command=self.export_to_pdf
        )
        pdf_btn.pack(pady=5)

        # -----------------------------
        # EXCEL BUTTON (GREEN)
        # -----------------------------
        excel_btn = tk.Button(
            main_frame,
            text="Export to Excel",
            width=25,
            bg="#1D6F42",
            fg="white",
            activebackground="#14532D",
            command=self.export_to_excel
        )
        excel_btn.pack(pady=5)

        # -----------------------------
        # PRINT BUTTON (BLUE-GRAY)
        # -----------------------------
        print_btn = tk.Button(
            main_frame,
            text="Print",
            width=25,
            bg="#3A4A5A",
            fg="white",
            activebackground="#2C3947",
            command=self.print_report
        )
        print_btn.pack(pady=5)

    # ---------------------------------------------------------
    # REAL PDF EXPORT (FPDF2)
    # ---------------------------------------------------------
    def export_to_pdf(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("PDF files", "*.pdf")],
            title="Save PDF Report"
        )
        if not file_path:
            return

        try:
            pdf = FPDF()
            pdf.add_page()
            pdf.set_font("Arial", size=12)

            pdf.cell(200, 10, txt=self.report_title, ln=True, align="C")
            pdf.ln(5)

            for row in self.data_rows:
                line = " | ".join([str(x) for x in row])
                pdf.multi_cell(0, 8, txt=line)

            pdf.output(file_path)

            messagebox.showinfo("PDF Export", f"PDF saved:\n{file_path}")

        except Exception as e:
            messagebox.showerror("PDF Error", f"Failed to export PDF:\n{e}")

    # ---------------------------------------------------------
    # REAL EXCEL EXPORT (openpyxl)
    # ---------------------------------------------------------
    def export_to_excel(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx")],
            title="Save Excel Report"
        )
        if not file_path:
            return

        try:
            wb = Workbook()
            ws = wb.active
            ws.title = "Report"

            # Write header row
            headers = [
                "First Name", "Last Name", "Employee ID", "Hours", "Job Title",
                "Builder", "Jobsite", "Model", "Lot", "Block",
                "Material1", "Material2", "Material3", "Material4",
                "Material5", "Material6", "Material7", "Pay"
            ]
            ws.append(headers)

            # Write data rows
            for row in self.data_rows:
                ws.append(list(row))

            wb.save(file_path)

            messagebox.showinfo("Excel Export", f"Excel file saved:\n{file_path}")

        except Exception as e:
            messagebox.showerror("Excel Error", f"Failed to export Excel:\n{e}")

    # ---------------------------------------------------------
    # REAL PRINTING (pywin32)
    # ---------------------------------------------------------
    def print_report(self):
        try:
            # Create a temporary text file to print
            temp_file = tempfile.mktemp(".txt")

            with open(temp_file, "w", encoding="utf-8") as f:
                f.write(self.report_title + "\n\n")
                for row in self.data_rows:
                    line = " | ".join([str(x) for x in row])
                    f.write(line + "\n")

            # Send to printer
            win32api.ShellExecute(
                0,
                "print",
                temp_file,
                None,
                ".",
                0
            )

            messagebox.showinfo("Print", "Report sent to printer.")

        except Exception as e:
            messagebox.showerror("Print Error", f"Failed to print:\n{e}")