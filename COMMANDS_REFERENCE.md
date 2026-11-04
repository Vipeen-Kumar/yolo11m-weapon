# 💻 Command Reference Guide

## 🟢 RUNNING THE APP (Main Commands)

### Easiest Way - Double-Click File
```
Double-click: run_streamlit_app.bat
```

### Or Use These Commands

#### Windows CMD
```cmd
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
venv\Scripts\activate
streamlit run streamlit_app.py
```

#### Windows PowerShell
```powershell
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
.\venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

#### Using Batch File (CMD)
```cmd
run_streamlit_app.bat
```

#### Using PowerShell File (PowerShell)
```powershell
.\run_streamlit_app.ps1
```

---

## 🔧 VIRTUAL ENVIRONMENT COMMANDS

### Activate venv

**Windows CMD:**
```cmd
venv\Scripts\activate
```

**Windows PowerShell:**
```powershell
.\venv\Scripts\Activate.ps1
```

### Deactivate venv
```cmd
deactivate
```

### Reinstall All Dependencies
```cmd
pip install -r requirements.txt
```

### Install Streamlit Only
```cmd
pip install streamlit
```

### Install Specific Package Version
```cmd
pip install streamlit==1.28.0
```

### List All Installed Packages
```cmd
pip list
```

### Show Package Information
```cmd
pip show streamlit
```

### Upgrade pip
```cmd
python -m pip install --upgrade pip
```

---

## 🚀 STREAMLIT-SPECIFIC COMMANDS

### Run App (Basic)
```cmd
streamlit run streamlit_app.py
```

### Run on Different Port
```cmd
streamlit run streamlit_app.py --server.port 8502
```

### Run with Debug Mode
```cmd
streamlit run streamlit_app.py --logger.level=debug
```

### Run without Browser Auto-Open
```cmd
streamlit run streamlit_app.py --browser.gatherUsageStats false
```

### Clear Streamlit Cache
```cmd
streamlit cache clear
```

### Check Streamlit Version
```cmd
streamlit --version
```

### Show Streamlit Configuration
```cmd
streamlit config show
```

---

## 🔍 DIAGNOSTIC COMMANDS

### Verify Python Installation
```cmd
python --version
```

### Verify Python Path
```cmd
python -c "import sys; print(sys.executable)"
```

### Check if Streamlit is Installed
```cmd
python -c "import streamlit; print(streamlit.__version__)"
```

### Check if YOLO is Installed
```cmd
python -c "import ultralytics; print(ultralytics.__version__)"
```

### Check if OpenCV is Installed
```cmd
python -c "import cv2; print(cv2.__version__)"
```

### Check if PyTorch is Installed
```cmd
python -c "import torch; print(torch.__version__)"
```

### List All Important Versions
```cmd
python -c "import streamlit as st; import ultralytics; import cv2; import torch; import numpy; print(f'Streamlit: {st.__version__}'); print(f'YOLOv11: {ultralytics.__version__}'); print(f'OpenCV: {cv2.__version__}'); print(f'PyTorch: {torch.__version__}'); print(f'NumPy: {numpy.__version__}')"
```

---

## 📦 DEPENDENCY COMMANDS

### Install All from requirements.txt
```cmd
pip install -r requirements.txt
```

### Install Without Cache (Clean Install)
```cmd
pip install --no-cache-dir -r requirements.txt
```

### Update All Packages
```cmd
pip install --upgrade -r requirements.txt
```

### Create New requirements.txt
```cmd
pip freeze > requirements.txt
```

### Install Single Package with Specific Version
```cmd
pip install streamlit==1.28.0
pip install ultralytics==8.0.0
pip install opencv-python==4.8.0
```

### Uninstall Package
```cmd
pip uninstall streamlit
```

### Uninstall Multiple Packages
```cmd
pip uninstall streamlit ultralytics opencv-python -y
```

---

## 🎯 YOLO COMMANDS (Legacy CLI)

### Run on Webcam (Legacy)
```cmd
python run_yolo.py --mode webcam --model best.pt
```

### Run on Image (Legacy)
```cmd
python run_yolo.py --mode image --source photo.jpg --model best.pt
```

### Run on Video (Legacy)
```cmd
python run_yolo.py --mode video --source video.mp4 --model best.pt
```

### Run Webcam for 60 Seconds (Legacy)
```cmd
python run_yolo.py --mode webcam --duration 60 --model best.pt
```

---

## 🛠️ TROUBLESHOOTING COMMANDS

### Test if Webcam Works (Python)
```cmd
python -c "import cv2; cap = cv2.VideoCapture(0); print(f'Webcam available: {cap.isOpened()}'); cap.release()"
```

### Check Available Cameras
```cmd
python -c "import cv2; [print(f'Camera {i}: {cv2.VideoCapture(i).isOpened()}') for i in range(5)]"
```

### Clear pip Cache
```cmd
pip cache purge
```

### Verify All Dependencies at Once
```cmd
python -c "
try:
    import streamlit
    import cv2
    import ultralytics
    import torch
    import numpy
    import PIL
    print('✅ All dependencies installed successfully!')
