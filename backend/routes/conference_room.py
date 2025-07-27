"""
Conference Room API for Daena AI VP System
Handles real-time conference discussions, issue tracking, and participant management
"""

from fastapi import APIRouter, HTTPException, Depends, Request, WebSocket, WebSocketDisconnect
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from fastapi.templating import Jinja2Templates
from typing import List, Dict, Any, Optional
from datetime import datetime
import os
import logging
import json
import uuid
from pydantic import BaseModel

from backend.services.auth_service import auth_service, User
from backend.services.council_service import council_service
from backend.services.websocket_service import websocket_manager

router = APIRouter(prefix="/api/v1/conference-room", tags=["conference-room"])
security = HTTPBearer()

logger = logging.getLogger(__name__)
templates = Jinja2Templates(directory=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "frontend", "templates"))

# Conference Models
class ConferenceParticipant(BaseModel):
    id: str
    name: str
    role: str  # "user", "ai", "councilor", "founder", "system"
    status: str  # "online", "offline", "speaking", "listening"
    avatar: Optional[str] = None

class ConferenceMessage(BaseModel):
    id: str
    sender: str
    content: str
    timestamp: datetime
    message_type: str  # "user", "ai", "councilor", "system"
    issues: List[str] = []
    metadata: Dict[str, Any] = {}

class ConferenceIssue(BaseModel):
    id: str
    title: str
    description: str
    status: str  # "open", "discussing", "resolved", "deferred"
    priority: str  # "low", "medium", "high", "critical"
    created_by: str
    created_at: datetime
    resolved_at: Optional[datetime] = None
    tags: List[str] = []

class Conference(BaseModel):
    id: str
    title: str
    focus_area: str
    participants: List[ConferenceParticipant]
    messages: List[ConferenceMessage]
    issues: List[ConferenceIssue]
    status: str  # "setup", "active", "paused", "ended"
    created_at: datetime
    started_at: Optional[datetime] = None
    ended_at: Optional[datetime] = None
    metadata: Dict[str, Any] = {}

# In-memory conference storage (replace with database in production)
ACTIVE_CONFERENCES: Dict[str, Conference] = {}
CONFERENCE_WEBSOCKETS: Dict[str, List[WebSocket]] = {}

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> User:
    """Get current authenticated user"""
    return auth_service.get_current_user(credentials)

@router.get("/")
async def get_conference_room_page(request: Request):
    """Get the conference room dashboard page"""
    return templates.TemplateResponse("conference_room.html", {"request": request})

@router.post("/conferences")
async def create_conference(conference_data: Dict[str, Any], user: User = Depends(get_current_user)):
    """Create a new conference"""
    conference_id = str(uuid.uuid4())
    
    # Create default participants
    participants = [
        ConferenceParticipant(
            id=str(uuid.uuid4()),
            name=user.username,
            role="user",
            status="online"
        ),
        ConferenceParticipant(
            id=str(uuid.uuid4()),
            name="Daena AI VP",
            role="ai",
            status="online"
        )
    ]
    
    # Add councilors if requested
    if conference_data.get("include_councilors", True):
        councilors = [
            ("Steve Jobs", "councilor"),
            ("Satya Nadella", "councilor"),
            ("Sheryl Sandberg", "councilor")
        ]
        for name, role in councilors:
            participants.append(ConferenceParticipant(
                id=str(uuid.uuid4()),
                name=name,
                role=role,
                status="online"
            ))
    
    conference = Conference(
        id=conference_id,
        title=conference_data.get("title", "New Conference"),
        focus_area=conference_data.get("focus_area", "general"),
        participants=participants,
        messages=[],
        issues=[],
        status="setup",
        created_at=datetime.now(),
        metadata=conference_data.get("metadata", {})
    )
    
    ACTIVE_CONFERENCES[conference_id] = conference
    CONFERENCE_WEBSOCKETS[conference_id] = []
    
    logger.info(f"Conference created: {conference_id} by {user.username}")
    
    return {
        "success": True,
        "conference": conference.dict(),
        "message": "Conference created successfully"
    }

