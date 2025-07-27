# Routes package initialization
# This file is intentionally minimal to avoid import conflicts

# Export available route modules
__all__ = [
    "agents",
    "departments", 
    "projects",
    "daena_decisions",
    "agent_builder_complete",
    "agent_builder_platform",
    "cmp_voting",
    "strategic_meetings",
    "honey_knowledge",
    "voice_agents",
    "founder_panel",
    "task_timeline",
    "consultation",
    "monitoring",
    "data_sources",
    "ai_models",
    "workflows",
    "security",
    "users",
    "tasks",
    "notifications",
                  "council",
              "strategic_assembly"
]

# NOTE: No actual imports here to prevent circular import issues
# Individual routers are imported directly in main.py using safe_import_router()

from .council import *
from .strategic_assembly import *
