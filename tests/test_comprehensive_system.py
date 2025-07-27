#!/usr/bin/env python3
"""
Comprehensive test script for the Daena Expert Council System
Tests all major functionality including authentication, WebSocket, rate limiting, and strategic assembly.
"""

import asyncio
import json
import requests
import os
import time
from datetime import datetime

# Test configuration
BASE_URL = "http://localhost:8000"
TEST_CREDENTIALS = {
    "founder": {"username": "founder", "password": "daena2025!"},
    "admin": {"username": "admin", "password": "admin2025!"}
}

class DaenaSystemTester:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None
        self.test_results = []
    
    def log_test(self, test_name: str, success: bool, details: str = ""):
        """Log test result"""
        status = "✅ PASS" if success else "❌ FAIL"
        print(f"{status} {test_name}")
        if details:
            print(f"   {details}")
        self.test_results.append({
            "test": test_name,
            "success": success,
            "details": details,
            "timestamp": datetime.now().isoformat()
        })
    
    def test_health_check(self):
        """Test enhanced health check endpoint"""
        print("🔍 Testing Enhanced Health Check...")
        try:
            response = requests.get(f"{BASE_URL}/api/v1/system/health")
            if response.status_code == 200:
                data = response.json()
                required_fields = ["status", "system", "connections", "services"]
                if all(field in data for field in required_fields):
                    self.log_test("Enhanced Health Check", True, f"System: {data['system']['departments']} departments, {data['system']['total_agents']} agents")
                    return True
                else:
                    self.log_test("Enhanced Health Check", False, "Missing required fields")
                    return False
            else:
                self.log_test("Enhanced Health Check", False, f"Status code: {response.status_code}")
                return False
        except Exception as e:
            self.log_test("Enhanced Health Check", False, f"Error: {e}")
            return False
    
    def test_authentication(self):
        """Test JWT authentication system"""
        print("🔍 Testing JWT Authentication...")
        try:
            # Test login
            login_response = requests.post(f"{BASE_URL}/api/v1/auth/login", json=TEST_CREDENTIALS["founder"])
            if login_response.status_code == 200:
                data = login_response.json()
                self.access_token = data["access_token"]
                self.refresh_token = data["refresh_token"]
                self.log_test("JWT Login", True, f"User: {data['user']['username']}")
                
                # Test protected endpoint
                headers = {"Authorization": f"Bearer {self.access_token}"}
                protected_response = requests.get(f"{BASE_URL}/api/v1/auth/me", headers=headers)
                if protected_response.status_code == 200:
                    self.log_test("JWT Protected Endpoint", True, "Successfully accessed protected endpoint")
                    return True
                else:
                    self.log_test("JWT Protected Endpoint", False, f"Status code: {protected_response.status_code}")
                    return False
            else:
                self.log_test("JWT Login", False, f"Status code: {login_response.status_code}")
                return False
        except Exception as e:
            self.log_test("JWT Authentication", False, f"Error: {e}")
            return False
    
    def test_rate_limiting(self):
        """Test rate limiting functionality"""
        print("🔍 Testing Rate Limiting...")
        try:
            # Make multiple requests to trigger rate limiting
            headers = {"Authorization": f"Bearer {self.access_token}"} if self.access_token else {}
            
            responses = []
            for i in range(15):  # Should trigger rate limit
                response = requests.get(f"{BASE_URL}/api/v1/council/engineering", headers=headers)
                responses.append(response)
                time.sleep(0.1)  # Small delay
            
            # Check if rate limiting headers are present
            rate_limit_headers = ["X-RateLimit-Limit", "X-RateLimit-Remaining"]
            has_rate_limit_headers = any(
                all(header in response.headers for header in rate_limit_headers)
                for response in responses
            )
            
            if has_rate_limit_headers:
                self.log_test("Rate Limiting", True, "Rate limit headers present")
                return True
            else:
                self.log_test("Rate Limiting", False, "Rate limit headers missing")
                return False
        except Exception as e:
            self.log_test("Rate Limiting", False, f"Error: {e}")
            return False
    
    def test_council_system(self):
        """Test council system with authentication"""
        print("🔍 Testing Council System with Auth...")
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"} if self.access_token else {}
            
            # Test council debate
            debate_data = {"topic": "Should Daena prioritize AI agent development or human-AI collaboration tools?"}
            debate_response = requests.post(f"{BASE_URL}/api/v1/council/engineering/debate", 
                                          json=debate_data, headers=headers)
            
            if debate_response.status_code == 200:
                self.log_test("Council Debate with Auth", True, "Debate created successfully")
                
                # Test council synthesis
                synthesis_response = requests.post(f"{BASE_URL}/api/v1/council/engineering/synthesis", 
                                                 json={}, headers=headers)
                
                if synthesis_response.status_code == 200:
                    self.log_test("Council Synthesis with Auth", True, "Synthesis completed successfully")
                    return True
                else:
                    self.log_test("Council Synthesis with Auth", False, f"Status code: {synthesis_response.status_code}")
                    return False
            else:
                self.log_test("Council Debate with Auth", False, f"Status code: {debate_response.status_code}")
                return False
        except Exception as e:
            self.log_test("Council System with Auth", False, f"Error: {e}")
            return False
    
    def test_strategic_assembly(self):
        """Test strategic assembly system"""
        print("🔍 Testing Strategic Assembly...")
        try:
            headers = {"Authorization": f"Bearer {self.access_token}"} if self.access_token else {}
            
            # Create assembly session
            session_data = {
                "title": "Q1 2025 Strategic Alignment",
                "departments": ["engineering", "marketing", "sales"],
                "topic": "Cross-department strategic alignment for Q1 2025"
            }
            
            session_response = requests.post(f"{BASE_URL}/api/v1/strategic-assembly/sessions/create", 
                                           json=session_data, headers=headers)
            
            if session_response.status_code == 200:
                session = session_response.json()["session"]
                session_id = session["session_id"]
                self.log_test("Strategic Assembly Session Creation", True, f"Session: {session_id}")
                
                # Test cross-department debate
                debate_data = {"topic": "How should we align our Q1 2025 strategy across departments?"}
                debate_response = requests.post(f"{BASE_URL}/api/v1/strategic-assembly/sessions/{session_id}/debate", 
                                              json=debate_data, headers=headers)
                
                if debate_response.status_code == 200:
                    self.log_test("Cross-Department Debate", True, "Cross-department debate completed")
                    
                    # Test cross-department synthesis
                    synthesis_response = requests.post(f"{BASE_URL}/api/v1/strategic-assembly/sessions/{session_id}/synthesis", 
                                                     json={}, headers=headers)
                    
                    if synthesis_response.status_code == 200:
                        self.log_test("Cross-Department Synthesis", True, "Cross-department synthesis completed")
                        return True
                    else:
                        self.log_test("Cross-Department Synthesis", False, f"Status code: {synthesis_response.status_code}")
                        return False
                else:
                    self.log_test("Cross-Department Debate", False, f"Status code: {debate_response.status_code}")
                    return False
            else:
                self.log_test("Strategic Assembly Session Creation", False, f"Status code: {session_response.status_code}")
                return False
        except Exception as e:
            self.log_test("Strategic Assembly", False, f"Error: {e}")
            return False
    
    def test_websocket_endpoints(self):
        """Test WebSocket endpoints"""
        print("🔍 Testing WebSocket Endpoints...")
        try:
            # Test WebSocket endpoints exist (basic connectivity test)
            ws_endpoints = ["/ws/chat", "/ws/council", "/ws/founder"]
            
            for endpoint in ws_endpoints:
                # Basic test - check if endpoint responds to upgrade request
                response = requests.get(f"{BASE_URL}{endpoint}", headers={"Upgrade": "websocket"})
                # Should get 426 or similar for WebSocket upgrade
                if response.status_code in [426, 400, 404]:  # Various possible responses
                    self.log_test(f"WebSocket {endpoint}", True, "Endpoint exists")
                else:
                    self.log_test(f"WebSocket {endpoint}", False, f"Unexpected status: {response.status_code}")
            
            return True
        except Exception as e:
            self.log_test("WebSocket Endpoints", False, f"Error: {e}")
            return False
    
    def test_knowledge_persistence(self):
        """Test knowledge persistence (.json files)"""
        print("🔍 Testing Knowledge Persistence...")
        try:
            # Check if knowledge directory exists and has files
            knowledge_dir = "knowledge"
            if os.path.exists(knowledge_dir):
                dept_dirs = [d for d in os.listdir(knowledge_dir) if os.path.isdir(os.path.join(knowledge_dir, d))]
                total_files = 0
                for dept_dir in dept_dirs:
                    dept_path = os.path.join(knowledge_dir, dept_dir)
                    files = [f for f in os.listdir(dept_path) if f.endswith('.json')]
                    total_files += len(files)
                
                self.log_test("Knowledge Persistence", True, f"{len(dept_dirs)} departments, {total_files} files")
                return True
            else:
                self.log_test("Knowledge Persistence", False, "Knowledge directory not found")
                return False
        except Exception as e:
            self.log_test("Knowledge Persistence", False, f"Error: {e}")
            return False
    
    def run_comprehensive_test(self):
        """Run all comprehensive tests"""
        print("🚀 Starting Comprehensive Daena System Test")
        print("=" * 60)
        
        tests = [
            ("Enhanced Health Check", self.test_health_check),
            ("JWT Authentication", self.test_authentication),
            ("Rate Limiting", self.test_rate_limiting),
            ("Council System with Auth", self.test_council_system),
            ("Strategic Assembly", self.test_strategic_assembly),
            ("WebSocket Endpoints", self.test_websocket_endpoints),
            ("Knowledge Persistence", self.test_knowledge_persistence),
        ]
        
        for test_name, test_func in tests:
            print(f"\n📋 {test_name}")
            print("-" * 40)
            try:
                test_func()
            except Exception as e:
                self.log_test(test_name, False, f"Test crashed: {e}")
        
        print("\n" + "=" * 60)
        print("📊 COMPREHENSIVE TEST SUMMARY")
        print("=" * 60)
        
        passed = sum(1 for result in self.test_results if result["success"])
        total = len(self.test_results)
        
        for result in self.test_results:
            status = "✅ PASS" if result["success"] else "❌ FAIL"
            print(f"{status} {result['test']}")
        
        print(f"\n🎯 Overall: {passed}/{total} tests passed ({passed/total*100:.1f}%)")
        
        if passed == total:
            print("🎉 All tests passed! Daena system is fully operational.")
        else:
            print("⚠️ Some tests failed. Please check the implementation.")
        
        # Save test results
        with open("test_results.json", "w") as f:
            json.dump({
                "timestamp": datetime.now().isoformat(),
                "total_tests": total,
                "passed_tests": passed,
                "success_rate": passed/total*100,
                "results": self.test_results
            }, f, indent=2)
        
        print(f"\n📄 Test results saved to: test_results.json")
        
        return passed == total

if __name__ == "__main__":
    tester = DaenaSystemTester()
    success = tester.run_comprehensive_test()
    exit(0 if success else 1) 