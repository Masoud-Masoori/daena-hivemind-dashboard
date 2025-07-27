#!/bin/bash
# Daena AI VP System - Unix/Linux Launcher
# ========================================

echo "Daena AI VP System - Unix/Linux Launcher"
echo "========================================"
echo

# Check if Python is available
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 not found. Please install Python 3.8+ and try again."
    echo
    echo "Installation commands:"
    echo "  Ubuntu/Debian: sudo apt-get install python3 python3-pip"
    echo "  CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "  macOS: brew install python3"
    exit 1
fi

echo "✅ Python3 found"
echo

# Check if we're in the right directory
if [ ! -f "backend/main.py" ]; then
    echo "❌ Backend directory not found. Please run from project root."
    echo
    echo "Current directory: $(pwd)"
    echo "Expected files: backend/main.py, frontend/templates/"
    exit 1
fi

if [ ! -d "frontend/templates" ]; then
    echo "⚠️  Frontend templates not found. Creating minimal setup..."
    mkdir -p frontend/templates
fi

echo "✅ Environment check passed"
echo

# Kill any existing Python processes that might be using port 8000
echo "🔍 Checking for existing processes..."
pkill -f "uvicorn" 2>/dev/null || true
sleep 2

echo "🚀 Starting Daena AI VP System..."
echo
echo "Features available:"
echo "  • Main Dashboard"
echo "  • Expert Council System"
echo "  • Strategic Room"
echo "  • Voice Panel"
echo "  • Department Management"
echo "  • Real-time Chat"
echo

# Launch the system
python3 launch.py

if [ $? -ne 0 ]; then
    echo
    echo "❌ Failed to start Daena AI VP System"
    echo
    echo "Troubleshooting:"
    echo "1. Check if port 8000 is available"
    echo "2. Ensure all dependencies are installed: pip3 install -r requirements.txt"
    echo "3. Check the logs in daena.log"
    echo
    exit 1
fi

echo
echo "🌐 Opening dashboard..."
python3 open_dashboard.py

echo
echo "🎉 Daena AI VP System is ready!"
echo
echo "Quick Access:"
echo "  • Main Dashboard: http://localhost:8000"
echo "  • Council Dashboard: http://localhost:8000/council-dashboard"
echo "  • Strategic Room: http://localhost:8000/strategic-room"
echo "  • Voice Panel: http://localhost:8000/voice-panel"
echo "  • API Docs: http://localhost:8000/docs"
echo 