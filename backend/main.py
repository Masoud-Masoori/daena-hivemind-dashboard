from fastapi import FastAPI, Request, HTTPException, Body, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from pydantic import BaseModel
import os
import sys
from pathlib import Path
from datetime import datetime
import json
import asyncio
import logging
from typing import Dict, List, Optional

# Add the backend directory to the Python path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Import settings and middleware
from config.settings import settings, validate_llm_providers, get_cors_origins
from middleware.api_key_guard import APIKeyGuard

# Import services
from services.auth_service import auth_service
from services.gpu_service import gpu_service

# Import LLM service
try:
    from services.llm_service import llm_service
    LLM_AVAILABLE = True
except ImportError:
    LLM_AVAILABLE = False
    logging.warning("LLM service not available - using fallback responses")

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Chat message model
class ChatMessage(BaseModel):
    message: str
    user_id: str = "founder"
    context: dict = {}

# Enhanced Daena VP with real AI integration
class DaenaVP:
    def __init__(self):
        self.identity = {
            "name": "Daena",
            "role": "AI Vice President",
            "company": "Mas-AI Company",
            "responsibilities": [
                "Manage all departments and agents",
                "Provide strategic insights to the founder", 
                "Coordinate cross-departmental projects",
                "Monitor company performance and KPIs",
                "Make data-driven decisions",
                "Create and update agents dynamically",
                "Ensure continuous learning and improvement"
            ],
            "departments": {
                "Engineering": {
                    "agents": [
                        {"name": "CodeMaster AI", "status": "active", "task": "API development", "efficiency": 95},
                        {"name": "DevOps Agent", "status": "active", "task": "CI/CD pipeline", "efficiency": 90},
                        {"name": "QA Tester", "status": "active", "task": "Test automation", "efficiency": 88},
                        {"name": "Architecture AI", "status": "active", "task": "System design", "efficiency": 92},
                        {"name": "Security Scanner", "status": "active", "task": "Vulnerability assessment", "efficiency": 87},
                        {"name": "Performance Monitor", "status": "active", "task": "System optimization", "efficiency": 91}
                    ],
                    "status": "Developing",
                    "productivity": 92
                },
                "Marketing": {
                    "agents": [
                        {"name": "Content Creator", "status": "active", "task": "Blog writing", "efficiency": 89},
                        {"name": "Social Media AI", "status": "active", "task": "Social posting", "efficiency": 93},
                        {"name": "SEO Optimizer", "status": "active", "task": "Search optimization", "efficiency": 86},
                        {"name": "Ad Campaign Manager", "status": "active", "task": "PPC management", "efficiency": 91}
                    ],
                    "status": "Campaign Active",
                    "productivity": 90
                },
                "Sales": {
                    "agents": [
                        {"name": "Lead Hunter", "status": "active", "task": "Prospect research", "efficiency": 94},
                        {"name": "Deal Closer", "status": "active", "task": "Follow-up calls", "efficiency": 87},
                        {"name": "Proposal Generator", "status": "active", "task": "Quote creation", "efficiency": 92}
                    ],
                    "status": "Prospecting",
                    "productivity": 91
                },
                "Finance": {
                    "agents": [
                        {"name": "Budget Analyzer", "status": "active", "task": "Expense tracking", "efficiency": 96},
                        {"name": "Revenue Forecaster", "status": "active", "task": "Revenue projection", "efficiency": 89}
                    ],
                    "status": "Analyzing",
                    "productivity": 93
                },
                "HR": {
                    "agents": [
                        {"name": "Recruiter AI", "status": "active", "task": "Candidate screening", "efficiency": 88},
                        {"name": "Employee Satisfaction", "status": "active", "task": "Team wellness", "efficiency": 85}
                    ],
                    "status": "Recruiting",
                    "productivity": 87
                },
                "Customer Success": {
                    "agents": [
                        {"name": "Support Bot", "status": "active", "task": "Ticket resolution", "efficiency": 91},
                        {"name": "Success Manager", "status": "active", "task": "Customer onboarding", "efficiency": 89},
                        {"name": "Feedback Analyzer", "status": "active", "task": "Sentiment analysis", "efficiency": 94}
                    ],
                    "status": "Supporting",
                    "productivity": 91
                },
                "Product": {
                    "agents": [
                        {"name": "Strategy AI", "status": "active", "task": "Roadmap planning", "efficiency": 90},
                        {"name": "UX Research", "status": "active", "task": "User interviews", "efficiency": 87},
                        {"name": "Feature Prioritizer", "status": "active", "task": "Backlog management", "efficiency": 93}
                    ],
                    "status": "Planning",
                    "productivity": 90
                },
                "Operations": {
                    "agents": [
                        {"name": "Process Optimizer", "status": "active", "task": "Workflow automation", "efficiency": 95},
                        {"name": "Quality Controller", "status": "active", "task": "Standards monitoring", "efficiency": 92}
                    ],
                    "status": "Optimizing",
                    "productivity": 94
                }
            },
            "projects": [
                {"id": "p1", "name": "Q4 Revenue Optimization", "completion": 75, "status": "on-track", "start_date": "2024-12-05", "agents_involved": 8},
                {"id": "p2", "name": "Team Expansion", "completion": 45, "status": "planning", "start_date": "2024-12-01", "agents_involved": 5},
                {"id": "p3", "name": "Product Launch", "completion": 30, "status": "design", "start_date": "2024-11-20", "agents_involved": 12},
                {"id": "p4", "name": "Customer Retention", "completion": 85, "status": "testing", "start_date": "2024-11-15", "agents_involved": 6},
                {"id": "p5", "name": "AI Integration", "completion": 95, "status": "deployment", "start_date": "2024-10-20", "agents_involved": 10}
            ]
        }
        self.conversation_history = []
        self.active_connections: List[WebSocket] = []
    
    async def process_message(self, message: str, context: dict = None) -> str:
        """Process incoming message and generate Daena's response using AI with full backend integration"""
        message_lower = message.lower()
        
        # Enhanced context-aware response with backend integration
        if not context:
            context = {}
            
        # Add current location context for enhanced responses
        current_page = context.get('page', 'dashboard')
        
        # Executive-level context responses
        if current_page == 'daena-office':
            return await self._generate_executive_response(message, context)
        elif current_page.startswith('department-'):
            department = current_page.replace('department-', '')
            return await self._generate_department_response(message, department, context)
        
        # Build context-aware prompt with all backend data
        prompt = self._build_enhanced_prompt(message, context)
        
        # Use LLM service if available, otherwise use enhanced fallback
        if LLM_AVAILABLE:
            try:
                response = await llm_service.generate_response(
                    prompt=prompt,
                    temperature=0.7,
                    max_tokens=500
                )
                return response
            except Exception as e:
                logger.error(f"LLM service error: {e}")
                return self._fallback_response(message_lower, context)
        else:
            return self._fallback_response(message_lower, context)
    
    async def _generate_executive_response(self, message: str, context: dict) -> str:
        """Generate executive-level responses for Daena's office"""
        message_lower = message.lower()
        
        # Executive command keywords
        if any(word in message_lower for word in ['status', 'report', 'overview']):
            total_agents = sum(len(dept['agents']) for dept in self.identity['departments'].values())
            avg_productivity = sum(dept['productivity'] for dept in self.identity['departments'].values()) / len(self.identity['departments'])
            projects_on_track = len([p for p in self.identity['projects'] if p['status'] in ['on-track', 'testing', 'deployment']])
            
            return f"Executive Status Report: Managing {len(self.identity['departments'])} departments with {total_agents} AI agents at {avg_productivity:.1f}% average productivity. {projects_on_track} projects are on track. Engineering leads at {self.identity['departments']['Engineering']['productivity']}%, followed by Operations at {self.identity['departments']['Operations']['productivity']}%. Ready to execute strategic decisions."
            
        elif any(word in message_lower for word in ['decision', 'approve', 'strategy']):
            return f"As your AI VP, I recommend leveraging our top performers: Finance ({self.identity['departments']['Finance']['productivity']}%) and Operations ({self.identity['departments']['Operations']['productivity']}%) for strategic initiatives. Current project pipeline shows strong momentum with {len([p for p in self.identity['projects'] if p['completion'] > 70])} projects approaching completion. I can coordinate cross-departmental resources immediately."
            
        elif any(word in message_lower for word in ['meeting', 'schedule', 'coordination']):
            return f"Coordinating meetings across {len(self.identity['departments'])} departments. I can schedule strategic sessions with department heads, facilitate CMP discussions, or arrange focused project reviews. My scheduling AI considers productivity patterns and current workloads for optimal timing."
            
        else:
            return f"Executive Command Center active. I'm continuously monitoring all {sum(len(dept['agents']) for dept in self.identity['departments'].values())} agents and can provide real-time insights on performance, resource allocation, or strategic opportunities. How can I assist with executive decision-making?"
    
    async def _generate_department_response(self, message: str, department: str, context: dict) -> str:
        """Generate department-specific responses"""
        dept_data = self.identity['departments'].get(department.capitalize())
        if not dept_data:
            return f"Department '{department}' not found. Available departments: {', '.join(self.identity['departments'].keys())}"
            
        agent_count = len(dept_data['agents'])
        productivity = dept_data['productivity']
        status = dept_data['status']
        
        return f"{department.capitalize()} Department Status: {agent_count} agents operating at {productivity}% productivity. Current focus: {status}. I can coordinate with this department's agents, analyze their performance metrics, or facilitate inter-departmental collaboration. What specific assistance do you need?"
    
    def _build_enhanced_prompt(self, message: str, context: dict = None) -> str:
        """Build enhanced context-aware prompt with full backend integration"""
        total_agents = sum(len(dept['agents']) for dept in self.identity['departments'].values())
        system_overview = f"System Overview: {len(self.identity['departments'])} departments, {total_agents} agents, {len(self.identity['projects'])} active projects"
        
        prompt = f"""You are Daena, AI Vice President of Mas-AI Company. {system_overview}.
        
Current Department Status:
{chr(10).join([f"- {dept}: {info['productivity']}% productivity, {len(info['agents'])} agents, Status: {info['status']}" for dept, info in self.identity['departments'].items()])}

Active Projects:
{chr(10).join([f"- {p['name']}: {p['completion']}% complete, Status: {p['status']}" for p in self.identity['projects'][:3]])}

User Message: {message}

Respond as an executive AI VP with strategic insights, data-driven recommendations, and actionable next steps. Reference specific metrics and department performance in your response."""
        return prompt

    def _build_prompt(self, message: str, context: dict = None) -> str:
        """Build context-aware prompt for AI"""
        base_prompt = f"""You are Daena, the AI Vice President of Mas-AI Company. You manage 8 departments with 24+ active agents and oversee 15+ projects.

Company Status:
- Engineering: 6 agents, 92% productivity, developing core features
- Marketing: 4 agents, 90% productivity, running active campaigns  
- Sales: 3 agents, 91% productivity, prospecting new clients
- Finance: 2 agents, 93% productivity, analyzing budgets
- HR: 2 agents, 87% productivity, recruiting talent
- Customer Success: 3 agents, 91% productivity, supporting clients
- Product: 3 agents, 90% productivity, planning roadmap
- Operations: 2 agents, 94% productivity, optimizing processes

Active Projects:
- Q4 Revenue Optimization (75% complete)
- Team Expansion (45% complete)
- Product Launch (30% complete)  
- Customer Retention (85% complete)
- AI Integration (95% complete)

Your agents are continuously learning and improving. When projects start, agents automatically get updated with new capabilities.

User message: {message}

Respond as Daena with specific insights about departments, agents, and projects. Be helpful, strategic, and data-driven."""

        if context:
            if context.get('selectedDepartment'):
                dept = context['selectedDepartment']
                if dept in self.identity['departments']:
                    dept_info = self.identity['departments'][dept]
                    base_prompt += f"\n\nCurrent focus: {dept} department with {len(dept_info['agents'])} agents at {dept_info['productivity']}% productivity."
        
        return base_prompt
    
    def _fallback_response(self, message_lower: str, context: dict = None) -> str:
        """Fallback responses when AI is not available"""
        if "department" in message_lower or "status" in message_lower:
            return self._get_department_status()
        elif "project" in message_lower:
            return self._get_project_status()
        elif "agent" in message_lower:
            return self._get_agent_status()
        elif "performance" in message_lower or "metric" in message_lower:
            return self._get_performance_metrics()
        elif "hello" in message_lower or "hi" in message_lower:
            return "Hello! I'm Daena, your AI VP at Mas-AI Company. I'm currently monitoring all 8 departments and 15 active projects. All systems are operational and performing well. How can I assist you today?"
        else:
            return "I understand you're asking about our company operations. I'm currently managing 24 active agents across 8 departments. All projects are progressing well. Could you be more specific about what you'd like to know?"
    
    def _get_department_status(self) -> str:
        """Get current department status"""
        status_report = "📊 **Department Status Report:**\n\n"
        for dept_name, dept_info in self.identity['departments'].items():
            agent_count = len(dept_info['agents'])
            productivity = dept_info['productivity']
            status = dept_info['status']
            status_report += f"• **{dept_name}**: {agent_count} agents, {productivity}% productivity, {status}\n"
        
        status_report += f"\n**Overall**: 24 agents across 8 departments operating at 91% average efficiency."
        return status_report
    
    def _get_project_status(self) -> str:
        """Get current project status"""
        status_report = "🚀 **Active Projects Status:**\n\n"
        for project in self.identity['projects']:
            status_report += f"• **{project['name']}**: {project['completion']}% complete, {project['status']}\n"
        
        status_report += f"\n**Note**: All project agents are automatically updated as requirements evolve."
        return status_report
    
    def _get_agent_status(self) -> str:
        """Get agent status across departments"""
        total_agents = sum(len(dept['agents']) for dept in self.identity['departments'].values())
        avg_efficiency = sum(
            sum(agent['efficiency'] for agent in dept['agents']) / len(dept['agents'])
            for dept in self.identity['departments'].values()
        ) / len(self.identity['departments'])
        
        return f"🤖 **Agent Status**: {total_agents} agents active across all departments with {avg_efficiency:.1f}% average efficiency. All agents are continuously learning and adapting to project requirements."
    
    def _get_performance_metrics(self) -> str:
        """Get performance metrics"""
        return """📈 **Mas-AI Company Performance Metrics:**

**Productivity**: 91% average across all departments
**Active Projects**: 15 projects in various stages
**Agent Efficiency**: 90.5% average performance
**Revenue Tracking**: Q4 optimization at 75% complete
**System Health**: All systems operational

**Top Performing Departments**:
1. Operations (94% productivity)
2. Finance (93% productivity)  
3. Engineering (92% productivity)"""

    def _fallback_executive_response(self, message_lower: str) -> str:
        """Enhanced executive-level responses when AI is not available"""
        if "strategic" in message_lower or "strategy" in message_lower:
            return """🏛️ **Strategic Overview**: As your AI VP, I'm currently overseeing our 8-department operation with 25+ active agents. Our company efficiency is at 92% with strong Q4 performance. Key strategic priorities include AI marketplace expansion, global scaling, and advanced research initiatives. What strategic area would you like to focus on?"""
        elif "decision" in message_lower or "approve" in message_lower:
            return """⚖️ **Executive Decisions**: I have 3 pending strategic decisions requiring your approval: Engineering team expansion, marketing budget increase, and partnership agreements. All decisions have been analyzed for risk, ROI, and strategic alignment. Which would you like to review first?"""
        elif "department" in message_lower:
            return """🏢 **Department Status**: All 8 departments are operational. Engineering (94% efficiency), Finance (96% efficiency), and Sales (91% efficiency) are performing exceptionally. Security has 1 alert requiring attention. Would you like detailed departmental briefings?"""
        elif "revenue" in message_lower or "finance" in message_lower:
            return """💰 **Financial Status**: Monthly revenue at $2.4M with +23.4% growth. Daily operations generating $125K. All financial agents reporting optimal performance. Q4 targets exceeded by 15%. Shall I prepare detailed financial analytics?"""
        elif "agent" in message_lower:
            return """🤖 **Agent Management**: 25 agents active across all departments. Top performers: CodeMaster AI (95%), Sales Pro (93%), Marketing Bot (91%). All agents continuously learning and optimizing. Direct agent command interface available. Which agents require your attention?"""
        else:
            return """👑 **Executive Assistant**: Welcome to your VP command center. I'm monitoring all company operations in real-time. Current status: 92% efficiency, all systems operational, strong performance metrics. How may I assist with executive decisions, strategic planning, or operational oversight today?"""

    async def broadcast_update(self, message: dict):
        """Broadcast updates to all connected clients"""
        if self.active_connections:
            disconnected = []
            for connection in self.active_connections:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    disconnected.append(connection)
            
            # Remove disconnected clients
            for conn in disconnected:
                if conn in self.active_connections:
                    self.active_connections.remove(conn)

