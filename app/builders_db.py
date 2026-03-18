import tkinter as tk
from tkinter import messagebox, filedialog
import pandas as pd
from session_context import exit_session, verify_admin, enforce_plan
from db_connection import get_db_connection
from startup_page import StartPageFrame
from Admin_Interface import AdminInterfaceFrame
from database import DatabasePortalFrame


class BuildersDBFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.table_name = "AIAI_Builders_Info"

        # Main container
        self.outer_frame = tk.Frame(self)
        self.outer_frame.pack(fill="both", expand=True)

        # Canvas + scrollbars
        self.canvas = tk.Canvas(self.outer_frame)
        self.scrollbar_y = tk.Scrollbar(self.outer_frame, orient="vertical", command=self.canvas.yview)
        self.scrollbar_x = tk.Scrollbar(self.outer_frame, orient="horizontal", command=self.canvas.xview)

        self.canvas.configure(yscrollcommand=self.scrollbar_y.set, xscrollcommand=self.scrollbar_x.set)

        self.scrollbar_y.pack(side="right", fill="y")
        self.scrollbar_x.pack(side="bottom", fill="x")
        self.canvas.pack(side="left", fill="both", expand=True)

        # Frame inside canvas
        self.scroll_frame = tk.Frame(self.canvas)
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))

    # ----------------------------------------------------------------------
    # on_show — NOW loads the table safely
    # ----------------------------------------------------------------------
    def on_show(self):
        if not verify_admin():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        if not enforce_plan("pro", "enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            self.controller.show_frame(StartPageFrame)
            return False

        # Ensure SQL Server is configured BEFORE loading table
        try:
            conn = get_db_connection()
            conn.close()
        except Exception:
            messagebox.showerror("Database Error", "Could not connect to database.")
            return False

        # NOW it is safe to load the table
        self.update_table()
        return True

    # ----------------------------------------------------------------------
    # Navigation
    # ----------------------------------------------------------------------
    def exit_app(self):
        exit_session()

    def admin_interface(self):
        self.controller.show_frame(AdminInterfaceFrame)

    def return_to_database_portal(self):
        self.controller.show_frame(DatabasePortalFrame)

    # ----------------------------------------------------------------------
    # Load & Display Table
    # ----------------------------------------------------------------------
    def update_table(self):
        # Clear old widgets
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        # Safe DB connection (activation already validated in on_show)
        cnxn = get_db_connection()
        with cnxn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM AIAI_Builders_Info")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

        # Column headers
        for j, col_name in enumerate(columns):
            tk.Label(
                self.scroll_frame,
                text=col_name,
                font=("Arial", 10, "bold"),
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5
            ).grid(row=0, column=j, sticky="nsew")

        tk.Label(
            self.scroll_frame,
            text="Actions",
            font=("Arial", 10, "bold"),
            borderwidth=1,
            relief="solid",
            padx=5,
            pady=5
        ).grid(row=0, column=len(columns), columnspan=2, sticky="nsew")

        # Data rows
        for i, row in enumerate(data, start=1):

            for j, value in enumerate(row):
                tk.Label(
                    self.scroll_frame,
                    text=value,
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5
                ).grid(row=i, column=j, sticky="nsew")

            tk.Button(
                self.scroll_frame,
                text="Edit",
                command=lambda r=row: self.edit_builder_info(r),
                bg="purple"
            ).grid(row=i, column=len(row))

            tk.Button(
                self.scroll_frame,
                text="Delete",
                command=lambda r=row: self.delete_builder_info(r),
                bg="red"
            ).grid(row=i, column=len(row) + 1)

        # Bottom buttons
        tk.Button(
            self.scroll_frame,
            text="Export Data",
            bg="gold",
            command=self.export_data_to_csv
        ).grid(row=len(data) + 1, column=0, columnspan=2, pady=10)

        tk.Button(
            self.scroll_frame,
            text="Exit",
            command=self.exit_app,
            bg="red"
        ).grid(row=len(data) + 2, column=0, columnspan=2)

        tk.Button(
            self.scroll_frame,
            text="Admin Interface",
            command=self.admin_interface,
            bg="green"
        ).grid(row=len(data) + 2, column=2, columnspan=2)

        tk.Button(
            self.scroll_frame,
            text="Database Portal",
            command=self.return_to_database_portal,
            bg="blue"
        ).grid(row=len(data) + 2, column=4, columnspan=2)

    # ----------------------------------------------------------------------
    # Edit Builder Info
    # ----------------------------------------------------------------------
    def edit_builder_info(self, row):
        edit_window = tk.Toplevel(self)
        edit_window.title("Edit Builder Info")

        entries = []

        for i, value in enumerate(row):
            tk.Label(edit_window, text=f"{i+1}").grid(row=0, column=i)
            entry = tk.Entry(edit_window)
            entry.insert(0, value)
            entry.grid(row=1, column=i)
            entries.append(entry)

        def save_changes():
            new_values = [e.get() for e in entries]
            identifier = row[0]  # builder_name (primary key or unique)

            cnxn = get_db_connection()
            with cnxn as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    UPDATE AIAI_Builders_Info SET 
                        builder_name=?, jobsite_name=?, jobsite_address=?, city=?, state=?, zip_code=?,
                        model_name=?, jobsite_lot_number=?, builder_block_number=?, job_total_sq_ft=?, 
                        ext_block_sq_footage=?, ceiling_area_sq_footage=?, garage_ceiling_sq_footage=?, 
                        garage_wall_sq_footage=?, int_wall_sq_footage=?, miscellaneous_info=?
                    WHERE builder_name=?
                ''', new_values + [identifier])
                conn.commit()

            edit_window.destroy()
            self.update_table()

        tk.Button(edit_window, text="Save", command=save_changes).grid(row=2, column=len(row) // 2)

    # ----------------------------------------------------------------------
    # Delete Builder Info
    # ----------------------------------------------------------------------
    def delete_builder_info(self, row):
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            return

        identifier = row[0]  # builder_name

        cnxn = get_db_connection()
        with cnxn as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM AIAI_Builders_Info WHERE builder_name=?", (identifier,))
            conn.commit()

        self.update_table()

    # ----------------------------------------------------------------------
    # Export CSV
    # ----------------------------------------------------------------------
    def export_data_to_csv(self):
        try:
            file_path = filedialog.asksaveasfilename(
                defaultextension=".csv",
                filetypes=[("CSV files", "*.csv")]
            )
            if not file_path:
                return

            cnxn = get_db_connection()
            with cnxn as conn:
                cursor = conn.cursor()
                cursor.execute("SELECT * FROM AIAI_Builders_Info")
                rows = cursor.fetchall()
                columns = [desc[0] for desc in cursor.description]

            df = pd.DataFrame(rows, columns=columns)
            df.to_csv(file_path, index=False)

            messagebox.showinfo("Export Success", "Data exported successfully.")

        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred: {e}")