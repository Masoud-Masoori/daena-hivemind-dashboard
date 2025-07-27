from fastapi import APIRouter, HTTPException, UploadFile, File, Form, WebSocket, WebSocketDisconnect
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import json
import os
from datetime import datetime
import asyncio
import uuid
import hashlib
from pathlib import Path

router = APIRouter(prefix="/voice-agents", tags=["Voice Agent Communication"])

# Voice Agent Models
class VoiceAgent(BaseModel):
    id: str
    name: str
    department: str
    voice_profile: str  # "professional", "friendly", "authoritative", "calm", "energetic"
    voice_enabled: bool
    current_conversation: Optional[str]
    voice_status: str  # "idle", "speaking", "listening", "in_meeting", "muted"
    last_voice_activity: datetime
    web3_identity: Optional[str] = None
    voice_signature: Optional[str] = None

class VoiceConversation(BaseModel):
    id: str
    title: str
    participants: List[str]  # Agent IDs
    conversation_type: str  # "one_on_one", "group", "meeting", "consultation"
    start_time: datetime
    end_time: Optional[datetime]
    status: str  # "active", "paused", "ended", "archived"
    transcript: List[Dict[str, Any]]
    voice_recording_url: Optional[str]
    web3_transaction_hash: Optional[str] = None

class VoiceMessage(BaseModel):
    id: str
    conversation_id: str
    sender_id: str
    sender_name: str
    message_type: str  # "speech", "command", "llm_response", "system"
    content: str
    timestamp: datetime
    voice_duration: Optional[float]  # seconds
    confidence_score: Optional[float]
    web3_signature: Optional[str] = None

# Mock data for voice agents
mock_voice_agents = [
    VoiceAgent(
        id="daena-voice",
        name="Daena",
        department="executive",
        voice_profile="authoritative",
        voice_enabled=True,
        current_conversation=None,
        voice_status="idle",
        last_voice_activity=datetime.now(),
        web3_identity="0xdaena123456789abcdef"
    ),
    VoiceAgent(
        id="sunflower-voice",
        name="Sunflower",
        department="marketing",
        voice_profile="friendly",
        voice_enabled=True,
        current_conversation=None,
        voice_status="idle",
        last_voice_activity=datetime.now(),
        web3_identity="0xsunflower987654321fedcba"
    ),
    VoiceAgent(
        id="honeycomb-voice",
        name="Honeycomb",
        department="technology",
        voice_profile="professional",
        voice_enabled=True,
        current_conversation=None,
        voice_status="idle",
        last_voice_activity=datetime.now(),
        web3_identity="0xhoneycombabcdef123456"
    )
]

mock_conversations = [
    VoiceConversation(
        id="conv-001",
        title="Q4 Strategy Discussion",
        participants=["daena-voice", "sunflower-voice", "honeycomb-voice"],
        conversation_type="meeting",
        start_time=datetime.now(),
        end_time=None,
        status="active",
        transcript=[],
        voice_recording_url=None
    )
]

# WebSocket connections for real-time voice communication
voice_connections: Dict[str, WebSocket] = {}

@router.get("/agents")
async def get_voice_agents():
    """Get all voice-enabled agents"""
    return {
        "agents": mock_voice_agents,
        "total_agents": len(mock_voice_agents),
        "active_agents": len([a for a in mock_voice_agents if a.voice_status != "idle"])
    }

@router.get("/agents/{agent_id}")
async def get_voice_agent(agent_id: str):
    """Get a specific voice agent"""
    for agent in mock_voice_agents:
        if agent.id == agent_id:
            return agent
    raise HTTPException(status_code=404, detail="Voice agent not found")

@router.post("/agents/{agent_id}/voice-toggle")
async def toggle_voice_agent(agent_id: str, enabled: bool):
    """Toggle voice for an agent"""
    for agent in mock_voice_agents:
        if agent.id == agent_id:
            agent.voice_enabled = enabled
            agent.voice_status = "idle" if enabled else "muted"
            return {"message": f"Voice {'enabled' if enabled else 'disabled'} for {agent.name}", "agent": agent}
    raise HTTPException(status_code=404, detail="Voice agent not found")

@router.post("/agents/{agent_id}/voice-profile")
async def update_voice_profile(agent_id: str, profile: str):
    """Update voice profile for an agent"""
    valid_profiles = ["professional", "friendly", "authoritative", "calm", "energetic"]
    if profile not in valid_profiles:
        raise HTTPException(status_code=400, detail=f"Invalid profile. Must be one of: {valid_profiles}")
    
    for agent in mock_voice_agents:
        if agent.id == agent_id:
            agent.voice_profile = profile
            return {"message": f"Voice profile updated to {profile}", "agent": agent}
    raise HTTPException(status_code=404, detail="Voice agent not found")

@router.get("/conversations")
async def get_voice_conversations():
    """Get all voice conversations"""
    return {
        "conversations": mock_conversations,
        "total_conversations": len(mock_conversations),
        "active_conversations": len([c for c in mock_conversations if c.status == "active"])
    }

