from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session
from backend.database import get_db, Agent as DBAgent
import json
import uuid
from datetime import datetime

router = APIRouter()

# Pydantic Models
class AgentTemplate(BaseModel):
    id: str
    name: str
    description: str
    category: str
    default_config: Dict[str, Any]
    customization_questions: List[Dict[str, Any]]
    integrations: List[Dict[str, Any]]
    visual_flow: List[Dict[str, Any]]
    demo_data: Dict[str, Any]

class CustomizationRequest(BaseModel):
    template_id: str
    answers: Dict[str, Any]

class DemoRequest(BaseModel):
    template_id: str
    config: Dict[str, Any]
    customizations: Dict[str, Any]

class AgentCreateRequest(BaseModel):
    template_id: str
    name: str
    description: str
    config: Dict[str, Any]
    customizations: Dict[str, Any]
    integrations: List[str]

# Predefined Agent Templates
AGENT_TEMPLATES = {
    "email-manager": {
        "id": "email-manager",
        "name": "Email Manager",
        "description": "Automatically read, analyze, and respond to emails",
        "category": "Communication",
        "default_config": {
            "name": "Email Manager",
            "description": "AI-powered email assistant",
            "capabilities": ["email reading", "response generation", "priority sorting"],
            "integrations": ["gmail", "outlook"],
            "automation_level": "semi-auto",
            "response_style": "professional",
            "industry": "general",
            "language": "en",
            "timezone": "UTC",
            "working_hours": "9-5",
            "special_instructions": ""
        },
        "customization_questions": [
            {
                "id": "response-style",
                "type": "select",
                "question": "How formal should email responses be?",
                "options": ["Very formal", "Professional", "Casual", "Friendly"],
                "required": True,
                "field": "response_style",
                "help_text": "This affects the tone of all generated responses"
            },
            {
                "id": "industry",
                "type": "text",
                "question": "What industry do you work in?",
                "placeholder": "e.g., Technology, Healthcare, Finance",
                "required": False,
                "field": "industry",
                "help_text": "Helps customize responses for your specific field"
            },
            {
                "id": "automation-level",
                "type": "radio",
                "question": "How much automation do you want?",
                "options": ["Show me responses first", "Send automatically for simple emails", "Fully automatic"],
                "required": True,
                "field": "automation_level",
                "help_text": "Controls how much human oversight is required"
            },
            {
                "id": "working-hours",
                "type": "text",
                "question": "When should the agent be active?",
                "placeholder": "e.g., 9 AM - 6 PM, Monday-Friday",
                "required": False,
                "field": "working_hours",
                "help_text": "Agent will only process emails during these hours"
            },
            {
                "id": "special-instructions",
                "type": "text",
                "question": "Any special instructions for the agent?",
                "placeholder": "e.g., Always mention our company values, Never discuss pricing",
                "required": False,
                "field": "special_instructions",
                "help_text": "Custom rules or guidelines for the agent to follow"
            }
        ],
        "integrations": [
            {
                "id": "gmail",
                "name": "Gmail",
                "type": "email",
                "description": "Connect to your Gmail account",
                "setup_required": True,
                "cost": 0,
                "benefits": ["Direct email access", "Real-time notifications", "Calendar integration"]
            },
            {
                "id": "outlook",
                "name": "Outlook",
                "type": "email",
                "description": "Connect to your Outlook account",
                "setup_required": True,
                "cost": 0,
                "benefits": ["Enterprise email support", "Microsoft 365 integration", "Advanced security"]
            }
        ],
        "visual_flow": [
            {
                "id": "email-trigger",
                "type": "trigger",
                "name": "New Email",
                "description": "Detects incoming emails",
                "position": {"x": 100, "y": 100},
                "connections": ["email-analyzer"],
                "config": {"frequency": "realtime", "filters": []}
            },
            {
                "id": "email-analyzer",
                "type": "processor",
                "name": "Analyze Content",
                "description": "Understands email intent and priority",
                "position": {"x": 300, "y": 100},
                "connections": ["response-generator", "priority-sorter"],
                "config": {"model": "gpt-4", "analysis": ["sentiment", "intent", "urgency"]}
            },
            {
                "id": "response-generator",
                "type": "processor",
                "name": "Generate Response",
                "description": "Creates appropriate email replies",
                "position": {"x": 500, "y": 100},
                "connections": ["response-review"],
                "config": {"style": "professional", "tone": "friendly"}
            },
            {
                "id": "response-review",
                "type": "condition",
                "name": "Review Required?",
                "description": "Decides if human review is needed",
                "position": {"x": 700, "y": 100},
                "connections": ["send-email", "human-review"],
                "config": {"auto_send": False, "confidence_threshold": 0.8}
            },
            {
                "id": "send-email",
                "type": "action",
                "name": "Send Response",
                "description": "Delivers the email reply",
                "position": {"x": 900, "y": 50},
                "connections": [],
                "config": {"method": "smtp", "tracking": True}
            },
            {
                "id": "human-review",
                "type": "action",
                "name": "Human Review",
                "description": "Sends to human for approval",
                "position": {"x": 900, "y": 150},
                "connections": [],
                "config": {"notification": "email", "approval": "required"}
            }
        ],
        "demo_data": {
            "sample_email": {
                "from": "john.doe@company.com",
                "subject": "Meeting Request for Next Week",
                "body": "Hi there, I would like to schedule a meeting to discuss our project collaboration. Are you available next Tuesday at 2 PM?",
                "timestamp": "2024-01-15T10:30:00Z"
            },
            "generated_response": {
                "subject": "Re: Meeting Request for Next Week",
                "body": "Hi John, Thank you for reaching out! I would be happy to meet with you next Tuesday at 2 PM to discuss our project collaboration. I have that time slot available and it works perfectly for me. I'll send you a calendar invitation shortly. Looking forward to our discussion! Best regards, [Your Name]",
                "confidence": 0.92,
                "processing_time": "2.3s"
            }
        }
    },
    "calendar-assistant": {
        "id": "calendar-assistant",
        "name": "Calendar Assistant",
        "description": "Manage your schedule and coordinate meetings",
        "category": "Productivity",
        "default_config": {
            "name": "Calendar Assistant",
            "description": "AI-powered calendar management",
            "capabilities": ["meeting scheduling", "conflict resolution", "reminder management"],
            "integrations": ["google-calendar", "outlook-calendar"],
            "automation_level": "semi-auto",
            "response_style": "professional",
            "industry": "general",
            "language": "en",
            "timezone": "UTC",
            "working_hours": "9-5",
            "special_instructions": ""
        },
        "customization_questions": [
            {
                "id": "meeting-duration",
                "type": "select",
                "question": "What's your default meeting duration?",
                "options": ["30 minutes", "45 minutes", "1 hour", "Custom"],
                "required": True,
                "field": "working_hours",
                "help_text": "Default duration for new meetings"
            }
        ],
        "integrations": [
            {
                "id": "google-calendar",
                "name": "Google Calendar",
                "type": "calendar",
                "description": "Connect to Google Calendar",
                "setup_required": True,
                "cost": 0,
                "benefits": ["Real-time sync", "Meeting suggestions", "Travel time calculation"]
            }
        ],
        "visual_flow": [],
        "demo_data": {}
    },
    "chat-support": {
        "id": "chat-support",
        "name": "Chat Support Agent",
        "description": "Provide customer support through chat interfaces",
        "category": "Customer Service",
        "default_config": {
            "name": "Chat Support Agent",
            "description": "AI-powered customer support",
            "capabilities": ["chat responses", "ticket creation", "escalation"],
            "integrations": ["slack", "discord", "website"],
            "automation_level": "semi-auto",
            "response_style": "friendly",
            "industry": "general",
            "language": "en",
            "timezone": "UTC",
            "working_hours": "24/7",
            "special_instructions": ""
        },
        "customization_questions": [
            {
                "id": "support-style",
                "type": "select",
                "question": "What type of support do you provide?",
                "options": ["Technical support", "Sales support", "General inquiries", "All of the above"],
                "required": True,
                "field": "special_instructions",
                "help_text": "Helps customize responses for your support type"
            }
        ],
        "integrations": [
            {
                "id": "slack",
                "name": "Slack",
                "type": "chat",
                "description": "Connect to Slack workspace",
                "setup_required": True,
                "cost": 0,
                "benefits": ["Real-time messaging", "Channel integration", "File sharing"]
            }
        ],
        "visual_flow": [],
        "demo_data": {}
    }
}

