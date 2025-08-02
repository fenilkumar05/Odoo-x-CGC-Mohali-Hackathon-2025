@echo off
echo.
echo ========================================
echo   QuickDesk Help Desk System
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo Virtual environment not found. Running setup...
    python setup.py
    if errorlevel 1 (
        echo Setup failed. Please check the error messages above.
        pause
        exit /b 1
    )
)

echo Starting QuickDesk...
echo.
echo Open your browser and go to: http://localhost:5000
echo Default admin login: admin@quickdesk.com / admin123
echo.
echo Press Ctrl+C to stop the server
echo ========================================

REM Start the application
venv\Scripts\python.exe app.py

pause
