from db_connection import get_db_connection
import sys

session_context = {}

# ---------------------------------------------------------
# SETTERS
# ---------------------------------------------------------
def set_user(username, user_key, company_name, is_admin, license_id, subscription_plan):
    session_context["username"] = username
    session_context["user_key"] = user_key
    session_context["company_name"] = company_name
    session_context["is_admin"] = is_admin
    session_context["license_id"] = license_id
    session_context["subscription_plan"] = subscription_plan

def set_installer(username, user_key, is_installer, license_id, subscription_plan):
    session_context["username"] = username
    session_context["user_key"] = user_key
    session_context["is_installer"] = is_installer
    session_context["license_id"] = license_id
    session_context["subscription_plan"] = subscription_plan

# ---------------------------------------------------------
# GETTERS
# ---------------------------------------------------------
def get_user(): return session_context.get("username")
def get_user_key(): return session_context.get("user_key")
def get_company_name(): return session_context.get("company_name")
def get_is_admin(): return session_context.get("is_admin")
def get_is_installer(): return session_context.get("is_installer")
def get_subscription_plan_from_session(): return session_context.get("subscription_plan")

# ---------------------------------------------------------
# CLEAR + EXIT
# ---------------------------------------------------------
def clear_user():
    session_context.clear()

def exit():
    clear_user()
    sys.exit(0)

# ---------------------------------------------------------
# FLAG NORMALIZATION
# ---------------------------------------------------------
def normalize_flag(value):
    if value is None:
        return False
    v = str(value).strip().lower()
    return v in ("yes", "1", "true", "y", "t")

# ---------------------------------------------------------
# PLAN ENFORCEMENT
# ---------------------------------------------------------
def enforce_plan(*allowed_plans):
    plan = get_subscription_plan_from_session()
    return plan in allowed_plans

def enforce_installer_plan(*allowed_plans):
    plan = get_subscription_plan_from_session()
    return plan in allowed_plans

# ---------------------------------------------------------
# VERIFY ADMIN
# ---------------------------------------------------------
def verify_admin():
    username = get_user()
    if not username:
        return False

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT is_admin FROM users WHERE username = ?",
            (username,)
        )
        row = cursor.fetchone()

        if not row:
            return False

        db_is_admin = normalize_flag(row[0])
        session_is_admin = normalize_flag(get_is_admin())

        return db_is_admin and session_is_admin

# ---------------------------------------------------------
# VERIFY INSTALLER
# ---------------------------------------------------------
def verify_installer():
    username = get_user()
    if not username:
        return False

    with get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute(
            "SELECT is_installer FROM AIAI_Employee_Info WHERE Employee_Username = ?",
            (username,)
        )
        row = cursor.fetchone()

        if not row:
            return False

        db_is_installer = normalize_flag(row[0])
        session_is_installer = normalize_flag(get_is_installer())

        return db_is_installer and session_is_installer

def exit_session():
    sys.exit()