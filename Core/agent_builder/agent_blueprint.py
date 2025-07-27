"""Advanced Agent Blueprint System - Defines the structure for AI-generated agents."""

from typing import Dict, List, Optional, Any, Union
from enum import Enum
from pydantic import BaseModel, Field, validator
from datetime import datetime
import json
import hashlib
import uuid

class AgentType(str, Enum):
    """Types of agents that can be created."""
    PERSONAL_ASSISTANT = "personal_assistant"
    EMAIL_MANAGER = "email_manager"
    CALENDAR_ASSISTANT = "calendar_assistant"
    CUSTOMER_SERVICE = "customer_service"
    DATA_ANALYST = "data_analyst"
    CONTENT_CREATOR = "content_creator"
    PROJECT_MANAGER = "project_manager"
    RESEARCH_ASSISTANT = "research_assistant"
    SOCIAL_MEDIA_MANAGER = "social_media_manager"
    FINANCIAL_ADVISOR = "financial_advisor"
    CUSTOM = "custom"

class IntegrationType(str, Enum):
    """Types of integrations available."""
    EMAIL = "email"
    CALENDAR = "calendar"
    CRM = "crm"
    SOCIAL_MEDIA = "social_media"
    FILE_STORAGE = "file_storage"
    DATABASE = "database"
    API = "api"
    WEBHOOK = "webhook"
    VOICE = "voice"
    CHAT = "chat"

class SecurityLevel(str, Enum):
    """Security levels for agents."""
    BASIC = "basic"
    ENHANCED = "enhanced"
    ENTERPRISE = "enterprise"
    GOVERNMENT = "government"

class TaskPriority(str, Enum):
    """Task priority levels."""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"

class AgentTask(BaseModel):
    """Individual task within an agent."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    priority: TaskPriority = TaskPriority.MEDIUM
    triggers: List[str] = Field(default_factory=list)
    actions: List[Dict[str, Any]] = Field(default_factory=list)
    conditions: List[Dict[str, Any]] = Field(default_factory=list)
    estimated_duration: Optional[int] = None  # in minutes
    dependencies: List[str] = Field(default_factory=list)
    retry_policy: Dict[str, Any] = Field(default_factory=dict)
    success_criteria: List[str] = Field(default_factory=list)

class AgentIntegration(BaseModel):
    """Integration configuration for an agent."""
    type: IntegrationType
    name: str
    config: Dict[str, Any] = Field(default_factory=dict)
    credentials: Optional[Dict[str, Any]] = None
    permissions: List[str] = Field(default_factory=list)
    rate_limits: Optional[Dict[str, Any]] = None
    webhook_url: Optional[str] = None
    api_keys: Optional[Dict[str, str]] = None
    oauth_config: Optional[Dict[str, Any]] = None

class AgentSecurity(BaseModel):
    """Security configuration for an agent."""
    level: SecurityLevel = SecurityLevel.BASIC
    encryption_enabled: bool = True
    audit_logging: bool = True
    data_retention_days: int = 90
    access_controls: List[str] = Field(default_factory=list)
    threat_detection: bool = False
    sandbox_mode: bool = True
    api_rate_limiting: bool = True
    sensitive_data_handling: Dict[str, Any] = Field(default_factory=dict)

class AgentBlueprint(BaseModel):
    """Complete blueprint for an AI-generated agent."""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: str
    type: AgentType
    version: str = "1.0.0"
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    
    # Core configuration
    capabilities: List[str] = Field(default_factory=list)
    skills: List[str] = Field(default_factory=list)
    personality: Dict[str, Any] = Field(default_factory=dict)
    communication_style: Dict[str, Any] = Field(default_factory=dict)
    
    # Tasks and workflows
    tasks: List[AgentTask] = Field(default_factory=list)
    workflows: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Integrations
    integrations: List[AgentIntegration] = Field(default_factory=list)
    required_apis: List[str] = Field(default_factory=list)
    
    # Security and compliance
    security: AgentSecurity = Field(default_factory=AgentSecurity)
    compliance: List[str] = Field(default_factory=list)
    
    # Performance and monitoring
    performance_metrics: List[str] = Field(default_factory=list)
    monitoring_config: Dict[str, Any] = Field(default_factory=dict)
    
    # Advanced features
    learning_capabilities: Dict[str, Any] = Field(default_factory=dict)
    adaptation_rules: List[Dict[str, Any]] = Field(default_factory=list)
    fallback_strategies: List[Dict[str, Any]] = Field(default_factory=list)
    
    # Metadata
    tags: List[str] = Field(default_factory=list)
    category: Optional[str] = None
    difficulty_level: Optional[str] = None
    estimated_cost: Optional[float] = None
    
    # Privacy and data handling
    data_privacy: Dict[str, Any] = Field(default_factory=dict)
    data_sources: List[str] = Field(default_factory=list)
    data_destinations: List[str] = Field(default_factory=list)
    
    # Custom fields
    custom_config: Dict[str, Any] = Field(default_factory=dict)
    metadata: Dict[str, Any] = Field(default_factory=dict)

    @validator('id')
    def validate_id(cls, v):
        """Ensure ID is unique and valid."""
        if not v or len(v) < 10:
            return str(uuid.uuid4())
        return v

    def generate_hash(self) -> str:
        """Generate a unique hash for this blueprint."""
        content = json.dumps(self.dict(), sort_keys=True, default=str)
        return hashlib.sha256(content.encode()).hexdigest()

    def validate_integrations(self) -> List[str]:
        """Validate all integrations and return any issues."""
        issues = []
        for integration in self.integrations:
            if not integration.name:
                issues.append(f"Integration missing name: {integration.type}")
            if integration.type == IntegrationType.API and not integration.api_keys:
                issues.append(f"API integration missing keys: {integration.name}")
        return issues

    def get_estimated_complexity(self) -> str:
        """Calculate estimated complexity based on tasks and integrations."""
        task_count = len(self.tasks)
        integration_count = len(self.integrations)
        
        if task_count > 20 or integration_count > 10:
            return "high"
        elif task_count > 10 or integration_count > 5:
            return "medium"
        else:
            return "low"

    def to_deployment_config(self) -> Dict[str, Any]:
        """Convert blueprint to deployment configuration."""
        return {
            "agent_id": self.id,
            "name": self.name,
            "type": self.type.value,
            "config": {
                "tasks": [task.dict() for task in self.tasks],
                "integrations": [integration.dict() for integration in self.integrations],
                "security": self.security.dict(),
                "monitoring": self.monitoring_config,
                "custom": self.custom_config
            },
            "metadata": {
                "version": self.version,
                "created_at": self.created_at.isoformat(),
                "complexity": self.get_estimated_complexity(),
                "hash": self.generate_hash()
            }
        }

    class Config:
        """Pydantic configuration."""
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }
        schema_extra = {
            "example": {
                "name": "Email Assistant Pro",
                "description": "Advanced email management agent",
                "type": "email_manager",
                "capabilities": ["email_processing", "smart_replies", "scheduling"],
                "security": {"level": "enhanced", "encryption_enabled": True}
            }
        } 