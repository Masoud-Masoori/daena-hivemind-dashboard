from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import random

router = APIRouter()

# Pydantic models
class SecurityEventBase(BaseModel):
    type: str  # 'authentication', 'authorization', 'data_access', 'system_change', 'threat_detected'
    severity: str  # 'low', 'medium', 'high', 'critical'
    source: str
    description: str
    metadata: Dict[str, Any]

class SecurityEventCreate(SecurityEventBase):
    pass

class SecurityEvent(SecurityEventBase):
    id: str
    timestamp: str
    resolved: bool

class SecurityPolicy(BaseModel):
    id: str
    name: str
    description: str
    rules: List[Dict[str, Any]]
    enabled: bool
    created_at: str
    updated_at: str

class SecurityScan(BaseModel):
    scan_id: str
    status: str  # 'running', 'completed', 'failed'
    started_at: str
    completed_at: Optional[str] = None
    vulnerabilities: List[Dict[str, Any]]
    recommendations: List[Dict[str, Any]]

# Mock data storage
security_events_db = {
    "event-001": {
        "id": "event-001",
        "type": "authentication",
        "severity": "medium",
        "source": "192.168.1.100",
        "description": "Multiple failed login attempts detected",
        "timestamp": "2025-01-14T16:45:00Z",
        "resolved": False,
        "metadata": {
            "user_id": "user-123",
            "attempts": 5,
            "timeframe": "5 minutes"
        }
    },
    "event-002": {
        "id": "event-002",
        "type": "data_access",
        "severity": "high",
        "source": "agent-001",
        "description": "Unauthorized access attempt to sensitive data",
        "timestamp": "2025-01-14T15:30:00Z",
        "resolved": True,
        "metadata": {
            "data_type": "customer_records",
            "access_method": "api_call",
            "blocked": True
        }
    },
    "event-003": {
        "id": "event-003",
        "type": "threat_detected",
        "severity": "critical",
        "source": "network_monitor",
        "description": "Suspicious network activity detected",
        "timestamp": "2025-01-14T14:20:00Z",
        "resolved": False,
        "metadata": {
            "threat_type": "ddos_attack",
            "source_ips": ["203.0.113.1", "203.0.113.2"],
            "requests_per_second": 1000
        }
    }
}

security_policies = {
    "policy-001": {
        "id": "policy-001",
        "name": "Authentication Policy",
        "description": "Enforce strong authentication requirements",
        "rules": [
            {
                "rule_id": "auth-001",
                "name": "Password Complexity",
                "description": "Passwords must meet complexity requirements",
                "enabled": True,
                "conditions": {
                    "min_length": 8,
                    "require_uppercase": True,
                    "require_lowercase": True,
                    "require_numbers": True,
                    "require_special": True
                }
            },
            {
                "rule_id": "auth-002",
                "name": "Failed Login Lockout",
                "description": "Lock account after 5 failed attempts",
                "enabled": True,
                "conditions": {
                    "max_attempts": 5,
                    "lockout_duration": 300,
                    "reset_after": 1800
                }
            }
        ],
        "enabled": True,
        "created_at": "2025-01-14T10:00:00Z",
        "updated_at": "2025-01-14T10:00:00Z"
    }
}

security_scans = {}

@router.get("/events", response_model=List[SecurityEvent])
async def get_security_events(severity: Optional[str] = None, limit: int = 100):
    """Get security events with optional filtering"""
    events = list(security_events_db.values())
    
    if severity:
        events = [event for event in events if event["severity"] == severity]
    
    # Sort by timestamp (newest first) and limit
    events.sort(key=lambda x: x["timestamp"], reverse=True)
    return events[:limit]

@router.get("/events/{event_id}", response_model=SecurityEvent)
async def get_security_event(event_id: str):
    """Get a specific security event"""
    if event_id not in security_events_db:
        raise HTTPException(status_code=404, detail="Security event not found")
    return security_events_db[event_id]

