@echo off
cd /d C:\TripGuard\backend
call venv\Scripts\activate.bat
python manage.py fetch_alerts >> C:\TripGuard\logs\fetch_alerts.log 2>&1
