#!/usr/bin/env python3
"""
Daena AI VP System - Server Status Checker
==========================================
This script checks if the Daena server is running and provides status information.
"""

import requests
import socket
import sys
import time
from datetime import datetime

def check_port(port=8000):
    """Check if a port is open"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(1)
            result = s.connect_ex(('localhost', port))
            return result == 0
    except:
        return False

def check_server_health(port=8000):
    """Check server health endpoint"""
    try:
        response = requests.get(f"http://localhost:{port}/api/v1/system/health", timeout=5)
        if response.status_code == 200:
            return response.json()
        return None
    except:
        return None

def main():
    print("Daena AI VP System - Server Status Checker")
    print("=" * 50)
    
    # Check if server is running on port 8000
    if check_port(8000):
        print("✅ Server is running on port 8000")
        
        # Check health endpoint
        health_data = check_server_health(8000)
        if health_data:
            print("✅ Health check passed")
            print(f"📊 Status: {health_data.get('status', 'Unknown')}")
            print(f"📅 Timestamp: {health_data.get('timestamp', 'Unknown')}")
            print(f"🏢 Departments: {health_data.get('system', {}).get('departments', 'Unknown')}")
            print(f"🤖 Agents: {health_data.get('system', {}).get('total_agents', 'Unknown')}")
            print(f"📈 Projects: {health_data.get('system', {}).get('projects', 'Unknown')}")
            
            print(f"\n🌐 Access URLs:")
            print(f"   Main Dashboard: http://localhost:8000")
            print(f"   API Docs: http://localhost:8000/docs")
            print(f"   Health Check: http://localhost:8000/api/v1/system/health")
        else:
            print("⚠️  Server is running but health check failed")
    else:
        print("❌ Server is not running on port 8000")
        
        # Check other common ports
        for port in [8001, 8002, 8003, 8080]:
            if check_port(port):
                print(f"✅ Found server running on port {port}")
                health_data = check_server_health(port)
                if health_data:
                    print(f"✅ Health check passed on port {port}")
                    print(f"🌐 Access URL: http://localhost:{port}")
                break
        else:
            print("❌ No Daena server found on common ports")
            print("\nTo start the server:")
            print("   python launch.py")
            print("   or")
            print("   launch.bat")

if __name__ == "__main__":
    main() 