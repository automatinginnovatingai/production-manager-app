import os
import json
import requests
import zipfile
import shutil
import tkinter as tk
from tkinter import messagebox

# === Configuration ===
VERSION_FILE = "version_info.json"
VERSION_URL = "https://raw.githubusercontent.com/automatinginnovatingai/production-manager-app-sql-server-express/master/version_info.json"

# The folder where your app lives
BASE_DIR = os.path.join(os.getcwd(), "app")

# === Helper Functions ===

def version_tuple(version):
    parts = version.split(".")
    return tuple(int(p) for p in parts + ['0'] * (3 - len(parts)))


def get_current_version():
    try:
        with open(VERSION_FILE, "r") as f:
            data = json.load(f)
            return data.get("sql_server_express", {}).get("version", "0.0.0")
    except FileNotFoundError:
        return "0.0.0"


def get_latest_version():
    try:
        r = requests.get(VERSION_URL, timeout=5)
        r.raise_for_status()
        data = r.json()
        return data["sql_server_express"]["version"], data["sql_server_express"]["url"]
    except Exception as e:
        messagebox.showerror("Version Check Failed", str(e))
        return None, None


def backup_current_app():
    backup_path = BASE_DIR + "_backup"
    if os.path.exists(backup_path):
        shutil.rmtree(backup_path)
    if os.path.exists(BASE_DIR):
        shutil.copytree(BASE_DIR, backup_path)


def rollback_update():
    backup_path = BASE_DIR + "_backup"
    if os.path.exists(backup_path):
        if os.path.exists(BASE_DIR):
            shutil.rmtree(BASE_DIR)
        shutil.copytree(backup_path, BASE_DIR)
        messagebox.showwarning("Rollback Performed", "App restored from backup.")


def download_update(url):
    zip_name = "sql_server_express_update.zip"
    try:
        r = requests.get(url, stream=True, timeout=10)
        r.raise_for_status()
        with open(zip_name, "wb") as f:
            for chunk in r.iter_content(8192):
                f.write(chunk)
        return zip_name
    except Exception as e:
        messagebox.showerror("Download Failed", str(e))
        return None


def apply_update(version_str, url):
    update_zip = download_update(url)

    if not update_zip:
        rollback_update()
        return False

    backup_current_app()

    try:
        with zipfile.ZipFile(update_zip, "r") as zip_ref:
            zip_ref.extractall(BASE_DIR)
        os.remove(update_zip)

        # Save new version
        with open(VERSION_FILE, "w") as f:
            json.dump({"sql_server_express": {"version": version_str}}, f, indent=4)

        messagebox.showinfo("Update Complete", f"App updated to {version_str}")
        return True

    except Exception as e:
        messagebox.showerror("Install Failed", str(e))
        rollback_update()
        return False


# === Main Update Logic ===

def check_and_update():
    current_version = get_current_version()
    latest_version, url = get_latest_version()

    if not latest_version:
        return

    if version_tuple(latest_version) > version_tuple(current_version):
        apply_update(latest_version, url)
    else:
        messagebox.showinfo("Up to Date", "You already have the latest version.")


# === Run updater ===
if __name__ == "__main__":
    check_and_update()