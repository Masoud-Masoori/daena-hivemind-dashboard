from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import json
import os
from datetime import datetime
import asyncio
import uuid

router = APIRouter(prefix="/consultation", tags=["VP Consultation"])

# VP Models
class VPRequest(BaseModel):
    id: str
    user_id: str
    query: str
    context: Optional[Dict[str, Any]]
    priority: str
    department: Optional[str]
    timestamp: datetime
    status: str

class VPResponse(BaseModel):
    id: str
    request_id: str
    response: str
    reasoning: str
    decisions: List[Dict[str, Any]]
    actions_taken: List[str]
    llm_consultations: List[Dict[str, Any]]
    confidence_score: float
    timestamp: datetime

class VPMemory(BaseModel):
    id: str
    key: str
    value: Any
    context: str
    timestamp: datetime
    expires_at: Optional[datetime]

# Mock VP Memory Store
vp_memory = {
    "company_state": {
        "total_revenue": 15000000.0,
        "active_projects": 45,
        "employee_count": 85,
        "system_health": "excellent",
        "last_updated": datetime.now()
    },
    "recent_decisions": [
        {
            "id": "dec_001",
            "decision": "Approved blockchain integration project",
            "reasoning": "High ROI potential, aligns with tech strategy",
            "timestamp": datetime.now(),
            "impact": "positive"
        }
    ],
    "escalated_issues": [
        {
            "id": "esc_001", 
            "issue": "Marketing budget overrun",
            "severity": "medium",
            "status": "under_review",
            "timestamp": datetime.now()
        }
    ]
}

# Mock consultation history
consultation_history = []

@router.post("/ask", response_model=VPResponse)
async def ask_vp(request: VPRequest, background_tasks: BackgroundTasks):
    """Ask Daena VP for consultation and decision-making"""
    
    # Generate response ID
    response_id = str(uuid.uuid4())
    
    # Simulate VP processing
    response_text = await process_vp_query(request.query, request.context)
    
    # Create VP response
    vp_response = VPResponse(
        id=response_id,
        request_id=request.id,
        response=response_text,
        reasoning="Based on company data, market analysis, and historical patterns",
        decisions=[
            {
                "action": "approve_project",
                "confidence": 0.85,
                "reasoning": "Project aligns with strategic goals"
            }
        ],
        actions_taken=[
            "Analyzed company financials",
            "Consulted with department heads", 
            "Reviewed market conditions",
            "Generated decision matrix"
        ],
        llm_consultations=[
            {
                "model": "gpt-4",
                "opinion": "Strongly recommend approval",
                "confidence": 0.92
            },
            {
                "model": "claude-3",
                "opinion": "Approve with conditions",
                "confidence": 0.88
            }
        ],
        confidence_score=0.87,
        timestamp=datetime.now()
    )
    
    # Store in history
    consultation_history.append({
        "request": request.dict(),
        "response": vp_response.dict()
    })
    
    # Background task to update memory
    background_tasks.add_task(update_vp_memory, request, vp_response)
    
    return vp_response

@router.get("/memory")
async def get_vp_memory():
    """Get Daena VP's current memory and knowledge"""
    return {
        "memory": vp_memory,
        "total_consultations": len(consultation_history),
        "last_updated": datetime.now()
    }

@router.post("/memory/update")
async def update_vp_memory_item(key: str, value: Any, context: str = ""):
    """Update specific VP memory item"""
    vp_memory[key] = {
        "value": value,
        "context": context,
        "timestamp": datetime.now()
    }
    return {"message": f"Memory updated: {key}", "status": "success"}

@router.get("/history")
async def get_consultation_history(limit: int = 50):
    """Get consultation history"""
    return consultation_history[-limit:]

@router.post("/upload-document")
async def upload_document_for_vp(file: UploadFile = File(...), context: str = Form("")):
    """Upload document for VP analysis"""
    
    # Simulate document processing
    document_id = str(uuid.uuid4())
    
    # Store document info in memory
    vp_memory[f"document_{document_id}"] = {
        "filename": file.filename,
        "context": context,
        "uploaded_at": datetime.now(),
        "status": "processed"
    }
    
    return {
        "document_id": document_id,
        "filename": file.filename,
        "status": "uploaded_and_processed",
        "message": "Document available for VP consultation"
    }

@router.post("/escalate")
async def escalate_issue(issue: Dict[str, Any]):
    """Escalate issue to VP for decision"""
    
    escalation_id = str(uuid.uuid4())
    
    escalated_issue = {
        "id": escalation_id,
        "issue": issue.get("description"),
        "severity": issue.get("severity", "medium"),
        "department": issue.get("department"),
        "requested_by": issue.get("requested_by"),
        "status": "under_review",
        "timestamp": datetime.now()
    }
    
    vp_memory["escalated_issues"].append(escalated_issue)
    
    return {
        "escalation_id": escalation_id,
        "status": "escalated",
        "message": "Issue escalated to VP for review"
    }

@router.get("/analytics")
async def get_vp_analytics():
    """Get VP consultation analytics"""
    
    total_consultations = len(consultation_history)
    avg_confidence = sum(c["response"]["confidence_score"] for c in consultation_history) / total_consultations if total_consultations > 0 else 0
    
    return {
        "total_consultations": total_consultations,
        "average_confidence": avg_confidence,
        "escalated_issues": len(vp_memory["escalated_issues"]),
        "memory_items": len(vp_memory),
        "last_consultation": consultation_history[-1]["timestamp"] if consultation_history else None
    }

async def process_vp_query(query: str, context: Optional[Dict[str, Any]]) -> str:
    """Process VP query and generate response"""
    
    # Simulate VP analysis
    if "budget" in query.lower():
        return "Based on current financial analysis, I recommend proceeding with the budget allocation. Our Q4 projections show strong revenue growth that supports this investment."
    
    elif "project" in query.lower():
        return "I've analyzed the project proposal against our strategic objectives. The ROI projections and risk assessment support moving forward. I recommend approval with quarterly review checkpoints."
    
    elif "hiring" in query.lower():
        return "The hiring request aligns with our growth strategy. I've reviewed the budget impact and team capacity. Recommend proceeding with the recruitment process."
    
    else:
        return "I've analyzed your request against our company data and strategic objectives. Based on current metrics and market conditions, I recommend proceeding with the proposed action."

async def update_vp_memory(request: VPRequest, response: VPResponse):
    """Update VP memory with new consultation"""
    
    # Update consultation count
    vp_memory["company_state"]["total_consultations"] = vp_memory["company_state"].get("total_consultations", 0) + 1
    
    # Store key insights
    vp_memory[f"consultation_{request.id}"] = {
        "query": request.query,
        "response": response.response,
        "confidence": response.confidence_score,
        "timestamp": response.timestamp
    } 