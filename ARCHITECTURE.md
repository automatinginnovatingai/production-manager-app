"""
Production Manager App – Architecture Overview & License Statement
==================================================================

Overview:
---------
The Production Manager App is a closed-source Windows `.exe` application designed for offline use,
with secure license enforcement and automated Excel reporting. It does not rely on cloud services
or persistent backend sessions.

Architecture:
-------------
License Enforcement Flow:
    User Launches App → License Prompt → Gumroad API Validation → Local Unlock

    - On first launch, the app prompts for a Gumroad license key.
    - The key is verified via Gumroad’s /v2/licenses/verify endpoint.
    - If valid, the encrypted `.exe` payload is unlocked and the app initializes.
    - License status may be revalidated periodically (e.g. every 7 days).

Local Session Context:
    - All user activity is stored locally in an encrypted SQLite database.
    - No Redis, cloud sync, or external session store is used.
    - Secure login is enforced using salted + hashed admin credentials.

Payroll & Job Entry Workflow:
    Admin Login → Job Entry → Payroll Calculation → Excel Export

    - Admin enters job details, employee info, and material usage.
    - Payroll is calculated using configurable methods:
        • Square footage × rate
        • Bags installed × piece rate
        • Hourly wage
    - Pay is auto-split across employees per job.
    - Excel reports are auto-generated two days after the pay period ends.

File Storage & Export:
    - All data is stored locally under:
        Documents/AIAI_PM_App/Payroll_Excels/YYYY-MM/Payroll_YYYY-MM.xlsx
    - Each employee receives a dedicated worksheet labeled by week.
    - Reports are compatible with Microsoft Excel and grouped by month.

Versions:
---------
The app is offered in three tiers to suit different team sizes and reporting needs:
    The Production Manager App is available in three tiers, tailored to different team sizes and operational needs:
        • Basic
            Supports multiple admin accounts with seperate Admin Add-on license.
            Provides all essential production‑management features for individuals or small teams.
            Includes limited export customization and automatic database cleanup.
        • Pro
            Supports multiple admin accounts with seperate Admin Add-on license.
            Enhanced Excel exports and prepopulated database fields for faster paperwork:
            material details, employee profiles, and builder information.
        • Enterprise
            Includes all Pro features, plus:
            Supports multiple admin accounts with seperate Admin Add-on license.
            Supports multiple installer accounts with seperate Installer Add-on license.
            • Custom reporting templates
            • Priority support
            • Installer login functionality
            • Daily production input by installers
            • Separate login pages for admins and installers
    In the Pro and Enterprise tiers, users can prepopulate the local database with structured entries for materials, employees, and builders. These entries are automatically fetched and surfaced in dropdown menus within each employee’s production worksheet, streamlining data entry and reducing manual input errors.        

License Statement:
------------------
All Rights Reserved  
Copyright © 2025 Automating Innovating AI

This documentation is provided for informational purposes only. The Production Manager App (.exe)
is proprietary software and is not distributed via GitHub.

Unauthorized copying, distribution, reverse engineering, or modification of the software or its
components is strictly prohibited.

The receipt or possession of this documentation does not convey or imply any right to use,
reproduce, or distribute the Production Manager App.

The software is provided "AS IS", without warranty of any kind, express or implied, including but
not limited to the warranties of merchantability, fitness for a particular purpose, and
non-infringement.

For access to the app, visit: https://automatinginnovatingai.com
For support, contact: automatinginnovatingai@outlook.com
"""