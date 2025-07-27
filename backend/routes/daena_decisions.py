from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any
import os
from pathlib import Path
from datetime import datetime, timedelta
import random

router = APIRouter(prefix="/daena", tags=["daena"])

# Get templates directory
project_root = Path(__file__).parent.parent.parent
templates_dir = project_root / "frontend" / "templates"
templates = Jinja2Templates(directory=str(templates_dir))

# Daena Decision Log - Git History for AI
DAENA_DECISIONS = [
    {
        "id": "dec_001",
        "timestamp": "2024-01-15T11:30:00Z",
        "title": "Approved Enterprise Security Protocol",
        "description": "Implemented enhanced security measures for TechCorp enterprise client after threat assessment",
        "type": "security_override",
        "impact": "high",
        "agents_involved": 3,
        "departments_affected": ["Engineering", "Security", "Legal"],
        "reasoning": "Enterprise client requires SOC2 compliance and enhanced data protection",
        "override_previous_decision": False,
        "risk_assessment": "Low risk, high reward for client satisfaction and compliance",
        "metrics_impact": {
            "security_score": "+5.2%",
            "client_satisfaction": "+8.1%",
            "compliance_score": "+12.3%"
        },
        "related_projects": ["proj_002"],
        "related_agents": ["security_lead", "eng_lead", "legal_counsel"]
    },
    {
        "id": "dec_002",
        "timestamp": "2024-01-15T10:45:00Z",
        "title": "Resource Reallocation for AI Platform",
        "description": "Redirected engineering resources to prioritize AI agent builder platform development",
        "type": "resource_allocation",
        "impact": "medium",
        "agents_involved": 5,
        "departments_affected": ["Engineering", "Product", "Marketing"],
        "reasoning": "Market analysis shows high demand for no-code AI solutions",
        "override_previous_decision": True,
        "risk_assessment": "Medium risk due to timeline compression, but high market opportunity",
        "metrics_impact": {
            "development_velocity": "+15.2%",
            "market_positioning": "+22.1%",
            "team_efficiency": "+8.7%"
        },
        "related_projects": ["proj_001"],
        "related_agents": ["eng_lead", "prod_manager", "marketing_lead"]
    },
    {
        "id": "dec_003",
        "timestamp": "2024-01-15T10:15:00Z",
        "title": "Client Communication Protocol Update",
        "description": "Enhanced client communication frequency and transparency measures",
        "type": "process_improvement",
        "impact": "medium",
        "agents_involved": 8,
        "departments_affected": ["Sales", "Marketing", "Product", "Engineering"],
        "reasoning": "Client feedback indicates need for better communication and transparency",
        "override_previous_decision": False,
        "risk_assessment": "Low risk, high impact on client satisfaction",
        "metrics_impact": {
            "client_satisfaction": "+12.5%",
            "communication_efficiency": "+18.3%",
            "project_success_rate": "+6.8%"
        },
        "related_projects": ["proj_001", "proj_002", "proj_003", "proj_004", "proj_005"],
        "related_agents": ["sales_lead", "marketing_lead", "prod_manager"]
    },
    {
        "id": "dec_004",
        "timestamp": "2024-01-15T09:30:00Z",
        "title": "Budget Optimization for Q1",
        "description": "Reallocated budget to maximize ROI across all active projects",
        "type": "financial_decision",
        "impact": "high",
        "agents_involved": 2,
        "departments_affected": ["Finance", "Engineering"],
        "reasoning": "Analysis shows better ROI from engineering investments vs marketing spend",
        "override_previous_decision": True,
        "risk_assessment": "Medium risk due to reduced marketing budget, but higher engineering output",
        "metrics_impact": {
            "roi": "+18.7%",
            "engineering_velocity": "+25.3%",
            "cost_efficiency": "+12.1%"
        },
        "related_projects": ["proj_001", "proj_002", "proj_003"],
        "related_agents": ["finance_manager", "eng_lead"]
    },
    {
        "id": "dec_005",
        "timestamp": "2024-01-15T09:00:00Z",
        "title": "Agent Performance Optimization",
        "description": "Implemented new performance tracking and optimization protocols for all agents",
        "type": "system_optimization",
        "impact": "medium",
        "agents_involved": 12,
        "departments_affected": ["Engineering", "HR", "All Departments"],
        "reasoning": "Performance analysis shows opportunity for 15-20% efficiency improvement",
        "override_previous_decision": False,
        "risk_assessment": "Low risk, high potential for performance improvement",
        "metrics_impact": {
            "agent_efficiency": "+16.8%",
            "task_completion_rate": "+12.4%",
            "overall_productivity": "+14.2%"
        },
        "related_projects": ["proj_001", "proj_002", "proj_003", "proj_004", "proj_005"],
        "related_agents": ["hr_manager", "eng_lead", "all_agents"]
    },
    {
        "id": "dec_006",
        "timestamp": "2024-01-15T08:45:00Z",
        "title": "Market Strategy Pivot",
        "description": "Shifted focus from B2C to B2B market based on revenue analysis",
        "type": "strategic_decision",
        "impact": "high",
        "agents_involved": 6,
        "departments_affected": ["Sales", "Marketing", "Product"],
        "reasoning": "B2B market shows 3x higher LTV and better product-market fit",
        "override_previous_decision": True,
        "risk_assessment": "High risk due to strategy change, but data supports decision",
        "metrics_impact": {
            "revenue_per_customer": "+280%",
            "sales_cycle_length": "-25%",
            "customer_acquisition_cost": "-40%"
        },
        "related_projects": ["proj_001", "proj_002", "proj_003"],
        "related_agents": ["sales_lead", "marketing_lead", "prod_manager"]
    },
    {
        "id": "dec_007",
        "timestamp": "2024-01-15T08:15:00Z",
        "title": "Technology Stack Standardization",
        "description": "Standardized technology stack across all projects for better maintainability",
        "type": "technical_decision",
        "impact": "medium",
        "agents_involved": 4,
        "departments_affected": ["Engineering"],
        "reasoning": "Reduces maintenance overhead and improves team collaboration",
        "override_previous_decision": False,
        "risk_assessment": "Low risk, high long-term benefit",
        "metrics_impact": {
            "development_speed": "+22.1%",
            "maintenance_cost": "-18.7%",
            "code_quality": "+15.3%"
        },
        "related_projects": ["proj_001", "proj_002", "proj_003", "proj_004", "proj_005"],
        "related_agents": ["eng_lead", "eng_dev", "eng_devops"]
    },
    {
        "id": "dec_008",
        "timestamp": "2024-01-15T07:30:00Z",
        "title": "Client Onboarding Process Enhancement",
        "description": "Streamlined client onboarding process to reduce time-to-value",
        "type": "process_improvement",
        "impact": "medium",
        "agents_involved": 3,
        "departments_affected": ["Sales", "Engineering", "Product"],
        "reasoning": "Current onboarding takes too long, affecting client satisfaction",
        "override_previous_decision": False,
        "risk_assessment": "Low risk, immediate positive impact",
        "metrics_impact": {
            "time_to_value": "-35%",
            "client_satisfaction": "+18.9%",
            "onboarding_success_rate": "+24.6%"
        },
        "related_projects": ["proj_002", "proj_003", "proj_004"],
        "related_agents": ["sales_lead", "eng_lead", "prod_manager"]
    },
    {
        "id": "dec_009",
        "timestamp": "2024-01-15T07:00:00Z",
        "title": "Quality Assurance Protocol",
        "description": "Implemented comprehensive QA protocol across all development projects",
        "type": "quality_improvement",
        "impact": "medium",
        "agents_involved": 5,
        "departments_affected": ["Engineering", "Product"],
        "reasoning": "Recent bug reports indicate need for better quality control",
        "override_previous_decision": False,
        "risk_assessment": "Low risk, high quality improvement",
        "metrics_impact": {
            "bug_rate": "-45.2%",
            "code_quality": "+28.7%",
            "client_satisfaction": "+16.3%"
        },
        "related_projects": ["proj_001", "proj_002", "proj_003", "proj_004"],
        "related_agents": ["eng_lead", "eng_dev", "prod_manager", "prod_designer"]
    },
    {
        "id": "dec_010",
        "timestamp": "2024-01-15T06:30:00Z",
        "title": "Team Collaboration Enhancement",
        "description": "Implemented new collaboration tools and protocols for better cross-department communication",
        "type": "organizational_improvement",
        "impact": "medium",
        "agents_involved": 12,
        "departments_affected": ["All Departments"],
        "reasoning": "Cross-department communication gaps identified in recent project reviews",
        "override_previous_decision": False,
        "risk_assessment": "Low risk, immediate collaboration improvement",
        "metrics_impact": {
            "communication_efficiency": "+31.2%",
            "project_coordination": "+26.8%",
            "team_satisfaction": "+19.4%"
        },
        "related_projects": ["proj_001", "proj_002", "proj_003", "proj_004", "proj_005"],
        "related_agents": ["all_agents"]
    }
]

