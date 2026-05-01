# Production Manager App — Unified SQL Express & SQL Server Edition  
## Initial GitHub Release — Version 1.0.0

This release introduces the fully unified version of the Production Manager App, combining all features and license tiers into a single Windows `.exe` application. The app now supports **both SQL Express and SQL Server**, selected during installation, eliminating the need for separate builds or database versions.

All license tiers (Basic, Pro, Enterprise) are included in one unified application, with access determined by the user’s Gumroad license key.

---
Role‑Based Access Control (RBAC)
All AIAI applications now include a unified, secure RBAC system designed for multi‑admin environments and professional data governance.

Global Admin
Full system access. Can configure company‑wide settings, manage other admins, control data sources, and access all modules.

Local Admin
Operational access only. Can manage day‑to‑day tasks such as employees, jobs, materials, time entries, invoices, or inventory (depending on the app). Cannot modify global settings or create new companies.

Admin‑Only Registration
Only administrators can register accounts. No employee or installer self‑registration is allowed.

Dynamic UI Permissions
Each screen automatically adapts to the user’s role. Restricted modules are hidden or blocked with clear access messages.

Centralized Permission Enforcement
All role checks are handled through a unified RBAC engine to ensure consistent security across every module and workflow.

Multi‑Admin Support 
Global Admin customers can add additional administrators using the Admin Add‑on. Each admin receives their own secure login and role‑based access.

This RBAC system ensures secure, scalable, and professional‑grade access control across all AIAI applications.

---

## Included in This Release
- Basic Plan  
- Pro Plan  
- Enterprise Plan  
- Admin Add‑on  
- Installer Add‑on  
- Unified SQL Express + SQL Server architecture  
- One installer, one app, one onboarding flow  

---

## Plan Descriptions

### **Basic Plan**
Provides all essential production‑management features for individuals or small teams.  
Includes core workflow tools, job entry, payroll calculation, and standard reporting.  
Ideal for users who need a reliable, cost‑effective foundation without advanced automation.

---

### **Pro Plan**
Expands on the Basic plan with enhanced productivity tools and deeper reporting.  
Designed for growing teams that manage multiple projects and need more flexibility.  
Includes prepopulated database fields for materials, employees, and builders to speed up data entry.

---

### **Enterprise Plan**
Unlocks the full capabilities of the system, including everything in Pro plus advanced features and enterprise‑grade controls.  
Required for organizations with multiple administrators or complex operational needs.  
Serves as the base license for all administrative and installer functionality.

Enterprise includes:
- Custom reporting templates  
- Priority support  
- Installer login functionality  
- Daily production input by installers  
- Separate login pages for admins and installers  

---

### **Admin Add‑on**
A supplemental license for each additional administrator beyond the main admin included with the Enterprise plan.  
Ensures secure, individual admin access without shared credentials.  
Cannot function alone — requires an active Basic, Pro, or Enterprise plan.

---

### **Installer Add‑on**
Available only to Enterprise customers.  
Provides installer‑level login access for organizations that deploy installers or field crews.  
Cannot be used as a standalone license.

---

## License Activation
This app requires a valid Gumroad license key to unlock full functionality.

- You will be prompted to enter your license key on first launch.  
- The app verifies your key securely via Gumroad’s API.  
- If the license is invalid or revoked, access will be restricted.  
- Internet access is required for initial license validation.

After activation, the app operates fully offline.

---

## Database
The Production Manager App now supports **two database modes**, selected during installation:

### **SQL Express (Local Database — Recommended for 1–5 users)**
- Automatically installed and configured by the installer  
- Ideal for individuals, small teams, and single‑machine setups  
- Fully offline and self‑contained  

### **SQL Server (Remote or On‑Prem Server)**
- Connect to an existing SQL Server instance  
- Supports multi‑user environments and IT‑managed deployments  
- Ideal for medium‑to‑large teams or companies with dedicated servers  

Both modes use the same unified application and feature set.

---

## Stability
This version is the current stable build distributed through the updater and is the foundation for all future updates.