@router.get("/conferences/{conference_id}")
async def get_conference(conference_id: str, user: User = Depends(get_current_user)):
    """Get conference details"""
    if conference_id not in ACTIVE_CONFERENCES:
        raise HTTPException(status_code=404, detail="Conference not found")
    
    conference = ACTIVE_CONFERENCES[conference_id]
    return {
        "success": True,
        "conference": conference.dict()
    }

@router.post("/conferences/{conference_id}/start")
async def start_conference(conference_id: str, user: User = Depends(get_current_user)):
    """Start a conference"""
    if conference_id not in ACTIVE_CONFERENCES:
        raise HTTPException(status_code=404, detail="Conference not found")
    
    conference = ACTIVE_CONFERENCES[conference_id]
    conference.status = "active"
    conference.started_at = datetime.now()
    
    # Add system message
    system_message = ConferenceMessage(
        id=str(uuid.uuid4()),
        sender="System",
        content=f"Conference '{conference.title}' started. Focus: {conference.focus_area}",
        timestamp=datetime.now(),
        message_type="system"
    )
    conference.messages.append(system_message)
    
    # Notify all connected clients
    await broadcast_to_conference(conference_id, {
        "type": "conference_started",
        "conference": conference.dict()
    })
    
    return {
        "success": True,
        "message": "Conference started successfully"
    }

@router.post("/conferences/{conference_id}/messages")
async def send_message(
    conference_id: str, 
    message_data: Dict[str, Any], 
    user: User = Depends(get_current_user)
):
    """Send a message to the conference"""
    if conference_id not in ACTIVE_CONFERENCES:
        raise HTTPException(status_code=404, detail="Conference not found")
    
    conference = ACTIVE_CONFERENCES[conference_id]
    
    # Create user message
    user_message = ConferenceMessage(
        id=str(uuid.uuid4()),
        sender=user.username,
        content=message_data.get("content", ""),
        timestamp=datetime.now(),
        message_type="user"
    )
    conference.messages.append(user_message)
    
    # Generate AI response if needed
    ai_response = await generate_ai_response(conference, user_message)
    if ai_response:
        conference.messages.append(ai_response)
        
        # Track issues if found
        if ai_response.issues:
            for issue in ai_response.issues:
                await track_issue(conference_id, issue, "ai")
    
    # Broadcast to all participants
    await broadcast_to_conference(conference_id, {
        "type": "new_messages",
        "messages": [user_message.dict(), ai_response.dict() if ai_response else None]
    })
    
    return {
        "success": True,
        "message": "Message sent successfully"
    }

@router.post("/conferences/{conference_id}/issues")
async def track_issue(
    conference_id: str, 
    issue_data: Dict[str, Any], 
    user: User = Depends(get_current_user)
):
    """Track an issue in the conference"""
    if conference_id not in ACTIVE_CONFERENCES:
        raise HTTPException(status_code=404, detail="Conference not found")
    
    conference = ACTIVE_CONFERENCES[conference_id]
    
    issue = ConferenceIssue(
        id=str(uuid.uuid4()),
        title=issue_data.get("title", "New Issue"),
        description=issue_data.get("description", ""),
        status="open",
        priority=issue_data.get("priority", "medium"),
        created_by=user.username,
        created_at=datetime.now(),
        tags=issue_data.get("tags", [])
    )
    
    conference.issues.append(issue)
    
    # Add system message about the issue
    system_message = ConferenceMessage(
        id=str(uuid.uuid4()),
        sender="System",
        content=f"Issue tracked: {issue.title}",
        timestamp=datetime.now(),
        message_type="system"
    )
    conference.messages.append(system_message)
    
    # Broadcast to all participants
    await broadcast_to_conference(conference_id, {
        "type": "issue_tracked",
        "issue": issue.dict()
    })
    
    return {
        "success": True,
        "issue": issue.dict()
    }