@router.get("/decisions", response_class=HTMLResponse)
async def daena_decisions_dashboard(request: Request):
    """Daena decisions overview dashboard"""
    return templates.TemplateResponse("daena_decisions.html", {
        "request": request,
        "decisions": DAENA_DECISIONS
    })

@router.get("/api/v1/daena/decisions")
async def get_daena_decisions() -> List[Dict[str, Any]]:
    """Get all Daena decisions"""
    return DAENA_DECISIONS

@router.get("/api/v1/daena/decisions/{decision_id}")
async def get_daena_decision(decision_id: str) -> Dict[str, Any]:
    """Get specific Daena decision details"""
    for decision in DAENA_DECISIONS:
        if decision["id"] == decision_id:
            return decision
    raise HTTPException(status_code=404, detail="Decision not found")

@router.get("/api/v1/daena/decisions/impact/{impact_level}")
async def get_decisions_by_impact(impact_level: str) -> List[Dict[str, Any]]:
    """Get decisions by impact level (high, medium, low)"""
    valid_impacts = ["high", "medium", "low"]
    if impact_level.lower() not in valid_impacts:
        raise HTTPException(status_code=400, detail="Invalid impact level")
    
    return [d for d in DAENA_DECISIONS if d["impact"] == impact_level.lower()]

