from django.urls import path
from . import views

urlpatterns = [
    path('detect/', views.detect_disease),
    path('diseases/', views.get_diseases),
    path('model-info/', views.get_model_info),
    path('diseases/<int:disease_id>/', views.get_disease_detail),
]

