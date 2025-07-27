"""
Simplified External Agent Builder API Routes

Public API endpoints for the Agent Builder product to interact with
Daena Company's autonomous AI infrastructure.
"""

from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Dict, List, Optional, Any
from pydantic import BaseModel
import uuid
from datetime import datetime
import json

router = APIRouter(prefix="/api/v1/external", tags=["external-agent-builder"])

# Security
security = HTTPBearer()

# Pydantic models for API
class AgentCreateRequest(BaseModel):
    user_id: str
    name: str
    description: str
    agent_type: str
    capabilities: List[str]
    integrations: List[str]
    triggers: List[str]
    actions: List[str]
    llm_model: str
    voice_enabled: bool
    custom_prompt: Optional[str] = None

class AgentCreateResponse(BaseModel):
    agent_id: str
    status: str
    message: str
    estimated_cost: float
    deployment_time: int

class AgentTemplate(BaseModel):
    id: str
    name: str
    description: str
    category: str
    complexity: str
    estimated_cost: float
    features: List[str]
    integrations: List[str]

class IntegrationInfo(BaseModel):
    id: str
    name: str
    description: str
    category: str
    auth_type: str
    required_fields: List[str]
    icon_url: str

class LLMModel(BaseModel):
    id: str
    name: str
    provider: str
    capabilities: List[str]
    cost_per_token: float
    max_tokens: int

class AgentAnalysisRequest(BaseModel):
    description: str

class AgentAnalysisResponse(BaseModel):
    suggested_type: str
    suggested_capabilities: List[str]
    suggested_integrations: List[str]
    complexity: str
    estimated_cost: float
    confidence: float

class AgentValidationRequest(BaseModel):
    name: str
    description: str
    agent_type: str
    capabilities: List[str]
    integrations: List[str]
    triggers: List[str]
    actions: List[str]
    llm_model: str
    voice_enabled: bool
    custom_prompt: Optional[str] = None

class AgentValidationResponse(BaseModel):
    valid: bool
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]

# Predefined agent templates
AGENT_TEMPLATES = [
    {
        "id": "email_assistant",
        "name": "Email Assistant",
        "description": "Automatically reads, categorizes, and responds to emails",
        "category": "communication",
        "complexity": "medium",
        "estimated_cost": 0.05,
        "features": ["email_reading", "email_responding", "categorization", "scheduling"],
        "integrations": ["gmail", "outlook", "calendar"]
    },
    {
        "id": "customer_support",
        "name": "Customer Support Agent",
        "description": "Handles customer inquiries and support tickets",
        "category": "support",
        "complexity": "high",
        "estimated_cost": 0.08,
        "features": ["ticket_management", "knowledge_base", "escalation", "analytics"],
        "integrations": ["zendesk", "intercom", "slack", "email"]
    },
    {
        "id": "social_media_manager",
        "name": "Social Media Manager",
        "description": "Manages social media accounts and content",
        "category": "marketing",
        "complexity": "medium",
        "estimated_cost": 0.06,
        "features": ["content_creation", "scheduling", "engagement", "analytics"],
        "integrations": ["twitter", "linkedin", "facebook", "instagram"]
    },
    {
        "id": "data_analyst",
        "name": "Data Analyst",
        "description": "Analyzes data and generates insights",
        "category": "analytics",
        "complexity": "high",
        "estimated_cost": 0.10,
        "features": ["data_processing", "visualization", "reporting", "predictions"],
        "integrations": ["google_sheets", "airtable", "database", "api"]
    },
    {
        "id": "calendar_assistant",
        "name": "Calendar Assistant",
        "description": "Manages calendar and scheduling",
        "category": "productivity",
        "complexity": "low",
        "estimated_cost": 0.03,
        "features": ["scheduling", "reminders", "meeting_coordination", "availability"],
        "integrations": ["google_calendar", "outlook", "zoom", "teams"]
    }
]

