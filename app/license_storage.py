import os
import json
import win32crypt

CONFIG_PATH = r"C:\ProgramData\AIManager\activation.json"

# Fix for PyInstaller: define constant manually
CRYPTPROTECT_LOCAL_MACHINE = 0x4

def dpapi_encrypt(data: bytes) -> bytes:
    return win32crypt.CryptProtectData(
        data,
        None,
        None,
        None,
        None,
        CRYPTPROTECT_LOCAL_MACHINE
    )

def dpapi_decrypt(data: bytes) -> bytes:
    return win32crypt.CryptUnprotectData(
        data,
        None,
        None,
        None,
        0
    )[1]

def save_local_activation(activation_id, sql_host, sql_db, sql_user, sql_pwd):
    payload = json.dumps({
        "activation_id": activation_id,
        "sql_host": sql_host,
        "sql_db": sql_db,
        "sql_user": sql_user,
        "sql_pwd": sql_pwd
    }).encode()

    encrypted = dpapi_encrypt(payload)

    os.makedirs(os.path.dirname(CONFIG_PATH), exist_ok=True)
    with open(CONFIG_PATH, "wb") as f:
        f.write(encrypted)

def load_local_activation():
    if not os.path.exists(CONFIG_PATH):
        raise ValueError("Activation not configured on this machine.")

    with open(CONFIG_PATH, "rb") as f:
        encrypted = f.read()

    decrypted = dpapi_decrypt(encrypted)
    return json.loads(decrypted.decode())