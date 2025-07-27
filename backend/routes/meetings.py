"""
Enhanced Meeting System Router
CMP discussions, multiple simultaneous rooms, real-time participation, knowledge extraction
"""

from fastapi import APIRouter, Depends, HTTPException, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import json
import asyncio
from enum import Enum

# Import database models
from models.database import get_session, Meeting, MeetingParticipant, Agent, User, KnowledgeBase, Message

router = APIRouter(prefix="/api/v1/meetings", tags=["Meetings & CMP"])

# Enums
class MeetingType(str, Enum):
    CMP_DISCUSSION = "cmp_discussion"
    PROJECT_REVIEW = "project_review"
    BRAINSTORM = "brainstorm"
    STRATEGIC_PLANNING = "strategic_planning"
    CROSS_DEPARTMENT = "cross_department"
    EMERGENCY = "emergency"

class ParticipantRole(str, Enum):
    MODERATOR = "moderator"
    PARTICIPANT = "participant"
    OBSERVER = "observer"
    AI_AGENT = "ai_agent"

# Pydantic models
class MeetingCreate(BaseModel):
    title: str
    description: Optional[str] = None
    meeting_type: MeetingType
    department_id: Optional[int] = None
    scheduled_start: datetime
    scheduled_end: datetime
    agenda: List[Dict] = []
    objectives: List[str] = []
    max_participants: int = 10
    is_public: bool = True
    priority_level: int = 3

class JoinMeetingRequest(BaseModel):
    user_id: Optional[int] = None
    agent_id: Optional[int] = None
    role: ParticipantRole = ParticipantRole.PARTICIPANT

class CMPMessage(BaseModel):
    content: str
    message_type: str = "discussion"  # discussion, question, answer, conclusion, vote
    responding_to: Optional[str] = None
    metadata: Optional[Dict] = None

class CMPResponse(BaseModel):
    agent_name: str
    content: str
    confidence: float
    reasoning: str
    supporting_data: Optional[Dict] = None

# WebSocket connection manager
class MeetingConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, List[WebSocket]] = {}
        self.meeting_participants: Dict[str, List[Dict]] = {}
    
    async def connect(self, websocket: WebSocket, meeting_id: str, participant_info: Dict):
        await websocket.accept()
        if meeting_id not in self.active_connections:
            self.active_connections[meeting_id] = []
            self.meeting_participants[meeting_id] = []
        
        self.active_connections[meeting_id].append(websocket)
        self.meeting_participants[meeting_id].append(participant_info)
        
        # Notify others about new participant
        await self.broadcast_to_meeting(meeting_id, {
            "type": "participant_joined",
            "participant": participant_info,
            "timestamp": datetime.utcnow().isoformat()
        })
    
    def disconnect(self, websocket: WebSocket, meeting_id: str):
        if meeting_id in self.active_connections:
            self.active_connections[meeting_id].remove(websocket)
            if not self.active_connections[meeting_id]:
                del self.active_connections[meeting_id]
                del self.meeting_participants[meeting_id]
    
    async def broadcast_to_meeting(self, meeting_id: str, message: Dict):
        if meeting_id in self.active_connections:
            disconnected = []
            for connection in self.active_connections[meeting_id]:
                try:
                    await connection.send_text(json.dumps(message))
                except:
                    disconnected.append(connection)
            
            # Remove disconnected connections
            for conn in disconnected:
                self.active_connections[meeting_id].remove(conn)

manager = MeetingConnectionManager()

# Helper functions
async def generate_cmp_responses(question: str, context: Dict = None) -> List[CMPResponse]:
    """Generate responses from multiple AI agents for CMP discussion"""
    # Simulated AI agent responses - integrate with actual LLMs
    agents_responses = [
        CMPResponse(
            agent_name="Analytics Agent",
            content=f"Based on data analysis, regarding '{question[:30]}...', I see a 73% correlation with previous successful outcomes.",
            confidence=0.85,
            reasoning="Historical data analysis shows strong patterns in similar scenarios"
        ),
        CMPResponse(
            agent_name="Strategy Agent", 
            content=f"From a strategic perspective on '{question[:30]}...', this aligns with our Q1 objectives but may require resource reallocation.",
            confidence=0.78,
            reasoning="Strategic framework evaluation indicates moderate complexity with clear execution path"
        ),
        CMPResponse(
            agent_name="Risk Assessment Agent",
            content=f"Risk analysis for '{question[:30]}...' shows medium risk profile with manageable mitigation strategies.",
            confidence=0.82,
            reasoning="Comprehensive risk modeling indicates acceptable risk levels with proper controls"
        )
    ]
    return agents_responses

