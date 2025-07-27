from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/projects", tags=["projects"])

# Get templates directory
project_root = Path(__file__).parent.parent.parent
templates_dir = project_root / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Enhanced projects with comprehensive tracking
PROJECTS = [
    {
        "id": "proj_001",
        "name": "AI Agent Builder Platform",
        "description": "No-code platform for building custom AI agents",
        "client": "Internal Product",
        "status": "active",
        "progress": 75,
        "timeline": "6 months",
        "start_date": "2024-01-01",
        "end_date": "2024-06-30",
        "team_size": 8,
        "revenue": 0,  # Internal project
        "budget": 150000,
        "departments_involved": ["Engineering", "Product", "Marketing"],
        "agents_assigned": [
            {"id": "eng_lead", "name": "Alex CodeMaster", "department": "Engineering", "contribution": 30},
            {"id": "prod_manager", "name": "Casey Vision", "department": "Product", "contribution": 25},
            {"id": "marketing_lead", "name": "Jordan Brand", "department": "Marketing", "contribution": 20}
        ],
        "milestones": [
            {"id": 1, "name": "MVP Development", "status": "completed", "due_date": "2024-03-15"},
            {"id": 2, "name": "Beta Testing", "status": "in_progress", "due_date": "2024-04-30"},
            {"id": 3, "name": "Public Launch", "status": "pending", "due_date": "2024-06-15"}
        ],
        "risks": [
            {"level": "medium", "description": "Technical complexity of no-code interface"},
            {"level": "low", "description": "Market competition from existing platforms"}
        ],
        "client_feedback": [
            {"date": "2024-01-15", "rating": 5, "comment": "Excellent progress on MVP development"},
            {"date": "2024-01-10", "rating": 4, "comment": "UI/UX design exceeds expectations"}
        ],
        "daena_decisions": [
            {"timestamp": "2024-01-15T10:30:00Z", "decision": "Approved additional resources for beta testing"},
            {"timestamp": "2024-01-10T14:20:00Z", "decision": "Prioritized user experience over feature complexity"}
        ]
    },
    {
        "id": "proj_002",
        "name": "Enterprise AI Integration",
        "description": "Custom AI solution for TechCorp enterprise client",
        "client": "TechCorp Inc.",
        "status": "active",
        "progress": 45,
        "timeline": "4 months",
        "start_date": "2024-02-01",
        "end_date": "2024-05-31",
        "team_size": 6,
        "revenue": 125000,
        "budget": 80000,
        "departments_involved": ["Engineering", "Sales", "Legal"],
        "agents_assigned": [
            {"id": "eng_dev", "name": "Sam Builder", "department": "Engineering", "contribution": 40},
            {"id": "sales_lead", "name": "Morgan Closer", "department": "Sales", "contribution": 30},
            {"id": "legal_counsel", "name": "Justice Law", "department": "Legal", "contribution": 15}
        ],
        "milestones": [
            {"id": 1, "name": "Requirements Analysis", "status": "completed", "due_date": "2024-02-15"},
            {"id": 2, "name": "Development Phase", "status": "in_progress", "due_date": "2024-04-15"},
            {"id": 3, "name": "Testing & Deployment", "status": "pending", "due_date": "2024-05-15"}
        ],
        "risks": [
            {"level": "high", "description": "Complex enterprise security requirements"},
            {"level": "medium", "description": "Client timeline constraints"}
        ],
        "client_feedback": [
            {"date": "2024-01-15", "rating": 5, "comment": "Excellent communication and technical expertise"},
            {"date": "2024-01-08", "rating": 4, "comment": "Requirements gathering was thorough and professional"}
        ],
        "daena_decisions": [
            {"timestamp": "2024-01-15T11:00:00Z", "decision": "Approved security audit for enterprise client"},
            {"timestamp": "2024-01-08T16:45:00Z", "decision": "Allocated additional engineering resources"}
        ]
    },
    {
        "id": "proj_003",
        "name": "Marketing Automation Suite",
        "description": "AI-powered marketing automation platform for startups",
        "client": "GrowthStart Ventures",
        "status": "active",
        "progress": 60,
        "timeline": "5 months",
        "start_date": "2024-01-15",
        "end_date": "2024-06-15",
        "team_size": 5,
        "revenue": 85000,
        "budget": 60000,
        "departments_involved": ["Engineering", "Marketing", "Product"],
        "agents_assigned": [
            {"id": "eng_devops", "name": "Jordan Deploy", "department": "Engineering", "contribution": 35},
            {"id": "marketing_specialist", "name": "Avery Growth", "department": "Marketing", "contribution": 30},
            {"id": "prod_designer", "name": "Taylor Creator", "department": "Product", "contribution": 25}
        ],
        "milestones": [
            {"id": 1, "name": "Platform Architecture", "status": "completed", "due_date": "2024-02-28"},
            {"id": 2, "name": "Core Features", "status": "in_progress", "due_date": "2024-04-30"},
            {"id": 3, "name": "Integration Testing", "status": "pending", "due_date": "2024-05-30"}
        ],
        "risks": [
            {"level": "medium", "description": "Integration with third-party marketing tools"},
            {"level": "low", "description": "Client adoption timeline"}
        ],
        "client_feedback": [
            {"date": "2024-01-14", "rating": 4, "comment": "Platform architecture looks promising"},
            {"date": "2024-01-05", "rating": 5, "comment": "Team is very responsive to our needs"}
        ],
        "daena_decisions": [
            {"timestamp": "2024-01-14T13:15:00Z", "decision": "Approved third-party integrations budget"},
            {"timestamp": "2024-01-05T10:30:00Z", "decision": "Prioritized user experience features"}
        ]
    },
    {
        "id": "proj_004",
        "name": "Financial Analytics Dashboard",
        "description": "Real-time financial analytics and reporting system",
        "client": "FinTech Solutions",
        "status": "active",
        "progress": 30,
        "timeline": "3 months",
        "start_date": "2024-03-01",
        "end_date": "2024-05-31",
        "team_size": 4,
        "revenue": 95000,
        "budget": 50000,
        "departments_involved": ["Engineering", "Finance", "Security"],
        "agents_assigned": [
            {"id": "eng_lead", "name": "Alex CodeMaster", "department": "Engineering", "contribution": 40},
            {"id": "finance_manager", "name": "Quinn Numbers", "department": "Finance", "contribution": 35},
            {"id": "security_lead", "name": "Guardian Shield", "department": "Security", "contribution": 25}
        ],
        "milestones": [
            {"id": 1, "name": "Data Architecture", "status": "in_progress", "due_date": "2024-03-31"},
            {"id": 2, "name": "Dashboard Development", "status": "pending", "due_date": "2024-04-30"},
            {"id": 3, "name": "Security Audit", "status": "pending", "due_date": "2024-05-15"}
        ],
        "risks": [
            {"level": "high", "description": "Financial data security and compliance"},
            {"level": "medium", "description": "Real-time data processing complexity"}
        ],
        "client_feedback": [
            {"date": "2024-01-12", "rating": 5, "comment": "Security approach is comprehensive"},
            {"date": "2024-01-03", "rating": 4, "comment": "Technical team is highly skilled"}
        ],
        "daena_decisions": [
            {"timestamp": "2024-01-12T15:20:00Z", "decision": "Approved enhanced security measures"},
            {"timestamp": "2024-01-03T11:45:00Z", "decision": "Allocated additional security resources"}
        ]
    },
    {
        "id": "proj_005",
        "name": "HR Management System",
        "description": "AI-powered HR management and employee development platform",
        "client": "PeopleFirst Corp",
        "status": "active",
        "progress": 20,
        "timeline": "4 months",
        "start_date": "2024-03-15",
        "end_date": "2024-07-15",
        "team_size": 3,
        "revenue": 75000,
        "budget": 45000,
        "departments_involved": ["Engineering", "HR", "Product"],
        "agents_assigned": [
            {"id": "eng_dev", "name": "Sam Builder", "department": "Engineering", "contribution": 45},
            {"id": "hr_manager", "name": "Skyler People", "department": "HR", "contribution": 40},
            {"id": "prod_manager", "name": "Casey Vision", "department": "Product", "contribution": 15}
        ],
        "milestones": [
            {"id": 1, "name": "Requirements Gathering", "status": "completed", "due_date": "2024-03-31"},
            {"id": 2, "name": "Core Development", "status": "in_progress", "due_date": "2024-05-31"},
            {"id": 3, "name": "Testing & Training", "status": "pending", "due_date": "2024-07-01"}
        ],
        "risks": [
            {"level": "medium", "description": "HR compliance requirements"},
            {"level": "low", "description": "User adoption and training"}
        ],
        "client_feedback": [
            {"date": "2024-01-10", "rating": 5, "comment": "Requirements analysis was thorough"},
            {"date": "2024-01-02", "rating": 4, "comment": "Team understands our HR needs well"}
        ],
        "daena_decisions": [
            {"timestamp": "2024-01-10T14:30:00Z", "decision": "Approved compliance framework implementation"},
            {"timestamp": "2024-01-02T09:15:00Z", "decision": "Prioritized user-friendly interface design"}
        ]
    }
]