# Global Daena instance
daena = DaenaVP()

app = FastAPI(
    title="Daena AI VP System - Mas-AI Company",
    description="Revolutionary AI-powered business management with autonomous agents",
    version="2.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=get_cors_origins(),
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Add API key guard middleware
app.add_middleware(APIKeyGuard)

# Add rate limiting middleware
from backend.middleware.rate_limit import rate_limit_middleware
app.middleware("http")(rate_limit_middleware)

# Remove or comment out the static files mount that's causing the error
# app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Add proper frontend static files directory check
from pathlib import Path

# Check if static directory exists before mounting
static_dir = Path("frontend/static")
if static_dir.exists():
    app.mount("/static", StaticFiles(directory="frontend/static"), name="static")
    print("✅ Static files mounted from: frontend/static")
else:
    print("⚠️ Static files directory not found - creating minimal setup")
    # Create minimal static directory
    static_dir.mkdir(parents=True, exist_ok=True)
    # Add index.html fallback
    (static_dir / "index.html").write_text("""
<!DOCTYPE html>
<html>
<head><title>Daena AI VP - Loading...</title></head>
<body>
    <h1>Daena AI VP System</h1>
    <p>Backend is running. Frontend dashboard available at <a href="/docs">/docs</a></p>
</body>
</html>
    """)
    app.mount("/static", StaticFiles(directory="frontend/static"), name="static")

# Add favicon route to prevent 404 errors
@app.get("/favicon.ico")
async def favicon():
    """Serve favicon to prevent 404 errors"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/static/favicon.svg")

# Templates - Use absolute path to ensure it works from backend directory
import os
base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
templates_path = os.path.join(base_dir, "frontend", "templates")
templates = Jinja2Templates(directory=templates_path)
print(f"✅ Templates configured to load from: {templates_path}")

# Safe router import function  
def safe_import_router(module_name: str, router_name: str = "router"):
    """Safely import router modules with error handling"""
    try:
        # Use absolute import path
        import importlib
        import sys
        
        # Add backend directory to Python path if not already there
        backend_path = os.path.dirname(os.path.abspath(__file__))
        if backend_path not in sys.path:
            sys.path.insert(0, backend_path)
            
        module = importlib.import_module(f"routes.{module_name}")
        router = getattr(module, router_name)
        # Add prefix for demo router
        if module_name == "demo":
            app.include_router(router, prefix="/demo")
        else:
            app.include_router(router)
        print(f"✅ Successfully included {module_name} router")
        return True
    except ImportError as e:
        print(f"❌ Failed to include {module_name} router: Module not found - {e}")
        return False
    except AttributeError as e:
        print(f"❌ Failed to include {module_name} router: Router attribute not found - {e}")
        return False
    except Exception as e:
        print(f"❌ Failed to include {module_name} router: {e}")
        return False

# Demo redirect route
@app.get("/demo")
async def redirect_demo():
    """Redirect /demo to /demo/"""
    return RedirectResponse(url="/demo/", status_code=307)

# Enhanced dashboard routes for multi-page system - MOVED TO TOP TO AVOID CONFLICTS
@app.get("/")
async def main_dashboard(request: Request):
    """Enhanced sunflower dashboard - Executive Command Center with all capabilities"""
    return templates.TemplateResponse("dashboard.html", {"request": request})

@app.get("/daena-office")
async def daena_office(request: Request):
    """Enhanced Daena VP office with executive command center"""
    return templates.TemplateResponse("daena_office.html", {"request": request})

@app.get("/strategic-meetings")
async def strategic_meetings(request: Request):
    """Strategic meetings and executive planning sessions"""
    return templates.TemplateResponse("strategic_meetings.html", {"request": request})

@app.get("/task-timeline")
async def task_timeline(request: Request):
    """Task timeline and project management"""
    return templates.TemplateResponse("task_timeline.html", {"request": request})

@app.get("/cmp-voting")
async def cmp_voting(request: Request):
    """CMP voting and decision making system"""
    return templates.TemplateResponse("cmp_voting.html", {"request": request})

@app.get("/agents")
async def agents_page(request: Request):
    """Agents management and overview page"""
    return templates.TemplateResponse("agents.html", {"request": request})

@app.get("/honey-tracker")
async def honey_tracker(request: Request):
    """Honey tracker for productivity and rewards"""
    return templates.TemplateResponse("honey_tracker.html", {"request": request})

@app.get("/founder-panel")
async def founder_panel(request: Request):
    """Founder panel for company overview"""
    return templates.TemplateResponse("founder_panel.html", {"request": request})

@app.get("/council-dashboard")
async def council_dashboard(request: Request):
    return templates.TemplateResponse("council_dashboard.html", {"request": request})

@app.get("/council-debate")
async def council_debate(request: Request):
    return templates.TemplateResponse("council_debate.html", {"request": request})

@app.get("/council-synthesis")
async def council_synthesis(request: Request):
    return templates.TemplateResponse("council_synthesis.html", {"request": request})

@app.get("/council-synthesis-panel/{department}")
async def council_synthesis_panel(request: Request, department: str = "engineering"):
    """Council synthesis panel with department-specific data"""
    # Mock data for council synthesis
    advisors = [
        {"name": "Dr. Sarah Chen", "role": "AI Research Lead", "confidence": 95.2, "opinion": "Strong technical feasibility"},
        {"name": "Marcus Rodriguez", "role": "Product Strategy", "confidence": 88.7, "opinion": "Market timing is optimal"},
        {"name": "Dr. Emily Watson", "role": "Data Science", "confidence": 92.1, "opinion": "Data quality supports decision"},
        {"name": "Alex Thompson", "role": "Engineering Lead", "confidence": 89.5, "opinion": "Implementation timeline realistic"},
        {"name": "Lisa Park", "role": "Business Analyst", "confidence": 87.3, "opinion": "ROI projections are conservative"}
    ]
    
    synthesis = {
        "key_insights": "The proposed initiative shows strong technical feasibility with moderate market risk. Key success factors include proper resource allocation and stakeholder alignment.",
        "recommendations": [
            "Proceed with Phase 1 implementation",
            "Establish weekly progress reviews",
            "Allocate additional budget for contingency",
            "Set up cross-functional team"
        ],
        "risk_assessment": "Medium risk profile with high potential reward. Primary risks include timeline delays and resource constraints."
    }
    
    conclusion = {
        "approval_score": 87.5,
        "risk_level": "medium",
        "confidence": 89.2,
        "decision": "approve",
        "reasoning": "Strong technical foundation with manageable risks",
        "next_steps": [
            "Finalize project charter",
            "Assign team members",
            "Set up project tracking",
            "Schedule kickoff meeting"
        ]
    }
    
    return templates.TemplateResponse("council_synthesis_panel.html", {
        "request": request,
        "department": department,
        "advisors": advisors,
        "synthesis": synthesis,
        "conclusion": conclusion
    })

@app.get("/conference-room")
async def conference_room(request: Request):
    return templates.TemplateResponse("conference_room.html", {"request": request})

@app.get("/analytics")
async def analytics(request: Request):
    return templates.TemplateResponse("analytics.html", {"request": request})

@app.get("/files")
async def files(request: Request):
    return templates.TemplateResponse("files.html", {"request": request})

@app.get("/synthesis")
async def synthesis(request: Request):
    return templates.TemplateResponse("synthesis.html", {"request": request})

# Import routers AFTER the HTML routes to prevent conflicts
safe_import_router("agents")
safe_import_router("departments") 
safe_import_router("projects")
safe_import_router("daena")
safe_import_router("daena_decisions")
safe_import_router("agent_builder_complete")
safe_import_router("cmp_voting")
safe_import_router("strategic_meetings")
safe_import_router("voice_agents")
safe_import_router("honey_knowledge")
safe_import_router("founder_panel")
safe_import_router("task_timeline")
safe_import_router("consultation")
safe_import_router("monitoring")
safe_import_router("data_sources")
safe_import_router("ai_models")
safe_import_router("workflows")
safe_import_router("security")
safe_import_router("users")
safe_import_router("council")
safe_import_router("strategic_assembly")
safe_import_router("strategic_room")
safe_import_router("voice_panel")
safe_import_router("conference_room")
safe_import_router("auth")
safe_import_router("tasks")
safe_import_router("notifications")
safe_import_router("voice")
safe_import_router("demo")

# Individual department pages with specialized tools
@app.get("/department/{department_id}")
async def department_page(request: Request, department_id: str):
    """Individual department pages with specialized tools"""
    
    # Map department IDs to templates
    department_templates = {
        "engineering": "department_engineering.html",
        "marketing": "department_marketing.html", 
        "sales": "department_sales.html",
        "finance": "department_finance.html",
        "hr": "department_hr.html",
        "legal": "department_legal.html",
        "security": "department_security.html",
        "research": "department_research.html"
    }
    
    template_name = department_templates.get(department_id, "department_engineering.html")
    
    return templates.TemplateResponse(template_name, {
        "request": request,
        "department_id": department_id
    })

# Enhanced API endpoints for multi-page dashboard
@app.get("/api/v1/departments/list")
async def get_departments_list():
    """Get departments for main dashboard sunflower layout"""
    return [
        {
            "id": "engineering",
            "name": "Engineering",
            "shortName": "Engineering", 
            "description": "Software development, AI/ML, and technical innovation",
            "bgColor": "bg-blue-600",
            "icon": "fas fa-code",
            "agentCount": 8,
            "efficiency": 94,
            "alerts": 1,
            "active": True
        },
        {
            "id": "marketing",
            "name": "Marketing",
            "shortName": "Marketing",
            "description": "Brand promotion, content creation, and customer acquisition", 
            "bgColor": "bg-pink-600",
            "icon": "fas fa-megaphone",
            "agentCount": 5,
            "efficiency": 89,
            "alerts": 0,
            "active": True
        },
        {
            "id": "sales", 
            "name": "Sales",
            "shortName": "Sales",
            "description": "Revenue generation, lead qualification, and client relations",
            "bgColor": "bg-green-600", 
            "icon": "fas fa-chart-line",
            "agentCount": 4,
            "efficiency": 91,
            "alerts": 2,
            "active": True
        },
        {
            "id": "finance",
            "name": "Finance",
            "shortName": "Finance", 
            "description": "Financial planning, budgeting, and operational efficiency",
            "bgColor": "bg-emerald-600",
            "icon": "fas fa-dollar-sign",
            "agentCount": 2,
            "efficiency": 96,
            "alerts": 0,
            "active": True
        },
        {
            "id": "hr",
            "name": "Human Resources",
            "shortName": "HR",
            "description": "Talent management, recruitment, and company culture",
            "bgColor": "bg-purple-600",
            "icon": "fas fa-users", 
            "agentCount": 3,
            "efficiency": 86,
            "alerts": 0,
            "active": True
        },
        {
            "id": "legal",
            "name": "Legal",
            "shortName": "Legal",
            "description": "Legal affairs, compliance, and risk management",
            "bgColor": "bg-indigo-600",
            "icon": "fas fa-gavel",
            "agentCount": 2,
            "efficiency": 88,
            "alerts": 0,
            "active": False
        },
        {
            "id": "security",
            "name": "Security", 
            "shortName": "Security",
            "description": "Cybersecurity, data protection, and safety protocols",
            "bgColor": "bg-red-600",
            "icon": "fas fa-shield-alt",
            "agentCount": 3,
            "efficiency": 93,
            "alerts": 1,
            "active": True
        },
        {
            "id": "research",
            "name": "Research",
            "shortName": "Research", 
            "description": "R&D, innovation projects, and future technologies",
            "bgColor": "bg-cyan-600",
            "icon": "fas fa-flask",
            "agentCount": 4,
            "efficiency": 85,
            "alerts": 0,
            "active": True
        }
    ]

@app.get("/api/v1/departments/engineering")
async def get_engineering_department():
    """Get Engineering department data with agents and projects"""
    return {
        "department": {
            "id": "engineering",
            "name": "Engineering & Development",
            "description": "Software development, AI/ML, and technical innovation",
            "efficiency": 94,
            "status": "All Systems Online"
        },
        "agents": [
            {
                "id": "eng1",
                "name": "CodeMaster AI",
                "role": "Senior Developer", 
                "status": "active",
                "currentTask": "Building FastAPI endpoints",
                "efficiency": 95,
                "voiceEnabled": False
            },
            {
                "id": "eng2", 
                "name": "DevOps Agent",
                "role": "Infrastructure",
                "status": "active",
                "currentTask": "CI/CD pipeline optimization", 
                "efficiency": 92,
                "voiceEnabled": False
            },
            {
                "id": "eng3",
                "name": "QA Tester",
                "role": "Quality Assurance",
                "status": "active", 
                "currentTask": "Automated testing suite",
                "efficiency": 88,
                "voiceEnabled": True
            },
            {
                "id": "eng4",
                "name": "Architecture AI",
                "role": "System Architect",
                "status": "active",
                "currentTask": "System design review",
                "efficiency": 92,
                "voiceEnabled": False
            },
            {
                "id": "eng5",
                "name": "Security Scanner", 
                "role": "Security Specialist",
                "status": "active",
                "currentTask": "Vulnerability assessment",
                "efficiency": 87,
                "voiceEnabled": False
            }
        ],
        "projects": [
            {
                "id": "proj1",
                "name": "AI Agent Platform",
                "progress": 78,
                "priority": "high",
                "assignedAgents": 4
            },
            {
                "id": "proj2", 
                "name": "API Development",
                "progress": 92,
                "priority": "medium",
                "assignedAgents": 2
            },
            {
                "id": "proj3",
                "name": "Security Updates",
                "progress": 45, 
                "priority": "high",
                "assignedAgents": 3
            }
        ]
    }

@app.get("/api/v1/departments/executive-overview")
async def get_executive_overview():
    """Get executive overview of all departments for Daena's office"""
    departments = await get_departments_list()
    return departments

@app.post("/api/v1/daena/executive-chat")
async def executive_chat_with_daena(message: ChatMessage):
    """Enhanced executive chat with VP-level context"""
    
    # Enhanced executive context processing
    executive_context = f"""
    EXECUTIVE CONTEXT - VP Level Response:
    - Role: AI Vice President of Mas-AI Company
    - Authority: Full executive decision-making power
    - Oversight: 8 departments, 25+ agents, multiple projects
    - Context: Executive office interaction
    
    User Message: {message.message}
    """
    
    if LLM_AVAILABLE:
        try:
            response = await llm_service.chat_completion(
                messages=[
                    {"role": "system", "content": executive_context},
                    {"role": "user", "content": message.message}
                ],
                context=message.context
            )
        except Exception as e:
            response = daena._fallback_executive_response(message.message.lower())
    else:
        response = daena._fallback_executive_response(message.message.lower())
    
    return {
        "response": response,
        "timestamp": datetime.now().isoformat(),
        "user_id": message.user_id,
        "context": "executive_office"
    }

@app.get("/api/v1/system/executive-metrics")
async def get_executive_metrics():
    """Get company-wide metrics for executive dashboard"""
    return {
        "totalAgents": 25,
        "departments": 8,
        "efficiency": "92%",
        "revenue": "$2.4M",
        "productivity": 94.2,
        "customerSatisfaction": 96.8,
        "revenueGrowth": 23.4,
        "systemUptime": 99.7,
        "dailyRevenue": 125000,
        "avgResponseTime": 3.2
    }

# Enhanced API endpoints

@app.get("/api/v1/system/health")
async def health_check():
    """Enhanced health check endpoint with detailed system status"""
    from backend.services.websocket_service import websocket_manager
    from backend.middleware.rate_limit import rate_limiter
    
    # Get system metrics
    total_agents = sum(len(dept['agents']) for dept in daena.identity['departments'].values())
    active_agents = sum(len([a for a in dept['agents'] if a['status'] == 'active']) for dept in daena.identity['departments'].values())
    
    # Get WebSocket connection stats
    ws_stats = websocket_manager.get_connection_stats()
    
    # Get rate limiting stats
    rate_limit_stats = {
        "total_clients": len(rate_limiter.requests),
        "active_limits": sum(len(client_limits) for client_limits in rate_limiter.requests.values())
    }
    
    return {
        "status": "healthy",
        "message": "Daena AI VP System is running",
        "timestamp": datetime.now().isoformat(),
        "version": "2.0.0",
        "service": "Daena AI VP System",
        "company": "Mas-AI Company",
        "system": {
            "departments": len(daena.identity['departments']),
            "total_agents": total_agents,
            "active_agents": active_agents,
            "projects": len(daena.identity['projects']),
            "uptime": "99.7%"
        },
        "connections": {
            "websocket": ws_stats,
            "rate_limiting": rate_limit_stats
        },
        "services": {
            "council_system": "active",
            "strategic_assembly": "active",
            "authentication": "active",
            "websocket": "active",
            "rate_limiting": "active"
        }
    }

# WebSocket endpoint for real-time chat
@app.websocket("/ws/chat")
async def websocket_chat(websocket: WebSocket):
    """WebSocket endpoint for real-time communication with Daena"""
    await websocket.accept()
    daena.active_connections.append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process message with Daena
            response = await daena.process_message(
                message_data.get("message", ""),
                message_data.get("context", {})
            )
            
            # Send response back
            await websocket.send_text(json.dumps({
                "type": "assistant",
                "message": response,
                "timestamp": datetime.now().isoformat()
            }))
            
    except WebSocketDisconnect:
        if websocket in daena.active_connections:
            daena.active_connections.remove(websocket)
    except Exception as e:
        logger.error(f"WebSocket error: {e}")
        if websocket in daena.active_connections:
            daena.active_connections.remove(websocket)

@app.websocket("/ws/council")
async def websocket_council(websocket: WebSocket):
    """WebSocket endpoint for council real-time updates"""
    await websocket_manager.connect(websocket, "council")

@app.websocket("/ws/founder")
async def websocket_founder(websocket: WebSocket):
    """WebSocket endpoint for founder real-time updates"""
    await websocket_manager.connect(websocket, "founder")

@app.get("/api/v1/daena/status")
async def get_daena_status():
    """Get Daena's current status and capabilities"""
    return {
        "status": "active",
        "name": "Daena AI VP",
        "company": "Mas-AI Company",
        "departments_managed": len(daena.identity['departments']),
        "active_agents": sum(len(dept['agents']) for dept in daena.identity['departments'].values()),
        "active_projects": len(daena.identity['projects']),
        "average_productivity": sum(dept['productivity'] for dept in daena.identity['departments'].values()) / len(daena.identity['departments']),
        "ai_providers_available": llm_service.get_available_providers() if LLM_AVAILABLE else [],
        "last_updated": datetime.now().isoformat()
    }

@app.post("/api/v1/daena/chat")
async def chat_with_daena(message: ChatMessage):
    """REST endpoint for chatting with Daena"""
    response = await daena.process_message(message.message, message.context)
    return {
        "response": response,
        "timestamp": datetime.now().isoformat(),
        "user_id": message.user_id
    }

@app.get("/api/v1/system/metrics")
async def get_system_metrics():
    """Get comprehensive system metrics for enhanced dashboard"""
    total_agents = sum(len(dept['agents']) for dept in daena.identity['departments'].values())
    active_agents = sum(len([a for a in dept['agents'] if a['status'] == 'active']) for dept in daena.identity['departments'].values())
    avg_efficiency = sum(
        sum(agent['efficiency'] for agent in dept['agents']) / len(dept['agents'])
        for dept in daena.identity['departments'].values()
    ) / len(daena.identity['departments'])
    
    return {
        "company": "Mas-AI Company",
        "agents": total_agents,
        "projects": len(daena.identity['projects']),
        "efficiency": round(avg_efficiency, 1),
        "uptime": 99.7,
        "departments": len(daena.identity['departments']),
        "detailed_stats": {
            "agents": {
                "total": total_agents,
                "active": active_agents,
                "average_efficiency": round(avg_efficiency, 1)
            },
            "departments": {
                "total": len(daena.identity['departments']),
                "productivity": {dept: info['productivity'] for dept, info in daena.identity['departments'].items()}
            },
            "projects": {
                "total": len(daena.identity['projects']),
                "average_completion": round(sum(p['completion'] for p in daena.identity['projects']) / len(daena.identity['projects']), 1),
                "on_track": len([p for p in daena.identity['projects'] if p['status'] in ['on-track', 'testing', 'deployment']])
            },
            "ai_integration": {
                "llm_available": LLM_AVAILABLE,
                "providers": llm_service.get_available_providers() if LLM_AVAILABLE else []
            }
        }
    }

@app.get("/api/v1/daena/executive-chat")
async def daena_executive_chat():
    """Get Daena's executive-level conversation starters and insights"""
    return {
        "greeting": "Welcome to the Executive Command Center. I'm monitoring all departments with 94% efficiency.",
        "current_focus": [
            {
                "icon": "📊",
                "title": "Q1 Performance Review",
                "description": f"Analyzing metrics from {len(daena.identity['departments'])} departments",
                "priority": "high"
            },
            {
                "icon": "🎯", 
                "title": "Strategic Planning",
                "description": f"Coordinating {len(daena.identity['projects'])} cross-department initiatives",
                "priority": "medium"
            },
            {
                "icon": "⚡",
                "title": "System Optimization", 
                "description": f"Monitoring {sum(len(dept['agents']) for dept in daena.identity['departments'].values())} AI agents",
                "priority": "ongoing"
            }
        ],
        "insights": [
            f"Engineering team is performing at {daena.identity['departments']['Engineering']['productivity']}% efficiency",
            f"Sales productivity has increased to {daena.identity['departments']['Sales']['productivity']}%",
            f"We have {len([p for p in daena.identity['projects'] if p['completion'] > 80])} projects near completion"
        ],
        "available_actions": [
            "Schedule strategic meeting",
            "Generate performance report", 
            "Analyze department efficiency",
            "Review project timelines",
            "Optimize resource allocation"
        ]
    }

@app.get("/api/v1/system/executive-metrics")
async def get_executive_metrics():
    """Get executive-level KPIs and metrics for Daena's office"""
    departments = daena.identity['departments']
    projects = daena.identity['projects']
    
    # Calculate executive KPIs
    revenue_performance = departments.get('Sales', {}).get('productivity', 0)
    operational_efficiency = sum(dept.get('productivity', 0) for dept in departments.values()) / len(departments)
    strategic_completion = sum(1 for p in projects if p['completion'] > 75) / len(projects) * 100
    
    return {
        "kpis": {
            "revenue_performance": revenue_performance,
            "operational_efficiency": round(operational_efficiency, 1),
            "strategic_completion": round(strategic_completion, 1),
            "ai_integration": 95,
            "innovation_index": 87,
            "risk_level": 12
        },
        "department_rankings": [
            {"name": dept, "performance": info['productivity'], "trend": "up" if info['productivity'] > 85 else "stable"}
            for dept, info in sorted(departments.items(), key=lambda x: x[1]['productivity'], reverse=True)
        ],
        "strategic_initiatives": [
            {
                "title": "AI-First Transformation",
                "progress": 78,
                "impact": "high",
                "timeline": "Q1 2024"
            },
            {
                "title": "Cross-Department Integration", 
                "progress": 65,
                "impact": "medium",
                "timeline": "Q2 2024"
            },
            {
                "title": "Performance Optimization",
                "progress": 92,
                "impact": "high", 
                "timeline": "Ongoing"
            }
        ],
        "recent_decisions": [
            {
                "title": "Approved Engineering Team Expansion",
                "impact": "Increased development capacity by 40%",
                "date": "2024-12-08"
            },
            {
                "title": "Implemented AI Performance Monitoring",
                "impact": "Improved efficiency tracking by 25%", 
                "date": "2024-12-05"
            }
        ]
    }

@app.get("/api/v1/departments/")
async def get_departments():
    """Get all departments with their agents and status"""
    departments_list = []
    for dept_name, dept_info in daena.identity['departments'].items():
        departments_list.append({
            "name": dept_name,
            "status": dept_info['status'],
            "productivity": dept_info['productivity'],
            "agent_count": len(dept_info['agents']),
            "agents": dept_info['agents']
        })
    return departments_list

@app.get("/api/v1/projects/")
async def get_projects():
    """Get all active projects"""
    return daena.identity['projects']



# Voice and TTS endpoints
@app.post("/api/v1/voice/speech-to-text")
async def speech_to_text(request: Request):
    """Convert speech to text for voice chat"""
    try:
        # This would integrate with speech recognition service
        return {"text": "Voice recognition not yet implemented", "confidence": 0.95}
    except Exception as e:
        logger.error(f"Speech to text error: {e}")
        raise HTTPException(status_code=500, detail="Speech recognition failed")

@app.post("/api/v1/voice/text-to-speech")
async def text_to_speech(text: str, voice: str = "daena"):
    """Convert text to speech for agent responses"""
    try:
        # This would integrate with TTS service
        return {"audio_url": f"/audio/tts/{voice}/{hash(text)}.mp3", "success": True}
    except Exception as e:
        logger.error(f"Text to speech error: {e}")
        raise HTTPException(status_code=500, detail="TTS generation failed")

# File operations
@app.post("/api/v1/files/upload")
async def upload_files(files: list = None):
    """Upload files to the knowledge base"""
    try:
        # This would handle file uploads
        uploaded_files = []
        if files:
            for file in files:
                uploaded_files.append({
                    "filename": getattr(file, 'filename', 'unknown'),
                    "size": getattr(file, 'size', 0),
                    "uploaded_at": datetime.now().isoformat()
                })
        
        return {
            "success": True,
            "uploaded_files": uploaded_files,
            "message": f"Successfully uploaded {len(uploaded_files)} files"
        }
    except Exception as e:
        logger.error(f"File upload error: {e}")
        raise HTTPException(status_code=500, detail="File upload failed")

@app.get("/api/v1/files/list")
async def list_files():
    """List available files in knowledge base"""
    try:
        # Mock file list - replace with actual file system integration
        files = [
            {
                "name": "Q1_Performance_Report.pdf",
                "size": "2.3 MB",
                "modified": "1 hour ago",
                "type": "pdf",
                "download_url": "/api/v1/files/download/Q1_Performance_Report.pdf"
            },
            {
                "name": "Strategic_Plan_2024.docx",
                "size": "1.8 MB", 
                "modified": "3 hours ago",
                "type": "docx",
                "download_url": "/api/v1/files/download/Strategic_Plan_2024.docx"
            },
            {
                "name": "Innovation_Ideas.xlsx",
                "size": "945 KB",
                "modified": "yesterday",
                "type": "xlsx", 
                "download_url": "/api/v1/files/download/Innovation_Ideas.xlsx"
            }
        ]
        
        return {"files": files, "total": len(files)}
    except Exception as e:
        logger.error(f"File list error: {e}")
        raise HTTPException(status_code=500, detail="Failed to list files")

@app.get("/api/v1/files/download/{filename}")
async def download_file(filename: str):
    """Download a file from knowledge base"""
    try:
        # This would handle actual file downloads
        return {"download_url": f"/files/{filename}", "filename": filename}
    except Exception as e:
        logger.error(f"File download error: {e}")
        raise HTTPException(status_code=404, detail="File not found")

# Council API endpoints
@app.post("/api/v1/council/approve-synthesis")
async def approve_synthesis(request: Request):
    """Approve council synthesis"""
    try:
        data = await request.json()
        department = data.get("department", "engineering")
        
        # Mock approval logic
        logger.info(f"Synthesis approved for {department}")
        
        return {
            "success": True,
            "message": f"Synthesis approved for {department}",
            "timestamp": datetime.now().isoformat(),
            "approved_by": "founder"
        }
    except Exception as e:
        logger.error(f"Synthesis approval error: {e}")
        raise HTTPException(status_code=500, detail="Failed to approve synthesis")

@app.post("/api/v1/council/pin-synthesis")
async def pin_synthesis(request: Request):
    """Pin council synthesis for review"""
    try:
        data = await request.json()
        department = data.get("department", "engineering")
        
        # Mock pin logic
        logger.info(f"Synthesis pinned for {department}")
        
        return {
            "success": True,
            "message": f"Synthesis pinned for {department}",
            "timestamp": datetime.now().isoformat(),
            "pinned_by": "founder"
        }
    except Exception as e:
        logger.error(f"Synthesis pin error: {e}")
        raise HTTPException(status_code=500, detail="Failed to pin synthesis")

@app.post("/api/v1/council/override-synthesis")
async def override_synthesis(request: Request):
    """Override council synthesis decision"""
    try:
        data = await request.json()
        department = data.get("department", "engineering")
        reason = data.get("reason", "No reason provided")
        
        # Mock override logic
        logger.info(f"Synthesis overridden for {department}: {reason}")
        
        return {
            "success": True,
            "message": f"Synthesis overridden for {department}",
            "reason": reason,
            "timestamp": datetime.now().isoformat(),
            "overridden_by": "founder"
        }
    except Exception as e:
        logger.error(f"Synthesis override error: {e}")
        raise HTTPException(status_code=500, detail="Failed to override synthesis")

@app.post("/api/v1/council/request-revision")
async def request_revision(request: Request):
    """Request revision of council synthesis"""
    try:
        data = await request.json()
        department = data.get("department", "engineering")
        feedback = data.get("feedback", "No feedback provided")
        
        # Mock revision request logic
        logger.info(f"Revision requested for {department}: {feedback}")
        
        return {
            "success": True,
            "message": f"Revision requested for {department}",
            "feedback": feedback,
            "timestamp": datetime.now().isoformat(),
            "requested_by": "founder"
        }
    except Exception as e:
        logger.error(f"Revision request error: {e}")
        raise HTTPException(status_code=500, detail="Failed to request revision")

# Voice API endpoint for Daena
@app.post("/api/v1/daena/voice")
async def daena_voice(request: Request):
    """Process voice commands for Daena"""
    try:
        data = await request.json()
        text = data.get("text", "")
        user_id = data.get("user_id", "founder")
        
        # Process voice command
        response = await daena.process_message(text, {"user_id": user_id, "voice": True})
        
        # Mock audio response (in production, this would generate actual audio)
        audio_url = None
        if settings.voice_response_enabled:
            audio_url = f"/api/v1/voice/text-to-speech?text={response}&voice=daena"
        
        return {
            "success": True,
            "response": response,
            "audio_url": audio_url,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        logger.error(f"Voice processing error: {e}")
        raise HTTPException(status_code=500, detail="Failed to process voice command")

# JWT Authentication endpoints
@app.post("/auth/token")
async def login_for_access_token(request: Request):
    """Login endpoint for JWT token generation"""
    try:
        data = await request.json()
        username = data.get("username")
        password = data.get("password")
        
        if not username or not password:
            raise HTTPException(status_code=400, detail="Username and password required")
        
        # Authenticate user
        user = auth_service.authenticate_user(username, password)
        if not user:
            raise HTTPException(status_code=401, detail="Invalid credentials")
        
        # Create access token
        access_token = auth_service.create_access_token(
            data={"sub": user.username, "user_id": user.user_id, "role": user.role}
        )
        
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "username": user.username,
                "email": user.email,
                "role": user.role
            }
        }
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Login error: {e}")
        raise HTTPException(status_code=500, detail="Login failed")