@router.post("/events", response_model=SecurityEvent)
async def create_security_event(event_data: SecurityEventCreate):
    """Create a new security event"""
    event_id = f"event-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    
    new_event = {
        "id": event_id,
        "type": event_data.type,
        "severity": event_data.severity,
        "source": event_data.source,
        "description": event_data.description,
        "timestamp": now,
        "resolved": False,
        "metadata": event_data.metadata
    }
    
    security_events_db[event_id] = new_event
    return new_event

@router.post("/events/{event_id}/resolve")
async def resolve_security_event(event_id: str, resolution: str):
    """Resolve a security event"""
    if event_id not in security_events_db:
        raise HTTPException(status_code=404, detail="Security event not found")
    
    security_events_db[event_id]["resolved"] = True
    security_events_db[event_id]["metadata"]["resolution"] = resolution
    security_events_db[event_id]["metadata"]["resolved_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Security event resolved successfully"}

@router.get("/dashboard")
async def get_security_dashboard():
    """Get security dashboard data"""
    total_events = len(security_events_db)
    critical_events = sum(1 for event in security_events_db.values() if event["severity"] == "critical")
    high_events = sum(1 for event in security_events_db.values() if event["severity"] == "high")
    unresolved_events = sum(1 for event in security_events_db.values() if not event["resolved"])
    
    # Recent threats
    recent_threats = [
        event for event in security_events_db.values()
        if event["type"] == "threat_detected" and 
        datetime.fromisoformat(event["timestamp"].replace("Z", "+00:00")) > datetime.now().replace(tzinfo=None) - timedelta(hours=24)
    ]
    
    return {
        "threats": {
            "total": total_events,
            "critical": critical_events,
            "high": high_events,
            "unresolved": unresolved_events,
            "recent_threats": len(recent_threats)
        },
        "vulnerabilities": {
            "critical": 2,
            "high": 5,
            "medium": 12,
            "low": 25
        },
        "compliance": {
            "gdpr": "compliant",
            "sox": "compliant",
            "pci_dss": "non_compliant",
            "iso_27001": "in_progress"
        }
    }

@router.post("/scan")
async def run_security_scan(background_tasks: BackgroundTasks):
    """Run a comprehensive security scan"""
    scan_id = f"scan-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    
    # Create scan record
    scan = {
        "scan_id": scan_id,
        "status": "running",
        "started_at": now,
        "completed_at": None,
        "vulnerabilities": [],
        "recommendations": []
    }
    
    security_scans[scan_id] = scan
    
    # Simulate security scan
    def simulate_scan():
        import time
        time.sleep(5)  # Simulate scan time
        
        # Generate mock vulnerabilities
        vulnerabilities = [
            {
                "id": f"vuln-{str(uuid.uuid4())[:8]}",
                "severity": "high",
                "title": "SQL Injection Vulnerability",
                "description": "Potential SQL injection in user input validation",
                "cve_id": "CVE-2024-1234",
                "affected_component": "user_authentication",
                "recommendation": "Implement parameterized queries"
            },
            {
                "id": f"vuln-{str(uuid.uuid4())[:8]}",
                "severity": "medium",
                "title": "Weak Password Policy",
                "description": "Password policy does not enforce complexity requirements",
                "cve_id": None,
                "affected_component": "authentication_system",
                "recommendation": "Enforce strong password requirements"
            }
        ]
        
        recommendations = [
            {
                "id": f"rec-{str(uuid.uuid4())[:8]}",
                "priority": "high",
                "title": "Enable Multi-Factor Authentication",
                "description": "Implement MFA for all user accounts",
                "implementation_effort": "medium",
                "security_impact": "high"
            },
            {
                "id": f"rec-{str(uuid.uuid4())[:8]}",
                "priority": "medium",
                "title": "Update Security Headers",
                "description": "Add security headers to web responses",
                "implementation_effort": "low",
                "security_impact": "medium"
            }
        ]
        
        # Update scan results
        security_scans[scan_id]["status"] = "completed"
        security_scans[scan_id]["completed_at"] = datetime.utcnow().isoformat() + "Z"
        security_scans[scan_id]["vulnerabilities"] = vulnerabilities
        security_scans[scan_id]["recommendations"] = recommendations
    
    background_tasks.add_task(simulate_scan)
    
    return {
        "scan_id": scan_id,
        "status": "started",
        "message": "Security scan initiated"
    }