@router.get("/templates", response_model=List[AgentTemplate])
async def get_agent_templates():
    """Get all available agent templates"""
    return list(AGENT_TEMPLATES.values())

@router.get("/templates/{template_id}", response_model=AgentTemplate)
async def get_agent_template(template_id: str):
    """Get a specific agent template by ID"""
    if template_id not in AGENT_TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found")
    return AGENT_TEMPLATES[template_id]

@router.post("/customize")
async def process_customization(request: CustomizationRequest):
    """Process customization answers and return updated config"""
    if request.template_id not in AGENT_TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template = AGENT_TEMPLATES[request.template_id]
    config = template["default_config"].copy()
    
    # Apply customization answers to config
    for question in template["customization_questions"]:
        if question["id"] in request.answers:
            field = question["field"]
            config[field] = request.answers[question["id"]]
    
    return {
        "config": config,
        "template": template,
        "customizations": request.answers
    }

@router.post("/demo")
async def generate_demo(request: DemoRequest):
    """Generate a demo preview based on template and configuration"""
    if request.template_id not in AGENT_TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template = AGENT_TEMPLATES[request.template_id]
    
    # Simulate demo generation based on template
    if request.template_id == "email-manager":
        demo_preview = {
            "input": template["demo_data"]["sample_email"],
            "output": template["demo_data"]["generated_response"],
            "processing_steps": [
                "Analyzing email content and intent",
                "Determining appropriate response style",
                "Generating professional reply",
                "Applying industry-specific context",
                "Finalizing response with signature"
            ],
            "confidence": 0.92,
            "estimated_time": 2.3
        }
    else:
        # Generic demo for other templates
        demo_preview = {
            "input": {"type": "sample_input", "content": "Sample input data"},
            "output": {"type": "sample_output", "content": "Sample output data"},
            "processing_steps": [
                "Processing input data",
                "Applying configuration",
                "Generating response",
                "Formatting output"
            ],
            "confidence": 0.85,
            "estimated_time": 1.5
        }
    
    return {
        "demo_preview": demo_preview,
        "config": request.config,
        "template": template
    }

