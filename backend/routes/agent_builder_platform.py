from fastapi import APIRouter, HTTPException, Request, Form, UploadFile, File
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any, Optional
import os
from pathlib import Path
from datetime import datetime, timedelta
import json
import uuid

router = APIRouter(prefix="/agent-builder", tags=["agent-builder"])

# Get templates directory
project_root = Path(__file__).parent.parent.parent
templates_dir = project_root / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Agent Builder Platform Data
AGENT_TEMPLATES = [
    {
        "id": "template_001",
        "name": "Email Assistant",
        "description": "AI agent for email management and response automation",
        "category": "productivity",
        "difficulty": "beginner",
        "price": 0,
        "features": ["Email classification", "Auto-response", "Calendar integration"],
        "prompt_template": "Create an AI agent that can help manage emails by classifying them, drafting responses, and integrating with calendar for scheduling meetings.",
        "config": {
            "model": "gpt-4",
            "tools": ["email_api", "calendar_api", "gmail_integration"],
            "personality": "professional and helpful",
            "capabilities": ["email_processing", "response_generation", "scheduling"]
        },
        "usage_count": 1247,
        "rating": 4.8,
        "created_by": "Daena AI",
        "created_date": "2024-01-01"
    },
    {
        "id": "template_002",
        "name": "Customer Support Bot",
        "description": "Intelligent customer support agent with FAQ handling",
        "category": "customer_service",
        "difficulty": "beginner",
        "price": 0,
        "features": ["FAQ handling", "Ticket creation", "Escalation logic"],
        "prompt_template": "Build a customer support AI agent that can answer common questions, create support tickets, and escalate complex issues to human agents.",
        "config": {
            "model": "gpt-4",
            "tools": ["knowledge_base", "ticket_system", "chat_interface"],
            "personality": "friendly and professional",
            "capabilities": ["question_answering", "ticket_management", "escalation"]
        },
        "usage_count": 892,
        "rating": 4.6,
        "created_by": "Daena AI",
        "created_date": "2024-01-05"
    },
    {
        "id": "template_003",
        "name": "Data Analyst",
        "description": "Advanced data analysis and reporting agent",
        "category": "analytics",
        "difficulty": "expert",
        "price": 29.99,
        "features": ["Data visualization", "Statistical analysis", "Report generation"],
        "prompt_template": "Develop an expert-level AI agent for data analysis that can process large datasets, perform statistical analysis, and generate comprehensive reports with visualizations.",
        "config": {
            "model": "gpt-4",
            "tools": ["pandas", "matplotlib", "scikit-learn", "database_connector"],
            "personality": "analytical and precise",
            "capabilities": ["data_processing", "statistical_analysis", "visualization", "reporting"]
        },
        "usage_count": 456,
        "rating": 4.9,
        "created_by": "DataScience Pro",
        "created_date": "2024-01-10"
    },
    {
        "id": "template_004",
        "name": "Content Creator",
        "description": "AI agent for content creation and marketing",
        "category": "marketing",
        "difficulty": "intermediate",
        "price": 19.99,
        "features": ["Blog writing", "Social media posts", "SEO optimization"],
        "prompt_template": "Create a content creation AI agent that can write blog posts, generate social media content, and optimize for SEO with keyword research.",
        "config": {
            "model": "gpt-4",
            "tools": ["seo_api", "social_media_api", "content_calendar"],
            "personality": "creative and engaging",
            "capabilities": ["content_writing", "seo_optimization", "social_media_management"]
        },
        "usage_count": 678,
        "rating": 4.7,
        "created_by": "Content Master",
        "created_date": "2024-01-08"
    },
    {
        "id": "template_005",
        "name": "Sales Assistant",
        "description": "AI-powered sales assistant for lead qualification and follow-up",
        "category": "sales",
        "difficulty": "intermediate",
        "price": 39.99,
        "features": ["Lead qualification", "Follow-up automation", "CRM integration"],
        "prompt_template": "Build a sales assistant AI agent that can qualify leads, automate follow-up sequences, and integrate with CRM systems for pipeline management.",
        "config": {
            "model": "gpt-4",
            "tools": ["crm_api", "email_automation", "lead_scoring"],
            "personality": "persuasive and professional",
            "capabilities": ["lead_qualification", "follow_up", "crm_integration"]
        },
        "usage_count": 334,
        "rating": 4.5,
        "created_by": "Sales Expert",
        "created_date": "2024-01-12"
    }
]

