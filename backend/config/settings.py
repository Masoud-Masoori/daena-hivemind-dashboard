"""
Production-ready configuration settings for Daena AI System
"""

import os
import json
from pathlib import Path
from typing import List, Optional
from pydantic import Field, ConfigDict, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict
from dotenv import load_dotenv

# Load environment variables
project_root = Path(__file__).parent.parent.parent
env_file = project_root / ".env"
if env_file.exists():
    load_dotenv(env_file)

class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        extra="allow", 
        protected_namespaces=(),
        env_file=".env",
        env_file_encoding='utf-8',
        case_sensitive=False
    )
    
    # API Configuration
    app_name: str = "Mas-AI Company - Daena AI VP System"
    app_version: str = "2.0.0"
    debug: bool = True
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    cors_origins: List[str] = ["http://localhost:3000", "http://localhost:8000", "http://127.0.0.1:3000", "http://127.0.0.1:8000"]
    
    # API Keys - Production Configuration
    api_key: str = "daena_secure_key_2025"
    
    # AI Provider API Keys
    openai_api_key: Optional[str] = Field(None, env="OPENAI_API_KEY")
    anthropic_api_key: Optional[str] = Field(None, env="ANTHROPIC_API_KEY") 
    gemini_api_key: Optional[str] = Field(None, env="GEMINI_API_KEY")
    deepseek_api_key: Optional[str] = Field(None, env="DEEPSEEK_API_KEY")
    grok_api_key: Optional[str] = Field(None, env="GROK_API_KEY")
    mistral_api_key: Optional[str] = Field(None, env="MISTRAL_API_KEY")
    
    # Voice Services
    elevenlabs_api_key: Optional[str] = Field(None, env="ELEVENLABS_API_KEY")
    did_api_key: Optional[str] = Field(None, env="DID_API_KEY")
    google_tts_api_key: Optional[str] = Field(None, env="GOOGLE_TTS_API_KEY")
    
    # Authentication & Roles
    auth_enabled: bool = True
    founder_role: str = "founder"
    agent_role: str = "agent"
    guest_role: str = "guest"
    session_expiry: int = 3600
    
    # Voice Configuration
    voice_enabled: bool = True
    raw_voice_activation_phrases: Optional[str] = None  # Raw string from env
    voice_response_enabled: bool = True
    voice_recognition_enabled: bool = True
    voice_env_path: str = "./daena_tts/Scripts/Activate.ps1"
    
    # Hybrid GPU/Cloud Configuration
    gpu_enabled: bool = True
    gcp_fallback_enabled: bool = True
    gcp_project_id: Optional[str] = Field(None, env="GCP_PROJECT_ID")
    gcp_zone: str = "us-central1-a"
    gcp_instance_name: str = "daena-gpu-instance"
    gcp_machine_type: str = "n1-standard-4"
    gcp_gpu_type: str = "nvidia-tesla-t4"
    gcp_gpu_count: int = 1

    @property
    def voice_activation_phrases(self) -> List[str]:
        """
        Robust accessor for voice activation phrases:
        - Supports JSON list format: '["Hey Daena", "Jarvis"]'
        - Supports comma-separated: 'Hey Daena,Jarvis'
        - Supports blank or unset values (returns default)
        """
        raw = self.raw_voice_activation_phrases
        if not raw:
            return ["Hey Daena", "Computer", "Assistant"]
        try:
            parsed = json.loads(raw)
            if isinstance(parsed, list) and all(isinstance(x, str) for x in parsed):
                return parsed
        except Exception:
            pass
        return [p.strip() for p in raw.split(",") if p.strip()]

    @property
    def voice_activation_phrases_list(self) -> list[str]:
        """Alias for backward compatibility"""
        return self.voice_activation_phrases

    @field_validator("cors_origins", mode='before')
    @classmethod
    def assemble_cors_origins(cls, v):
        if isinstance(v, str):
            return [i.strip() for i in v.split(",")]
        return v
    
    # Monetization
    stripe_publishable_key: Optional[str] = Field(None, env="STRIPE_PUBLISHABLE_KEY")
    stripe_secret_key: Optional[str] = Field(None, env="STRIPE_SECRET_KEY")
    enable_payments: bool = False
    marketplace_enabled: bool = True
    commission_rate: float = 0.15
    
    # Database Configuration
    database_url: str = "sqlite:///./daena.db"
    postgres_server: str = "localhost"
    postgres_user: str = "postgres"
    postgres_password: str = "postgres"
    postgres_db: str = "daena"
    
    # Redis Configuration
    redis_host: str = "localhost"
    redis_port: int = 6379
    
    # Monitoring
    prometheus_enabled: bool = True
    metrics_port: int = 9090

settings = Settings()

def validate_llm_providers():
    """Validate that at least one LLM provider is configured"""
    provider_keys = [
        settings.openai_api_key,
        settings.gemini_api_key,
        settings.anthropic_api_key,
        settings.deepseek_api_key,
        settings.grok_api_key,
        settings.mistral_api_key,
    ]
    if not any(provider_keys):
        print("⚠️ WARNING: No LLM providers are configured. AI responses will be disabled.")
    else:
        print("✅ LLM providers configured.")

def get_database_url() -> str:
    """Construct database URL from settings"""
    if settings.database_url and settings.database_url.startswith("postgresql"):
        return settings.database_url
    
    # Fallback to constructing from individual components
    return f"postgresql://{settings.postgres_user}:{settings.postgres_password}@{settings.postgres_server}/{settings.postgres_db}"

def get_cors_origins():
    """Get CORS origins for FastAPI"""
    return settings.cors_origins
