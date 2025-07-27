"""Message class for Daena's messaging system."""
from enum import Enum
from typing import Dict, Any, Optional
from datetime import datetime
from pydantic import BaseModel

class MessageType(str, Enum):
    """Types of messages in the system."""
    STATUS = "status"
    RESULT = "result"
    TASK = "task"
    ERROR = "error"
    SYSTEM = "system"

class Message(BaseModel):
    """A message in the system."""
    id: str
    type: MessageType
    sender: str
    content: Dict[str, Any]
    timestamp: datetime = datetime.now()
    recipient: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None 