async def extract_meeting_knowledge(meeting_id: str, session):
    """Extract knowledge from meeting discussions and save to knowledge base"""
    meeting = session.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
    if not meeting:
        return
    
    # Get all messages from the meeting
    # This would analyze the conversation and extract key insights
    knowledge_entry = KnowledgeBase(
        knowledge_id=str(uuid.uuid4()),
        title=f"Insights from {meeting.title}",
        content=f"Key decisions and insights from meeting: {meeting.title}",
        knowledge_type="meeting_summary",
        source_type="meeting",
        source_meeting_id=meeting.id,
        participants=[p.user_id or p.agent_id for p in meeting.participants],
        priority_level=meeting.priority_level,
        confidence_score=0.8,
        tags=["meeting", "summary", meeting.meeting_type]
    )
    session.add(knowledge_entry)
    session.commit()

# Meeting Management Routes
@router.post("/create", response_model=Dict)
async def create_meeting(meeting_data: MeetingCreate):
    """Create a new meeting"""
    session = get_session()
    try:
        meeting_id = str(uuid.uuid4())
        meeting_room_id = f"room_{meeting_id[:8]}"
        
        meeting = Meeting(
            meeting_id=meeting_id,
            title=meeting_data.title,
            description=meeting_data.description,
            department_id=meeting_data.department_id,
            meeting_type=meeting_data.meeting_type,
            scheduled_start=meeting_data.scheduled_start,
            scheduled_end=meeting_data.scheduled_end,
            meeting_room_id=meeting_room_id,
            agenda=meeting_data.agenda,
            objectives=meeting_data.objectives,
            priority_level=meeting_data.priority_level,
            is_public=meeting_data.is_public,
            max_participants=meeting_data.max_participants,
            status="scheduled"
        )
        session.add(meeting)
        session.commit()
        
        # If it's a CMP discussion, auto-add AI agents
        if meeting_data.meeting_type == MeetingType.CMP_DISCUSSION:
            ai_agents = session.query(Agent).filter(Agent.status == "active").limit(5).all()
            for agent in ai_agents:
                participant = MeetingParticipant(
                    meeting_id=meeting.id,
                    participant_type="agent",
                    agent_id=agent.id,
                    role="ai_agent",
                    is_present=False
                )
                session.add(participant)
            session.commit()
        
        return {
            "meeting_id": meeting_id,
            "room_id": meeting_room_id,
            "status": "created",
            "websocket_url": f"/ws/meetings/{meeting_id}",
            "join_url": f"/meetings/{meeting_id}/join",
            "scheduled_start": meeting_data.scheduled_start
        }
    finally:
        session.close()

@router.get("/active")
async def get_active_meetings():
    """Get all currently active meetings"""
    session = get_session()
    try:
        current_time = datetime.utcnow()
        
        # Active meetings (in progress or about to start)
        active_meetings = session.query(Meeting).filter(
            Meeting.status.in_(["scheduled", "active"]),
            Meeting.scheduled_start <= current_time + timedelta(hours=1),
            Meeting.scheduled_end >= current_time - timedelta(minutes=30)
        ).order_by(Meeting.scheduled_start).all()
        
        return {
            "active_meetings": [
                {
                    "meeting_id": meeting.meeting_id,
                    "title": meeting.title,
                    "meeting_type": meeting.meeting_type,
                    "room_id": meeting.meeting_room_id,
                    "status": meeting.status,
                    "scheduled_start": meeting.scheduled_start,
                    "scheduled_end": meeting.scheduled_end,
                    "participant_count": len(meeting.participants),
                    "max_participants": meeting.max_participants,
                    "is_public": meeting.is_public,
                    "department": meeting.department.name if meeting.department else "Cross-department"
                }
                for meeting in active_meetings
            ]
        }
    finally:
        session.close()

