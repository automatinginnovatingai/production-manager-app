import os
import shutil
import tkinter as tk
from PIL import Image, ImageTk
import sys
import calendar
from datetime import datetime, date
from user_guide import UserGuideFrame
from user_login import UserLoginFrame
from user_registration import UserRegistrationFrame


# ---------- shared helpers ----------

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# ---------- splash page (was show_image) ----------

class PMMSplashFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.controller.title("Automating Innovating Innovating AI - Production Manager App - © 2024 Automating Innovating AI")

        self.canvas = tk.Canvas(self, width=controller.winfo_screenwidth(),
                                height=controller.winfo_screenheight(),
                                highlightthickness=0, bd=0)
        self.canvas.pack(fill="both", expand=True)

        image_path = resource_path("tools/automating_innovating_ai_photo.jpg")
        image = Image.open(image_path)

        # KEEP A STRONG REFERENCE
        self.splash_image = ImageTk.PhotoImage(image)

        # DRAW AFTER THE FRAME IS VISIBLE
        self.after(10, lambda: self.canvas.create_image(0, 0, image=self.splash_image, anchor="nw"))

# ---------- home portal (was open_home_window) ----------

class PMMHomeFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        self.controller.title("Automating Innovating AI - Production Manager Insulation Payroll App")

        canvas = tk.Canvas(self, width=controller.winfo_screenwidth(),
                           height=controller.winfo_screenheight(), highlightthickness=0, bd=0)
        canvas.pack(fill="both", expand=True)

        frame = tk.Frame(self)
        frame.place(relx=0.5, rely=0.5, anchor="center")

        home_portal_label = tk.Label(frame, text="Home")
        title_label = tk.Label(frame,
                               text="Automating Innovating AI Production Manager App Home Portal",
                               font="bold")
        home_portal_label.grid(row=0, column=0)
        title_label.grid(row=1, column=0)

        signin_button = tk.Button(frame, text="Admin Login",
                                  command=self.signin_user,
                                  font="bold", bg="green")
        signin_button.grid(row=3, column=0, sticky="news", padx=20, pady=10)

        register_button = tk.Button(frame, text="Admin Registration Form",
                                    command=self.register_new_user,
                                    font="bold", bg="blue")
        register_button.grid(row=4, column=0, sticky="news", padx=20, pady=10)

        user_guide_button = tk.Button(frame, text="User Guide",
                                      command=self.user_guide,
                                      font="bold", bg="yellow")
        user_guide_button.grid(row=5, column=0, sticky="news", padx=20, pady=10)

        exit_button = tk.Button(frame, text="Exit",
                                command=self.exit_app,
                                font="bold", bg="red")
        exit_button.grid(row=6, column=0, sticky="news", padx=20, pady=10)

        calendar_frame = tk.LabelFrame(frame, text="Calendar", font="bold")
        calendar_frame.grid(row=0, column=11, padx=20, pady=10)

        now = datetime.now()
        t = now.strftime("%H:%M:%S")
        s1 = now.strftime("%m/%d/%Y")
        my_date = date.today()
        day_name = calendar.day_name[my_date.weekday()]

        tk.Label(calendar_frame, text="Time").grid(row=1, column=11)
        tk.Label(calendar_frame, text=t).grid(row=2, column=11)

        tk.Label(calendar_frame, text="MM/DD/YYYY").grid(row=3, column=11)
        tk.Label(calendar_frame, text=s1).grid(row=4, column=11)

        tk.Label(calendar_frame, text="Day of the Week").grid(row=5, column=11)
        tk.Label(calendar_frame, text=day_name).grid(row=6, column=11)

    # ----- button actions -----
    def signin_user(self):
        self.controller.show_frame(UserLoginFrame)

    def register_new_user(self):
        self.controller.show_frame(UserRegistrationFrame)

    def user_guide(self):
        self.controller.show_frame(UserGuideFrame) 

    def exit_app(self):
        self.controller.destroy()
        