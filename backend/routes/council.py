from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import List, Dict, Any
from datetime import datetime
import uuid
from fastapi.templating import Jinja2Templates
from fastapi import Request
import os
import logging

from backend.services.council_service import council_service
from backend.services.auth_service import auth_service, User
from backend.models.council import AdvisorModel, ScoutModel, SynthesizerModel, DebateRecordModel

router = APIRouter(prefix="/api/v1/council", tags=["council"])
security = HTTPBearer()

# Audit logging
logger = logging.getLogger(__name__)

def audit_log(action: str, user: str, details: dict):
    """Audit logging for council actions"""
    logger.info(f"Council Action: {action} by {user} - {details}")

# Authentication dependency
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    return auth_service.get_current_user(credentials)

# Optional authentication for public endpoints
def get_current_user_optional(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current user if authenticated, otherwise return None"""
    try:
        return auth_service.get_current_user(credentials)
    except:
        return None

# In-memory council state (to be replaced with DB/service)
COUNCIL_STATE = {}

templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "templates"))

@router.get("/{department}/panel")
async def get_council_panel(department: str, request: Request):
    state = COUNCIL_STATE.get(department, {"advisors": [], "scouts": [], "synthesizer": None, "debate_history": [], "last_synthesis": None})
    return templates.TemplateResponse("council_panel.html", {"request": request, "council": state, "department": department})

@router.get("/{department}/debate-panel")
async def get_council_debate_panel(department: str, request: Request):
    state = COUNCIL_STATE.get(department, {"advisors": [], "scouts": [], "synthesizer": None, "debate_history": [], "last_synthesis": None})
    debate = state["debate_history"][-1] if state["debate_history"] else None
    return templates.TemplateResponse("council_debate_panel.html", {"request": request, "debate": debate, "department": department})

@router.get("/{department}/synthesis-panel")
async def get_council_synthesis_panel(department: str, request: Request):
    state = COUNCIL_STATE.get(department, {"advisors": [], "scouts": [], "synthesizer": None, "debate_history": [], "last_synthesis": None})
    synthesis = state["last_synthesis"] if state["last_synthesis"] else None
    return templates.TemplateResponse("council_synthesis_panel.html", {"request": request, "synthesis": synthesis, "department": department})

@router.get("/{department}")
async def get_council_state(department: str, user: User = Depends(get_current_user)):
    """Get council state for a department"""
    audit_log("get_council_state", user.username, {"department": department})
    
    # Initialize council state if it doesn't exist
    if department not in COUNCIL_STATE:
        # Get department-specific councilors
        councilors = council_service.get_department_councilors(department)
        
        COUNCIL_STATE[department] = {
            "advisors": councilors["advisors"],
            "scouts": councilors["scouts"],
            "synthesizer": {
                "name": "SynthAI",
                "model": "gpt-4",
                "last_synced": datetime.now().isoformat(),
                "description": "AI Synthesizer that combines expert insights into actionable recommendations"
            },
            "debate_history": [],
            "last_synthesis": None,
            "department": department,
            "department_display_name": councilors["department_display_name"]
        }
    
    state = COUNCIL_STATE[department]
    return {"success": True, "council": state}

@router.post("/{department}/debate")
async def post_council_debate(department: str, debate_input: Dict[str, Any], user: User = Depends(get_current_user)):
    audit_log("post_council_debate", user.username, {"department": department, "debate_input": debate_input})
    topic = debate_input.get("topic", "Default council topic")
    
    # Ensure council state exists
    if department not in COUNCIL_STATE:
        await get_council_state(department, user)
    
    # Use existing advisors from council state
    advisors = COUNCIL_STATE[department]["advisors"]
    debate = await council_service.run_debate(department, topic, advisors)
    COUNCIL_STATE[department]["debate_history"].append(debate.dict())
    return {"success": True, "debate": debate.dict()}

@router.post("/{department}/synthesis")
async def post_council_synthesis(department: str, synthesis_input: Dict[str, Any], user: User = Depends(get_current_user)):
    audit_log("post_council_synthesis", user.username, {"department": department, "synthesis_input": synthesis_input})
    
    # Ensure council state exists
    if department not in COUNCIL_STATE:
        await get_council_state(department, user)
    
    # Use last debate
    debate = None
    if COUNCIL_STATE[department]["debate_history"]:
        debate = COUNCIL_STATE[department]["debate_history"][-1]
    else:
        return {"success": False, "error": "No debate found for synthesis."}
    
    debate_obj = DebateRecordModel(**debate)
    scouts = COUNCIL_STATE[department]["scouts"]
    scout_findings = await council_service.run_scouts(department, scouts)
    synthesizer = COUNCIL_STATE[department]["synthesizer"]
    synthesis = await council_service.run_synthesis(department, debate_obj, scout_findings, synthesizer)
    COUNCIL_STATE[department]["last_synthesis"] = synthesis.dict()
    council_service.save_outcome(department, synthesis)
    return {"success": True, "synthesis": synthesis.dict()}

@router.post("/{department}/update-scouting")
async def post_update_scouting(department: str, scouting_input: Dict[str, Any], user: User = Depends(get_current_user)):
    """Update advisor/scout knowledge for a department"""
    audit_log("post_update_scouting", user.username, {"department": department, "scouting_input": scouting_input})
    # TODO: Integrate with advisor/scout retraining logic
    COUNCIL_STATE.setdefault(department, {"advisors": [], "scouts": [], "debate_history": [], "synthesizer": None, "last_synthesis": None})
    COUNCIL_STATE[department]["scouts"].append({
        "update": scouting_input,
        "timestamp": datetime.now().isoformat()
    })
    return {"success": True}

@router.post("/{department}/founder-feedback")
async def post_founder_feedback(department: str, feedback: Dict[str, str], user: User = Depends(get_current_user)):
    audit_log("post_founder_feedback", user.username, {"department": department, "feedback": feedback})
    # Attach founder feedback to last synthesis
    state = COUNCIL_STATE.setdefault(department, {"advisors": [], "scouts": [], "debate_history": [], "synthesizer": None, "last_synthesis": None})
    if state["last_synthesis"]:
        state["last_synthesis"]["founder_feedback"] = feedback.get("comment", "")
        # Optionally, mark as overridden
        if feedback.get("override"):
            state["last_synthesis"]["outcome"] = "overridden"
        # Re-autosave
        from backend.services.council_service import council_service
        from backend.models.council import SynthesisRecordModel
        council_service.save_outcome(department, SynthesisRecordModel(**state["last_synthesis"]))
        return {"success": True, "updated": True}
    return {"success": False, "error": "No synthesis to update."}

@router.post("/{department}/rerun-debate")
async def rerun_debate(department: str, user: User = Depends(get_current_user)):
    audit_log("rerun_debate", user.username, {"department": department})
    # Use last topic and advisors
    state = COUNCIL_STATE.setdefault(department, {"advisors": [], "scouts": [], "debate_history": [], "synthesizer": None, "last_synthesis": None})
    if state["debate_history"]:
        topic = state["debate_history"][-1]["topic"]
    else:
        topic = "Default council topic"
    advisors = [
        AdvisorModel(name="Steve Jobs", persona="Visionary", expertise="Product/UX"),
        AdvisorModel(name="Satya Nadella", persona="Empathetic Leader", expertise="Tech/Strategy"),
        AdvisorModel(name="Sheryl Sandberg", persona="Operational Excellence", expertise="Ops/HR"),
        AdvisorModel(name="Elon Musk", persona="Bold Innovator", expertise="Engineering/Scale"),
        AdvisorModel(name="Indra Nooyi", persona="Strategic Thinker", expertise="Finance/Strategy")
    ]
    from backend.services.council_service import council_service
    debate = await council_service.run_debate(department, topic, advisors)
    state["debate_history"].append(debate.dict())
    return {"success": True, "debate": debate.dict()}

@router.post("/{department}/rerun-synthesis")
async def rerun_synthesis(department: str, user: User = Depends(get_current_user)):
    audit_log("rerun_synthesis", user.username, {"department": department})
    state = COUNCIL_STATE.setdefault(department, {"advisors": [], "scouts": [], "debate_history": [], "synthesizer": None, "last_synthesis": None})
    if not state["debate_history"]:
        return {"success": False, "error": "No debate to synthesize."}
    from backend.services.council_service import council_service
    from backend.models.council import DebateRecordModel, ScoutModel, SynthesizerModel
    debate_obj = DebateRecordModel(**state["debate_history"][-1])
    scouts = [ScoutModel(name="Scout Alpha", focus_area="AI Trends", sources=["source1", "source2"]), ScoutModel(name="Scout Beta", focus_area="Market Research", sources=["source3"])]
    scout_findings = await council_service.run_scouts(department, scouts)
    synthesizer = SynthesizerModel(name="SynthAI", model="gpt-4", last_synced=datetime.now().isoformat())
    synthesis = await council_service.run_synthesis(department, debate_obj, scout_findings, synthesizer)
    state["last_synthesis"] = synthesis.dict()
    council_service.save_outcome(department, synthesis)
    return {"success": True, "synthesis": synthesis.dict()} 