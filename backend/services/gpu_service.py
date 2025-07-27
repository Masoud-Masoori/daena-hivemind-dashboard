"""
GPU Service for Daena AI System
Handles local GPU detection and cloud GPU routing
"""

import os
import logging
import asyncio
from typing import Dict, Optional, Any
from enum import Enum

logger = logging.getLogger(__name__)

class GPUProvider(str, Enum):
    LOCAL = "local"
    GCP = "gcp"
    AWS = "aws"
    AZURE = "azure"

class GPUService:
    def __init__(self):
        self.local_gpu_available = False
        self.cloud_gpu_available = False
        self.gcp_project_id = "daena-460722"
        self.current_load = 0
        self.setup_gpu_detection()
    
    def setup_gpu_detection(self):
        """Detect available GPU resources"""
        # Check for local GPU
        self.local_gpu_available = self._check_local_gpu()
        
        # Check for cloud GPU access
        self.cloud_gpu_available = self._check_cloud_gpu()
        
        logger.info(f"GPU Setup - Local: {self.local_gpu_available}, Cloud: {self.cloud_gpu_available}")
    
    def _check_local_gpu(self) -> bool:
        """Check if local GPU is available"""
        try:
            # Try PyTorch CUDA
            try:
                import torch
                if torch.cuda.is_available():
                    gpu_count = torch.cuda.device_count()
                    logger.info(f"Local GPU detected: {gpu_count} CUDA devices")
                    return True
            except ImportError:
                pass
            
            # Try TensorFlow GPU
            try:
                import tensorflow as tf
                gpus = tf.config.list_physical_devices('GPU')
                if gpus:
                    logger.info(f"Local GPU detected: {len(gpus)} TensorFlow devices")
                    return True
            except ImportError:
                pass
            
            # Check for NVIDIA GPU via nvidia-smi
            try:
                import subprocess
                result = subprocess.run(['nvidia-smi'], capture_output=True, text=True)
                if result.returncode == 0:
                    logger.info("Local GPU detected via nvidia-smi")
                    return True
            except (FileNotFoundError, subprocess.SubprocessError):
                pass
            
            logger.info("No local GPU detected")
            return False
            
        except Exception as e:
            logger.error(f"Error checking local GPU: {e}")
            return False
    
    def _check_cloud_gpu(self) -> bool:
        """Check if cloud GPU access is available"""
        try:
            # Check for GCP credentials
            gcp_credentials = os.getenv('GOOGLE_APPLICATION_CREDENTIALS')
            if gcp_credentials and os.path.exists(gcp_credentials):
                logger.info("GCP credentials found")
                return True
            
            # Check for service account key
            service_account_key = os.getenv('GCP_SERVICE_ACCOUNT_KEY')
            if service_account_key:
                logger.info("GCP service account key found")
                return True
            
            logger.info("No cloud GPU access configured")
            return False
            
        except Exception as e:
            logger.error(f"Error checking cloud GPU: {e}")
            return False
    
    def get_optimal_gpu_provider(self, task_type: str, task_size: str = "medium") -> GPUProvider:
        """Determine optimal GPU provider based on task and current load"""
        # Update current load
        self.current_load = self._get_current_load()
        
        # For small tasks, prefer local if available
        if task_size == "small" and self.local_gpu_available:
            return GPUProvider.LOCAL
        
        # For large tasks or high load, prefer cloud
        if task_size == "large" or self.current_load > 80:
            if self.cloud_gpu_available:
                return GPUProvider.GCP
            elif self.local_gpu_available:
                return GPUProvider.LOCAL
        
        # For synthesis tasks, prefer cloud for better models
        if task_type == "synthesis" and self.cloud_gpu_available:
            return GPUProvider.GCP
        
        # Default to local if available
        if self.local_gpu_available:
            return GPUProvider.LOCAL
        
        # Fallback to cloud
        if self.cloud_gpu_available:
            return GPUProvider.GCP
        
        return None
    
    def _get_current_load(self) -> int:
        """Get current system load (mock implementation)"""
        try:
            import psutil
            return int(psutil.cpu_percent())
        except ImportError:
            # Mock load if psutil not available
            import random
            return random.randint(20, 90)
    
    async def route_task_to_gpu(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Route task to appropriate GPU provider"""
        task_type = task_data.get("type", "general")
        task_size = task_data.get("size", "medium")
        
        provider = self.get_optimal_gpu_provider(task_type, task_size)
        
        if provider == GPUProvider.LOCAL:
            return await self._execute_local_gpu_task(task_data)
        elif provider == GPUProvider.GCP:
            return await self._execute_cloud_gpu_task(task_data)
        else:
            # Fallback to CPU
            return await self._execute_cpu_task(task_data)
    
    async def _execute_local_gpu_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task on local GPU"""
        try:
            logger.info(f"Executing task on local GPU: {task_data.get('name', 'Unknown')}")
            
            # Mock local GPU execution
            await asyncio.sleep(1)  # Simulate processing time
            
            return {
                "success": True,
                "provider": "local_gpu",
                "execution_time": 1.0,
                "result": f"Local GPU task completed: {task_data.get('name', 'Unknown')}",
                "gpu_utilization": 75
            }
            
        except Exception as e:
            logger.error(f"Local GPU task failed: {e}")
            return {
                "success": False,
                "provider": "local_gpu",
                "error": str(e)
            }
    
    async def _execute_cloud_gpu_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task on cloud GPU (GCP)"""
        try:
            logger.info(f"Executing task on cloud GPU: {task_data.get('name', 'Unknown')}")
            
            # Mock cloud GPU execution
            await asyncio.sleep(2)  # Simulate network latency + processing
            
            return {
                "success": True,
                "provider": "gcp_gpu",
                "execution_time": 2.0,
                "result": f"Cloud GPU task completed: {task_data.get('name', 'Unknown')}",
                "gpu_type": "A100",
                "cost": 0.15  # Mock cost in USD
            }
            
        except Exception as e:
            logger.error(f"Cloud GPU task failed: {e}")
            return {
                "success": False,
                "provider": "gcp_gpu",
                "error": str(e)
            }
    
    async def _execute_cpu_task(self, task_data: Dict[str, Any]) -> Dict[str, Any]:
        """Execute task on CPU (fallback)"""
        try:
            logger.info(f"Executing task on CPU: {task_data.get('name', 'Unknown')}")
            
            # Mock CPU execution
            await asyncio.sleep(3)  # Simulate slower CPU processing
            
            return {
                "success": True,
                "provider": "cpu",
                "execution_time": 3.0,
                "result": f"CPU task completed: {task_data.get('name', 'Unknown')}",
                "cpu_utilization": 85
            }
            
        except Exception as e:
            logger.error(f"CPU task failed: {e}")
            return {
                "success": False,
                "provider": "cpu",
                "error": str(e)
            }
    
    def get_gpu_status(self) -> Dict[str, Any]:
        """Get current GPU status"""
        return {
            "local_gpu_available": self.local_gpu_available,
            "cloud_gpu_available": self.cloud_gpu_available,
            "current_load": self.current_load,
            "gcp_project_id": self.gcp_project_id,
            "optimal_provider": self.get_optimal_gpu_provider("general", "medium")
        }
    
    async def setup_cloud_gpu(self) -> bool:
        """Setup cloud GPU infrastructure"""
        try:
            if not self.cloud_gpu_available:
                logger.warning("Cloud GPU not configured")
                return False
            
            # Mock cloud GPU setup
            logger.info("Setting up cloud GPU infrastructure...")
            await asyncio.sleep(1)
            
            logger.info("Cloud GPU setup completed")
            return True
            
        except Exception as e:
            logger.error(f"Cloud GPU setup failed: {e}")
            return False

# Global GPU service instance
gpu_service = GPUService() 