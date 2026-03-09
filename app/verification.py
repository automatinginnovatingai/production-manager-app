import uuid
from tkinter import messagebox
from db_connection import  get_db_connection, generate_hash

def host_verification():
    """Retrieve stored user key and company name from the database."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT user_key, company_name FROM companies ORDER BY company_name DESC LIMIT 1")
            result = cursor.fetchone()
            conn.close()
            return result if result else (None, None)
        except Exception as e:
            messagebox.showerror(f"Database error: {e}")
            return None, None
    return None, None

def get_stored_mac_data():
    """Retrieve stored hashed MAC address and salt from the database."""
    conn = get_db_connection()
    if conn:
        try:
            cursor = conn.cursor()
            cursor.execute("SELECT hash, salt FROM encryption_key LIMIT 1")
            result = cursor.fetchone()
            conn.close()
            return result if result else (None, None)
        except Exception as e:
            messagebox.showerror(f"Database error: {e}")
            return None, None
    return None, None

def get_mac_address():
    """Retrieve the MAC address of the current machine."""
    return ':'.join(['{:02x}'.format((uuid.getnode() >> i) & 0xff) for i in range(0, 48, 8)])

def verify_mac_address():
    """Verify if the current MAC address matches the stored hash."""
    stored_hashed_mac, stored_salt = get_stored_mac_data()
    if not stored_hashed_mac or not stored_salt:
        messagebox.showerror("MAC address verification failed: No stored hash data.")
        return False

    current_mac_address = get_mac_address()
    computed_hash = generate_hash(current_mac_address, stored_salt)

    return computed_hash == stored_hashed_mac

def verify_user():
    """Verify user key and company name from the database."""
    stored_user_key, stored_company_name = host_verification()
    if not stored_user_key or not stored_company_name:
        messagebox.showerror("User verification failed: No valid company data.")
        return False
    return True  # If data exists, user is verified
def main():
    if verify_mac_address() and verify_user():
        import Admin_Interface 
        Admin_Interface.setup_gui()
    else:
        messagebox.showerror("Verification Failed", "Unauthorized host machine.")
        exit()

if __name__ == "__main__":
    main()    