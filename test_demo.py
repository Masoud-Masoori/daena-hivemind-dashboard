#!/usr/bin/env python3
"""
Comprehensive Demo Test for Daena AI VP
Tests all enhanced demo features including Azure OpenAI integration
"""

import requests
import time
import json

def test_demo():
    """Test all demo endpoints"""
    base_url = "http://localhost:3000"  # Updated to port 3000
    
    print("🧪 Testing Daena AI VP Enhanced Demo")
    print("=" * 50)
    
    # Test 1: Health check
    print("\n1️⃣ Testing Health Check...")
    try:
        response = requests.get(f"{base_url}/demo/health", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Service: {data.get('service')}")
            print(f"   ✅ Azure OpenAI: {data.get('azure_openai')}")
            print(f"   ✅ Agents: {data.get('agents_available')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Health check error: {e}")
    
    # Test 2: Demo page
    print("\n2️⃣ Testing Demo Page...")
    try:
        response = requests.get(f"{base_url}/demo/", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            print(f"   ✅ Page loaded: {len(response.text)} characters")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Demo page error: {e}")
    
    # Test 3: System Status
    print("\n3️⃣ Testing System Status...")
    try:
        response = requests.get(f"{base_url}/demo/system-status", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Backend: {data.get('backend')}")
            print(f"   ✅ Azure OpenAI: {data.get('azure_openai')}")
            print(f"   ✅ Gmail: {data.get('gmail')}")
            print(f"   ✅ Voice: {data.get('voice')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ System status error: {e}")
    
    # Test 4: Demo Data
    print("\n4️⃣ Testing Demo Data...")
    try:
        response = requests.get(f"{base_url}/demo/demo-data", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Investors: {len(data.get('investors', {}))}")
            print(f"   ✅ Email Tones: {len(data.get('email_tones', []))}")
            print(f"   ✅ Company: {data.get('company_info', {}).get('name')}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Demo data error: {e}")
    
    # Test 5: Chat endpoint
    print("\n5️⃣ Testing Chat with Daena...")
    try:
        response = requests.post(f"{base_url}/demo/chat", 
                               json={"message": "Hello Daena, tell me about your investor outreach capabilities"}, 
                               timeout=10)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Response: {data.get('response', '')[:100]}...")
            print(f"   ✅ Tokens Used: {data.get('tokens_used', 0)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Chat error: {e}")
    
    # Test 6: Generate Email
    print("\n6️⃣ Testing Email Generation...")
    try:
        response = requests.post(f"{base_url}/demo/generate-email", 
                               json={
                                   "investor_type": "toronto_ai",
                                   "tone": "professional",
                                   "custom_message": "We're seeking Series A funding for our AI VP platform"
                               }, 
                               timeout=15)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Subject: {data.get('subject', '')[:50]}...")
            print(f"   ✅ Body Length: {len(data.get('body', ''))} characters")
            print(f"   ✅ Tokens Used: {data.get('tokens_used', 0)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Email generation error: {e}")
    
    # Test 7: Send Email (Simulated)
    print("\n7️⃣ Testing Email Sending...")
    try:
        response = requests.post(f"{base_url}/demo/send-email", 
                               json={
                                   "investor_type": "canadian_tech",
                                   "tone": "confident",
                                   "custom_message": "Ready to revolutionize business leadership"
                               }, 
                               timeout=15)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Status: {data.get('status')}")
            print(f"   ✅ Message: {data.get('message', '')[:50]}...")
            print(f"   ✅ Tokens Used: {data.get('tokens_used', 0)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Email sending error: {e}")
    
    # Test 8: Usage Stats
    print("\n8️⃣ Testing Usage Statistics...")
    try:
        response = requests.get(f"{base_url}/demo/usage-stats", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Tokens Used: {data.get('tokens_used', 0)}")
            print(f"   ✅ Emails Sent: {data.get('emails_sent', 0)}")
            print(f"   ✅ Voice Interactions: {data.get('voice_interactions', 0)}")
            print(f"   ✅ Session Duration: {data.get('session_duration', 0):.1f}s")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Usage stats error: {e}")
    
    # Test 9: Email History
    print("\n9️⃣ Testing Email History...")
    try:
        response = requests.get(f"{base_url}/demo/email-history", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Emails in History: {data.get('count', 0)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Email history error: {e}")
    
    # Test 10: Voice Interaction
    print("\n🔟 Testing Voice Interaction...")
    try:
        response = requests.post(f"{base_url}/demo/voice-interaction", timeout=5)
        print(f"   Status: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"   ✅ Voice Interactions: {data.get('voice_interactions', 0)}")
        else:
            print(f"   ❌ Error: {response.text}")
    except Exception as e:
        print(f"   ❌ Voice interaction error: {e}")

def test_azure_connection():
    """Test Azure OpenAI connection specifically"""
    print("\n🔗 Testing Azure OpenAI Connection...")
    try:
        response = requests.get("http://localhost:3000/demo/health", timeout=5)
        if response.status_code == 200:
            data = response.json()
            if data.get('azure_openai') == 'connected':
                print("   ✅ Azure OpenAI is connected and working")
                return True
            else:
                print("   ❌ Azure OpenAI is not connected")
                return False
        else:
            print("   ❌ Cannot reach demo server")
            return False
    except Exception as e:
        print(f"   ❌ Connection test error: {e}")
        return False

if __name__ == "__main__":
    print("⏳ Waiting for server to start...")
    time.sleep(3)
    
    # Test Azure connection first
    azure_connected = test_azure_connection()
    
    if azure_connected:
        test_demo()
        print("\n🎉 Demo testing completed!")
        print("🌐 Demo available at: http://localhost:3000/demo")
        print("📊 API docs at: http://localhost:3000/docs")
    else:
        print("\n⚠️  Azure OpenAI not connected. Some features may not work.")
        print("   Please check your Azure configuration and try again.")
        print("🌐 Demo available at: http://localhost:3000/demo") 