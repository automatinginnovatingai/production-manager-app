Production Manager App — User Guide
Version: 1.0.1
Build Date: 2025-09-08

Welcome to the Automating Innovating AI Production Manager App — a secure, offline-first tool designed to simplify payroll, job tracking, and production reporting for insulation companies and small-to-mid-sized contractors.

This guide provides everything you need to install, activate, and begin using the app successfully.

------------------------------------------------------------
DATABASE SELECTION (IMPORTANT)
------------------------------------------------------------
On first launch, you must choose between SQL Express and SQL Server. This determines where your data will be stored.

SQL EXPRESS (Recommended for most users)
• Best for small businesses, single-computer setups, and teams under ~10 employees.
• Free, installs automatically, and requires no IT knowledge.
• Stores data locally on the same computer running the app.
• Ideal if you want a simple, reliable setup with minimal configuration.

SQL SERVER (For larger companies or IT-managed environments)
• Best for companies that already use SQL Server or have an IT department.
• Supports multiple computers connecting to the same shared database.
• Allows centralized data storage on a server.
• Ideal for larger teams, multi-user environments, or companies needing advanced database control.

If you are unsure which option to choose, select SQL Express. You can migrate to SQL Server later if your company grows.

------------------------------------------------------------
KEY FEATURES
------------------------------------------------------------

Secure Login
• Bcrypt-protected passwords with salted + hashed credentials.
• Session-based access control.

Payroll Management
• Calculate weekly payroll using:
  - Square footage × rate
  - Bags installed × piece rate
  - Hourly wage
• Supports up to four employees per job.
• Automatic pay splitting.
• Material usage tracking (manufacturer, type, size).
• Enter “0” in unused fields to avoid calculation errors.

Employee Job Entry
Each job entry includes:
• Employee names and IDs
• Hours worked
• Job role
• Builder, model, lot/block
• Optional product details (e.g., R-30x16, Fi-Foil, baffles)

Pay Week Entry & Auto-Export
• Set payroll start and end days (e.g., Thursday → Wednesday).
• App automatically exports payroll 2 days after the end day.
• Exports saved under:
  Documents/AIAI_PM_App/Payroll_Excels/YYYY-MM/Payroll_YYYY-MM.xlsx
• Each employee receives a dedicated worksheet.
• Totals auto-calculated.
• Option to open the workbook immediately after export.

Data Protection
• Automatic duplicate detection.
• Local SQL database (Express or Server).
• No cloud storage.

Reporting
• Clean Excel-compatible exports.
• Organized by month and week.
• Customizable file names.

Auto-Updating
• App checks for new versions automatically.

User-Friendly Interface
• Fullscreen workflow.
• Large buttons and clear navigation.
• No technical knowledge required.

------------------------------------------------------------
SYSTEM REQUIREMENTS
------------------------------------------------------------
• Windows 10 or later.
• Microsoft Excel (required for viewing reports).
• Approximately 980 MB free disk space.
• SQL Express or SQL Server (selected during setup).
• Internet connection required only for license activation.

------------------------------------------------------------
LICENSE ACTIVATION
------------------------------------------------------------
A valid Gumroad license key is required.

• You will be prompted on first launch.
• The app verifies your key securely.
• If invalid or revoked, access is restricted.
• Internet is required only once for activation.

------------------------------------------------------------
GETTING STARTED
------------------------------------------------------------
1. Launch the Production Manager App.
2. Choose SQL Express or SQL Server.
3. Enter your Gumroad license key.
4. Register your Admin account.
5. Log in using your new credentials.
6. Navigate to the Admin Interface.
7. Open “Employee Worksheet” to begin entering jobs and payroll.

------------------------------------------------------------
NAVIGATION & EXITING
------------------------------------------------------------
• Use the dashboard to access all modules.
• Press Esc to exit fullscreen mode.
• Click “Exit” on any screen to close the app.

------------------------------------------------------------
TIPS FOR BEST RESULTS
------------------------------------------------------------
• Export payroll regularly to maintain backups.
• Keep Excel updated.
• Use strong admin passwords.
• Ensure payroll data is complete before the auto-export date.

------------------------------------------------------------
TROUBLESHOOTING
------------------------------------------------------------

App won’t launch:
• Ensure Windows 10+ is installed.
• Confirm Excel is installed.

License key rejected:
• Verify your Gumroad purchase email.
• Check for typos.

Export failed:
• Ensure Excel is installed.
• Confirm all payroll fields are filled.

Auto-update not working:
• Check your internet connection.
• Ensure firewall isn’t blocking the app.

------------------------------------------------------------
SUPPORT
------------------------------------------------------------
Questions or feedback?
Email: automatinginnovatingai@outlook.com

Thank you for using the Production Manager App!