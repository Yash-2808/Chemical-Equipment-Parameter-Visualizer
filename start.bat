@echo off
echo Starting Chemical Equipment Parameter Visualizer
echo.

echo Starting Django Backend Server...
cd backend
start "Django Backend" cmd /k "python manage.py runserver"

echo Waiting for Django server to start...
timeout /t 5 /nobreak >nul

echo Starting React Web Frontend...
cd ..\web-frontend
start "React Frontend" cmd /k "set PORT=3001 && npm start"

echo.
echo Application is starting up...
echo.
echo Backend API: http://localhost:8000/api/
echo Web Frontend: http://localhost:3001
echo.
echo Press any key to start Desktop Application...
pause >nul

echo Starting PyQt5 Desktop Application...
cd ..\desktop-frontend
python main.py

pause
