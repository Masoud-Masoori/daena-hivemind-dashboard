"""
Daena AI VP Router - Executive AI Assistant Routes
Comprehensive chat, file management, monitoring, and coordination features
"""

from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import StreamingResponse, FileResponse
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import json
import os
import aiofiles
from pathlib import Path

# Import database models
from models.database import get_session, Agent, Conversation, Message, FileStorage, DaenaActivity, Schedule, KnowledgeBase

router = APIRouter(prefix="/api/v1/daena", tags=["Daena AI VP"])

# Pydantic models
class ChatMessage(BaseModel):
    content: str
    message_type: str = "text"
    attachments: Optional[List[str]] = None

class ChatResponse(BaseModel):
    message_id: str
    content: str
    message_type: str
    timestamp: datetime
    attachments: Optional[List[Dict]] = None

class ConversationCreate(BaseModel):
    title: Optional[str] = None
    context: Optional[Dict] = None

class DaenaStatus(BaseModel):
    status: str
    current_projects: List[Dict]
    priorities: List[Dict]
    performance_metrics: Dict
    active_conversations: int
    recent_activities: List[Dict]

class MeetingRequest(BaseModel):
    title: str
    description: Optional[str] = None
    participants: List[str]
    scheduled_time: datetime
    duration_minutes: int = 60
    meeting_type: str = "general"

class FileMetadata(BaseModel):
    filename: str
    description: Optional[str] = None
    tags: Optional[List[str]] = None
    is_public: bool = False

# Helper functions
def get_daena_agent(session):
    """Get the Daena AI VP agent"""
    return session.query(Agent).filter(Agent.agent_type == "daena").first()

def generate_ai_response(message: str, context: Dict = None) -> str:
    """Generate AI response (placeholder - integrate with your LLM)"""
    # This would integrate with your actual LLM
    responses = [
        f"As your AI VP, I understand you're asking about: {message[:50]}... Let me analyze this and provide strategic insights.",
        f"Based on my monitoring of all departments, here's my assessment of: {message[:50]}...",
        f"I've been tracking this across our systems. Here's what I recommend regarding: {message[:50]}...",
        f"From an executive perspective, considering our current priorities: {message[:50]}..."
    ]
    return responses[hash(message) % len(responses)]

# Chat and Conversation Routes
@router.post("/chat/start", response_model=Dict)
async def start_conversation(
    conversation_data: ConversationCreate,
    user_id: Optional[int] = None
):
    """Start a new conversation with Daena"""
    session = get_session()
    try:
        daena = get_daena_agent(session)
        if not daena:
            raise HTTPException(status_code=404, detail="Daena AI VP not found")
        
        conversation_id = str(uuid.uuid4())
        conversation = Conversation(
            conversation_id=conversation_id,
            user_id=user_id,
            agent_id=daena.id,
            title=conversation_data.title or f"Chat with Daena - {datetime.now().strftime('%Y-%m-%d %H:%M')}",
            conversation_type="chat",
            context=conversation_data.context or {}
        )
        session.add(conversation)
        session.commit()
        
        # Add welcome message
        welcome_message = Message(
            conversation_id=conversation.id,
            sender_type="agent",
            sender_id=str(daena.id),
            content="Hello! I'm Daena, your AI Vice President. I'm here to help you with strategic decisions, monitor our operations, manage projects, and coordinate across all departments. How can I assist you today?",
            message_type="text",
            metadata={"welcome": True}
        )
        session.add(welcome_message)
        session.commit()
        
        return {
            "conversation_id": conversation_id,
            "status": "started",
            "daena_status": "ready",
            "welcome_message": welcome_message.content
        }
    finally:
        session.close()