@router.post("/create", response_model=Dict[str, Any])
async def create_agent_from_template(request: AgentCreateRequest, db: Session = Depends(get_db)):
    """Create an agent from a template with customizations"""
    if request.template_id not in AGENT_TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template = AGENT_TEMPLATES[request.template_id]
    
    # Create the agent in the database
    db_agent = DBAgent(
        name=request.name,
        description=request.description,
        capabilities=json.dumps(request.config.get("capabilities", [])),
        type=request.template_id,
        department="general",
        status="idle",
        is_active=True
    )
    
    db.add(db_agent)
    db.commit()
    db.refresh(db_agent)
    
    # Store additional configuration
    agent_config = {
        "template_id": request.template_id,
        "config": request.config,
        "customizations": request.customizations,
        "integrations": request.integrations,
        "created_at": datetime.utcnow().isoformat(),
        "visual_flow": template.get("visual_flow", []),
        "demo_data": template.get("demo_data", {})
    }
    
    # In a real implementation, you might store this in a separate config table
    # For now, we'll return it with the agent
    
    return {
        "agent": {
            "id": db_agent.id,
            "name": db_agent.name,
            "description": db_agent.description,
            "type": db_agent.type,
            "status": db_agent.status,
            "created_at": db_agent.created_at.isoformat() if db_agent.created_at else None
        },
        "config": agent_config,
        "template": template
    }

@router.get("/templates/{template_id}/flow")
async def get_visual_flow(template_id: str):
    """Get the visual flow for a specific template"""
    if template_id not in AGENT_TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template = AGENT_TEMPLATES[template_id]
    return {
        "flow": template.get("visual_flow", []),
        "template_id": template_id
    }

@router.post("/templates/{template_id}/test")
async def test_template_config(template_id: str, config: Dict[str, Any]):
    """Test a template configuration with sample data"""
    if template_id not in AGENT_TEMPLATES:
        raise HTTPException(status_code=404, detail="Template not found")
    
    template = AGENT_TEMPLATES[template_id]
    
    # Simulate testing the configuration
    test_result = {
        "success": True,
        "test_data": template.get("demo_data", {}),
        "config_valid": True,
        "estimated_performance": {
            "response_time": "2-3 seconds",
            "accuracy": "92%",
            "cost_per_month": "$5-10"
        }
    }
    
    return test_result 