@router.get("/", response_class=HTMLResponse)
async def projects_dashboard(request: Request):
    """Projects overview dashboard"""
    return templates.TemplateResponse("projects.html", {
        "request": request,
        "projects": PROJECTS
    })

@router.get("/api/v1/projects")
async def get_projects() -> List[Dict[str, Any]]:
    """Get all projects"""
    return PROJECTS

@router.get("/api/v1/projects/{project_id}")
async def get_project(project_id: str) -> Dict[str, Any]:
    """Get specific project details"""
    for project in PROJECTS:
        if project["id"] == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")

@router.get("/api/v1/projects/{project_id}/revenue")
async def get_project_revenue(project_id: str) -> Dict[str, Any]:
    """Get revenue details for a specific project"""
    for project in PROJECTS:
        if project["id"] == project_id:
            return {
                "project_id": project_id,
                "revenue": project["revenue"],
                "budget": project["budget"],
                "profit_margin": ((project["revenue"] - project["budget"]) / project["revenue"] * 100) if project["revenue"] > 0 else 0
            }
    raise HTTPException(status_code=404, detail="Project not found")

@router.get("/api/v1/projects/{project_id}/timeline")
async def get_project_timeline(project_id: str) -> Dict[str, Any]:
    """Get timeline details for a specific project"""
    for project in PROJECTS:
        if project["id"] == project_id:
            return {
                "project_id": project_id,
                "timeline": project["timeline"],
                "start_date": project["start_date"],
                "end_date": project["end_date"],
                "progress": project["progress"],
                "milestones": project["milestones"]
            }
    raise HTTPException(status_code=404, detail="Project not found")

