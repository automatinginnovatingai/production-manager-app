Automating Innovating AI – Production Manager App
README.txt
Version: 2.0.0
============================================================

Overview
--------
The Production Manager App is part of the Automating Innovating AI CRM Suite — a unified,
multi‑tenant platform designed for construction‑industry trades. All CRM apps now share
a common architecture:

• Global Admin + Local Admin RBAC
• company_id data isolation
• Shared core tables (Companies, Divisions, Regions, Users, Roles, Permissions)
• Centralized RBAC enforcement
• Modular feature access per app
• Inventory App + Payroll App integration
• Offline‑first operation with secure local SQL storage

This app manages production workflows, employee job tickets, payroll preparation,
inventory usage, and reporting for your company.

============================================================
DATABASE SELECTION (IMPORTANT)
============================================================
On first launch, you must choose between SQL Express and SQL Server. This determines
where your data will be stored.

SQL EXPRESS (Recommended for most users)
• Best for small businesses, single‑computer setups, and teams under ~10 employees.
• Free, installs automatically, and requires no IT knowledge.
• Stores data locally on the same computer running the app.
• Ideal for simple, reliable setups with minimal configuration.

SQL SERVER (For larger companies or IT‑managed environments)
• Best for companies that already use SQL Server or have an IT department.
• Supports multiple computers connecting to the same shared database.
• Allows centralized data storage on a server.
• Ideal for larger teams, multi‑user environments, or companies needing advanced control.

If unsure, choose SQL Express. You can migrate to SQL Server later.

============================================================
ADMIN ROLES
============================================================

GLOBAL ADMIN (Corporate Level)
• Creates companies, divisions, and regions
• Manages subscription plans and license upgrades
• Manages all admins (global + local)
• Controls payroll schedules and exports
• Oversees inventory, suppliers, and purchase orders
• Integrates Payroll App and Inventory App with CRM modules
• Full access to all reports and data

LOCAL ADMIN (Division/Region Level)
• Enters employee job tickets and production data
• Reviews work tickets before payroll is processed
• Manages inventory and POs if permissions allow
• Cannot modify subscription plans or corporate settings
• Access limited by assigned role + permissions

============================================================
KEY FEATURES
============================================================

Secure Login & RBAC
• Bcrypt‑protected passwords with salted + hashed credentials.
• Role‑based access control enforced by centralized RBAC.
• company_id isolation across all tables.

Payroll Management
• Calculate weekly payroll using:
  - Square footage × rate
  - Bags installed × piece rate
  - Hourly wage
• Supports up to four employees per job.
• Automatic pay splitting.
• Material usage tracking (manufacturer, type, size).
• Enter “0” in unused fields to avoid calculation errors.

Employee Job Entry (Local Admin)
Each job entry includes:
• Employee names and IDs
• Hours worked
• Job role
• Builder, model, lot/block
• Optional product details (e.g., R‑30x16, Fi‑Foil, baffles)
• All saved using company_id for multi‑tenant isolation

Work Ticket Printing
• Local Admins can print work tickets directly from their machine.
• Printing does not require company_id (local action).
• Saved tickets always include company_id.

Pay Week Entry & Auto‑Export (Global Admin)
• Set payroll start and end days (e.g., Thursday → Wednesday).
• App automatically exports payroll 2 days after the end day.
• Exports saved under:
  Documents/AIAI_PM_App/Payroll_Excels/YYYY‑MM/Payroll_YYYY‑MM.xlsx
• Each employee receives a dedicated worksheet.
• Totals auto‑calculated.
• Option to open the workbook immediately after export.

Inventory Integration
• Universal material database (generic fields)
• CRM apps store trade‑specific material extensions
• Supplier management
• Purchase order creation and receiving
• Inventory adjustments and transaction logs
• All inventory operations scoped by company_id

Reporting
• Weekly production sheets
• Payroll exports
• Material usage reports
• All reports require reports_view permission

Data Protection
• Automatic duplicate detection
• Local SQL database (Express or Server)
• No cloud storage
• All SQL queries scoped by company_id

Auto‑Updating
• App checks for new versions automatically.

User‑Friendly Interface
• Fullscreen workflow
• Large buttons and clear navigation
• No technical knowledge required

============================================================
SYSTEM REQUIREMENTS
============================================================
• Windows 10 or later
• Microsoft Excel (required for viewing reports)
• Approximately 980 MB free disk space
• SQL Express or SQL Server (selected during setup)
• Internet connection required only for license activation

============================================================
LICENSE ACTIVATION
============================================================
A valid Gumroad license key is required.

• You will be prompted on first launch.
• The app verifies your key securely.
• If invalid or revoked, access is restricted.
• Internet is required only once for activation.

============================================================
GETTING STARTED
============================================================
1. Launch the Production Manager App.
2. Choose SQL Express or SQL Server.
3. Enter your Gumroad license key.
4. Register your Global Admin account.
5. Create Local Admins as needed.
6. Log in using your credentials.
7. Navigate to the Admin Interface.
8. Open “Employee Worksheet” to begin entering jobs and payroll.

============================================================
NAVIGATION & EXITING
============================================================
• Use the dashboard to access all modules.
• Press Esc to exit fullscreen mode.
• Click “Exit” on any screen to close the app.

============================================================
TIPS FOR BEST RESULTS
============================================================
• Export payroll regularly to maintain backups.
• Keep Excel updated.
• Use strong admin passwords.
• Ensure payroll data is complete before the auto‑export date.
• Review admin permissions periodically.

============================================================
TROUBLESHOOTING
============================================================

App won’t launch:
• Ensure Windows 10+ is installed.
• Confirm Excel is installed.

License key rejected:
• Verify your Gumroad purchase email.
• Check for typos.

Export failed:
• Ensure Excel is installed.
• Confirm all payroll fields are filled.

Auto‑update not working:
• Check your internet connection.
• Ensure firewall isn’t blocking the app.

============================================================
SUPPORT
============================================================
Questions or feedback?
Email: automatinginnovatingai@outlook.com

Thank you for using the Automating Innovating AI CRM Suite!
