from fastapi import APIRouter, HTTPException, BackgroundTasks
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime, timedelta
import uuid
import random

router = APIRouter()

# Pydantic models
class WorkflowStep(BaseModel):
    id: str
    name: str
    type: str  # 'agent_action', 'condition', 'delay', 'webhook', 'data_transform'
    config: Dict[str, Any]
    order: int
    dependencies: List[str]

class WorkflowBase(BaseModel):
    name: str
    description: str
    steps: List[WorkflowStep]
    triggers: List[str]

class WorkflowCreate(WorkflowBase):
    pass

class WorkflowUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    steps: Optional[List[WorkflowStep]] = None
    triggers: Optional[List[str]] = None

class Workflow(WorkflowBase):
    id: str
    status: str  # 'active', 'inactive', 'draft'
    created_at: str
    last_executed: Optional[str] = None
    execution_count: int
    success_rate: float

class WorkflowExecution(BaseModel):
    execution_id: str
    workflow_id: str
    status: str  # 'running', 'completed', 'failed', 'cancelled'
    input: Optional[Dict[str, Any]] = None
    result: Optional[Dict[str, Any]] = None
    logs: List[Dict[str, Any]]
    started_at: str
    completed_at: Optional[str] = None
    error: Optional[str] = None

# Mock data storage
workflows_db = {
    "workflow-001": {
        "id": "workflow-001",
        "name": "Customer Support Automation",
        "description": "Automated customer support workflow with AI agents",
        "status": "active",
        "steps": [
            {
                "id": "step-1",
                "name": "Analyze Customer Query",
                "type": "agent_action",
                "config": {"agent_id": "agent-001", "action": "analyze_query"},
                "order": 1,
                "dependencies": []
            },
            {
                "id": "step-2",
                "name": "Route to Department",
                "type": "condition",
                "config": {"condition": "query_type", "routes": {"technical": "step-3", "billing": "step-4"}},
                "order": 2,
                "dependencies": ["step-1"]
            },
            {
                "id": "step-3",
                "name": "Technical Support",
                "type": "agent_action",
                "config": {"agent_id": "agent-002", "action": "technical_support"},
                "order": 3,
                "dependencies": ["step-2"]
            }
        ],
        "triggers": ["new_customer_query", "support_ticket_created"],
        "created_at": "2025-01-14T10:00:00Z",
        "last_executed": "2025-01-14T16:30:00Z",
        "execution_count": 45,
        "success_rate": 0.92
    },
    "workflow-002": {
        "id": "workflow-002",
        "name": "Data Processing Pipeline",
        "description": "Automated data processing and analysis workflow",
        "status": "active",
        "steps": [
            {
                "id": "step-1",
                "name": "Data Validation",
                "type": "data_transform",
                "config": {"validation_rules": ["required_fields", "data_types"]},
                "order": 1,
                "dependencies": []
            },
            {
                "id": "step-2",
                "name": "Data Cleaning",
                "type": "agent_action",
                "config": {"agent_id": "agent-003", "action": "clean_data"},
                "order": 2,
                "dependencies": ["step-1"]
            },
            {
                "id": "step-3",
                "name": "Send to Analytics",
                "type": "webhook",
                "config": {"url": "https://analytics.example.com/webhook", "method": "POST"},
                "order": 3,
                "dependencies": ["step-2"]
            }
        ],
        "triggers": ["new_data_upload", "daily_processing"],
        "created_at": "2025-01-13T14:00:00Z",
        "last_executed": "2025-01-14T06:00:00Z",
        "execution_count": 12,
        "success_rate": 0.98
    }
}

workflow_executions = {}

@router.get("/", response_model=List[Workflow])
async def get_workflows():
    """Get all workflows"""
    return list(workflows_db.values())

@router.get("/{workflow_id}", response_model=Workflow)
async def get_workflow(workflow_id: str):
    """Get a specific workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    return workflows_db[workflow_id]

@router.post("/", response_model=Workflow)
async def create_workflow(workflow_data: WorkflowCreate):
    """Create a new workflow"""
    workflow_id = f"workflow-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    
    new_workflow = {
        "id": workflow_id,
        "name": workflow_data.name,
        "description": workflow_data.description,
        "status": "draft",
        "steps": [step.dict() for step in workflow_data.steps],
        "triggers": workflow_data.triggers,
        "created_at": now,
        "last_executed": None,
        "execution_count": 0,
        "success_rate": 0.0
    }
    
    workflows_db[workflow_id] = new_workflow
    return new_workflow

@router.put("/{workflow_id}", response_model=Workflow)
async def update_workflow(workflow_id: str, workflow_data: WorkflowUpdate):
    """Update a workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_db[workflow_id]
    update_data = workflow_data.dict(exclude_unset=True)
    
    for field, value in update_data.items():
        if field == "steps":
            workflow[field] = [step.dict() if hasattr(step, 'dict') else step for step in value]
        else:
            workflow[field] = value
    
    return workflow

