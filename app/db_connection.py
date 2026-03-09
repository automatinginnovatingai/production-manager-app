import pyodbc
from license_storage import load_local_activation

def get_db_connection():
    try:
        cfg = load_local_activation()
    except Exception:
        # Return None so caller can redirect to SQLConnectionFrame
        return None, None

    host = cfg["sql_host"]
    db = cfg["sql_db"]
    user = cfg["sql_user"]
    pwd = cfg["sql_pwd"]

    # Windows Authentication mode
    if user is None and pwd is None:
        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={host};"
            f"DATABASE={db};"
            f"Trusted_Connection=yes;"
            "Encrypt=no;"
        )

    # SQL Authentication mode
    else:
        conn_str = (
            f"DRIVER={{ODBC Driver 18 for SQL Server}};"
            f"SERVER={host};"
            f"DATABASE={db};"
            f"UID={user};"
            f"PWD={pwd};"
            "Encrypt=yes;TrustServerCertificate=no;Connection Timeout=60;"
        )

    conn = pyodbc.connect(conn_str)
    return conn, conn.cursor()