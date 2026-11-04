# 🎯 YOLO Streamlit Web App - Complete Guide

## ✨ Features

✅ **Model Selection**: Choose between `best.pt` and `last.pt`  
✅ **Image Detection**: Upload images and get instant detection results  
✅ **Video Detection**: Process videos with YOLO inference  
✅ **Webcam Detection**: Real-time detection from your laptop camera  
✅ **Confidence Threshold**: Adjustable confidence threshold (0-100%)  
✅ **Statistics Display**: See detailed detection metrics  
✅ **Download Results**: Save annotated images

---

## 🚀 Quick Start (3 Steps)

### Step 1: Open Command Prompt or PowerShell

**Windows CMD:**
```bash
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
```

**Windows PowerShell:**
```bash
cd C:\Users\vipee\Desktop\college\LY-all-pro\yolo-m-vip
```

### Step 2: Run the App

#### Option A: Using Batch File (Easiest - CMD)
```bash
run_streamlit_app.bat
```

#### Option B: Using PowerShell
```bash
.\run_streamlit_app.ps1
```

#### Option C: Manual Command

**CMD:**
```bash
venv\Scripts\activate.bat
streamlit run streamlit_app.py
```

**PowerShell:**
```bash
.\venv\Scripts\Activate.ps1
streamlit run streamlit_app.py
```

### Step 3: The app automatically opens in your browser
- If it doesn't, visit: `http://localhost:8501`

---

## 📖 How to Use the App

### 1. **Load a Model (First Step)**
   - Go to the sidebar on the left (⚙️ Configuration)
   - Select either **best.pt** or **last.pt**
   - Click **🔄 Load Model** button
   - Wait for ✅ success message

### 2. **Choose Detection Mode**
   - Select one of three modes:
     - 📷 **Image Detection**
     - 🎬 **Video Detection**
     - 📹 **Webcam Detection**

### 3. **Adjust Confidence Threshold (Optional)**
   - Use the slider in the sidebar
   - Range: 0% to 100%
   - Lower = more detections (more false positives)
   - Higher = fewer detections (only very confident ones)

### 4. **Run Detection**
   - Follow the instructions for your chosen mode
   - Click the detection button
   - View results and download if needed

---

## 📷 Image Detection

1. Select **📷 Image Detection** mode
2. Upload an image file (JPG, PNG, BMP, WebP)
3. Click **🚀 Run Detection**
4. View results:
   - Original image on the left
   - Annotated image on the right
   - Detection statistics
   - Object details table
5. Click **⬇️ Download Annotated Image** to save the result

**Supported Formats:** JPG, JPEG, PNG, BMP, WebP

---

## 🎬 Video Detection

1. Select **🎬 Video Detection** mode
2. Upload a video file (MP4, AVI, MOV, MKV, etc.)
3. Click **🚀 Run Detection on Video**
4. Wait for processing (can take a few moments)
5. View the processed video
6. Click **⬇️ Download Processed Video** to save the result

**Supported Formats:** MP4, AVI, MOV, MKV, FLV, WMV

⚠️ **Note:** Video processing takes longer. Be patient!

---

## 📹 Webcam Detection

1. Select **📹 Webcam Detection** mode
2. Adjust settings in the right panel:
   - **Duration:** How long to run (5-300 seconds, default 30)
   - **Frame Skip:** Process every nth frame (higher = faster)
3. Click **🎥 Start Webcam**
4. Allow camera access if prompted by Windows
5. Watch real-time detections
6. View statistics as they update

**Settings Explained:**
- **Duration:** 30 seconds is good for testing
- **Frame Skip:** 
  - 1 = Process every frame (slow but accurate)
  - 2 = Process every 2nd frame (faster)
  - 3+ = Even faster (use for weak computers)

---

## 🔧 Virtual Environment Guide

### What is a Virtual Environment?

A virtual environment is an isolated Python space for this project. It keeps all dependencies separate from your system Python.

### How to Activate (Manual)

**Windows CMD:**
```bash
venv\Scripts\activate
```

**Windows PowerShell:**
```bash
.\venv\Scripts\Activate.ps1
```

You'll see `(venv)` at the start of your command line when active.

