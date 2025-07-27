# DEPRECATED: Use Core/messaging/message_bus.py instead
raise ImportError("backend/message_bus.py is deprecated. Use Core/messaging/message_bus.py instead.")

import asyncio
import json
import logging
from typing import Dict, Any, Optional, List
from enum import Enum
from datetime import datetime
from pydantic import BaseModel

logger = logging.getLogger(__name__)

class MessageType(Enum):
    TASK = "task"
    RESULT = "result"
    STATUS = "status"
    ALERT = "alert"
    METRIC = "metric"
    COMMAND = "command"

class MessagePriority(Enum):
    LOW = 0
    NORMAL = 1
    HIGH = 2
    CRITICAL = 3

class AgentStatus(Enum):
    IDLE = "idle"
    BUSY = "busy"
    ERROR = "error"
    OFFLINE = "offline"

class Message(BaseModel):
    id: str
    type: MessageType
    sender: str
    recipient: Optional[str]
    content: Dict[str, Any]
    priority: MessagePriority = MessagePriority.NORMAL
    timestamp: datetime = datetime.now()
    metadata: Dict[str, Any] = {}

class Agent(BaseModel):
    id: str
    name: str
    department: str
    status: AgentStatus = AgentStatus.IDLE
    capabilities: List[str]
    current_task: Optional[str] = None
    last_seen: datetime = datetime.now()

class MessageBus:
    def __init__(self):
        self.agents: Dict[str, Agent] = {}
        self.message_queue: asyncio.Queue = asyncio.Queue()
        self.subscribers: Dict[str, List[asyncio.Queue]] = {}
        self.running = False

    async def start(self):
        """Start the message bus."""
        self.running = True
        asyncio.create_task(self._process_messages())

    async def stop(self):
        """Stop the message bus."""
        self.running = False
        # Clear all queues
        while not self.message_queue.empty():
            await self.message_queue.get()
        for queues in self.subscribers.values():
            for queue in queues:
                while not queue.empty():
                    await queue.get()

    async def register_agent(self, agent: Agent):
        """Register a new agent with the message bus."""
        self.agents[agent.id] = agent
        self.subscribers[agent.id] = []
        logger.info(f"Agent registered: {agent.name} ({agent.id})")

    async def unregister_agent(self, agent_id: str):
        """Unregister an agent from the message bus."""
        if agent_id in self.agents:
            del self.agents[agent_id]
            del self.subscribers[agent_id]
            logger.info(f"Agent unregistered: {agent_id}")

    async def subscribe(self, agent_id: str, queue: asyncio.Queue):
        """Subscribe an agent to receive messages."""
        if agent_id not in self.subscribers:
            self.subscribers[agent_id] = []
        self.subscribers[agent_id].append(queue)
        logger.info(f"Agent subscribed: {agent_id}")

    async def unsubscribe(self, agent_id: str, queue: asyncio.Queue):
        """Unsubscribe an agent from receiving messages."""
        if agent_id in self.subscribers and queue in self.subscribers[agent_id]:
            self.subscribers[agent_id].remove(queue)
            logger.info(f"Agent unsubscribed: {agent_id}")

    async def publish(self, message: Message):
        """Publish a message to the message bus."""
        await self.message_queue.put(message)
        logger.info(f"Message published: {message.type.value} from {message.sender}")

    async def _process_messages(self):
        """Process messages in the queue."""
        while self.running:
            try:
                message = await self.message_queue.get()
                
                # Update agent status if it's a status message
                if message.type == MessageType.STATUS:
                    if message.sender in self.agents:
                        self.agents[message.sender].status = AgentStatus(message.content.get("status"))
                        self.agents[message.sender].last_seen = datetime.now()

                # Route message to recipients
                if message.recipient:
                    # Direct message to specific agent
                    if message.recipient in self.subscribers:
                        for queue in self.subscribers[message.recipient]:
                            await queue.put(message)
                else:
                    # Broadcast to all agents
                    for queues in self.subscribers.values():
                        for queue in queues:
                            await queue.put(message)

                self.message_queue.task_done()
            except Exception as e:
                logger.error(f"Error processing message: {str(e)}")

    async def get_agent_status(self, agent_id: str) -> Optional[Agent]:
        """Get the current status of an agent."""
        return self.agents.get(agent_id)

    async def get_all_agents(self) -> List[Agent]:
        """Get all registered agents."""
        return list(self.agents.values())

    async def route_task(self, task: Dict[str, Any], priority: MessagePriority = MessagePriority.NORMAL) -> str:
        """Route a task to the most appropriate agent."""
        # Simple routing based on agent capabilities and current status
        best_agent = None
        best_score = -1

        for agent in self.agents.values():
            if agent.status != AgentStatus.IDLE:
                continue

            # Calculate score based on capabilities match
            score = sum(1 for cap in task.get("required_capabilities", []) 
                       if cap in agent.capabilities)
            
            if score > best_score:
                best_score = score
                best_agent = agent

        if best_agent:
            message = Message(
                id=f"task_{datetime.now().timestamp()}",
                type=MessageType.TASK,
                sender="system",
                recipient=best_agent.id,
                content=task,
                priority=priority
            )
            await self.publish(message)
            return message.id
        else:
            raise RuntimeError("No suitable agent found for task")

# Create a global message bus instance
message_bus = MessageBus() 