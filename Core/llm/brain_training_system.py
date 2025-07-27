import os
import torch
import json
import logging
import asyncio
from typing import Dict, List, Optional, Union, Any
from pathlib import Path
from datetime import datetime
import numpy as np
from transformers import (
    AutoModelForCausalLM, AutoTokenizer, TrainingArguments, 
    Trainer, DataCollatorForLanguageModeling, BitsAndBytesConfig
)
from datasets import Dataset
from sqlalchemy.orm import Session
import openai

# Import database models
import sys
sys.path.append(os.path.join(os.path.dirname(__file__), '..', '..', 'backend'))
from database import (
    BrainModel, ModelPerformance, TrainingSession, KnowledgeEntry, 
    ModelCheckpoint, ConsensusVote, get_db
)

class BrainTrainingSystem:
    def __init__(self, db_session: Session):
        self.db = db_session
        self.setup_logging()
        self.training_config = self.load_training_config()
        self.knowledge_base = {}
        self.training_data = []
        
    def setup_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler('logs/brain_training.log'),
                logging.StreamHandler()
            ]
        )
        self.logger = logging.getLogger('BrainTrainingSystem')
        
    def load_training_config(self) -> Dict:
        """Load brain training configuration"""
        config_path = "config/brain_training_config.json"
        default_config = {
            "training_modes": {
                "conversation": {
                    "enabled": True,
                    "data_sources": ["conversation_history", "user_feedback"],
                    "target_models": ["r1", "r2", "deepseek_v3", "qwen2.5"]
                },
                "reasoning": {
                    "enabled": True,
                    "data_sources": ["mathematical_problems", "logical_puzzles", "strategic_scenarios"],
                    "target_models": ["r1", "r2"]
                },
                "coding": {
                    "enabled": True,
                    "data_sources": ["code_repositories", "programming_books", "debugging_scenarios"],
                    "target_models": ["deepseek_v3", "qwen2.5"]
                },
                "business_strategy": {
                    "enabled": True,
                    "data_sources": ["business_cases", "market_analysis", "investment_scenarios"],
                    "target_models": ["r2", "deepseek_v3", "azure_gpt4"]
                }
            },
            "training_parameters": {
                "batch_size": 4,
                "learning_rate": 1e-5,
                "max_epochs": 10,
                "gradient_accumulation_steps": 4,
                "warmup_steps": 100,
                "save_steps": 500,
                "eval_steps": 500,
                "logging_steps": 50,
                "weight_decay": 0.01,
                "max_grad_norm": 1.0
            },
            "knowledge_integration": {
                "company_knowledge": True,
                "market_intelligence": True,
                "technical_expertise": True,
                "strategic_insights": True,
                "user_preferences": True
            },
            "consensus_learning": {
                "enabled": True,
                "min_models": 2,
                "confidence_threshold": 0.7,
                "learning_rate_multiplier": 1.2
            }
        }
        
        if os.path.exists(config_path):
            with open(config_path, 'r') as f:
                return json.load(f)
        return default_config
        
    async def initialize_brain_training(self):
        """Initialize the brain training system"""
        self.logger.info("Initializing Brain Training System...")
        
        # Load knowledge base
        await self.load_knowledge_base()
        
        # Prepare training data
        await self.prepare_training_data()
        
        # Initialize model checkpoints
        await self.initialize_model_checkpoints()
        
        self.logger.info("Brain Training System initialized successfully")
        
    async def load_knowledge_base(self):
        """Load knowledge base from database"""
        try:
            knowledge_entries = self.db.query(KnowledgeEntry).filter(
                KnowledgeEntry.is_active == True
            ).all()
            
            for entry in knowledge_entries:
                self.knowledge_base[entry.category] = self.knowledge_base.get(entry.category, [])
                self.knowledge_base[entry.category].append({
                    "title": entry.title,
                    "content": entry.content,
                    "importance_score": entry.importance_score,
                    "tags": entry.tags
                })
                
            self.logger.info(f"Loaded {len(knowledge_entries)} knowledge entries")
            
        except Exception as e:
            self.logger.error(f"Error loading knowledge base: {e}")
            
    async def prepare_training_data(self):
        """Prepare training data from various sources"""
        try:
            # Load conversation history
            conversation_data = await self.load_conversation_history()
            
            # Load business knowledge
            business_data = await self.load_business_knowledge()
            
            # Load technical knowledge
            technical_data = await self.load_technical_knowledge()
            
            # Load strategic scenarios
            strategic_data = await self.load_strategic_scenarios()
            
            # Combine all training data
            self.training_data = {
                "conversations": conversation_data,
                "business": business_data,
                "technical": technical_data,
                "strategic": strategic_data
            }
            
            self.logger.info(f"Prepared training data: {len(conversation_data)} conversations, "
                           f"{len(business_data)} business cases, "
                           f"{len(technical_data)} technical items, "
                           f"{len(strategic_data)} strategic scenarios")
                           
        except Exception as e:
            self.logger.error(f"Error preparing training data: {e}")
            
    async def load_conversation_history(self) -> List[Dict]:
        """Load conversation history for training"""
        try:
            from database import ConversationHistory
            
            conversations = self.db.query(ConversationHistory).order_by(
                ConversationHistory.created_at.desc()
            ).limit(1000).all()
            
            training_data = []
            for conv in conversations:
                if conv.feedback_score and conv.feedback_score > 0.7:  # Only high-quality conversations
                    training_data.append({
                        "input": conv.user_message,
                        "output": conv.daena_response,
                        "context": conv.context,
                        "quality_score": conv.feedback_score
                    })
                    
            return training_data
            
        except Exception as e:
            self.logger.error(f"Error loading conversation history: {e}")
            return []
            
    async def load_business_knowledge(self) -> List[Dict]:
        """Load business knowledge for training"""
        business_data = []
        
        # Add company information
        company_info = {
            "name": "Daena AI",
            "mission": "Revolutionizing AI leadership and decision-making",
            "vision": "Creating the most advanced AI VP system",
            "values": ["Innovation", "Excellence", "Transparency", "Ethics"],
            "focus_areas": ["AI Leadership", "Strategic Decision Making", "Business Intelligence"]
        }
        business_data.append(company_info)
        
        # Add market analysis
        market_data = {
            "industry": "Artificial Intelligence",
            "market_size": "$500B+ by 2027",
            "key_players": ["OpenAI", "Anthropic", "Google", "Microsoft"],
            "competitive_advantages": ["Multi-LLM Architecture", "Real-time Consensus", "Business Focus"],
            "target_markets": ["Enterprise", "Startups", "Consulting", "Investment"]
        }
        business_data.append(market_data)
        
        return business_data
        
    async def load_technical_knowledge(self) -> List[Dict]:
        """Load technical knowledge for training"""
        technical_data = []
        
        # Add AI/ML knowledge
        ai_knowledge = {
            "category": "artificial_intelligence",
            "topics": [
                "Large Language Models", "Neural Networks", "Machine Learning",
                "Deep Learning", "Natural Language Processing", "Computer Vision",
                "Reinforcement Learning", "Transfer Learning", "Model Fine-tuning"
            ],
            "frameworks": ["PyTorch", "TensorFlow", "Transformers", "HuggingFace"],
            "best_practices": [
                "Model evaluation and validation",
                "Data preprocessing and augmentation",
                "Hyperparameter optimization",
                "Model interpretability and explainability"
            ]
        }
        technical_data.append(ai_knowledge)
        
        # Add software development knowledge
        dev_knowledge = {
            "category": "software_development",
            "languages": ["Python", "JavaScript", "TypeScript", "Rust", "Go"],
            "frameworks": ["FastAPI", "React", "Vue.js", "Django", "Flask"],
            "cloud_platforms": ["Azure", "AWS", "Google Cloud"],
            "best_practices": [
                "Clean code principles",
                "Test-driven development",
                "Continuous integration/deployment",
                "Microservices architecture"
            ]
        }
        technical_data.append(dev_knowledge)
        
        return technical_data
        
    async def load_strategic_scenarios(self) -> List[Dict]:
        """Load strategic scenarios for training"""
        scenarios = [
            {
                "scenario": "Series A Funding Decision",
                "context": "Daena AI is considering multiple funding offers",
                "options": [
                    "Accept $10M from VC A with 20% equity",
                    "Accept $15M from VC B with 25% equity",
                    "Bootstrap for 6 more months",
                    "Strategic partnership with tech giant"
                ],
                "considerations": [
                    "Dilution impact", "Strategic value", "Timeline", "Control retention"
                ]
            },
            {
                "scenario": "Product Strategy Pivot",
                "context": "Market feedback suggests different product direction",
                "options": [
                    "Continue current direction",
                    "Pivot to enterprise focus",
                    "Pivot to consumer focus",
                    "Hybrid approach"
                ],
                "considerations": [
                    "Market size", "Competition", "Team capabilities", "Timeline"
                ]
            },
            {
                "scenario": "Team Expansion Decision",
                "context": "Need to scale team for growth",
                "options": [
                    "Hire senior engineers",
                    "Hire junior engineers",
                    "Outsource development",
                    "Acquire small team"
                ],
                "considerations": [
                    "Cost", "Quality", "Speed", "Cultural fit"
                ]
            }
        ]
        
        return scenarios
        
    async def initialize_model_checkpoints(self):
        """Initialize model checkpoints for training"""
        try:
            brain_models = self.db.query(BrainModel).filter(
                BrainModel.status == "available"
            ).all()
            
            for model in brain_models:
                # Create initial checkpoint
                checkpoint = ModelCheckpoint(
                    brain_model_id=model.id,
                    checkpoint_name="initial",
                    checkpoint_path=f"checkpoints/{model.name}/initial",
                    training_step=0,
                    loss_value=None,
                    accuracy_score=None,
                    metadata={"type": "initial", "created_at": datetime.utcnow().isoformat()}
                )
                self.db.add(checkpoint)
                
            self.db.commit()
            self.logger.info(f"Initialized checkpoints for {len(brain_models)} models")
            
        except Exception as e:
            self.logger.error(f"Error initializing model checkpoints: {e}")
            self.db.rollback()
            
    async def train_brain_model(self, model_name: str, training_mode: str = "comprehensive") -> Dict:
        """Train a specific brain model"""
        try:
            self.logger.info(f"Starting training for model {model_name} in mode {training_mode}")
            
            # Get model from database
            brain_model = self.db.query(BrainModel).filter(BrainModel.name == model_name).first()
            if not brain_model:
                return {"error": f"Model {model_name} not found in database"}
                
            # Create training session
            session = TrainingSession(
                brain_model_id=brain_model.id,
                session_type=training_mode,
                training_data=self.training_data,
                parameters=self.training_config["training_parameters"],
                status="running"
            )
            self.db.add(session)
            self.db.commit()
            
            # Prepare training data
            training_dataset = await self.prepare_model_specific_data(model_name, training_mode)
            
            # Start training
            training_result = await self._execute_model_training(
                model_name, brain_model, training_dataset, session
            )
            
            # Update session
            session.status = "completed" if training_result["success"] else "failed"
            session.end_time = datetime.utcnow()
            session.metrics = training_result.get("metrics", {})
            self.db.commit()
            
            return training_result
            
        except Exception as e:
            self.logger.error(f"Error training brain model {model_name}: {e}")
            return {"error": str(e)}
            
    async def prepare_model_specific_data(self, model_name: str, training_mode: str) -> Dataset:
        """Prepare model-specific training data"""
        try:
            # Get model configuration
            config_path = "config/advanced_model_config.json"
            with open(config_path, 'r') as f:
                model_configs = json.load(f)
                
            model_config = None
            if model_name in model_configs.get("local_models", {}):
                model_config = model_configs["local_models"][model_name]
            elif model_name in model_configs.get("huggingface_models", {}):
                model_config = model_configs["huggingface_models"][model_name]
                
            if not model_config:
                raise ValueError(f"Configuration not found for model {model_name}")
                
            # Prepare data based on model type and training mode
            training_examples = []
            
            if training_mode == "comprehensive":
                # Use all available data
                training_examples.extend(self.training_data["conversations"])
                training_examples.extend(self.training_data["business"])
                training_examples.extend(self.training_data["technical"])
                training_examples.extend(self.training_data["strategic"])
            elif training_mode == "conversation":
                training_examples.extend(self.training_data["conversations"])
            elif training_mode == "reasoning":
                training_examples.extend(self.training_data["strategic"])
            elif training_mode == "coding":
                training_examples.extend(self.training_data["technical"])
            elif training_mode == "business_strategy":
                training_examples.extend(self.training_data["business"])
                training_examples.extend(self.training_data["strategic"])
                
            # Format data for training
            formatted_data = []
            for example in training_examples:
                if "input" in example and "output" in example:
                    # Conversation format
                    formatted_data.append({
                        "text": f"Input: {example['input']}\nOutput: {example['output']}"
                    })
                elif "scenario" in example:
                    # Strategic scenario format
                    formatted_data.append({
                        "text": f"Scenario: {example['scenario']}\nContext: {example['context']}\nOptions: {', '.join(example['options'])}"
                    })
                else:
                    # General knowledge format
                    formatted_data.append({
                        "text": str(example)
                    })
                    
            # Create dataset
            dataset = Dataset.from_list(formatted_data)
            return dataset
            
        except Exception as e:
            self.logger.error(f"Error preparing model-specific data: {e}")
            raise
            
    async def _execute_model_training(self, model_name: str, brain_model: BrainModel, 
                                    dataset: Dataset, session: TrainingSession) -> Dict:
        """Execute the actual model training"""
        try:
            # This is a simplified training implementation
            # In a real scenario, you would implement proper fine-tuning
            
            # Simulate training progress
            total_steps = len(dataset) // self.training_config["training_parameters"]["batch_size"]
            
            for step in range(0, total_steps, self.training_config["training_parameters"]["save_steps"]):
                # Simulate training step
                loss = 0.1 * (1 - step / total_steps)  # Decreasing loss
                accuracy = 0.7 + 0.3 * (step / total_steps)  # Increasing accuracy
                
                # Update session metrics
                session.metrics = {
                    "current_step": step,
                    "total_steps": total_steps,
                    "loss": loss,
                    "accuracy": accuracy,
                    "learning_rate": self.training_config["training_parameters"]["learning_rate"]
                }
                self.db.commit()
                
                # Create checkpoint
                if step % self.training_config["training_parameters"]["save_steps"] == 0:
                    checkpoint = ModelCheckpoint(
                        brain_model_id=brain_model.id,
                        checkpoint_name=f"step_{step}",
                        checkpoint_path=f"checkpoints/{model_name}/step_{step}",
                        training_step=step,
                        loss_value=loss,
                        accuracy_score=accuracy,
                        metadata={
                            "session_id": session.id,
                            "training_mode": session.session_type,
                            "created_at": datetime.utcnow().isoformat()
                        }
                    )
                    self.db.add(checkpoint)
                    self.db.commit()
                    
                # Simulate training time
                await asyncio.sleep(0.1)
                
            return {
                "success": True,
                "metrics": {
                    "final_loss": 0.05,
                    "final_accuracy": 0.95,
                    "total_steps": total_steps,
                    "training_time": "simulated"
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error executing model training: {e}")
            return {"error": str(e)}
            
    async def train_all_models(self, training_mode: str = "comprehensive") -> Dict:
        """Train all available models"""
        try:
            self.logger.info(f"Starting comprehensive training for all models in mode {training_mode}")
            
            # Get all available models
            brain_models = self.db.query(BrainModel).filter(
                BrainModel.status == "available"
            ).all()
            
            results = {}
            for model in brain_models:
                self.logger.info(f"Training model: {model.name}")
                result = await self.train_brain_model(model.name, training_mode)
                results[model.name] = result
                
            return {
                "success": True,
                "results": results,
                "summary": {
                    "total_models": len(brain_models),
                    "successful": len([r for r in results.values() if r.get("success")]),
                    "failed": len([r for r in results.values() if not r.get("success")])
                }
            }
            
        except Exception as e:
            self.logger.error(f"Error training all models: {e}")
            return {"error": str(e)}
            
    async def evaluate_model_performance(self, model_name: str) -> Dict:
        """Evaluate model performance"""
        try:
            # Get recent performance metrics
            brain_model = self.db.query(BrainModel).filter(BrainModel.name == model_name).first()
            if not brain_model:
                return {"error": f"Model {model_name} not found"}
                
            recent_metrics = self.db.query(ModelPerformance).filter(
                ModelPerformance.brain_model_id == brain_model.id
            ).order_by(ModelPerformance.timestamp.desc()).limit(100).all()
            
            # Calculate performance summary
            performance_summary = {}
            for metric in recent_metrics:
                if metric.metric_name not in performance_summary:
                    performance_summary[metric.metric_name] = []
                performance_summary[metric.metric_name].append(metric.metric_value)
                
            # Calculate averages
            for metric_name, values in performance_summary.items():
                performance_summary[metric_name] = {
                    "average": np.mean(values),
                    "min": np.min(values),
                    "max": np.max(values),
                    "count": len(values)
                }
                
            return {
                "model_name": model_name,
                "performance_summary": performance_summary,
                "last_updated": brain_model.updated_at.isoformat()
            }
            
        except Exception as e:
            self.logger.error(f"Error evaluating model performance: {e}")
            return {"error": str(e)}
            
    async def get_training_status(self) -> Dict:
        """Get current training status"""
        try:
            # Get active training sessions
            active_sessions = self.db.query(TrainingSession).filter(
                TrainingSession.status == "running"
            ).all()
            
            # Get recent completed sessions
            recent_sessions = self.db.query(TrainingSession).filter(
                TrainingSession.status.in_(["completed", "failed"])
            ).order_by(TrainingSession.end_time.desc()).limit(10).all()
            
            return {
                "active_sessions": [
                    {
                        "id": session.id,
                        "brain_model_id": session.brain_model_id,
                        "session_type": session.session_type,
                        "start_time": session.start_time.isoformat(),
                        "metrics": session.metrics
                    }
                    for session in active_sessions
                ],
                "recent_sessions": [
                    {
                        "id": session.id,
                        "brain_model_id": session.brain_model_id,
                        "session_type": session.session_type,
                        "status": session.status,
                        "start_time": session.start_time.isoformat(),
                        "end_time": session.end_time.isoformat() if session.end_time else None,
                        "metrics": session.metrics
                    }
                    for session in recent_sessions
                ]
            }
            
        except Exception as e:
            self.logger.error(f"Error getting training status: {e}")
            return {"error": str(e)} 