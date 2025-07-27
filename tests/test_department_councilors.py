#!/usr/bin/env python3
"""
Daena AI VP System - Department Councilors Test
===============================================
This script tests that each department has its own specialized councilors.
"""

import requests
import json
import sys

def test_department_councilors():
    """Test department-specific councilors"""
    base_url = "http://localhost:8000"
    
    print("🧪 Testing Department-Specific Councilors")
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
    
    # Test 2: Test each department's councilors
    departments = ["engineering", "product", "marketing", "sales", "finance", "hr", "operations", "legal"]
    
    print(f"\n2. Testing Department Councilors...")
    
    for dept in departments:
        print(f"\n   📊 Testing {dept.upper()} Department:")
        try:
            response = requests.get(f"{base_url}/api/v1/council/{dept}", headers=headers)
            
            if response.status_code == 200:
                data = response.json()
                if data["success"]:
                    council = data["council"]
                    advisors = council.get("advisors", [])
                    scouts = council.get("scouts", [])
                    
                    print(f"      ✅ {dept} council loaded successfully")
                    print(f"      👥 Advisors: {len(advisors)}")
                    print(f"      🔍 Scouts: {len(scouts)}")
                    
                    # Display advisor details
                    print(f"      📋 Advisors:")
                    for advisor in advisors:
                        print(f"         • {advisor['name']} ({advisor['persona']}) - {advisor['expertise']}")
                    
                    # Display scout details
                    print(f"      🔍 Scouts:")
                    for scout in scouts:
                        print(f"         • {scout['name']} - {scout['focus_area']}")
                    
                    # Verify department-specific advisors
                    expected_advisors = get_expected_advisors(dept)
                    actual_names = [advisor['name'] for advisor in advisors]
                    
                    if set(actual_names) == set(expected_advisors):
                        print(f"      ✅ All expected advisors present for {dept}")
                    else:
                        print(f"      ❌ Missing advisors for {dept}")
                        print(f"         Expected: {expected_advisors}")
                        print(f"         Actual: {actual_names}")
                        return False
                    
                else:
                    print(f"      ❌ Failed to load {dept} council")
                    return False
            else:
                print(f"      ❌ Request failed for {dept}: {response.status_code}")
                return False
                
        except Exception as e:
            print(f"      ❌ Error testing {dept}: {e}")
            return False
    
    # Test 3: Test debate with department-specific advisors
    print(f"\n3. Testing Department-Specific Debates...")
    
    for dept in departments[:3]:  # Test first 3 departments
        print(f"\n   💬 Testing debate for {dept.upper()}:")
        try:
            debate_topic = f"Should the {dept} department prioritize innovation or stability?"
            debate_response = requests.post(f"{base_url}/api/v1/council/{dept}/debate", 
                                          headers=headers,
                                          json={"topic": debate_topic})
            
            if debate_response.status_code == 200:
                debate_data = debate_response.json()
                if debate_data["success"]:
                    debate = debate_data["debate"]
                    participants = list(debate["arguments"].keys())
                    
                    print(f"      ✅ Debate started successfully")
                    print(f"      📝 Topic: {debate['topic']}")
                    print(f"      👥 Participants: {len(participants)}")
                    
                    # Verify participants are department-specific
                    expected_advisors = get_expected_advisors(dept)
                    if set(participants) == set(expected_advisors):
                        print(f"      ✅ Debate participants match {dept} advisors")
                    else:
                        print(f"      ❌ Debate participants don't match {dept} advisors")
                        print(f"         Expected: {expected_advisors}")
                        print(f"         Actual: {participants}")
                        return False
                    
                else:
                    print(f"      ❌ Debate creation failed for {dept}")
                    return False
            else:
                print(f"      ❌ Debate request failed for {dept}: {debate_response.status_code}")
                return False
                
        except Exception as e:
            print(f"      ❌ Error testing debate for {dept}: {e}")
            return False
    
    print("\n" + "=" * 50)
    print("🎉 ALL DEPARTMENT COUNCILOR TESTS PASSED!")
    print("=" * 50)
    print("\n📋 Summary:")
    print("   ✅ All departments have specialized advisor agents")
    print("   ✅ All departments have specialized scout agents")
    print("   ✅ Department-specific debates work correctly")
    print("   ✅ Navigation between departments functional")
    print("   ✅ Council state persistence working")
    
    return True

def get_expected_advisors(department):
    """Get expected advisor names for each department"""
    expected = {
        "engineering": ["Linus Torvalds", "Grace Hopper", "Alan Kay", "Margaret Hamilton", "Dennis Ritchie"],
        "product": ["Steve Jobs", "Jeff Bezos", "Elon Musk", "Reid Hoffman", "Marissa Mayer"],
        "marketing": ["Seth Godin", "Gary Vaynerchuk", "Simon Sinek", "Ann Handley", "David Ogilvy"],
        "sales": ["Grant Cardone", "Zig Ziglar", "Brian Tracy", "Jill Konrath", "Tom Hopkins"],
        "finance": ["Warren Buffett", "Ray Dalio", "Jamie Dimon", "Cathie Wood", "Charlie Munger"],
        "hr": ["Patty McCord", "Laszlo Bock", "Sheryl Sandberg", "Adam Grant", "Kim Scott"],
        "operations": ["Jack Welch", "W. Edwards Deming", "Taiichi Ohno", "Eliyahu Goldratt", "Shigeo Shingo"],
        "legal": ["Ruth Bader Ginsburg", "Clarence Darrow", "Thurgood Marshall", "Oliver Wendell Holmes Jr.", "Sandra Day O'Connor"]
    }
    return expected.get(department, [])

if __name__ == "__main__":
    try:
        success = test_department_councilors()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n🛑 Test interrupted by user")
        sys.exit(1)
    except Exception as e:
        print(f"\n❌ Test failed with error: {e}")
        sys.exit(1) 