@router.post("/conversations")
async def create_voice_conversation(conversation: VoiceConversation):
    """Create a new voice conversation"""
    conversation.id = f"conv-{uuid.uuid4().hex[:8]}"
    conversation.start_time = datetime.now()
    conversation.status = "active"
    
    # Generate Web3 transaction hash
    conv_data = {
        "conversation_id": conversation.id,
        "participants": conversation.participants,
        "timestamp": conversation.start_time.isoformat()
    }
    conversation.web3_transaction_hash = hashlib.sha256(json.dumps(conv_data, sort_keys=True).encode()).hexdigest()
    
    mock_conversations.append(conversation)
    return {"message": "Voice conversation created", "conversation": conversation}

@router.get("/conversations/{conversation_id}")
async def get_voice_conversation(conversation_id: str):
    """Get a specific voice conversation"""
    for conversation in mock_conversations:
        if conversation.id == conversation_id:
            return conversation
    raise HTTPException(status_code=404, detail="Voice conversation not found")

@router.post("/conversations/{conversation_id}/join")
async def join_voice_conversation(conversation_id: str, agent_id: str):
    """Join a voice conversation"""
    for conversation in mock_conversations:
        if conversation.id == conversation_id:
            if agent_id not in conversation.participants:
                conversation.participants.append(agent_id)
            
            # Update agent status
            for agent in mock_voice_agents:
                if agent.id == agent_id:
                    agent.current_conversation = conversation_id
                    agent.voice_status = "in_meeting"
                    break
            
            return {"message": f"Agent {agent_id} joined conversation", "conversation": conversation}
    raise HTTPException(status_code=404, detail="Voice conversation not found")

@router.post("/conversations/{conversation_id}/leave")
async def leave_voice_conversation(conversation_id: str, agent_id: str):
    """Leave a voice conversation"""
    for conversation in mock_conversations:
        if conversation.id == conversation_id:
            if agent_id in conversation.participants:
                conversation.participants.remove(agent_id)
            
            # Update agent status
            for agent in mock_voice_agents:
                if agent.id == agent_id:
                    agent.current_conversation = None
                    agent.voice_status = "idle"
                    break
            
            return {"message": f"Agent {agent_id} left conversation", "conversation": conversation}
    raise HTTPException(status_code=404, detail="Voice conversation not found")

@router.post("/conversations/{conversation_id}/end")
async def end_voice_conversation(conversation_id: str):
    """End a voice conversation"""
    for conversation in mock_conversations:
        if conversation.id == conversation_id:
            conversation.status = "ended"
            conversation.end_time = datetime.now()
            
            # Update all participant agents
            for agent_id in conversation.participants:
                for agent in mock_voice_agents:
                    if agent.id == agent_id:
                        agent.current_conversation = None
                        agent.voice_status = "idle"
                        break
            
            return {"message": "Voice conversation ended", "conversation": conversation}
    raise HTTPException(status_code=404, detail="Voice conversation not found")

@router.post("/conversations/{conversation_id}/messages")
async def send_voice_message(conversation_id: str, message: VoiceMessage):
    """Send a voice message in a conversation"""
    message.id = f"msg-{uuid.uuid4().hex[:8]}"
    message.timestamp = datetime.now()
    
    # Generate Web3 signature
    msg_data = {
        "sender_id": message.sender_id,
        "content": message.content,
        "timestamp": message.timestamp.isoformat()
    }
    message.web3_signature = hashlib.sha256(json.dumps(msg_data, sort_keys=True).encode()).hexdigest()
    
    # Add to conversation transcript
    for conversation in mock_conversations:
        if conversation.id == conversation_id:
            conversation.transcript.append({
                "id": message.id,
                "sender_id": message.sender_id,
                "sender_name": message.sender_name,
                "message_type": message.message_type,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "voice_duration": message.voice_duration,
                "confidence_score": message.confidence_score,
                "web3_signature": message.web3_signature
            })
            
            # Update agent activity
            for agent in mock_voice_agents:
                if agent.id == message.sender_id:
                    agent.last_voice_activity = datetime.now()
                    agent.voice_status = "speaking" if message.message_type == "speech" else "listening"
                    break
            
            return {"message": "Voice message sent", "voice_message": message}
    
    raise HTTPException(status_code=404, detail="Voice conversation not found")

