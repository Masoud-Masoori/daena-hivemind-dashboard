from fastapi import APIRouter, HTTPException, UploadFile, File, Form
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import json
import os
from datetime import datetime, timedelta
import asyncio
import uuid
import hashlib
from pathlib import Path

router = APIRouter(prefix="/honey-knowledge", tags=["Honey Knowledge System"])

# Honey Knowledge Models
class KnowledgeSource(BaseModel):
    id: str
    type: str  # "project", "llm_consultation", "meeting", "training", "experience", "file_access"
    source_name: str
    description: str
    timestamp: datetime
    confidence_score: float
    file_path: Optional[str] = None
    web3_hash: Optional[str] = None

class HoneyKnowledge(BaseModel):
    id: str
    title: str
    content: str
    category: str  # "strategy", "technical", "business", "process", "insight", "customer_intel"
    department: str
    agent_contributors: List[str]
    sources: List[KnowledgeSource]
    honey_volume: float  # 0.0 to 1.0 representing knowledge density
    last_updated: datetime
    is_verified: bool = False
    web3_contract_hash: Optional[str] = None
    access_level: str = "department"  # "public", "department", "confidential", "hidden"

class ProjectHoney(BaseModel):
    id: str
    project_id: str
    project_name: str
    honey_knowledge: List[HoneyKnowledge]
    total_honey_volume: float
    knowledge_growth_rate: float
    last_activity: datetime
    contract_signed: bool = False
    contract_hash: Optional[str] = None

# Mock data for honey knowledge
mock_honey_knowledge = [
    HoneyKnowledge(
        id="honey-001",
        title="Customer Behavior Patterns Q4",
        content="Analysis of customer behavior patterns shows 40% increase in mobile usage during evening hours...",
        category="customer_intel",
        department="marketing",
        agent_contributors=["Sunflower", "Bee 001", "Bee 002"],
        sources=[
            KnowledgeSource(
                id="source-001",
                type="project",
                source_name="Q4 Analytics Project",
                description="Customer analytics data analysis",
                timestamp=datetime.now(),
                confidence_score=0.92
            )
        ],
        honey_volume=0.85,
        last_updated=datetime.now(),
        is_verified=True,
        access_level="department"
    ),
    HoneyKnowledge(
        id="honey-002",
        title="AI Agent Optimization Strategies",
        content="Best practices for optimizing AI agent performance include workload balancing and memory management...",
        category="technical",
        department="technology",
        agent_contributors=["Honeycomb", "Bee 003"],
        sources=[
            KnowledgeSource(
                id="source-002",
                type="llm_consultation",
                source_name="GPT-4 Consultation",
                description="AI optimization strategies consultation",
                timestamp=datetime.now(),
                confidence_score=0.88
            )
        ],
        honey_volume=0.78,
        last_updated=datetime.now(),
        is_verified=True,
        access_level="department"
    )
]

mock_project_honey = [
    ProjectHoney(
        id="project-honey-001",
        project_id="proj-001",
        project_name="Market Expansion Initiative",
        honey_knowledge=[mock_honey_knowledge[0]],
        total_honey_volume=0.85,
        knowledge_growth_rate=0.15,
        last_activity=datetime.now(),
        contract_signed=True
    )
]

@router.get("/")
async def get_honey_knowledge():
    """Get all honey knowledge"""
    return {
        "honey_knowledge": mock_honey_knowledge,
        "total_items": len(mock_honey_knowledge),
        "total_volume": sum(h.honey_volume for h in mock_honey_knowledge),
        "verified_items": len([h for h in mock_honey_knowledge if h.is_verified])
    }

@router.get("/department/{department}")
async def get_department_honey(department: str):
    """Get honey knowledge for a specific department"""
    dept_honey = [h for h in mock_honey_knowledge if h.department.lower() == department.lower()]
    return {
        "department": department,
        "honey_knowledge": dept_honey,
        "total_items": len(dept_honey),
        "total_volume": sum(h.honey_volume for h in dept_honey)
    }

@router.get("/category/{category}")
async def get_category_honey(category: str):
    """Get honey knowledge by category"""
    category_honey = [h for h in mock_honey_knowledge if h.category.lower() == category.lower()]
    return {
        "category": category,
        "honey_knowledge": category_honey,
        "total_items": len(category_honey),
        "total_volume": sum(h.honey_volume for h in category_honey)
    }

