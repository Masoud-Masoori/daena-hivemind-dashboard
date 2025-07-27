from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import random

router = APIRouter()

# Pydantic models
class TaskBase(BaseModel):
    title: str
    description: str
    priority: str  # 'low', 'medium', 'high', 'urgent'
    assigned_agent: str
    department: str

class TaskCreate(TaskBase):
    pass

class TaskUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    priority: Optional[str] = None
    assigned_agent: Optional[str] = None
    department: Optional[str] = None

class Task(TaskBase):
    id: str
    status: str  # 'pending', 'running', 'completed', 'failed', 'cancelled'
    created_at: str
    started_at: Optional[str] = None
    completed_at: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    error: Optional[str] = None

class TaskAssignment(BaseModel):
    agent_id: str

# Mock data storage
tasks_db = {
    "task-001": {
        "id": "task-001",
        "title": "Customer Data Analysis",
        "description": "Analyze customer behavior patterns from the last quarter",
        "status": "running",
        "priority": "high",
        "assigned_agent": "agent-001",
        "department": "Analytics",
        "created_at": "2025-01-14T10:00:00Z",
        "started_at": "2025-01-14T10:05:00Z",
        "completed_at": None,
        "result": None,
        "error": None
    },
    "task-002": {
        "id": "task-002",
        "title": "System Security Audit",
        "description": "Perform comprehensive security audit of all systems",
        "status": "completed",
        "priority": "urgent",
        "assigned_agent": "agent-002",
        "department": "Security",
        "created_at": "2025-01-14T08:00:00Z",
        "started_at": "2025-01-14T08:10:00Z",
        "completed_at": "2025-01-14T12:30:00Z",
        "result": {
            "vulnerabilities_found": 3,
            "critical_issues": 0,
            "recommendations": ["Update firewall rules", "Enable MFA"]
        },
        "error": None
    },
    "task-003": {
        "id": "task-003",
        "title": "Database Optimization",
        "description": "Optimize database queries and indexes for better performance",
        "status": "pending",
        "priority": "medium",
        "assigned_agent": "agent-003",
        "department": "IT",
        "created_at": "2025-01-14T14:00:00Z",
        "started_at": None,
        "completed_at": None,
        "result": None,
        "error": None
    },
    "task-004": {
        "id": "task-004",
        "title": "API Integration Testing",
        "description": "Test integration with third-party APIs",
        "status": "failed",
        "priority": "high",
        "assigned_agent": "agent-001",
        "department": "Development",
        "created_at": "2025-01-14T09:00:00Z",
        "started_at": "2025-01-14T09:15:00Z",
        "completed_at": "2025-01-14T11:45:00Z",
        "result": None,
        "error": "API endpoint timeout after 30 seconds"
    }
}

@router.get("/", response_model=List[Task])
async def get_tasks(status: Optional[str] = None, priority: Optional[str] = None):
    """Get all tasks with optional filtering"""
    tasks = list(tasks_db.values())
    
    if status:
        tasks = [task for task in tasks if task["status"] == status]
    
    if priority:
        tasks = [task for task in tasks if task["priority"] == priority]
    
    # Sort by creation date (newest first)
    tasks.sort(key=lambda x: x["created_at"], reverse=True)
    return tasks

@router.get("/{task_id}", response_model=Task)
async def get_task(task_id: str):
    """Get a specific task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    return tasks_db[task_id]

@router.post("/", response_model=Task)
async def create_task(task_data: TaskCreate):
    """Create a new task"""
    task_id = f"task-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    
    new_task = {
        "id": task_id,
        "title": task_data.title,
        "description": task_data.description,
        "status": "pending",
        "priority": task_data.priority,
        "assigned_agent": task_data.assigned_agent,
        "department": task_data.department,
        "created_at": now,
        "started_at": None,
        "completed_at": None,
        "result": None,
        "error": None
    }
    
    tasks_db[task_id] = new_task
    return new_task

@router.put("/{task_id}", response_model=Task)
async def update_task(task_id: str, task_data: TaskUpdate):
    """Update a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    update_data = task_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        task[field] = value
    
    return task

@router.delete("/{task_id}")
async def delete_task(task_id: str):
    """Delete a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    del tasks_db[task_id]
    return {"message": "Task deleted successfully"}

@router.post("/{task_id}/assign")
async def assign_task(task_id: str, assignment: TaskAssignment):
    """Assign a task to an agent"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    task["assigned_agent"] = assignment.agent_id
    
    return {"message": f"Task assigned to agent {assignment.agent_id}"}

