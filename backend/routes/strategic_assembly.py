from fastapi import APIRouter, HTTPException, Depends, Request
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any
from datetime import datetime
import os
import logging

from backend.services.auth_service import auth_service, User
from backend.services.council_service import council_service
from backend.services.websocket_service import websocket_manager
from backend.models.council import AdvisorModel, ScoutModel, SynthesizerModel, DebateRecordModel

router = APIRouter(prefix="/api/v1/strategic-assembly", tags=["strategic-assembly"])
security = HTTPBearer()

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "templates"))

# In-memory assembly state
ASSEMBLY_STATE = {
    "sessions": [],
    "cross_department_synthesis": [],
    "founder_decisions": []
}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    return auth_service.get_current_user(credentials)

@router.get("/dashboard")
async def strategic_assembly_dashboard(request: Request):
    """Strategic Assembly Dashboard"""
    return templates.TemplateResponse("strategic_assembly_dashboard.html", {"request": request})

@router.get("/sessions")
async def get_assembly_sessions(user: User = Depends(get_current_user)):
    """Get all strategic assembly sessions"""
    return {
        "success": True,
        "sessions": ASSEMBLY_STATE["sessions"],
        "total_sessions": len(ASSEMBLY_STATE["sessions"])
    }

@router.post("/sessions/create")
async def create_assembly_session(session_data: Dict[str, Any], user: User = Depends(get_current_user)):
    """Create a new strategic assembly session"""
    session_id = f"assembly-{datetime.now().strftime('%Y%m%d%H%M%S')}"
    
    session = {
        "session_id": session_id,
        "title": session_data.get("title", "Strategic Assembly Session"),
        "departments": session_data.get("departments", []),
        "topic": session_data.get("topic", "Cross-department strategic alignment"),
        "created_by": user.username,
        "created_at": datetime.now().isoformat(),
        "status": "active",
        "participants": [],
        "synthesis": None
    }
    
    ASSEMBLY_STATE["sessions"].append(session)
    
    # Notify via WebSocket
    await websocket_manager.send_founder_alert("assembly_session_created", {
        "session_id": session_id,
        "title": session["title"],
        "departments": session["departments"]
    })
    
    return {"success": True, "session": session}

@router.post("/sessions/{session_id}/debate")
async def run_cross_department_debate(session_id: str, debate_data: Dict[str, Any], user: User = Depends(get_current_user)):
    """Run debate across multiple departments"""
    session = next((s for s in ASSEMBLY_STATE["sessions"] if s["session_id"] == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    # Collect advisors from all participating departments
    all_advisors = []
    for dept in session["departments"]:
        dept_advisors = [
            AdvisorModel(name="Steve Jobs", persona="Visionary", expertise="Product/UX"),
            AdvisorModel(name="Satya Nadella", persona="Empathetic Leader", expertise="Tech/Strategy"),
            AdvisorModel(name="Sheryl Sandberg", persona="Operational Excellence", expertise="Ops/HR"),
            AdvisorModel(name="Elon Musk", persona="Bold Innovator", expertise="Engineering/Scale"),
            AdvisorModel(name="Indra Nooyi", persona="Strategic Thinker", expertise="Finance/Strategy")
        ]
        all_advisors.extend(dept_advisors)
    
    # Run cross-department debate
    topic = debate_data.get("topic", session["topic"])
    debate = await council_service.run_debate(f"assembly-{session_id}", topic, all_advisors)
    
    # Store debate in session
    session["debate"] = debate.dict()
    session["last_updated"] = datetime.now().isoformat()
    
    # Notify via WebSocket
    await websocket_manager.send_council_update("assembly", "cross_department_debate", {
        "session_id": session_id,
        "debate": debate.dict(),
        "departments": session["departments"]
    })
    
    return {"success": True, "debate": debate.dict()}

@router.post("/sessions/{session_id}/synthesis")
async def run_cross_department_synthesis(session_id: str, synthesis_data: Dict[str, Any], user: User = Depends(get_current_user)):
    """Run synthesis across multiple departments"""
    session = next((s for s in ASSEMBLY_STATE["sessions"] if s["session_id"] == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    if not session.get("debate"):
        raise HTTPException(status_code=400, detail="No debate found for synthesis")
    
    # Create cross-department scouts
    scouts = [
        ScoutModel(name="Cross-Dept Scout Alpha", focus_area="Inter-departmental Alignment", sources=["dept1", "dept2"]),
        ScoutModel(name="Cross-Dept Scout Beta", focus_area="Strategic Synergies", sources=["dept3", "dept4"])
    ]
    
    # Run synthesis
    debate_obj = DebateRecordModel(**session["debate"])
    scout_findings = await council_service.run_scouts(f"assembly-{session_id}", scouts)
    synthesizer = SynthesizerModel(name="Assembly SynthAI", model="gpt-4", last_synced=datetime.now().isoformat())
    
    synthesis = await council_service.run_synthesis(f"assembly-{session_id}", debate_obj, scout_findings, synthesizer)
    
    # Store synthesis
    session["synthesis"] = synthesis.dict()
    session["last_updated"] = datetime.now().isoformat()
    
    # Add to cross-department synthesis history
    ASSEMBLY_STATE["cross_department_synthesis"].append({
        "session_id": session_id,
        "synthesis": synthesis.dict(),
        "departments": session["departments"],
        "created_at": datetime.now().isoformat()
    })
    
    # Notify founder
    await websocket_manager.send_founder_alert("cross_department_synthesis_complete", {
        "session_id": session_id,
        "synthesis": synthesis.dict(),
        "departments": session["departments"]
    })
    
    return {"success": True, "synthesis": synthesis.dict()}

@router.post("/sessions/{session_id}/founder-decision")
async def founder_decision(session_id: str, decision_data: Dict[str, Any], user: User = Depends(get_current_user)):
    """Founder decision on cross-department synthesis"""
    if user.role != "founder":
        raise HTTPException(status_code=403, detail="Only founder can make decisions")
    
    session = next((s for s in ASSEMBLY_STATE["sessions"] if s["session_id"] == session_id), None)
    if not session:
        raise HTTPException(status_code=404, detail="Session not found")
    
    decision = {
        "session_id": session_id,
        "decision": decision_data.get("decision", "approved"),
        "comment": decision_data.get("comment", ""),
        "action_items": decision_data.get("action_items", []),
        "made_by": user.username,
        "made_at": datetime.now().isoformat()
    }
    
    session["founder_decision"] = decision
    session["status"] = "completed"
    session["last_updated"] = datetime.now().isoformat()
    
    # Add to founder decisions history
    ASSEMBLY_STATE["founder_decisions"].append(decision)
    
    # Notify all departments
    await websocket_manager.broadcast_to_all({
        "type": "founder_decision",
        "session_id": session_id,
        "decision": decision,
        "departments": session["departments"]
    })
    
    return {"success": True, "decision": decision}

@router.get("/synthesis/history")
async def get_synthesis_history(user: User = Depends(get_current_user)):
    """Get cross-department synthesis history"""
    return {
        "success": True,
        "synthesis_history": ASSEMBLY_STATE["cross_department_synthesis"],
        "total_syntheses": len(ASSEMBLY_STATE["cross_department_synthesis"])
    }

@router.get("/decisions/history")
async def get_decisions_history(user: User = Depends(get_current_user)):
    """Get founder decisions history"""
    return {
        "success": True,
        "decisions_history": ASSEMBLY_STATE["founder_decisions"],
        "total_decisions": len(ASSEMBLY_STATE["founder_decisions"])
    } 