from rest_framework import serializers
from .models import PlantDisease, Treatment, PreventionTip, BestPractice, DiagnosisHistory

class TreatmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Treatment
        fields = '__all__'

class PreventionTipSerializer(serializers.ModelSerializer):
    class Meta:
        model = PreventionTip
        fields = '__all__'

class PlantDiseaseSerializer(serializers.ModelSerializer):
    treatments = TreatmentSerializer(many=True, read_only=True)
    prevention_tips = PreventionTipSerializer(many=True, read_only=True)
    
    class Meta:
        model = PlantDisease
        fields = '__all__'

class BestPracticeSerializer(serializers.ModelSerializer):
    class Meta:
        model = BestPractice
        fields = '__all__'

class DiagnosisHistorySerializer(serializers.ModelSerializer):
    disease_name = serializers.CharField(source='disease_detected.name', read_only=True)
    
    class Meta:
        model = DiagnosisHistory
        fields = '__all__'
        read_only_fields = ('user', 'created_at')

class ImageUploadSerializer(serializers.Serializer):
    image = serializers.ImageField()
    plant_type = serializers.CharField(max_length=100, required=False)