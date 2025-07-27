"""Agent class for Daena's agent system."""
from enum import Enum
from typing import Dict, Any, Optional
from pydantic import BaseModel

class AgentStatus(str, Enum):
    """Status of an agent."""
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

class Agent(BaseModel):
    """An agent in the system."""
    id: str
    name: str
    department: str
    status: AgentStatus = AgentStatus.IDLE
    capabilities: Dict[str, Any] = {}
    metadata: Optional[Dict[str, Any]] = None 