@router.put("/conferences/{conference_id}/issues/{issue_id}")
async def update_issue(
    conference_id: str,
    issue_id: str,
    update_data: Dict[str, Any],
    user: User = Depends(get_current_user)
):
    """Update an issue status"""
    if conference_id not in ACTIVE_CONFERENCES:
        raise HTTPException(status_code=404, detail="Conference not found")
    
    conference = ACTIVE_CONFERENCES[conference_id]
    issue = next((i for i in conference.issues if i.id == issue_id), None)
    
    if not issue:
        raise HTTPException(status_code=404, detail="Issue not found")
    
    # Update issue
    if "status" in update_data:
        issue.status = update_data["status"]
        if issue.status == "resolved":
            issue.resolved_at = datetime.now()
    
    if "priority" in update_data:
        issue.priority = update_data["priority"]
    
    # Broadcast update
    await broadcast_to_conference(conference_id, {
        "type": "issue_updated",
        "issue": issue.dict()
    })
    
    return {
        "success": True,
        "issue": issue.dict()
    }

@router.post("/conferences/{conference_id}/consult-council")
async def consult_council(
    conference_id: str,
    consultation_data: Dict[str, Any],
    user: User = Depends(get_current_user)
):
    """Consult the expert council during conference"""
    if conference_id not in ACTIVE_CONFERENCES:
        raise HTTPException(status_code=404, detail="Conference not found")
    
    conference = ACTIVE_CONFERENCES[conference_id]
    
    # Get councilors from the conference
    councilors = [p for p in conference.participants if p.role == "councilor"]
    
    if not councilors:
        raise HTTPException(status_code=400, detail="No councilors available")
    
    # Generate councilor responses
    responses = []
    for councilor in councilors:
        response = await generate_councilor_response(councilor, consultation_data.get("topic", ""))
        responses.append(response)
    
    # Add responses to conference
    for response in responses:
        conference.messages.append(response)
    
    # Broadcast responses
    await broadcast_to_conference(conference_id, {
        "type": "council_consultation",
        "responses": [r.dict() for r in responses]
    })
    
    return {
        "success": True,
        "responses": [r.dict() for r in responses]
    }

@router.post("/conferences/{conference_id}/end")
async def end_conference(conference_id: str, user: User = Depends(get_current_user)):
    """End a conference"""
    if conference_id not in ACTIVE_CONFERENCES:
        raise HTTPException(status_code=404, detail="Conference not found")
    
    conference = ACTIVE_CONFERENCES[conference_id]
    conference.status = "ended"
    conference.ended_at = datetime.now()
    
    # Add system message
    system_message = ConferenceMessage(
        id=str(uuid.uuid4()),
        sender="System",
        content=f"Conference '{conference.title}' ended. {len(conference.issues)} issues tracked, {len(conference.messages)} messages exchanged.",
        timestamp=datetime.now(),
        message_type="system"
    )
    conference.messages.append(system_message)
    
    # Save conference data
    await save_conference_data(conference)
    
    # Close all WebSocket connections
    if conference_id in CONFERENCE_WEBSOCKETS:
        for websocket in CONFERENCE_WEBSOCKETS[conference_id]:
            try:
                await websocket.close()
            except:
                pass
        del CONFERENCE_WEBSOCKETS[conference_id]
    
    return {
        "success": True,
        "message": "Conference ended successfully",
        "summary": {
            "total_messages": len(conference.messages),
            "total_issues": len(conference.issues),
            "duration_minutes": (conference.ended_at - conference.started_at).total_seconds() / 60 if conference.started_at else 0
        }
    }

@router.websocket("/ws/{conference_id}")
async def conference_websocket(websocket: WebSocket, conference_id: str):
    """WebSocket endpoint for real-time conference communication"""
    await websocket.accept()
    
    if conference_id not in CONFERENCE_WEBSOCKETS:
        CONFERENCE_WEBSOCKETS[conference_id] = []
    
    CONFERENCE_WEBSOCKETS[conference_id].append(websocket)
    
    try:
        while True:
            data = await websocket.receive_text()
            message_data = json.loads(data)
            
            # Handle different message types
            if message_data.get("type") == "join":
                await handle_join_message(conference_id, websocket, message_data)
            elif message_data.get("type") == "message":
                await handle_chat_message(conference_id, message_data)
            elif message_data.get("type") == "issue":
                await handle_issue_message(conference_id, message_data)
            
    except WebSocketDisconnect:
        CONFERENCE_WEBSOCKETS[conference_id].remove(websocket)
        logger.info(f"Client disconnected from conference {conference_id}")