@router.post("/{meeting_id}/join")
async def join_meeting(meeting_id: str, join_request: JoinMeetingRequest):
    """Join a meeting"""
    session = get_session()
    try:
        meeting = session.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        # Check if meeting is full
        current_participants = len([p for p in meeting.participants if p.is_present])
        if current_participants >= meeting.max_participants:
            raise HTTPException(status_code=403, detail="Meeting is full")
        
        # Check if participant is already in meeting
        existing = session.query(MeetingParticipant).filter(
            MeetingParticipant.meeting_id == meeting.id,
            MeetingParticipant.user_id == join_request.user_id,
            MeetingParticipant.agent_id == join_request.agent_id
        ).first()
        
        if existing:
            existing.is_present = True
            existing.joined_at = datetime.utcnow()
        else:
            participant = MeetingParticipant(
                meeting_id=meeting.id,
                participant_type="user" if join_request.user_id else "agent",
                user_id=join_request.user_id,
                agent_id=join_request.agent_id,
                role=join_request.role,
                joined_at=datetime.utcnow(),
                is_present=True
            )
            session.add(participant)
        
        # Update meeting status if first participant
        if meeting.status == "scheduled":
            meeting.status = "active"
            meeting.actual_start = datetime.utcnow()
        
        session.commit()
        
        return {
            "status": "joined",
            "meeting_id": meeting_id,
            "room_id": meeting.meeting_room_id,
            "participant_role": join_request.role,
            "websocket_url": f"/ws/meetings/{meeting_id}"
        }
    finally:
        session.close()

@router.get("/{meeting_id}/details")
async def get_meeting_details(meeting_id: str):
    """Get detailed meeting information"""
    session = get_session()
    try:
        meeting = session.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        participants = session.query(MeetingParticipant).filter(
            MeetingParticipant.meeting_id == meeting.id
        ).all()
        
        return {
            "meeting_id": meeting_id,
            "title": meeting.title,
            "description": meeting.description,
            "meeting_type": meeting.meeting_type,
            "status": meeting.status,
            "scheduled_start": meeting.scheduled_start,
            "scheduled_end": meeting.scheduled_end,
            "actual_start": meeting.actual_start,
            "room_id": meeting.meeting_room_id,
            "agenda": meeting.agenda,
            "objectives": meeting.objectives,
            "conclusions": meeting.conclusions,
            "priority_level": meeting.priority_level,
            "participants": [
                {
                    "type": p.participant_type,
                    "user_id": p.user_id,
                    "agent_id": p.agent_id,
                    "role": p.role,
                    "is_present": p.is_present,
                    "joined_at": p.joined_at,
                    "contribution_score": p.contribution_score
                }
                for p in participants
            ],
            "department": meeting.department.name if meeting.department else "Cross-department"
        }
    finally:
        session.close()

# CMP Discussion Routes
@router.post("/{meeting_id}/cmp/ask")
async def ask_cmp_question(meeting_id: str, message: CMPMessage):
    """Ask a question in CMP discussion"""
    session = get_session()
    try:
        meeting = session.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
        if not meeting or meeting.meeting_type != MeetingType.CMP_DISCUSSION:
            raise HTTPException(status_code=404, detail="CMP meeting not found")
        
        # Generate responses from AI agents
        responses = await generate_cmp_responses(message.content)
        
        # Broadcast question and responses to meeting participants
        await manager.broadcast_to_meeting(meeting_id, {
            "type": "cmp_question",
            "question": message.content,
            "timestamp": datetime.utcnow().isoformat(),
            "responses": [
                {
                    "agent": resp.agent_name,
                    "content": resp.content,
                    "confidence": resp.confidence,
                    "reasoning": resp.reasoning
                }
                for resp in responses
            ]
        })
        
        return {
            "status": "question_processed",
            "question": message.content,
            "responses": responses,
            "meeting_id": meeting_id
        }
    finally:
        session.close()

