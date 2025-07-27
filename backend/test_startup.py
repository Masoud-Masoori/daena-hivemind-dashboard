#!/usr/bin/env python3
"""
Test script to check if the backend can start properly
"""

import sys
import os

# Add the current directory to Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test basic FastAPI import
        from fastapi import FastAPI
        print("✅ FastAPI imported successfully")
    except ImportError as e:
        print(f"❌ FastAPI import failed: {e}")
        return False
    
    try:
        # Test routes import
        from routes import agents, departments, consultation
        print("✅ Routes imported successfully")
    except ImportError as e:
        print(f"❌ Routes import failed: {e}")
        return False
    
    try:
        # Test main app creation
        from main import app
        print("✅ Main app imported successfully")
    except ImportError as e:
        print(f"❌ Main app import failed: {e}")
        return False
    
    return True

def test_endpoints():
    """Test if endpoints are accessible"""
    print("\nTesting endpoints...")
    
    try:
        from main import app
        from fastapi.testclient import TestClient
        
        client = TestClient(app)
        
        # Test health check
        response = client.get("/")
        if response.status_code == 200:
            print("✅ Health check endpoint works")
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
        
        # Test daena status
        response = client.get("/api/v1/daena/status")
        if response.status_code == 200:
            print("✅ Daena status endpoint works")
        else:
            print(f"❌ Daena status failed: {response.status_code}")
            return False
            
        return True
        
    except Exception as e:
        print(f"❌ Endpoint testing failed: {e}")
        return False

if __name__ == "__main__":
    print("🔍 Backend Startup Test")
    print("=" * 40)
    
    if test_imports():
        print("\n✅ All imports successful!")
        
        if test_endpoints():
            print("\n✅ All endpoints working!")
            print("\n🎉 Backend is ready to start!")
        else:
            print("\n❌ Endpoint testing failed")
    else:
        print("\n❌ Import testing failed")
        sys.exit(1) 