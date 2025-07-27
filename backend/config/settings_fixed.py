from pydantic import BaseSettings
from typing import List, Optional
import os
from pathlib import Path

class Settings(BaseSettings):
    # Core API Settings
    api_key: str = "daena_secure_key_2025"
    environment: str = "development"
    debug: bool = True
    
    # Server Configuration
    host: str = "0.0.0.0"
    port: int = 8000
    
    # Database Configuration
    database_url: str = "sqlite:///./daena.db"
    
    # Security
    cors_origins: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000", 
        "http://127.0.0.1:8000",
        "http://127.0.0.1:3000"
    ]
    
    # LLM Configuration
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    gemini_api_key: Optional[str] = None
    
    # Voice Settings
    voice_enabled: bool = True
    voice_env_path: str = "./daena_tts/Scripts/Activate.ps1"
    
    # Monitoring
    prometheus_enabled: bool = True
    metrics_port: int = 9090
    log_level: str = "INFO"
    
    # Frontend Settings
    next_public_api_url: str = "http://localhost:8000"
    next_public_api_key: str = "daena_secure_key_2025"
    
    # Database Settings (if using PostgreSQL)
    postgres_server: str = "localhost"
    postgres_user: str = "postgres" 
    postgres_password: str = "postgres"
    postgres_db: str = "daena"
    
    # Redis Settings
    redis_host: str = "localhost"
    redis_port: str = "6379"
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        # Allow extra fields without validation errors
        extra = "allow"

def get_cors_origins() -> List[str]:
    """Get CORS origins from settings"""
    return settings.cors_origins

def validate_llm_providers() -> dict:
    """Validate and return available LLM providers"""
    providers = {}
    
    if settings.openai_api_key:
        providers["openai"] = True
    if settings.anthropic_api_key:
        providers["anthropic"] = True  
    if settings.gemini_api_key:
        providers["gemini"] = True
        
    if not providers:
        providers["fallback"] = True
        
    return providers

# Create settings instance
settings = Settings()

# Validation functions
def get_database_url() -> str:
    """Get the appropriate database URL"""
    if settings.database_url.startswith("sqlite"):
        # Ensure SQLite database directory exists
        db_path = Path(settings.database_url.replace("sqlite:///", ""))
        db_path.parent.mkdir(parents=True, exist_ok=True)
    return settings.database_url

def get_static_files_path() -> str:
    """Get the static files directory path"""
    static_path = Path("frontend/static")
    static_path.mkdir(parents=True, exist_ok=True)
    return str(static_path)

def get_templates_path() -> str:
    """Get the templates directory path"""
    templates_path = Path("frontend/templates")
    templates_path.mkdir(parents=True, exist_ok=True)
    return str(templates_path)

# Export commonly used settings
API_KEY = settings.api_key
DATABASE_URL = get_database_url()
CORS_ORIGINS = get_cors_origins()
LLM_PROVIDERS = validate_llm_providers()
STATIC_PATH = get_static_files_path()
TEMPLATES_PATH = get_templates_path()

print(f"✅ Settings loaded: {settings.environment} environment")
print(f"🔑 API Key configured: {settings.api_key[:10]}...")
print(f"🗄️ Database: {settings.database_url}")
print(f"🌐 CORS Origins: {len(settings.cors_origins)} configured")
print(f"🤖 LLM Providers: {list(LLM_PROVIDERS.keys())}")
print(f"📁 Static Path: {STATIC_PATH}")
print(f"📄 Templates Path: {TEMPLATES_PATH}") 