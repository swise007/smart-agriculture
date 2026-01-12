@echo off
echo Setting up Smart Agriculture Project...

:: Create directory structure
mkdir backend\disease_detector\migrations
mkdir backend\ml_model\trained_models
mkdir backend\media\diagnosis_images
mkdir backend\media\temp

:: Create __init__.py files
echo. > backend\disease_detector\migrations\__init__.py
echo. > backend\disease_detector\__init__.py
echo. > backend\plant_disease\__init__.py
echo. > backend\ml_model\__init__.py

echo Project structure created!
echo Now run the installation commands...
pause