@router.post("/conversations/{conversation_id}/llm-consultation")
async def request_llm_voice_consultation(conversation_id: str, query: str, llm_model: str = "gpt-4"):
    """Request LLM consultation during voice conversation"""
    # Simulate LLM response
    llm_response = f"Based on the conversation context, {llm_model} suggests: {query}"
    
    # Create voice message for LLM response
    message = VoiceMessage(
        id=f"msg-{uuid.uuid4().hex[:8]}",
        conversation_id=conversation_id,
        sender_id="llm-system",
        sender_name=f"{llm_model} Assistant",
        message_type="llm_response",
        content=llm_response,
        timestamp=datetime.now(),
        confidence_score=0.92
    )
    
    # Add to conversation
    for conversation in mock_conversations:
        if conversation.id == conversation_id:
            conversation.transcript.append({
                "id": message.id,
                "sender_id": message.sender_id,
                "sender_name": message.sender_name,
                "message_type": message.message_type,
                "content": message.content,
                "timestamp": message.timestamp.isoformat(),
                "confidence_score": message.confidence_score
            })
            return {"message": "LLM consultation completed", "llm_response": message}
    
    raise HTTPException(status_code=404, detail="Voice conversation not found")

@router.websocket("/ws/voice/{conversation_id}")
async def voice_websocket_endpoint(websocket: WebSocket, conversation_id: str):
    """WebSocket endpoint for real-time voice communication"""
    await websocket.accept()
    voice_connections[conversation_id] = websocket
    
    try:
        while True:
            data = await websocket.receive_text()
            message = json.loads(data)
            
            # Handle different voice message types
            if message["type"] == "join_voice":
                await websocket.send_text(json.dumps({
                    "type": "system",
                    "message": f"Agent {message['agent_id']} joined voice conversation"
                }))
            
            elif message["type"] == "voice_message":
                # Process voice message
                voice_msg = {
                    "type": "voice_message",
                    "sender_id": message["sender_id"],
                    "sender_name": message["sender_name"],
                    "content": message["content"],
                    "timestamp": datetime.now().isoformat(),
                    "voice_duration": message.get("voice_duration"),
                    "confidence_score": message.get("confidence_score", 0.85)
                }
                await websocket.send_text(json.dumps(voice_msg))
            
            elif message["type"] == "voice_command":
                # Handle voice commands
                command_response = {
                    "type": "command_response",
                    "command": message["command"],
                    "response": f"Executing command: {message['command']}",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send_text(json.dumps(command_response))
            
            elif message["type"] == "llm_request":
                # Simulate LLM voice consultation
                llm_response = {
                    "type": "llm_voice_response",
                    "model": message["model"],
                    "response": f"Voice consultation from {message['model']}: {message['query']}",
                    "timestamp": datetime.now().isoformat()
                }
                await websocket.send_text(json.dumps(llm_response))
    
    except WebSocketDisconnect:
        if conversation_id in voice_connections:
            del voice_connections[conversation_id]

@router.get("/voice-analytics")
async def get_voice_analytics():
    """Get analytics on voice communication"""
    return {
        "total_agents": len(mock_voice_agents),
        "voice_enabled_agents": len([a for a in mock_voice_agents if a.voice_enabled]),
        "active_conversations": len([c for c in mock_conversations if c.status == "active"]),
        "total_conversations": len(mock_conversations),
        "total_messages": sum(len(c.transcript) for c in mock_conversations),
        "agent_activity": {
            agent.name: {
                "voice_status": agent.voice_status,
                "last_activity": agent.last_voice_activity.isoformat(),
                "current_conversation": agent.current_conversation
            }
            for agent in mock_voice_agents
        }
    }

@router.get("/web3/voice-identities")
async def get_web3_voice_identities():
    """Get Web3 identities for voice agents"""
    identities = [
        {
            "agent_id": agent.id,
            "agent_name": agent.name,
            "web3_identity": agent.web3_identity,
            "voice_signature": agent.voice_signature
        }
        for agent in mock_voice_agents
        if agent.web3_identity
    ]
    return {"voice_identities": identities}

@router.post("/web3/verify-voice")
async def verify_voice_identity(agent_id: str, voice_signature: str):
    """Verify voice identity with Web3"""
    for agent in mock_voice_agents:
        if agent.id == agent_id:
            agent.voice_signature = voice_signature
            return {
                "message": "Voice identity verified",
                "agent_id": agent_id,
                "voice_signature": voice_signature,
                "verification_hash": hashlib.sha256(voice_signature.encode()).hexdigest()
            }
    raise HTTPException(status_code=404, detail="Voice agent not found")

@router.post("/voice-recording")
async def upload_voice_recording(
    conversation_id: str,
    agent_id: str,
    recording: UploadFile = File(...)
):
    """Upload voice recording for a conversation"""
    # Save recording
    recording_path = f"voice_recordings/{conversation_id}_{agent_id}_{recording.filename}"
    os.makedirs("voice_recordings", exist_ok=True)
    
    with open(recording_path, "wb") as buffer:
        content = await recording.read()
        buffer.write(content)
    
    # Update conversation with recording URL
    for conversation in mock_conversations:
        if conversation.id == conversation_id:
            conversation.voice_recording_url = recording_path
            return {
                "message": "Voice recording uploaded",
                "recording_path": recording_path,
                "conversation_id": conversation_id
            }
    
    raise HTTPException(status_code=404, detail="Voice conversation not found") 