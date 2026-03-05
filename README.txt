# 🧱 Production Manager App – Offline Payroll & Job Tracker (.exe)

This repository contains documentation for the Production Manager App—a closed-source Windows application designed for small production teams to manage job entries, payroll, and material usage entirely offline.

The Production Manager App was built to modernize workflows in the construction industry—specifically within fiberglass insulation. After witnessing firsthand how companies rely on paper-heavy, manual processes to handle installer paperwork, I saw an opportunity to streamline operations.
This app replaces inefficient routines with a secure, offline  solution that automates payroll calculations, centralizes job data, and generates Excel reports—no cloud dependency, no wasted time, and no paper trails. It’s designed to bring real-world construction workflows into the future of tech, without compromising operational safety or control.

## 🔐 Key Features

- Offline-first `.exe` app with no cloud dependencies
- Secure login with salted + hashed credentials
- Weekly payroll calculation based on:
  - Square footage × rate
  - Bags installed × piece rate
  - Hourly wage
- Auto-splitting pay across multiple employees per job
- Full job entry interface with builder, model, lot/block, and insulation specs
- Auto-export to Excel with per-employee sheets grouped by week
- Local SQLite database with smart cleanup and de-duplication
- Automatic version checking and update prompts

## 🧩 License Enforcement

The `.exe` is encrypted and gated by Gumroad license validation.  
- Users must enter a valid license key on first launch  
- License keys are verified via Gumroad’s API  
- Invalid or revoked keys restrict access  
- No backend session store—validation is stateless and secure

## 🧰 Versions Available

The app is offered in three tiers to suit different team sizes and reporting needs:

| Version     | Features                                                                 |
|-------------|--------------------------------------------------------------------------|
| **Basic**   | Single-user access, manual payroll entry, limited export customization   |
| **Pro**     | Multi-user support, auto-pay splitting, enhanced Excel exports           |
| **Enterprise** | All Pro features + custom reporting, priority support, audit logging  |
| **Installer Add-on** | Allows installers to login and complete production paperwork    |
| **User must purchase Enterprise version to use Installer Add-on license                |
| **Admin Add-on** | Allows additional administrators to login to app on all 3 versions  |
| **User must purchase Admin Add-on license.                                             |

All versions are distributed via Gumroad. License keys are unique per purchase and required to unlock the app.

👉 [View all versions and purchase on Gumroad]
Production Manager App Gumroad Page
https://automateai56.gumroad.com/l/comcj

## 📁 This Repo

This GitHub repository does **not** contain the `.exe` binary or source code.  
It exists to document the app’s architecture, license model, and usage flow.

## 📜 License

This software is proprietary and closed-source.  
See [`LICENSE.txt`](LICENSE.txt) for details.

## 📷 Screenshots & Demo

Visit the Gumroad page for a demo video and UI walkthrough.  
You’ll find examples of payroll entry, Excel exports, and job tracking in action.

## 📬 Support

Questions or feedback? Contact the developer:  
📧 automatinginnovatingai@outlook.com