@router.post("/")
async def create_honey_knowledge(honey: HoneyKnowledge):
    """Create new honey knowledge"""
    honey.id = f"honey-{uuid.uuid4().hex[:8]}"
    honey.last_updated = datetime.now()
    
    # Generate Web3 hash for verification
    honey_data = {
        "title": honey.title,
        "content": honey.content,
        "department": honey.department,
        "timestamp": honey.last_updated.isoformat()
    }
    honey.web3_contract_hash = hashlib.sha256(json.dumps(honey_data, sort_keys=True).encode()).hexdigest()
    
    mock_honey_knowledge.append(honey)
    return {"message": "Honey knowledge created", "honey": honey}

@router.post("/from-file")
async def create_honey_from_file(
    title: str = Form(...),
    category: str = Form(...),
    department: str = Form(...),
    file: UploadFile = File(...),
    agent_contributors: str = Form(...)  # JSON string of agent names
):
    """Create honey knowledge from uploaded file"""
    # Save file
    file_path = f"uploads/{file.filename}"
    os.makedirs("uploads", exist_ok=True)
    
    with open(file_path, "wb") as buffer:
        content = await file.read()
        buffer.write(content)
    
    # Create honey knowledge
    honey = HoneyKnowledge(
        id=f"honey-{uuid.uuid4().hex[:8]}",
        title=title,
        content=f"Knowledge extracted from file: {file.filename}",
        category=category,
        department=department,
        agent_contributors=json.loads(agent_contributors),
        sources=[
            KnowledgeSource(
                id=f"source-{uuid.uuid4().hex[:8]}",
                type="file_access",
                source_name=file.filename,
                description=f"File uploaded: {file.filename}",
                timestamp=datetime.now(),
                confidence_score=0.90,
                file_path=file_path
            )
        ],
        honey_volume=0.75,
        last_updated=datetime.now()
    )
    
    mock_honey_knowledge.append(honey)
    return {"message": "Honey knowledge created from file", "honey": honey}

@router.post("/{honey_id}/verify")
async def verify_honey_knowledge(honey_id: str):
    """Verify honey knowledge with Web3"""
    for honey in mock_honey_knowledge:
        if honey.id == honey_id:
            honey.is_verified = True
            honey.web3_contract_hash = hashlib.sha256(
                json.dumps({
                    "id": honey.id,
                    "title": honey.title,
                    "verified_at": datetime.now().isoformat()
                }, sort_keys=True).encode()
            ).hexdigest()
            return {"message": "Honey knowledge verified", "honey": honey}
    raise HTTPException(status_code=404, detail="Honey knowledge not found")

@router.get("/projects")
async def get_project_honey():
    """Get honey knowledge organized by projects"""
    return {
        "project_honey": mock_project_honey,
        "total_projects": len(mock_project_honey),
        "total_volume": sum(p.total_honey_volume for p in mock_project_honey)
    }

@router.get("/projects/{project_id}")
async def get_project_honey_detail(project_id: str):
    """Get honey knowledge for a specific project"""
    for project in mock_project_honey:
        if project.project_id == project_id:
            return project
    raise HTTPException(status_code=404, detail="Project not found")

@router.post("/projects/{project_id}/contract")
async def sign_project_contract(project_id: str, contract_data: Dict[str, Any]):
    """Sign a contract for project honey knowledge"""
    for project in mock_project_honey:
        if project.project_id == project_id:
            project.contract_signed = True
            project.contract_hash = hashlib.sha256(
                json.dumps(contract_data, sort_keys=True).encode()
            ).hexdigest()
            return {"message": "Project contract signed", "project": project}
    raise HTTPException(status_code=404, detail="Project not found")

@router.get("/growth-analytics")
async def get_honey_growth_analytics():
    """Get analytics on honey knowledge growth"""
    return {
        "total_knowledge_items": len(mock_honey_knowledge),
        "average_honey_volume": sum(h.honey_volume for h in mock_honey_knowledge) / len(mock_honey_knowledge) if mock_honey_knowledge else 0,
        "department_breakdown": {
            dept: len([h for h in mock_honey_knowledge if h.department == dept])
            for dept in set(h.department for h in mock_honey_knowledge)
        },
        "category_breakdown": {
            cat: len([h for h in mock_honey_knowledge if h.category == cat])
            for cat in set(h.category for h in mock_honey_knowledge)
        },
        "verification_rate": len([h for h in mock_honey_knowledge if h.is_verified]) / len(mock_honey_knowledge) if mock_honey_knowledge else 0
    }

