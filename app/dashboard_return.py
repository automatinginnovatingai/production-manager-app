import tkinter as tk
from session_context import clear_user



class DashboardReturnFrame(tk.Frame):
    def __init__(self, controller):
        super().__init__(controller)
        self.controller = controller

        # Main dashboard screen
        label = tk.Label(
            self,
            text="Production Manager App",
            font=("Arial", 24)
        )
        label.pack(expand=True)

        # When the user closes the window, redirect to exit_session screen
        self.bind("<<ShowFrame>>", lambda e: self.after(1000, self.return_to_dashboard))

    # ---------------------------------------------------------
    # EXIT APP
    # ---------------------------------------------------------
    def redirect_user(self):
        clear_user()
        from startup_page import StartPageFrame
        self.controller.show_frame(StartPageFrame)

    # ---------------------------------------------------------
    # PASSWORD RESET SUCCESS → SHOW MESSAGE → EXIT
    # ---------------------------------------------------------
    def reset_password_window(self, callback):
        reset_win = tk.Toplevel(self)
        reset_win.title("Reset Password")

        # Build your reset GUI here...

        def on_success():
            reset_win.destroy()
            callback()

        # Call on_success() when password reset is complete

    # ---------------------------------------------------------
    # SHOW "PASSWORD CHANGED" SCREEN
    # ---------------------------------------------------------
    def return_to_dashboard(self):
        msg = tk.Toplevel(self)
        msg.attributes("-fullscreen", True)
        msg.configure(bg="black")

        label = tk.Label(
            msg,
            text="Password changed.",
            font=("Helvetica", 48, "bold"),
            fg="white",
            bg="black"
        )
        label.pack(expand=True)

        msg.after(2000, lambda: self.go_to_dashboard(msg))

    # ---------------------------------------------------------
    # SHOW "EXITING APP" SCREEN → EXIT
    # ---------------------------------------------------------
    def go_to_dashboard(self, msg_window):
        msg_window.destroy()

        exit_screen = tk.Toplevel(self)
        exit_screen.attributes("-fullscreen", True)
        exit_screen.configure(bg="black")

        label = tk.Label(
            exit_screen,
            text="Exiting app. Restart app after it closes.",
            font=("Helvetica", 48, "bold"),
            fg="white",
            bg="black"
        )
        label.pack(expand=True)

        exit_screen.after(2000, self.redirect_user)


def main():
    # Only here so the file doesn't break if run directly.
    pass