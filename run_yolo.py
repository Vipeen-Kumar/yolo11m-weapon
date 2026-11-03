import cv2
import argparse
from pathlib import Path
from ultralytics import YOLO
import os

def load_model(model_path):
    """Load YOLO model from the given path"""
    print(f"Loading model from: {model_path}")
    model = YOLO(model_path)
    return model

def detect_on_image(model, image_path, output_dir="results"):
    """Run detection on a single image"""
    print(f"\n📸 Running detection on image: {image_path}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Run inference
    results = model.predict(source=image_path, save=True, project=output_dir, name="images")
    
    print(f"✅ Image detection complete! Results saved to: {output_dir}")
    return results

def detect_on_video(model, video_path, output_dir="results"):
    """Run detection on a video"""
    print(f"\n🎬 Running detection on video: {video_path}")
    
    # Create output directory
    os.makedirs(output_dir, exist_ok=True)
    
    # Run inference
    results = model.predict(source=video_path, save=True, project=output_dir, name="videos")
    
    print(f"✅ Video detection complete! Results saved to: {output_dir}")
    return results

def detect_on_webcam(model, duration_seconds=30):
    """Run detection on webcam stream"""
    print(f"\n🎥 Starting webcam detection (will run for {duration_seconds} seconds)")
    print("Press 'q' to quit early")
    
    cap = cv2.VideoCapture(0)
    
    if not cap.isOpened():
        print("❌ Error: Could not open webcam. Check if your camera is connected.")
        return
    
    # Get camera properties
    fps = int(cap.get(cv2.CAP_PROP_FPS))
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    
    print(f"Camera settings - FPS: {fps}, Resolution: {width}x{height}")
    
    frame_count = 0
    max_frames = fps * duration_seconds
    
    while frame_count < max_frames:
        ret, frame = cap.read()
        
        if not ret:
            print("❌ Error reading frame from webcam")
            break
        
        # Run YOLO inference on frame
        results = model(frame)
        
        # Visualize results
        annotated_frame = results[0].plot()
        
        # Display frame
        cv2.imshow('YOLO Detection - Webcam', annotated_frame)
        
        # Print detection info
        detections = results[0].boxes
        if len(detections) > 0:
            print(f"Frame {frame_count}: Detected {len(detections)} objects")
        
        frame_count += 1
        
        # Press 'q' to quit
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("⏸️ Stopped by user")
            break
    
    cap.release()
    cv2.destroyAllWindows()
    print(f"✅ Webcam detection complete! Processed {frame_count} frames")

def main():
    parser = argparse.ArgumentParser(description="YOLO Object Detection - Image, Video, or Webcam")
    parser.add_argument('--model', type=str, default='best.pt', help='Path to YOLO model (.pt file)')
    parser.add_argument('--mode', type=str, choices=['image', 'video', 'webcam'], 
                       help='Detection mode: image, video, or webcam')
    parser.add_argument('--source', type=str, help='Path to image or video file')
    parser.add_argument('--output', type=str, default='results', help='Output directory for results')
    parser.add_argument('--duration', type=int, default=30, help='Webcam duration in seconds')
    
    args = parser.parse_args()
    
    # Load model
    if not os.path.exists(args.model):
        print(f"❌ Error: Model file not found: {args.model}")
        print(f"Available models in current directory:")
        for f in os.listdir('.'):
            if f.endswith('.pt'):
                print(f"  - {f}")
        return
    
    model = load_model(args.model)
    
    # Run detection based on mode
    if args.mode == 'image':
        if not args.source:
            print("❌ Error: --source required for image mode")
            return
        if not os.path.exists(args.source):
            print(f"❌ Error: Image file not found: {args.source}")
            return
        detect_on_image(model, args.source, args.output)
        
    elif args.mode == 'video':
        if not args.source:
            print("❌ Error: --source required for video mode")
            return
        if not os.path.exists(args.source):
            print(f"❌ Error: Video file not found: {args.source}")
            return
        detect_on_video(model, args.source, args.output)
        
    elif args.mode == 'webcam':
        detect_on_webcam(model, args.duration)
    
    else:
        print("Please specify a mode: --mode {image, video, webcam}")
        print("\nExamples:")
        print("  python run_yolo.py --mode image --source photo.jpg")
        print("  python run_yolo.py --mode video --source video.mp4")
        print("  python run_yolo.py --mode webcam --duration 60")

if __name__ == "__main__":
    main()
