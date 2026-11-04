import streamlit as st
import cv2
import numpy as np
from ultralytics import YOLO
from PIL import Image
import os
from pathlib import Path
from io import BytesIO
import warnings
import pandas as pd
import plotly.graph_objects as go
import tempfile

# Import analytics module
from analytics import YOLO11Analytics

# Suppress warnings
warnings.filterwarnings("ignore")
os.environ['STREAMLIT_LOGGER_LEVEL'] = 'error'

# Disable TensorFlow/PyTorch verbose logging
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '3'
import logging
logging.getLogger('ultralytics').setLevel(logging.ERROR)

# Set page config
st.set_page_config(
    page_title="YOLO Object Detection",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
        .main-header {
            font-size: 2.5rem;
            color: #1f77b4;
            text-align: center;
            margin-bottom: 2rem;
        }
        .section-header {
            font-size: 1.5rem;
            color: #ff7f0e;
            margin-top: 2rem;
            margin-bottom: 1rem;
        }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'model_loaded' not in st.session_state:
    st.session_state.model_loaded = False
    st.session_state.model = None
    st.session_state.current_model = None
    st.session_state.analytics_evaluated = False

# Main title
st.markdown('<h1 class="main-header">🎯 YOLO Object Detection</h1>', unsafe_allow_html=True)
st.write("Detect objects in images, videos, or live webcam feeds with YOLOv11.m")

# Sidebar configuration
st.sidebar.markdown("## ⚙️ Configuration")

# Model selection
model_choice = st.sidebar.radio(
    "Select Model:",
    options=["best.pt", "last.pt"],
    help="Choose between the best or last checkpoint model"
)

# Load model
@st.cache_resource
def load_model(model_name):
    """Load YOLO model with caching"""
    try:
        model = YOLO(model_name)
        return model
    except Exception as e:
        st.error(f"Error loading model: {e}")
        return None

if st.sidebar.button("🔄 Load Model", use_container_width=True):
    with st.spinner(f"Loading {model_choice}..."):
        model = load_model(model_choice)
        if model:
            st.session_state.model = model
            st.session_state.model_loaded = True
            st.session_state.current_model = model_choice
            st.sidebar.success(f"✅ {model_choice} loaded successfully!")
        else:
            st.session_state.model_loaded = False

# Display loaded model info
if st.session_state.model_loaded:
    st.sidebar.info(f"📦 Loaded Model: **{st.session_state.current_model}**")
else:
    st.sidebar.warning("⚠️ Please load a model first")

st.sidebar.markdown("---")

# Confidence threshold
confidence = st.sidebar.slider(
    "Confidence Threshold:",
    min_value=0.0,
    max_value=1.0,
    value=0.45,
    step=0.05,
    help="Minimum confidence score for detections"
)

# Main content
mode = st.radio(
    "📌 What would you like to do?",
    options=["📷 Image Detection", "🎬 Video Detection", "📹 Webcam Detection", "📊 Model Analytics"],
    horizontal=True,
    help="Select the type of input for object detection"
)

st.markdown("---")

# IMAGE DETECTION
if mode == "📷 Image Detection":
    st.markdown('<h2 class="section-header">📷 Image Detection</h2>', unsafe_allow_html=True)
    
    if not st.session_state.model_loaded:
        st.error("❌ Please load a model first from the sidebar")
    else:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("### Upload Image")
            uploaded_file = st.file_uploader(
                "Choose an image file",
                type=["jpg", "jpeg", "png", "bmp", "webp"],
                help="Supported formats: JPG, PNG, BMP, WebP"
            )
        
        if uploaded_file is not None:
            # Display original image
            image = Image.open(uploaded_file)
            with col1:
                st.image(image, caption="Original Image", use_column_width=True)
            
            # Run detection
            if st.button("🚀 Run Detection", key="image_detect", use_container_width=True):
                with st.spinner("Running detection..."):
                    # Convert PIL image to numpy array
                    img_array = np.array(image)
                    
                    # Run YOLO inference
                    results = st.session_state.model.predict(
                        source=img_array,
                        conf=confidence,
                        verbose=False
                    )
                    
                    # Get annotated frame
                    annotated_img = results[0].plot()
                    annotated_img_pil = Image.fromarray(annotated_img)
                    
                    with col2:
                        st.image(annotated_img_pil, caption="Detection Results", use_column_width=True)
                    
                    # Display statistics
                    st.markdown("### 📊 Detection Statistics")
                    detections = results[0].boxes
                    st.metric("Objects Detected", len(detections))
                    
                    if len(detections) > 0:
                        # Create a dataframe with detection details
                        detection_data = []
                        for box in detections:
                            detection_data.append({
                                "Class": st.session_state.model.names[int(box.cls)],
                                "Confidence": f"{float(box.conf):.2%}",
                                "X1": f"{int(box.xyxy[0][0])}",
                                "Y1": f"{int(box.xyxy[0][1])}",
                                "X2": f"{int(box.xyxy[0][2])}",
                                "Y2": f"{int(box.xyxy[0][3])}"
                            })
                        
                        st.dataframe(detection_data, use_container_width=True, hide_index=True)
                        
                        # Download annotated image
                        from io import BytesIO
                        buf = BytesIO()
                        annotated_img_pil.save(buf, format="PNG")
                        buf.seek(0)
                        st.download_button(
                            label="⬇️ Download Annotated Image",
                            data=buf.getvalue(),
                            file_name="detection_result.png",
                            mime="image/png",
                            use_container_width=True
                        )
                    else:
                        st.info("ℹ️ No objects detected in this image")

# VIDEO DETECTION
elif mode == "🎬 Video Detection":
    st.markdown('<h2 class="section-header">🎬 Video Detection</h2>', unsafe_allow_html=True)
    
    if not st.session_state.model_loaded:
        st.error("❌ Please load a model first from the sidebar")
    else:
        st.write("### Upload Video")
        uploaded_video = st.file_uploader(
            "Choose a video file",
            type=["mp4", "avi", "mov", "mkv", "flv", "wmv"],
            help="Supported formats: MP4, AVI, MOV, MKV, FLV, WMV"
        )
        
        if uploaded_video is not None:
            st.write(f"**Selected file:** {uploaded_video.name}")
            
            # Save uploaded video temporarily
            temp_video_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
            with open(temp_video_path, "wb") as f:
                f.write(uploaded_video.read())
            
            if st.button("🚀 Run Detection on Video", key="video_detect", use_container_width=True):
                with st.spinner("Processing video... This may take a few moments ⏳"):
                    # Create output path
                    output_path = tempfile.NamedTemporaryFile(suffix=".mp4", delete=False).name
                    
                    # Run YOLO inference on video
                    results = st.session_state.model.predict(
                        source=temp_video_path,
                        conf=confidence,
                        save=True,
                        project=tempfile.gettempdir(),
                        name="detection",
                        verbose=False
                    )
                    
                    # Find the output video
                    temp_dir = tempfile.gettempdir()
                    detection_dir = os.path.join(temp_dir, "detection", "runs", "detect", "predict")
                    
                    # Get video files from results
                    video_files = []
                    for root, dirs, files in os.walk(temp_dir):
                        for file in files:
                            if file.endswith((".mp4", ".avi")):
                                video_files.append(os.path.join(root, file))
                    
                    if video_files:
                        output_video = video_files[0]
                        st.success("✅ Video processing complete!")
                        
                        # Display the video
                        st.video(output_video)
                        
                        # Download button
                        with open(output_video, "rb") as f:
                            st.download_button(
                                label="⬇️ Download Processed Video",
                                data=f.read(),
                                file_name="detection_video.mp4",
                                mime="video/mp4",
                                use_container_width=True
                            )
                    else:
                        st.info("ℹ️ Video processed. Check the output directory.")
            
            # Cleanup
            os.unlink(temp_video_path)

# WEBCAM DETECTION
elif mode == "📹 Webcam Detection":
    st.markdown('<h2 class="section-header">📹 Webcam Detection</h2>', unsafe_allow_html=True)
    
    if not st.session_state.model_loaded:
        st.error("❌ Please load a model first from the sidebar")
    else:
        col1, col2 = st.columns([2, 1])
        
        with col2:
            st.write("### ⚙️ Settings")
            
            # Speed Mode Selection
            speed_mode = st.radio(
                "Speed Mode:",
                options=["🐢 Normal", "⚡ Fast", "🚀 Ultra Fast"],
                index=1,
                help="Higher speed = faster but less accurate"
            )
            
            if speed_mode == "🐢 Normal":
                frame_skip = 1
                st.info("Processing every frame - Most accurate")
            elif speed_mode == "⚡ Fast":
                frame_skip = 5
                st.info("Processing every 5th frame - Good balance")
            else:  # Ultra Fast
                frame_skip = 10
                st.info("Processing every 10th frame - Fastest!")
            
            st.markdown("---")
            
            # Confidence threshold
            conf_webcam = st.slider(
                "Confidence:",
                min_value=0.0,
                max_value=1.0,
                value=confidence,
                step=0.05
            )
        
        with col1:
            # Control buttons in columns
            col_start, col_stop = st.columns(2)
            
            with col_start:
                start_webcam = st.button("🎥 Start Camera", key="webcam_start", use_container_width=True)
            
            with col_stop:
                stop_webcam = st.button("🛑 Stop Camera", key="webcam_stop", use_container_width=True)
        
        # Webcam session state
        if 'webcam_running' not in st.session_state:
            st.session_state.webcam_running = False
        
        if start_webcam:
            st.session_state.webcam_running = True
        
        if stop_webcam:
            st.session_state.webcam_running = False
        
        # Run webcam loop
        if st.session_state.webcam_running:
            cap = cv2.VideoCapture(0)
            
            if not cap.isOpened():
                st.error("❌ Error: Could not open webcam. Make sure your camera is connected and accessible.")
                st.session_state.webcam_running = False
            else:
                # Optimize camera for speed
                cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
                cap.set(cv2.CAP_PROP_FPS, 30)
                
                # Get camera properties
                fps = int(cap.get(cv2.CAP_PROP_FPS))
                width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
                height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
                
                mode_text = f"{speed_mode}"
                st.write(f"📊 {mode_text} | FPS: {fps}, Resolution: {width}x{height}")
                st.warning("⏹️ Click 'Stop Camera' button to stop streaming")
                
                # Create placeholders
                frame_placeholder = st.empty()
                stats_placeholder = st.empty()
                
                frame_count = 0
                detection_count = 0
                processed_count = 0
                
                try:
                    while st.session_state.webcam_running:
                        ret, frame = cap.read()
                        
                        if not ret:
                            st.error("❌ Error reading from webcam")
                            break
                        
                        # Process based on frame skip
                        if frame_count % frame_skip == 0:
                            try:
                                # Run YOLO inference
                                results = st.session_state.model.predict(
                                    source=frame,
                                    conf=conf_webcam,
                                    verbose=False
                                )
                                
                                # Get annotated frame
                                annotated_frame = results[0].plot()
                                detection_count = len(results[0].boxes)
                                processed_count += 1
                            except:
                                annotated_frame = frame
                                detection_count = 0
                        else:
                            annotated_frame = frame
                        
                        # Convert BGR to RGB for display
                        frame_rgb = cv2.cvtColor(annotated_frame, cv2.COLOR_BGR2RGB)
                        
                        # Display frame
                        frame_placeholder.image(frame_rgb, use_column_width=True)
                        
                        # Update stats
                        with stats_placeholder.container():
                            col_a, col_b, col_c, col_d = st.columns(4)
                            with col_a:
                                st.metric("📹 Frames", frame_count)
                            with col_b:
                                st.metric("🎯 Detected", detection_count)
                            with col_c:
                                st.metric("⚙️ Processed", processed_count)
                            with col_d:
                                fps_current = int(frame_count / max(1, (frame_count / 30)))
                                st.metric("⚡ Speed", f"{fps_current} FPS")
                        
                        frame_count += 1
                
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                
                finally:
                    cap.release()
                    st.session_state.webcam_running = False
                    st.success("✅ Camera stopped!")
        else:
            st.info("👉 Click 'Start Camera' button to begin live detection")

# MODEL ANALYTICS DASHBOARD
elif mode == "📊 Model Analytics":
    st.markdown('<h2 class="section-header">📊 Model Performance & Analytics Dashboard</h2>', unsafe_allow_html=True)
    
    st.write("""
    This dashboard evaluates your trained YOLO11 model on your dataset and displays comprehensive performance analysis.
    All metrics are generated by running inference on your dataset images.
    """)
    
    if not st.session_state.model_loaded:
        st.error("❌ Please load a model first from the sidebar")
    else:
        # Initialize analytics
        @st.cache_resource
        def load_analytics():
            analytics = YOLO11Analytics(
                model_obj=st.session_state.model,
                dataset_path=None
            )
            return analytics
        
        analytics = load_analytics()
        
        # Check if dataset exists
        dataset_path = analytics.find_dataset()
        if not dataset_path:
            st.error("❌ Dataset not found. Expected location: dataset/Dataset/")
            st.info("ℹ️ Please ensure your dataset exists in the 'dataset/Dataset/' directory")
        else:
            st.success(f"✅ Dataset found: {dataset_path}")
            
            # Evaluate model
            if st.button("🚀 Evaluate Model on Dataset", use_container_width=True):
                analytics.evaluate_model_on_dataset()
                st.session_state.analytics_evaluated = True
            
            # Display results if evaluation completed
            if st.session_state.get('analytics_evaluated', False):
                metrics = analytics.metrics_data
                
                if metrics:
                    st.markdown("---")
                    
                    # ===== METRICS OVERVIEW =====
                    st.subheader("📈 Evaluation Metrics")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Total Detections",
                            f"{int(metrics.get('total_detections', 0))}"
                        )
                    
                    with col2:
                        st.metric(
                            "Mean Confidence",
                            f"{metrics.get('mean_confidence', 0):.3f}"
                        )
                    
                    with col3:
                        st.metric(
                            "Images Processed",
                            f"{int(metrics.get('total_images', 0))}"
                        )
                    
                    with col4:
                        st.metric(
                            "Avg Detections/Image",
                            f"{metrics.get('detections_per_image', 0):.2f}"
                        )
                    
                    st.markdown("---")
                    
                    # Additional metrics
                    col1, col2, col3, col4 = st.columns(4)
                    
                    with col1:
                        st.metric(
                            "Max Confidence",
                            f"{metrics.get('max_confidence', 0):.3f}"
                        )
                    
                    with col2:
                        st.metric(
                            "Min Confidence",
                            f"{metrics.get('min_confidence', 0):.3f}"
                        )
                    
                    with col3:
                        st.metric(
                            "Classes Detected",
                            f"{int(metrics.get('classes_detected', 0))}"
                        )
                    
                    with col4:
                        st.metric(
                            "Images with Detections",
                            f"{int(metrics.get('images_with_detections', 0))}"
                        )
                    
                    st.markdown("---")
                    
                    # ===== CONFIDENCE ANALYSIS =====
                    st.subheader("🎯 Confidence Analysis")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = analytics.create_confidence_distribution_graph()
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No detections to analyze")
                    
                    with col2:
                        # Confidence statistics
                        st.write("### Confidence Statistics")
                        high_conf = int(metrics.get('high_confidence_detections', 0))
                        med_conf = int(metrics.get('medium_confidence_detections', 0))
                        low_conf = int(metrics.get('low_confidence_detections', 0))
                        
                        st.write(f"**High Confidence (>0.8):** {high_conf} detections")
                        st.write(f"**Medium Confidence (0.5-0.8):** {med_conf} detections")
                        st.write(f"**Low Confidence (<0.5):** {low_conf} detections")
                        
                        # Pie chart
                        conf_data = {
                            'High (>0.8)': high_conf,
                            'Medium (0.5-0.8)': med_conf,
                            'Low (<0.5)': low_conf
                        }
                        fig = go.Figure(data=[go.Pie(
                            labels=list(conf_data.keys()),
                            values=list(conf_data.values()),
                            marker=dict(colors=['#2ca02c', '#ff7f0e', '#d62728'])
                        )])
                        fig.update_layout(height=400, showlegend=True)
                        st.plotly_chart(fig, use_container_width=True)
                    
                    st.markdown("---")
                    
                    # ===== CLASS ANALYSIS =====
                    st.subheader("📊 Class Distribution")
                    
                    col1, col2 = st.columns(2)
                    
                    with col1:
                        fig = analytics.create_class_distribution_graph()
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No class data available")
                    
                    with col2:
                        fig = analytics.create_confidence_by_class_graph()
                        if fig:
                            st.plotly_chart(fig, use_container_width=True)
                        else:
                            st.info("No class data available")
                    
                    st.markdown("---")
                    
                    # ===== DETECTION ANALYSIS =====
                    st.subheader("🔍 Detection Analysis")
                    
                    fig = analytics.create_detections_per_image_graph()
                    if fig:
                        st.plotly_chart(fig, use_container_width=True)
                    else:
                        st.info("No detection data available")
                    
                    st.markdown("---")
                    
                    # ===== DETAILED RESULTS =====
                    if st.checkbox("📋 Show Detailed Detection Results"):
                        if 'detections' in analytics.evaluation_results:
                            detections_df = pd.DataFrame(analytics.evaluation_results['detections'])
                            st.dataframe(detections_df, use_container_width=True)
                            
                            # Download option
                            csv = detections_df.to_csv(index=False)
                            st.download_button(
                                label="⬇️ Download Detection Results as CSV",
                                data=csv,
                                file_name="yolo11_detection_results.csv",
                                mime="text/csv",
                                use_container_width=True
                            )
                else:
                    st.info("👉 Click '🚀 Evaluate Model on Dataset' to start analysis")

# Footer
st.markdown("---")
st.markdown("""
    <div style="text-align: center; color: gray; margin-top: 2rem;">
        <p>🎯 YOLO Object Detection | Powered by YOLOv11 & Streamlit</p>
    </div>
""", unsafe_allow_html=True)
