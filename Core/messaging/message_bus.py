"""Message bus for Daena's messaging system."""
import asyncio
import logging
from typing import Dict, List, Optional
from .message import Message, MessageType
from ..agents.agent import Agent, AgentStatus

logger = logging.getLogger(__name__)

class MessageBus:
    """Message bus for handling communication between agents."""
    
    def __init__(self):
        """Initialize the message bus."""
        self.agents: Dict[str, Agent] = {}
        self.queues: Dict[str, asyncio.Queue] = {}
        self.subscribers: Dict[str, List[str]] = {}
        self._running = False
        
    async def start(self):
        """Start the message bus."""
        self._running = True
        logger.info("Message bus started")
        
    async def stop(self):
        """Stop the message bus."""
        self._running = False
        logger.info("Message bus stopped")
        
    async def register_agent(self, agent: Agent):
        """Register a new agent."""
        if agent.id in self.agents:
            raise ValueError(f"Agent {agent.id} already registered")
            
        self.agents[agent.id] = agent
        self.queues[agent.id] = asyncio.Queue()
        self.subscribers[agent.id] = []
        logger.info(f"Agent {agent.id} registered")
        
    async def unregister_agent(self, agent_id: str):
        """Unregister an agent."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not registered")
            
        del self.agents[agent_id]
        del self.queues[agent_id]
        del self.subscribers[agent_id]
        logger.info(f"Agent {agent_id} unregistered")
        
    async def subscribe(self, agent_id: str, queue: asyncio.Queue):
        """Subscribe an agent to messages."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not registered")
            
        self.subscribers[agent_id].append(queue)
        logger.info(f"Agent {agent_id} subscribed")
        
    async def unsubscribe(self, agent_id: str, queue: asyncio.Queue):
        """Unsubscribe an agent from messages."""
        if agent_id not in self.agents:
            raise ValueError(f"Agent {agent_id} not registered")
            
        self.subscribers[agent_id].remove(queue)
        logger.info(f"Agent {agent_id} unsubscribed")
        
    async def publish(self, message: Message):
        """Publish a message to all subscribers."""
        if not self._running:
            raise RuntimeError("Message bus is not running")
            
        for agent_id, queues in self.subscribers.items():
            for queue in queues:
                await queue.put(message)
        logger.info(f"Message {message.id} published")
        
    async def get_all_agents(self) -> List[Agent]:
        """Get all registered agents."""
        return list(self.agents.values()) 