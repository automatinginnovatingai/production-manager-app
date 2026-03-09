Production Manager App - User Guide
====================================
Version: 1.0.0
Build Date: 2025-09-08

Welcome to the Automating Innovating AI Production Manager App — a streamlined, secure, and intuitive tool 
for managing production workflows, employee payroll, and data exports.

Key Features
------------
• Secure Login:
  - Encrypted password protection with industry-standard hashing.

• Payroll Management:
  - Input and calculate weekly payroll with precision.
  - Calculate material usage using:
      • Columns to use for calculation: (e.g. Sqft/Bags Installed × Pay Per Tube/Piece Rate)
      • Bag method: (e.g. 5 bags × $4.50 = $22.50)
      • Square footage: (e.g. 2000 ft² × $0.045 = $90.00)
      • Hourly wage: (e.g. 10 hours x $17.45 = $174.50)
      • Enter 0 in Sqft/Bags Installed and/or Pay Per Tube/Piece Rate columns that has no data to input
  - Add up to four employees for each job.
  - Automatic pay splitting among listed employees.

• Employee Job Entry:
  Each job entry will require:
      - First and last name of each employee
      - Employee ID (if applicable)
      - Work hours and job roles
      - Builder, job site, model, and lot/block details
      - Optional: Product info such as manufacturer and insulation type/size
        • Manufacturer (e.g. Owens Corning, Knauf)
        • Type and size (e.g. R-30x16, R-30x24, Fi-Foilx24, baffles)

• Pay Week Entry & Auto Export
  This application also streamlines the process of marking pay cycles and exporting enhanced Excel reports.
  • Set the start and end day of the payroll period using a friendly fullscreen interface.
  - Example: Start Day = Thursday, End Day = Wednesday
  - Payroll is exported automatically 2 days after the end day
  - Press Esc to exit fullscreen mode at any time
  • Authorization Required
  - Only verified sessions (secure login with salted + hashed credentials) can access this module
  • What Gets Exported
  - Weekly employee payroll grouped by name or ID
  - Exported to Excel files saved monthly under:
  Documents/AIAI_PM_App/Payroll_Excels/YYYY-MM/Payroll_YYYY-MM.xlsx
  - Each employee gets a dedicated sheet labeled by week number (e.g. John_Doe_Week_2)
  - Totals are auto-calculated and displayed per sheet
  • After export:
  - You’ll be asked if you’d like to open the workbook immediately
  - Excel must be installed to view reports
  Tip: Ensure pay data is complete before the scheduled export date (End Day + 2). The export runs automatically when the day arrives.

• Data Protection:
  - Automatic de-duplication to prevent redundant entries.

• Reporting:
  - Clean Excel-compatible CSV exports grouped by month/day.
  - Ability to customize export file names.

• Auto-Updating:
  - Automatically checks for new app versions.

• Friendly Interface:
  - Designed for ease of use—no technical knowledge required!

System Requirements
-------------------
• Operating System: Windows 10 or later is required.
• Microsoft Excel must be installed to view reports.
• At least 130 MB of available local disk space is recommended:
    - Data is stored useing client's SQL Server Database.
    - Monthly Excel files are created with worksheets by day.

License Activation  
------------------  
This app requires a valid Gumroad license key to unlock full functionality.  
• You will be prompted to enter your license key on first launch.  
• The app verifies your key securely via Gumroad’s API.  
• If the license is invalid or revoked, access will be restricted.  
Note: Internet access is required for initial license validation.

Getting Started
---------------
1. Launch the app via the Production Manager icon.
2. Click 'Admin Registration' to create an account.
3. After registering, click 'Admin Login' to sign in.
4. Navigate to the Admin Interface.
5. Click 'Employee Worksheet' to begin logging job and payroll data.

Navigation & Exiting
---------------------
• Use the dashboard to access key modules.
• Click the 'Exit' button on any screen to close the app.

Tips
----
• Export data regularly to back up your records.
• Use strong admin credentials.
• Keep Excel updated for full report compatibility.

Troubleshooting  
---------------  
• App won’t launch: Ensure Windows 10+ is installed and Excel is available.  
• License key rejected: Double-check your Gumroad purchase email.  
• Export failed: Confirm pay data is complete and Excel is installed.  
• Auto-update not working: Check your internet connection and firewall settings.

Support
-------
Questions or feedback? Visit the support page or contact the developer.
• @ automatinginnovatingai@outlook.com
Thank you for using Production Manager App!