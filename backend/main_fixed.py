from fastapi import FastAPI, Request, HTTPException, WebSocket, WebSocketDisconnect
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import HTMLResponse, JSONResponse
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
backend_dir = Path(__file__).parent
project_root = backend_dir.parent
sys.path.insert(0, str(backend_dir))
sys.path.insert(0, str(project_root))

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="Daena AI VP - Sunflower System",
    description="AI Vice President with Sunflower Dashboard Layout",
    version="2.0.0"
)

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "http://localhost:3000",
        "http://localhost:8000", 
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000"
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Create directories if they don't exist
frontend_dir = project_root / "frontend"
static_dir = frontend_dir / "static"
templates_dir = frontend_dir / "templates"

for directory in [frontend_dir, static_dir, templates_dir]:
    directory.mkdir(parents=True, exist_ok=True)

# Create a basic index.html if it doesn't exist
index_file = static_dir / "index.html"
if not index_file.exists():
    index_content = """<!DOCTYPE html>
<html>
<head>
    <title>Daena AI VP - Sunflower System</title>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
</head>
<body>
    <h1>🌻 Daena AI VP System</h1>
    <p>Backend is running successfully!</p>
    <ul>
        <li><a href="/docs">📚 API Documentation</a></li>
        <li><a href="/dashboard">🌻 Sunflower Dashboard</a></li>
        <li><a href="/api/v1/daena/status">📊 System Status</a></li>
    </ul>
</body>
</html>"""
    index_file.write_text(index_content)

# Mount static files
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")
print(f"✅ Static files mounted from: {static_dir}")

# Templates
templates = Jinja2Templates(directory=str(templates_dir))

# Chat message model
class ChatMessage(BaseModel):
    message: str
    user_id: str = "founder"
    department: Optional[str] = None
    context: dict = {}