# Available integrations
AVAILABLE_INTEGRATIONS = [
    {
        "id": "gmail",
        "name": "Gmail",
        "description": "Email service integration",
        "category": "communication",
        "auth_type": "oauth2",
        "required_fields": ["client_id", "client_secret"],
        "icon_url": "/icons/gmail.png"
    },
    {
        "id": "slack",
        "name": "Slack",
        "description": "Team communication platform",
        "category": "communication",
        "auth_type": "oauth2",
        "required_fields": ["client_id", "client_secret"],
        "icon_url": "/icons/slack.png"
    },
    {
        "id": "notion",
        "name": "Notion",
        "description": "Workspace and documentation",
        "category": "productivity",
        "auth_type": "api_key",
        "required_fields": ["api_key"],
        "icon_url": "/icons/notion.png"
    },
    {
        "id": "stripe",
        "name": "Stripe",
        "description": "Payment processing",
        "category": "finance",
        "auth_type": "api_key",
        "required_fields": ["secret_key", "publishable_key"],
        "icon_url": "/icons/stripe.png"
    },
    {
        "id": "openai",
        "name": "OpenAI",
        "description": "AI model provider",
        "category": "ai",
        "auth_type": "api_key",
        "required_fields": ["api_key"],
        "icon_url": "/icons/openai.png"
    }
]

# Available LLM models
AVAILABLE_LLM_MODELS = [
    {
        "id": "gpt-4",
        "name": "GPT-4",
        "provider": "OpenAI",
        "capabilities": ["text_generation", "code_generation", "analysis"],
        "cost_per_token": 0.00003,
        "max_tokens": 8192
    },
    {
        "id": "gpt-3.5-turbo",
        "name": "GPT-3.5 Turbo",
        "provider": "OpenAI",
        "capabilities": ["text_generation", "conversation"],
        "cost_per_token": 0.000002,
        "max_tokens": 4096
    },
    {
        "id": "claude-3-opus",
        "name": "Claude 3 Opus",
        "provider": "Anthropic",
        "capabilities": ["text_generation", "analysis", "reasoning"],
        "cost_per_token": 0.000015,
        "max_tokens": 200000
    },
    {
        "id": "claude-3-sonnet",
        "name": "Claude 3 Sonnet",
        "provider": "Anthropic",
        "capabilities": ["text_generation", "analysis"],
        "cost_per_token": 0.000003,
        "max_tokens": 200000
    }
]

# Simple API key verification (for demo purposes)
def verify_api_key(api_key: str) -> bool:
    """Simple API key verification"""
    # In production, this would check against a database
    valid_keys = ["demo-key-123", "test-key-456", "daena-external-api"]
    return api_key in valid_keys

@router.get("/test")
async def test_endpoint():
    """
    Simple test endpoint to verify the API is working
    """
    return {"message": "External Agent Builder API is working!", "status": "success"}

@router.get("/templates/list", response_model=List[AgentTemplate])
async def get_agent_templates(category: Optional[str] = None):
    """
    Get available agent templates
    """
    if category:
        return [template for template in AGENT_TEMPLATES if template["category"] == category]
    return AGENT_TEMPLATES

@router.get("/integrations/available", response_model=List[IntegrationInfo])
async def get_available_integrations():
    """
    Get available integrations
    """
    return AVAILABLE_INTEGRATIONS

@router.get("/llm/models", response_model=List[LLMModel])
async def get_llm_models():
    """
    Get available LLM models
    """
    return AVAILABLE_LLM_MODELS

