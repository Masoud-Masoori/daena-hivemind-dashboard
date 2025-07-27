from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional, Dict, Any
from pydantic import BaseModel
import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path
import threading

router = APIRouter(prefix="/task-timeline", tags=["Task Timeline Tracking"])

# Task Timeline Models
class TaskEvent(BaseModel):
    id: str
    task_id: str
    project_id: str
    event_type: str  # "created", "started", "completed", "failed", "paused", "resumed", "error", "resolution"
    description: str
    details: Optional[Dict[str, Any]] = None
    agent_id: Optional[str] = None
    agent_name: Optional[str] = None
    timestamp: datetime
    duration: Optional[float] = None  # seconds
    error_code: Optional[str] = None
    error_message: Optional[str] = None
    resolution_steps: Optional[List[str]] = None
    honey_knowledge_generated: Optional[List[str]] = None
    web3_transaction_hash: Optional[str] = None

class TaskTimeline(BaseModel):
    id: str
    task_id: str
    project_id: str
    project_name: str
    task_name: str
    events: List[TaskEvent]
    total_duration: float
    status: str  # "active", "completed", "failed", "paused"
    created_at: datetime
    updated_at: datetime
    error_count: int = 0
    resolution_count: int = 0
    honey_knowledge_count: int = 0

class ProjectTimeline(BaseModel):
    id: str
    project_id: str
    project_name: str
    task_timelines: List[TaskTimeline]
    total_tasks: int
    completed_tasks: int
    failed_tasks: int
    total_duration: float
    created_at: datetime
    updated_at: datetime

# Mock data storage
task_timelines: Dict[str, TaskTimeline] = {}
project_timelines: Dict[str, ProjectTimeline] = {}

# File-based persistence
TIMELINE_DIR = Path("persistent_timeline_logs")
TIMELINE_DIR.mkdir(exist_ok=True)
TIMELINE_LOCK = threading.Lock()

def persist_timeline(timeline: TaskTimeline):
    """Persist timeline to file"""
    with TIMELINE_LOCK:
        path = TIMELINE_DIR / f"timeline_{timeline.task_id}.json"
        with open(path, "w", encoding="utf-8") as f:
            json.dump(timeline.model_dump(), f, default=str)

def load_timeline(task_id: str) -> Optional[Dict[str, Any]]:
    """Load timeline from file"""
    path = TIMELINE_DIR / f"timeline_{task_id}.json"
    if path.exists():
        with open(path, "r", encoding="utf-8") as f:
            return json.load(f)
    return None

