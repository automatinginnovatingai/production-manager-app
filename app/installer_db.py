import tkinter as tk
from tkinter import messagebox
from Admin_Interface import AdminInterfaceFrame
from database import DatabasePortalFrame
from startup_page import StartPageFrame
from session_context import verify_admin, exit_session, enforce_plan
from db_connection import get_db_connection
from path_utils import hash_password


class InstallerDBFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller
        self.build_ui()   # UI only — no SQL here

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

        # SQL CHECK — ensure activation + SQL config exists
        try:
            conn, cursor = get_db_connection()
            conn.close()
        except Exception:
            messagebox.showerror("Database Error", "Could not connect to database.")
            return False

        # NOW load table safely
        self.load_table()
        return True

    # ---------------------------------------------------------
    # MAIN UI (NO SQL HERE)
    # ---------------------------------------------------------
    def build_ui(self):
        title = tk.Label(
            self,
            text="Automating Innovating AI Production Manager App - Employee Info Dashboard",
            font=("Arial", 16, "bold"),
            pady=10
        )
        title.pack()

        # Scrollable container
        container = tk.Frame(self)
        container.pack(fill="both", expand=True)

        # Canvas
        self.canvas = tk.Canvas(container, highlightthickness=0)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        # Scrollbars
        self.scroll_y = tk.Scrollbar(container, orient="vertical", command=self.canvas.yview)
        self.scroll_y.grid(row=0, column=1, sticky="ns")

        self.scroll_x = tk.Scrollbar(container, orient="horizontal", command=self.canvas.xview)
        self.scroll_x.grid(row=1, column=0, sticky="ew")

        self.canvas.configure(yscrollcommand=self.scroll_y.set, xscrollcommand=self.scroll_x.set)

        # Frame inside canvas
        self.scroll_frame = tk.Frame(self.canvas)
        self.window = self.canvas.create_window((0, 0), window=self.scroll_frame, anchor="nw")

        # Update scrollregion when inner frame changes size
        def update_scrollregion(event):
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))

        self.scroll_frame.bind("<Configure>", update_scrollregion)

        # Allow expansion
        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        # ❌ Removed self.load_table() — SQL cannot run here

    # ---------------------------------------------------------
    # LOAD TABLE (SQL OK — called only after activation)
    # ---------------------------------------------------------
    def load_table(self):
        for widget in self.scroll_frame.winfo_children():
            widget.destroy()

        cnxn = get_db_connection()
        with cnxn as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM AIAI_Employee_Info")
            data = cursor.fetchall()
            columns = [desc[0] for desc in cursor.description]

        visible_columns = [
            "First_Name", "Middle_Name", "Last_Name", "ID", "Email",
            "Address", "Apt_Number", "City", "State", "Zip_Code",
            "Phone_Number", "Title", "is_installer"
        ]

        # Header
        for j, col_name in enumerate(visible_columns):
            if col_name in columns:
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
            text="Actions (Edit, Delete, Username, Password)",
            font=("Arial", 10, "bold")
        ).grid(row=0, column=len(visible_columns), columnspan=4)

        # Rows
        for i, row in enumerate(data, start=1):
            for j, col_name in enumerate(visible_columns):
                if col_name in columns:
                    col_index = columns.index(col_name)
                    value = row[col_index]

                    if col_name == "is_installer":
                        display_value = "Yes" if value else "No"
                    else:
                        display_value = "" if value is None else str(value)

                    tk.Label(
                        self.scroll_frame,
                        text=display_value,
                        borderwidth=1,
                        relief="solid",
                        padx=3,
                        pady=3
                    ).grid(row=i, column=j, sticky="nsew")

            # Action buttons
            tk.Button(
                self.scroll_frame,
                text="Edit",
                bg="green",
                width=8,
                command=lambda r=row: self.edit_installer_info(r, columns)
            ).grid(row=i, column=len(visible_columns))

            tk.Button(
                self.scroll_frame,
                text="Delete",
                bg="red",
                width=8,
                command=lambda r=row: self.delete_installer_info(r, columns)
            ).grid(row=i, column=len(visible_columns) + 1)

            tk.Button(
                self.scroll_frame,
                text="Username",
                bg="brown",
                width=10,
                command=lambda r=row: self.open_username_reset_window(r, columns)
            ).grid(row=i, column=len(visible_columns) + 2)

            tk.Button(
                self.scroll_frame,
                text="Password",
                bg="yellow",
                width=10,
                command=lambda r=row: self.open_password_reset_window(r, columns)
            ).grid(row=i, column=len(visible_columns) + 3)

        # Navigation buttons
        final_row = len(data) + 2
        nav = tk.Frame(self.scroll_frame)
        nav.grid(row=final_row, column=0, columnspan=len(visible_columns) + 4, pady=10)

        tk.Button(nav, text="Exit", command=exit_session, bg="red").pack(side=tk.LEFT, padx=10)
        tk.Button(
            nav,
            text="Admin Interface",
            bg="green",
            command=lambda: self.controller.show_frame(AdminInterfaceFrame)
        ).pack(side=tk.LEFT, padx=10)
        tk.Button(
            nav,
            text="Database Portal",
            bg="blue",
            command=lambda: self.controller.show_frame(DatabasePortalFrame)
        ).pack(side=tk.LEFT, padx=10)

    # ---------------------------------------------------------
    # DELETE INSTALLER
    # ---------------------------------------------------------
    def delete_installer_info(self, row, columns):
        confirm = messagebox.askyesno("Confirm Deletion", "Are you sure?")
        if not confirm:
            return

        user_key_index = columns.index("user_key")
        raw_user_key = row[user_key_index]

        cnxn = get_db_connection()
        with cnxn as conn:
            cursor = conn.cursor()
            cursor.execute(
                "DELETE FROM AIAI_Employee_Info WHERE user_key = ?",
                (raw_user_key,)
            )
            conn.commit()

        messagebox.showinfo("Success", "User deleted.")
        self.load_table()

    # ---------------------------------------------------------
    # EDIT INSTALLER INFO
    # ---------------------------------------------------------
    def edit_installer_info(self, row, columns):
        win = tk.Toplevel(self)
        win.title("Edit Installer Info")
        win.attributes("-fullscreen", True)

        visible_columns = [
            "First_Name", "Middle_Name", "Last_Name", "ID", "Email",
            "Address", "Apt_Number", "City", "State", "Zip_Code",
            "Phone_Number", "Title"
        ]

        container = tk.Frame(win)
        container.pack(fill="both", expand=True)

        canvas = tk.Canvas(container)
        scroll_frame = tk.Frame(canvas)

        vsb = tk.Scrollbar(container, orient="vertical", command=canvas.yview)
        hsb = tk.Scrollbar(container, orient="horizontal", command=canvas.xview)

        canvas.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)

        vsb.pack(side="right", fill="y")
        hsb.pack(side="bottom", fill="x")
        canvas.pack(side="left", fill="both", expand=True)

        canvas.create_window((0, 0), window=scroll_frame, anchor="nw")

        scroll_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        entries = []

        for i, col in enumerate(visible_columns):
            if col not in columns:
                continue

            col_index = columns.index(col)
            raw_value = row[col_index]

            if isinstance(raw_value, bytes):
                raw_value = raw_value.decode()

            display_value = "" if raw_value is None else str(raw_value)

            tk.Label(scroll_frame, text=col).grid(row=0, column=i, padx=5, pady=5)
            entry = tk.Entry(scroll_frame)
            entry.insert(0, display_value)
            entry.grid(row=1, column=i, padx=5, pady=5)
            entries.append(entry)

        # is_installer field
        tk.Label(scroll_frame, text="is_installer").grid(row=0, column=len(entries), padx=5, pady=5)
        installer_entry = tk.Entry(scroll_frame)

        if "is_installer" in columns:
            inst_idx = columns.index("is_installer")
            inst_val = row[inst_idx]
            installer_entry.insert(0, "Yes" if inst_val else "No")

        installer_entry.grid(row=1, column=len(entries), padx=5, pady=5)

        def save_changes():
            entry_map = dict(zip(visible_columns, entries))

            update_dict = {
                col: entry_map[col].get()
                for col in visible_columns
            }

            installer_val = installer_entry.get().strip().lower()
            if installer_val in ("yes", "no", "1", "0", "true", "false"):
                is_installer_value = 1 if installer_val in ("yes", "1", "true") else 0
                update_dict["is_installer"] = is_installer_value

            set_clause = ", ".join([f"{col} = ?" for col in update_dict])
            params = list(update_dict.values())

            raw_user_key = row[columns.index("user_key")]
            if isinstance(raw_user_key, bytes):
                raw_user_key = raw_user_key.decode()

            params.append(raw_user_key)

            cnxn = get_db_connection()
            with cnxn as conn:
                cursor = conn.cursor()
                cursor.execute(
                    f"UPDATE AIAI_Employee_Info SET {set_clause} WHERE user_key = ?",
                    params
                )
                conn.commit()

            win.destroy()
            self.load_table()

        button_frame = tk.Frame(scroll_frame)
        button_frame.grid(row=2, column=0, columnspan=len(entries) + 1, pady=20)

        tk.Button(button_frame, text="Save", command=save_changes, bg="green").pack(side=tk.LEFT, padx=10)
        tk.Button(button_frame, text="Exit", command=win.destroy, bg="red").pack(side=tk.LEFT, padx=10)

    # ---------------------------------------------------------
    # RESET USERNAME
    # ---------------------------------------------------------
    def open_username_reset_window(self, row, columns):
        win = tk.Toplevel(self)
        win.title("Reset Username")
        win.attributes("-fullscreen", True)

        tk.Label(
            win,
            text="Automating Innovating AI Production Manager App - Change Username Dashboard",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=6, pady=(20, 10))

        try:
            first_name = row[columns.index("First_Name")]
            last_name = row[columns.index("Last_Name")]
        except Exception:
            first_name = last_name = "[Error]"

        first_name = "" if first_name is None else str(first_name)
        last_name = "" if last_name is None else str(last_name)

        tk.Label(
            win,
            text=f"Reset username for {first_name} {last_name}",
            font=("Arial", 12, "italic")
        ).grid(row=1, column=0, columnspan=6, pady=(5, 15))

        tk.Label(win, text="Enter New Username").grid(row=2, column=0, sticky="e")
        username_entry = tk.Entry(win)
        username_entry.grid(row=2, column=1, sticky="w")

        def save_new_username():
            new_username = username_entry.get()

            user_key_index = columns.index("user_key")
            raw_user_key = row[user_key_index]

            try:
                cnxn = get_db_connection()
                with cnxn as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE AIAI_Employee_Info SET Employee_Username = ? WHERE user_key = ?",
                        (new_username, raw_user_key)
                    )
                    conn.commit()

                win.destroy()
                self.load_table()

            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

        tk.Button(win, text="Save", command=save_new_username, bg="green").grid(row=2, column=3)
        tk.Button(win, text="Exit", command=win.destroy, bg="red").grid(row=2, column=4)

    # ---------------------------------------------------------
    # RESET PASSWORD
    # ---------------------------------------------------------
    def open_password_reset_window(self, row, columns):
        win = tk.Toplevel(self)
        win.title("Reset Password")
        win.attributes("-fullscreen", True)

        tk.Label(
            win,
            text="Automating Innovating AI Production Manager App - Change Password Dashboard",
            font=("Helvetica", 16, "bold")
        ).grid(row=0, column=0, columnspan=6, pady=(20, 10))

        try:
            first_name = row[columns.index("First_Name")]
            last_name = row[columns.index("Last_Name")]
        except Exception:
            first_name = last_name = "[Error]"

        first_name = "" if first_name is None else str(first_name)
        last_name = "" if last_name is None else str(last_name)

        tk.Label(
            win,
            text=f"Reset password for {first_name} {last_name}",
            font=("Arial", 12, "italic")
        ).grid(row=1, column=0, columnspan=6, pady=(5, 15))

        tk.Label(win, text="Enter New Password").grid(row=2, column=0, sticky="e")
        password_entry = tk.Entry(win, show="*")
        password_entry.grid(row=2, column=1, sticky="w")

        def save_new_password():
            new_password = password_entry.get()
            hashed_pw = hash_password(new_password)

            user_key_index = columns.index("user_key")
            raw_user_key = row[user_key_index]

            try:
                cnxn = get_db_connection()
                with cnxn as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "UPDATE AIAI_Employee_Info SET Employee_Password = ? WHERE user_key = ?",
                        (hashed_pw, raw_user_key)
                    )
                    conn.commit()

                win.destroy()
                self.load_table()

            except Exception as e:
                messagebox.showerror("Database Error", f"An error occurred: {e}")

        tk.Button(win, text="Save", command=save_new_password, bg="green").grid(row=2, column=2)
        tk.Button(win, text="Exit", command=win.destroy, bg="red").grid(row=2, column=3)


def main():
    pass