@router.post("/agents/create", response_model=AgentCreateResponse)
async def create_agent(
    request: AgentCreateRequest,
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Create a new agent using Daena Company's infrastructure
    """
    # Verify API key
    if not verify_api_key(credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    try:
        # Generate unique agent ID
        agent_id = str(uuid.uuid4())
        
        # Calculate estimated cost (simplified)
        estimated_cost = 0.05  # Base cost
        if request.voice_enabled:
            estimated_cost += 0.02
        if len(request.integrations) > 0:
            estimated_cost += len(request.integrations) * 0.01
        
        return AgentCreateResponse(
            agent_id=agent_id,
            status="created",
            message="Agent created successfully",
            estimated_cost=estimated_cost,
            deployment_time=5  # seconds
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create agent: {str(e)}"
        )

@router.get("/agents/{agent_id}/status")
async def get_agent_status(
    agent_id: str,
    api_credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get the status of a deployed agent
    """
    if not verify_api_key(api_credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    return {
        "agent_id": agent_id,
        "status": "active",
        "name": "Sample Agent",
        "description": "A sample agent created via API",
        "created_at": datetime.utcnow().isoformat(),
        "last_activity": datetime.utcnow().isoformat(),
        "total_interactions": 0,
        "success_rate": 0.95
    }

@router.post("/agents/analyze", response_model=AgentAnalysisResponse)
async def analyze_agent_request(
    request: AgentAnalysisRequest,
    api_credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Analyze a natural language agent request
    """
    if not verify_api_key(api_credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    try:
        # Simple analysis based on keywords
        description = request.description.lower()
        
        if "email" in description:
            suggested_type = "email_assistant"
            suggested_capabilities = ["email_reading", "email_responding"]
            suggested_integrations = ["gmail", "outlook"]
        elif "support" in description or "customer" in description:
            suggested_type = "customer_support"
            suggested_capabilities = ["ticket_management", "knowledge_base"]
            suggested_integrations = ["zendesk", "slack"]
        elif "social" in description or "media" in description:
            suggested_type = "social_media_manager"
            suggested_capabilities = ["content_creation", "scheduling"]
            suggested_integrations = ["twitter", "linkedin"]
        else:
            suggested_type = "general_assistant"
            suggested_capabilities = ["text_processing", "api_integration"]
            suggested_integrations = ["email", "calendar"]
        
        return AgentAnalysisResponse(
            suggested_type=suggested_type,
            suggested_capabilities=suggested_capabilities,
            suggested_integrations=suggested_integrations,
            complexity="medium",
            estimated_cost=0.05,
            confidence=0.85
        )
        
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to analyze request: {str(e)}"
        )

@router.post("/agents/validate", response_model=AgentValidationResponse)
async def validate_agent_config(
    request: AgentValidationRequest,
    api_credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Validate an agent configuration
    """
    if not verify_api_key(api_credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    errors = []
    warnings = []
    suggestions = []
    
    # Validate required fields
    if not request.name or len(request.name.strip()) < 3:
        errors.append("Agent name must be at least 3 characters long")
    
    if not request.description or len(request.description.strip()) < 10:
        errors.append("Agent description must be at least 10 characters long")
    
    if not request.capabilities:
        errors.append("At least one capability must be specified")
    
    # Validate LLM model
    valid_models = [model["id"] for model in AVAILABLE_LLM_MODELS]
    if request.llm_model not in valid_models:
        errors.append(f"Invalid LLM model. Available models: {', '.join(valid_models)}")
    
    # Validate integrations
    valid_integrations = [integration["id"] for integration in AVAILABLE_INTEGRATIONS]
    for integration in request.integrations:
        if integration not in valid_integrations:
            errors.append(f"Invalid integration: {integration}")
    
    # Warnings and suggestions
    if len(request.capabilities) > 5:
        warnings.append("Too many capabilities may affect performance")
        suggestions.append("Consider focusing on core capabilities first")
    
    if request.voice_enabled and "speech_recognition" not in request.capabilities:
        suggestions.append("Consider adding speech recognition capability for voice features")
    
    return AgentValidationResponse(
        valid=len(errors) == 0,
        errors=errors,
        warnings=warnings,
        suggestions=suggestions
    )

@router.get("/billing/usage")
async def get_usage_metrics(
    user_id: str,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    api_credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """
    Get usage metrics for billing
    """
    if not verify_api_key(api_credentials.credentials):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key"
        )
    
    # Mock usage data
    return {
        "user_id": user_id,
        "period": {
            "start_date": start_date or "2024-01-01",
            "end_date": end_date or "2024-12-31"
        },
        "usage": {
            "total_agents": 3,
            "total_interactions": 1250,
            "total_cost": 0.75,
            "success_rate": 0.95
        },
        "breakdown": {
            "agent_creation": 0.15,
            "api_calls": 0.45,
            "integrations": 0.15
        }
    } 