# app_controller.py
import tkinter as tk
import session_context

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automating Innovating AI - Production Manager App")
        self.attributes("-fullscreen", True)

        # key: page_class, value: frame instance
        self.frames = {}

    def exit_session(self):
        session_context.exit_session()
        self.destroy()    

    def add_frame(self, page_class):
        frame = page_class(self)
        self.frames[page_class] = frame
        frame.place(relwidth=1, relheight=1)

    def show_frame(self, page_class):
        frame = self.frames[page_class]

        # Optional hook; safe to ignore if frame doesn't define it
        if hasattr(frame, "on_show"):
            if frame.on_show() is False:
                return

        frame.tkraise()