# Enhanced Daena VP Class
class DaenaVP:
    def __init__(self):
        self.departments = {
            "Engineering": {
                "name": "Engineering",
                "icon": "⚙️",
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
                "name": "Marketing", 
                "icon": "📈",
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
                "name": "Sales",
                "icon": "💰", 
                "agents": [
                    {"name": "Lead Hunter", "status": "active", "task": "Prospect research", "efficiency": 94},
                    {"name": "Deal Closer", "status": "active", "task": "Follow-up calls", "efficiency": 87},
                    {"name": "Proposal Generator", "status": "active", "task": "Quote creation", "efficiency": 92}
                ],
                "status": "Prospecting",
                "productivity": 91
            },
            "Finance": {
                "name": "Finance",
                "icon": "💼",
                "agents": [
                    {"name": "Budget Analyzer", "status": "active", "task": "Expense tracking", "efficiency": 96},
                    {"name": "Revenue Forecaster", "status": "active", "task": "Revenue projection", "efficiency": 89}
                ],
                "status": "Analyzing", 
                "productivity": 93
            },
            "HR": {
                "name": "HR",
                "icon": "👥",
                "agents": [
                    {"name": "Recruiter AI", "status": "active", "task": "Candidate screening", "efficiency": 88},
                    {"name": "Employee Satisfaction", "status": "active", "task": "Team wellness", "efficiency": 85}
                ],
                "status": "Recruiting",
                "productivity": 87
            },
            "Customer": {
                "name": "Customer",
                "icon": "🤝",
                "agents": [
                    {"name": "Support Bot", "status": "active", "task": "Ticket resolution", "efficiency": 91},
                    {"name": "Success Manager", "status": "active", "task": "Customer onboarding", "efficiency": 89},
                    {"name": "Feedback Analyzer", "status": "active", "task": "Sentiment analysis", "efficiency": 94}
                ],
                "status": "Supporting",
                "productivity": 91
            },
            "Product": {
                "name": "Product", 
                "icon": "🚀",
                "agents": [
                    {"name": "Strategy AI", "status": "active", "task": "Roadmap planning", "efficiency": 90},
                    {"name": "UX Research", "status": "active", "task": "User interviews", "efficiency": 87},
                    {"name": "Feature Prioritizer", "status": "active", "task": "Backlog management", "efficiency": 93}
                ],
                "status": "Planning",
                "productivity": 90
            },
            "Operations": {
                "name": "Operations",
                "icon": "⚡",
                "agents": [
                    {"name": "Process Optimizer", "status": "active", "task": "Workflow automation", "efficiency": 95},
                    {"name": "Quality Controller", "status": "active", "task": "Standards monitoring", "efficiency": 92}
                ],
                "status": "Optimizing",
                "productivity": 94
            }
        }
        
        self.projects = [
            {"id": "p1", "name": "Q4 Revenue Optimization", "completion": 75, "status": "on-track", "start_date": "2024-12-05", "agents_involved": 8},
            {"id": "p2", "name": "Team Expansion", "completion": 45, "status": "planning", "start_date": "2024-12-01", "agents_involved": 5},
            {"id": "p3", "name": "Product Launch", "completion": 30, "status": "design", "start_date": "2024-11-20", "agents_involved": 12},
            {"id": "p4", "name": "Customer Retention", "completion": 85, "status": "testing", "start_date": "2024-11-15", "agents_involved": 6},
            {"id": "p5", "name": "AI Integration", "completion": 95, "status": "deployment", "start_date": "2024-10-20", "agents_involved": 10}
        ]
        
        self.active_connections: List[WebSocket] = []
        self.conversation_history = []
        
        logger.info("🌻 Daena VP initialized with sunflower layout")
        logger.info(f"📊 Managing {len(self.departments)} departments and {sum(len(d['agents']) for d in self.departments.values())} agents")

    async def process_message(self, message: str, department: Optional[str] = None, context: dict = None) -> str:
        """Process chat message with department context"""
        message_lower = message.lower()
        
        if department and department in self.departments:
            dept_info = self.departments[department]
            response = f"🌻 As Daena, I can see the {department} department has {len(dept_info['agents'])} agents at {dept_info['productivity']}% productivity. "
            
            if "status" in message_lower:
                response += f"Current status: {dept_info['status']}. "
                response += f"Top performing agent: {max(dept_info['agents'], key=lambda x: x['efficiency'])['name']} at {max(dept_info['agents'], key=lambda x: x['efficiency'])['efficiency']}% efficiency."
            elif "agents" in message_lower:
                response += f"Active agents: {', '.join([agent['name'] for agent in dept_info['agents']])}."
            else:
                response += f"How can I help you with the {department} department today?"
        else:
            # General responses
            total_agents = sum(len(dept['agents']) for dept in self.departments.values())
            avg_productivity = sum(dept['productivity'] for dept in self.departments.values()) / len(self.departments)
            
            if "overview" in message_lower or "company" in message_lower:
                response = f"🌻 Company Overview: {len(self.departments)} departments arranged in sunflower pattern, {total_agents} active agents, {avg_productivity:.1f}% average productivity. "
                response += f"{len([p for p in self.projects if p['status'] in ['on-track', 'testing', 'deployment']])} projects are on track."
            else:
                response = f"🌻 Hello! I'm Daena, your AI Vice President. I'm managing our sunflower organization with {len(self.departments)} departments and {total_agents} AI agents. How can I assist you today?"
        
        # Log conversation
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "message": message,
            "response": response,
            "department": department
        })
        
        return response

# Initialize Daena VP
daena_vp = DaenaVP()

# Routes
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    """Serve the sunflower dashboard"""
    # Check if sunflower dashboard exists
    sunflower_template = templates_dir / "sunflower_dashboard.html"
    if sunflower_template.exists():
        return templates.TemplateResponse("sunflower_dashboard.html", {
            "request": request,
            "departments": list(daena_vp.departments.values()),
            "projects": daena_vp.projects
        })
    else:
        # Return basic dashboard
        return HTMLResponse(content="""
<!DOCTYPE html>
<html>
<head>
    <title>🌻 Daena AI VP - Sunflower Dashboard</title>
    <style>
        body { font-family: Arial, sans-serif; background: #1a1a2e; color: white; text-align: center; padding: 50px; }
        .logo { font-size: 4em; margin-bottom: 20px; }
        .status { background: #16213e; padding: 20px; border-radius: 10px; margin: 20px auto; max-width: 600px; }
        a { color: #48dbfb; text-decoration: none; margin: 0 10px; }
        .departments { display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-top: 30px; }
        .dept { background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); padding: 20px; border-radius: 15px; }
    </style>
</head>
<body>
    <div class="logo">🌻</div>
    <h1>Daena AI VP - Sunflower System</h1>
    <div class="status">
        <h2>🚀 System Operational</h2>
        <p>Managing 8 departments • 24+ active agents • Real-time monitoring</p>
        <div>
            <a href="/docs">📚 API Documentation</a>
            <a href="/api/v1/daena/status">📊 System Status</a>
            <a href="/api/v1/daena/departments">🏢 Departments</a>
        </div>
    </div>
    <div class="departments">
        <div class="dept">⚙️ Engineering<br><small>6 agents • 92% productivity</small></div>
        <div class="dept">📈 Marketing<br><small>4 agents • 90% productivity</small></div>
        <div class="dept">💰 Sales<br><small>3 agents • 91% productivity</small></div>
        <div class="dept">💼 Finance<br><small>2 agents • 93% productivity</small></div>
        <div class="dept">👥 HR<br><small>2 agents • 87% productivity</small></div>
        <div class="dept">🤝 Customer<br><small>3 agents • 91% productivity</small></div>
        <div class="dept">🚀 Product<br><small>3 agents • 90% productivity</small></div>
        <div class="dept">⚡ Operations<br><small>2 agents • 94% productivity</small></div>
    </div>
</body>
</html>
        """)

