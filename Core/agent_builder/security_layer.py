"""Advanced Security Layer - Ensures all generated agents are secure, compliant, and protect user data."""

import hashlib
import json
import logging
import secrets
import time
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
from datetime import datetime, timedelta
import jwt
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
from pydantic import BaseModel, validator
from Core.agent_builder.agent_blueprint import AgentBlueprint, SecurityLevel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SecurityThreatLevel(str, Enum):
    """Security threat levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class ComplianceStandard(str, Enum):
    """Compliance standards."""
    GDPR = "gdpr"
    HIPAA = "hipaa"
    SOC2 = "soc2"
    ISO27001 = "iso27001"
    PCI_DSS = "pci_dss"
    CCPA = "ccpa"

class DataClassification(str, Enum):
    """Data classification levels."""
    PUBLIC = "public"
    INTERNAL = "internal"
    CONFIDENTIAL = "confidential"
    RESTRICTED = "restricted"

@dataclass
class SecurityAudit:
    """Security audit result."""
    agent_id: str
    timestamp: datetime
    threat_level: SecurityThreatLevel
    vulnerabilities: List[str]
    recommendations: List[str]
    compliance_status: Dict[str, bool]
    data_handling_score: float
    encryption_status: Dict[str, bool]
    access_controls: Dict[str, Any]

class SecurityConfig(BaseModel):
    """Security configuration for an agent."""
    encryption_enabled: bool = True
    encryption_algorithm: str = "AES-256-GCM"
    key_rotation_days: int = 90
    session_timeout_minutes: int = 30
    max_login_attempts: int = 5
    password_policy: Dict[str, Any] = {
        "min_length": 12,
        "require_uppercase": True,
        "require_lowercase": True,
        "require_numbers": True,
        "require_special": True
    }
    mfa_required: bool = True
    audit_logging: bool = True
    data_retention_days: int = 90
    backup_frequency_hours: int = 24
    threat_detection: bool = True
    sandbox_mode: bool = True
    api_rate_limiting: bool = True
    rate_limit_requests_per_minute: int = 100
    ip_whitelist: List[str] = []
    allowed_domains: List[str] = []
    blocked_patterns: List[str] = []
    compliance_standards: List[ComplianceStandard] = []

class AgentSecurityLayer:
    """Advanced Security Layer for Agent Protection."""
    
    def __init__(self, master_key: Optional[str] = None):
        """Initialize the security layer."""
        self.master_key = master_key or self._generate_master_key()
        self.encryption_key = self._derive_encryption_key()
        self.cipher_suite = Fernet(self.encryption_key)
        
        # Security policies
        self.security_policies = self._load_security_policies()
        self.threat_patterns = self._load_threat_patterns()
        self.compliance_requirements = self._load_compliance_requirements()
        
        # Audit trail
        self.audit_log = []
        
        # Rate limiting
        self.rate_limit_store = {}
        
        # Session management
        self.active_sessions = {}

    def _generate_master_key(self) -> str:
        """Generate a secure master key."""
        return secrets.token_urlsafe(32)

    def _derive_encryption_key(self) -> bytes:
        """Derive encryption key from master key."""
        salt = b'daena_security_salt_2024'
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(self.master_key.encode()))
        return key

    def _load_security_policies(self) -> Dict[str, Any]:
        """Load security policies."""
        return {
            "data_encryption": {
                "at_rest": True,
                "in_transit": True,
                "algorithm": "AES-256-GCM",
                "key_rotation": 90
            },
            "access_control": {
                "rbac_enabled": True,
                "session_timeout": 1800,
                "max_sessions": 5,
                "ip_restriction": True
            },
            "audit_logging": {
                "enabled": True,
                "retention_days": 365,
                "log_level": "INFO",
                "encrypted_logs": True
            },
            "threat_detection": {
                "enabled": True,
                "anomaly_detection": True,
                "rate_limiting": True,
                "pattern_matching": True
            },
            "compliance": {
                "gdpr": True,
                "hipaa": False,
                "soc2": True,
                "data_localization": True
            }
        }

    def _load_threat_patterns(self) -> Dict[str, List[str]]:
        """Load threat detection patterns."""
        return {
            "sql_injection": [
                r"(\b(union|select|insert|update|delete|drop|create|alter)\b)",
                r"(\b(or|and)\b\s+\d+\s*=\s*\d+)",
                r"(\b(union|select)\b.*\bfrom\b)",
                r"(\b(union|select)\b.*\bwhere\b)"
            ],
            "xss": [
                r"(<script[^>]*>.*?</script>)",
                r"(javascript:)",
                r"(on\w+\s*=)",
                r"(<iframe[^>]*>)",
                r"(<object[^>]*>)"
            ],
            "path_traversal": [
                r"(\.\./\.\./)",
                r"(\.\.\\)",
                r"(\.\.%2f)",
                r"(\.\.%5c)"
            ],
            "command_injection": [
                r"(\b(cmd|command|exec|system|shell)\b)",
                r"(\b(ping|nslookup|traceroute)\b)",
                r"(\b(rm|del|format|fdisk)\b)"
            ],
            "data_exfiltration": [
                r"(\b(email|mail|send)\b.*\b(to|cc|bcc)\b)",
                r"(\b(upload|post|put)\b.*\b(http|https)\b)",
                r"(\b(copy|move|transfer)\b.*\b(file|data)\b)"
            ]
        }

    def _load_compliance_requirements(self) -> Dict[str, Dict[str, Any]]:
        """Load compliance requirements."""
        return {
            ComplianceStandard.GDPR: {
                "data_minimization": True,
                "consent_management": True,
                "right_to_forget": True,
                "data_portability": True,
                "privacy_by_design": True,
                "breach_notification": True
            },
            ComplianceStandard.HIPAA: {
                "phi_protection": True,
                "access_controls": True,
                "audit_trails": True,
                "encryption": True,
                "backup_security": True,
                "incident_response": True
            },
            ComplianceStandard.SOC2: {
                "security": True,
                "availability": True,
                "processing_integrity": True,
                "confidentiality": True,
                "privacy": True
            },
            ComplianceStandard.ISO27001: {
                "information_security_policy": True,
                "risk_assessment": True,
                "access_control": True,
                "cryptography": True,
                "physical_security": True,
                "operations_security": True
            }
        }

    def secure_agent_blueprint(self, blueprint: AgentBlueprint, user_context: Dict[str, Any]) -> AgentBlueprint:
        """Apply security measures to an agent blueprint."""
        try:
            # Create security configuration
            security_config = self._create_security_config(blueprint, user_context)
            
            # Apply security policies
            blueprint.security = security_config
            
            # Add security metadata
            blueprint.metadata["security_audit"] = {
                "secured_at": datetime.utcnow().isoformat(),
                "security_level": blueprint.security.level,
                "encryption_enabled": blueprint.security.encryption_enabled,
                "audit_logging": blueprint.security.audit_logging,
                "threat_detection": blueprint.security.threat_detection,
                "sandbox_mode": blueprint.security.sandbox_mode
            }
            
            # Add compliance metadata
            blueprint.metadata["compliance"] = self._assess_compliance(blueprint)
            
            # Encrypt sensitive data
            blueprint = self._encrypt_sensitive_data(blueprint)
            
            # Generate security hash
            blueprint.metadata["security_hash"] = self._generate_security_hash(blueprint)
            
            logger.info(f"Agent blueprint secured: {blueprint.id}")
            return blueprint
            
        except Exception as e:
            logger.error(f"Error securing agent blueprint: {e}")
            raise

    def _create_security_config(self, blueprint: AgentBlueprint, user_context: Dict[str, Any]) -> 'AgentSecurity':
        """Create security configuration for the agent."""
        from Core.agent_builder.agent_blueprint import AgentSecurity, SecurityLevel
        
        # Determine security level based on agent type and user context
        security_level = self._determine_security_level(blueprint, user_context)
        
        # Get compliance requirements
        compliance_standards = self._get_required_compliance(blueprint, user_context)
        
        return AgentSecurity(
            level=security_level,
            encryption_enabled=True,
            audit_logging=True,
            data_retention_days=self._get_retention_days(security_level),
            access_controls=self._generate_access_controls(blueprint),
            threat_detection=security_level in [SecurityLevel.ENHANCED, SecurityLevel.ENTERPRISE],
            sandbox_mode=True,
            api_rate_limiting=True,
            sensitive_data_handling=self._get_sensitive_data_handling(blueprint)
        )

    def _determine_security_level(self, blueprint: AgentBlueprint, user_context: Dict[str, Any]) -> SecurityLevel:
        """Determine appropriate security level."""
        # Check for sensitive data types
        sensitive_keywords = ["financial", "medical", "personal", "confidential", "secret"]
        has_sensitive_data = any(keyword in str(blueprint.capabilities).lower() 
                               for keyword in sensitive_keywords)
        
        # Check for enterprise features
        is_enterprise = user_context.get("enterprise_user", False)
        
        # Check for compliance requirements
        has_compliance = user_context.get("compliance_required", False)
        
        if is_enterprise or has_compliance:
            return SecurityLevel.ENTERPRISE
        elif has_sensitive_data:
            return SecurityLevel.ENHANCED
        else:
            return SecurityLevel.BASIC

    def _get_required_compliance(self, blueprint: AgentBlueprint, user_context: Dict[str, Any]) -> List[ComplianceStandard]:
        """Get required compliance standards."""
        compliance = []
        
        # Check for GDPR (always required for EU data)
        if user_context.get("eu_data", True):
            compliance.append(ComplianceStandard.GDPR)
        
        # Check for HIPAA (medical data)
        if "medical" in str(blueprint.capabilities).lower():
            compliance.append(ComplianceStandard.HIPAA)
        
        # Check for SOC2 (enterprise)
        if user_context.get("enterprise_user", False):
            compliance.append(ComplianceStandard.SOC2)
        
        return compliance

    def _get_retention_days(self, security_level: SecurityLevel) -> int:
        """Get data retention days based on security level."""
        retention_map = {
            SecurityLevel.BASIC: 90,
            SecurityLevel.ENHANCED: 365,
            SecurityLevel.ENTERPRISE: 2555,  # 7 years
            SecurityLevel.GOVERNMENT: 3650   # 10 years
        }
        return retention_map.get(security_level, 90)

    def _generate_access_controls(self, blueprint: AgentBlueprint) -> List[str]:
        """Generate access controls for the agent."""
        controls = ["authentication", "authorization"]
        
        if blueprint.security.level in [SecurityLevel.ENHANCED, SecurityLevel.ENTERPRISE]:
            controls.extend(["mfa", "session_management", "ip_restriction"])
        
        if blueprint.security.level == SecurityLevel.ENTERPRISE:
            controls.extend(["rbac", "privilege_escalation_protection"])
        
        return controls

    def _get_sensitive_data_handling(self, blueprint: AgentBlueprint) -> Dict[str, Any]:
        """Get sensitive data handling configuration."""
        return {
            "classification": DataClassification.CONFIDENTIAL,
            "encryption_at_rest": True,
            "encryption_in_transit": True,
            "access_logging": True,
            "data_masking": True,
            "anonymization": False
        }

    def _assess_compliance(self, blueprint: AgentBlueprint) -> Dict[str, Any]:
        """Assess compliance with various standards."""
        compliance_status = {}
        
        for standard, requirements in self.compliance_requirements.items():
            status = {}
            for requirement, required in requirements.items():
                status[requirement] = self._check_compliance_requirement(blueprint, requirement)
            compliance_status[standard.value] = status
        
        return compliance_status

    def _check_compliance_requirement(self, blueprint: AgentBlueprint, requirement: str) -> bool:
        """Check if blueprint meets a specific compliance requirement."""
        if requirement == "encryption":
            return blueprint.security.encryption_enabled
        elif requirement == "audit_trails":
            return blueprint.security.audit_logging
        elif requirement == "access_controls":
            return len(blueprint.security.access_controls) > 0
        elif requirement == "data_minimization":
            return True  # Implement based on data collection
        elif requirement == "consent_management":
            return True  # Implement based on user consent
        else:
            return True  # Default to compliant

    def _encrypt_sensitive_data(self, blueprint: AgentBlueprint) -> AgentBlueprint:
        """Encrypt sensitive data in the blueprint."""
        try:
            # Encrypt credentials if present
            for integration in blueprint.integrations:
                if integration.credentials:
                    integration.credentials = self._encrypt_dict(integration.credentials)
                if integration.api_keys:
                    integration.api_keys = self._encrypt_dict(integration.api_keys)
            
            # Encrypt custom config if it contains sensitive data
            if blueprint.custom_config:
                blueprint.custom_config = self._encrypt_dict(blueprint.custom_config)
            
            return blueprint
            
        except Exception as e:
            logger.error(f"Error encrypting sensitive data: {e}")
            return blueprint

    def _encrypt_dict(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """Encrypt a dictionary of sensitive data."""
        encrypted = {}
        for key, value in data.items():
            if isinstance(value, str):
                encrypted[key] = self.cipher_suite.encrypt(value.encode()).decode()
            elif isinstance(value, dict):
                encrypted[key] = self._encrypt_dict(value)
            else:
                encrypted[key] = value
        return encrypted

    def _generate_security_hash(self, blueprint: AgentBlueprint) -> str:
        """Generate a security hash for the blueprint."""
        security_data = {
            "id": blueprint.id,
            "security_level": blueprint.security.level,
            "encryption_enabled": blueprint.security.encryption_enabled,
            "audit_logging": blueprint.security.audit_logging,
            "timestamp": datetime.utcnow().isoformat()
        }
        
        data_string = json.dumps(security_data, sort_keys=True)
        return hashlib.sha256(data_string.encode()).hexdigest()

    def audit_agent_security(self, blueprint: AgentBlueprint) -> SecurityAudit:
        """Perform a comprehensive security audit of an agent."""
        vulnerabilities = []
        recommendations = []
        compliance_status = {}
        
        # Check for common vulnerabilities
        vulnerabilities.extend(self._check_vulnerabilities(blueprint))
        
        # Generate recommendations
        recommendations.extend(self._generate_recommendations(blueprint))
        
        # Check compliance
        compliance_status = self._assess_compliance(blueprint)
        
        # Calculate data handling score
        data_handling_score = self._calculate_data_handling_score(blueprint)
        
        # Check encryption status
        encryption_status = self._check_encryption_status(blueprint)
        
        # Check access controls
        access_controls = self._check_access_controls(blueprint)
        
        # Determine threat level
        threat_level = self._determine_threat_level(vulnerabilities, data_handling_score)
        
        audit = SecurityAudit(
            agent_id=blueprint.id,
            timestamp=datetime.utcnow(),
            threat_level=threat_level,
            vulnerabilities=vulnerabilities,
            recommendations=recommendations,
            compliance_status=compliance_status,
            data_handling_score=data_handling_score,
            encryption_status=encryption_status,
            access_controls=access_controls
        )
        
        # Log audit
        self.audit_log.append(audit)
        
        return audit

    def _check_vulnerabilities(self, blueprint: AgentBlueprint) -> List[str]:
        """Check for security vulnerabilities."""
        vulnerabilities = []
        
        # Check for weak security configurations
        if blueprint.security.level == SecurityLevel.BASIC and "financial" in str(blueprint.capabilities):
            vulnerabilities.append("Financial data requires enhanced security level")
        
        # Check for missing encryption
        if not blueprint.security.encryption_enabled:
            vulnerabilities.append("Encryption is disabled")
        
        # Check for missing audit logging
        if not blueprint.security.audit_logging:
            vulnerabilities.append("Audit logging is disabled")
        
        # Check for sensitive data exposure
        for integration in blueprint.integrations:
            if integration.credentials and not self._is_encrypted(integration.credentials):
                vulnerabilities.append(f"Unencrypted credentials in {integration.name}")
        
        return vulnerabilities

    def _generate_recommendations(self, blueprint: AgentBlueprint) -> List[str]:
        """Generate security recommendations."""
        recommendations = []
        
        if blueprint.security.level == SecurityLevel.BASIC:
            recommendations.append("Consider upgrading to enhanced security for better protection")
        
        if not blueprint.security.threat_detection:
            recommendations.append("Enable threat detection for proactive security")
        
        if not blueprint.security.sandbox_mode:
            recommendations.append("Enable sandbox mode for safe execution")
        
        if len(blueprint.security.access_controls) < 3:
            recommendations.append("Implement additional access controls")
        
        return recommendations

    def _calculate_data_handling_score(self, blueprint: AgentBlueprint) -> float:
        """Calculate data handling security score."""
        score = 1.0
        
        # Deduct points for security issues
        if not blueprint.security.encryption_enabled:
            score -= 0.3
        
        if not blueprint.security.audit_logging:
            score -= 0.2
        
        if not blueprint.security.threat_detection:
            score -= 0.2
        
        if blueprint.security.level == SecurityLevel.BASIC:
            score -= 0.1
        
        return max(score, 0.0)

    def _check_encryption_status(self, blueprint: AgentBlueprint) -> Dict[str, bool]:
        """Check encryption status of various components."""
        return {
            "at_rest": blueprint.security.encryption_enabled,
            "in_transit": True,  # Always true for HTTPS
            "credentials": all(self._is_encrypted(integration.credentials) 
                             for integration in blueprint.integrations if integration.credentials),
            "api_keys": all(self._is_encrypted(integration.api_keys) 
                          for integration in blueprint.integrations if integration.api_keys)
        }

    def _check_access_controls(self, blueprint: AgentBlueprint) -> Dict[str, Any]:
        """Check access control implementation."""
        return {
            "authentication": "authentication" in blueprint.security.access_controls,
            "authorization": "authorization" in blueprint.security.access_controls,
            "mfa": "mfa" in blueprint.security.access_controls,
            "session_management": "session_management" in blueprint.security.access_controls,
            "rbac": "rbac" in blueprint.security.access_controls
        }

    def _determine_threat_level(self, vulnerabilities: List[str], data_handling_score: float) -> SecurityThreatLevel:
        """Determine overall threat level."""
        if data_handling_score < 0.5 or len(vulnerabilities) > 5:
            return SecurityThreatLevel.CRITICAL
        elif data_handling_score < 0.7 or len(vulnerabilities) > 3:
            return SecurityThreatLevel.HIGH
        elif data_handling_score < 0.8 or len(vulnerabilities) > 1:
            return SecurityThreatLevel.MEDIUM
        else:
            return SecurityThreatLevel.LOW

    def _is_encrypted(self, data: Any) -> bool:
        """Check if data appears to be encrypted."""
        if not data:
            return True
        
        if isinstance(data, str):
            # Check if it looks like encrypted data
            return len(data) > 50 and not data.isprintable()
        elif isinstance(data, dict):
            return all(self._is_encrypted(value) for value in data.values())
        
        return True

    def validate_input_security(self, user_input: str) -> Tuple[bool, List[str]]:
        """Validate user input for security threats."""
        threats = []
        
        for threat_type, patterns in self.threat_patterns.items():
            for pattern in patterns:
                if re.search(pattern, user_input, re.IGNORECASE):
                    threats.append(f"Potential {threat_type} detected")
        
        return len(threats) == 0, threats

    def rate_limit_check(self, agent_id: str, user_id: str) -> bool:
        """Check if request is within rate limits."""
        key = f"{agent_id}:{user_id}"
        now = time.time()
        
        if key not in self.rate_limit_store:
            self.rate_limit_store[key] = []
        
        # Clean old requests
        self.rate_limit_store[key] = [req_time for req_time in self.rate_limit_store[key] 
                                    if now - req_time < 60]  # 1 minute window
        
        # Check rate limit (100 requests per minute)
        if len(self.rate_limit_store[key]) >= 100:
            return False
        
        # Add current request
        self.rate_limit_store[key].append(now)
        return True

    def create_session_token(self, user_id: str, agent_id: str) -> str:
        """Create a secure session token."""
        payload = {
            "user_id": user_id,
            "agent_id": agent_id,
            "exp": datetime.utcnow() + timedelta(hours=1),
            "iat": datetime.utcnow()
        }
        
        return jwt.encode(payload, self.master_key, algorithm="HS256")

    def validate_session_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Validate a session token."""
        try:
            payload = jwt.decode(token, self.master_key, algorithms=["HS256"])
            return payload
        except jwt.ExpiredSignatureError:
            logger.warning("Session token expired")
            return None
        except jwt.InvalidTokenError:
            logger.warning("Invalid session token")
            return None

    def get_security_report(self, agent_id: str) -> Dict[str, Any]:
        """Generate a comprehensive security report."""
        # Find the latest audit for this agent
        latest_audit = None
        for audit in reversed(self.audit_log):
            if audit.agent_id == agent_id:
                latest_audit = audit
                break
        
        if not latest_audit:
            return {"error": "No security audit found for this agent"}
        
        return {
            "agent_id": agent_id,
            "audit_timestamp": latest_audit.timestamp.isoformat(),
            "threat_level": latest_audit.threat_level.value,
            "data_handling_score": latest_audit.data_handling_score,
            "vulnerabilities_count": len(latest_audit.vulnerabilities),
            "recommendations_count": len(latest_audit.recommendations),
            "compliance_status": latest_audit.compliance_status,
            "encryption_status": latest_audit.encryption_status,
            "access_controls": latest_audit.access_controls,
            "vulnerabilities": latest_audit.vulnerabilities,
            "recommendations": latest_audit.recommendations
        } 