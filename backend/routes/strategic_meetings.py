from fastapi import APIRouter, HTTPException, UploadFile, File, Form, BackgroundTasks, WebSocket, WebSocketDisconnect
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import json
import os
from datetime import datetime
import asyncio
import uuid
import hashlib
from pathlib import Path
import threading

router = APIRouter(prefix="/strategic-meetings", tags=["Strategic Meetings"])

# Strategic Meeting Models
class MeetingParticipant(BaseModel):
    id: str
    name: str
    role: str  # "daena", "department_head", "agent", "founder", "hidden_dept"
    department: Optional[str]
    status: str  # "present", "absent", "speaking", "listening"
    voice_enabled: bool = True
    web3_wallet: Optional[str] = None

class MeetingTopic(BaseModel):
    id: str
    title: str
    description: str
    priority: str  # "critical", "high", "medium", "low"
    status: str  # "pending", "discussing", "voting", "resolved", "escalated"
    assigned_departments: List[str]
    llm_consultations: List[Dict[str, Any]]
    honey_knowledge_generated: List[str]
    contract_hash: Optional[str] = None

class StrategicMeeting(BaseModel):
    id: str
    title: str
    description: str
    meeting_type: str  # "daily_standup", "project_review", "crisis_management", "strategic_planning"
    participants: List[MeetingParticipant]
    topics: List[MeetingTopic]
    start_time: datetime
    end_time: Optional[datetime] = None
    status: str  # "scheduled", "in_progress", "completed", "cancelled"
    recording_url: Optional[str] = None
    transcript: List[Dict[str, Any]]
    decisions_made: List[Dict[str, Any]]
    llm_consensus: Dict[str, Any]
    web3_transaction_hash: Optional[str] = None

# Mock data for strategic meetings
mock_meetings = [
    StrategicMeeting(
        id="meeting-001",
        title="Q4 Strategy Planning",
        description="Planning for Q4 business strategy and resource allocation",
        meeting_type="strategic_planning",
        participants=[
            MeetingParticipant(id="daena-001", name="Daena", role="daena", department="executive", status="present", voice_enabled=True),
            MeetingParticipant(id="sunflower-001", name="Sunflower", role="department_head", department="marketing", status="present", voice_enabled=True),
            MeetingParticipant(id="honeycomb-001", name="Honeycomb", role="department_head", department="technology", status="present", voice_enabled=True),
            MeetingParticipant(id="founder-001", name="Founder", role="founder", department="executive", status="present", voice_enabled=True),
        ],
        topics=[
            MeetingTopic(
                id="topic-001",
                title="Market Expansion Strategy",
                description="Discuss expansion into new markets",
                priority="high",
                status="discussing",
                assigned_departments=["marketing", "sales"],
                llm_consultations=[],
                honey_knowledge_generated=[]
            )
        ],
        start_time=datetime.now(),
        end_time=None,
        status="in_progress",
        recording_url=None,
        transcript=[],
        decisions_made=[],
        llm_consensus={}
    )
]

# WebSocket connections for real-time meetings
active_connections: Dict[str, WebSocket] = {}

# File-based persistence helpers (simple JSON per meeting)
PERSIST_DIR = Path("persistent_meeting_logs")
PERSIST_DIR.mkdir(exist_ok=True)
PERSIST_LOCK = threading.Lock()

def persist_meeting(meeting):
    with PERSIST_LOCK:
        path = PERSIST_DIR / f"{meeting.id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(meeting.model_dump(), f, default=str)

def load_meeting(meeting_id):
    path = PERSIST_DIR / f"{meeting_id}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data
    return None

@router.get("/")
async def get_meetings():
    """Get all strategic meetings"""
    return {
        "meetings": mock_meetings,
        "total": len(mock_meetings),
        "active": len([m for m in mock_meetings if m.status == "in_progress"])
    }