### How to Deactivate

```bash
deactivate
```

### Reinstall Dependencies (If Needed)

```bash
pip install -r requirements.txt
```

### Check Installed Packages

```bash
pip list
```

---

## 📦 Dependencies

All packages are already installed. Here's what's installed:

- **ultralytics** - YOLOv11 model framework
- **opencv-python** - Computer vision library
- **torch** - PyTorch (AI framework)
- **torchvision** - Vision utilities
- **numpy** - Numerical computing
- **pillow** - Image processing
- **streamlit** - Web app framework

---

## ❓ Troubleshooting

### ❌ "ModuleNotFoundError: No module named 'streamlit'"

**Solution:**
```bash
venv\Scripts\activate
pip install streamlit
```

### ❌ "Could not open webcam"

**Solutions:**
- Make sure no other app is using your camera
- Check if Windows has given Python permission to access the camera:
  - Settings → Privacy & security → Camera → Allow Python
- Try restarting the app
- Try a different USB camera if available

### ❌ App runs very slowly

**Solutions:**
- Use `last.pt` instead of `best.pt` (lighter model)
- Increase "Frame Skip" in webcam mode
- Close other applications
- Check if your camera resolution is too high

### ❌ Video processing stuck or too slow

**Solutions:**
- Try a smaller video file first
- Use a lower resolution video
- Close other applications
- Be patient - processing takes time

### ❌ Port 8501 already in use

**Solution:**
```bash
streamlit run streamlit_app.py --server.port 8502
```

---

## 💻 System Requirements

- **OS:** Windows 10 or later
- **RAM:** 4GB minimum (8GB recommended)
- **GPU:** Optional (NVIDIA GPU recommended for speed)
- **Camera:** Webcam for webcam detection mode
- **Python:** 3.8 or later (already in venv)

---

## 🎯 File Structure

```
yolo-m-vip/
├── streamlit_app.py           ← Main web app file
├── run_streamlit_app.bat      ← Run app from CMD
├── run_streamlit_app.ps1      ← Run app from PowerShell
├── run_yolo.py                ← CLI version (legacy)
├── best.pt                    ← Best model
├── last.pt                    ← Last checkpoint
├── requirements.txt           ← Dependencies
├── STREAMLIT_GUIDE.md         ← This file
├── venv/                      ← Virtual environment
└── results/                   ← Output folder (auto-created)
```

---

## 🔐 Performance Tips

### For Faster Detection:

1. **Use last.pt instead of best.pt** - Lighter model
2. **Lower confidence threshold** - Fewer calculations
3. **Increase frame skip** in webcam mode
4. **Use GPU** if available (auto-enabled if NVIDIA GPU present)
5. **Close background apps** - Free up RAM

### For Better Accuracy:

1. **Use best.pt** - More accurate model
2. **Raise confidence threshold** - Only confident detections
3. **Use frame skip = 1** - Process every frame
4. **Use good lighting** - Better image quality

---

## 📊 Understanding Results

### Detection Metrics:

- **Objects Detected:** Total number of objects found
- **Confidence:** How sure the model is (0-100%)
- **Class:** Type of object detected
- **Bounding Box:** Position (X1, Y1, X2, Y2)

### Color Codes:

- Different colored boxes = different object classes
- Brighter boxes = higher confidence
- Fainter boxes = lower confidence (usually filtered out)

---

## 🆘 Getting Help

**Model Issues:**
- Make sure `best.pt` and `last.pt` are in the project folder
- Try re-downloading the models

**Camera Issues:**
- Check Windows camera permissions
- Try another app first to verify camera works
- Restart your computer

**Dependency Issues:**
- Delete `venv` folder and recreate
- Run `pip install -r requirements.txt` again

---

## 🎓 Learning Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **YOLOv11 Docs:** https://docs.ultralytics.com
- **OpenCV Docs:** https://docs.opencv.org

---

## ✨ Version Info

- **App Version:** 1.0
- **YOLOv11:** Latest
- **Streamlit:** 1.28.0+
- **Python:** 3.8+

---

**Happy Detecting! 🎯**

If you have questions, just run the app and explore!
