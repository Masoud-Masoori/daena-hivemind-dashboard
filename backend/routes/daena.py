from fastapi import APIRouter, HTTPException, WebSocket, WebSocketDisconnect
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import json
import uuid
import asyncio
from pydantic import BaseModel

router = APIRouter(prefix="/api/v1/daena", tags=["Daena AI VP"])

# Daena AI VP Models
class DaenaMessage(BaseModel):
    id: str
    type: str  # "user" or "assistant"
    content: str
    timestamp: datetime
    context: Optional[Dict[str, Any]] = None

class DaenaSession(BaseModel):
    session_id: str
    user_id: Optional[str] = None
    started_at: datetime
    last_activity: datetime
    messages: List[DaenaMessage] = []
    context: Dict[str, Any] = {}

# Active sessions storage
active_sessions: Dict[str, DaenaSession] = {}
active_connections: Dict[str, WebSocket] = {}

@router.get("/status")
async def get_daena_status():
    """Get Daena AI VP system status and capabilities"""
    try:
        from .departments import DEPARTMENTS
        
        # Calculate system metrics
        total_agents = sum(dept["agents_count"] for dept in DEPARTMENTS)
        voice_enabled_agents = sum(
            len([a for a in dept.get("agents", []) if a.get("voice_enabled", False)]) 
            for dept in DEPARTMENTS
        )
        active_projects = sum(len(dept.get("active_projects", [])) for dept in DEPARTMENTS)
        
        # System health metrics
        system_health = {
            "overall_score": 98.5,
            "departments_online": len(DEPARTMENTS),
            "agents_active": total_agents,
            "voice_agents_active": voice_enabled_agents,
            "active_projects": active_projects,
            "system_uptime": "99.8%",
            "response_time_avg": "0.8s",
            "last_health_check": datetime.now().isoformat()
        }
        
        # Daena capabilities
        capabilities = {
            "executive_oversight": True,
            "cross_department_coordination": True,
            "strategic_analysis": True,
            "real_time_monitoring": True,
            "voice_interaction": True,
            "predictive_analytics": True,
            "automated_decision_making": True,
            "compliance_monitoring": True,
            "performance_optimization": True,
            "crisis_management": True
        }
        
        # Current focus areas
        focus_areas = [
            "Q1 strategic planning",
            "Department performance optimization", 
            "Agent efficiency monitoring",
            "Cross-team collaboration enhancement",
            "Innovation pipeline management"
        ]
        
        return {
            "success": True,
            "daena_status": "active",
            "system_health": system_health,
            "capabilities": capabilities,
            "current_focus": focus_areas,
            "active_sessions": len(active_sessions),
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get Daena status: {str(e)}")

@router.post("/chat/start")
async def start_daena_chat(user_id: Optional[str] = None):
    """Start a new chat session with Daena AI VP"""
    session_id = str(uuid.uuid4())
    
    session = DaenaSession(
        session_id=session_id,
        user_id=user_id,
        started_at=datetime.now(),
        last_activity=datetime.now(),
        messages=[
            DaenaMessage(
                id=str(uuid.uuid4()),
                type="assistant",
                content="Hello! I'm Daena, your AI Vice President. I have complete oversight of all 8 departments and 47 AI agents. I can provide strategic insights, coordinate cross-department initiatives, and help optimize your business operations. How can I assist you today?",
                timestamp=datetime.now(),
                context={"greeting": True, "capabilities_mentioned": True}
            )
        ],
        context={
            "user_preferences": {},
            "conversation_topics": [],
            "active_departments": [],
            "current_projects": []
        }
    )
    
    active_sessions[session_id] = session
    
    return {
        "success": True,
        "session": session,
        "welcome_message": session.messages[0].content,
        "available_commands": [
            "/status - Get system overview",
            "/departments - List all departments", 
            "/agents - Show agent status",
            "/projects - View active projects",
            "/metrics - Performance analytics",
            "/help - Show all commands"
        ]
    }

@router.post("/chat/{session_id}/message")
async def send_message_to_daena(session_id: str, message_data: Dict[str, Any]):
    """Send a message to Daena AI VP"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    session = active_sessions[session_id]
    user_message_content = message_data.get("content", "").strip()
    
    if not user_message_content:
        raise HTTPException(status_code=400, detail="Message content is required")
    
    # Add user message
    user_message = DaenaMessage(
        id=str(uuid.uuid4()),
        type="user",
        content=user_message_content,
        timestamp=datetime.now()
    )
    session.messages.append(user_message)
    session.last_activity = datetime.now()
    
    # Generate Daena response
    daena_response = await generate_daena_response(user_message_content, session)
    
    # Add Daena response
    assistant_message = DaenaMessage(
        id=str(uuid.uuid4()),
        type="assistant",
        content=daena_response["content"],
        timestamp=datetime.now(),
        context=daena_response.get("context", {})
    )
    session.messages.append(assistant_message)
    
    return {
        "success": True,
        "session_id": session_id,
        "user_message": user_message,
        "daena_response": assistant_message,
        "session_updated": session.last_activity.isoformat()
    }

@router.get("/chat/{session_id}")
async def get_chat_session(session_id: str):
    """Get chat session details and history"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    session = active_sessions[session_id]
    
    return {
        "success": True,
        "session": session,
        "message_count": len(session.messages),
        "duration": (datetime.now() - session.started_at).total_seconds()
    }

@router.delete("/chat/{session_id}")
async def end_chat_session(session_id: str):
    """End a chat session with Daena AI VP"""
    if session_id not in active_sessions:
        raise HTTPException(status_code=404, detail="Chat session not found")
    
    session = active_sessions.pop(session_id)
    
    # Close WebSocket connection if exists
    if session_id in active_connections:
        await active_connections[session_id].close()
        del active_connections[session_id]
    
    return {
        "success": True,
        "message": "Chat session ended",
        "session_duration": (datetime.now() - session.started_at).total_seconds(),
        "total_messages": len(session.messages)
    }

@router.websocket("/chat/{session_id}/ws")
async def daena_websocket(websocket: WebSocket, session_id: str):
    """WebSocket connection for real-time chat with Daena AI VP"""
    await websocket.accept()
    active_connections[session_id] = websocket
    
    try:
        # Send welcome message if new session
        if session_id not in active_sessions:
            welcome_response = await start_daena_chat()
            await websocket.send_text(json.dumps({
                "type": "session_started",
                "data": welcome_response
            }))
        
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "message":
                # Process message through Daena
                response = await send_message_to_daena(session_id, {
                    "content": message_data.get("content", "")
                })
                
                # Send response back
                await websocket.send_text(json.dumps({
                    "type": "message_response",
                    "data": response
                }))
            
            elif message_data.get("type") == "voice_start":
                # Handle voice interaction start
                await websocket.send_text(json.dumps({
                    "type": "voice_ready",
                    "data": {"message": "Voice interaction ready"}
                }))
            
            elif message_data.get("type") == "voice_end":
                # Handle voice interaction end
                await websocket.send_text(json.dumps({
                    "type": "voice_ended",
                    "data": {"message": "Voice interaction ended"}
                }))
    
    except WebSocketDisconnect:
        if session_id in active_connections:
            del active_connections[session_id]

@router.get("/insights/executive")
async def get_executive_insights():
    """Get high-level executive insights from Daena AI VP"""
    try:
        from .departments import DEPARTMENTS
        
        # Generate executive-level insights
        insights = {
            "strategic_overview": {
                "company_health_score": 94.2,
                "growth_trajectory": "positive",
                "key_strengths": [
                    "Strong engineering team performance (94.2% efficiency)",
                    "Excellent customer satisfaction (4.7/5.0)",
                    "Robust sales pipeline ($450K projected)"
                ],
                "areas_for_improvement": [
                    "Marketing campaign ROI optimization",
                    "Cross-department collaboration enhancement",
                    "Process automation opportunities"
                ]
            },
            "department_performance": [
                {
                    "department": dept["name"],
                    "score": sum(dept["metrics"].values()) / len(dept["metrics"]) if isinstance(list(dept["metrics"].values())[0], (int, float)) else 90,
                    "trend": "positive" if dept["id"] in ["engineering", "sales", "customer_success"] else "stable",
                    "key_metric": list(dept["metrics"].keys())[0] if dept["metrics"] else "efficiency"
                }
                for dept in DEPARTMENTS
            ],
            "ai_agent_analytics": {
                "total_agents": sum(dept["agents_count"] for dept in DEPARTMENTS),
                "average_efficiency": 93.8,
                "voice_enabled_percentage": 87.2,
                "top_performers": [
                    "Morgan Closer (Sales) - 97.2%",
                    "Alex CodeMaster (Engineering) - 96.5%", 
                    "Drew Numbers (Finance) - 96.1%"
                ]
            },
            "predictive_analytics": {
                "revenue_forecast": "$520K next month",
                "efficiency_trend": "+2.3% improvement",
                "risk_factors": [
                    "Market volatility impact",
                    "Talent acquisition challenges",
                    "Technology infrastructure scaling"
                ],
                "opportunities": [
                    "AI automation expansion",
                    "Customer success program scaling",
                    "Strategic partnership development"
                ]
            },
            "recommendations": [
                {
                    "priority": "high",
                    "area": "Revenue Growth",
                    "action": "Accelerate enterprise sales program",
                    "impact": "15-20% revenue increase"
                },
                {
                    "priority": "medium", 
                    "area": "Operational Efficiency",
                    "action": "Implement cross-department AI automation",
                    "impact": "12% efficiency improvement"
                },
                {
                    "priority": "medium",
                    "area": "Customer Experience",
                    "action": "Enhance support automation platform",
                    "impact": "25% faster resolution times"
                }
            ]
        }
        
        return {
            "success": True,
            "insights": insights,
            "generated_at": datetime.now().isoformat(),
            "confidence_score": 0.92
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to generate insights: {str(e)}")

@router.get("/coordination/departments")
async def get_department_coordination():
    """Get cross-department coordination opportunities and conflicts"""
    try:
        from .departments import DEPARTMENTS
        
        coordination_data = {
            "active_collaborations": [
                {
                    "departments": ["Engineering & Technology", "Product & Innovation"],
                    "project": "AI Platform Development",
                    "status": "active",
                    "progress": 78,
                    "next_milestone": "Beta testing phase"
                },
                {
                    "departments": ["Sales & Revenue", "Marketing & Brand"],
                    "project": "Enterprise Campaign Launch",
                    "status": "planning",
                    "progress": 45,
                    "next_milestone": "Campaign strategy finalization"
                },
                {
                    "departments": ["Customer Success & Support", "Product & Innovation"],
                    "project": "Customer Portal Enhancement",
                    "status": "development",
                    "progress": 62,
                    "next_milestone": "User testing phase"
                }
            ],
            "potential_synergies": [
                {
                    "departments": ["Engineering & Technology", "Operations & Strategy"],
                    "opportunity": "Process automation infrastructure",
                    "potential_impact": "20% efficiency gain",
                    "effort_required": "medium"
                },
                {
                    "departments": ["HR & Culture", "Customer Success & Support"],
                    "opportunity": "Employee satisfaction methodology sharing",
                    "potential_impact": "Improved culture metrics",
                    "effort_required": "low"
                }
            ],
            "resource_conflicts": [
                {
                    "departments": ["Engineering & Technology", "Product & Innovation"],
                    "conflict": "Shared design system resources", 
                    "severity": "low",
                    "resolution": "Implement resource scheduling system"
                }
            ],
            "coordination_score": 87.5,
            "recommendations": [
                "Establish weekly cross-department sync meetings",
                "Implement shared project management dashboard",
                "Create resource allocation optimization system"
            ]
        }
        
        return {
            "success": True,
            "coordination": coordination_data,
            "last_updated": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get coordination data: {str(e)}")

async def generate_daena_response(user_input: str, session: DaenaSession) -> Dict[str, Any]:
    """Generate contextual response from Daena AI VP"""
    
    # Command processing
    if user_input.startswith("/"):
        return await process_daena_command(user_input, session)
    
    # Context analysis
    context_keywords = {
        "departments": ["department", "team", "group", "division"],
        "agents": ["agent", "ai", "bot", "assistant"],
        "performance": ["performance", "metric", "efficiency", "productivity"],
        "strategy": ["strategy", "plan", "roadmap", "vision", "goal"],
        "projects": ["project", "initiative", "task", "work"],
        "finance": ["revenue", "profit", "cost", "budget", "financial"],
        "sales": ["sales", "deal", "customer", "client", "prospect"],
        "hr": ["employee", "talent", "culture", "hiring", "retention"]
    }
    
    detected_context = []
    for category, keywords in context_keywords.items():
        if any(keyword in user_input.lower() for keyword in keywords):
            detected_context.append(category)
    
    # Generate response based on context
    if "departments" in detected_context:
        response = await generate_department_response(user_input, session)
    elif "agents" in detected_context:
        response = await generate_agent_response(user_input, session) 
    elif "performance" in detected_context:
        response = await generate_performance_response(user_input, session)
    elif "strategy" in detected_context:
        response = await generate_strategy_response(user_input, session)
    elif "projects" in detected_context:
        response = await generate_project_response(user_input, session)
    else:
        response = await generate_general_response(user_input, session)
    
    # Update session context
    session.context["conversation_topics"].extend(detected_context)
    session.context["last_response_type"] = response.get("type", "general")
    
    return response

async def process_daena_command(command: str, session: DaenaSession) -> Dict[str, Any]:
    """Process Daena AI VP commands"""
    
    command = command.lower().strip()
    
    if command == "/status":
        status_data = await get_daena_status()
        return {
            "content": f"System Status: {status_data['system_health']['overall_score']}% healthy. {status_data['system_health']['departments_online']} departments online with {status_data['system_health']['agents_active']} active agents. Current uptime: {status_data['system_health']['system_uptime']}.",
            "type": "status",
            "context": {"command": "status", "data": status_data}
        }
    
    elif command == "/departments":
        from .departments import DEPARTMENTS
        dept_list = ", ".join([dept["name"] for dept in DEPARTMENTS])
        return {
            "content": f"Active Departments ({len(DEPARTMENTS)}): {dept_list}. Each department has specialized AI agents and ongoing projects. Which department would you like to know more about?",
            "type": "departments",
            "context": {"command": "departments", "count": len(DEPARTMENTS)}
        }
    
    elif command == "/agents":
        from .departments import DEPARTMENTS
        total_agents = sum(dept["agents_count"] for dept in DEPARTMENTS)
        voice_agents = sum(len([a for a in dept.get("agents", []) if a.get("voice_enabled", False)]) for dept in DEPARTMENTS)
        return {
            "content": f"Agent Overview: {total_agents} total agents across all departments. {voice_agents} agents support voice interaction. Top performers include Morgan Closer (Sales), Alex CodeMaster (Engineering), and Drew Numbers (Finance).",
            "type": "agents",
            "context": {"command": "agents", "total": total_agents, "voice_enabled": voice_agents}
        }
    
    elif command == "/projects":
        from .departments import DEPARTMENTS
        total_projects = sum(len(dept.get("active_projects", [])) for dept in DEPARTMENTS)
        return {
            "content": f"Active Projects: {total_projects} projects currently in progress. Key initiatives include AI Platform Development (78% complete), Enterprise Sales Program (72% complete), and Brand Identity Refresh (83% complete).",
            "type": "projects", 
            "context": {"command": "projects", "total": total_projects}
        }
    
    elif command == "/metrics":
        return {
            "content": "Performance Metrics: Overall efficiency at 93.8%, customer satisfaction 4.7/5.0, revenue growth trending positive. Engineering leads efficiency at 94.2%, Sales exceeding quota at 112.3%. Would you like detailed metrics for any specific department?",
            "type": "metrics",
            "context": {"command": "metrics"}
        }
    
    elif command == "/help":
        return {
            "content": "Available Commands:\n/status - System overview\n/departments - List departments\n/agents - Agent information\n/projects - Active projects\n/metrics - Performance data\n/help - This help menu\n\nYou can also ask me about strategy, coordination, insights, or any business questions.",
            "type": "help",
            "context": {"command": "help"}
        }
    
    else:
        return {
            "content": "Unknown command. Type /help to see available commands, or ask me anything about your business operations.",
            "type": "error",
            "context": {"command": "unknown", "input": command}
        }

async def generate_department_response(user_input: str, session: DaenaSession) -> Dict[str, Any]:
    """Generate department-focused response"""
    return {
        "content": "I'm monitoring all 8 departments continuously. Each department has specialized AI agents working on strategic initiatives. Engineering is leading with 94.2% efficiency, while Sales is exceeding targets at 112.3% quota attainment. Would you like to dive deeper into any specific department's performance or coordination opportunities?",
        "type": "department_analysis",
        "context": {"focus": "departments", "metrics_included": True}
    }

async def generate_agent_response(user_input: str, session: DaenaSession) -> Dict[str, Any]:
    """Generate agent-focused response"""
    return {
        "content": "Our 47 AI agents are performing exceptionally well across all departments. Top performers include Morgan Closer in Sales (97.2% efficiency), Alex CodeMaster in Engineering (96.5%), and Drew Numbers in Finance (96.1%). 87% of our agents support voice interaction for enhanced collaboration. Which agent or team would you like to know more about?",
        "type": "agent_analysis",
        "context": {"focus": "agents", "performance_data": True}
    }

async def generate_performance_response(user_input: str, session: DaenaSession) -> Dict[str, Any]:
    """Generate performance-focused response"""
    return {
        "content": "Current performance metrics show strong company health at 94.2% overall score. Key highlights: Engineering efficiency (94.2%), Customer satisfaction (4.7/5.0), Sales quota attainment (112.3%), and system uptime (99.8%). Revenue is trending positive with $425K monthly performance. I recommend focusing on marketing ROI optimization and cross-department collaboration for further improvements.",
        "type": "performance_analysis", 
        "context": {"focus": "performance", "recommendations": True}
    }

async def generate_strategy_response(user_input: str, session: DaenaSession) -> Dict[str, Any]:
    """Generate strategy-focused response"""
    return {
        "content": "From a strategic perspective, I see strong opportunities in AI automation expansion, enterprise sales acceleration, and customer success program scaling. Our current strategic initiatives are progressing well with Q1 planning at 80% completion. I recommend prioritizing the enterprise sales program for immediate revenue impact and implementing cross-department AI automation for long-term efficiency gains.",
        "type": "strategy_analysis",
        "context": {"focus": "strategy", "recommendations": True}
    }

async def generate_project_response(user_input: str, session: DaenaSession) -> Dict[str, Any]:
    """Generate project-focused response"""
    return {
        "content": "Currently tracking 24 active projects across all departments. Major initiatives include AI Platform Development (78% complete), Enterprise Sales Program (72%), Brand Identity Refresh (83%), and Customer Portal Enhancement (62%). Engineering and Product teams are collaborating excellently on the AI platform. Would you like detailed status on any specific project or department initiatives?",
        "type": "project_analysis",
        "context": {"focus": "projects", "status_included": True}
    }

async def generate_general_response(user_input: str, session: DaenaSession) -> Dict[str, Any]:
    """Generate general conversational response"""
    responses = [
        "As your AI VP, I'm here to provide strategic insights and coordinate across all departments. I have real-time visibility into every aspect of your business operations.",
        "I'm analyzing your question in the context of our current business performance and strategic objectives. Let me provide you with data-driven insights.",
        "From my executive oversight perspective, I can help you understand the interconnections between departments, projects, and performance metrics.",
        "I'm continuously monitoring all business operations and can provide strategic recommendations based on real-time data and predictive analytics."
    ]
    
    import random
    return {
        "content": random.choice(responses) + " What specific aspect of your business would you like to explore?",
        "type": "general",
        "context": {"focus": "general", "conversational": True}
    } 