@router.post("/")
async def create_meeting(meeting: StrategicMeeting):
    """Create a new strategic meeting"""
    meeting.id = f"meeting-{uuid.uuid4().hex[:8]}"
    meeting.start_time = datetime.now()
    meeting.status = "scheduled"
    mock_meetings.append(meeting)
    
    # Generate Web3 contract hash for meeting
    contract_data = {
        "meeting_id": meeting.id,
        "participants": [p.name for p in meeting.participants],
        "topics": [t.title for t in meeting.topics],
        "timestamp": meeting.start_time.isoformat()
    }
    meeting.web3_transaction_hash = hashlib.sha256(json.dumps(contract_data, sort_keys=True).encode()).hexdigest()
    
    return {"message": "Meeting created successfully", "meeting": meeting}

@router.get("/{meeting_id}")
async def get_meeting(meeting_id: str):
    """Get a specific meeting"""
    for meeting in mock_meetings:
        if meeting.id == meeting_id:
            return meeting
    raise HTTPException(status_code=404, detail="Meeting not found")

@router.post("/{meeting_id}/start")
async def start_meeting(meeting_id: str):
    """Start a meeting"""
    for meeting in mock_meetings:
        if meeting.id == meeting_id:
            meeting.status = "in_progress"
            meeting.start_time = datetime.now()
            return {"message": "Meeting started", "meeting": meeting}
    raise HTTPException(status_code=404, detail="Meeting not found")

@router.post("/{meeting_id}/end")
async def end_meeting(meeting_id: str):
    """End a meeting"""
    for meeting in mock_meetings:
        if meeting.id == meeting_id:
            meeting.status = "completed"
            meeting.end_time = datetime.now()
            return {"message": "Meeting ended", "meeting": meeting}
    raise HTTPException(status_code=404, detail="Meeting not found")

@router.post("/{meeting_id}/topics")
async def add_topic(meeting_id: str, topic: MeetingTopic):
    """Add a topic to a meeting"""
    for meeting in mock_meetings:
        if meeting.id == meeting_id:
            topic.id = f"topic-{uuid.uuid4().hex[:8]}"
            meeting.topics.append(topic)
            return {"message": "Topic added", "topic": topic}
    raise HTTPException(status_code=404, detail="Meeting not found")

@router.post("/{meeting_id}/participants")
async def add_participant(meeting_id: str, participant: MeetingParticipant):
    """Add a participant to a meeting"""
    for meeting in mock_meetings:
        if meeting.id == meeting_id:
            participant.id = f"participant-{uuid.uuid4().hex[:8]}"
            meeting.participants.append(participant)
            return {"message": "Participant added", "participant": participant}
    raise HTTPException(status_code=404, detail="Meeting not found")

@router.post("/{meeting_id}/llm-consultation")
async def request_llm_consultation(meeting_id: str, topic_id: str, llm_models: List[str] = ["gpt-4", "claude-3", "gemini"]):
    """Request LLM consultation for a topic"""
    consultation_result = {
        "id": f"consultation-{uuid.uuid4().hex[:8]}",
        "topic_id": topic_id,
        "models_consulted": llm_models,
        "responses": {},
        "consensus": "",
        "timestamp": datetime.now().isoformat()
    }
    
    # Simulate LLM responses
    for model in llm_models:
        consultation_result["responses"][model] = {
            "response": f"Analysis from {model}: This topic requires strategic consideration...",
            "confidence": 0.85,
            "recommendations": ["Option A", "Option B", "Option C"]
        }
    
    # Generate consensus
    consultation_result["consensus"] = "Based on LLM analysis, recommended approach is Option A with 85% confidence."
    
    # Add to meeting
    for meeting in mock_meetings:
        if meeting.id == meeting_id:
            for topic in meeting.topics:
                if topic.id == topic_id:
                    topic.llm_consultations.append(consultation_result)
                    meeting.llm_consensus = consultation_result
                    return {"message": "LLM consultation completed", "consultation": consultation_result}
    
    raise HTTPException(status_code=404, detail="Meeting or topic not found")

