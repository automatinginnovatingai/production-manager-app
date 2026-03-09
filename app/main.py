# main.py
from app_controller import App
from Production_Manager_App import PMMSplashFrame
from license_validator import LicensePageFrame

def run_license_logic_sql(app):
    app.show_frame(LicensePageFrame)

def main():
    app = App()

    # Show splash FIRST
    app.show_frame(PMMSplashFrame)

    # After splash finishes (5 seconds), go straight to License Page
    app.after(5000, lambda: run_license_logic_sql(app))

    app.mainloop()

if __name__ == "__main__":
    main()