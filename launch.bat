@echo off
echo Daena AI VP System - Windows Launcher
echo ========================================
echo.

REM Check if Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python not found. Please install Python 3.8+ and try again.
    echo.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

echo ✅ Python found
echo.

REM Check if we're in the right directory
if not exist "backend\main.py" (
    echo ❌ Backend directory not found. Please run from project root.
    echo.
    echo Current directory: %CD%
    echo Expected files: backend\main.py, frontend\templates\
    pause
    exit /b 1
)

if not exist "frontend\templates\" (
    echo ⚠️  Frontend templates not found. Creating minimal setup...
    mkdir "frontend\templates" 2>nul
)

echo ✅ Environment check passed
echo.

REM Kill any existing Python processes that might be using port 8000
echo 🔍 Checking for existing processes...
taskkill /F /IM python.exe >nul 2>&1
timeout /t 2 >nul

echo 🚀 Starting Daena AI VP System...
echo.
echo Features available:
echo   • Main Dashboard
echo   • Expert Council System
echo   • Strategic Room
echo   • Voice Panel
echo   • Department Management
echo   • Real-time Chat
echo.

REM Launch the system in background
echo 🌐 Starting server and opening dashboard...
start /B python launch.py

REM Wait a moment for server to start
echo ⏳ Waiting for server to start...
timeout /t 5 >nul

REM Try to open dashboard automatically
echo 🌐 Opening dashboard in browser...
python open_dashboard.py

if errorlevel 1 (
    echo.
    echo ⚠️  Could not automatically open dashboard
    echo 🌐 Please manually open: http://localhost:8000
    echo.
)

echo.
echo 🎉 Daena AI VP System is ready!
echo.
echo Quick Access:
echo   • Main Dashboard: http://localhost:8000
echo   • Council Dashboard: http://localhost:8000/council-dashboard
echo   • Strategic Room: http://localhost:8000/strategic-room
echo   • Voice Panel: http://localhost:8000/voice-panel
echo   • API Docs: http://localhost:8000/docs
echo.
echo Press any key to exit...
pause >nul 