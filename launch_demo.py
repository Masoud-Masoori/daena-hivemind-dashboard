#!/usr/bin/env python3
"""
Daena AI VP Demo Launcher
Launches the demo server with all necessary components
"""

import os
import sys
import subprocess
import time
import webbrowser
import socket
from pathlib import Path

def check_dependencies():
    """Check if required dependencies are installed"""
    required_packages = [
        "fastapi",
        "uvicorn",
        "jinja2",
        "python-multipart",
        "openai",
        "requests",
        "PyJWT"
    ]
    
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package.replace("-", "_"))
        except ImportError:
            missing_packages.append(package)
    
    if missing_packages:
        print(f"❌ Missing required packages: {', '.join(missing_packages)}")
        print("Installing missing packages...")
        subprocess.run([sys.executable, "-m", "pip", "install"] + missing_packages)
        print("✅ Dependencies installed")
    else:
        print("✅ All dependencies are installed")

def setup_environment():
    """Setup environment variables"""
    env_vars = {
        # Gmail Configuration
        "GMAIL_USER": "masoud.masoori@gmail.com",
        "GMAIL_APP_PASSWORD": "",  # Set this for real email sending
        
        # Azure OpenAI Configuration - Updated to new endpoint
        "OPENAI_API_TYPE": "azure",
        "OPENAI_API_KEY": "1HmnkpDuMqMzKDtYbpcckyVQC6qlggup3zAVmfkG65BjxAtT9JKtJQQJ99BGACHYHv6XJ3w3AAAAACOGX3DN",
        "OPENAI_API_BASE": "https://masou-mdksrl1q-eastus2.openai.azure.com/",
        "OPENAI_API_VERSION": "2024-02-15",
        "OPENAI_DEPLOYMENT_NAME": "daena",
        
        # Demo Configuration
        "DEMO_PORT": "3000",
        "DEMO_MODE": "production"
    }
    
    for key, value in env_vars.items():
        if not os.getenv(key):
            os.environ[key] = value
            print(f"✅ Set {key} to configured value")
        else:
            print(f"✅ {key} already set")

def find_available_port(start_port=3000, max_attempts=10):
    """Find an available port starting from start_port"""
    for port in range(start_port, start_port + max_attempts):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('localhost', port))
                return port
        except OSError:
            continue
    return None

def start_server():
    """Start the FastAPI server"""
    print("🚀 Starting Daena AI VP Demo Server...")
    print("=" * 50)
    
    # Change to backend directory
    backend_dir = Path("backend")
    if not backend_dir.exists():
        print("❌ Backend directory not found")
        return False
    
    os.chdir(backend_dir)
    
    # Find available port
    port = find_available_port(3000)
    if not port:
        print("❌ No available ports found")
        return False
    
    print(f"🌐 Using port {port}")
    
    # Start server
    try:
        cmd = [
            sys.executable, "-m", "uvicorn", 
            "main:app", 
            "--host", "0.0.0.0", 
            "--port", str(port),
            "--reload"
        ]
        
        print(f"Starting server with command: {' '.join(cmd)}")
        
        # Store port in environment for browser opening
        os.environ['DEMO_PORT'] = str(port)
        
        subprocess.run(cmd)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
    except Exception as e:
        print(f"❌ Failed to start server: {e}")
        return False
    
    return True

def open_demo():
    """Open demo in browser"""
    print("🌐 Opening demo in browser...")
    time.sleep(3)  # Wait for server to start
    
    port = os.getenv('DEMO_PORT', '3000')
    demo_url = f"http://localhost:{port}/demo"
    
    try:
        webbrowser.open(demo_url)
        print(f"✅ Demo opened in browser at {demo_url}")
    except Exception as e:
        print(f"⚠️  Could not open browser automatically: {e}")
        print(f"🌐 Please open: {demo_url}")

def main():
    """Main launcher function"""
    print("🎯 Daena AI VP Demo Launcher")
    print("=" * 50)
    
    # Check dependencies
    check_dependencies()
    
    # Setup environment
    setup_environment()
    
    # Start server
    if start_server():
        print("✅ Server started successfully")
    else:
        print("❌ Failed to start server")
        sys.exit(1)

if __name__ == "__main__":
    main() 