@router.delete("/{workflow_id}")
async def delete_workflow(workflow_id: str):
    """Delete a workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    del workflows_db[workflow_id]
    return {"message": "Workflow deleted successfully"}

@router.post("/{workflow_id}/execute")
async def execute_workflow(workflow_id: str, input_data: Optional[Dict[str, Any]] = None, background_tasks: BackgroundTasks = None):
    """Execute a workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflow = workflows_db[workflow_id]
    if workflow["status"] != "active":
        raise HTTPException(status_code=400, detail="Workflow is not active")
    
    execution_id = f"exec-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    
    # Create execution record
    execution = {
        "execution_id": execution_id,
        "workflow_id": workflow_id,
        "status": "running",
        "input": input_data or {},
        "result": None,
        "logs": [],
        "started_at": now,
        "completed_at": None,
        "error": None
    }
    
    workflow_executions[execution_id] = execution
    
    # Update workflow stats
    workflow["execution_count"] += 1
    workflow["last_executed"] = now
    
    # Simulate workflow execution
    def simulate_execution():
        import time
        logs = []
        
        # Execute each step
        for step in workflow["steps"]:
            time.sleep(1)  # Simulate step execution time
            
            log_entry = {
                "timestamp": datetime.utcnow().isoformat() + "Z",
                "step_id": step["id"],
                "step_name": step["name"],
                "status": "completed",
                "message": f"Step '{step['name']}' executed successfully"
            }
            logs.append(log_entry)
            
            # Update execution logs
            workflow_executions[execution_id]["logs"] = logs
        
        # Complete execution
        workflow_executions[execution_id]["status"] = "completed"
        workflow_executions[execution_id]["completed_at"] = datetime.utcnow().isoformat() + "Z"
        workflow_executions[execution_id]["result"] = {
            "steps_completed": len(workflow["steps"]),
            "execution_time": "5.2s",
            "output": {"status": "success", "data": "Workflow completed successfully"}
        }
        
        # Update success rate
        successful_executions = sum(1 for exec_id, exec_data in workflow_executions.items() 
                                  if exec_data["workflow_id"] == workflow_id and exec_data["status"] == "completed")
        workflow["success_rate"] = successful_executions / workflow["execution_count"]
    
    if background_tasks:
        background_tasks.add_task(simulate_execution)
    else:
        # For immediate execution (not recommended for long workflows)
        simulate_execution()
    
    return {
        "execution_id": execution_id,
        "status": "started",
        "message": "Workflow execution started"
    }

@router.get("/executions/{execution_id}")
async def get_workflow_execution(execution_id: str):
    """Get workflow execution status"""
    if execution_id not in workflow_executions:
        raise HTTPException(status_code=404, detail="Workflow execution not found")
    
    return workflow_executions[execution_id]

@router.get("/{workflow_id}/history")
async def get_workflow_history(workflow_id: str):
    """Get workflow execution history"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    # Get all executions for this workflow
    executions = [
        exec_data for exec_id, exec_data in workflow_executions.items()
        if exec_data["workflow_id"] == workflow_id
    ]
    
    # Calculate statistics
    total_executions = len(executions)
    successful_executions = sum(1 for e in executions if e["status"] == "completed")
    failed_executions = sum(1 for e in executions if e["status"] == "failed")
    
    return {
        "executions": executions,
        "statistics": {
            "total_executions": total_executions,
            "successful_executions": successful_executions,
            "failed_executions": failed_executions,
            "success_rate": successful_executions / total_executions if total_executions > 0 else 0,
            "average_execution_time": "4.5s"  # Mock data
        }
    }

@router.post("/{workflow_id}/activate")
async def activate_workflow(workflow_id: str):
    """Activate a workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflows_db[workflow_id]["status"] = "active"
    return {"message": "Workflow activated successfully"}

@router.post("/{workflow_id}/deactivate")
async def deactivate_workflow(workflow_id: str):
    """Deactivate a workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    workflows_db[workflow_id]["status"] = "inactive"
    return {"message": "Workflow deactivated successfully"}

@router.post("/{workflow_id}/duplicate")
async def duplicate_workflow(workflow_id: str):
    """Duplicate a workflow"""
    if workflow_id not in workflows_db:
        raise HTTPException(status_code=404, detail="Workflow not found")
    
    original_workflow = workflows_db[workflow_id]
    new_workflow_id = f"workflow-{str(uuid.uuid4())[:8]}"
    now = datetime.utcnow().isoformat() + "Z"
    
    new_workflow = {
        "id": new_workflow_id,
        "name": f"{original_workflow['name']} (Copy)",
        "description": original_workflow["description"],
        "status": "draft",
        "steps": original_workflow["steps"].copy(),
        "triggers": original_workflow["triggers"].copy(),
        "created_at": now,
        "last_executed": None,
        "execution_count": 0,
        "success_rate": 0.0
    }
    
    workflows_db[new_workflow_id] = new_workflow
    return new_workflow 