@router.post("/{meeting_id}/decisions")
async def record_decision(meeting_id: str, decision: Dict[str, Any]):
    """Record a decision made in the meeting"""
    decision["id"] = f"decision-{uuid.uuid4().hex[:8]}"
    decision["timestamp"] = datetime.now().isoformat()
    
    for meeting in mock_meetings:
        if meeting.id == meeting_id:
            meeting.decisions_made.append(decision)
            return {"message": "Decision recorded", "decision": decision}
    
    raise HTTPException(status_code=404, detail="Meeting not found")

@router.get("/hidden-departments")
async def get_hidden_departments():
    """Get hidden departments for intelligence gathering"""
    hidden_departments = [
        {
            "id": "intel-001",
            "name": "Intelligence Division",
            "purpose": "Customer behavior analysis and market intelligence",
            "agents": [
                {"id": "agent-intel-001", "name": "Observer", "status": "active", "current_task": "Analyzing customer patterns"},
                {"id": "agent-intel-002", "name": "Analyst", "status": "active", "current_task": "Processing market data"}
            ],
            "active_operations": 3,
            "last_report": datetime.now().isoformat()
        },
        {
            "id": "cyber-001", 
            "name": "Cybersecurity Division",
            "purpose": "Threat monitoring and security analysis",
            "agents": [
                {"id": "agent-cyber-001", "name": "Guardian", "status": "active", "current_task": "Monitoring network traffic"},
                {"id": "agent-cyber-002", "name": "Sentinel", "status": "active", "current_task": "Analyzing security threats"}
            ],
            "active_operations": 2,
            "last_report": datetime.now().isoformat()
        }
    ]
    return {"hidden_departments": hidden_departments}

@router.post("/hidden-departments/{dept_id}/operations")
async def create_hidden_operation(dept_id: str, operation: Dict[str, Any]):
    """Create a new hidden operation"""
    operation["id"] = f"op-{uuid.uuid4().hex[:8]}"
    operation["status"] = "active"
    operation["created_at"] = datetime.now().isoformat()
    return {"message": "Operation created", "operation": operation}