USER_AGENTS = []  # Store user-created agents

@router.get("/", response_class=HTMLResponse)
async def agent_builder_dashboard(request: Request):
    """Agent Builder platform dashboard"""
    return templates.TemplateResponse("agent_builder.html", {
        "request": request,
        "templates": AGENT_TEMPLATES
    })

@router.get("/api/v1/templates")
async def get_agent_templates() -> List[Dict[str, Any]]:
    """Get all agent templates"""
    return AGENT_TEMPLATES

@router.get("/api/v1/templates/{template_id}")
async def get_agent_template(template_id: str) -> Dict[str, Any]:
    """Get specific agent template"""
    for template in AGENT_TEMPLATES:
        if template["id"] == template_id:
            return template
    raise HTTPException(status_code=404, detail="Template not found")

@router.get("/api/v1/templates/category/{category}")
async def get_templates_by_category(category: str) -> List[Dict[str, Any]]:
    """Get templates by category"""
    return [t for t in AGENT_TEMPLATES if t["category"] == category]

@router.get("/api/v1/templates/difficulty/{difficulty}")
async def get_templates_by_difficulty(difficulty: str) -> List[Dict[str, Any]]:
    """Get templates by difficulty level"""
    valid_difficulties = ["beginner", "intermediate", "expert"]
    if difficulty.lower() not in valid_difficulties:
        raise HTTPException(status_code=400, detail="Invalid difficulty level")
    
    return [t for t in AGENT_TEMPLATES if t["difficulty"] == difficulty.lower()]

@router.post("/api/v1/agents/create-simple")
async def create_simple_agent(
    name: str = Form(...),
    description: str = Form(...),
    prompt: str = Form(...),
    category: str = Form(...)
) -> Dict[str, Any]:
    """Create a simple agent from text prompt (Beginner mode)"""
    
    agent_id = str(uuid.uuid4())
    new_agent = {
        "id": agent_id,
        "name": name,
        "description": description,
        "prompt": prompt,
        "category": category,
        "type": "simple",
        "created_date": datetime.now().isoformat(),
        "status": "active",
        "config": {
            "model": "gpt-4",
            "personality": "helpful and professional",
            "capabilities": ["text_processing", "basic_automation"]
        },
        "usage_stats": {
            "conversations": 0,
            "tasks_completed": 0,
            "user_satisfaction": 0
        }
    }
    
    USER_AGENTS.append(new_agent)
    
    return {
        "success": True,
        "agent_id": agent_id,
        "message": f"Agent '{name}' created successfully!",
        "agent": new_agent
    }

@router.post("/api/v1/agents/create-advanced")
async def create_advanced_agent(
    name: str = Form(...),
    description: str = Form(...),
    model: str = Form(...),
    tools: List[str] = Form(...),
    personality: str = Form(...),
    capabilities: List[str] = Form(...),
    custom_config: Optional[str] = Form(None)
) -> Dict[str, Any]:
    """Create an advanced agent with full customization (Expert mode)"""
    
    agent_id = str(uuid.uuid4())
    
    # Parse custom config if provided
    config_data = {}
    if custom_config:
        try:
            config_data = json.loads(custom_config)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid custom configuration JSON")
    
    new_agent = {
        "id": agent_id,
        "name": name,
        "description": description,
        "type": "advanced",
        "created_date": datetime.now().isoformat(),
        "status": "active",
        "config": {
            "model": model,
            "tools": tools,
            "personality": personality,
            "capabilities": capabilities,
            **config_data
        },
        "usage_stats": {
            "conversations": 0,
            "tasks_completed": 0,
            "user_satisfaction": 0,
            "api_calls": 0
        }
    }
    
    USER_AGENTS.append(new_agent)
    
    return {
        "success": True,
        "agent_id": agent_id,
        "message": f"Advanced agent '{name}' created successfully!",
        "agent": new_agent
    }