@router.get("/api/v1/projects/{project_id}/team")
async def get_project_team(project_id: str) -> Dict[str, Any]:
    """Get team details for a specific project"""
    for project in PROJECTS:
        if project["id"] == project_id:
            return {
                "project_id": project_id,
                "team_size": project["team_size"],
                "agents_assigned": project["agents_assigned"],
                "departments_involved": project["departments_involved"]
            }
    raise HTTPException(status_code=404, detail="Project not found")

@router.get("/api/v1/projects/{project_id}/feedback")
async def get_project_feedback(project_id: str) -> Dict[str, Any]:
    """Get client feedback for a specific project"""
    for project in PROJECTS:
        if project["id"] == project_id:
            return {
                "project_id": project_id,
                "client_feedback": project["client_feedback"],
                "average_rating": sum(f["rating"] for f in project["client_feedback"]) / len(project["client_feedback"]) if project["client_feedback"] else 0
            }
    raise HTTPException(status_code=404, detail="Project not found")

@router.get("/api/v1/projects/{project_id}/daena-decisions")
async def get_project_daena_decisions(project_id: str) -> Dict[str, Any]:
    """Get Daena decisions for a specific project"""
    for project in PROJECTS:
        if project["id"] == project_id:
            return {
                "project_id": project_id,
                "daena_decisions": project["daena_decisions"]
            }
    raise HTTPException(status_code=404, detail="Project not found")

@router.get("/api/v1/projects/revenue/summary")
async def get_revenue_summary() -> Dict[str, Any]:
    """Get revenue summary across all projects"""
    total_revenue = sum(p["revenue"] for p in PROJECTS)
    total_budget = sum(p["budget"] for p in PROJECTS)
    active_projects = len([p for p in PROJECTS if p["status"] == "active"])
    
    return {
        "total_revenue": total_revenue,
        "total_budget": total_budget,
        "total_profit": total_revenue - total_budget,
        "profit_margin": ((total_revenue - total_budget) / total_revenue * 100) if total_revenue > 0 else 0,
        "active_projects": active_projects,
        "average_revenue_per_project": total_revenue / len(PROJECTS) if PROJECTS else 0
    }

@router.get("/project/{project_id}", response_class=HTMLResponse)
async def project_detail(request: Request, project_id: str):
    """Project detail page"""
    project = None
    for p in PROJECTS:
        if p["id"] == project_id:
            project = p
            break
    
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    return templates.TemplateResponse("project_detail.html", {
        "request": request,
        "project": project
    }) 