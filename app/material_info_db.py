import tkinter as tk
from tkinter import messagebox, filedialog
import uuid
import pandas as pd
from Admin_Interface import AdminInterfaceFrame
from database import DatabasePortalFrame
from startup_page import StartPageFrame
from session_context import verify_admin, exit_session, enforce_plan
from db_connection import get_db_connection


class MaterialInfoDBFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.entries = {}

        # UI only – no SQL here
        self.build_ui()

    def on_show(self):
        # ADMIN CHECK
        if not verify_admin():
            messagebox.showerror("User not authorized")
            exit_session()
            return False

        # PLAN CHECK
        if not enforce_plan("pro", "enterprise"):
            messagebox.showerror("Access Denied", "You must be subscribed to a plan.")
            self.controller.show_frame(StartPageFrame)
            return False

        # SQL / activation check
        try:
            conn, cursor = get_db_connection()
            conn.close()
        except Exception:
            messagebox.showerror("Database Error", "Could not connect to database.")
            return False

        # Now safe to hit DB
        self.update_table()
        return True

    # ---------------------------------------------------------
    # UI
    # ---------------------------------------------------------
    def build_ui(self):
        self.canvas = tk.Canvas(self)
        self.scroll_y = tk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scroll_x = tk.Scrollbar(self, orient="horizontal", command=self.canvas.xview)

        self.scroll_frame = tk.Frame(self.canvas)
        self.scroll_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        self.scroll_y.pack(side="right", fill="y")
        self.scroll_x.pack(side="bottom", fill="x")

        self.button_frame = tk.Frame(self)
        self.button_frame.pack(side="top", fill="x", pady=10)

        tk.Button(
            self.button_frame,
            text="Export Data",
            command=self.export_data_to_csv,
            bg="green",
            fg="white"
        ).pack(side="left", padx=5)

        tk.Button(
            self.button_frame,
            text="Exit",
            command=exit_session,
            bg="red",
            fg="white"
        ).pack(side="left", padx=5)

        tk.Button(
            self.button_frame,
            text="Admin Interface",
            command=lambda: self.controller.show_frame(AdminInterfaceFrame),
            bg="gold",
            fg="black"
        ).pack(side="left", padx=5)

        tk.Button(
            self.button_frame,
            text="Database Portal",
            command=lambda: self.controller.show_frame(DatabasePortalFrame),
            bg="cyan",
            fg="black"
        ).pack(side="left", padx=5)

    # ---------------------------------------------------------
    # TABLE
    # ---------------------------------------------------------
    def update_table(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        cnxn = get_db_connection()
        with cnxn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM AIAI_Material_Info")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

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
            font=("Arial", 10, "bold")
        ).grid(row=0, column=len(columns), columnspan=2)

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
                command=lambda r=row: self.edit_material_info(r),
                bg="purple",
                fg="white"
            ).grid(row=i, column=len(row), padx=5, pady=5)

            tk.Button(
                self.scroll_frame,
                text="Delete",
                command=lambda r=row: self.delete_material_info(r),
                bg="red",
                fg="white"
            ).grid(row=i, column=len(row) + 1, padx=5, pady=5)

        self.build_form(len(data) + 3, len(columns))

    # ---------------------------------------------------------
    # FORM
    # ---------------------------------------------------------
    def build_form(self, row_start, col_span):
        form_frame = tk.LabelFrame(self.scroll_frame, text="Add New Material", font=("Arial", 12, "bold"))
        form_frame.grid(row=row_start, column=0, columnspan=col_span + 2, pady=20)

        fields = ["Material Name", "Material R Value", "Material Width", "Square Footage", "Pay Rate"]
        self.entries = {}

        for i, field in enumerate(fields):
            tk.Label(form_frame, text=field).grid(row=i, column=0, sticky="w", padx=10, pady=5)
            entry = tk.Entry(form_frame)
            entry.grid(row=i, column=1, padx=10, pady=5)
            self.entries[field] = entry

        tk.Button(
            form_frame,
            text="Save",
            command=self.save_material,
            bg="green",
            fg="white"
        ).grid(row=len(fields), column=0, columnspan=2, pady=10)

    # ---------------------------------------------------------
    # SAVE MATERIAL
    # ---------------------------------------------------------
    def save_material(self):
        material_id = str(uuid.uuid4())
        data = (
            material_id,
            self.entries["Material Name"].get(),
            self.entries["Material R Value"].get(),
            self.entries["Material Width"].get(),
            self.entries["Square Footage"].get(),
            self.entries["Pay Rate"].get()
        )

        try:
            cnxn = get_db_connection()
            with cnxn as conn:
                cursor = conn.cursor()
                # Table creation should be handled in migrations / schema init, not here.
                cursor.execute(
                    '''
                    INSERT INTO AIAI_Material_Info (
                        material_id, material_name, material_r_value,
                        material_width, square_footage, pay_rate
                    ) VALUES (?, ?, ?, ?, ?, ?)
                    ''',
                    data
                )
                conn.commit()

            messagebox.showinfo("Success", "Material data saved successfully!")
            self.update_table()

        except Exception as e:
            messagebox.showerror("Database Error", f"An error occurred: {e}")

    # ---------------------------------------------------------
    # EDIT MATERIAL
    # ---------------------------------------------------------
    def edit_material_info(self, row):
        win = tk.Toplevel(self)
        win.title("Edit Material Info")

        edit_entries = []
        for i, value in enumerate(row[1:]):
            tk.Label(win, text=f"Field {i+1}").grid(row=0, column=i)
            entry = tk.Entry(win)
            entry.insert(0, value)
            entry.grid(row=1, column=i)
            edit_entries.append(entry)

        def save_changes():
            new_values = [e.get() for e in edit_entries]
            cnxn = get_db_connection()
            with cnxn as conn:
                cursor = conn.cursor()
                cursor.execute(
                    '''
                    UPDATE AIAI_Material_Info SET
                        material_name = ?,
                        material_r_value = ?,
                        material_width = ?,
                        square_footage = ?,
                        pay_rate = ?
                    WHERE material_id = ?
                    ''',
                    (*new_values, row[0])
                )
                conn.commit()

            win.destroy()
            self.update_table()

        tk.Button(win, text="Save", command=save_changes).grid(row=2, column=len(row) // 2)

    # ---------------------------------------------------------
    # DELETE MATERIAL
    # ---------------------------------------------------------
    def delete_material_info(self, row):
        if not messagebox.askyesno("Confirm Delete", "Are you sure you want to delete this record?"):
            return

        cnxn = get_db_connection()
        with cnxn as conn:
            cursor = conn.cursor()
            cursor.execute("DELETE FROM AIAI_Material_Info WHERE material_id = ?", (row[0],))
            conn.commit()

        self.update_table()

    # ---------------------------------------------------------
    # EXPORT CSV
    # ---------------------------------------------------------
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
                df = pd.read_sql_query("SELECT * FROM AIAI_Material_Info", conn)
                df.to_csv(file_path, index=False)

            messagebox.showinfo("Export Success", "Data exported successfully.")

        except Exception as e:
            messagebox.showerror("Export Error", f"An error occurred: {e}")


def main():
    pass