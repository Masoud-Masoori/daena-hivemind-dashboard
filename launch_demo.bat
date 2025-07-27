@echo off
chcp 65001 >nul
echo.
echo 🎯 Daena AI VP Demo Launcher
echo ================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python is not installed or not in PATH
    echo Please install Python 3.8+ and try again
    pause
    exit /b 1
)

REM Check if virtual environment exists
if exist "venv_daena_main_py310\Scripts\activate.bat" (
    echo ✅ Found virtual environment
    call venv_daena_main_py310\Scripts\activate.bat
) else (
    echo ⚠️  Virtual environment not found, using system Python
)

echo 🔍 Checking dependencies...
python -c "import fastapi, uvicorn, openai, requests, PyJWT" >nul 2>&1
if errorlevel 1 (
    echo 🔧 Installing required packages...
    pip install fastapi uvicorn openai requests PyJWT python-multipart jinja2
    if errorlevel 1 (
        echo ❌ Failed to install dependencies
        pause
        exit /b 1
    )
)

echo 🔧 Setting up environment variables...
set GMAIL_USER=masoud.masoori@gmail.com
set GMAIL_APP_PASSWORD=demo_password_for_testing
set OPENAI_API_TYPE=azure
set OPENAI_API_KEY=1HmnkpDuMqMzKDtYbpcckyVQC6qlggup3zAVmfkG65BjxAtT9JKtJQQJ99BGACHYHv6XJ3w3AAAAACOGX3DN
set OPENAI_API_BASE=https://masou-mdksrl1q-eastus2.openai.azure.com/
set OPENAI_API_VERSION=2024-02-15
set OPENAI_DEPLOYMENT_NAME=daena
set DEMO_PORT=3000
set DEMO_MODE=production

echo ✅ Environment variables configured

echo 🔍 Finding available port...
set PORT=3000
:port_check
netstat -an | find ":%PORT%" >nul
if not errorlevel 1 (
    echo ⚠️  Port %PORT% is in use, trying next port...
    set /a PORT+=1
    if %PORT% gtr 3010 (
        echo ❌ No available ports found
        pause
        exit /b 1
    )
    goto port_check
)

echo ✅ Using port %PORT%

echo 🚀 Starting Daena AI VP Demo Server...
echo ================================
echo 🌐 Using port %PORT%
echo.

REM Change to backend directory
cd backend

REM Start the server
echo Starting server with command: python -m uvicorn main:app --host 0.0.0.0 --port %PORT% --reload
python -m uvicorn main:app --host 0.0.0.0 --port %PORT% --reload

if errorlevel 1 (
    echo ❌ Server failed to start
    echo.
    echo 🔧 Troubleshooting:
    echo    1. Check if port %PORT% is available
    echo    2. Ensure all dependencies are installed
    echo    3. Check the logs for errors
    echo    4. Try running: pip install -r requirements.txt
    echo.
    pause
    exit /b 1
)

echo ✅ Server stopped successfully
pause 