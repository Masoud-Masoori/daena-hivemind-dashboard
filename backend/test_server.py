#!/usr/bin/env python3
"""
Simple test script to start the Daena backend server
"""

import uvicorn
import sys
import os

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    print("Starting Daena AI VP System...")
    print("Testing server startup...")
    
    try:
        # Import the app
        from main import app
        print("✅ App imported successfully")
        
        # Start the server
        uvicorn.run(
            app,
            host="127.0.0.1",
            port=8000,
            log_level="info"
        )
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main() 