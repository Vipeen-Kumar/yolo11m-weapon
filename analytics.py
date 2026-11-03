import os
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from pathlib import Path
import streamlit as st
import warnings

warnings.filterwarnings("ignore")


class YOLO11Analytics:
    def __init__(self, model_obj=None, dataset_path=None):
        self.model = model_obj
        self.dataset_path = dataset_path
        self.metrics_data = {}
        self.evaluation_results = {}
        self.metrics_available = {}
        self.dataset_images = []

    def find_dataset(self):
        possible_paths = [
            Path.cwd() / "dataset" / "Dataset",
            Path.cwd() / "dataset",
            Path.cwd() / "data",
        ]
        for path in possible_paths:
            if path.exists() and (path / "images").exists():
                self.dataset_path = path
                return path
        return None

    def load_dataset_images(self):
        if not self.dataset_path:
            self.dataset_path = self.find_dataset()
        if not self.dataset_path:
            return []
        images_dir = self.dataset_path / "images"
        test_images_dir = self.dataset_path / "images_test"
        images = []
        if images_dir.exists():
            images.extend(list(images_dir.glob("*.jpg")))
            images.extend(list(images_dir.glob("*.png")))
        if test_images_dir.exists():
            images.extend(list(test_images_dir.glob("*.jpg")))
            images.extend(list(test_images_dir.glob("*.png")))
        self.dataset_images = images
        self.metrics_available['dataset_images'] = len(images) > 0
        return images

    def evaluate_model_on_dataset(self):
        if not self.model:
            st.error("Model not loaded")
            return False
        images = self.load_dataset_images()
        if not images:
            st.warning("No images found in dataset")
            return False
        st.info(f"Evaluating model on {len(images)} images...")
        detections_list = []
        confidence_scores = []
        class_predictions = []
        progress_bar = st.progress(0)
        for idx, img_path in enumerate(images):
            try:
                results = self.model.predict(source=str(img_path), conf=0.25, verbose=False)
                if results and len(results) > 0:
                    result = results[0]
                    boxes = result.boxes
                    if boxes is not None:
                        for box in boxes:
                            conf_val = float(box.conf[0]) if box.conf is not None else 0
                            cls_val = int(box.cls[0]) if box.cls is not None else 0
                            detections_list.append({
                                'image': img_path.name,
                                'class': cls_val,
                                'confidence': conf_val,
                                'x1': float(box.xyxy[0][0]),
                                'y1': float(box.xyxy[0][1]),
                                'x2': float(box.xyxy[0][2]),
                                'y2': float(box.xyxy[0][3]),
                            })
                            confidence_scores.append(conf_val)
                            class_predictions.append(cls_val)
            except:
                pass
            progress_bar.progress((idx + 1) / len(images))
        self._calculate_performance_metrics(detections_list, confidence_scores, class_predictions, len(images))
        self.metrics_available['model_evaluated'] = True
        return True

    def _calculate_performance_metrics(self, detections, confidences, classes, total_images):
        metrics = {}
        if detections:
            detections_df = pd.DataFrame(detections)
            metrics['mean_confidence'] = float(np.mean(confidences)) if confidences else 0
            metrics['max_confidence'] = float(np.max(confidences)) if confidences else 0
            metrics['min_confidence'] = float(np.min(confidences)) if confidences else 0
            metrics['std_confidence'] = float(np.std(confidences)) if len(confidences) > 1 else 0
            metrics['total_detections'] = len(detections)
            metrics['detections_per_image'] = len(detections) / total_images if total_images > 0 else 0
            if classes:
                class_counts = pd.Series(classes).value_counts()
                metrics['classes_detected'] = len(class_counts)
                metrics['most_common_class'] = int(class_counts.idxmax())
            else:
                metrics['classes_detected'] = 0
            high_conf = len([c for c in confidences if c > 0.8])
            medium_conf = len([c for c in confidences if 0.5 <= c <= 0.8])
            low_conf = len([c for c in confidences if c < 0.5])
            metrics['high_confidence_detections'] = high_conf
            metrics['medium_confidence_detections'] = medium_conf
            metrics['low_confidence_detections'] = low_conf
        else:
            metrics['mean_confidence'] = 0
            metrics['max_confidence'] = 0
            metrics['min_confidence'] = 0
            metrics['std_confidence'] = 0
            metrics['total_detections'] = 0
            metrics['detections_per_image'] = 0
            metrics['classes_detected'] = 0
            metrics['high_confidence_detections'] = 0
            metrics['medium_confidence_detections'] = 0
            metrics['low_confidence_detections'] = 0
        metrics['total_images'] = total_images
        metrics['images_with_detections'] = len(set([d['image'] for d in detections])) if detections else 0
        self.metrics_data = metrics
        self.evaluation_results['detections'] = detections
        self.metrics_available['metrics_calculated'] = True

    def create_confidence_distribution_graph(self):
        if 'detections' not in self.evaluation_results:
            return None
        detections = self.evaluation_results['detections']
        if not detections:
            return None
        df = pd.DataFrame(detections)
        confidences = df['confidence'].values
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=confidences,
            nbinsx=20,
            name='Confidence Distribution',
            marker_color='#1f77b4',
            hovertemplate='<b>Confidence</b>: %{x}<br><b>Count</b>: %{y}<extra></extra>'
        ))
        fig.update_layout(
            title="Detection Confidence Distribution",
            xaxis_title="Confidence Score",
            yaxis_title="Number of Detections",
            hovermode='x',
            template='plotly_white',
            height=450,
            showlegend=False
        )
        return fig

    def create_class_distribution_graph(self):
        if 'detections' not in self.evaluation_results:
            return None
        detections = self.evaluation_results['detections']
        if not detections:
            return None
        df = pd.DataFrame(detections)
        class_counts = df['class'].value_counts().sort_index()
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[f"Class {i}" for i in class_counts.index],
            y=class_counts.values,
            marker_color='#2ca02c',
            text=class_counts.values,
            textposition='outside',
            hovertemplate='<b>%{x}</b><br><b>Count</b>: %{y}<extra></extra>'
        ))
        fig.update_layout(
            title="Class Distribution in Detections",
            xaxis_title="Class",
            yaxis_title="Number of Detections",
            template='plotly_white',
            height=450,
            showlegend=False
        )
        return fig

    def create_confidence_by_class_graph(self):
        if 'detections' not in self.evaluation_results:
            return None
        detections = self.evaluation_results['detections']
        if not detections:
            return None
        df = pd.DataFrame(detections)
        avg_conf = df.groupby('class')['confidence'].agg(['mean', 'std', 'count'])
        fig = go.Figure()
        fig.add_trace(go.Bar(
            x=[f"Class {i}" for i in avg_conf.index],
            y=avg_conf['mean'],
            error_y=dict(type='data', array=avg_conf['std']),
            marker_color='#ff7f0e',
            text=[f"{v:.3f}" for v in avg_conf['mean']],
            textposition='outside',
            hovertemplate='<b>%{x}</b><br><b>Avg</b>: %{y:.3f}<extra></extra>'
        ))
        fig.update_layout(
            title="Average Detection Confidence by Class",
            xaxis_title="Class",
            yaxis_title="Average Confidence",
            template='plotly_white',
            height=450,
            showlegend=False
        )
        return fig

    def create_detections_per_image_graph(self):
        if 'detections' not in self.evaluation_results:
            return None
        detections = self.evaluation_results['detections']
        if not detections:
            return None
        df = pd.DataFrame(detections)
        detections_per_image = df.groupby('image').size()
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=detections_per_image.values,
            nbinsx=15,
            name='Detections Per Image',
            marker_color='#d62728',
            hovertemplate='<b>Count</b>: %{x}<br><b>Images</b>: %{y}<extra></extra>'
        ))
        fig.update_layout(
            title="Distribution of Detections Per Image",
            xaxis_title="Number of Detections",
            yaxis_title="Number of Images",
            template='plotly_white',
            height=450,
            showlegend=False
        )
        return fig
