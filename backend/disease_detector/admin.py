from django.contrib import admin
from .models import PlantDisease, Treatment, PreventionTip, Diagnosis, DiagnosisHistory


@admin.register(PlantDisease)
class PlantDiseaseAdmin(admin.ModelAdmin):
    list_display = ('name', 'description')


@admin.register(Treatment)
class TreatmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'disease', 'method')


@admin.register(PreventionTip)
class PreventionTipAdmin(admin.ModelAdmin):
    list_display = ('disease', 'tip')


@admin.register(Diagnosis)
class DiagnosisAdmin(admin.ModelAdmin):
    list_display = ('result', 'confidence', 'created_at')


@admin.register(DiagnosisHistory)
class DiagnosisHistoryAdmin(admin.ModelAdmin):
    list_display = ('diagnosis', 'date', 'notes')

