Private-Network SaaS Architecture Instructions

Overview

CRM, Payroll, and Inventory applications operate like a Software-as-a-Service (SaaS) platform, but instead of running on the public internet, they run on a private network using a Python-based executable (.exe). This allows all authorized users across different regions, states, divisions, or countries to use the same application installation while keeping their data fully isolated and secure.

Key Principles

1. One Application Installation for the Entire Corporation

The global/corporate admin only needs to download and install the application once.

All registered users can use this same application as long as they have permission to access the corporate server.

No additional installations are required for other regions, states, or divisions.

2. Private Network or VPN Access Required

Users must be connected to the corporation’s private network or VPN.

If they can reach the corporate server, they can use the app—regardless of physical location.

3. Multiple Users Supported Simultaneously

The system supports many users at the same time without conflict.

SQL Server manages concurrent access using transactions and row-level locking.

Each user session is independent and does not interfere with others.

4. Data Isolation and Security

All data separation is handled by the backend using company_id isolation.

Role-Based Access Control (RBAC) ensures users only see what their role allows.

Users from different divisions or regions cannot access each other’s data.

5. Multiple GUIs Can Run at the Same Time

Mulitple interfaces can all be used simultaneously by different users.

Each GUI runs locally on the user’s machine and connects to the same backend.

There is no limitation based on location or number of active users.

6. SaaS-Like Behavior on a Private Network

The architecture mirrors a cloud SaaS system:

One shared application

Centralized backend

Multiple simultaneous users

Full data isolation

The only difference is that the app runs as a desktop executable instead of through a web browser.

Summary

One installation serves the entire corporation.

Users anywhere can access the app if they have private network/VPN access.

Multiple users can work at the same time without issues.

Data is fully isolated using company_id and RBAC.

The system behaves like a SaaS platform but operates on a private network.

Practical Example

A user in California opens the Employee Portal.

A user in Texas opens the Production Worksheet.

A global admin in New York opens the Admin Interface.

All three connect to the same corporate server.

All three work simultaneously without conflict.

Each sees only the data their role and company permissions allow.

Final Notes

This architecture is designed for scalability, security, and simplicity. As long as users can reach the corporate server through the private network or VPN, they can use the CRM, Payroll, and Inventory applications from anywhere with full functionality and data protection.