@router.get("/file-access")
async def get_file_access_knowledge():
    """Get honey knowledge from file access"""
    file_knowledge = [
        h for h in mock_honey_knowledge 
        if any(s.type == "file_access" for s in h.sources)
    ]
    return {
        "file_knowledge": file_knowledge,
        "total_files": len(file_knowledge),
        "file_types": list(set(
            s.source_name.split('.')[-1] 
            for h in file_knowledge 
            for s in h.sources 
            if s.type == "file_access"
        ))
    }

@router.post("/llm-consultation")
async def create_honey_from_llm_consultation(
    title: str = Form(...),
    content: str = Form(...),
    department: str = Form(...),
    llm_model: str = Form(...),
    confidence_score: float = Form(...),
    agent_contributors: str = Form(...)  # JSON string
):
    """Create honey knowledge from LLM consultation"""
    honey = HoneyKnowledge(
        id=f"honey-{uuid.uuid4().hex[:8]}",
        title=title,
        content=content,
        category="insight",
        department=department,
        agent_contributors=json.loads(agent_contributors),
        sources=[
            KnowledgeSource(
                id=f"source-{uuid.uuid4().hex[:8]}",
                type="llm_consultation",
                source_name=f"{llm_model} Consultation",
                description=f"Knowledge generated from {llm_model} consultation",
                timestamp=datetime.now(),
                confidence_score=confidence_score
            )
        ],
        honey_volume=confidence_score,
        last_updated=datetime.now()
    )
    
    mock_honey_knowledge.append(honey)
    return {"message": "Honey knowledge created from LLM consultation", "honey": honey}

@router.get("/web3/verified")
async def get_web3_verified_knowledge():
    """Get all Web3 verified honey knowledge"""
    verified_knowledge = [h for h in mock_honey_knowledge if h.is_verified and h.web3_contract_hash]
    return {
        "verified_knowledge": verified_knowledge,
        "total_verified": len(verified_knowledge),
        "total_contracts": len([h for h in verified_knowledge if h.web3_contract_hash])
    }

@router.post("/web3/deploy-contract")
async def deploy_knowledge_contract(honey_id: str):
    """Deploy a Web3 contract for honey knowledge"""
    for honey in mock_honey_knowledge:
        if honey.id == honey_id:
            # Simulate Web3 contract deployment
            contract_address = f"0x{uuid.uuid4().hex[:40]}"
            honey.web3_contract_hash = contract_address
            return {
                "message": "Knowledge contract deployed",
                "contract_address": contract_address,
                "honey_id": honey_id,
                "transaction_hash": f"0x{uuid.uuid4().hex[:64]}"
            }
    raise HTTPException(status_code=404, detail="Honey knowledge not found") 

@router.get("/honey/structure/{project_id}")
async def get_honey_structure(project_id: str):
    """Return honeycomb layout for a given project showing honey volume, linked items, and agent contributions"""
    
    # Find the project
    project = next((p for p in mock_project_honey if p.project_id == project_id), None)
    if not project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Get linked LLM consultations from project's honey knowledge
    linked_consultations = [
        {
            "id": h.id,
            "title": h.title,
            "agent": h.agent_contributors[0] if h.agent_contributors else "unknown",
            "llm_model": next((s.source_name for s in h.sources if s.type == "llm_consultation"), "unknown"),
            "timestamp": h.last_updated,
            "honey_volume": h.honey_volume
        }
        for h in project.honey_knowledge 
        if any(s.type == "llm_consultation" for s in h.sources)
    ]
    
    # Get linked tasks (simulated)
    linked_tasks = [
        {
            "id": f"task-{i}",
            "title": f"Task {i}",
            "status": "completed",
            "assigned_agent": "agent-1",
            "honey_volume": 0.5
        }
        for i in range(1, 4)
    ]
    
    # Get linked meetings (simulated)
    linked_meetings = [
        {
            "id": f"meeting-{i}",
            "title": f"Meeting {i}",
            "type": "strategic",
            "status": "completed",
            "honey_volume": 0.8
        }
        for i in range(1, 3)
    ]
    
    # Calculate total honey volume
    total_honey = (
        sum(c.honey_volume for c in linked_consultations) +
        sum(t.honey_volume for t in linked_tasks) +
        sum(m.honey_volume for m in linked_meetings)
    )
    
    # Create honeycomb structure
    honeycomb_structure = {
        "project_id": project_id,
        "project_name": project.project_name,
        "total_honey_volume": total_honey,
        "honeycomb_cells": [
            {
                "type": "consultation",
                "data": linked_consultations,
                "honey_volume": sum(c.honey_volume for c in linked_consultations),
                "cell_count": len(linked_consultations)
            },
            {
                "type": "task",
                "data": linked_tasks,
                "honey_volume": sum(t.honey_volume for t in linked_tasks),
                "cell_count": len(linked_tasks)
            },
            {
                "type": "meeting",
                "data": linked_meetings,
                "honey_volume": sum(m.honey_volume for m in linked_meetings),
                "cell_count": len(linked_meetings)
            }
        ],
        "agent_contributions": [
            {
                "agent_id": "agent-1",
                "agent_name": "Sunflower",
                "honey_contributed": 2.5,
                "tasks_completed": 3,
                "consultations_made": 2
            },
            {
                "agent_id": "agent-2", 
                "agent_name": "Honeycomb",
                "honey_contributed": 1.8,
                "tasks_completed": 2,
                "consultations_made": 1
            }
        ]
    }
    
    return honeycomb_structure 