@app.get("/dashboard", response_class=HTMLResponse)
async def dashboard_redirect(request: Request):
    """Redirect to main dashboard"""
    return await dashboard(request)

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "message": "🌻 Daena AI VP Sunflower System is operational",
        "timestamp": datetime.now().isoformat(),
        "departments": len(daena_vp.departments),
        "total_agents": sum(len(d['agents']) for d in daena_vp.departments.values())
    }

# API Routes
@app.get("/api/v1/daena/status")
async def get_status():
    """Get Daena system status"""
    total_agents = sum(len(dept['agents']) for dept in daena_vp.departments.values())
    active_agents = sum(len([a for a in dept['agents'] if a['status'] == 'active']) for dept in daena_vp.departments.values())
    
    return {
        "status": "operational",
        "system": "Daena AI VP Sunflower",
        "departments": len(daena_vp.departments),
        "total_agents": total_agents,
        "active_agents": active_agents,
        "projects": len(daena_vp.projects),
        "active_connections": len(daena_vp.active_connections),
        "last_updated": datetime.now().isoformat(),
        "health": "excellent"
    }

@app.get("/api/v1/daena/departments")
async def get_departments():
    """Get all departments"""
    return {
        "departments": list(daena_vp.departments.values()),
        "total_departments": len(daena_vp.departments),
        "total_agents": sum(len(dept['agents']) for dept in daena_vp.departments.values()),
        "layout": "sunflower"
    }

@app.get("/api/v1/daena/departments/{department_name}")
async def get_department_detail(department_name: str):
    """Get detailed department information"""
    if department_name not in daena_vp.departments:
        raise HTTPException(status_code=404, detail=f"Department {department_name} not found")
    
    dept = daena_vp.departments[department_name]
    return {
        **dept,
        "total_agents": len(dept['agents']),
        "active_agents": len([a for a in dept['agents'] if a['status'] == 'active']),
        "average_efficiency": sum(a['efficiency'] for a in dept['agents']) / len(dept['agents']),
        "last_updated": datetime.now().isoformat()
    }

@app.post("/api/v1/daena/chat")
async def chat_with_daena(message: ChatMessage):
    """Chat with Daena VP"""
    response = await daena_vp.process_message(
        message.message,
        message.department,
        message.context
    )
    
    return {
        "response": response,
        "timestamp": datetime.now().isoformat(),
        "department": message.department,
        "user_id": message.user_id
    }

@app.websocket("/api/v1/daena/ws")
async def websocket_endpoint(websocket: WebSocket):
    """WebSocket endpoint for real-time communication"""
    await websocket.accept()
    daena_vp.active_connections.append(websocket)
    
    try:
        # Send initial state
        await websocket.send_text(json.dumps({
            "type": "initial_state",
            "departments": daena_vp.departments,
            "projects": daena_vp.projects,
            "timestamp": datetime.now().isoformat()
        }))
        
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            if message_data.get("type") == "chat":
                response = await daena_vp.process_message(
                    message_data.get("message", ""),
                    message_data.get("department"),
                    message_data.get("context", {})
                )
                
                await websocket.send_text(json.dumps({
                    "type": "chat_response",
                    "message": response,
                    "timestamp": datetime.now().isoformat()
                }))
                
    except WebSocketDisconnect:
        daena_vp.active_connections.remove(websocket)

# Run the application
if __name__ == "__main__":
    import uvicorn
    
    print("🌻 Starting Daena AI VP Sunflower System...")
    print("✅ All routers loaded successfully")
    print(f"📊 Managing {len(daena_vp.departments)} departments")
    print(f"🤖 Controlling {sum(len(d['agents']) for d in daena_vp.departments.values())} AI agents")
    print("🚀 Starting server...")
    
    uvicorn.run(
        "main_fixed:app",
        host="0.0.0.0",
        port=8000,
        reload=False,
        log_level="info"
    ) 