@router.post("/{meeting_id}/conclude")
async def conclude_meeting(meeting_id: str, conclusions: List[str]):
    """Conclude a meeting and extract knowledge"""
    session = get_session()
    try:
        meeting = session.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        meeting.status = "completed"
        meeting.actual_end = datetime.utcnow()
        meeting.conclusions = conclusions
        
        # Mark all participants as no longer present
        participants = session.query(MeetingParticipant).filter(
            MeetingParticipant.meeting_id == meeting.id
        ).all()
        for participant in participants:
            if participant.is_present:
                participant.is_present = False
                participant.left_at = datetime.utcnow()
        
        session.commit()
        
        # Extract knowledge in background
        await extract_meeting_knowledge(meeting_id, session)
        
        # Notify participants
        await manager.broadcast_to_meeting(meeting_id, {
            "type": "meeting_concluded",
            "conclusions": conclusions,
            "timestamp": datetime.utcnow().isoformat(),
            "meeting_id": meeting_id
        })
        
        return {
            "status": "concluded",
            "meeting_id": meeting_id,
            "conclusions": conclusions,
            "duration_minutes": (meeting.actual_end - meeting.actual_start).total_seconds() / 60,
            "knowledge_extracted": True
        }
    finally:
        session.close()

@router.get("/schedule")
async def get_meeting_schedule(days_ahead: int = 7):
    """Get meeting schedule"""
    session = get_session()
    try:
        end_date = datetime.utcnow() + timedelta(days=days_ahead)
        
        meetings = session.query(Meeting).filter(
            Meeting.scheduled_start >= datetime.utcnow(),
            Meeting.scheduled_start <= end_date
        ).order_by(Meeting.scheduled_start).all()
        
        return {
            "schedule": [
                {
                    "meeting_id": meeting.meeting_id,
                    "title": meeting.title,
                    "meeting_type": meeting.meeting_type,
                    "scheduled_start": meeting.scheduled_start,
                    "scheduled_end": meeting.scheduled_end,
                    "status": meeting.status,
                    "department": meeting.department.name if meeting.department else "Cross-department",
                    "participant_count": len(meeting.participants),
                    "is_public": meeting.is_public
                }
                for meeting in meetings
            ]
        }
    finally:
        session.close()

@router.get("/knowledge/extract/{meeting_id}")
async def get_meeting_knowledge(meeting_id: str):
    """Get extracted knowledge from a meeting"""
    session = get_session()
    try:
        meeting = session.query(Meeting).filter(Meeting.meeting_id == meeting_id).first()
        if not meeting:
            raise HTTPException(status_code=404, detail="Meeting not found")
        
        knowledge_entries = session.query(KnowledgeBase).filter(
            KnowledgeBase.source_meeting_id == meeting.id
        ).all()
        
        return {
            "meeting_id": meeting_id,
            "meeting_title": meeting.title,
            "knowledge_entries": [
                {
                    "knowledge_id": entry.knowledge_id,
                    "title": entry.title,
                    "content": entry.content,
                    "knowledge_type": entry.knowledge_type,
                    "confidence_score": entry.confidence_score,
                    "tags": entry.tags,
                    "created_at": entry.created_at
                }
                for entry in knowledge_entries
            ]
        }
    finally:
        session.close()

# WebSocket endpoint for real-time meeting communication
@router.websocket("/ws/{meeting_id}")
async def websocket_meeting(websocket: WebSocket, meeting_id: str):
    """WebSocket endpoint for real-time meeting communication"""
    await manager.connect(websocket, meeting_id, {
        "type": "user",  # Would be determined from auth
        "name": "User",  # Would be from user profile
        "joined_at": datetime.utcnow().isoformat()
    })
    
    try:
        while True:
            # Receive message from client
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Process different message types
            if message_data.get("type") == "chat_message":
                # Broadcast chat message to all participants
                await manager.broadcast_to_meeting(meeting_id, {
                    "type": "chat_message",
                    "sender": message_data.get("sender"),
                    "content": message_data.get("content"),
                    "timestamp": datetime.utcnow().isoformat()
                })
            
            elif message_data.get("type") == "cmp_question":
                # Handle CMP question and generate AI responses
                question = message_data.get("content")
                responses = await generate_cmp_responses(question)
                
                await manager.broadcast_to_meeting(meeting_id, {
                    "type": "cmp_responses",
                    "question": question,
                    "responses": [
                        {
                            "agent": resp.agent_name,
                            "content": resp.content,
                            "confidence": resp.confidence
                        }
                        for resp in responses
                    ],
                    "timestamp": datetime.utcnow().isoformat()
                })
            
    except WebSocketDisconnect:
        manager.disconnect(websocket, meeting_id) 