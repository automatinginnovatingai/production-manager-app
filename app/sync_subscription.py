from db_connection import get_db_connection
from license_validator import gumroad_verify, normalize_gumroad_variant
import hmac
import hashlib
import os


# ---------------------------------------------------------
# Verify license with Gumroad
# ---------------------------------------------------------
def verify_license_with_gumroad(license_key: str):
    response = gumroad_verify(license_key)
    if not response or not response.get("success"):
        return None
    return response.get("purchase", {})


# ---------------------------------------------------------
# Sync subscription plan + store hashed license
# ---------------------------------------------------------
def sync_subscription_with_gumroad(company_id: str, license_key: str, purchase: dict):
    raw_variant = purchase.get("variants")
    subscription_plan = normalize_gumroad_variant(raw_variant)
    last_verified = purchase.get("updated_at")

    # Create salt for hashing
    salt = os.urandom(32)

    # Hash Gumroad license key
    gumroad_hash = hmac.new(
        salt,
        license_key.encode("utf-8"),
        hashlib.sha256
    ).digest()

    conn, cursor = get_db_connection()

    # Update company subscription plan
    cursor.execute("""
        UPDATE companies
        SET subscription_plan = ?, payment_status = 'active'
        WHERE company_id = ?
    """, (subscription_plan, company_id))

    # Store hashed license in activations table
    cursor.execute("""
        INSERT INTO activations (gumroad_key_hash, installer_id, plan)
        VALUES (?, ?, ?)
    """, (gumroad_hash, company_id, subscription_plan))

    conn.commit()
    return subscription_plan


# ---------------------------------------------------------
# Upgrade flow: user enters a NEW license key
# ---------------------------------------------------------
def upgrade_license(company_id: str, new_license_key: str):
    purchase = verify_license_with_gumroad(new_license_key)
    if not purchase:
        return None  # invalid or revoked

    return sync_subscription_with_gumroad(company_id, new_license_key, purchase)