from sqlalchemy import create_engine, Column, Integer, String, DateTime, ForeignKey, Text, Boolean, Float, JSON
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
import datetime

# Create SQLAlchemy engine (SQLite for development, easy to switch to MongoDB later)
engine = create_engine("sqlite:///./daena.db", connect_args={"check_same_thread": False})

# Create declarative base
Base = declarative_base()

# Example User model
class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)
    role = Column(String, default="user")
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Enhanced Agent model with brain training capabilities
class Agent(Base):
    __tablename__ = "agents"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    department = Column(String, default="general")
    status = Column(String, default="idle")
    type = Column(String)
    capabilities = Column(Text)
    description = Column(Text)
    is_active = Column(Boolean, default=True)
    brain_model_id = Column(Integer, ForeignKey("brain_models.id"), nullable=True)
    training_status = Column(String, default="untrained")
    performance_score = Column(Float, default=0.0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    brain_model = relationship("BrainModel", back_populates="agents")

# Enhanced Brain Model for multi-LLM training with R1/R2 support
class BrainModel(Base):
    __tablename__ = "brain_models"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    model_type = Column(String)  # "r1", "r2", "deepseek_v3", "qwen", "yi", "hybrid", "openai_gpt4"
    model_path = Column(String, nullable=True)  # Local path or cloud endpoint
    provider = Column(String)  # "local", "azure", "huggingface", "anthropic", "openai"
    api_key = Column(String, nullable=True)
    config = Column(JSON)  # Model-specific configuration
    status = Column(String, default="available")  # available, training, error, offline
    performance_metrics = Column(JSON, default={})
    last_used = Column(DateTime, nullable=True)
    model_size = Column(String, nullable=True)  # "7B", "14B", "70B", etc.
    context_length = Column(Integer, default=4096)
    is_quantized = Column(Boolean, default=False)
    quantization_type = Column(String, nullable=True)  # "int8", "int4", "gguf", etc.
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

    agents = relationship("Agent", back_populates="brain_model")
    training_sessions = relationship("TrainingSession", back_populates="brain_model")
    consensus_votes = relationship("ConsensusVote", back_populates="brain_model")
    model_checkpoints = relationship("ModelCheckpoint", back_populates="brain_model")

# New: Model Checkpoints for training progress
class ModelCheckpoint(Base):
    __tablename__ = "model_checkpoints"
    id = Column(Integer, primary_key=True, index=True)
    brain_model_id = Column(Integer, ForeignKey("brain_models.id"))
    checkpoint_name = Column(String)
    checkpoint_path = Column(String)
    training_step = Column(Integer, default=0)
    loss_value = Column(Float, nullable=True)
    accuracy_score = Column(Float, nullable=True)
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    
    brain_model = relationship("BrainModel", back_populates="model_checkpoints")

# Enhanced Training Sessions for brain development
class TrainingSession(Base):
    __tablename__ = "training_sessions"
    id = Column(Integer, primary_key=True, index=True)
    brain_model_id = Column(Integer, ForeignKey("brain_models.id"))
    session_type = Column(String)  # "conversation", "decision", "strategy", "knowledge", "reasoning"
    training_data = Column(JSON)
    parameters = Column(JSON)  # Training parameters
    status = Column(String, default="running")  # running, completed, failed, paused
    start_time = Column(DateTime, default=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)
    metrics = Column(JSON, default={})  # Training metrics
    loss_history = Column(JSON, default=[])
    learning_rate = Column(Float, nullable=True)
    batch_size = Column(Integer, nullable=True)
    epochs_completed = Column(Integer, default=0)
    total_epochs = Column(Integer, default=1)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

    brain_model = relationship("BrainModel", back_populates="training_sessions")

# Enhanced Consensus System for multi-LLM decisions
class ConsensusVote(Base):
    __tablename__ = "consensus_votes"
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(String, index=True)  # Unique topic identifier
    brain_model_id = Column(Integer, ForeignKey("brain_models.id"))
    vote = Column(Text)  # The model's decision/vote
    confidence = Column(Float, default=0.0)  # Confidence score
    reasoning = Column(Text, nullable=True)  # Explanation for the vote
    vote_weight = Column(Float, default=1.0)  # Weight for this model's vote
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    
    brain_model = relationship("BrainModel", back_populates="consensus_votes")

# New: Consensus Topics for organizing votes
class ConsensusTopic(Base):
    __tablename__ = "consensus_topics"
    id = Column(Integer, primary_key=True, index=True)
    topic_id = Column(String, unique=True, index=True)
    title = Column(String)
    description = Column(Text)
    category = Column(String)  # "business", "technical", "strategy", "investment"
    status = Column(String, default="active")  # active, resolved, archived
    required_consensus = Column(Float, default=0.7)  # Minimum consensus threshold
    deadline = Column(DateTime, nullable=True)
    final_decision = Column(Text, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    resolved_at = Column(DateTime, nullable=True)

# Enhanced Knowledge Base for training data
class KnowledgeEntry(Base):
    __tablename__ = "knowledge_entries"
    id = Column(Integer, primary_key=True, index=True)
    category = Column(String, index=True)  # "company", "market", "technology", "strategy", "investor"
    title = Column(String)
    content = Column(Text)
    source = Column(String, nullable=True)
    tags = Column(JSON, default=[])
    importance_score = Column(Float, default=0.0)
    embedding_vector = Column(Text, nullable=True)  # Vector representation for similarity search
    last_accessed = Column(DateTime, nullable=True)
    access_count = Column(Integer, default=0)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# New: Training Data Sources
class TrainingDataSource(Base):
    __tablename__ = "training_data_sources"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    source_type = Column(String)  # "file", "api", "database", "web_scrape"
    source_path = Column(String)
    format_type = Column(String)  # "json", "csv", "txt", "jsonl"
    is_active = Column(Boolean, default=True)
    last_sync = Column(DateTime, nullable=True)
    sync_frequency = Column(Integer, default=3600)  # seconds
    metadata = Column(JSON, default={})
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# New: Model Performance Tracking
class ModelPerformance(Base):
    __tablename__ = "model_performance"
    id = Column(Integer, primary_key=True, index=True)
    brain_model_id = Column(Integer, ForeignKey("brain_models.id"))
    metric_name = Column(String)  # "accuracy", "latency", "throughput", "memory_usage"
    metric_value = Column(Float)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    context = Column(JSON, default={})  # Additional context for the metric

# Enhanced Conversation History
class ConversationHistory(Base):
    __tablename__ = "conversation_history"
    id = Column(Integer, primary_key=True, index=True)
    session_id = Column(String, index=True)
    user_message = Column(Text)
    daena_response = Column(Text)
    brain_model_used = Column(String, nullable=True)
    context = Column(JSON, default={})
    feedback_score = Column(Float, nullable=True)
    response_time_ms = Column(Integer, nullable=True)
    tokens_used = Column(Integer, nullable=True)
    cost_estimate = Column(Float, nullable=True)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)

# Enhanced Consultation model
class Consultation(Base):
    __tablename__ = "consultations"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    topic = Column(String)
    start_time = Column(DateTime)
    duration = Column(Integer)
    notes = Column(Text)
    status = Column(String, default="scheduled")
    brain_models_used = Column(JSON, default=[])  # List of models used during consultation
    consensus_required = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)
    end_time = Column(DateTime, nullable=True)

    user = relationship("User")
    messages = relationship("Message", back_populates="consultation")

