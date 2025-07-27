from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any
import os
from pathlib import Path
from datetime import datetime
import uuid

from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/departments", tags=["departments"])

# Get templates directory
project_root = Path(__file__).parent.parent.parent
templates_dir = project_root / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Modern 2025 Enterprise Departments with Immersive Room Experience
DEPARTMENTS = [
    {
        "id": "engineering",
        "name": "Engineering & Technology",
        "description": "Software development, AI/ML, cloud infrastructure, and technical innovation",
        "color": "#0066cc",
        "icon": "fas fa-code",
        "room_type": "tech_lab",
        "voice_enabled": True,
        "agents_count": 8,
        "room_experience": {
            "environment": "Modern tech lab with multiple monitors, whiteboards, and AI development tools",
            "ambient_sound": "keyboard_typing_servers_humming",
            "lighting": "blue_ambient_tech_lighting",
            "interactive_elements": ["code_editor", "deployment_dashboard", "server_monitoring", "ai_model_training"],
            "meeting_spaces": ["standup_area", "code_review_corner", "innovation_pod"]
        },
        "metrics": {
            "code_quality_score": 94.2,
            "deployment_frequency": "12/day",
            "system_uptime": "99.8%",
            "bug_resolution_time": "2.3 hours",
            "innovation_index": 89.5
        },
        "active_projects": [
            {"id": "ai_platform", "name": "AI Agent Platform", "progress": 78, "priority": "high"},
            {"id": "cloud_migration", "name": "Cloud Infrastructure", "progress": 92, "priority": "medium"},
            {"id": "security_update", "name": "Security Enhancement", "progress": 45, "priority": "high"}
        ],
        "agents": [
            {
                "id": "eng_001",
                "name": "Alex CodeMaster",
                "role": "Lead Software Architect",
                "status": "active",
                "voice_enabled": True,
                "specialization": "AI/ML Systems",
                "current_task": "Optimizing neural network architecture",
                "efficiency": 96.5,
                "experience_years": 8,
                "personality": "analytical_innovative"
            },
            {
                "id": "eng_002", 
                "name": "Sam DevOps",
                "role": "Cloud Infrastructure Engineer",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Kubernetes & AWS",
                "current_task": "Scaling microservices cluster",
                "efficiency": 94.2,
                "experience_years": 6,
                "personality": "methodical_reliable"
            },
            {
                "id": "eng_003",
                "name": "Jordan Security",
                "role": "Cybersecurity Specialist",
                "status": "monitoring",
                "voice_enabled": True,
                "specialization": "Security Architecture",
                "current_task": "Threat analysis and prevention",
                "efficiency": 91.8,
                "experience_years": 7,
                "personality": "vigilant_protective"
            }
        ]
    },
    {
        "id": "product",
        "name": "Product & Innovation",
        "description": "Product strategy, UX/UI design, innovation management, and user research",
        "color": "#8b5cf6",
        "icon": "fas fa-lightbulb",
        "room_type": "design_studio",
        "voice_enabled": True,
        "agents_count": 6,
        "room_experience": {
            "environment": "Creative design studio with mood boards, prototyping stations, and user journey maps",
            "ambient_sound": "creative_ambience_design_tools",
            "lighting": "warm_creative_lighting",
            "interactive_elements": ["design_canvas", "user_feedback_wall", "prototype_station", "analytics_dashboard"],
            "meeting_spaces": ["brainstorm_lounge", "user_testing_lab", "strategy_room"]
        },
        "metrics": {
            "user_satisfaction": 4.8,
            "feature_adoption_rate": 87.3,
            "time_to_market": "8.2 weeks",
            "design_system_compliance": 95.6,
            "innovation_pipeline": 23
        },
        "active_projects": [
            {"id": "ui_redesign", "name": "Dashboard Redesign", "progress": 65, "priority": "high"},
            {"id": "mobile_app", "name": "Mobile Experience", "progress": 30, "priority": "medium"},
            {"id": "user_research", "name": "Customer Journey Analysis", "progress": 88, "priority": "low"}
        ],
        "agents": [
            {
                "id": "prod_001",
                "name": "Casey Vision",
                "role": "Chief Product Officer",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Product Strategy",
                "current_task": "Q1 roadmap planning",
                "efficiency": 93.7,
                "experience_years": 10,
                "personality": "visionary_strategic"
            },
            {
                "id": "prod_002",
                "name": "Riley Designer",
                "role": "Senior UX/UI Designer",
                "status": "active",
                "voice_enabled": True,
                "specialization": "User Experience Design",
                "current_task": "Design system updates",
                "efficiency": 91.4,
                "experience_years": 5,
                "personality": "creative_empathetic"
            }
        ]
    },
    {
        "id": "sales",
        "name": "Sales & Revenue",
        "description": "Sales operations, lead generation, customer acquisition, and revenue optimization",
        "color": "#10b981",
        "icon": "fas fa-chart-line",
        "room_type": "sales_floor",
        "voice_enabled": True,
        "agents_count": 7,
        "room_experience": {
            "environment": "Dynamic sales floor with performance dashboards, call stations, and deal tracking boards",
            "ambient_sound": "professional_phone_calls_typing",
            "lighting": "energetic_bright_lighting",
            "interactive_elements": ["sales_dashboard", "lead_tracker", "call_center", "performance_metrics"],
            "meeting_spaces": ["deal_room", "training_corner", "celebration_area"]
        },
        "metrics": {
            "monthly_revenue": 425000,
            "conversion_rate": 23.8,
            "avg_deal_size": 12500,
            "sales_cycle": "18.5 days",
            "quota_attainment": 112.3
        },
        "active_projects": [
            {"id": "enterprise_sales", "name": "Enterprise Sales Program", "progress": 72, "priority": "high"},
            {"id": "crm_optimization", "name": "CRM System Upgrade", "progress": 55, "priority": "medium"},
            {"id": "sales_training", "name": "AI Sales Training", "progress": 90, "priority": "low"}
        ],
        "agents": [
            {
                "id": "sales_001",
                "name": "Morgan Closer",
                "role": "VP of Sales",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Enterprise Sales",
                "current_task": "Q1 forecast review",
                "efficiency": 97.2,
                "experience_years": 12,
                "personality": "persuasive_results_driven"
            },
            {
                "id": "sales_002",
                "name": "Taylor Lead",
                "role": "Lead Generation Specialist",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Inbound/Outbound Sales",
                "current_task": "Lead qualification automation",
                "efficiency": 89.6,
                "experience_years": 4,
                "personality": "energetic_persistent"
            }
        ]
    },
    {
        "id": "marketing",
        "name": "Marketing & Brand",
        "description": "Digital marketing, brand management, content creation, and growth strategies",
        "color": "#f59e0b",
        "icon": "fas fa-bullhorn",
        "room_type": "creative_studio",
        "voice_enabled": True,
        "agents_count": 6,
        "room_experience": {
            "environment": "Vibrant creative studio with brand displays, content creation stations, and campaign boards",
            "ambient_sound": "creative_energy_collaboration",
            "lighting": "colorful_brand_lighting",
            "interactive_elements": ["campaign_dashboard", "content_studio", "brand_wall", "analytics_center"],
            "meeting_spaces": ["creative_lounge", "video_studio", "strategy_war_room"]
        },
        "metrics": {
            "brand_awareness": 78.5,
            "campaign_roi": 340,
            "social_engagement": 156000,
            "lead_generation": 2450,
            "content_performance": 92.1
        },
        "active_projects": [
            {"id": "brand_refresh", "name": "Brand Identity Refresh", "progress": 83, "priority": "high"},
            {"id": "digital_campaign", "name": "Q1 Digital Campaign", "progress": 45, "priority": "high"},
            {"id": "content_strategy", "name": "Content Marketing Strategy", "progress": 67, "priority": "medium"}
        ],
        "agents": [
            {
                "id": "mkt_001",
                "name": "Avery Brand",
                "role": "Chief Marketing Officer",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Brand Strategy",
                "current_task": "Brand positioning review",
                "efficiency": 94.8,
                "experience_years": 9,
                "personality": "creative_strategic"
            },
            {
                "id": "mkt_002",
                "name": "Blake Content",
                "role": "Content Marketing Manager",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Content Creation",
                "current_task": "Video content production",
                "efficiency": 88.3,
                "experience_years": 6,
                "personality": "creative_storyteller"
            }
        ]
    },
    {
        "id": "finance",
        "name": "Finance & Operations",
        "description": "Financial planning, accounting, operations management, and business intelligence",
        "color": "#059669",
        "icon": "fas fa-chart-pie",
        "room_type": "executive_suite",
        "voice_enabled": True,
        "agents_count": 5,
        "room_experience": {
            "environment": "Professional executive suite with financial dashboards, meeting rooms, and analytics displays",
            "ambient_sound": "quiet_professional_ambience",
            "lighting": "professional_executive_lighting",
            "interactive_elements": ["financial_dashboard", "analytics_center", "forecasting_station", "compliance_monitor"],
            "meeting_spaces": ["boardroom", "planning_room", "audit_chamber"]
        },
        "metrics": {
            "monthly_burn_rate": 180000,
            "cash_runway": "18 months",
            "profit_margin": 24.7,
            "operational_efficiency": 91.2,
            "compliance_score": 98.5
        },
        "active_projects": [
            {"id": "financial_audit", "name": "Annual Financial Audit", "progress": 90, "priority": "high"},
            {"id": "budget_planning", "name": "2025 Budget Planning", "progress": 60, "priority": "medium"},
            {"id": "cost_optimization", "name": "Cost Optimization Initiative", "progress": 35, "priority": "low"}
        ],
        "agents": [
            {
                "id": "fin_001",
                "name": "Drew Numbers",
                "role": "Chief Financial Officer",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Financial Strategy",
                "current_task": "Quarterly financial review",
                "efficiency": 96.1,
                "experience_years": 15,
                "personality": "analytical_precise"
            },
            {
                "id": "fin_002",
                "name": "Quinn Analyst",
                "role": "Business Intelligence Analyst",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Data Analytics",
                "current_task": "Revenue forecast modeling",
                "efficiency": 92.7,
                "experience_years": 7,
                "personality": "detail_oriented_insightful"
            }
        ]
    },
    {
        "id": "hr",
        "name": "Human Resources & Culture",
        "description": "Talent acquisition, employee development, culture building, and people operations",
        "color": "#dc2626",
        "icon": "fas fa-users",
        "room_type": "people_space",
        "voice_enabled": True,
        "agents_count": 4,
        "room_experience": {
            "environment": "Welcoming people-focused space with collaboration areas, wellness zones, and culture displays",
            "ambient_sound": "collaborative_positive_energy",
            "lighting": "warm_welcoming_lighting",
            "interactive_elements": ["talent_dashboard", "culture_wall", "wellness_center", "feedback_station"],
            "meeting_spaces": ["interview_rooms", "wellness_lounge", "team_building_area"]
        },
        "metrics": {
            "employee_satisfaction": 4.6,
            "retention_rate": 94.2,
            "time_to_hire": "12.3 days",
            "culture_score": 88.7,
            "development_participation": 97.1
        },
        "active_projects": [
            {"id": "talent_pipeline", "name": "Talent Pipeline Development", "progress": 70, "priority": "high"},
            {"id": "culture_initiative", "name": "Culture Enhancement Program", "progress": 55, "priority": "medium"},
            {"id": "performance_system", "name": "Performance Management System", "progress": 85, "priority": "low"}
        ],
        "agents": [
            {
                "id": "hr_001",
                "name": "Harper People",
                "role": "Chief People Officer",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Talent Strategy",
                "current_task": "Culture assessment review",
                "efficiency": 93.4,
                "experience_years": 11,
                "personality": "empathetic_strategic"
            },
            {
                "id": "hr_002",
                "name": "River Talent",
                "role": "Talent Acquisition Manager",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Recruitment",
                "current_task": "Engineering team expansion",
                "efficiency": 87.9,
                "experience_years": 5,
                "personality": "people_focused_efficient"
            }
        ]
    },
    {
        "id": "customer_success",
        "name": "Customer Success & Support",
        "description": "Customer relationship management, support operations, and success programs",
        "color": "#7c3aed",
        "icon": "fas fa-heart",
        "room_type": "service_center",
        "voice_enabled": True,
        "agents_count": 6,
        "room_experience": {
            "environment": "Customer-focused service center with support stations, feedback displays, and success tracking",
            "ambient_sound": "helpful_service_environment",
            "lighting": "friendly_service_lighting",
            "interactive_elements": ["support_dashboard", "customer_feedback_wall", "success_metrics", "escalation_center"],
            "meeting_spaces": ["customer_call_rooms", "success_planning_area", "feedback_review_space"]
        },
        "metrics": {
            "customer_satisfaction": 4.7,
            "support_response_time": "2.3 hours",
            "resolution_rate": 96.8,
            "churn_rate": 2.1,
            "nps_score": 67
        },
        "active_projects": [
            {"id": "support_automation", "name": "Support Automation Platform", "progress": 75, "priority": "high"},
            {"id": "customer_portal", "name": "Customer Self-Service Portal", "progress": 40, "priority": "medium"},
            {"id": "success_program", "name": "Customer Success Program", "progress": 90, "priority": "low"}
        ],
        "agents": [
            {
                "id": "cs_001",
                "name": "Sage Helper",
                "role": "VP of Customer Success",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Customer Relationship Management",
                "current_task": "Customer health score analysis",
                "efficiency": 95.3,
                "experience_years": 8,
                "personality": "helpful_relationship_focused"
            },
            {
                "id": "cs_002",
                "name": "Finn Support",
                "role": "Senior Support Specialist",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Technical Support",
                "current_task": "Complex issue resolution",
                "efficiency": 91.6,
                "experience_years": 6,
                "personality": "patient_problem_solver"
            }
        ]
    },
    {
        "id": "operations",
        "name": "Operations & Strategy",
        "description": "Business operations, strategic planning, process optimization, and compliance",
        "color": "#1f2937",
        "icon": "fas fa-cogs",
        "room_type": "command_center",
        "voice_enabled": True,
        "agents_count": 5,
        "room_experience": {
            "environment": "Strategic command center with operational dashboards, process maps, and planning stations",
            "ambient_sound": "strategic_planning_efficiency",
            "lighting": "focused_operational_lighting",
            "interactive_elements": ["operations_dashboard", "process_optimizer", "strategic_planning_board", "compliance_monitor"],
            "meeting_spaces": ["strategy_room", "operations_center", "planning_hub"]
        },
        "metrics": {
            "operational_efficiency": 93.5,
            "process_optimization": 87.2,
            "strategic_alignment": 91.8,
            "compliance_rate": 99.1,
            "cost_effectiveness": 88.9
        },
        "active_projects": [
            {"id": "process_automation", "name": "Process Automation Initiative", "progress": 65, "priority": "high"},
            {"id": "strategic_plan", "name": "2025 Strategic Plan", "progress": 80, "priority": "high"},
            {"id": "compliance_update", "name": "Compliance Framework Update", "progress": 50, "priority": "medium"}
        ],
        "agents": [
            {
                "id": "ops_001",
                "name": "Cameron Strategy",
                "role": "Chief Operating Officer",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Strategic Operations",
                "current_task": "Strategic planning review",
                "efficiency": 94.7,
                "experience_years": 13,
                "personality": "strategic_systematic"
            },
            {
                "id": "ops_002",
                "name": "Parker Process",
                "role": "Process Optimization Manager",
                "status": "active",
                "voice_enabled": True,
                "specialization": "Process Engineering",
                "current_task": "Workflow optimization analysis",
                "efficiency": 90.4,
                "experience_years": 7,
                "personality": "methodical_improvement_focused"
            }
        ]
    }
]

