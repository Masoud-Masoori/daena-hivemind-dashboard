import importlib
import json
from Agents import common
from Core.messaging.message_bus import MessageBus
from Core.messaging.message import Message
from typing import Dict, Any
import asyncio

# Load configuration
with open("Core/config.json") as f:
    config = json.load(f)

# Initialize global components
memory = common.DaenaMemory()
bus = common.MessageBus()

# Import agent classes dynamically based on config
agents_config = config.get("departments", [])
agents = {}
for agent_conf in agents_config:
    name = agent_conf["name"]
    module = agent_conf["module"]  # e.g., "marketing_agent"
    class_name = agent_conf["class"]
    try:
        agent_module = importlib.import_module(f"Agents.{module}")
        AgentClass = getattr(agent_module, class_name)
        agent_instance = AgentClass(name=name, bus=bus, memory=memory, config=agent_conf)
        agents[name] = agent_instance
        print(f"Initialized agent: {name}")
    except Exception as e:
        print(f"Error initializing agent {name}: {e}")

# Governance agents (hidden)
gov_agents_config = config.get("governance", [])
gov_agents = {}
for agent_conf in gov_agents_config:
    name = agent_conf["name"]
    module = agent_conf["module"]
    class_name = agent_conf["class"]
    try:
        agent_module = importlib.import_module(f"Governance.{module}")
        AgentClass = getattr(agent_module, class_name)
        agent_instance = AgentClass(name=name, bus=bus, memory=memory, config=agent_conf, watched_agents=agents)
        gov_agents[name] = agent_instance
        print(f"Initialized governance agent: {name}")
    except Exception as e:
        print(f"Error initializing governance agent {name}: {e}")

class Orchestrator:
    def __init__(self):
        self.bus = MessageBus()
        self.agents: Dict[str, Any] = {}
        self.gov_agents: Dict[str, Any] = {}

    async def register_agent(self, agent_name: str, agent_instance: Any):
        """Register an agent with the orchestrator."""
        self.agents[agent_name] = agent_instance
        await self.bus.subscribe(f"agent.{agent_name}", agent_instance.handle_message)
        print(f"[Orchestrator] Registered agent: {agent_name}")

    async def register_gov_agent(self, agent_name: str, agent_instance: Any):
        """Register a governance agent with the orchestrator."""
        self.gov_agents[agent_name] = agent_instance
        await self.bus.subscribe(f"agent.{agent_name}", agent_instance.handle_message)
        print(f"[Orchestrator] Registered governance agent: {agent_name}")

    async def start(self):
        """Start the orchestrator's main loop."""
        print("Daena orchestrator running. Waiting for tasks...")
        # Start message processing
        await self.bus.process_messages()

    async def stop(self):
        """Stop the orchestrator."""
        await self.bus.stop()
        print("Orchestrator stopped")

# Create global orchestrator instance
orchestrator = Orchestrator()

async def main():
    """Main entry point for the orchestrator."""
    try:
        await orchestrator.start()
    except KeyboardInterrupt:
        print("\nShutting down orchestrator...")
        await orchestrator.stop()

if __name__ == "__main__":
    asyncio.run(main())
