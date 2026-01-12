import tensorflow as tf
import numpy as np
import cv2
import os
import requests
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class PlantDiseasePredictor:
    def __init__(self):
        self.model = None
        self.class_names = [
            'Apple_Apple_scab', 'Apple_Black_rot', 'Apple_Cedar_apple_rust', 'Apple_healthy',
            'Blueberry_healthy', 'Cherry_healthy', 'Cherry_Powdery_mildew',
            'Corn_Cercospora_leaf_spot Gray_leaf_spot', 'Corn_Common_rust', 'Corn_healthy', 'Corn_Northern_Leaf_Blight',
            'Grape_Black_rot', 'Grape_Esca_(Black_Measles)', 'Grape_healthy', 'Grape_Leaf_blight_(Isariopsis_Leaf_Spot)',
            'Orange_Haunglongbing_(Citrus_greening)', 'Peach_Bacterial_spot', 'Peach_healthy',
            'Pepper_bell_Bacterial_spot', 'Pepper_bell_healthy',
            'Potato_Early_blight', 'Potato_healthy', 'Potato_Late_blight',
            'Raspberry_healthy', 'Soybean_healthy',
            'Squash_Powdery_mildew', 'Strawberry_healthy', 'Strawberry_Leaf_scorch',
            'Tomato_Bacterial_spot', 'Tomato_Early_blight', 'Tomato_healthy', 'Tomato_Late_blight',
            'Tomato_Leaf_Mold', 'Tomato_Septoria_leaf_spot', 'Tomato_Spider_mites Two-spotted_spider_mite',
            'Tomato_Target_Spot', 'Tomato_Tomato_mosaic_virus', 'Tomato_Tomato_YellowLeaf_Curl_Virus'
        ]
        self.load_model()
    
    def load_model(self):
        """Load the pre-trained model"""
        try:
            # For now, we'll use a mock model. In production, you'd load a real model.
            # You can download a pre-trained plant disease model from:
            # https://www.kaggle.com/datasets/emmarex/plantdisease
            self.model = self.create_mock_model()
            logger.info("AI Model loaded successfully (mock implementation)")
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            self.model = self.create_mock_model()
    
    def create_mock_model(self):
        """Create a mock model for testing"""
        # This is a placeholder. In production, replace with actual model loading.
        class MockModel:
            def predict(self, x):
                # Mock predictions - in real implementation, this would be actual model predictions
                batch_size = x.shape[0]
                # Generate random probabilities that sum to 1
                predictions = np.random.rand(batch_size, len(self.class_names))
                predictions = predictions / predictions.sum(axis=1, keepdims=True)
                return predictions
        return MockModel()
    
    def preprocess_image(self, image_path, target_size=(256, 256)):
        """Preprocess image for model prediction"""
        try:
            # Read image
            image = cv2.imread(image_path)
            if image is None:
                raise ValueError("Could not read image")
            
            # Convert BGR to RGB
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            
            # Resize image
            image = cv2.resize(image, target_size)
            
            # Normalize pixel values
            image = image / 255.0
            
            # Add batch dimension
            image = np.expand_dims(image, axis=0)
            
            return image
        except Exception as e:
            logger.error(f"Error preprocessing image: {e}")
            return None
    
    def predict_disease(self, image_path):
        """Predict disease from image"""
        try:
            if self.model is None:
                return "Model not loaded", 0.0
            
            # Preprocess image
            processed_image = self.preprocess_image(image_path)
            if processed_image is None:
                return "Error processing image", 0.0
            
            # Make prediction
            predictions = self.model.predict(processed_image)
            predicted_class_idx = np.argmax(predictions[0])
            confidence = float(predictions[0][predicted_class_idx])
            
            # Get class name
            predicted_class = self.class_names[predicted_class_idx]
            
            return predicted_class, confidence
            
        except Exception as e:
            logger.error(f"Error during prediction: {e}")
            return "Prediction error", 0.0
    
    def get_disease_info(self, disease_name):
        """Get information about the detected disease"""
        disease_info = {
            'name': disease_name,
            'is_healthy': 'healthy' in disease_name.lower(),
            'plant_type': self.extract_plant_type(disease_name),
            'treatment': self.get_treatment_advice(disease_name),
            'prevention': self.get_prevention_tips(disease_name)
        }
        return disease_info
    
    def extract_plant_type(self, disease_name):
        """Extract plant type from disease name"""
        if '_' in disease_name:
            return disease_name.split('_')[0]
        return "Unknown"
    
    def get_treatment_advice(self, disease_name):
        """Get treatment advice based on disease"""
        treatments = {
            'Early_blight': [
                "Apply copper-based fungicides every 7-10 days",
                "Remove and destroy infected plant parts",
                "Use chlorothalonil or mancozeb fungicides"
            ],
            'Late_blight': [
                "Apply fungicides containing chlorothalonil or metalaxyl",
                "Remove infected plants immediately",
                "Avoid overhead watering"
            ],
            'Powdery_mildew': [
                "Apply sulfur-based fungicides",
                "Use neem oil as organic treatment",
                "Improve air circulation around plants"
            ],
            'Bacterial_spot': [
                "Apply copper-based bactericides",
                "Use streptomycin sprays",
                "Remove and destroy infected plants"
            ]
        }
        
        for key, treatment in treatments.items():
            if key.lower() in disease_name.lower():
                return treatment
        
        return [
            "Consult with local agricultural extension",
            "Use appropriate fungicides/bactericides",
            "Remove infected plant material"
        ]
    
    def get_prevention_tips(self, disease_name):
        """Get prevention tips based on disease"""
        return [
            "Practice crop rotation",
            "Ensure proper plant spacing for air circulation",
            "Water at the base of plants, avoid overhead irrigation",
            "Use disease-resistant varieties when possible",
            "Monitor plants regularly for early signs of disease"
        ]

# Global predictor instance
predictor = PlantDiseasePredictor()