@router.post("/{task_id}/start")
async def start_task(task_id: str, background_tasks: BackgroundTasks):
    """Start a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    
    if task["status"] != "pending":
        raise HTTPException(status_code=400, detail="Task is not in pending status")
    
    task["status"] = "running"
    task["started_at"] = datetime.utcnow().isoformat() + "Z"
    
    # Simulate task execution
    def simulate_task_execution():
        import time
        time.sleep(random.uniform(5, 15))  # Simulate variable execution time
        
        # Randomly determine success or failure
        if random.random() > 0.1:  # 90% success rate
            task["status"] = "completed"
            task["completed_at"] = datetime.utcnow().isoformat() + "Z"
            task["result"] = {
                "execution_time": f"{random.randint(5, 15)}s",
                "data_processed": random.randint(100, 1000),
                "success": True
            }
        else:
            task["status"] = "failed"
            task["completed_at"] = datetime.utcnow().isoformat() + "Z"
            task["error"] = "Task execution failed due to system error"
    
    background_tasks.add_task(simulate_task_execution)
    
    return {"message": "Task started successfully"}

@router.post("/{task_id}/cancel")
async def cancel_task(task_id: str):
    """Cancel a task"""
    if task_id not in tasks_db:
        raise HTTPException(status_code=404, detail="Task not found")
    
    task = tasks_db[task_id]
    
    if task["status"] in ["completed", "failed", "cancelled"]:
        raise HTTPException(status_code=400, detail="Task cannot be cancelled")
    
    task["status"] = "cancelled"
    task["completed_at"] = datetime.utcnow().isoformat() + "Z"
    
    return {"message": "Task cancelled successfully"}

@router.get("/agent/{agent_id}")
async def get_agent_tasks(agent_id: str):
    """Get all tasks assigned to a specific agent"""
    agent_tasks = [task for task in tasks_db.values() if task["assigned_agent"] == agent_id]
    return agent_tasks

@router.get("/department/{department}")
async def get_department_tasks(department: str):
    """Get all tasks for a specific department"""
    dept_tasks = [task for task in tasks_db.values() if task["department"] == department]
    return dept_tasks

@router.get("/stats/overview")
async def get_task_stats():
    """Get task statistics"""
    total_tasks = len(tasks_db)
    pending_tasks = sum(1 for task in tasks_db.values() if task["status"] == "pending")
    running_tasks = sum(1 for task in tasks_db.values() if task["status"] == "running")
    completed_tasks = sum(1 for task in tasks_db.values() if task["status"] == "completed")
    failed_tasks = sum(1 for task in tasks_db.values() if task["status"] == "failed")
    
    priority_counts = {}
    for task in tasks_db.values():
        priority = task["priority"]
        priority_counts[priority] = priority_counts.get(priority, 0) + 1
    
    department_counts = {}
    for task in tasks_db.values():
        dept = task["department"]
        department_counts[dept] = department_counts.get(dept, 0) + 1
    
    # Calculate success rate
    total_completed = completed_tasks + failed_tasks
    success_rate = completed_tasks / total_completed if total_completed > 0 else 0
    
    return {
        "total_tasks": total_tasks,
        "pending_tasks": pending_tasks,
        "running_tasks": running_tasks,
        "completed_tasks": completed_tasks,
        "failed_tasks": failed_tasks,
        "success_rate": success_rate,
        "priority_distribution": priority_counts,
        "department_distribution": department_counts
    }

@router.get("/stats/performance")
async def get_task_performance():
    """Get task performance metrics"""
    completed_tasks = [task for task in tasks_db.values() if task["status"] == "completed"]
    
    if not completed_tasks:
        return {"message": "No completed tasks found"}
    
    # Calculate average completion time
    completion_times = []
    for task in completed_tasks:
        if task["started_at"] and task["completed_at"]:
            start_time = datetime.fromisoformat(task["started_at"].replace("Z", "+00:00"))
            end_time = datetime.fromisoformat(task["completed_at"].replace("Z", "+00:00"))
            duration = (end_time - start_time).total_seconds()
            completion_times.append(duration)
    
    avg_completion_time = sum(completion_times) / len(completion_times) if completion_times else 0
    
    # Calculate tasks by priority
    priority_performance = {}
    for priority in ["low", "medium", "high", "urgent"]:
        priority_tasks = [task for task in completed_tasks if task["priority"] == priority]
        if priority_tasks:
            priority_times = []
            for task in priority_tasks:
                if task["started_at"] and task["completed_at"]:
                    start_time = datetime.fromisoformat(task["started_at"].replace("Z", "+00:00"))
                    end_time = datetime.fromisoformat(task["completed_at"].replace("Z", "+00:00"))
                    duration = (end_time - start_time).total_seconds()
                    priority_times.append(duration)
            
            priority_performance[priority] = {
                "count": len(priority_tasks),
                "avg_completion_time": sum(priority_times) / len(priority_times) if priority_times else 0
            }
    
    return {
        "total_completed_tasks": len(completed_tasks),
        "average_completion_time_seconds": avg_completion_time,
        "priority_performance": priority_performance,
        "recent_completions": len([task for task in completed_tasks 
                                 if datetime.fromisoformat(task["completed_at"].replace("Z", "+00:00")) > 
                                 datetime.now().replace(tzinfo=None) - timedelta(hours=24)])
    } 