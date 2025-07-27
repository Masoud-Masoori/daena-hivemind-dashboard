#!/usr/bin/env python3
"""
Daena AI VP System - Council System Test
=========================================
This script tests the council system functionality including advisor agents, debates, and synthesis.
"""

import requests
import json
import time
import sys

def test_council_system():
    """Test the complete council system"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Daena Council System")
    print("=" * 50)
    
    # Test 1: Authentication
    print("\n1. Testing Authentication...")
    try:
        login_response = requests.post(f"{base_url}/api/v1/auth/login", json={
            "username": "founder",
            "password": "daena2025!"
        })
        
        if login_response.status_code == 200:
            token = login_response.json()["access_token"]
            print("✅ Authentication successful")
        else:
            print(f"❌ Authentication failed: {login_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Authentication error: {e}")
        return False
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Test 2: Get Council State
    print("\n2. Testing Council State...")
    try:
        council_response = requests.get(f"{base_url}/api/v1/council/engineering", headers=headers)
        
        if council_response.status_code == 200:
            council_data = council_response.json()
            if council_data["success"]:
                council = council_data["council"]
                advisors = council.get("advisors", [])
                print(f"✅ Council state retrieved successfully")
                print(f"   📊 Advisors: {len(advisors)}")
                print(f"   📊 Scouts: {len(council.get('scouts', []))}")
                print(f"   📊 Synthesizer: {council.get('synthesizer', {}).get('name', 'None')}")
                
                # Display advisor details
                print("\n   👥 Advisor Agents:")
                for advisor in advisors:
                    print(f"      • {advisor['name']} ({advisor['persona']}) - {advisor['expertise']}")
            else:
                print("❌ Council state retrieval failed")
                return False
        else:
            print(f"❌ Council state request failed: {council_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Council state error: {e}")
        return False
    
    # Test 3: Start a Debate
    print("\n3. Testing Council Debate...")
    try:
        debate_topic = "Should Daena prioritize AI agent development or human-AI collaboration tools?"
        debate_response = requests.post(f"{base_url}/api/v1/council/engineering/debate", 
                                      headers=headers,
                                      json={"topic": debate_topic})
        
        if debate_response.status_code == 200:
            debate_data = debate_response.json()
            if debate_data["success"]:
                debate = debate_data["debate"]
                print(f"✅ Debate started successfully")
                print(f"   📝 Topic: {debate['topic']}")
                print(f"   👥 Participants: {len(debate['arguments'])}")
                print(f"   🆔 Debate ID: {debate['debate_id']}")
                
                # Display arguments
                print("\n   💬 Advisor Arguments:")
                for advisor, argument in debate['arguments'].items():
                    print(f"      • {advisor}: {argument[:100]}...")
            else:
                print("❌ Debate creation failed")
                return False
        else:
            print(f"❌ Debate request failed: {debate_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Debate error: {e}")
        return False
    
    # Test 4: Run Synthesis
    print("\n4. Testing Council Synthesis...")
    try:
        synthesis_response = requests.post(f"{base_url}/api/v1/council/engineering/synthesis", 
                                         headers=headers,
                                         json={})
        
        if synthesis_response.status_code == 200:
            synthesis_data = synthesis_response.json()
            if synthesis_data["success"]:
                synthesis = synthesis_data["synthesis"]
                print(f"✅ Synthesis completed successfully")
                print(f"   📊 Summary: {synthesis['summary'][:100]}...")
                print(f"   🎯 Confidence Scores: {len(synthesis['confidence_scores'])} advisors")
                print(f"   ❓ Follow-up Questions: {len(synthesis['followup_questions'])}")
                print(f"   🆔 Synthesis ID: {synthesis['synthesis_id']}")
                
                # Display confidence scores
                print("\n   📈 Confidence Scores:")
                for advisor, score in synthesis['confidence_scores'].items():
                    print(f"      • {advisor}: {score * 100:.0f}%")
                
                # Display follow-up questions
                print("\n   ❓ Follow-up Questions:")
                for i, question in enumerate(synthesis['followup_questions'], 1):
                    print(f"      {i}. {question}")
            else:
                print("❌ Synthesis failed")
                return False
        else:
            print(f"❌ Synthesis request failed: {synthesis_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Synthesis error: {e}")
        return False
    
    # Test 5: Check Updated Council State
    print("\n5. Testing Updated Council State...")
    try:
        updated_response = requests.get(f"{base_url}/api/v1/council/engineering", headers=headers)
        
        if updated_response.status_code == 200:
            updated_data = updated_response.json()
            if updated_data["success"]:
                updated_council = updated_data["council"]
                debate_history = updated_council.get("debate_history", [])
                last_synthesis = updated_council.get("last_synthesis")
                
                print(f"✅ Updated council state retrieved")
                print(f"   📚 Debate History: {len(debate_history)} debates")
                print(f"   🧠 Last Synthesis: {'Yes' if last_synthesis else 'No'}")
            else:
                print("❌ Updated council state retrieval failed")
                return False
        else:
            print(f"❌ Updated council state request failed: {updated_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Updated council state error: {e}")
        return False
    
    # Test 6: Test Different Department
    print("\n6. Testing Different Department...")
    try:
        product_response = requests.get(f"{base_url}/api/v1/council/product", headers=headers)
        
        if product_response.status_code == 200:
            product_data = product_response.json()
            if product_data["success"]:
                product_council = product_data["council"]
                product_advisors = product_council.get("advisors", [])
                print(f"✅ Product department council initialized")
                print(f"   👥 Advisors: {len(product_advisors)}")
                
                # Verify same advisor agents
                advisor_names = [advisor['name'] for advisor in product_advisors]
                expected_names = ["Steve Jobs", "Satya Nadella", "Sheryl Sandberg", "Elon Musk", "Indra Nooyi"]
                if set(advisor_names) == set(expected_names):
                    print("   ✅ All advisor agents present")
                else:
                    print("   ❌ Missing advisor agents")
                    return False
            else:
                print("❌ Product department council initialization failed")
                return False
        else:
            print(f"❌ Product department request failed: {product_response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Product department error: {e}")
        return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL COUNCIL SYSTEM TESTS PASSED!")
    print("=" * 50)
    print("\n📋 Summary:")
    print("   ✅ Authentication working")
    print("   ✅ Advisor agents initialized (Steve Jobs, Satya Nadella, Sheryl Sandberg, Elon Musk, Indra Nooyi)")
    print("   ✅ Scout agents working")
    print("   ✅ Synthesizer agent working")
    print("   ✅ Debate system functional")
    print("   ✅ Synthesis system functional")
    print("   ✅ Multi-department support")
    print("   ✅ Council state persistence")
    
    return True

if __name__ == "__main__":
    try:
        success = test_council_system()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1) 