@router.get("/scan/{scan_id}")
async def get_security_scan_results(scan_id: str):
    """Get security scan results"""
    if scan_id not in security_scans:
        raise HTTPException(status_code=404, detail="Security scan not found")
    
    return security_scans[scan_id]

@router.get("/policies", response_model=List[SecurityPolicy])
async def get_security_policies():
    """Get all security policies"""
    return list(security_policies.values())

@router.get("/policies/{policy_id}", response_model=SecurityPolicy)
async def get_security_policy(policy_id: str):
    """Get a specific security policy"""
    if policy_id not in security_policies:
        raise HTTPException(status_code=404, detail="Security policy not found")
    return security_policies[policy_id]

@router.put("/policies/{policy_id}")
async def update_security_policy(policy_id: str, policy_data: Dict[str, Any]):
    """Update a security policy"""
    if policy_id not in security_policies:
        raise HTTPException(status_code=404, detail="Security policy not found")
    
    policy = security_policies[policy_id]
    
    # Update policy fields
    for field, value in policy_data.items():
        if field in ["name", "description", "rules", "enabled"]:
            policy[field] = value
    
    policy["updated_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Security policy updated successfully"}

@router.post("/policies")
async def create_security_policy(policy_data: Dict[str, Any]):
    """Create a new security policy"""
    policy_id = f"policy-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    
    new_policy = {
        "id": policy_id,
        "name": policy_data["name"],
        "description": policy_data["description"],
        "rules": policy_data.get("rules", []),
        "enabled": policy_data.get("enabled", True),
        "created_at": now,
        "updated_at": now
    }
    
    security_policies[policy_id] = new_policy
    return new_policy

@router.delete("/policies/{policy_id}")
async def delete_security_policy(policy_id: str):
    """Delete a security policy"""
    if policy_id not in security_policies:
        raise HTTPException(status_code=404, detail="Security policy not found")
    
    del security_policies[policy_id]
    return {"message": "Security policy deleted successfully"}

@router.get("/threat-intelligence")
async def get_threat_intelligence():
    """Get threat intelligence data"""
    return {
        "recent_threats": [
            {
                "threat_name": "Log4Shell",
                "severity": "critical",
                "description": "Remote code execution vulnerability in Log4j",
                "affected_systems": ["web_servers", "application_servers"],
                "mitigation": "Update to Log4j 2.17.0 or later"
            },
            {
                "threat_name": "SolarWinds Supply Chain Attack",
                "severity": "high",
                "description": "Supply chain attack affecting SolarWinds Orion",
                "affected_systems": ["network_monitoring"],
                "mitigation": "Verify system integrity and update software"
            }
        ],
        "threat_indicators": {
            "suspicious_ips": ["203.0.113.1", "198.51.100.1"],
            "malicious_domains": ["malware.example.com", "phishing.site.com"],
            "file_hashes": ["abc123def456", "xyz789uvw012"]
        },
        "risk_score": 7.5,
        "last_updated": datetime.utcnow().isoformat() + "Z"
    }

@router.post("/incident-response")
async def trigger_incident_response(incident_data: Dict[str, Any]):
    """Trigger incident response procedures"""
    incident_id = f"incident-{str(uuid.uuid4())[:8]}"
    
    # Simulate incident response
    response_actions = [
        "Isolating affected systems",
        "Blocking malicious IPs",
        "Notifying security team",
        "Starting forensic analysis"
    ]
    
    return {
        "incident_id": incident_id,
        "status": "response_initiated",
        "actions_taken": response_actions,
        "estimated_resolution_time": "2-4 hours",
        "severity": incident_data.get("severity", "medium")
    } 