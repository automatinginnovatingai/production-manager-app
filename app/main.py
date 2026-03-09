# main.py (inside the app folder)
import tkinter.messagebox as mb
from app_controller import App

from startup_page import StartPageFrame
from Production_Manager_App import PMMSplashFrame, PMMHomeFrame
from Admin_Interface import AdminInterfaceFrame
from Automating_Innovating_AI_Production_Manager_App import EmployeeDailyWorkFrame
from builders_db import BuildersDBFrame
from database import DatabasePortalFrame
from builders_info import BuildersInfoFrame
from csv_upload import CSVUploadFrame
from dashboard_return import DashboardReturnFrame
from installer_db import InstallerDBFrame
from installer_info import InstallerInfoFrame
from material_info_db import MaterialInfoDBFrame
from material_info import MaterialInfoFrame
from password_reset import PasswordResetFrame
from pay_week_schedule import PayWeekScheduleFrame
from terms_conditions import TermsConditionsFrame
from user_guide import UserGuideFrame
from user_login import UserLoginFrame
from user_registration import UserRegistrationFrame
from weekly_production_sheet import WeeklyProductionSheetFrame
from Installer_Interface import InstallerInterfaceFrame
from installer_login import InstallerLoginFrame
from employee_interface import InstallerDailyWorkFrame
from CSV_View import CSV_ViewFrame
from sql_connection_page import SQLConnectionFrame
from license_validator import LicensePageFrame
from admin_license_activation import AdminLicenseActivationFrame


def run_license_logic_sql(app):
    # NO load_local_activation HERE.
    # First step after splash is ALWAYS the license page.
    app.show_frame(LicensePageFrame)


def main():
    app = App()

    for page in (
        LicensePageFrame,
        AdminLicenseActivationFrame,
        StartPageFrame,
        PMMSplashFrame,
        PMMHomeFrame,
        TermsConditionsFrame,
        AdminInterfaceFrame,
        EmployeeDailyWorkFrame,
        BuildersDBFrame,
        PasswordResetFrame,
        DatabasePortalFrame,
        BuildersInfoFrame,
        CSVUploadFrame,
        DashboardReturnFrame,
        InstallerDBFrame,
        InstallerInfoFrame,
        MaterialInfoDBFrame,
        MaterialInfoFrame,
        UserGuideFrame,
        UserLoginFrame,
        UserRegistrationFrame,
        WeeklyProductionSheetFrame,
        PayWeekScheduleFrame,
        InstallerInterfaceFrame,
        InstallerDailyWorkFrame,
        InstallerLoginFrame,
        CSV_ViewFrame,
        SQLConnectionFrame,
    ):
        app.add_frame(page)

    # Show splash FIRST
    app.show_frame(PMMSplashFrame)

    # After splash finishes (5 seconds), go straight to License Page
    app.after(5000, lambda: run_license_logic_sql(app))

    app.mainloop()


if __name__ == "__main__":
    main()