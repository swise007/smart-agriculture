from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
import os
import tempfile
from .models import DiagnosisHistory, PlantDisease
from ml_model.custom_predictor import predictor  # Use your custom model


# ==========================================
# 1. AI DISEASE DETECTION (MAIN FUNCTION)
# ==========================================
@api_view(['POST'])
@permission_classes([AllowAny])
def detect_disease(request):
    """AI-powered disease detection using your custom PyTorch model"""
    if 'image' not in request.FILES:
        return Response(
            {'error': 'No image file provided'}, 
            status=status.HTTP_400_BAD_REQUEST
        )
    
    image_file = request.FILES['image']
    
    try:
        # Save uploaded image to temporary file
        with tempfile.NamedTemporaryFile(delete=False, suffix='.jpg') as tmp_file:
            for chunk in image_file.chunks():
                tmp_file.write(chunk)
            temp_path = tmp_file.name
        
        # Use your custom model to predict disease
        disease_name, confidence = predictor.predict_disease(temp_path)
        
        # Get detailed disease information
        disease_info = predictor.get_disease_info(disease_name)
        
        # Clean up temporary file
        try:
            os.unlink(temp_path)
        except:
            pass
        
        # Prepare comprehensive response
        response_data = {
            'disease_detected': disease_name,
            'scientific_name': disease_info['scientific_name'],
            'confidence': confidence,
            'is_healthy': disease_info['is_healthy'],
            'plant_type': disease_info['plant_type'],
            'symptoms': disease_info['symptoms'],
            'causes': disease_info['causes'],
            'treatment_advice': disease_info['treatment_advice'],
            'prevention_tips': disease_info['prevention_tips'],
            'model_type': 'Custom PyTorch Model',
            'message': 'AI analysis complete using your trained model'
        }
        
        # Save to diagnosis history if user is authenticated
        if request.user.is_authenticated:
            disease_obj, created = PlantDisease.objects.get_or_create(
                name=disease_name,
                defaults={
                    'scientific_name': disease_info['scientific_name'],
                    'description': f'{disease_info["symptoms"]}. Causes: {disease_info["causes"]}',
                    'symptoms': disease_info['symptoms'],
                    'causes': disease_info['causes']
                }
            )
            
            DiagnosisHistory.objects.create(
                user=request.user,
                image=image_file,
                plant_type=disease_info['plant_type'],
                disease_detected=disease_obj,
                confidence=confidence,
                is_healthy=disease_info['is_healthy']
            )
        
        return Response(response_data, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response(
            {'error': f'Error processing image: {str(e)}'},
            status=status.HTTP_500_INTERNAL_SERVER_ERROR
        )


# ==========================================
# 2. GET LIST OF DISEASES
# ==========================================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_diseases(request):
    """Return list of diseases stored in the database"""
    diseases = PlantDisease.objects.all().values(
        'id', 'name', 'scientific_name', 'symptoms', 'causes'
    )
    return Response(list(diseases))


# ==========================================
# 3. GET DISEASE DETAILS
# ==========================================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_disease_detail(request, disease_id):
    """Return full disease details"""
    try:
        disease = PlantDisease.objects.get(id=disease_id)
        data = {
            'id': disease.id,
            'name': disease.name,
            'scientific_name': disease.scientific_name,
            'description': disease.description,
            'symptoms': disease.symptoms,
            'causes': disease.causes,
        }
        return Response(data)
    except PlantDisease.DoesNotExist:
        return Response(
            {'error': 'Disease not found'},
            status=status.HTTP_404_NOT_FOUND
        )


# ==========================================
# 4. MODEL INFO
# ==========================================
@api_view(['GET'])
@permission_classes([AllowAny])
def get_model_info(request):
    """Return information about the AI model"""
    model_info = {
        "model_name": "Custom Plant Disease Model",
        "framework": "PyTorch",
        "input_type": "Leaf Image",
        "version": "1.0",
        "status": "Model Loaded Successfully" if predictor.model_loaded else "Using Mock Model"
    }
    return Response(model_info)