except ImportError as e:
    print(f'❌ Missing dependency: {e}')
"
```

### Check GPU Availability (PyTorch)
```cmd
python -c "import torch; print(f'GPU Available: {torch.cuda.is_available()}'); print(f'GPU Device: {torch.cuda.get_device_name(0) if torch.cuda.is_available() else \"None\"}')"
```

---

## 📋 WINDOWS-SPECIFIC COMMANDS

### Navigate to Project Directory (CMD)
```cmd
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
```

### Navigate to Project Directory (PowerShell)
```powershell
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
```

### List Files in Directory (CMD)
```cmd
dir
```

### List Files in Directory (PowerShell)
```powershell
Get-ChildItem
```

### Remove venv Folder (CMD)
```cmd
rmdir /s /q venv
```

### Remove venv Folder (PowerShell)
```powershell
Remove-Item -Recurse -Force venv
```

### Copy File (CMD)
```cmd
copy run_streamlit_app.bat run_streamlit_app_backup.bat
```

### Run Batch File from CMD
```cmd
run_streamlit_app.bat
```

### Run PowerShell Script
```powershell
.\run_streamlit_app.ps1
```

### Check if Process Running on Port 8501
```cmd
netstat -ano | findstr :8501
```

### Kill Process on Port 8501 (PowerShell)
```powershell
Stop-Process -Id (Get-NetTCPConnection -LocalPort 8501).OwningProcess -Force
```

---

## 🚀 QUICK COPY-PASTE COMMANDS

### Copy This Entire Block to Run App (CMD)
```cmd
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
venv\Scripts\activate
pip install -q streamlit
streamlit run streamlit_app.py
```

### Copy This to Verify Setup (CMD)
```cmd
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
venv\Scripts\activate
python -c "import streamlit, cv2, ultralytics, torch, numpy, PIL; print('✅ All dependencies ready!')"
```

### Copy This to Install Everything (CMD)
```cmd
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 📊 Useful Environment Variables

### Set Streamlit Port
```cmd
set STREAMLIT_SERVER_PORT=8502
streamlit run streamlit_app.py
```

### Disable Streamlit Analytics
```cmd
set STREAMLIT_ANALYTICS_ENABLED=false
streamlit run streamlit_app.py
```

### Enable Debug Logging
```cmd
set STREAMLIT_LOGGER_LEVEL=debug
streamlit run streamlit_app.py
```

---

## 🎯 Common Workflows

### Complete Setup from Scratch
```cmd
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
venv\Scripts\activate
pip install -r requirements.txt
streamlit run streamlit_app.py
```

### Test All Dependencies
```cmd
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
venv\Scripts\activate
python -c "import streamlit, cv2, ultralytics, torch, numpy, PIL; print('✅ Ready!')"
```

### Update Everything
```cmd
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
venv\Scripts\activate
pip install --upgrade -r requirements.txt
```

### Fresh Start (Remove and Recreate venv)
```cmd
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
rmdir /s /q venv
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

---

## 🔗 Useful Links

- **Streamlit Docs**: https://docs.streamlit.io
- **YOLOv11 Docs**: https://docs.ultralytics.com
- **PyTorch Docs**: https://pytorch.org/docs
- **OpenCV Docs**: https://docs.opencv.org

---

## 💡 TIPS

1. **Always activate venv first** before running any pip commands
2. **Copy-paste commands carefully** - some have special characters
3. **Use CMD for .bat files**, use PowerShell for .ps1 files
4. **Keep requirements.txt updated** when adding new packages
5. **Check Python version** - must be 3.8 or later

---

**Last Updated:** November 2024  
**Status:** ✅ Ready to Use