@router.websocket("/ws/{meeting_id}")
async def websocket_endpoint(websocket: WebSocket, meeting_id: str):
    """WebSocket endpoint for real-time meeting communication"""
    await websocket.accept()
    active_connections[meeting_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different message types
            if message["type"] == "join":
                await websocket.send_text(json.dumps({
                    "type": "system",
                    "message": f"Participant {message['participant']} joined the meeting"
                }))
            
            elif message["type"] == "speak":
                await websocket.send_text(json.dumps({
                    "type": "speech",
                    "participant": message["participant"],
                    "message": message["message"],
                    "timestamp": datetime.now().isoformat()
                }))
            
            elif message["type"] == "llm_request":
                # Simulate LLM consultation
                llm_response = {
                    "type": "llm_response",
                    "model": message["model"],
                    "response": f"LLM {message['model']} analysis: {message['query']}",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send_text(json.dumps(llm_response))
    
    except WebSocketDisconnect:
        if meeting_id in active_connections:
            del active_connections[meeting_id]

@router.get("/web3/contracts")
async def get_web3_contracts():
    """Get Web3 contracts for meetings"""
    contracts = []
    for meeting in mock_meetings:
        if meeting.web3_transaction_hash:
            contracts.append({
                "meeting_id": meeting.id,
                "contract_hash": meeting.web3_transaction_hash,
                "participants": [p.name for p in meeting.participants],
                "status": meeting.status,
                "created_at": meeting.start_time.isoformat()
            })
    return {"contracts": contracts}

@router.post("/web3/deploy-contract")
async def deploy_meeting_contract(meeting_id: str):
    """Deploy a Web3 contract for a meeting"""
    # Simulate Web3 contract deployment
    contract_address = f"0x{uuid.uuid4().hex[:40]}"
    return {
        "message": "Contract deployed successfully",
        "contract_address": contract_address,
        "meeting_id": meeting_id,
        "transaction_hash": f"0x{uuid.uuid4().hex[:64]}"
    } 

@router.post("/{meeting_id}/present")
async def present_to_meeting(meeting_id: str, presentation: Dict[str, Any]):
    """Present content to a strategic meeting"""
    for meeting in mock_meetings:
        if meeting.id == meeting_id:
            presentation_entry = {
                "id": f"presentation-{uuid.uuid4().hex[:8]}",
                "type": presentation.get("type", "project"),
                "content": presentation.get("content", ""),
                "presented_by": presentation.get("presented_by", "Daena"),
                "timestamp": datetime.now().isoformat(),
                "participants_reached": len(meeting.participants)
            }
            
            # Add to meeting transcript
            meeting.transcript.append({
                "id": f"msg-{uuid.uuid4().hex[:8]}",
                "sender_name": presentation_entry["presented_by"],
                "content": f"Presented: {presentation_entry['content']}",
                "timestamp": datetime.now().isoformat(),
                "message_type": "presentation"
            })
            
            # Persist meeting
            persist_meeting(meeting)
            
            return {"message": "Presentation added to meeting", "presentation": presentation_entry}
    
    raise HTTPException(status_code=404, detail="Meeting not found")

@router.post("/{meeting_id}/cmp-vote")
async def trigger_cmp_vote(meeting_id: str, question: str = Form(...)):
    """Trigger CMP (Consensus Model Protocol) voting in a meeting"""
    for meeting in mock_meetings:
        if meeting.id == meeting_id:
            # Simulate LLM responses
            llm_responses = {
                "gpt4": {
                    "response": f"GPT-4 analysis: {question} - Based on current market conditions and strategic objectives...",
                    "confidence": 0.92,
                    "reasoning": "High confidence due to comprehensive data analysis"
                },
                "yi": {
                    "response": f"Yi analysis: {question} - Considering the technical feasibility and resource constraints...",
                    "confidence": 0.88,
                    "reasoning": "Good confidence with technical focus"
                },
                "claude": {
                    "response": f"Claude analysis: {question} - From an ethical and strategic perspective...",
                    "confidence": 0.90,
                    "reasoning": "Strong confidence with ethical considerations"
                }
            }
            
            # Daena's summary and decision
            daena_summary = {
                "summary": f"Consensus reached on {question}. All models agree on the strategic direction with slight variations in emphasis.",
                "decision": "Proceed with implementation",
                "confidence": 0.91,
                "consensus_score": 0.89
            }
            
            # Store in meeting
            meeting.llm_consensus = {
                "question": question,
                "responses": llm_responses,
                "daena_summary": daena_summary,
                "timestamp": datetime.now().isoformat()
            }
            
            # Add to transcript
            meeting.transcript.append({
                "id": f"msg-{uuid.uuid4().hex[:8]}",
                "sender_name": "Daena",
                "content": f"CMP Vote completed: {daena_summary['decision']}",
                "timestamp": datetime.now().isoformat(),
                "message_type": "cmp_vote"
            })
            
            # Persist meeting
            persist_meeting(meeting)
            
            return {
                "message": "CMP vote completed",
                "llm_responses": llm_responses,
                "daena_summary": daena_summary
            }
    
    raise HTTPException(status_code=404, detail="Meeting not found")

@router.post("/observer/join")
async def join_observer_mode(user_id: str = Form(...), permissions: List[str] = Form(...)):
    """Join observer mode for strategic meetings"""
    observer_session = {
        "id": f"observer-{uuid.uuid4().hex[:8]}",
        "user_id": user_id,
        "permissions": permissions,
        "mode": "observer",
        "start_time": datetime.now().isoformat(),
        "active_meetings": [],
        "status": "active"
    }
    
    # In a real implementation, you'd store this in a database
    # For now, we'll return the session
    return {
        "message": "Observer mode activated",
        "session": observer_session
    }

@router.post("/observer/{session_id}/leave")
async def leave_observer_mode(session_id: str):
    """Leave observer mode"""
    return {
        "message": "Observer mode deactivated",
        "session_id": session_id,
        "end_time": datetime.now().isoformat()
    }

@router.get("/observer/sessions")
async def get_observer_sessions():
    """Get all active observer sessions"""
    # Mock observer sessions
    mock_sessions = [
        {
            "id": "observer-001",
            "user_id": "founder",
            "permissions": ["read", "observe"],
            "mode": "observer",
            "start_time": datetime.now().isoformat(),
            "active_meetings": ["meeting-001"],
            "status": "active"
        }
    ]
    return {"observer_sessions": mock_sessions}

@router.get("/meetings/{meeting_id}/observer")
async def observe_meeting(meeting_id: str):
    """Founder can observe live meeting without participating"""
    meeting = next((m for m in mock_meetings if m.id == meeting_id), None)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    return {
        "meeting_id": meeting_id,
        "status": meeting.status,
        "participants": [p.name for p in meeting.participants],
        "current_topic": meeting.topics[-1].title if meeting.topics else None,
        "transcript": meeting.transcript,
        "llm_consensus": meeting.llm_consensus,
        "decisions_made": meeting.decisions_made
    } 

@router.post("/founder/override")
async def founder_override(override_request: Dict[str, Any]):
    """Accept override action from founder, record it in CMP memory, and require Daena's confirmation"""
    
    # Validate override request
    required_fields = ["action", "reason", "target_meeting_id", "founder_id"]
    for field in required_fields:
        if field not in override_request:
            raise HTTPException(status_code=400, detail=f"Missing required field: {field}")
    
    # Find the meeting
    meeting_id = override_request["target_meeting_id"]
    meeting = next((m for m in mock_meetings if m.id == meeting_id), None)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    
    # Create override record
    override_record = {
        "id": f"override-{uuid.uuid4().hex[:8]}",
        "timestamp": datetime.now(),
        "founder_id": override_request["founder_id"],
        "action": override_request["action"],
        "reason": override_request["reason"],
        "target_meeting_id": meeting_id,
        "status": "pending_daena_confirmation",
        "daena_confirmation": None
    }
    
    # Simulate Daena's confirmation process
    daena_confirmation = {
        "confirmed": True,
        "response": f"Override accepted. {override_request['action']} will be executed with caution.",
        "timestamp": datetime.now(),
        "confidence": 0.75,
        "additional_notes": "Monitoring required for this override action."
    }
    
    override_record["daena_confirmation"] = daena_confirmation
    override_record["status"] = "confirmed"
    
    # Add to meeting decisions
    meeting.decisions_made.append({
        "type": "founder_override",
        "data": override_record,
        "timestamp": datetime.now()
    })
    
    # Notify meeting participants
    if meeting_id in active_connections:
        await active_connections[meeting_id].send_text(json.dumps({
            "type": "founder_override",
            "data": override_record
        }))
    
    return {
        "message": "Founder override processed",
        "override": override_record,
        "daena_confirmation": daena_confirmation
    }

@router.get("/founder/overrides")
async def get_founder_overrides():
    """Get all founder override actions"""
    overrides = []
    for meeting in mock_meetings:
        for decision in meeting.decisions_made:
            if decision.get("type") == "founder_override":
                overrides.append(decision["data"])
    
    return {
        "overrides": overrides,
        "total_overrides": len(overrides),
        "pending_confirmation": len([o for o in overrides if o["status"] == "pending_daena_confirmation"])
    } 

@router.get("/meetings/{meeting_id}/transcript")
async def get_meeting_transcript(meeting_id: str):
    """Fetch the chat log (transcript) for a meeting (persistent)."""
    meeting = next((m for m in mock_meetings if m.id == meeting_id), None)
    if not meeting:
        # Try to load from file
        data = load_meeting(meeting_id)
        if data:
            return {"transcript": data.get("transcript", [])}
        raise HTTPException(status_code=404, detail="Meeting not found")
    return {"transcript": meeting.transcript}

@router.post("/meetings/{meeting_id}/transcript")
async def append_meeting_transcript(meeting_id: str, message: Dict[str, Any]):
    """Append a chat message to the meeting transcript (persistent)."""
    meeting = next((m for m in mock_meetings if m.id == meeting_id), None)
    if not meeting:
        raise HTTPException(status_code=404, detail="Meeting not found")
    message["id"] = f"msg-{uuid.uuid4().hex[:8]}"
    message["timestamp"] = datetime.now().isoformat()
    meeting.transcript.append(message)
    persist_meeting(meeting)
    return {"message": "Message added", "msg": message}

# Observer join/leave (track in-memory for now)
active_observers: Dict[str, List[str]] = {}  # meeting_id -> list of observer ids

@router.post("/meetings/{meeting_id}/observer/join")
async def observer_join(meeting_id: str, observer_id: str = Form(...)):
    """Join a meeting as observer."""
    if meeting_id not in active_observers:
        active_observers[meeting_id] = []
    if observer_id not in active_observers[meeting_id]:
        active_observers[meeting_id].append(observer_id)
    return {"message": f"Observer {observer_id} joined meeting {meeting_id}"}

@router.post("/meetings/{meeting_id}/observer/leave")
async def observer_leave(meeting_id: str, observer_id: str = Form(...)):
    """Leave observer mode for a meeting."""
    if meeting_id in active_observers and observer_id in active_observers[meeting_id]:
        active_observers[meeting_id].remove(observer_id)
        return {"message": f"Observer {observer_id} left meeting {meeting_id}"}
    return {"message": f"Observer {observer_id} was not in meeting {meeting_id}"}

# Participant voting (CMP voting, not just LLMs)
participant_votes: Dict[str, List[Dict[str, Any]]] = {}  # meeting_id -> list of votes

@router.get("/meetings/{meeting_id}/votes")
async def get_participant_votes(meeting_id: str):
    """Get all participant votes for a meeting."""
    return {"votes": participant_votes.get(meeting_id, [])}

@router.post("/meetings/{meeting_id}/votes")
async def submit_participant_vote(meeting_id: str, vote: Dict[str, Any]):
    """Submit a participant vote for a meeting."""
    vote["id"] = f"vote-{uuid.uuid4().hex[:8]}"
    vote["timestamp"] = datetime.now().isoformat()
    if meeting_id not in participant_votes:
        participant_votes[meeting_id] = []
    participant_votes[meeting_id].append(vote)
    return {"message": "Vote submitted", "vote": vote}

# Audit log: all events (chat, votes, presentations, overrides)
@router.get("/meetings/{meeting_id}/audit-log")
async def get_meeting_audit_log(meeting_id: str):
    """Fetch all meeting events: transcript, votes, presentations, overrides."""
    meeting = next((m for m in mock_meetings if m.id == meeting_id), None)
    if not meeting:
        data = load_meeting(meeting_id)
        if not data:
            raise HTTPException(status_code=404, detail="Meeting not found")
        transcript = data.get("transcript", [])
    else:
        transcript = meeting.transcript
    votes = participant_votes.get(meeting_id, [])
    # For simplicity, treat presentations as transcript events with type 'presentation'
    presentations = [e for e in transcript if e.get("type") == "presentation"]
    # Founder overrides (search transcript for type 'override' or use a separate log if needed)
    overrides = [e for e in transcript if e.get("type") == "override"]
    return {
        "transcript": transcript,
        "votes": votes,
        "presentations": presentations,
        "overrides": overrides
    } 