# Enhanced Message model
class Message(Base):
    __tablename__ = "messages"
    id = Column(Integer, primary_key=True, index=True)
    consultation_id = Column(Integer, ForeignKey("consultations.id"))
    sender = Column(String)
    content = Column(Text)
    timestamp = Column(DateTime, default=datetime.datetime.utcnow)
    message_type = Column(String, default="text")  # text, voice, image, file
    brain_model_used = Column(String, nullable=True)
    confidence_score = Column(Float, nullable=True)

    consultation = relationship("Consultation", back_populates="messages")

# New: System Configuration
class SystemConfig(Base):
    __tablename__ = "system_config"
    id = Column(Integer, primary_key=True, index=True)
    config_key = Column(String, unique=True, index=True)
    config_value = Column(Text)
    config_type = Column(String, default="string")  # string, int, float, bool, json
    description = Column(Text, nullable=True)
    is_sensitive = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.datetime.utcnow, onupdate=datetime.datetime.utcnow)

# Database session
def get_db():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create all tables
def create_tables():
    Base.metadata.create_all(bind=engine)

# Initialize default data
def initialize_default_data():
    SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    db = SessionLocal()
    
    try:
        # Add default system configurations
        default_configs = [
            {"key": "default_brain_model", "value": "openai_gpt4", "type": "string", "description": "Default brain model for Daena"},
            {"key": "consensus_threshold", "value": "0.7", "type": "float", "description": "Default consensus threshold for decisions"},
            {"key": "max_training_epochs", "value": "10", "type": "int", "description": "Maximum training epochs for brain models"},
            {"key": "enable_voice", "value": "true", "type": "bool", "description": "Enable voice interaction"},
            {"key": "enable_cmp", "value": "true", "type": "bool", "description": "Enable CMP decision engine"},
        ]
        
        for config in default_configs:
            existing = db.query(SystemConfig).filter(SystemConfig.config_key == config["key"]).first()
            if not existing:
                db_config = SystemConfig(
                    config_key=config["key"],
                    config_value=config["value"],
                    config_type=config["type"],
                    description=config["description"]
                )
                db.add(db_config)
        
        db.commit()
        
    except Exception as e:
        print(f"Error initializing default data: {e}")
        db.rollback()
    finally:
        db.close() 