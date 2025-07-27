#!/usr/bin/env python3
"""
Daena AI VP System - Launch Script
==================================
This script launches the Daena AI VP system with proper configuration
and error handling for production deployment.
"""

import os
import sys
import uvicorn
import logging
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(sys.stdout)
    ]
)

# Try to add file handler, but don't fail if permission denied
try:
    file_handler = logging.FileHandler('daena.log', encoding='utf-8')
    file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))
    logging.getLogger().addHandler(file_handler)
except PermissionError:
    print("Warning: Could not create log file due to permissions. Logging to console only.")
except Exception as e:
    print(f"Warning: Could not create log file: {e}. Logging to console only.")

logger = logging.getLogger(__name__)

def check_environment():
    """Check if the environment is properly configured"""
    logger.info("Checking environment configuration...")
    
    # Check if we're in the right directory
    if not Path("backend").exists():
        logger.error("Backend directory not found. Please run from project root.")
        return False
    
    if not Path("frontend").exists():
        logger.warning("Frontend directory not found. Creating minimal setup...")
        Path("frontend/static").mkdir(parents=True, exist_ok=True)
        Path("frontend/templates").mkdir(parents=True, exist_ok=True)
    
    # Check for required files
    required_files = [
        "backend/main.py",
        "config/settings.py",
        "backend/services/auth_service.py"
    ]
    
    for file_path in required_files:
        if not Path(file_path).exists():
            logger.error(f"Required file not found: {file_path}")
            return False
    
    # Check for new feature files
    new_features = [
        "backend/routes/strategic_room.py",
        "backend/routes/voice_panel.py",
        "backend/services/gpu_service.py",
        "frontend/templates/strategic_room.html",
        "frontend/templates/voice_panel.html"
    ]
    
    for feature_file in new_features:
        if Path(feature_file).exists():
            logger.info(f"✅ Feature available: {feature_file}")
        else:
            logger.warning(f"⚠️  Feature not found: {feature_file}")
    
    logger.info("Environment check passed")
    return True

def check_dependencies():
    """Check if all required dependencies are available"""
    logger.info("Checking dependencies...")
    
    try:
        import fastapi
        import uvicorn
        import pydantic
        import jinja2
        logger.info("✅ Core dependencies available")
    except ImportError as e:
        logger.error(f"❌ Missing dependency: {e}")
        return False
    
    # Check for optional dependencies
    optional_deps = {
        "openai": "OpenAI API integration",
        "anthropic": "Claude API integration", 
        "google.generativeai": "Gemini API integration",
        "torch": "PyTorch for GPU acceleration",
        "tensorflow": "TensorFlow for GPU acceleration"
    }
    
    for dep, description in optional_deps.items():
        try:
            __import__(dep)
            logger.info(f"✅ {description} available")
        except ImportError:
            logger.warning(f"⚠️  {description} not available (optional)")
    
    return True

def check_port_available(port):
    """Check if a port is available"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=8000, max_attempts=10):
    """Find an available port starting from start_port"""
    for i in range(max_attempts):
        port = start_port + i
        if check_port_available(port):
            return port
    return None

def kill_existing_processes():
    """Kill any existing Python processes that might be using port 8000"""
    try:
        import subprocess
        import platform
        
        if platform.system() == "Windows":
            subprocess.run(['taskkill', '/F', '/IM', 'python.exe'], 
                          capture_output=True, shell=True)
        else:
            subprocess.run(['pkill', '-f', 'uvicorn'], 
                          capture_output=True)
        logger.info("✅ Killed existing Python processes")
    except Exception as e:
        logger.warning(f"⚠️  Could not kill existing processes: {e}")

def print_startup_banner(port):
    """Print a nice startup banner"""
    print("\n" + "="*60)
    print("🚀 Daena AI VP System - Launching...")
    print("="*60)
    print(f"📍 URL: http://localhost:{port}")
    print(f"📚 API Docs: http://localhost:{port}/docs")
    print(f"🏥 Health Check: http://localhost:{port}/api/v1/system/health")
    print()
    print("🎯 Available Features:")
    print("   • Main Dashboard")
    print("   • Expert Council System")
    print("   • Strategic Room")
    print("   • Voice Panel")
    print("   • Department Management")
    print("   • Real-time Chat & WebSockets")
    print("   • JWT Authentication")
    print("   • GPU Acceleration")
    print()
    print("💡 Quick Access:")
    print(f"   • Council Dashboard: http://localhost:{port}/council-dashboard")
    print(f"   • Strategic Room: http://localhost:{port}/strategic-room")
    print(f"   • Voice Panel: http://localhost:{port}/voice-panel")
    print()
    print("Press Ctrl+C to stop the server")
    print("="*60)

def main():
    """Main launch function"""
    print("Daena AI VP System - Launching...")
    print("=" * 50)
    
    # Environment checks
    if not check_environment():
        logger.error("❌ Environment check failed. Exiting.")
        sys.exit(1)
    
    if not check_dependencies():
        logger.error("❌ Dependency check failed. Exiting.")
        sys.exit(1)
    
    # Import the app
    try:
        from backend.main import app
        logger.info("✅ Backend application loaded successfully")
    except Exception as e:
        logger.error(f"❌ Failed to load backend application: {e}")
        sys.exit(1)
    
    # Configuration
    host = os.getenv("HOST", "0.0.0.0")
    preferred_port = int(os.getenv("PORT", "8000"))
    reload = os.getenv("RELOAD", "false").lower() == "true"
    log_level = os.getenv("LOG_LEVEL", "info").lower()
    
    # Check if preferred port is available
    if not check_port_available(preferred_port):
        logger.warning(f"⚠️  Port {preferred_port} is already in use!")
        print(f"\n⚠️  Port {preferred_port} is already in use!")
        print("Options:")
        print("1. Kill existing processes and use port 8000")
        print("2. Use a different port")
        print("3. Exit")
        
        choice = input("\nEnter your choice (1-3): ").strip()
        
        if choice == "1":
            kill_existing_processes()
            port = preferred_port
        elif choice == "2":
            port = find_available_port(preferred_port + 1)
            if port is None:
                logger.error("❌ No available ports found")
                sys.exit(1)
            logger.info(f"✅ Using alternative port: {port}")
        else:
            logger.info("👋 Exiting...")
            sys.exit(0)
    else:
        port = preferred_port
    
    logger.info(f"🚀 Starting server on {host}:{port}")
    logger.info(f"🔄 Reload mode: {reload}")
    logger.info(f"📝 Log level: {log_level}")
    
    # Print startup banner
    print_startup_banner(port)
    
    try:
        uvicorn.run(
            "backend.main:app",
            host=host,
            port=port,
            reload=reload,
            log_level=log_level,
            access_log=True
        )
    except KeyboardInterrupt:
        logger.info("🛑 Server stopped by user")
        print("\n🛑 Server stopped by user")
    except Exception as e:
        logger.error(f"❌ Server error: {e}")
        print(f"\n❌ Server error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main() 