# app_controller.py
import tkinter as tk
import session_context

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Automating Innovating AI - Production Manager App")
        self.attributes("-fullscreen", True)

        # Only store frames AFTER they are created
        self.frames = {}

    def exit_session(self):
        session_context.exit_session()
        self.destroy()

    def show_frame(self, page_class):
        # Create frame only when needed
        if page_class not in self.frames:
            frame = page_class(self)
            self.frames[page_class] = frame
            frame.place(relwidth=1, relheight=1)
        else:
            frame = self.frames[page_class]

        # Run on_show AFTER frame is visible
        frame.tkraise()

        if hasattr(frame, "on_show"):
            frame.on_show()