@router.post("/api/v1/agents/create-from-template")
async def create_agent_from_template(
    template_id: str = Form(...),
    name: str = Form(...),
    customizations: Optional[str] = Form(None)
) -> Dict[str, Any]:
    """Create an agent from a template"""
    
    # Find the template
    template = None
    for t in AGENT_TEMPLATES:
        if t["id"] == template_id:
            template = t
            break
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    # Parse customizations if provided
    custom_config = {}
    if customizations:
        try:
            custom_config = json.loads(customizations)
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid customizations JSON")
    
    agent_id = str(uuid.uuid4())
    new_agent = {
        "id": agent_id,
        "name": name,
        "description": template["description"],
        "template_id": template_id,
        "type": "template_based",
        "created_date": datetime.now().isoformat(),
        "status": "active",
        "config": {
            **template["config"],
            **custom_config
        },
        "usage_stats": {
            "conversations": 0,
            "tasks_completed": 0,
            "user_satisfaction": 0
        }
    }
    
    USER_AGENTS.append(new_agent)
    
    # Update template usage count
    template["usage_count"] += 1
    
    return {
        "success": True,
        "agent_id": agent_id,
        "message": f"Agent '{name}' created from template successfully!",
        "agent": new_agent,
        "template": template
    }

@router.get("/api/v1/agents/user")
async def get_user_agents() -> List[Dict[str, Any]]:
    """Get all user-created agents"""
    return USER_AGENTS

@router.get("/api/v1/agents/{agent_id}")
async def get_user_agent(agent_id: str) -> Dict[str, Any]:
    """Get specific user agent"""
    for agent in USER_AGENTS:
        if agent["id"] == agent_id:
            return agent
    raise HTTPException(status_code=404, detail="Agent not found")

@router.post("/api/v1/agents/{agent_id}/chat")
async def chat_with_agent(
    agent_id: str,
    message: str = Form(...)
) -> Dict[str, Any]:
    """Chat with a user-created agent"""
    
    # Find the agent
    agent = None
    for a in USER_AGENTS:
        if a["id"] == agent_id:
            agent = a
            break
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Simulate agent response based on type and configuration
    if agent["type"] == "simple":
        response = f"Hello! I'm {agent['name']}. I understand you said: '{message}'. How can I help you with {agent['category']} tasks?"
    elif agent["type"] == "advanced":
        response = f"Advanced response from {agent['name']}: I can help you with {', '.join(agent['config']['capabilities'])}. Your message: '{message}'"
    else:  # template_based
        response = f"Template-based response from {agent['name']}: I'm designed for {agent['description']}. Your message: '{message}'"
    
    # Update usage stats
    agent["usage_stats"]["conversations"] += 1
    
    return {
        "agent_id": agent_id,
        "agent_name": agent["name"],
        "response": response,
        "timestamp": datetime.now().isoformat()
    }

@router.post("/api/v1/agents/{agent_id}/deploy")
async def deploy_agent(agent_id: str) -> Dict[str, Any]:
    """Deploy an agent for production use"""
    
    # Find the agent
    agent = None
    for a in USER_AGENTS:
        if a["id"] == agent_id:
            agent = a
            break
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    # Simulate deployment process
    deployment_id = str(uuid.uuid4())
    
    return {
        "success": True,
        "deployment_id": deployment_id,
        "agent_id": agent_id,
        "status": "deployed",
        "endpoint": f"/api/v1/deployed-agents/{deployment_id}",
        "message": f"Agent '{agent['name']}' deployed successfully!"
    }

@router.get("/api/v1/marketplace/stats")
async def get_marketplace_stats() -> Dict[str, Any]:
    """Get marketplace statistics"""
    total_templates = len(AGENT_TEMPLATES)
    total_agents_created = len(USER_AGENTS)
    total_usage = sum(t["usage_count"] for t in AGENT_TEMPLATES)
    
    return {
        "total_templates": total_templates,
        "total_agents_created": total_agents_created,
        "total_template_usage": total_usage,
        "popular_categories": ["productivity", "customer_service", "marketing"],
        "average_rating": sum(t["rating"] for t in AGENT_TEMPLATES) / total_templates if total_templates > 0 else 0
    }

@router.get("/template/{template_id}", response_class=HTMLResponse)
async def template_detail(request: Request, template_id: str):
    """Template detail page"""
    template = None
    for t in AGENT_TEMPLATES:
        if t["id"] == template_id:
            template = t
            break
    
    if not template:
        raise HTTPException(status_code=404, detail="Template not found")
    
    return templates.TemplateResponse("template_detail.html", {
        "request": request,
        "template": template
    })

@router.get("/agent/{agent_id}", response_class=HTMLResponse)
async def user_agent_detail(request: Request, agent_id: str):
    """User agent detail page"""
    agent = None
    for a in USER_AGENTS:
        if a["id"] == agent_id:
            agent = a
            break
    
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return templates.TemplateResponse("user_agent_detail.html", {
        "request": request,
        "agent": agent
    }) 