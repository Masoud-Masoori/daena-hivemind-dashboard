from fastapi import APIRouter, HTTPException
from typing import Dict, List, Any
from datetime import datetime, timedelta
import psutil
import json
from pathlib import Path

router = APIRouter()

def get_system_metrics() -> Dict[str, Any]:
    """Get current system metrics."""
    return {
        "cpu": {
            "percent": psutil.cpu_percent(interval=1),
            "count": psutil.cpu_count(),
            "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None
        },
        "memory": {
            "total": psutil.virtual_memory().total,
            "available": psutil.virtual_memory().available,
            "percent": psutil.virtual_memory().percent
        },
        "disk": {
            "total": psutil.disk_usage('/').total,
            "used": psutil.disk_usage('/').used,
            "free": psutil.disk_usage('/').free,
            "percent": psutil.disk_usage('/').percent
        },
        "network": {
            "bytes_sent": psutil.net_io_counters().bytes_sent,
            "bytes_recv": psutil.net_io_counters().bytes_recv,
            "packets_sent": psutil.net_io_counters().packets_sent,
            "packets_recv": psutil.net_io_counters().packets_recv
        }
    }

def get_model_metrics() -> Dict[str, Any]:
    """Get current model metrics."""
    try:
        with open("data/model_metrics.json", "r") as f:
            return json.load(f)
    except FileNotFoundError:
        return {
            "models": {},
            "last_updated": datetime.now().isoformat()
        }

@router.get("/system", response_model=Dict[str, Any])
async def get_system_status():
    """Get current system status and metrics."""
    try:
        return {
            "timestamp": datetime.now().isoformat(),
            "metrics": get_system_metrics(),
            "status": "healthy"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/models", response_model=Dict[str, Any])
async def get_models_status():
    """Get current status of all models."""
    try:
        return get_model_metrics()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs", response_model=List[Dict[str, Any]])
async def get_recent_logs(limit: int = 100):
    """Get recent system logs."""
    try:
        log_file = Path("logs/daena.log")
        if not log_file.exists():
            return []
        
        logs = []
        with open(log_file, "r") as f:
            for line in f.readlines()[-limit:]:
                try:
                    timestamp, level, message = line.split(" - ", 2)
                    logs.append({
                        "timestamp": timestamp,
                        "level": level,
                        "message": message.strip()
                    })
                except ValueError:
                    continue
        
        return logs
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/performance", response_model=Dict[str, Any])
async def get_performance_metrics(hours: int = 24):
    """Get performance metrics for the specified time period."""
    try:
        metrics_file = Path("data/performance_metrics.json")
        if not metrics_file.exists():
            return {
                "cpu_usage": [],
                "memory_usage": [],
                "response_times": [],
                "error_rates": []
            }
        
        with open(metrics_file, "r") as f:
            metrics = json.load(f)
        
        # Filter metrics for the specified time period
        cutoff_time = datetime.now() - timedelta(hours=hours)
        filtered_metrics = {
            key: [
                m for m in values
                if datetime.fromisoformat(m["timestamp"]) > cutoff_time
            ]
            for key, values in metrics.items()
        }
        
        return filtered_metrics
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 