@router.post("/task/{task_id}/event")
async def log_task_event(
    task_id: str,
    project_id: str,
    project_name: str,
    task_name: str,
    event_type: str,
    description: str,
    agent_id: Optional[str] = None,
    agent_name: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
    error_code: Optional[str] = None,
    error_message: Optional[str] = None,
    resolution_steps: Optional[List[str]] = None,
    honey_knowledge_generated: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Log a new task event"""
    
    # Create or get timeline
    if task_id not in task_timelines:
        timeline = TaskTimeline(
            id=f"timeline-{uuid.uuid4().hex[:8]}",
            task_id=task_id,
            project_id=project_id,
            project_name=project_name,
            task_name=task_name,
            events=[],
            total_duration=0.0,
            status="active",
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        task_timelines[task_id] = timeline
    else:
        timeline = task_timelines[task_id]
    
    # Create event
    event = TaskEvent(
        id=f"event-{uuid.uuid4().hex[:8]}",
        task_id=task_id,
        project_id=project_id,
        event_type=event_type,
        description=description,
        details=details,
        agent_id=agent_id,
        agent_name=agent_name,
        timestamp=datetime.now(),
        error_code=error_code,
        error_message=error_message,
        resolution_steps=resolution_steps,
        honey_knowledge_generated=honey_knowledge_generated
    )
    
    # Calculate duration if this is a completion event
    if event_type in ["completed", "failed", "paused"]:
        if timeline.events:
            last_event = timeline.events[-1]
            if last_event.event_type in ["created", "started", "resumed"]:
                duration = (event.timestamp - last_event.timestamp).total_seconds()
                event.duration = duration
                timeline.total_duration += duration
    
    # Update timeline statistics
    timeline.events.append(event)
    timeline.updated_at = datetime.now()
    
    if event_type == "error":
        timeline.error_count += 1
        timeline.status = "failed"
    elif event_type == "resolution":
        timeline.resolution_count += 1
    elif event_type == "completed":
        timeline.status = "completed"
    
    if honey_knowledge_generated:
        timeline.honey_knowledge_count += len(honey_knowledge_generated)
    
    # Update project timeline
    update_project_timeline(project_id, project_name, timeline)
    
    # Persist to file
    persist_timeline(timeline)
    
    return {
        "message": "Task event logged successfully",
        "event": event,
        "timeline": timeline
    }

def update_project_timeline(project_id: str, project_name: str, task_timeline: TaskTimeline):
    """Update project timeline with task timeline"""
    if project_id not in project_timelines:
        project_timeline = ProjectTimeline(
            id=f"project-timeline-{uuid.uuid4().hex[:8]}",
            project_id=project_id,
            project_name=project_name,
            task_timelines=[],
            total_tasks=0,
            completed_tasks=0,
            failed_tasks=0,
            total_duration=0.0,
            created_at=datetime.now(),
            updated_at=datetime.now()
        )
        project_timelines[project_id] = project_timeline
    else:
        project_timeline = project_timelines[project_id]
    
    # Update or add task timeline
    existing_task = None
    for i, task in enumerate(project_timeline.task_timelines):
        if task.task_id == task_timeline.task_id:
            existing_task = i
            break
    
    if existing_task is not None:
        project_timeline.task_timelines[existing_task] = task_timeline
    else:
        project_timeline.task_timelines.append(task_timeline)
    
    # Recalculate project statistics
    project_timeline.total_tasks = len(project_timeline.task_timelines)
    project_timeline.completed_tasks = len([t for t in project_timeline.task_timelines if t.status == "completed"])
    project_timeline.failed_tasks = len([t for t in project_timeline.task_timelines if t.status == "failed"])
    project_timeline.total_duration = sum(t.total_duration for t in project_timeline.task_timelines)
    project_timeline.updated_at = datetime.now()

@router.get("/task/{task_id}")
async def get_task_timeline(task_id: str) -> TaskTimeline:
    """Get timeline for a specific task"""
    if task_id not in task_timelines:
        # Try to load from file
        loaded_data = load_timeline(task_id)
        if loaded_data:
            # Reconstruct timeline from loaded data
            timeline = TaskTimeline(**loaded_data)
            task_timelines[task_id] = timeline
            return timeline
        else:
            raise HTTPException(status_code=404, detail="Task timeline not found")
    
    return task_timelines[task_id]

@router.get("/project/{project_id}")
async def get_project_timeline(project_id: str) -> ProjectTimeline:
    """Get timeline for a specific project"""
    if project_id not in project_timelines:
        raise HTTPException(status_code=404, detail="Project timeline not found")
    
    return project_timelines[project_id]

@router.get("/projects")
async def get_all_project_timelines() -> Dict[str, Any]:
    """Get all project timelines"""
    return {
        "projects": list(project_timelines.values()),
        "total_projects": len(project_timelines),
        "total_tasks": sum(p.total_tasks for p in project_timelines.values()),
        "completed_tasks": sum(p.completed_tasks for p in project_timelines.values()),
        "failed_tasks": sum(p.failed_tasks for p in project_timelines.values())
    }

@router.get("/task/{task_id}/events")
async def get_task_events(
    task_id: str,
    event_type: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
) -> Dict[str, Any]:
    """Get events for a specific task with optional filtering"""
    timeline = await get_task_timeline(task_id)
    
    events = timeline.events
    
    # Filter by event type
    if event_type:
        events = [e for e in events if e.event_type == event_type]
    
    # Filter by date range
    if start_date:
        start_dt = datetime.fromisoformat(start_date)
        events = [e for e in events if e.timestamp >= start_dt]
    
    if end_date:
        end_dt = datetime.fromisoformat(end_date)
        events = [e for e in events if e.timestamp <= end_dt]
    
    return {
        "task_id": task_id,
        "task_name": timeline.task_name,
        "events": events,
        "total_events": len(events),
        "filtered": event_type is not None or start_date is not None or end_date is not None
    }

@router.get("/task/{task_id}/errors")
async def get_task_errors(task_id: str) -> Dict[str, Any]:
    """Get all errors for a specific task"""
    timeline = await get_task_timeline(task_id)
    
    error_events = [e for e in timeline.events if e.event_type == "error"]
    resolution_events = [e for e in timeline.events if e.event_type == "resolution"]
    
    return {
        "task_id": task_id,
        "task_name": timeline.task_name,
        "errors": error_events,
        "resolutions": resolution_events,
        "total_errors": len(error_events),
        "total_resolutions": len(resolution_events),
        "error_rate": len(error_events) / len(timeline.events) if timeline.events else 0
    }

@router.get("/project/{project_id}/analytics")
async def get_project_analytics(project_id: str) -> Dict[str, Any]:
    """Get analytics for a specific project"""
    project_timeline = await get_project_timeline(project_id)
    
    # Calculate analytics
    all_events = []
    for task_timeline in project_timeline.task_timelines:
        all_events.extend(task_timeline.events)
    
    # Event type breakdown
    event_types = {}
    for event in all_events:
        event_types[event.event_type] = event_types.get(event.event_type, 0) + 1
    
    # Agent activity
    agent_activity = {}
    for event in all_events:
        if event.agent_name:
            agent_activity[event.agent_name] = agent_activity.get(event.agent_name, 0) + 1
    
    # Time-based analysis
    if all_events:
        events_by_hour = {}
        for event in all_events:
            hour = event.timestamp.hour
            events_by_hour[hour] = events_by_hour.get(hour, 0) + 1
        
        # Most active hours
        most_active_hours = sorted(events_by_hour.items(), key=lambda x: x[1], reverse=True)[:3]
    else:
        most_active_hours = []
    
    return {
        "project_id": project_id,
        "project_name": project_timeline.project_name,
        "total_events": len(all_events),
        "event_type_breakdown": event_types,
        "agent_activity": agent_activity,
        "most_active_hours": most_active_hours,
        "average_task_duration": project_timeline.total_duration / project_timeline.total_tasks if project_timeline.total_tasks > 0 else 0,
        "completion_rate": project_timeline.completed_tasks / project_timeline.total_tasks if project_timeline.total_tasks > 0 else 0,
        "error_rate": project_timeline.failed_tasks / project_timeline.total_tasks if project_timeline.total_tasks > 0 else 0
    }

@router.get("/analytics/global")
async def get_global_analytics() -> Dict[str, Any]:
    """Get global analytics across all projects"""
    all_timelines = list(task_timelines.values())
    
    if not all_timelines:
        return {
            "total_tasks": 0,
            "total_events": 0,
            "average_task_duration": 0,
            "completion_rate": 0,
            "error_rate": 0
        }
    
    total_events = sum(len(t.events) for t in all_timelines)
    total_duration = sum(t.total_duration for t in all_timelines)
    completed_tasks = len([t for t in all_timelines if t.status == "completed"])
    failed_tasks = len([t for t in all_timelines if t.status == "failed"])
    
    # Error analysis
    all_errors = []
    for timeline in all_timelines:
        errors = [e for e in timeline.events if e.event_type == "error"]
        all_errors.extend(errors)
    
    # Most common error types
    error_types = {}
    for error in all_errors:
        error_type = error.error_code or "unknown"
        error_types[error_type] = error_types.get(error_type, 0) + 1
    
    return {
        "total_tasks": len(all_timelines),
        "total_events": total_events,
        "average_task_duration": total_duration / len(all_timelines),
        "completion_rate": completed_tasks / len(all_timelines),
        "error_rate": failed_tasks / len(all_timelines),
        "total_errors": len(all_errors),
        "error_type_breakdown": error_types,
        "most_common_errors": sorted(error_types.items(), key=lambda x: x[1], reverse=True)[:5]
    }

@router.post("/task/{task_id}/resolution")
async def add_resolution(
    task_id: str,
    resolution_steps: List[str],
    agent_id: Optional[str] = None,
    agent_name: Optional[str] = None,
    honey_knowledge_generated: Optional[List[str]] = None
) -> Dict[str, Any]:
    """Add a resolution to a task"""
    return await log_task_event(
        task_id=task_id,
        project_id="",  # Will be filled from existing timeline
        project_name="",  # Will be filled from existing timeline
        task_name="",  # Will be filled from existing timeline
        event_type="resolution",
        description="Task resolution applied",
        agent_id=agent_id,
        agent_name=agent_name,
        resolution_steps=resolution_steps,
        honey_knowledge_generated=honey_knowledge_generated
    ) 