@router.get("/honey-tracker/visualization")
async def get_honey_visualization():
    """Get comprehensive honey visualization data"""
    # Calculate department totals
    department_totals = {}
    agent_totals = {}
    
    for honey in mock_honey_knowledge:
        dept = honey.department
        if dept not in department_totals:
            department_totals[dept] = 0
        department_totals[dept] += honey.honey_volume
        
        for agent in honey.agent_contributors:
            if agent not in agent_totals:
                agent_totals[agent] = 0
            agent_totals[agent] += honey.honey_volume / len(honey.agent_contributors)
    
    # Calculate analytics
    total_honey = sum(h.honey_volume for h in mock_honey_knowledge)
    avg_honey = total_honey / len(mock_honey_knowledge) if mock_honey_knowledge else 0
    verified_count = len([h for h in mock_honey_knowledge if h.is_verified])
    
    # Timeline data (last 30 days)
    timeline_data = []
    for i in range(30):
        date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0) - timedelta(days=i)
        daily_honey = sum(h.honey_volume for h in mock_honey_knowledge 
                         if h.last_updated.date() == date.date())
        timeline_data.append({
            "date": date.strftime("%Y-%m-%d"),
            "honey_volume": daily_honey,
            "new_items": len([h for h in mock_honey_knowledge 
                            if h.last_updated.date() == date.date()])
        })
    timeline_data.reverse()
    
    # Department efficiency (mock data)
    department_efficiency = {
        "Finance": 92.5,
        "Marketing": 88.3,
        "Technology": 95.1,
        "HR": 85.7,
        "Strategy": 90.2
    }
    
    # Top generators
    top_generators = []
    for agent, volume in sorted(agent_totals.items(), key=lambda x: x[1], reverse=True)[:10]:
        top_generators.append({
            "name": agent,
            "department": next((h.department for h in mock_honey_knowledge 
                              if agent in h.agent_contributors), "Unknown"),
            "honey_volume": round(volume, 2),
            "efficiency": round(volume / avg_honey * 100, 1) if avg_honey > 0 else 0,
            "status": "Active"
        })
    
    return {
        "analytics": {
            "total_honey": round(total_honey, 2),
            "honey_growth_rate": 15.3,  # Mock growth rate
            "honey_efficiency": round(verified_count / len(mock_honey_knowledge) * 100, 1) if mock_honey_knowledge else 0,
            "honey_quality_score": 89.7,  # Mock quality score
            "average_honey_volume": round(avg_honey, 2),
            "verified_items": verified_count,
            "total_items": len(mock_honey_knowledge)
        },
        "department_breakdown": [
            {
                "department": dept,
                "honey_volume": round(volume, 2),
                "efficiency": department_efficiency.get(dept, 85.0),
                "item_count": len([h for h in mock_honey_knowledge if h.department == dept])
            }
            for dept, volume in department_totals.items()
        ],
        "agent_breakdown": [
            {
                "agent": agent,
                "honey_volume": round(volume, 2),
                "department": next((h.department for h in mock_honey_knowledge 
                                  if agent in h.agent_contributors), "Unknown"),
                "efficiency": round(volume / avg_honey * 100, 1) if avg_honey > 0 else 0
            }
            for agent, volume in agent_totals.items()
        ],
        "timeline": timeline_data,
        "top_generators": top_generators,
        "honey_by_category": {
            cat: sum(h.honey_volume for h in mock_honey_knowledge if h.category == cat)
            for cat in set(h.category for h in mock_honey_knowledge)
        }
    }