@router.post("/chat/{conversation_id}/message", response_model=ChatResponse)
async def send_message(
    conversation_id: str,
    message: ChatMessage,
    user_id: Optional[int] = None
):
    """Send a message to Daena"""
    session = get_session()
    try:
        conversation = session.query(Conversation).filter(
            Conversation.conversation_id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        # Save user message
        user_message = Message(
            conversation_id=conversation.id,
            sender_type="user",
            sender_id=str(user_id) if user_id else "anonymous",
            content=message.content,
            message_type=message.message_type,
            attachments=message.attachments
        )
        session.add(user_message)
        
        # Generate Daena's response
        ai_response = generate_ai_response(message.content, conversation.context)
        
        response_message = Message(
            conversation_id=conversation.id,
            sender_type="agent",
            sender_id=str(conversation.agent_id),
            content=ai_response,
            message_type="text",
            metadata={"response_to": user_message.id}
        )
        session.add(response_message)
        
        # Update conversation
        conversation.updated_at = datetime.utcnow()
        session.commit()
        
        return ChatResponse(
            message_id=str(response_message.id),
            content=ai_response,
            message_type="text",
            timestamp=response_message.timestamp
        )
    finally:
        session.close()

@router.get("/chat/{conversation_id}/history")
async def get_conversation_history(conversation_id: str):
    """Get conversation history"""
    session = get_session()
    try:
        conversation = session.query(Conversation).filter(
            Conversation.conversation_id == conversation_id
        ).first()
        
        if not conversation:
            raise HTTPException(status_code=404, detail="Conversation not found")
        
        messages = session.query(Message).filter(
            Message.conversation_id == conversation.id
        ).order_by(Message.timestamp).all()
        
        return {
            "conversation_id": conversation_id,
            "title": conversation.title,
            "messages": [
                {
                    "id": msg.id,
                    "sender_type": msg.sender_type,
                    "sender_id": msg.sender_id,
                    "content": msg.content,
                    "message_type": msg.message_type,
                    "timestamp": msg.timestamp,
                    "attachments": msg.attachments
                }
                for msg in messages
            ]
        }
    finally:
        session.close()

# Status and Monitoring Routes
@router.get("/status", response_model=DaenaStatus)
async def get_daena_status():
    """Get Daena's current status and activities"""
    session = get_session()
    try:
        daena = get_daena_agent(session)
        if not daena:
            raise HTTPException(status_code=404, detail="Daena AI VP not found")
        
        # Get active conversations count
        active_conversations = session.query(Conversation).filter(
            Conversation.agent_id == daena.id,
            Conversation.is_active == True
        ).count()
        
        # Get recent activities
        recent_activities = session.query(DaenaActivity).filter(
            DaenaActivity.created_at >= datetime.utcnow() - timedelta(hours=24)
        ).order_by(DaenaActivity.created_at.desc()).limit(10).all()
        
        return DaenaStatus(
            status=daena.status,
            current_projects=daena.current_projects,
            priorities=daena.priorities,
            performance_metrics=daena.performance_metrics,
            active_conversations=active_conversations,
            recent_activities=[
                {
                    "id": activity.activity_id,
                    "type": activity.activity_type,
                    "description": activity.description,
                    "timestamp": activity.created_at,
                    "status": activity.status
                }
                for activity in recent_activities
            ]
        )
    finally:
        session.close()

@router.get("/dashboard")
async def get_executive_dashboard():
    """Get comprehensive executive dashboard data"""
    session = get_session()
    try:
        daena = get_daena_agent(session)
        
        # Get all departments performance
        from models.database import Department
        departments = session.query(Department).all()
        
        # Get recent meetings
        from models.database import Meeting
        recent_meetings = session.query(Meeting).filter(
            Meeting.created_at >= datetime.utcnow() - timedelta(days=7)
        ).order_by(Meeting.created_at.desc()).limit(5).all()
        
        # Get knowledge base insights
        recent_knowledge = session.query(KnowledgeBase).order_by(
            KnowledgeBase.created_at.desc()
        ).limit(10).all()
        
        return {
            "daena_info": {
                "name": daena.name,
                "status": daena.status,
                "current_projects": daena.current_projects,
                "priorities": daena.priorities,
                "performance_metrics": daena.performance_metrics
            },
            "departments": [
                {
                    "id": dept.id,
                    "name": dept.name,
                    "color": dept.color,
                    "performance_metrics": dept.performance_metrics,
                    "active_projects": dept.active_projects
                }
                for dept in departments
            ],
            "recent_meetings": [
                {
                    "id": meeting.meeting_id,
                    "title": meeting.title,
                    "status": meeting.status,
                    "scheduled_start": meeting.scheduled_start,
                    "department": meeting.department.name if meeting.department else "Cross-department"
                }
                for meeting in recent_meetings
            ],
            "knowledge_insights": [
                {
                    "id": knowledge.knowledge_id,
                    "title": knowledge.title,
                    "type": knowledge.knowledge_type,
                    "priority": knowledge.priority_level,
                    "created_at": knowledge.created_at
                }
                for knowledge in recent_knowledge
            ]
        }
    finally:
        session.close()

# File Management Routes
@router.post("/files/upload")
async def upload_file(
    file: UploadFile = File(...),
    description: str = Form(None),
    tags: str = Form(None),
    is_public: bool = Form(False),
    user_id: Optional[int] = None
):
    """Upload a file through Daena"""
    session = get_session()
    try:
        # Create uploads directory if it doesn't exist
        upload_dir = Path("uploads/daena")
        upload_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate unique filename
        file_id = str(uuid.uuid4())
        file_extension = Path(file.filename).suffix
        filename = f"{file_id}{file_extension}"
        file_path = upload_dir / filename
        
        # Save file
        async with aiofiles.open(file_path, 'wb') as f:
            content = await file.read()
            await f.write(content)
        
        # Parse tags
        tag_list = tags.split(',') if tags else []
        tag_list = [tag.strip() for tag in tag_list if tag.strip()]
        
        # Save to database
        file_record = FileStorage(
            file_id=file_id,
            filename=filename,
            original_filename=file.filename,
            file_path=str(file_path),
            file_size=len(content),
            file_type=file.content_type,
            file_category="document",  # Could be determined by file type
            uploader_id=user_id,
            description=description,
            tags=tag_list,
            is_public=is_public,
            metadata={"uploaded_via": "daena_vp"}
        )
        session.add(file_record)
        session.commit()
        
        return {
            "file_id": file_id,
            "filename": file.filename,
            "size": len(content),
            "type": file.content_type,
            "status": "uploaded",
            "message": "File uploaded successfully through Daena VP system"
        }
    finally:
        session.close()

@router.get("/files")
async def list_files(user_id: Optional[int] = None):
    """List files accessible through Daena"""
    session = get_session()
    try:
        query = session.query(FileStorage)
        if user_id:
            query = query.filter(
                (FileStorage.uploader_id == user_id) | (FileStorage.is_public == True)
            )
        else:
            query = query.filter(FileStorage.is_public == True)
        
        files = query.order_by(FileStorage.created_at.desc()).all()
        
        return {
            "files": [
                {
                    "file_id": file.file_id,
                    "filename": file.original_filename,
                    "size": file.file_size,
                    "type": file.file_type,
                    "description": file.description,
                    "tags": file.tags,
                    "download_count": file.download_count,
                    "created_at": file.created_at,
                    "is_public": file.is_public
                }
                for file in files
            ]
        }
    finally:
        session.close()

@router.get("/files/{file_id}/download")
async def download_file(file_id: str):
    """Download a file through Daena"""
    session = get_session()
    try:
        file_record = session.query(FileStorage).filter(
            FileStorage.file_id == file_id
        ).first()
        
        if not file_record:
            raise HTTPException(status_code=404, detail="File not found")
        
        # Increment download count
        file_record.download_count += 1
        session.commit()
        
        return FileResponse(
            path=file_record.file_path,
            filename=file_record.original_filename,
            media_type=file_record.file_type
        )
    finally:
        session.close()

# Scheduling Routes
@router.post("/schedule/meeting")
async def schedule_meeting(meeting_request: MeetingRequest):
    """Schedule a meeting through Daena"""
    session = get_session()
    try:
        schedule_id = str(uuid.uuid4())
        
        schedule = Schedule(
            schedule_id=schedule_id,
            event_type="meeting",
            title=meeting_request.title,
            description=meeting_request.description,
            scheduled_time=meeting_request.scheduled_time,
            duration_minutes=meeting_request.duration_minutes,
            participants=meeting_request.participants,
            priority=3,  # Default priority
            created_by="daena",
            metadata={
                "meeting_type": meeting_request.meeting_type,
                "created_via": "daena_vp"
            }
        )
        session.add(schedule)
        session.commit()
        
        return {
            "schedule_id": schedule_id,
            "status": "scheduled",
            "message": f"Meeting '{meeting_request.title}' scheduled successfully",
            "scheduled_time": meeting_request.scheduled_time,
            "participants": meeting_request.participants
        }
    finally:
        session.close()

@router.get("/schedule")
async def get_schedule(days_ahead: int = 7):
    """Get Daena's schedule and upcoming events"""
    session = get_session()
    try:
        end_date = datetime.utcnow() + timedelta(days=days_ahead)
        
        events = session.query(Schedule).filter(
            Schedule.scheduled_time >= datetime.utcnow(),
            Schedule.scheduled_time <= end_date,
            Schedule.status.in_(["scheduled", "in_progress"])
        ).order_by(Schedule.scheduled_time).all()
        
        return {
            "schedule": [
                {
                    "schedule_id": event.schedule_id,
                    "event_type": event.event_type,
                    "title": event.title,
                    "description": event.description,
                    "scheduled_time": event.scheduled_time,
                    "duration_minutes": event.duration_minutes,
                    "participants": event.participants,
                    "priority": event.priority,
                    "status": event.status
                }
                for event in events
            ]
        }
    finally:
        session.close()

# Knowledge Base Routes
@router.get("/knowledge/search")
async def search_knowledge(query: str, limit: int = 10):
    """Search Daena's knowledge base"""
    session = get_session()
    try:
        # Simple text search (in production, use proper full-text search)
        knowledge_entries = session.query(KnowledgeBase).filter(
            KnowledgeBase.content.contains(query) | 
            KnowledgeBase.title.contains(query)
        ).order_by(KnowledgeBase.confidence_score.desc()).limit(limit).all()
        
        return {
            "query": query,
            "results": [
                {
                    "knowledge_id": entry.knowledge_id,
                    "title": entry.title,
                    "content": entry.content[:200] + "..." if len(entry.content) > 200 else entry.content,
                    "type": entry.knowledge_type,
                    "confidence_score": entry.confidence_score,
                    "tags": entry.tags,
                    "created_at": entry.created_at
                }
                for entry in knowledge_entries
            ]
        }
    finally:
        session.close()

@router.post("/activity/log")
async def log_activity(
    activity_type: str,
    description: str,
    department: Optional[str] = None,
    priority: int = 3
):
    """Log a Daena activity"""
    session = get_session()
    try:
        activity = DaenaActivity(
            activity_id=str(uuid.uuid4()),
            activity_type=activity_type,
            description=description,
            department_involved=department,
            priority_level=priority,
            status="in_progress"
        )
        session.add(activity)
        session.commit()
        
        return {
            "activity_id": activity.activity_id,
            "status": "logged",
            "message": "Activity logged successfully"
        }
    finally:
        session.close()

# WebSocket for real-time communication (placeholder)
# This would be implemented with FastAPI WebSocket support
@router.get("/ws/info")
async def websocket_info():
    """Information about WebSocket endpoints"""
    return {
        "websocket_url": "/ws/daena",
        "features": [
            "Real-time chat",
            "Live status updates", 
            "Meeting notifications",
            "File upload progress",
            "System alerts"
        ],
        "message": "WebSocket endpoints will be implemented for real-time features"
    } 