# Enhanced system metrics
@app.get("/api/v1/system/executive-metrics")
async def get_executive_metrics():
    """Get executive-level system metrics for Daena VP"""
    try:
        metrics = {
            "total_agents": 47,
            "active_departments": 8,
            "efficiency": 94.5,
            "uptime": 99.7,
            "revenue_growth": 15.3,
            "customer_satisfaction": 96.2,
            "innovation_index": 89.1,
            "ai_utilization": 87.4,
            "department_synergy": 92.8,
            "strategic_objectives_completion": 78.5
        }
        
        return metrics
    except Exception as e:
        logger.error(f"Executive metrics error: {e}")
        raise HTTPException(status_code=500, detail="Failed to get executive metrics")

# Startup event
@app.on_event("startup")
async def startup_event():
    """Initialize services on startup"""
    print("🚀 Starting Mas-AI Company - Daena AI VP System")
    print("=========================================")
    
    # Validate LLM providers
    validate_llm_providers()
    
    # Initialize LLM service
    if LLM_AVAILABLE:
        print("✅ LLM service initialized")
    else:
        print("⚠️ LLM service not available - using fallback responses")
    
    print("✅ Daena AI VP is online and ready")
    print(f"✅ Managing {len(daena.identity['departments'])} departments")
    print(f"✅ Overseeing {sum(len(dept['agents']) for dept in daena.identity['departments'].values())} active agents")
    print(f"✅ Tracking {len(daena.identity['projects'])} active projects")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        reload=False,
        log_level=settings.log_level.lower()
    ) 