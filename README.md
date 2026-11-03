# YOLO11m Weapon Detection System

A real-time object detection system built with YOLOv11 (medium model) for detecting weapons and objects in images, videos, and webcam feeds. This project includes a production-ready Streamlit web application with model analytics and performance evaluation.

## 🎯 Key Features

- **Real-time Detection**: Detect weapons and objects in live webcam feeds
- **Multi-format Support**: 
  - Image detection (JPG, PNG, BMP, WebP)
  - Video detection (MP4, AVI, MOV, MKV, FLV, WMV)
  - Webcam live streaming with adjustable speed modes
- **Web-based Interface**: Streamlit application for easy access and control
- **Model Analytics**: Comprehensive dashboard for model performance evaluation
- **Configurable Parameters**: Adjustable confidence thresholds and detection settings
- **Optimized Performance**: Speed mode selection for webcam processing (Normal, Fast, Ultra Fast)
- **Result Export**: Download annotated images and detection data

## 🏗️ Project Architecture

```
yolo-m-vip/
├── streamlit_app.py          # Main Streamlit web application
├── analytics.py              # Model analytics and evaluation module
├── run_yolo.py               # CLI-based detection script
├── best.pt                   # Trained YOLOv11m model weights
├── requirements.txt          # Python dependencies
├── README.md                 # This file
└── dataset/                  # (Local only, not in GitHub)
    └── Dataset/
        ├── images/           # Training images
        ├── images_test/      # Test images
        ├── annotations/      # Annotation XML files
        └── annotations_test/ # Test annotations
```

## 🛠️ Technologies & Libraries

- **YOLO**: YOLOv11 (ultralytics) - State-of-the-art real-time object detection
- **Deep Learning**: PyTorch & TorchVision
- **Web Framework**: Streamlit - Modern Python web app framework
- **Computer Vision**: OpenCV - Image and video processing
- **Data Processing**: Pandas & NumPy
- **Visualization**: Plotly - Interactive charts and dashboards
- **Image Processing**: Pillow (PIL)

## 📋 Requirements

- Python 3.8+
- CUDA-enabled GPU (recommended for better performance)
- 8GB RAM minimum (16GB+ recommended)
- Webcam (optional, for webcam detection)

## 🚀 Installation

### 1. Clone the Repository

```bash
git clone https://github.com/Vipeen-Kumar/yolo11m-weapon.git
cd yolo11m-weapon
```

### 2. Create a Virtual Environment (Recommended)

**Windows (Command Prompt):**
```bash
python -m venv venv
venv\Scripts\activate
```

**Windows (PowerShell):**
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1
```

**Linux/Mac:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

If you encounter issues with PyTorch, install it separately:

```bash
# For CUDA 11.8 (GPU support)
pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu118

# Or for CPU only
pip install torch torchvision torchaudio
```

## 🎮 Usage

### Run the Streamlit Web Application

```bash
streamlit run streamlit_app.py
```

The application will be available at: `http://localhost:8501`

#### Features in Streamlit App:

1. **📷 Image Detection**
   - Upload image files
   - Adjust confidence threshold
   - View annotated results
   - Download detection results

2. **🎬 Video Detection**
   - Upload video files
   - Run inference on video
   - Download processed video with annotations

3. **📹 Webcam Detection**
   - Live real-time detection from your webcam
   - Three speed modes:
     - 🐢 Normal: Process every frame (most accurate)
     - ⚡ Fast: Process every 5th frame
     - 🚀 Ultra Fast: Process every 10th frame
   - Real-time statistics and metrics

4. **📊 Model Analytics**
   - Evaluate model on dataset
   - View confidence distribution
   - Analyze class-wise performance
   - Export detection results as CSV

### Command Line Interface (CLI)

Run detection from command line using `run_yolo.py`:

```bash
# Webcam detection (30 seconds)
python run_yolo.py --mode webcam

# Webcam detection (60 seconds)
python run_yolo.py --mode webcam --duration 60

# Image detection
python run_yolo.py --mode image --source photo.jpg

# Video detection
python run_yolo.py --mode video --source video.mp4

# Use specific model
python run_yolo.py --mode image --source photo.jpg --model best.pt

# Custom output directory
python run_yolo.py --mode image --source photo.jpg --output my_results
```

