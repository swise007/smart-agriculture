@echo off
echo Setting up Python environment...

:: Create virtual environment
python -m venv plant_env

:: Activate environment
call plant_env\Scripts\activate

:: Upgrade pip
python -m pip install --upgrade pip

:: Install requirements
pip install -r requirements.txt

echo Environment setup complete!
echo.
echo Next steps:
echo 1. cd backend
echo 2. python manage.py makemigrations
echo 3. python manage.py migrate
echo 4. python manage.py createsuperuser
echo 5. python manage.py runserver
pause