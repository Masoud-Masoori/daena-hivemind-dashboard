import asyncio
import json
import logging
import os
import psutil
import GPUtil
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from prometheus_client import Counter, Gauge, Histogram, start_http_server
import threading
import time

from Core.utils.monitoring_alerts import MonitoringAlert

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    filename='logs/monitoring.log'
)
logger = logging.getLogger(__name__)

# Prometheus metrics
HTTP_REQUESTS = Counter('sunflower_http_requests_total', 'Total HTTP requests', ['method', 'path', 'status'])
HTTP_DURATION = Histogram('sunflower_http_request_duration_seconds', 'HTTP request duration', ['path'])
CPU_USAGE = Gauge('sunflower_cpu_usage_percent', 'CPU usage percentage', ['cpu'])
MEMORY_USAGE = Gauge('sunflower_memory_usage_bytes', 'Memory usage in bytes', ['type'])
DISK_USAGE = Gauge('sunflower_disk_usage_percent', 'Disk usage percentage', ['mount'])
NETWORK_TRAFFIC = Counter('sunflower_network_bytes_total', 'Network traffic in bytes', ['interface', 'direction'])
GPU_USAGE = Gauge('sunflower_gpu_usage_percent', 'GPU usage percentage', ['gpu_id'])
GPU_TEMPERATURE = Gauge('sunflower_gpu_temperature_celsius', 'GPU temperature in Celsius', ['gpu_id'])
GPU_MEMORY = Gauge('sunflower_gpu_memory_bytes', 'GPU memory usage in bytes', ['gpu_id'])
CACHE_HITS = Counter('sunflower_cache_hits_total', 'Cache hits', ['cache_type'])
CACHE_MISSES = Counter('sunflower_cache_misses_total', 'Cache misses', ['cache_type'])
AGENT_STATUS = Gauge('sunflower_agent_status', 'Agent status', ['agent_id', 'status'])
MODEL_LOAD = Gauge('sunflower_model_load_percent', 'Model load percentage', ['model_id'])
VOICE_PROCESSING = Histogram('sunflower_voice_processing_seconds', 'Voice processing duration', ['operation'])
BLOCKCHAIN_TX = Counter('sunflower_blockchain_transactions_total', 'Blockchain transactions', ['type', 'status'])
API_LATENCY = Histogram('sunflower_api_latency_seconds', 'API endpoint latency', ['endpoint'])
ERROR_COUNT = Counter('sunflower_errors_total', 'Error count', ['type', 'component'])
QUEUE_SIZE = Gauge('sunflower_queue_size', 'Queue size', ['queue_name'])
THREAD_COUNT = Gauge('sunflower_thread_count', 'Thread count')
FILE_HANDLES = Gauge('sunflower_file_handles', 'Open file handles')
SOCKET_CONNECTIONS = Gauge('sunflower_socket_connections', 'Active socket connections')
MEMORY_LEAKS = Gauge('sunflower_memory_leaks_bytes', 'Potential memory leaks in bytes')
RESPONSE_TIME = Histogram('sunflower_response_time_seconds', 'Response time distribution', ['endpoint'])
BANDWIDTH_USAGE = Counter('sunflower_bandwidth_bytes_total', 'Bandwidth usage', ['direction'])
DATABASE_CONNECTIONS = Gauge('sunflower_database_connections', 'Active database connections', ['database'])
CACHE_SIZE = Gauge('sunflower_cache_size_bytes', 'Cache size in bytes', ['cache_type'])
PROCESS_CPU = Gauge('sunflower_process_cpu_percent', 'Process CPU usage', ['process'])
PROCESS_MEMORY = Gauge('sunflower_process_memory_bytes', 'Process memory usage', ['process'])
PROCESS_THREADS = Gauge('sunflower_process_threads', 'Process thread count', ['process'])
PROCESS_HANDLES = Gauge('sunflower_process_handles', 'Process handle count', ['process'])
PROCESS_IO = Counter('sunflower_process_io_bytes', 'Process I/O operations', ['process', 'operation'])
PROCESS_NETWORK = Counter('sunflower_process_network_bytes', 'Process network usage', ['process', 'direction'])
PROCESS_DISK = Counter('sunflower_process_disk_bytes', 'Process disk usage', ['process', 'operation'])
PROCESS_GPU = Gauge('sunflower_process_gpu_percent', 'Process GPU usage', ['process', 'gpu_id'])
PROCESS_GPU_MEMORY = Gauge('sunflower_process_gpu_memory_bytes', 'Process GPU memory usage', ['process', 'gpu_id'])
PROCESS_GPU_TEMPERATURE = Gauge('sunflower_process_gpu_temperature_celsius', 'Process GPU temperature', ['process', 'gpu_id'])
PROCESS_GPU_POWER = Gauge('sunflower_process_gpu_power_watts', 'Process GPU power usage', ['process', 'gpu_id'])
PROCESS_GPU_FAN = Gauge('sunflower_process_gpu_fan_percent', 'Process GPU fan speed', ['process', 'gpu_id'])
PROCESS_GPU_CLOCK = Gauge('sunflower_process_gpu_clock_mhz', 'Process GPU clock speed', ['process', 'gpu_id'])
PROCESS_GPU_MEMORY_CLOCK = Gauge('sunflower_process_gpu_memory_clock_mhz', 'Process GPU memory clock speed', ['process', 'gpu_id'])
PROCESS_GPU_UTILIZATION = Gauge('sunflower_process_gpu_utilization_percent', 'Process GPU utilization', ['process', 'gpu_id'])
PROCESS_GPU_MEMORY_UTILIZATION = Gauge('sunflower_process_gpu_memory_utilization_percent', 'Process GPU memory utilization', ['process', 'gpu_id'])
PROCESS_GPU_TEMPERATURE_UTILIZATION = Gauge('sunflower_process_gpu_temperature_utilization_percent', 'Process GPU temperature utilization', ['process', 'gpu_id'])
PROCESS_GPU_POWER_UTILIZATION = Gauge('sunflower_process_gpu_power_utilization_percent', 'Process GPU power utilization', ['process', 'gpu_id'])
PROCESS_GPU_FAN_UTILIZATION = Gauge('sunflower_process_gpu_fan_utilization_percent', 'Process GPU fan utilization', ['process', 'gpu_id'])
PROCESS_GPU_CLOCK_UTILIZATION = Gauge('sunflower_process_gpu_clock_utilization_percent', 'Process GPU clock utilization', ['process', 'gpu_id'])
PROCESS_GPU_MEMORY_CLOCK_UTILIZATION = Gauge('sunflower_process_gpu_memory_clock_utilization_percent', 'Process GPU memory clock utilization', ['process', 'gpu_id'])

