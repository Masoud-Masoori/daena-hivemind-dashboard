"""
Strategic Room Routes for Daena AI VP System
Aggregates synthesis from all departments and provides founder oversight
"""

from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any, Optional
from datetime import datetime, timedelta
import os
import logging
import json

from backend.services.auth_service import auth_service, User
from backend.services.council_service import council_service

router = APIRouter(prefix="/api/v1/strategic-room", tags=["strategic-room"])
security = HTTPBearer()

# Audit logging
logger = logging.getLogger(__name__)

def audit_log(action: str, user: str, details: dict):
    """Audit logging for strategic room actions"""
    logger.info(f"Strategic Room Action: {action} by {user} - {details}")

# Authentication dependency
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    return auth_service.get_current_user(credentials)

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "templates"))

@router.get("/")
async def get_strategic_room_page(request: Request):
    """Get the strategic room dashboard page"""
    return templates.TemplateResponse("strategic_room.html", {"request": request})

@router.get("/synthesis-summary")
async def get_synthesis_summary(user: User = Depends(get_current_user)):
    """Get aggregated synthesis from all departments"""
    audit_log("get_synthesis_summary", user.username, {})
    
    departments = ["engineering", "product", "marketing", "sales", "finance", "hr", "operations", "legal"]
    synthesis_data = {}
    
    for dept in departments:
        try:
            # Get latest synthesis from each department
            synthesis_file = f"knowledge/{dept}/latest_synthesis.json"
            if os.path.exists(synthesis_file):
                with open(synthesis_file, 'r') as f:
                    synthesis_data[dept] = json.load(f)
            else:
                synthesis_data[dept] = {
                    "department": dept,
                    "last_synthesis": None,
                    "status": "no_synthesis"
                }
        except Exception as e:
            logger.error(f"Error loading synthesis for {dept}: {e}")
            synthesis_data[dept] = {
                "department": dept,
                "last_synthesis": None,
                "status": "error"
            }
    
    return {
        "success": True,
        "synthesis_summary": synthesis_data,
        "timestamp": datetime.now().isoformat()
    }

@router.get("/conflicts-analysis")
async def get_conflicts_analysis(user: User = Depends(get_current_user)):
    """Analyze potential conflicts between department syntheses"""
    audit_log("get_conflicts_analysis", user.username, {})
    
    # Get synthesis from all departments
    synthesis_response = await get_synthesis_summary(user)
    synthesis_data = synthesis_response["synthesis_summary"]
    
    conflicts = []
    overlaps = []
    
    # Analyze for conflicts and overlaps
    dept_syntheses = []
    for dept, data in synthesis_data.items():
        if data.get("last_synthesis"):
            dept_syntheses.append({
                "department": dept,
                "synthesis": data["last_synthesis"]
            })
    
    # Simple conflict detection (can be enhanced with LLM analysis)
    for i, dept1 in enumerate(dept_syntheses):
        for j, dept2 in enumerate(dept_syntheses[i+1:], i+1):
            # Check for resource conflicts
            if "resource" in dept1["synthesis"].get("summary", "").lower() and \
               "resource" in dept2["synthesis"].get("summary", "").lower():
                conflicts.append({
                    "type": "resource_conflict",
                    "departments": [dept1["department"], dept2["department"]],
                    "description": f"Potential resource allocation conflict between {dept1['department']} and {dept2['department']}"
                })
            
            # Check for timeline conflicts
            if "timeline" in dept1["synthesis"].get("summary", "").lower() and \
               "timeline" in dept2["synthesis"].get("summary", "").lower():
                overlaps.append({
                    "type": "timeline_overlap",
                    "departments": [dept1["department"], dept2["department"]],
                    "description": f"Timeline overlap detected between {dept1['department']} and {dept2['department']}"
                })
    
    return {
        "success": True,
        "conflicts": conflicts,
        "overlaps": overlaps,
        "analysis_timestamp": datetime.now().isoformat()
    }