@router.get("/honey-tracker/analytics")
async def get_honey_analytics():
    """Get detailed honey analytics"""
    analytics = {
        "honey_metrics": {
            "total_volume": sum(item.honey_volume for item in mock_honey_knowledge),
            "average_per_item": sum(item.honey_volume for item in mock_honey_knowledge) / len(mock_honey_knowledge) if mock_honey_knowledge else 0,
            "highest_single_item": max(item.honey_volume for item in mock_honey_knowledge) if mock_honey_knowledge else 0,
            "total_items": len(mock_honey_knowledge)
        },
        "department_performance": {
            "Finance": {
                "total_honey": sum(item.honey_volume for item in mock_honey_knowledge if item.department.lower() == "finance"),
                "item_count": len([item for item in mock_honey_knowledge if item.department.lower() == "finance"]),
                "efficiency": 94.2
            },
            "Marketing": {
                "total_honey": sum(item.honey_volume for item in mock_honey_knowledge if item.department.lower() == "marketing"),
                "item_count": len([item for item in mock_honey_knowledge if item.department.lower() == "marketing"]),
                "efficiency": 89.7
            },
            "Technology": {
                "total_honey": sum(item.honey_volume for item in mock_honey_knowledge if item.department.lower() == "technology"),
                "item_count": len([item for item in mock_honey_knowledge if item.department.lower() == "technology"]),
                "efficiency": 96.1
            },
            "HR": {
                "total_honey": sum(item.honey_volume for item in mock_honey_knowledge if item.department.lower() == "hr"),
                "item_count": len([item for item in mock_honey_knowledge if item.department.lower() == "hr"]),
                "efficiency": 82.3
            },
            "Strategy": {
                "total_honey": sum(item.honey_volume for item in mock_honey_knowledge if item.department.lower() == "strategy"),
                "item_count": len([item for item in mock_honey_knowledge if item.department.lower() == "strategy"]),
                "efficiency": 98.5
            }
        },
        "honey_trends": {
            "daily_growth": 12.5,
            "weekly_growth": 18.3,
            "monthly_growth": 25.7,
            "quality_trend": "increasing",
            "volume_trend": "stable"
        }
    }
    return analytics

@router.post("/honey-tracker/add-honey")
async def add_honey_to_tracker(
    department: str = Form(...),
    honey_amount: float = Form(...),
    source: str = Form(...),
    description: str = Form(...)
):
    """Add honey to the tracker"""
    # Create a new honey knowledge item
    new_honey = HoneyKnowledge(
        id=f"honey-{uuid.uuid4().hex[:8]}",
        title=f"Honey from {source}",
        content=description,
        category="insight",
        department=department.lower(),
        agent_contributors=["System"],
        sources=[
            KnowledgeSource(
                id=f"source-{uuid.uuid4().hex[:8]}",
                type="manual_entry",
                source_name=source,
                description=description,
                timestamp=datetime.now(),
                confidence_score=0.8
            )
        ],
        honey_volume=honey_amount,
        last_updated=datetime.now()
    )
    
    mock_honey_knowledge.append(new_honey)
    return {
        "message": f"Honey added to {department} tracker",
        "honey_item": new_honey,
        "total_honey": sum(item.honey_volume for item in mock_honey_knowledge)
    }

@router.get("/honey-tracker/department/{department}")
async def get_department_honey_details(department: str):
    """Get detailed honey data for a specific department"""
    dept_honey = [h for h in mock_honey_knowledge if h.department.lower() == department.lower()]
    
    if not dept_honey:
        raise HTTPException(status_code=404, detail="Department not found")
    
    # Calculate department metrics
    total_volume = sum(h.honey_volume for h in dept_honey)
    avg_volume = total_volume / len(dept_honey)
    verified_count = len([h for h in dept_honey if h.is_verified])
    
    # Agent contributions
    agent_contributions = {}
    for honey in dept_honey:
        for agent in honey.agent_contributors:
            if agent not in agent_contributions:
                agent_contributions[agent] = 0
            agent_contributions[agent] += honey.honey_volume / len(honey.agent_contributors)
    
    return {
        "department": department,
        "total_honey_volume": round(total_volume, 2),
        "average_honey_volume": round(avg_volume, 2),
        "item_count": len(dept_honey),
        "verified_items": verified_count,
        "verification_rate": round(verified_count / len(dept_honey) * 100, 1),
        "agent_contributions": [
            {
                "agent": agent,
                "honey_volume": round(volume, 2),
                "percentage": round(volume / total_volume * 100, 1)
            }
            for agent, volume in sorted(agent_contributions.items(), key=lambda x: x[1], reverse=True)
        ],
        "honey_items": dept_honey,
        "category_breakdown": {
            cat: sum(h.honey_volume for h in dept_honey if h.category == cat)
            for cat in set(h.category for h in dept_honey)
        }
    } 