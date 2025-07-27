# DEPRECATED: Use Core/agents/agent.py and Core/messaging/message_bus.py instead
raise ImportError("Agents/common.py is deprecated. Use Core/agents/agent.py and Core/messaging/message_bus.py instead.")
from Core.message_bus import MessageBus, Message
from queue import Queue
from typing import Dict, Any, Optional

class AgentType:
    """Enum-like class for agent types."""
    SYSTEM = "system"
    USER = "user"
    TASK = "task"
    GOVERNANCE = "governance"
    CORE = "core"

class AgentBase:
    """Base class for all agents, providing common functionality."""
    def __init__(self, agent_type: AgentType, name: str = None, bus: MessageBus = None, memory = None, config: dict = None):
        self.agent_type = agent_type
        self.name = name or self.__class__.__name__
        self.bus = bus        # reference to MessageBus
        self.memory = memory  # reference to DaenaMemory
        self.config = config or {}
        self.loop_count = 0   # for loop detection / iteration count

    async def handle_message(self, message: Message):
        """Override this in subclass to handle incoming messages."""
        raise NotImplementedError

    async def send_message(self, target: str, content: Dict[str, Any]):
        """Send a message via the bus to another agent."""
        await self.bus.publish(
            topic=f"agent.{target}",
            content=content,
            sender=self.name,
            metadata={"agent_type": self.agent_type}
        )

    async def think(self, prompt: str):
        """
        Simulate the agent 'thinking' or planning a response.
        In a real agent, this might call an LLM to decide what to do.
        """
        print(f"[{self.name} thinking] {prompt}")
