import torch
from transformers import ViTFeatureExtractor, ViTForImageClassification
from PIL import Image
import os
import logging

logger = logging.getLogger(__name__)

MODEL_NAME = "wambugu71/crop_leaf_diseases_vit"

class HuggingFacePlantPredictor:
    def __init__(self):
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

        logger.info("Loading Hugging Face model...")
        self.feature_extractor = ViTFeatureExtractor.from_pretrained(MODEL_NAME)
        self.model = ViTForImageClassification.from_pretrained(MODEL_NAME)
        self.model.to(self.device)
        self.model.eval()

        self.id2label = self.model.config.id2label
        logger.info("Model loaded successfully.")

    def predict_disease(self, image_path):
        """Predict disease from image path"""
        try:
            image = Image.open(image_path).convert("RGB")

            inputs = self.feature_extractor(images=image, return_tensors="pt")
            inputs = {k: v.to(self.device) for k, v in inputs.items()}

            with torch.no_grad():
                outputs = self.model(**inputs)
                logits = outputs.logits
                probs = torch.softmax(logits, dim=1)

                pred_idx = torch.argmax(probs, dim=1).item()
                confidence = probs[0][pred_idx].item()

            disease_name = self.id2label.get(pred_idx, "Unknown")

            logger.info(f"Prediction: {disease_name}, confidence: {confidence:.4f}")
            return disease_name, round(confidence, 4)

        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return "Error", 0.0

    def get_disease_info(self, disease_name):
        """Return basic disease info based on label"""
        name = disease_name.lower()

        database = {
            "corn common rust": {
                "scientific_name": "Puccinia sorghi",
                "plant_type": "Corn",
                "symptoms": "Small reddish-brown pustules on leaves.",
                "causes": "Fungal infection in warm, humid conditions.",
                "treatment_advice": [
                    "Apply appropriate fungicides",
                    "Remove infected leaves",
                    "Use resistant varieties"
                ],
                "prevention_tips": [
                    "Rotate crops",
                    "Avoid overhead irrigation",
                    "Plant resistant hybrids"
                ],
                "is_healthy": False
            },
            "corn healthy": {
                "scientific_name": "Healthy plant",
                "plant_type": "Corn",
                "symptoms": "Green healthy leaves with no spots.",
                "causes": "Good growing conditions.",
                "treatment_advice": ["No treatment needed."],
                "prevention_tips": ["Maintain good agronomic practices."],
                "is_healthy": True
            },
            "potato early blight": {
                "scientific_name": "Alternaria solani",
                "plant_type": "Potato",
                "symptoms": "Brown spots with concentric rings on leaves.",
                "causes": "Fungal pathogen.",
                "treatment_advice": [
                    "Apply fungicides",
                    "Remove infected leaves"
                ],
                "prevention_tips": [
                    "Crop rotation",
                    "Avoid wet foliage"
                ],
                "is_healthy": False
            },
            "potato healthy": {
                "scientific_name": "Healthy plant",
                "plant_type": "Potato",
                "symptoms": "Normal green leaves.",
                "causes": "Good plant health.",
                "treatment_advice": ["No action needed."],
                "prevention_tips": ["Continue good practices."],
                "is_healthy": True
            },
            "tomato early blight": {
                "scientific_name": "Alternaria solani",
                "plant_type": "Tomato",
                "symptoms": "Dark brown spots with rings.",
                "causes": "Fungal disease.",
                "treatment_advice": [
                    "Apply copper-based fungicides",
                    "Remove infected parts"
                ],
                "prevention_tips": [
                    "Crop rotation",
                    "Proper spacing"
                ],
                "is_healthy": False
            },
            "tomato healthy": {
                "scientific_name": "Healthy plant",
                "plant_type": "Tomato",
                "symptoms": "Green healthy leaves.",
                "causes": "Good care.",
                "treatment_advice": ["No treatment needed."],
                "prevention_tips": ["Maintain good care."],
                "is_healthy": True
            }
        }

        for key, info in database.items():
            if key in name:
                return info

        # Default fallback
        return {
            "scientific_name": "Unknown",
            "plant_type": "Unknown",
            "symptoms": "Symptoms not available.",
            "causes": "Cause unknown.",
            "treatment_advice": ["Consult agricultural expert."],
            "prevention_tips": ["Monitor plant health regularly."],
            "is_healthy": "healthy" in name
        }


# Global instance used by Django views
predictor = HuggingFacePlantPredictor()
