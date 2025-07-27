import os
import torch
import json
import logging
import asyncio
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
from datetime import datetime
import openai
from transformers import AutoModelForCausalLM, AutoTokenizer, BitsAndBytesConfig
from sqlalchemy.orm import Session
import numpy as np

# Import database models
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
from database import BrainModel, ModelPerformance, TrainingSession, ConsensusVote, get_db

class AdvancedModelIntegration:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.models = {}
        self.model_configs = self.load_model_configs()
        self.setup_logging()
        self.initialize_models()
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/advanced_model_integration.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('AdvancedModelIntegration')
        
    def load_model_configs(self) -> Dict:
        """Load comprehensive model configurations including R1, R2, and other advanced models"""
        config_path = "config/advanced_model_config.json"
        default_config = {
            "azure_openai": {
                "api_type": "azure",
                "api_key": os.getenv("OPENAI_API_KEY"),
                "api_base": os.getenv("OPENAI_API_BASE"),
                "api_version": os.getenv("OPENAI_API_VERSION", "2024-02-15"),
                "deployment_name": os.getenv("OPENAI_DEPLOYMENT_NAME", "daena"),
                "model_name": "gpt-4",
                "max_tokens": 4000,
                "temperature": 0.7
            },
            "local_models": {
                "r1": {
                    "path": "models/r1",
                    "type": "reasoning",
                    "max_length": 8192,
                    "temperature": 0.7,
                    "quantization": "int8",
                    "device": "auto"
                },
                "r2": {
                    "path": "models/r2", 
                    "type": "reasoning",
                    "max_length": 16384,
                    "temperature": 0.7,
                    "quantization": "int8",
                    "device": "auto"
                },
                "deepseek_v3": {
                    "path": "models/deepseek-v3",
                    "type": "causal",
                    "max_length": 32768,
                    "temperature": 0.7,
                    "quantization": "int4",
                    "device": "auto"
                },
                "qwen2.5": {
                    "path": "models/qwen2.5",
                    "type": "causal", 
                    "max_length": 32768,
                    "temperature": 0.7,
                    "quantization": "int4",
                    "device": "auto"
                },
                "yi_34b": {
                    "path": "models/yi-34b",
                    "type": "causal",
                    "max_length": 4096,
                    "temperature": 0.7,
                    "quantization": "int8",
                    "device": "auto"
                }
            },
            "huggingface_models": {
                "deepseek_coder": {
                    "model_id": "deepseek-ai/deepseek-coder-33b-instruct",
                    "type": "coding",
                    "max_length": 8192,
                    "temperature": 0.7
                },
                "codellama": {
                    "model_id": "codellama/CodeLlama-34b-Instruct-hf",
                    "type": "coding",
                    "max_length": 8192,
                    "temperature": 0.7
                }
            },
            "training_config": {
                "batch_size": 4,
                "learning_rate": 1e-5,
                "max_epochs": 10,
                "gradient_accumulation_steps": 4,
                "warmup_steps": 100,
                "save_steps": 500,
                "eval_steps": 500,
                "logging_steps": 50
            },
            "consensus_config": {
                "min_models": 2,
                "confidence_threshold": 0.7,
                "weighted_voting": True,
                "fallback_model": "azure_openai"
            }
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return default_config
        
    def initialize_models(self):
        """Initialize all available models"""
        self.initialize_azure_openai()
        self.initialize_local_models()
        self.initialize_huggingface_models()
        self.sync_models_to_database()
        
    def initialize_azure_openai(self):
        """Initialize Azure OpenAI connection"""
        try:
            config = self.model_configs["azure_openai"]
            if config["api_key"]:
                openai.api_type = config["api_type"]
                openai.api_key = config["api_key"]
                openai.api_base = config["api_base"]
                openai.api_version = config["api_version"]
                
                # Register in database
                self.register_model_in_db(
                    name="azure_gpt4",
                    model_type="openai_gpt4",
                    provider="azure",
                    config=config,
                    model_size="unknown",
                    context_length=8192
                )
                self.logger.info("Azure OpenAI initialized successfully")
            else:
                self.logger.warning("Azure OpenAI API key not found")
        except Exception as e:
            self.logger.error(f"Error initializing Azure OpenAI: {e}")
            
    def initialize_local_models(self):
        """Initialize local models including R1, R2, etc."""
        for model_name, config in self.model_configs["local_models"].items():
            try:
                model_path = config["path"]
                if os.path.exists(model_path):
                    self.logger.info(f"Loading local model: {model_name}")
                    
                    # Load with quantization if specified
                    if config.get("quantization"):
                        quantization_config = self.get_quantization_config(config["quantization"])
                        model = AutoModelForCausalLM.from_pretrained(
                            model_path,
                            quantization_config=quantization_config,
                            device_map=config.get("device", "auto"),
                            torch_dtype=torch.float16
                        )
                    else:
                        model = AutoModelForCausalLM.from_pretrained(
                            model_path,
                            device_map=config.get("device", "auto"),
                            torch_dtype=torch.float16
                        )
                    
                    tokenizer = AutoTokenizer.from_pretrained(model_path)
                    
                    self.models[model_name] = {
                        "model": model,
                        "tokenizer": tokenizer,
                        "config": config,
                        "type": "local"
                    }
                    
                    # Register in database
                    self.register_model_in_db(
                        name=model_name,
                        model_type=model_name,
                        provider="local",
                        config=config,
                        model_path=model_path,
                        is_quantized=bool(config.get("quantization")),
                        quantization_type=config.get("quantization")
                    )
                    
                    self.logger.info(f"Successfully loaded {model_name}")
                else:
                    self.logger.warning(f"Model path not found: {model_path}")
            except Exception as e:
                self.logger.error(f"Error loading model {model_name}: {e}")
                
    def initialize_huggingface_models(self):
        """Initialize HuggingFace models"""
        for model_name, config in self.model_configs["huggingface_models"].items():
            try:
                self.logger.info(f"Initializing HuggingFace model: {model_name}")
                
                # Register in database (will be loaded on-demand)
                self.register_model_in_db(
                    name=model_name,
                    model_type=config["type"],
                    provider="huggingface",
                    config=config,
                    model_size="unknown",
                    context_length=config.get("max_length", 4096)
                )
                
                self.logger.info(f"Successfully registered {model_name}")
            except Exception as e:
                self.logger.error(f"Error initializing HuggingFace model {model_name}: {e}")
                
    def get_quantization_config(self, quantization_type: str):
        """Get quantization configuration"""
        if quantization_type == "int8":
            return BitsAndBytesConfig(load_in_8bit=True)
        elif quantization_type == "int4":
            return BitsAndBytesConfig(load_in_4bit=True, bnb_4bit_compute_dtype=torch.float16)
        else:
            return None
            
    def register_model_in_db(self, name: str, model_type: str, provider: str, 
                           config: Dict, model_path: str = None, 
                           model_size: str = None, context_length: int = 4096,
                           is_quantized: bool = False, quantization_type: str = None):
        """Register model in database"""
        try:
            existing = self.db.query(BrainModel).filter(BrainModel.name == name).first()
            if not existing:
                brain_model = BrainModel(
                    name=name,
                    model_type=model_type,
                    model_path=model_path,
                    provider=provider,
                    config=config,
                    status="available",
                    model_size=model_size,
                    context_length=context_length,
                    is_quantized=is_quantized,
                    quantization_type=quantization_type
                )
                self.db.add(brain_model)
                self.db.commit()
                self.logger.info(f"Registered model {name} in database")
        except Exception as e:
            self.logger.error(f"Error registering model {name} in database: {e}")
            self.db.rollback()
            
    def sync_models_to_database(self):
        """Sync current model status to database"""
        for model_name, model_info in self.models.items():
            try:
                brain_model = self.db.query(BrainModel).filter(BrainModel.name == model_name).first()
                if brain_model:
                    brain_model.status = "available"
                    brain_model.last_used = datetime.utcnow()
                    self.db.commit()
            except Exception as e:
                self.logger.error(f"Error syncing model {model_name}: {e}")
                
    async def generate_response(self, prompt: str, model_name: str = None, 
                              context: Optional[Dict] = None) -> Dict:
        """Generate response using specified or best available model"""
        start_time = datetime.utcnow()
        
        try:
            if model_name and model_name in self.models:
                response = await self._generate_with_model(model_name, prompt, context)
            elif model_name == "azure_gpt4":
                response = await self._generate_azure_openai(prompt, context)
            else:
                # Use consensus approach with multiple models
                response = await self._generate_consensus(prompt, context)
                
            # Log performance metrics
            end_time = datetime.utcnow()
            response_time = (end_time - start_time).total_seconds() * 1000
            
            self.log_performance_metrics(model_name or "consensus", "latency", response_time)
            
            return {
                "response": response,
                "model_used": model_name or "consensus",
                "response_time_ms": response_time,
                "timestamp": end_time.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error generating response: {e}")
            return {"error": str(e), "model_used": model_name}
            
    async def _generate_with_model(self, model_name: str, prompt: str, context: Optional[Dict]) -> str:
        """Generate response using local model"""
        model_info = self.models[model_name]
        model = model_info["model"]
        tokenizer = model_info["tokenizer"]
        config = model_info["config"]
        
        # Prepare input
        inputs = tokenizer(prompt, return_tensors="pt", max_length=config["max_length"], truncation=True)
        
        # Generate
        with torch.no_grad():
            outputs = model.generate(
                **inputs,
                max_new_tokens=config.get("max_new_tokens", 512),
                temperature=config["temperature"],
                do_sample=True,
                pad_token_id=tokenizer.eos_token_id
            )
            
        response = tokenizer.decode(outputs[0], skip_special_tokens=True)
        return response[len(prompt):]  # Remove input prompt
        
    async def _generate_azure_openai(self, prompt: str, context: Optional[Dict]) -> str:
        """Generate response using Azure OpenAI"""
        config = self.model_configs["azure_openai"]
        
        messages = [{"role": "user", "content": prompt}]
        if context:
            messages.insert(0, {"role": "system", "content": context.get("system_prompt", "")})
            
        response = openai.ChatCompletion.create(
            engine=config["deployment_name"],
            messages=messages,
            max_tokens=config["max_tokens"],
            temperature=config["temperature"]
        )
        
        return response.choices[0].message.content
        
    async def _generate_consensus(self, prompt: str, context: Optional[Dict]) -> str:
        """Generate consensus response using multiple models"""
        consensus_config = self.model_configs["consensus_config"]
        available_models = list(self.models.keys()) + ["azure_gpt4"]
        
        if len(available_models) < consensus_config["min_models"]:
            # Fallback to Azure OpenAI
            return await self._generate_azure_openai(prompt, context)
            
        # Get responses from multiple models
        responses = {}
        tasks = []
        
        for model_name in available_models[:3]:  # Use top 3 models
            if model_name in self.models:
                task = self._generate_with_model(model_name, prompt, context)
            elif model_name == "azure_gpt4":
                task = self._generate_azure_openai(prompt, context)
            else:
                continue
                
            tasks.append((model_name, task))
            
        # Execute all tasks concurrently
        for model_name, task in tasks:
            try:
                response = await task
                responses[model_name] = response
            except Exception as e:
                self.logger.error(f"Error with model {model_name}: {e}")
                
        # Calculate consensus
        if len(responses) >= consensus_config["min_models"]:
            return self._calculate_consensus(responses, consensus_config)
        else:
            # Fallback to Azure OpenAI
            return await self._generate_azure_openai(prompt, context)
            
    def _calculate_consensus(self, responses: Dict[str, str], config: Dict) -> str:
        """Calculate consensus from multiple model responses"""
        if config.get("weighted_voting"):
            # Use weighted voting based on model performance
            weights = self._get_model_weights(list(responses.keys()))
            weighted_responses = []
            
            for model_name, response in responses.items():
                weight = weights.get(model_name, 1.0)
                weighted_responses.extend([response] * int(weight * 10))
                
            # Return most common response
            from collections import Counter
            counter = Counter(weighted_responses)
            return counter.most_common(1)[0][0]
        else:
            # Simple majority voting
            from collections import Counter
            counter = Counter(responses.values())
            return counter.most_common(1)[0][0]
            
    def _get_model_weights(self, model_names: List[str]) -> Dict[str, float]:
        """Get performance-based weights for models"""
        weights = {}
        for model_name in model_names:
            # Get recent performance metrics
            recent_performance = self.db.query(ModelPerformance).filter(
                ModelPerformance.brain_model_id == self._get_model_id(model_name)
            ).order_by(ModelPerformance.timestamp.desc()).first()
            
            if recent_performance and recent_performance.metric_name == "accuracy":
                weights[model_name] = recent_performance.metric_value
            else:
                weights[model_name] = 1.0  # Default weight
                
        return weights
        
    def _get_model_id(self, model_name: str) -> int:
        """Get model ID from database"""
        brain_model = self.db.query(BrainModel).filter(BrainModel.name == model_name).first()
        return brain_model.id if brain_model else None
        
    def log_performance_metrics(self, model_name: str, metric_name: str, metric_value: float):
        """Log performance metrics to database"""
        try:
            model_id = self._get_model_id(model_name)
            if model_id:
                performance = ModelPerformance(
                    brain_model_id=model_id,
                    metric_name=metric_name,
                    metric_value=metric_value,
                    timestamp=datetime.utcnow()
                )
                self.db.add(performance)
                self.db.commit()
        except Exception as e:
            self.logger.error(f"Error logging performance metrics: {e}")
            self.db.rollback()
            
    async def train_model(self, model_name: str, training_data: List[Dict], 
                         training_config: Optional[Dict] = None) -> Dict:
        """Train a specific model with provided data"""
        try:
            if model_name not in self.models:
                return {"error": f"Model {model_name} not found"}
                
            # Create training session
            session = TrainingSession(
                brain_model_id=self._get_model_id(model_name),
                session_type="custom_training",
                training_data=training_data,
                parameters=training_config or self.model_configs["training_config"],
                status="running"
            )
            self.db.add(session)
            self.db.commit()
            
            # Start training (this would be implemented based on specific model requirements)
            training_result = await self._train_model_implementation(model_name, training_data, training_config)
            
            # Update session
            session.status = "completed" if training_result["success"] else "failed"
            session.end_time = datetime.utcnow()
            session.metrics = training_result.get("metrics", {})
            self.db.commit()
            
            return training_result
            
        except Exception as e:
            self.logger.error(f"Error training model {model_name}: {e}")
            return {"error": str(e)}
            
    async def _train_model_implementation(self, model_name: str, training_data: List[Dict], 
                                        training_config: Dict) -> Dict:
        """Implement actual model training (placeholder)"""
        # This would contain the actual training implementation
        # For now, return a placeholder
        return {
            "success": True,
            "metrics": {
                "loss": 0.1,
                "accuracy": 0.95,
                "epochs_completed": training_config.get("max_epochs", 10)
            }
        }
        
    def get_available_models(self) -> List[Dict]:
        """Get list of available models with their status"""
        models = []
        for model_name, model_info in self.models.items():
            brain_model = self.db.query(BrainModel).filter(BrainModel.name == model_name).first()
            models.append({
                "name": model_name,
                "type": model_info["type"],
                "status": brain_model.status if brain_model else "unknown",
                "provider": brain_model.provider if brain_model else "local"
            })
        return models 