async def generate_ai_response(conference: Conference, user_message: ConferenceMessage) -> Optional[ConferenceMessage]:
    """Generate AI response using Daena's capabilities"""
    try:
        # Use council service to generate response
        response_content = await council_service.llm.generate(
            f"Conference context: {conference.focus_area}. User message: {user_message.content}. Provide a helpful, focused response.",
            persona="Strategic Advisor"
        )
        
        # Analyze for issues
        issues = []
        if any(word in user_message.content.lower() for word in ["problem", "issue", "concern", "risk"]):
            issues.append("Problem identification")
        
        return ConferenceMessage(
            id=str(uuid.uuid4()),
            sender="Daena AI VP",
            content=response_content,
            timestamp=datetime.now(),
            message_type="ai",
            issues=issues
        )
    except Exception as e:
        logger.error(f"Error generating AI response: {e}")
        return None

async def generate_councilor_response(councilor: ConferenceParticipant, topic: str) -> ConferenceMessage:
    """Generate response from a specific councilor"""
    try:
        response_content = await council_service.llm.generate(
            f"Topic: {topic}. Respond as {councilor.name} with their unique perspective and expertise.",
            persona=councilor.name
        )
        
        return ConferenceMessage(
            id=str(uuid.uuid4()),
            sender=councilor.name,
            content=response_content,
            timestamp=datetime.now(),
            message_type="councilor"
        )
    except Exception as e:
        logger.error(f"Error generating councilor response: {e}")
        return ConferenceMessage(
            id=str(uuid.uuid4()),
            sender=councilor.name,
            content=f"As {councilor.name}, I believe we should focus on the core objectives.",
            timestamp=datetime.now(),
            message_type="councilor"
        )

async def broadcast_to_conference(conference_id: str, message: Dict[str, Any]):
    """Broadcast message to all participants in a conference"""
    if conference_id in CONFERENCE_WEBSOCKETS:
        for websocket in CONFERENCE_WEBSOCKETS[conference_id]:
            try:
                await websocket.send_text(json.dumps(message))
            except:
                # Remove disconnected websocket
                CONFERENCE_WEBSOCKETS[conference_id].remove(websocket)

async def handle_join_message(conference_id: str, websocket: WebSocket, message_data: Dict[str, Any]):
    """Handle participant join message"""
    if conference_id in ACTIVE_CONFERENCES:
        conference = ACTIVE_CONFERENCES[conference_id]
        await websocket.send_text(json.dumps({
            "type": "conference_data",
            "conference": conference.dict()
        }))

async def handle_chat_message(conference_id: str, message_data: Dict[str, Any]):
    """Handle chat message from WebSocket"""
    # This would integrate with the REST API message endpoint
    pass

async def handle_issue_message(conference_id: str, message_data: Dict[str, Any]):
    """Handle issue tracking message from WebSocket"""
    # This would integrate with the REST API issue endpoint
    pass

async def save_conference_data(conference: Conference):
    """Save conference data for later reference"""
    try:
        # Save to file system (replace with database in production)
        filename = f"conference_logs/{conference.id}_{conference.created_at.strftime('%Y%m%d_%H%M%S')}.json"
        os.makedirs("conference_logs", exist_ok=True)
        
        with open(filename, 'w') as f:
            json.dump(conference.dict(), f, default=str, indent=2)
        
        logger.info(f"Conference data saved: {filename}")
    except Exception as e:
        logger.error(f"Error saving conference data: {e}")

async def track_issue(conference_id: str, issue_title: str, created_by: str):
    """Track an issue in the conference"""
    if conference_id in ACTIVE_CONFERENCES:
        conference = ACTIVE_CONFERENCES[conference_id]
        
        issue = ConferenceIssue(
            id=str(uuid.uuid4()),
            title=issue_title,
            description=f"Issue identified during conference discussion",
            status="open",
            priority="medium",
            created_by=created_by,
            created_at=datetime.now()
        )
        
        conference.issues.append(issue) 