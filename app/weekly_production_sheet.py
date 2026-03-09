import tkinter as tk
from tkinter import messagebox
from db_connection import get_db_connection
from session_context import verify_admin, enforce_plan, exit_session
from Admin_Interface import AdminInterfaceFrame
from startup_page import StartPageFrame
from database import DatabasePortalFrame


class WeeklyProductionSheetFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.table_name = "AIAI_Weekly_Payroll"
        self._scroll_frame = None   # will be set in build_main_view()

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

        # Build UI fresh
        self.build_main_view()

        # Load SQL table AFTER activation is verified
        self.render_table(self._scroll_frame)
        return True

    # ---------------------------------------------------------
    # MAIN VIEW (UI ONLY — NO SQL HERE)
    # ---------------------------------------------------------
    def build_main_view(self):
        for w in self.winfo_children():
            w.destroy()

        button_frame = tk.Frame(self)
        button_frame.grid(row=0, column=0, columnspan=100, sticky="ew", pady=10)

        tk.Button(
            button_frame,
            text="Exit",
            bg="red",
            fg="white",
            command=self.controller.destroy
        ).grid(row=0, column=0, padx=5)

        tk.Button(
            button_frame,
            text="Admin Interface",
            bg="gold",
            fg="black",
            command=lambda: self.controller.show_frame(AdminInterfaceFrame)
        ).grid(row=0, column=1, padx=5)

        tk.Button(
            button_frame,
            text="Database Portal",
            bg="blue",
            fg="black",
            command=lambda: self.controller.show_frame(DatabasePortalFrame)
        ).grid(row=0, column=2, padx=5)

        tk.Label(
            button_frame,
            text="Automating Innovating AI Production Manager App",
            font=("Arial", 14, "bold"),
            fg="navy"
        ).grid(row=0, column=3, padx=20, sticky="w", columnspan=10)

        canvas = tk.Canvas(self)
        scrollbar_y = tk.Scrollbar(self, orient="vertical", command=canvas.yview)
        scrollbar_x = tk.Scrollbar(self, orient="horizontal", command=canvas.xview)
        scroll_frame = tk.Frame(canvas)

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        scrollbar_x.grid(row=2, column=0, sticky="ew")

        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # Store scroll_frame for later SQL loading
        self._scroll_frame = scroll_frame

    # ---------------------------------------------------------
    # RENDER TABLE (SQL OK — called after activation)
    # ---------------------------------------------------------
    def render_table(self, parent):
        # Clear old table content
        for w in parent.winfo_children():
            w.destroy()

        cnxn = get_db_connection()
        with cnxn as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = ?
            """, (self.table_name,))
            all_columns = [row[0] for row in cursor.fetchall()]

        excluded = {"Salt", "Employee_Hashed_ID", "payroll_id"}
        display_columns = [c for c in all_columns if c not in excluded]

        select_cols = ["payroll_id"] + display_columns

        with cnxn as conn:
            cursor = conn.cursor()
            cursor.execute(f"SELECT {', '.join(select_cols)} FROM {self.table_name}")
            data = cursor.fetchall()

        if not data:
            tk.Label(parent, text="No data found.", font=("Arial", 12, "italic")).grid(
                row=2, column=0, columnspan=len(display_columns) + 2
            )
            return

        # Header
        for j, col in enumerate(display_columns):
            tk.Label(
                parent,
                text=col,
                font=("Arial", 10, "bold"),
                bg="lightgray",
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5
            ).grid(row=1, column=j, sticky="nsew")

        tk.Label(parent, text="Edit", font=("Arial", 10, "bold"), bg="lightgray").grid(
            row=1, column=len(display_columns)
        )
        tk.Label(parent, text="Delete", font=("Arial", 10, "bold"), bg="lightgray").grid(
            row=1, column=len(display_columns) + 1
        )

        for i, row in enumerate(data, start=2):
            payroll_id = row[0]
            values = row[1:]

            for j, val in enumerate(values):
                tk.Label(
                    parent,
                    text="" if val is None else str(val),
                    borderwidth=1,
                    relief="solid",
                    padx=5,
                    pady=5,
                    anchor="w"
                ).grid(row=i, column=j, sticky="nsew")

            tk.Button(
                parent,
                text="Edit",
                bg="lightblue",
                command=lambda pid=payroll_id: self.open_edit_window(pid)
            ).grid(row=i, column=len(display_columns), sticky="nsew")

            tk.Button(
                parent,
                text="Delete",
                bg="salmon",
                command=lambda pid=payroll_id: self.delete_record(pid)
            ).grid(row=i, column=len(display_columns) + 1, sticky="nsew")

    # ---------------------------------------------------------
    # DELETE RECORD
    # ---------------------------------------------------------
    def delete_record(self, payroll_id):
        if not messagebox.askyesno("Confirm Delete", "Delete this record?"):
            return

        cnxn = get_db_connection()
        with cnxn as conn:
            cursor = conn.cursor()
            cursor.execute(
                f"DELETE FROM {self.table_name} WHERE payroll_id = ?",
                (payroll_id,)
            )
            conn.commit()

        # Refresh table
        self.render_table(self._scroll_frame)

    # ---------------------------------------------------------
    # EDIT WINDOW
    # ---------------------------------------------------------
    def open_edit_window(self, payroll_id):
        edit = tk.Toplevel(self)
        edit.title("Edit Weekly Production Info")
        edit.attributes("-fullscreen", True)

        tk.Label(
            edit,
            text="Automating Innovating AI Production Manager App",
            font=("Arial", 14, "bold"),
            fg="navy"
        ).grid(row=0, column=0, columnspan=10, pady=10)

        canvas = tk.Canvas(edit)
        scrollbar_y = tk.Scrollbar(edit, orient="vertical", command=canvas.yview)
        scrollbar_x = tk.Scrollbar(edit, orient="horizontal", command=canvas.xview)
        frame = tk.Frame(canvas)

        frame.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))
        canvas.create_window((0, 0), window=frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        canvas.grid(row=1, column=0, sticky="nsew")
        scrollbar_y.grid(row=1, column=1, sticky="ns")
        scrollbar_x.grid(row=2, column=0, sticky="ew")

        edit.grid_rowconfigure(1, weight=1)
        edit.grid_columnconfigure(0, weight=1)

        cnxn = get_db_connection()
        with cnxn as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT COLUMN_NAME
                FROM INFORMATION_SCHEMA.COLUMNS
                WHERE TABLE_NAME = ?
            """, (self.table_name,))
            all_columns = [row[0] for row in cursor.fetchall()]

            excluded = {"Salt", "Employee_Hashed_ID", "payroll_id"}
            display_columns = [c for c in all_columns if c not in excluded]

            cursor.execute(
                f"SELECT {', '.join(display_columns)} FROM {self.table_name} WHERE payroll_id = ?",
                (payroll_id,)
            )
            current_row = cursor.fetchone()

        if not current_row:
            messagebox.showerror("Error", "Record not found.")
            edit.destroy()
            return

        col_map = dict(zip(display_columns, current_row))
        entries = {}

        for i, col in enumerate(display_columns):
            tk.Label(
                frame,
                text=col,
                font=("Arial", 10, "bold"),
                bg="lightgray",
                borderwidth=1,
                relief="solid",
                padx=5,
                pady=5
            ).grid(row=0, column=i, sticky="nsew")

            e = tk.Entry(frame, width=20)
            e.insert(0, "" if col_map.get(col) is None else str(col_map.get(col)))
            e.grid(row=1, column=i, padx=5, pady=5)
            entries[col] = e

        def save_changes():
            try:
                updated_values = [entries[col].get() for col in display_columns]

                cnxn = get_db_connection()
                with cnxn as conn:
                    cursor = conn.cursor()
                    update_clause = ", ".join([f"{col} = ?" for col in display_columns])
                    cursor.execute(
                        f"""
                        UPDATE {self.table_name}
                        SET {update_clause}
                        WHERE payroll_id = ?
                        """,
                        (*updated_values, payroll_id)
                    )
                    conn.commit()

                messagebox.showinfo("Saved", "Data saved successfully.")
                edit.destroy()
                self.render_table(self._scroll_frame)

            except Exception as e:
                messagebox.showerror("Database Error", str(e))

        def export_data_to_csv():
            import CSV_File
            CSV_File.export_to_excel()

        btn_frame = tk.Frame(edit)
        btn_frame.grid(row=3, column=0, pady=20, sticky="ew")

        tk.Button(
            btn_frame,
            text="Save Changes",
            bg="blue",
            fg="white",
            command=save_changes
        ).grid(row=0, column=0, padx=10)

        tk.Button(
            btn_frame,
            text="Export to Excel",
            bg="green",
            fg="white",
            command=export_data_to_csv
        ).grid(row=0, column=1, padx=10)

        tk.Button(
            btn_frame,
            text="Weekly Production Info",
            bg="gold",
            fg="black",
            command=lambda: [edit.destroy(), self.render_table(self._scroll_frame)]
        ).grid(row=0, column=2, padx=10)


def main():
    pass