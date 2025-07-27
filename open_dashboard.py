#!/usr/bin/env python3
"""
Daena AI VP System - Dashboard Opener
=====================================
This script opens the Daena dashboard in the default browser.
"""

import webbrowser
import time
import requests
import sys
import json
import subprocess
import platform

def check_server_ready(port=8000, max_attempts=30):
    """Check if server is ready with enhanced health check"""
    print(f"🔍 Checking if server is ready on port {port}...")
    
    for i in range(max_attempts):
        try:
            # Try the health endpoint first
            response = requests.get(f"http://localhost:{port}/api/v1/system/health", timeout=2)
            if response.status_code == 200:
                health_data = response.json()
                print(f"✅ Server is healthy!")
                print(f"   Status: {health_data.get('status', 'unknown')}")
                print(f"   Version: {health_data.get('version', 'unknown')}")
                print(f"   Departments: {health_data.get('system', {}).get('departments', 0)}")
                print(f"   Active Agents: {health_data.get('system', {}).get('active_agents', 0)}")
                return True
        except requests.exceptions.ConnectionError:
            pass
        except requests.exceptions.Timeout:
            pass
        except Exception as e:
            print(f"⚠️  Health check error: {e}")
        
        # Show progress
        if i % 5 == 0:
            print(f"   Waiting... ({i+1}/{max_attempts})")
        time.sleep(1)
    
    return False

def open_browser_with_fallback(url):
    """Open browser with fallback methods"""
    try:
        # Try to open with default browser
        webbrowser.open(url)
        print(f"✅ Opened {url} in default browser")
        return True
    except Exception as e:
        print(f"⚠️  Could not open default browser: {e}")
        
        # Fallback: try platform-specific commands
        try:
            if platform.system() == "Windows":
                subprocess.run(['start', url], shell=True, check=True)
                print(f"✅ Opened {url} using Windows start command")
                return True
            elif platform.system() == "Darwin":  # macOS
                subprocess.run(['open', url], check=True)
                print(f"✅ Opened {url} using macOS open command")
                return True
            elif platform.system() == "Linux":
                subprocess.run(['xdg-open', url], check=True)
                print(f"✅ Opened {url} using Linux xdg-open command")
                return True
        except Exception as e2:
            print(f"⚠️  Platform-specific fallback failed: {e2}")
    
    return False

def print_feature_links(port):
    """Print all available feature links"""
    print("\n🎯 Available Features:")
    print("=" * 50)
    
    features = [
        ("Main Dashboard", f"http://localhost:{port}", "Primary executive dashboard"),
        ("Council Dashboard", f"http://localhost:{port}/council-dashboard", "Expert Council system"),
        ("Strategic Room", f"http://localhost:{port}/strategic-room", "Cross-department analysis"),
        ("Voice Panel", f"http://localhost:{port}/voice-panel", "Voice interaction interface"),
        ("API Documentation", f"http://localhost:{port}/docs", "Interactive API docs"),
        ("Health Check", f"http://localhost:{port}/api/v1/system/health", "System health status")
    ]
    
    for name, url, description in features:
        print(f"🔗 {name}")
        print(f"   URL: {url}")
        print(f"   Description: {description}")
        print()

def main():
    print("Daena AI VP System - Dashboard Opener")
    print("=" * 50)
    
    port = 8000
    
    if check_server_ready(port):
        print("\n🌐 Opening dashboard...")
        
        dashboard_url = f"http://localhost:{port}"
        
        # Open main dashboard
        print(f"🔗 Opening main dashboard: {dashboard_url}")
        if open_browser_with_fallback(dashboard_url):
            # Print all available features
            print_feature_links(port)
            
            print("✅ Dashboard opened in your default browser!")
            print("\n💡 Quick Tips:")
            print("   • Use Ctrl+Click to open links in new tabs")
            print("   • Bookmark frequently used pages")
            print("   • Check the API docs for integration options")
            print("   • Use the Voice Panel for hands-free interaction")
        else:
            print(f"\n❌ Could not open browser automatically")
            print(f"🌐 Please manually open: {dashboard_url}")
            print_feature_links(port)
        
    else:
        print("\n❌ Server is not ready. Please start the server first:")
        print("   python launch.py")
        print("   or")
        print("   launch.bat")
        print("\n🔧 Troubleshooting:")
        print("   1. Check if port 8000 is available")
        print("   2. Ensure all dependencies are installed")
        print("   3. Check the logs in daena.log")
        print("   4. Try running: pip install -r requirements.txt")
        sys.exit(1)

if __name__ == "__main__":
    main() 