# Pydantic models
class DepartmentCreate(BaseModel):
    name: str
    description: str
    color: str
    type: str

class AgentCreate(BaseModel):
    name: str
    role: str
    specialty: str
    personality_type: str
    voice_enabled: bool = False

@router.get("/")
async def get_departments():
    """Get all departments with their immersive room data"""
    return {
        "success": True,
        "departments": DEPARTMENTS,
        "total_count": len(DEPARTMENTS),
        "active_departments": len([d for d in DEPARTMENTS if d.get("voice_enabled", False)]),
        "total_agents": sum(d["agents_count"] for d in DEPARTMENTS)
    }

@router.post("/")
async def create_department(department_data: DepartmentCreate):
    """Create a new department"""
    try:
        new_department = {
            "id": f"dept-{str(uuid.uuid4())[:8]}",
            "name": department_data.name,
            "description": department_data.description,
            "color": department_data.color,
            "icon": "fas fa-building",
            "agents": [],
            "room_experience": {
                "environment": f"Dynamic {department_data.type} workspace with modern equipment and collaborative spaces",
                "ambient_sound": "Professional office ambience",
                "lighting": "Natural daylight with task lighting"
            },
            "projects": [],
            "metrics": {
                "efficiency": 85.0,
                "collaboration_score": 90.0,
                "innovation_index": 78.0
            },
            "created_at": datetime.now().isoformat()
        }
        
        # Add to global departments list
        DEPARTMENTS.append(new_department)
        
        return {
            "success": True,
            "message": "Department created successfully",
            "department": new_department
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create department: {str(e)}")

@router.post("/{department_id}/agents")
async def add_agent_to_department(department_id: str, agent_data: AgentCreate):
    """Add a new agent to a specific department"""
    try:
        department = next((d for d in DEPARTMENTS if d["id"] == department_id), None)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        
        new_agent = {
            "id": f"agent-{str(uuid.uuid4())[:8]}",
            "name": agent_data.name,
            "role": agent_data.role,
            "specialty": agent_data.specialty,
            "personality_type": agent_data.personality_type,
            "voice_enabled": agent_data.voice_enabled,
            "current_task": "Ready for assignment",
            "status": "idle",
            "efficiency": 95.0,
            "active_projects": [],
            "created_at": datetime.now().isoformat()
        }
        
        # Add agent to department
        department["agents"].append(new_agent)
        
        return {
            "success": True,
            "message": f"Agent {new_agent['name']} added to {department['name']}",
            "agent": new_agent,
            "department": department["name"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add agent: {str(e)}")

@router.get("/{department_id}")
async def get_department(department_id: str):
    """Get specific department with full room experience data"""
    department = next((d for d in DEPARTMENTS if d["id"] == department_id), None)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return {
        "success": True,
        "department": department,
        "room_status": "active",
        "available_interactions": [
            "voice_chat",
            "text_chat", 
            "agent_individual_chat",
            "department_meeting",
            "project_collaboration",
            "metrics_review"
        ]
    }

@router.get("/{department_id}/agents")
async def get_department_agents(department_id: str):
    """Get all agents in a specific department"""
    department = next((d for d in DEPARTMENTS if d["id"] == department_id), None)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return {
        "success": True,
        "department_id": department_id,
        "department_name": department["name"],
        "agents": department["agents"],
        "agents_count": len(department["agents"]),
        "voice_enabled_agents": len([a for a in department["agents"] if a.get("voice_enabled", False)])
    }

@router.get("/{department_id}/agents/{agent_id}")
async def get_specific_agent(department_id: str, agent_id: str):
    """Get specific agent for individual interaction"""
    department = next((d for d in DEPARTMENTS if d["id"] == department_id), None)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    agent = next((a for a in department["agents"] if a["id"] == agent_id), None)
    if not agent:
        raise HTTPException(status_code=404, detail="Agent not found")
    
    return {
        "success": True,
        "agent": agent,
        "department_context": {
            "id": department["id"],
            "name": department["name"],
            "room_type": department["room_type"]
        },
        "interaction_capabilities": {
            "voice_chat": agent.get("voice_enabled", False),
            "text_chat": True,
            "task_assignment": True,
            "performance_review": True,
            "project_collaboration": True
        }
    }

@router.post("/{department_id}/enter")
async def enter_department_room(department_id: str):
    """Enter a department's immersive room experience"""
    department = next((d for d in DEPARTMENTS if d["id"] == department_id), None)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Generate session ID for room experience
    session_id = str(uuid.uuid4())
    
    return {
        "success": True,
        "session_id": session_id,
        "department": department,
        "room_initialized": True,
        "welcome_message": f"Welcome to the {department['name']} department! You can now interact with our team.",
        "available_actions": [
            "talk_to_department",
            "talk_to_individual_agent",
            "review_projects",
            "check_metrics",
            "start_voice_chat",
            "collaborate_on_project"
        ]
    }

@router.post("/{department_id}/voice/start")
async def start_voice_chat(department_id: str, agent_id: str = None):
    """Start voice chat with department or specific agent"""
    department = next((d for d in DEPARTMENTS if d["id"] == department_id), None)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    if agent_id:
        agent = next((a for a in department["agents"] if a["id"] == agent_id), None)
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        if not agent.get("voice_enabled", False):
            raise HTTPException(status_code=400, detail="Agent does not support voice chat")
        
        chat_session = {
            "session_id": str(uuid.uuid4()),
            "type": "individual_agent_voice",
            "department_id": department_id,
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "status": "active",
            "started_at": datetime.now().isoformat()
        }
    else:
        chat_session = {
            "session_id": str(uuid.uuid4()),
            "type": "department_voice",
            "department_id": department_id,
            "department_name": department["name"],
            "status": "active",
            "started_at": datetime.now().isoformat()
        }
    
    return {
        "success": True,
        "voice_session": chat_session,
        "message": f"Voice chat started with {agent['name'] if agent_id else department['name']}"
    }

@router.get("/{department_id}/projects")
async def get_department_projects(department_id: str):
    """Get all active projects in a department"""
    department = next((d for d in DEPARTMENTS if d["id"] == department_id), None)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return {
        "success": True,
        "department_id": department_id,
        "projects": department["active_projects"],
        "projects_count": len(department["active_projects"])
    }

@router.get("/{department_id}/metrics")
async def get_department_metrics(department_id: str):
    """Get real-time department metrics and performance data"""
    department = next((d for d in DEPARTMENTS if d["id"] == department_id), None)
    if not department:
        raise HTTPException(status_code=404, detail="Department not found")
    
    return {
        "success": True,
        "department_id": department_id,
        "metrics": department["metrics"],
        "last_updated": datetime.now().isoformat()
    } 