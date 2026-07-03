
☣️ VIRUSBABA-RAT

Remote Administration Toolkit for Educational & Research Purposes

Version: 3.0
License: MIT
Python: 3.10+


📌 Overview

VIRUSBABA-RAT is a lightweight, educational Remote Administration Toolkit built with Python and Firebase. It is designed to demonstrate how remote monitoring and file transfer systems work behind the scenes.

⚠️ Important: This project is intended ONLY for educational purposes, authorized security testing, and personal research. You must have explicit permission from the system owner before using this tool. The author is not responsible for any misuse.


✨ Features

- 📡 Real-Time Victim Monitoring
  - PC Name, Public IP, Wi-Fi SSID
  - CPU, RAM, Disk, Battery usage
  - Active Window & Process tracking

- 📤 Remote File Transfer
  - Send any file (.exe, .bat, .pdf, .jpg, etc.)
  - Automatically opens on the victim's PC (just like double-click)
  - Supports all file types with default Windows associations

- ☁️ Firebase Backend
  - Firestore for real-time telemetry
  - Cloud Storage for secure file hosting

- ⚙️ Persistent & Stealth
  - Auto-startup via Windows Registry
  - Windows Defender exclusion (self-whitelisting)

- 🛠️ Custom Payload Builder
  - Built directly into the Controller GUI
  - Generate unlimited unique payloads with one click


🚀 Getting Started

Prerequisites

- Python 3.10+ installed on your system.
- A Google Firebase account (free tier works).
- Enable Firestore and Storage in your Firebase project.

Installation

1. Clone the repository
   git clone https://github.com/VIRUSBABA/VIRUSBABA-RAT.git
   cd VIRUSBABA-RAT

2. Install Python dependencies
   pip install -r requirements.txt

3. Set up Firebase
   - Go to your Firebase Console → Project Settings → Service Accounts.
   - Generate a new Service Account Key (.json file).
   - Save it securely (you will paste its content into the Controller).

4. Build the Controller
   - Run the build script:
     build_me.bat
   - Wait for the build to complete. The final GuardianController.exe will be in the dist/ folder.


🖥️ Usage

1. Open the Controller
   - Run dist\GuardianController.exe
   - Login: admin / admin

2. Configure Firebase
   - Go to the Firebase tab.
   - Paste the entire content of your serviceAccountKey.json.
   - Click Save and Test Connection (ensure it says "Success").

3. Generate a Payload
   - Go to the Builder tab.
   - Enter a victim name (e.g., Target-PC).
   - Click 🔥 Generate RAT.
   - The new Target-PC_RAT.exe will appear on your Desktop.

4. Deploy & Monitor
   - Run the generated EXE on the target machine (it runs silently).
   - Go to the Dashboard tab and click Refresh List.
   - The victim will appear with 🟢 ONLINE status.
   - Click on the victim to see PC details, IP, and Resources.

5. Send a File
   - Select the victim from the sidebar.
   - Click 📤 Send File.
   - Choose any file from your local system.
   - The file will upload to Firebase Storage, download to the victim's Downloads folder, and open automatically.


📸 Screenshots

Login Screen          | Main Dashboard
-|
[Login](Screenshots/login.png) | [Dashboard](Screenshots/dashboard.png)

Payload Builder       | Send File
-|
[Builder](Screenshots/builder.png) | [File Transfer](Screenshots/file_transfer.png)


🏗️ Project Structure

VIRUSBABA-RAT/
├── controller.py          # Main GUI (PyQt6)
├── payload_stub.py        # Victim agent (telemetry + file receiver)
├── build_me.bat           # One-click build script
├── embed_payload.py       # Embeds payload into controller
├── requirements.txt       # Python dependencies
└── dist/                  # Built EXE files (after compiling)


🔧 Troubleshooting

Issue                     | Solution
--|--
Firebase Test Fails       | Ensure your serviceAccountKey.json is valid and copied correctly. Enable Firestore & Storage.
Victim Not Showing        | Wait 10 seconds after running the payload. Click Refresh List. Ensure the victim has internet.
File Doesn't Open         | Ensure the victim has a default program associated with the file type (e.g., PDF reader for .pdf).
Windows Defender Blocks   | The payload includes an auto-exclusion feature. If flagged, temporarily disable Real-time Protection or add the folder to exclusions manually.

👨‍💻 Author

Name: VIRUSBABA (Muhammad Subhan)
Purpose: Educational & Research
LinkedIn: https://www.linkedin.com/in/muhammad-subhan-28a638327

⚠️ Disclaimer

This software is provided for educational and authorized testing purposes only. The author does not condone illegal activities or unauthorized access to computer systems. By using this software, you agree that you are solely responsible for complying with all applicable local, state, and federal laws. The author assumes no liability for any misuse or damage caused by this software.

📄 License

This project is licensed under the MIT License – see the LICENSE file for details.