@router.get("/api/v1/daena/decisions/type/{decision_type}")
async def get_decisions_by_type(decision_type: str) -> List[Dict[str, Any]]:
    """Get decisions by type"""
    return [d for d in DAENA_DECISIONS if d["type"] == decision_type]

@router.get("/api/v1/daena/decisions/project/{project_id}")
async def get_decisions_for_project(project_id: str) -> List[Dict[str, Any]]:
    """Get all decisions related to a specific project"""
    return [d for d in DAENA_DECISIONS if project_id in d.get("related_projects", [])]

@router.get("/api/v1/daena/decisions/agent/{agent_id}")
async def get_decisions_for_agent(agent_id: str) -> List[Dict[str, Any]]:
    """Get all decisions related to a specific agent"""
    return [d for d in DAENA_DECISIONS if agent_id in d.get("related_agents", [])]

@router.get("/api/v1/daena/decisions/summary")
async def get_decisions_summary() -> Dict[str, Any]:
    """Get summary statistics of Daena decisions"""
    total_decisions = len(DAENA_DECISIONS)
    high_impact = len([d for d in DAENA_DECISIONS if d["impact"] == "high"])
    medium_impact = len([d for d in DAENA_DECISIONS if d["impact"] == "medium"])
    low_impact = len([d for d in DAENA_DECISIONS if d["impact"] == "low"])
    overrides = len([d for d in DAENA_DECISIONS if d["override_previous_decision"]])
    
    return {
        "total_decisions": total_decisions,
        "high_impact_decisions": high_impact,
        "medium_impact_decisions": medium_impact,
        "low_impact_decisions": low_impact,
        "override_decisions": overrides,
        "average_agents_involved": sum(d["agents_involved"] for d in DAENA_DECISIONS) / total_decisions if total_decisions > 0 else 0
    }

@router.get("/api/v1/daena/status")
async def get_daena_status() -> Dict[str, Any]:
    """Get current Daena AI status"""
    return {
        "status": "active",
        "brain_ready": True,
        "agents_connected": 12,
        "last_decision": DAENA_DECISIONS[0]["timestamp"] if DAENA_DECISIONS else None,
        "total_decisions_today": len([d for d in DAENA_DECISIONS if d["timestamp"].startswith("2024-01-15")]),
        "system_health": "excellent",
        "decision_accuracy": 94.7,
        "response_time": "0.3s"
    }

@router.get("/decision/{decision_id}", response_class=HTMLResponse)
async def decision_detail(request: Request, decision_id: str):
    """Decision detail page"""
    decision = None
    for d in DAENA_DECISIONS:
        if d["id"] == decision_id:
            decision = d
            break
    
    if not decision:
        raise HTTPException(status_code=404, detail="Decision not found")
    
    return templates.TemplateResponse("decision_detail.html", {
        "request": request,
        "decision": decision
    }) 