## 📊 Model Weights

The project includes trained YOLOv11m model weights:

- **best.pt** (38.64 MB): Best model from training (recommended)
- **last.pt** (38.64 MB): Last epoch checkpoint

Both models are included in the GitHub repository.

### Model Loading

Models are automatically loaded when selected in the Streamlit application. The app caches the model in memory for performance optimization.

## 📈 Performance Metrics

The analytics dashboard provides comprehensive performance evaluation:

- **Total Detections**: Count of all detected objects
- **Mean/Min/Max Confidence**: Detection confidence statistics
- **Detections Per Image**: Average detection count per image
- **Class Distribution**: Breakdown of detected object classes
- **Confidence Analysis**: High/medium/low confidence detection ratios
- **Images with Detections**: Count of images with at least one detection

## 🐛 Troubleshooting

### Webcam Not Working
- Ensure no other application is using the camera
- Check Windows camera permissions for Python
- Try closing and reopening the app

### Models Not Loading
- Verify `best.pt` and `last.pt` exist in the project directory
- Check file permissions
- Ensure sufficient disk space

### Slow Performance
- Use Fast or Ultra Fast speed modes for webcam
- Reduce video resolution before processing
- Close other applications
- Consider using GPU (CUDA) for faster inference

### Import Errors
- Reinstall requirements: `pip install -r requirements.txt --force-reinstall`
- Update pip: `pip install --upgrade pip`
- Verify Python version: `python --version` (must be 3.8+)

### Out of Memory
- Reduce video quality
- Process smaller videos
- Use streaming mode for large videos
- Increase system RAM or use cloud deployment

## 🌐 Deployment

### Deploy on Streamlit Cloud

1. **Push to GitHub** (already done)

2. **Connect Streamlit Cloud**:
   - Go to [Streamlit Cloud](https://streamlit.io/cloud)
   - Click "New app"
   - Select your repository: `yolo11m-weapon`
   - Set main file path: `streamlit_app.py`
   - Click "Deploy"

3. **Configure Streamlit Secrets** (if needed):
   - Add any API keys or environment variables in the Streamlit Cloud dashboard
   - Secrets will be available as `st.secrets` in the app

### Deploy on Other Platforms

For Heroku, AWS, DigitalOcean, or custom servers:

```bash
# Install Gunicorn (for production WSGI server)
pip install gunicorn

# Run Streamlit with production settings
streamlit run streamlit_app.py --server.port=$PORT --server.headless true
```

**Note**: Model size (38.64 MB per model) is suitable for cloud deployment. Free tiers may have limitations on concurrent users.

## 📁 File Descriptions

- **streamlit_app.py**: Main web application with UI for all detection modes
- **analytics.py**: YOLO11Analytics class for model evaluation and performance metrics
- **run_yolo.py**: Command-line interface for detection tasks
- **requirements.txt**: All Python dependencies with versions
- **.gitignore**: Excludes dataset, cache, and temporary files from Git

## 🔐 Security Considerations

- No credentials or API keys are stored in code
- Model weights are public (trained on custom dataset)
- All input validation is handled by Streamlit and OpenCV
- For production deployment, add HTTPS and authentication if needed

## 📝 License

This project is provided as-is. The trained model weights are included in the repository.

## 🤝 Contributing

Contributions are welcome! For major changes:
1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a pull request

## 📞 Contact & Support

- **GitHub**: https://github.com/Vipeen-Kumar/yolo11m-weapon
- **Issues**: Report bugs via GitHub Issues tab

## 🎓 References

- [YOLOv11 Documentation](https://docs.ultralytics.com/models/yolov11/)
- [Streamlit Documentation](https://docs.streamlit.io/)
- [PyTorch Documentation](https://pytorch.org/docs/stable/index.html)
- [OpenCV Documentation](https://docs.opencv.org/)

---

**Last Updated**: November 2026  
**Python Version**: 3.8+  
**Framework**: Streamlit 1.28+

