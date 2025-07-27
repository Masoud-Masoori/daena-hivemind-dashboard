from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
from datetime import datetime, timedelta
import psutil
import json
from pathlib import Path

router = APIRouter()

def get_system_metrics() -> Dict[str, Any]:
    """Get current system metrics in the format expected by frontend."""
    try:
        return {
            "cpu_usage": psutil.cpu_percent(interval=1),
            "memory_usage": psutil.virtual_memory().percent,
            "disk_usage": psutil.disk_usage('/').percent,
            "gpu_usage": 0,  # Placeholder for GPU monitoring
            "network_io": {
                "bytes_sent": psutil.net_io_counters().bytes_sent,
                "bytes_recv": psutil.net_io_counters().bytes_recv
            },
            "active_connections": len(psutil.net_connections()),
            "uptime": (datetime.now() - datetime.fromtimestamp(psutil.boot_time())).total_seconds()
        }
    except Exception as e:
        return {
            "cpu_usage": 0,
            "memory_usage": 0,
            "disk_usage": 0,
            "gpu_usage": 0,
            "network_io": {"bytes_sent": 0, "bytes_recv": 0},
            "active_connections": 0,
            "uptime": 0
        }

def get_hive_data() -> Dict[str, Any]:
    """Get hive data in the format expected by frontend."""
    try:
        # Mock hive data for now - replace with actual hive logic
        return {
            "core": {
                "status": "active",
                "health": 95,
                "connections": 12
            },
            "departments": [
                {
                    "department_id": "ai",
                    "name": "AI Department",
                    "agent_count": 5,
                    "active_agents": 3,
                    "total_tasks": 150,
                    "success_rate": 0.92,
                    "average_response_time": 2.3
                },
                {
                    "department_id": "data",
                    "name": "Data Department", 
                    "agent_count": 3,
                    "active_agents": 2,
                    "total_tasks": 89,
                    "success_rate": 0.88,
                    "average_response_time": 1.8
                }
            ],
            "connections": [
                {
                    "from": "ai",
                    "to": "data",
                    "strength": 0.8,
                    "type": "data_flow"
                }
            ],
            "metrics": {
                "total_agents": 8,
                "active_agents": 5,
                "total_tasks": 239,
                "success_rate": 0.90
            }
        }
    except Exception as e:
        return {
            "core": {"status": "error", "health": 0, "connections": 0},
            "departments": [],
            "connections": [],
            "metrics": {"total_agents": 0, "active_agents": 0, "total_tasks": 0, "success_rate": 0}
        }

def get_agent_metrics() -> Dict[str, Any]:
    """Get agent metrics in the format expected by frontend."""
    try:
        # Mock agent metrics - replace with actual agent monitoring
        return {
            "agent_1": {
                "agent_id": "agent_1",
                "tasks_completed": 45,
                "tasks_failed": 2,
                "average_response_time": 1.2,
                "last_activity": datetime.now().isoformat(),
                "status": "idle"
            },
            "agent_2": {
                "agent_id": "agent_2", 
                "tasks_completed": 32,
                "tasks_failed": 1,
                "average_response_time": 0.8,
                "last_activity": datetime.now().isoformat(),
                "status": "busy"
            }
        }
    except Exception as e:
        return {}

@router.get("/metrics")
async def get_system_metrics_endpoint():
    """Get system metrics endpoint that frontend expects."""
    try:
        return get_system_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/hive/data")
async def get_hive_data_endpoint():
    """Get hive data endpoint that frontend expects."""
    try:
        return get_hive_data()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/agent-metrics")
async def get_agent_metrics_endpoint():
    """Get agent metrics endpoint that frontend expects."""
    try:
        return get_agent_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 