class SystemMonitor:
    def __init__(self, config_path: str = "config/monitoring.json"):
        """Initialize the system monitor."""
        self.config = self._load_config(config_path)
        self.alert_system = MonitoringAlert(config_path)
        self.metrics_history: List[Dict] = []
        self._ensure_directories()
        self._start_prometheus_server()

    def _ensure_directories(self):
        """Ensure required directories exist."""
        os.makedirs('logs', exist_ok=True)
        os.makedirs('exports/monitoring', exist_ok=True)

    def _load_config(self, config_path: str) -> Dict:
        """Load monitoring configuration."""
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load monitoring config: {e}")
            return {}

    def _start_prometheus_server(self):
        """Start Prometheus metrics server."""
        start_http_server(8000)

    def get_gpu_metrics(self) -> Dict:
        """Get current GPU metrics."""
        try:
            gpus = GPUtil.getGPUs()
            return {
                "gpus": [
                    {
                        "id": gpu.id,
                        "name": gpu.name,
                        "load": gpu.load * 100,
                        "memory_used": gpu.memoryUsed,
                        "memory_total": gpu.memoryTotal,
                        "temperature": gpu.temperature,
                        "power_draw": gpu.powerDraw if hasattr(gpu, 'powerDraw') else None
                    }
                    for gpu in gpus
                ]
            }
        except Exception as e:
            logger.error(f"Failed to get GPU metrics: {e}")
            return {"gpus": []}

    def get_system_metrics(self) -> Dict:
        """Get current system metrics."""
        try:
            cpu_usage = psutil.cpu_percent(interval=1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            network = psutil.net_io_counters()
            gpu_metrics = self.get_gpu_metrics()

            return {
                "cpu": {
                    "usage": cpu_usage,
                    "cores": psutil.cpu_count(),
                    "frequency": psutil.cpu_freq().current if psutil.cpu_freq() else None,
                    "temperature": self._get_cpu_temperature()
                },
                "memory": {
                    "total": memory.total,
                    "used": memory.used,
                    "free": memory.free,
                    "usage_percent": memory.percent,
                    "swap": {
                        "total": psutil.swap_memory().total,
                        "used": psutil.swap_memory().used,
                        "free": psutil.swap_memory().free,
                        "percent": psutil.swap_memory().percent
                    }
                },
                "disk": {
                    "total": disk.total,
                    "used": disk.used,
                    "free": disk.free,
                    "usage_percent": disk.percent,
                    "io": {
                        "read_bytes": psutil.disk_io_counters().read_bytes,
                        "write_bytes": psutil.disk_io_counters().write_bytes
                    }
                },
                "network": {
                    "bytes_sent": network.bytes_sent,
                    "bytes_recv": network.bytes_recv,
                    "packets_sent": network.packets_sent,
                    "packets_recv": network.packets_recv,
                    "connections": len(psutil.net_connections())
                },
                "gpu": gpu_metrics,
                "timestamp": datetime.utcnow().isoformat()
            }
        except Exception as e:
            logger.error(f"Failed to get system metrics: {e}")
            return {}

    def _get_cpu_temperature(self) -> Optional[float]:
        """Get CPU temperature if available."""
        try:
            temps = psutil.sensors_temperatures()
            if temps and 'coretemp' in temps:
                return sum(temp.current for temp in temps['coretemp']) / len(temps['coretemp'])
            return None
        except Exception:
            return None

    def get_model_metrics(self) -> Dict:
        """Get current model metrics."""
        try:
            # This is a placeholder - implement actual model metrics collection
            return {
                "models": [
                    {
                        "name": "local_model",
                        "status": "active",
                        "last_updated": datetime.utcnow().isoformat(),
                        "inference_time": 0.15,
                        "memory_usage": 1024,
                        "batch_size": 32,
                        "throughput": 100
                    }
                ]
            }
        except Exception as e:
            logger.error(f"Failed to get model metrics: {e}")
            return {}

    def cleanup_old_metrics(self):
        """Remove metrics older than the retention period."""
        retention_days = self.config.get('retention', {}).get('metrics', {}).get('days', 7)
        cutoff_date = datetime.utcnow() - timedelta(days=retention_days)
        
        self.metrics_history = [
            metric for metric in self.metrics_history
            if datetime.fromisoformat(metric['timestamp']) > cutoff_date
        ]

    def export_metrics(self):
        """Export metrics to file."""
        try:
            export_config = self.config.get('export', {})
            if not export_config.get('formats'):
                return

            timestamp = datetime.utcnow().strftime('%Y%m%d_%H%M%S')
            base_path = export_config.get('destination', 'exports/monitoring')

            for format in export_config['formats']:
                if format == 'json':
                    file_path = f"{base_path}/metrics_{timestamp}.json"
                    with open(file_path, 'w') as f:
                        json.dump(self.metrics_history, f, indent=2)
                elif format == 'csv':
                    file_path = f"{base_path}/metrics_{timestamp}.csv"
                    with open(file_path, 'w') as f:
                        # Write header
                        f.write("timestamp,cpu_usage,cpu_temp,memory_usage,disk_usage,gpu_usage\n")
                        # Write data
                        for metric in self.metrics_history:
                            gpu_usage = metric.get('gpu', {}).get('gpus', [{}])[0].get('load', 0)
                            f.write(
                                f"{metric['timestamp']},"
                                f"{metric['cpu']['usage']},"
                                f"{metric['cpu'].get('temperature', 'N/A')},"
                                f"{metric['memory']['usage_percent']},"
                                f"{metric['disk']['usage_percent']},"
                                f"{gpu_usage}\n"
                            )

            logger.info(f"Metrics exported to {base_path}")
        except Exception as e:
            logger.error(f"Failed to export metrics: {e}")

    async def monitor(self):
        """Main monitoring loop."""
        refresh_interval = self.config.get('refresh_interval', 30)
        
        while True:
            try:
                # Get current metrics
                system_metrics = self.get_system_metrics()
                model_metrics = self.get_model_metrics()
                
                # Store metrics
                self.metrics_history.append(system_metrics)
                
                # Process alerts
                self.alert_system.process_alerts(system_metrics)
                
                # Cleanup old metrics
                self.cleanup_old_metrics()
                
                # Export metrics if scheduled
                if datetime.utcnow().hour == 0 and datetime.utcnow().minute == 0:
                    self.export_metrics()
                
                # Wait for next interval
                await asyncio.sleep(refresh_interval)
                
            except Exception as e:
                logger.error(f"Error in monitoring loop: {e}")
                await asyncio.sleep(refresh_interval)

async def main():
    """Main entry point."""
    monitor = SystemMonitor()
    await monitor.monitor()

if __name__ == "__main__":
    asyncio.run(main()) 