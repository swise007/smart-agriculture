from django.db import models


class PlantDisease(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class Treatment(models.Model):
    disease = models.ForeignKey(PlantDisease, on_delete=models.CASCADE, related_name='treatments')
    name = models.CharField(max_length=100)
    description = models.TextField()
    method = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.disease.name})"


class PreventionTip(models.Model):
    disease = models.ForeignKey(PlantDisease, on_delete=models.CASCADE, related_name='prevention_tips')
    tip = models.TextField()

    def __str__(self):
        return f"Prevention for {self.disease.name}"


class Diagnosis(models.Model):
    image = models.ImageField(upload_to='diagnoses/')
    result = models.CharField(max_length=200)
    confidence = models.FloatField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.result} ({self.confidence*100:.1f}% confidence)"


class DiagnosisHistory(models.Model):
    diagnosis = models.ForeignKey(Diagnosis, on_delete=models.CASCADE, related_name='history')
    date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"History for {self.diagnosis.result} on {self.date.strftime('%Y-%m-%d')}"
