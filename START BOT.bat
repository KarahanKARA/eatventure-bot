@echo off
echo Checking requirements...
pip install -r requirements.txt >nul 2>&1

echo.
echo Running program...
python main.py

pause
