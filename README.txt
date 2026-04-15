Production Manager App – Offline Payroll & Job Tracker (.exe)

This repository contains documentation for the Production Manager App — a closed‑source Windows application designed for small to large production teams to manage job entries, payroll, and material usage entirely offline.

The Production Manager App was built to modernize workflows in the construction industry—specifically within fiberglass insulation and gutters. After witnessing firsthand how companies rely on paper-heavy, manual processes to handle installer paperwork, I saw an opportunity to streamline operations.
This app replaces inefficient routines with a secure, offline solution that automates payroll calculations, centralizes job data, and generates Excel reports—no cloud dependency, no wasted time, and no paper trails. It’s designed to bring real-world construction workflows into the future of tech, without compromising operational safety or control.

This release delivers major upgrades to workflow management, reporting, and SQL Server data handling. All legacy versions have been consolidated into one unified build. SQLite has been fully removed. The application now uses SQL Server Express or Full SQL Server, depending on the user’s environment.

------------------------------------------------------------
NEW FEATURES AND ENHANCEMENTS
------------------------------------------------------------

1. New Work Ticket Form
Users can now create, edit, and manage daily production work tickets directly inside the application.

2. SQL Data Transfer Tool (Old Host → New Host)
A guided workflow helps users migrate their SQL Server database from an old machine to a new host with minimal downtime.

3. Work Ticket Reporting Suite
Users can now generate:
- Daily work ticket reports
- Weekly summaries
- Monthly reports
Reports can be printed, exported to Excel, or generated as PDF files.

4. Unified SQL Server Architecture (SQLite Removed)
The previous SQLite version has been retired. The app now supports:
- SQL Server Express (free, recommended for small teams)
- Full SQL Server Standard/Enterprise (enterprise-grade)

The user selects their SQL Server instance during setup. The app automatically configures the connection and prepares the database schema.

5. UI and Stability Improvements
- More intuitive interface
- Streamlined upgrade flow using Gumroad license tiers
- Enhanced security for license validation and local data handling
- Minor bug fixes and performance improvements

------------------------------------------------------------
MULTI-USER SYNC & NETWORK REQUIREMENTS
------------------------------------------------------------

The Production Manager App uses SQL Server Express or Full SQL Server as the central data source. This allows multiple employees to stay up to date with job changes, work tickets, and reporting data in real time.

For multi-user environments, employees must be connected to the company’s private network. This can be done through:

• Local office network (LAN)
• Company VPN (for remote workers)

When connected, all users share the same SQL Server database and receive updates instantly. This ensures consistent data across all devices and prevents version conflicts.

------------------------------------------------------------
DATABASE SELECTION (CHOOSE DURING INSTALLATION)
------------------------------------------------------------

SQL Server Express (Local SQL Server – Small Businesses)
- Best for small businesses with 1–5 employees.
- Installs Microsoft SQL Server Express automatically during setup.
- Creates a secure, local SQL database on the company’s computer.
- Supports multiple users on the same network.
- More reliable and scalable than file-based databases.
- Free to use (SQL Server Express has no licensing cost).
- Has Microsoft‑imposed limits on database size, memory, and CPU.
- Choose SQL Server Express if you want a free, reliable, multi‑user local database.

Full SQL Server (Enterprise‑Grade – Medium to Large Companies)
- Best for companies with IT infrastructure or a dedicated server.
- Uses the full version of Microsoft SQL Server (Standard or Enterprise).
- No size, memory, or CPU limits.
- Supports many users, large data volumes, and high‑performance workloads.
- Includes advanced features such as SQL Server Agent, high availability, and enterprise‑level security.
- Requires a paid SQL Server license.
- Choose Full SQL Server if your company needs maximum performance, scalability, and enterprise features.

------------------------------------------------------------
KEY FEATURES
------------------------------------------------------------

- Offline‑first .exe app with no cloud dependencies
- Secure login with salted + hashed credentials
- Weekly payroll calculation based on:
  • Square footage × rate
  • Bags installed × piece rate
  • Hourly wage
- Auto‑splitting pay across multiple employees per job
- Full job entry interface with builder, model, lot/block, and insulation specs
- Auto‑export to Excel with per‑employee sheets grouped by week
- SQL Express or SQL Server database storage (installer‑selected)
- Built‑in data transfer system using SQL .bak files
- Automatic version checking and update prompts
- Unified architecture — all plans in one application

------------------------------------------------------------
LICENSE ENFORCEMENT
------------------------------------------------------------

The .exe is encrypted and gated by Gumroad license validation.

- Users must enter a valid license key on first launch
- License keys are verified via Gumroad’s API
- Invalid or revoked keys restrict access
- No backend session store — validation is stateless and secure
- After activation, the app operates fully offline

------------------------------------------------------------
VERSIONS AVAILABLE
------------------------------------------------------------

The app is offered in three tiers to suit different team sizes and reporting needs:

Basic
- Single‑user or small team access
- Core job entry and payroll tools
- Limited export customization

Pro
- All Basic features
- Enhanced Excel exports
- Prepopulated materials, employees, and builders
- Faster data entry with structured dropdowns

Enterprise
- All Pro features
- Custom reporting templates
- Priority support
- Installer login functionality
- Daily production input by installers
- Separate login pages for admins and installers

Add‑ons
- Installer Add‑on: Allows installers to log in and complete production paperwork (Enterprise required)
- Admin Add‑on: Allows additional administrators to log in across all versions

All versions are distributed via Gumroad. License keys are unique per purchase and required to unlock the app.

👉 Production Manager App Gumroad Page:
https://automateai56.gumroad.com/l/koxupw


------------------------------------------------------------
THIS REPO
------------------------------------------------------------

This GitHub repository does NOT contain the .exe binary or source code.  
It exists to document the app’s architecture, license model, and usage flow.

------------------------------------------------------------
LICENSE
------------------------------------------------------------

This software is proprietary and closed‑source.  
See LICENSE.txt for details.

------------------------------------------------------------
SUPPORT
------------------------------------------------------------

Questions or feedback? Contact the developer:  
automatinginnovatingai@outlook.com