@router.post("/founder-override")
async def founder_override(
    override_data: Dict[str, Any],
    user: User = Depends(get_current_user)
):
    """Allow founder to override or comment on synthesis"""
    audit_log("founder_override", user.username, override_data)
    
    if user.role != "founder":
        raise HTTPException(status_code=403, detail="Only founders can override synthesis")
    
    department = override_data.get("department")
    action = override_data.get("action")  # "override", "comment", "approve"
    comment = override_data.get("comment", "")
    
    # Save founder feedback
    feedback_file = f"knowledge/{department}/founder_feedback.json"
    feedback_data = {
        "timestamp": datetime.now().isoformat(),
        "founder": user.username,
        "action": action,
        "comment": comment,
        "original_synthesis": override_data.get("original_synthesis")
    }
    
    try:
        os.makedirs(os.path.dirname(feedback_file), exist_ok=True)
        with open(feedback_file, 'w') as f:
            json.dump(feedback_data, f, indent=2)
    except Exception as e:
        logger.error(f"Error saving founder feedback: {e}")
        raise HTTPException(status_code=500, detail="Failed to save feedback")
    
    return {
        "success": True,
        "message": f"Founder {action} recorded for {department}",
        "feedback": feedback_data
    }

@router.get("/department/{department}/synthesis")
async def get_department_synthesis(
    department: str,
    user: User = Depends(get_current_user)
):
    """Get detailed synthesis for a specific department"""
    audit_log("get_department_synthesis", user.username, {"department": department})
    
    try:
        synthesis_file = f"knowledge/{department}/latest_synthesis.json"
        if os.path.exists(synthesis_file):
            with open(synthesis_file, 'r') as f:
                synthesis = json.load(f)
        else:
            synthesis = {
                "department": department,
                "last_synthesis": None,
                "status": "no_synthesis"
            }
        
        # Get founder feedback if exists
        feedback_file = f"knowledge/{department}/founder_feedback.json"
        feedback = None
        if os.path.exists(feedback_file):
            with open(feedback_file, 'r') as f:
                feedback = json.load(f)
        
        return {
            "success": True,
            "synthesis": synthesis,
            "founder_feedback": feedback
        }
    except Exception as e:
        logger.error(f"Error loading department synthesis: {e}")
        raise HTTPException(status_code=500, detail="Failed to load synthesis")

@router.post("/generate-cross-department-analysis")
async def generate_cross_department_analysis(
    analysis_request: Dict[str, Any],
    user: User = Depends(get_current_user)
):
    """Generate cross-department analysis using LLM"""
    audit_log("generate_cross_department_analysis", user.username, analysis_request)
    
    # Get synthesis from all departments
    synthesis_response = await get_synthesis_summary(user)
    synthesis_data = synthesis_response["synthesis_summary"]
    
    # Prepare prompt for cross-department analysis
    prompt = f"""
    As Daena AI VP, analyze the following department syntheses and provide:
    1. Cross-department synergies and opportunities
    2. Potential conflicts or resource allocation issues
    3. Strategic recommendations for the founder
    4. Priority action items
    
    Department Syntheses:
    {json.dumps(synthesis_data, indent=2)}
    
    Analysis Request: {analysis_request.get('focus', 'general')}
    """
    
    try:
        # Use council service LLM for analysis
        analysis = await council_service.llm.generate_response(
            prompt=prompt,
            provider="openai",
            model="gpt-4",
            temperature=0.7,
            max_tokens=2000
        )
        
        # Save analysis
        analysis_file = f"knowledge/strategic_room/cross_department_analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs(os.path.dirname(analysis_file), exist_ok=True)
        
        analysis_data = {
            "timestamp": datetime.now().isoformat(),
            "requested_by": user.username,
            "focus": analysis_request.get('focus', 'general'),
            "analysis": analysis,
            "synthesis_data": synthesis_data
        }
        
        with open(analysis_file, 'w') as f:
            json.dump(analysis_data, f, indent=2)
        
        return {
            "success": True,
            "analysis": analysis,
            "analysis_file": analysis_file
        }
        
    except Exception as e:
        logger.error(f"Error generating cross-department analysis: {e}")
        raise HTTPException(status_code=500, detail="Failed to generate analysis") 