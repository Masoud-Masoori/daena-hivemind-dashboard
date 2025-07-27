from fastapi import APIRouter, HTTPException, Query
from typing import List, Optional
from datetime import datetime, timedelta
import psutil
import GPUtil
from pydantic import BaseModel

router = APIRouter()

class GPUMetrics(BaseModel):
    id: int
    name: str
    load: float
    memory_used: int
    memory_total: int
    temperature: float
    power_draw: Optional[float]

class CPUMetrics(BaseModel):
    usage: float
    cores: int
    frequency: Optional[float]
    temperature: Optional[float]
    per_core_usage: List[float]

class MemoryMetrics(BaseModel):
    total: int
    used: int
    free: int
    usage_percent: float
    swap: dict

class DiskMetrics(BaseModel):
    total: int
    used: int
    free: int
    usage_percent: float
    io: dict

class NetworkMetrics(BaseModel):
    bytes_sent: int
    bytes_recv: int
    packets_sent: int
    packets_recv: int
    connections: int

class SystemMetrics(BaseModel):
    timestamp: datetime
    cpu: CPUMetrics
    memory: MemoryMetrics
    disk: DiskMetrics
    network: NetworkMetrics
    gpu: Optional[List[GPUMetrics]]

@router.get("/metrics", response_model=List[SystemMetrics])
async def get_metrics(
    period: str = Query("1h", description="Time period for metrics (1h, 6h, 24h, 7d)"),
    interval: int = Query(30, description="Sampling interval in seconds")
):
    """Get system metrics for the specified time period."""
    try:
        # Convert period to timedelta
        period_map = {
            "1h": timedelta(hours=1),
            "6h": timedelta(hours=6),
            "24h": timedelta(hours=24),
            "7d": timedelta(days=7)
        }
        delta = period_map.get(period)
        if not delta:
            raise HTTPException(status_code=400, detail="Invalid period")

        # Get current metrics
        metrics = get_current_metrics()
        return [metrics]  # In a real implementation, this would return historical metrics

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/metrics/current", response_model=SystemMetrics)
async def get_current_metrics():
    """Get current system metrics."""
    try:
        # CPU metrics
        cpu_usage = psutil.cpu_percent(interval=1, percpu=True)
        cpu_metrics = CPUMetrics(
            usage=sum(cpu_usage) / len(cpu_usage),
            cores=psutil.cpu_count(),
            frequency=psutil.cpu_freq().current if psutil.cpu_freq() else None,
            temperature=get_cpu_temperature(),
            per_core_usage=cpu_usage
        )

        # Memory metrics
        memory = psutil.virtual_memory()
        swap = psutil.swap_memory()
        memory_metrics = MemoryMetrics(
            total=memory.total,
            used=memory.used,
            free=memory.free,
            usage_percent=memory.percent,
            swap={
                "total": swap.total,
                "used": swap.used,
                "free": swap.free,
                "percent": swap.percent
            }
        )

        # Disk metrics
        disk = psutil.disk_usage('/')
        disk_io = psutil.disk_io_counters()
        disk_metrics = DiskMetrics(
            total=disk.total,
            used=disk.used,
            free=disk.free,
            usage_percent=disk.percent,
            io={
                "read_bytes": disk_io.read_bytes,
                "write_bytes": disk_io.write_bytes,
                "read_count": disk_io.read_count,
                "write_count": disk_io.write_count
            }
        )

        # Network metrics
        network = psutil.net_io_counters()
        network_metrics = NetworkMetrics(
            bytes_sent=network.bytes_sent,
            bytes_recv=network.bytes_recv,
            packets_sent=network.packets_sent,
            packets_recv=network.packets_recv,
            connections=len(psutil.net_connections())
        )

        # GPU metrics
        try:
            gpus = GPUtil.getGPUs()
            gpu_metrics = [
                GPUMetrics(
                    id=gpu.id,
                    name=gpu.name,
                    load=gpu.load * 100,
                    memory_used=gpu.memoryUsed,
                    memory_total=gpu.memoryTotal,
                    temperature=gpu.temperature,
                    power_draw=gpu.powerDraw if hasattr(gpu, 'powerDraw') else None
                )
                for gpu in gpus
            ]
        except Exception:
            gpu_metrics = None

        return SystemMetrics(
            timestamp=datetime.utcnow(),
            cpu=cpu_metrics,
            memory=memory_metrics,
            disk=disk_metrics,
            network=network_metrics,
            gpu=gpu_metrics
        )

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def get_cpu_temperature():
    """Get CPU temperature if available."""
    try:
        temps = psutil.sensors_temperatures()
        if temps and 'coretemp' in temps:
            return sum(temp.current for temp in temps['coretemp']) / len(temps['coretemp'])
        return None
    except Exception:
        return None

@router.get("/metrics/summary")
async def get_metrics_summary():
    """Get a summary of current system metrics."""
    try:
        metrics = await get_current_metrics()
        return {
            "cpu_usage": metrics.cpu.usage,
            "memory_usage": metrics.memory.usage_percent,
            "disk_usage": metrics.disk.usage_percent,
            "gpu_usage": metrics.gpu[0].load if metrics.gpu else None,
            "network_traffic": {
                "sent": metrics.network.bytes_sent,
                "received": metrics.network.bytes_recv
            },
            "timestamp": metrics.timestamp
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e)) 