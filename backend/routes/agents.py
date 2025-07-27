from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any, Optional
import os
from pathlib import Path
from datetime import datetime, timedelta
import random
import uuid

router = APIRouter(prefix="/api/v1/agents", tags=["agents"])

# Get templates directory
project_root = Path(__file__).parent.parent.parent
templates_dir = project_root / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

@router.get("/")
async def get_all_agents():
    """Get all agents across all departments"""
    try:
        # Import departments data from departments.py
        from .departments import DEPARTMENTS
        
        all_agents = []
        for dept in DEPARTMENTS:
            for agent in dept.get("agents", []):
                agent_data = {
                    **agent,
                    "department_id": dept["id"],
                    "department_name": dept["name"],
                    "department_color": dept["color"]
                }
                all_agents.append(agent_data)
        
        return {
            "success": True,
            "agents": all_agents,
            "total_count": len(all_agents),
            "voice_enabled_count": len([a for a in all_agents if a.get("voice_enabled", False)])
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load agents: {str(e)}")

@router.get("/{agent_id}")
async def get_agent(agent_id: str):
    """Get specific agent details"""
    try:
        from .departments import DEPARTMENTS
        
        for dept in DEPARTMENTS:
            for agent in dept.get("agents", []):
                if agent["id"] == agent_id:
                    return {
                        "success": True,
                        "agent": {
                            **agent,
                            "department_id": dept["id"],
                            "department_name": dept["name"],
                            "department_color": dept["color"],
                            "room_type": dept["room_type"]
                        },
                        "interaction_capabilities": {
                            "voice_chat": agent.get("voice_enabled", False),
                            "text_chat": True,
                            "task_assignment": True,
                            "performance_review": True,
                            "project_collaboration": True
                        }
                    }
        
        raise HTTPException(status_code=404, detail="Agent not found")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load agent: {str(e)}")

@router.get("/department/{department_id}")
async def get_agents_by_department(department_id: str):
    """Get all agents in a specific department"""
    try:
        from .departments import DEPARTMENTS
        
        department = next((d for d in DEPARTMENTS if d["id"] == department_id), None)
        if not department:
            raise HTTPException(status_code=404, detail="Department not found")
        
        agents = []
        for agent in department.get("agents", []):
            agent_data = {
                **agent,
                "department_id": department["id"],
                "department_name": department["name"],
                "department_color": department["color"]
            }
            agents.append(agent_data)
        
        return {
            "success": True,
            "department_id": department_id,
            "department_name": department["name"],
            "agents": agents,
            "agents_count": len(agents)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load department agents: {str(e)}")

@router.post("/{agent_id}/chat/start")
async def start_agent_chat(agent_id: str, chat_type: str = "text"):
    """Start a chat session with a specific agent"""
    try:
        from .departments import DEPARTMENTS
        
        agent = None
        department = None
        
        for dept in DEPARTMENTS:
            for a in dept.get("agents", []):
                if a["id"] == agent_id:
                    agent = a
                    department = dept
                    break
            if agent:
                break
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        if chat_type == "voice" and not agent.get("voice_enabled", False):
            raise HTTPException(status_code=400, detail="Agent does not support voice chat")
        
        session_id = str(uuid.uuid4())
        
        chat_session = {
            "session_id": session_id,
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "department_id": department["id"],
            "department_name": department["name"],
            "chat_type": chat_type,
            "status": "active",
            "started_at": datetime.now().isoformat(),
            "welcome_message": f"Hello! I'm {agent['name']}, {agent['role']} in {department['name']}. I'm currently working on: {agent['current_task']}. How can I help you?"
        }
        
        return {
            "success": True,
            "chat_session": chat_session,
            "agent": agent,
            "department": {
                "id": department["id"],
                "name": department["name"],
                "color": department["color"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to start chat: {str(e)}")

@router.post("/{agent_id}/chat/{session_id}/message")
async def send_message_to_agent(agent_id: str, session_id: str, message: Dict[str, Any]):
    """Send a message to an agent in an active chat session"""
    try:
        from .departments import DEPARTMENTS
        
        agent = None
        department = None
        
        for dept in DEPARTMENTS:
            for a in dept.get("agents", []):
                if a["id"] == agent_id:
                    agent = a
                    department = dept
                    break
            if agent:
                break
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        user_message = message.get("content", "")
        if not user_message.strip():
            raise HTTPException(status_code=400, detail="Message content is required")
        
        # Generate AI response based on agent personality and role
        ai_response = generate_agent_response(agent, user_message, department)
        
        return {
            "success": True,
            "session_id": session_id,
            "user_message": {
                "id": str(uuid.uuid4()),
                "type": "user",
                "content": user_message,
                "timestamp": datetime.now().isoformat()
            },
            "agent_response": {
                "id": str(uuid.uuid4()),
                "type": "assistant",
                "content": ai_response,
                "timestamp": datetime.now().isoformat(),
                "agent_name": agent["name"]
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to send message: {str(e)}")

@router.get("/{agent_id}/performance")
async def get_agent_performance(agent_id: str):
    """Get agent performance metrics and analytics"""
    try:
        from .departments import DEPARTMENTS
        
        agent = None
        department = None
        
        for dept in DEPARTMENTS:
            for a in dept.get("agents", []):
                if a["id"] == agent_id:
                    agent = a
                    department = dept
                    break
            if agent:
                break
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        # Generate performance metrics
        performance_data = {
            "agent_id": agent_id,
            "current_efficiency": agent.get("efficiency", 90),
            "tasks_completed_today": random.randint(3, 12),
            "average_response_time": f"{random.uniform(0.5, 3.0):.1f} seconds",
            "user_satisfaction": random.uniform(4.2, 4.9),
            "collaboration_score": random.randint(85, 98),
            "learning_progress": random.randint(75, 95),
            "weekly_trends": {
                "efficiency": [92, 94, 91, 93, 95, 94, agent.get("efficiency", 90)],
                "tasks": [8, 10, 7, 9, 11, 8, random.randint(6, 12)],
                "satisfaction": [4.5, 4.6, 4.4, 4.7, 4.8, 4.6, random.uniform(4.2, 4.9)]
            },
            "specializations": agent.get("specialization", "General AI").split("/"),
            "recent_achievements": [
                f"Completed {agent.get('current_task', 'task optimization')}",
                f"Improved efficiency by {random.randint(2, 8)}%",
                f"Received {random.randint(3, 7)} positive user reviews"
            ]
        }
        
        return {
            "success": True,
            "agent": agent,
            "department": {
                "id": department["id"],
                "name": department["name"]
            },
            "performance": performance_data,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get performance data: {str(e)}")

@router.post("/{agent_id}/task/assign")
async def assign_task_to_agent(agent_id: str, task_data: Dict[str, Any]):
    """Assign a new task to an agent"""
    try:
        from .departments import DEPARTMENTS
        
        agent = None
        department = None
        
        for dept in DEPARTMENTS:
            for a in dept.get("agents", []):
                if a["id"] == agent_id:
                    agent = a
                    department = dept
                    break
            if agent:
                break
        
        if not agent:
            raise HTTPException(status_code=404, detail="Agent not found")
        
        task = {
            "id": str(uuid.uuid4()),
            "title": task_data.get("title", "New Task"),
            "description": task_data.get("description", ""),
            "priority": task_data.get("priority", "medium"),
            "estimated_duration": task_data.get("estimated_duration", "2 hours"),
            "assigned_at": datetime.now().isoformat(),
            "status": "assigned",
            "agent_id": agent_id,
            "agent_name": agent["name"],
            "department_id": department["id"]
        }
        
        return {
            "success": True,
            "message": f"Task assigned to {agent['name']}",
            "task": task,
            "agent": agent,
            "estimated_completion": (datetime.now() + timedelta(hours=2)).isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to assign task: {str(e)}")

@router.get("/voice-enabled")
async def get_voice_enabled_agents():
    """Get all agents that support voice interaction"""
    try:
        from .departments import DEPARTMENTS
        
        voice_agents = []
        for dept in DEPARTMENTS:
            for agent in dept.get("agents", []):
                if agent.get("voice_enabled", False):
                    agent_data = {
                        **agent,
                        "department_id": dept["id"],
                        "department_name": dept["name"],
                        "department_color": dept["color"]
                    }
                    voice_agents.append(agent_data)
        
        return {
            "success": True,
            "voice_agents": voice_agents,
            "total_count": len(voice_agents),
            "departments_with_voice": len(set(a["department_id"] for a in voice_agents))
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to load voice agents: {str(e)}")

@router.get("/search")
async def search_agents(
    query: str = "",
    department: Optional[str] = None,
    voice_enabled: Optional[bool] = None,
    status: Optional[str] = None
):
    """Search and filter agents based on criteria"""
    try:
        from .departments import DEPARTMENTS
        
        all_agents = []
        for dept in DEPARTMENTS:
            for agent in dept.get("agents", []):
                agent_data = {
                    **agent,
                    "department_id": dept["id"],
                    "department_name": dept["name"],
                    "department_color": dept["color"]
                }
                all_agents.append(agent_data)
        
        # Apply filters
        filtered_agents = all_agents
        
        if query:
            filtered_agents = [
                a for a in filtered_agents 
                if query.lower() in a["name"].lower() 
                or query.lower() in a["role"].lower()
                or query.lower() in a.get("specialization", "").lower()
            ]
        
        if department:
            filtered_agents = [a for a in filtered_agents if a["department_id"] == department]
        
        if voice_enabled is not None:
            filtered_agents = [a for a in filtered_agents if a.get("voice_enabled", False) == voice_enabled]
        
        if status:
            filtered_agents = [a for a in filtered_agents if a.get("status", "").lower() == status.lower()]
        
        return {
            "success": True,
            "agents": filtered_agents,
            "total_count": len(filtered_agents),
            "filters_applied": {
                "query": query,
                "department": department,
                "voice_enabled": voice_enabled,
                "status": status
            }
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search agents: {str(e)}")

def generate_agent_response(agent: Dict[str, Any], user_message: str, department: Dict[str, Any]) -> str:
    """Generate contextual AI response based on agent personality and role"""
    
    # Base responses by personality type
    personality_responses = {
        "analytical_innovative": [
            "Let me analyze this from a technical perspective and provide innovative solutions.",
            "Based on current data patterns, I recommend exploring these innovative approaches.",
            "I'll break this down analytically and suggest some creative alternatives."
        ],
        "methodical_reliable": [
            "I'll handle this systematically to ensure reliable results.",
            "Let me walk through this step-by-step using proven methodologies.",
            "I take a methodical approach to guarantee consistent, reliable outcomes."
        ],
        "vigilant_protective": [
            "I'm carefully monitoring all security aspects of this request.",
            "Security is my top priority - let me ensure this approach is safe and compliant.",
            "I'll implement protective measures while addressing your needs."
        ],
        "visionary_strategic": [
            "From a strategic standpoint, I see several long-term opportunities here.",
            "Let me share my vision for how this fits into our broader strategic goals.",
            "I'm thinking strategically about the bigger picture and future implications."
        ],
        "creative_empathetic": [
            "I understand what you're looking for - let me suggest some creative solutions.",
            "I'm approaching this with both creativity and empathy for user needs.",
            "Let me design something that's both innovative and user-friendly."
        ],
        "persuasive_results_driven": [
            "I'm focused on driving results that will exceed your expectations.",
            "Let me present a compelling case for the most effective approach.",
            "I'm confident we can achieve outstanding results with this strategy."
        ],
        "energetic_persistent": [
            "I'm excited to tackle this challenge with full energy and persistence!",
            "This is exactly the kind of problem I love solving - let's make it happen!",
            "I'll keep working on this until we find the perfect solution."
        ],
        "analytical_precise": [
            "I'll provide precise analysis based on accurate data and calculations.",
            "Let me give you exact figures and detailed analytical insights.",
            "Precision is key - I'll ensure every detail is accurate and well-analyzed."
        ],
        "detail_oriented_insightful": [
            "I've noticed some important details that provide valuable insights.",
            "Let me share detailed observations that reveal key insights about this situation.",
            "My attention to detail has uncovered some valuable insights for you."
        ],
        "empathetic_strategic": [
            "I understand the human impact while considering strategic implications.",
            "Let me balance empathy for people with strategic business needs.",
            "I'm thinking about both the human elements and strategic outcomes."
        ],
        "people_focused_efficient": [
            "I'll ensure this solution works efficiently for everyone involved.",
            "My focus is on creating people-friendly processes that are also highly efficient.",
            "Let me design an approach that puts people first while maximizing efficiency."
        ],
        "helpful_relationship_focused": [
            "I'm here to help and strengthen our relationship through excellent service.",
            "Building strong relationships is my priority - let me help you succeed.",
            "I'll provide helpful solutions that enhance our working relationship."
        ],
        "patient_problem_solver": [
            "I'll patiently work through this problem until we find the right solution.",
            "Let me take the time needed to properly understand and solve this challenge.",
            "I'm patient and thorough in my problem-solving approach."
        ],
        "strategic_systematic": [
            "I'll approach this strategically using systematic methods for optimal results.",
            "Let me apply strategic thinking with systematic execution.",
            "I combine strategic vision with systematic implementation."
        ],
        "methodical_improvement_focused": [
            "I'll systematically identify improvement opportunities and implement them.",
            "Let me methodically analyze this for continuous improvement possibilities.",
            "I focus on methodical approaches to drive ongoing improvements."
        ]
    }
    
    # Role-specific context
    role_contexts = {
        "Lead Software Architect": "From an architectural perspective",
        "Cloud Infrastructure Engineer": "Considering infrastructure requirements",
        "Cybersecurity Specialist": "With security best practices in mind",
        "Chief Product Officer": "From a product strategy standpoint",
        "Senior UX/UI Designer": "Focusing on user experience design",
        "VP of Sales": "Looking at this from a sales and revenue perspective",
        "Lead Generation Specialist": "Considering lead generation and conversion",
        "Chief Marketing Officer": "From a brand and marketing strategy angle",
        "Content Marketing Manager": "Thinking about content and messaging",
        "Chief Financial Officer": "From a financial and operational perspective",
        "Business Intelligence Analyst": "Based on data analysis and insights",
        "Chief People Officer": "Considering the human resources and culture impact",
        "Talent Acquisition Manager": "From a talent and recruitment perspective",
        "VP of Customer Success": "Focusing on customer satisfaction and success",
        "Senior Support Specialist": "From a technical support and service angle",
        "Chief Operating Officer": "Considering operational efficiency and strategy",
        "Process Optimization Manager": "Looking at process improvement opportunities"
    }
    
    # Get agent's personality and role
    personality = agent.get("personality", "analytical_innovative")
    role = agent.get("role", "AI Assistant")
    
    # Select appropriate response
    responses = personality_responses.get(personality, personality_responses["analytical_innovative"])
    base_response = random.choice(responses)
    
    # Add role context
    role_context = role_contexts.get(role, "From my expertise")
    
    # Combine with current task context
    current_task = agent.get("current_task", "optimizing workflows")
    
    # Generate contextual response
    contextual_response = f"{role_context}, {base_response.lower()} Since I'm currently working on {current_task}, I can apply those insights to help you. What specific aspect would you like me to focus on?"
    
    return contextual_response
