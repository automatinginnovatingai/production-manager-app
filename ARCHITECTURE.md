Production Manager App – Architecture Overview
==============================================

Overview
--------
The Production Manager App is a closed‑source Windows .exe application designed for offline use, with secure license enforcement, automated Excel reporting, and a streamlined workflow tailored for small‑to‑medium‑sized service businesses. It eliminates the complexity of cloud‑based CRMs by providing a fast, local, reliable Operational CRM that works entirely on the user’s machine or internal network.

The application supports both SQL Express and SQL Server, selected during installation, and operates entirely offline with no cloud dependencies.

Architecture
------------

Database Selection (Installer‑Driven)
-------------------------------------
During installation, the user selects one of two supported database modes:

1. SQL Express (Local Database – Recommended for 1–5 users)
   - Installer automatically installs and configures SQL Server Express.
   - Ideal for single‑machine setups or small office networks.

2. SQL Server (Remote or On‑Prem Server)
   - User connects to an existing SQL Server instance.
   - Supports multi‑user environments and IT‑managed deployments.

The installer writes a registry flag (UseSQLExpress) that determines which connection page the app loads on first run.

License Enforcement Flow
------------------------
User Launches App → License Prompt → Gumroad API Validation → Local Unlock

- User enters their Gumroad license key on first launch.
- The key is validated through Gumroad’s /v2/licenses/verify endpoint.
- If valid, the app unlocks and stores the license state locally.
- Periodic revalidation may occur (e.g., every 7 days).
- License variants determine access to Basic, Pro, or Enterprise features.

Local Session Context
---------------------
- All data is stored in SQL Express or SQL Server depending on installer selection.
- No cloud sync, Redis, or external session store is used.
- Secure login enforced using salted + hashed admin credentials.
- Fully offline operation with no external dependencies.

Data Transfer Between Computers
-------------------------------
The app includes a built‑in transfer system for migrating data to a new machine:

- Creates a .bak backup file from the old computer.
- Restores the .bak file on the new computer.
- Works for both SQL Express and SQL Server.
- Ideal for machine upgrades or office migrations.

SQL Connection Pages
--------------------
The app routes users to the correct connection setup page based on installer selection:

- sql_connection_page.py – SQL Express users
- sql_server_connection_page.py – SQL Server users

Both pages support:
- Connection testing
- Credential validation
- Database creation (if needed)
- Secure admin login setup

Payroll & Job Entry Workflow
----------------------------
Admin Login → Job Entry → Payroll Calculation → Excel Export

- Admin enters job details, employee info, and material usage.
- Payroll supports multiple calculation methods:
  • Square footage × rate
  • Bags installed × piece rate
  • Hourly wage
- Pay is automatically split across employees per job.
- Excel reports are generated two days after the pay period ends.

File Storage & Export
---------------------
All reports are stored locally under:

Documents/AIAI_PM_App/Payroll_Excels/YYYY-MM/Payroll_YYYY-MM.xlsx

- Each employee receives a dedicated worksheet labeled by week.
- Reports are grouped by month and compatible with Microsoft Excel.
- Pro and Enterprise tiers support enhanced export customization.

Feature Tiers
-------------

Basic
-----
- Supports multiple admin accounts (Admin Add‑on required).
- Core production‑management features for individuals or small teams.
- Limited export customization.
- Automatic database cleanup.

Pro
---
- All Basic features.
- Enhanced Excel exports.
- Prepopulated database fields for:
  • Materials
  • Employees
  • Builders
- Faster data entry with structured dropdowns.

Enterprise
----------
- All Pro features.
- Multiple installer accounts (Installer Add‑on required).
- Custom reporting templates.
- Priority support.
- Installer login functionality.
- Daily production input by installers.
- Separate login pages for admins and installers.

Update System
-------------
The app includes a built‑in update mechanism:

- Checks GitHub for the latest version.
- Downloads update packages (production_manager_app_update.zip).
- Automatically backs up the current installation.
- Automatically rolls back if an update fails.
- Uses a unified version_info.json structure.

Security
--------
- Salted + hashed admin credentials.
- Encrypted local storage for license and session data.
- No cloud storage or external session tracking.
- Role‑based access control for admins and installers.

License Statement
-----------------
All Rights Reserved
Copyright © 2025 Automating Innovating AI

The Production Manager App (.exe) is proprietary software and is not distributed via GitHub.

Unauthorized copying, distribution, reverse engineering, or modification of the software or its components is strictly prohibited.

Possession of this documentation does not grant any rights to use, reproduce, or distribute the Production Manager App.

The software is provided "AS IS", without warranty of any kind, express or implied.

For access to the app, visit: https://automatinginnovatingai.wordpress.com
For support, contact: automatinginnovatingai@outlook.com