# entry_point.py
import tkinter as tk
from PIL import Image, ImageTk
import os
import sys


def resource_path(relative_path):
    """Return absolute path to resource inside EXE or during development."""
    try:
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


class HomeFrame(tk.Frame):
    """Initial splash screen."""
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        controller.title("Automating Innovating AI - Production Manager App")

        canvas = tk.Canvas(
            self,
            width=controller.winfo_screenwidth(),
            height=controller.winfo_screenheight(),
            highlightthickness=0,
            bd=0
        )
        canvas.pack(fill="both", expand=True)

        image_path = resource_path("tools/automating_innovating_ai_photo.jpg")
        image = Image.open(image_path)
        self.background_image = ImageTk.PhotoImage(image)
        canvas.create_image(0, 0, image=self.background_image, anchor="nw")


def main():
    # Create the ONLY root window for splash
    root = tk.Tk()

    # Show splash
    splash = HomeFrame(root)
    splash.pack(fill="both", expand=True)
    root.update()

    # Remove splash
    splash.destroy()

    # Launch main application
    import main
    root.destroy()  # destroy splash root
    main.main()     # main.py creates its own App() root


if __name__ == "__main__":
    main()