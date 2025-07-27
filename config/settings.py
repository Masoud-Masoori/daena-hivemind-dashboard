"""
Daena Backend Settings Configuration
"""
import os
from typing import List, Optional
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # Project settings
    PROJECT_NAME: str = "Daena Backend"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Server settings
    BACKEND_PORT: int = 8000
    BACKEND_HOST: str = "0.0.0.0"
    
    # CORS settings
    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:3000",
        "http://localhost:8000",
        "http://127.0.0.1:3000",
        "http://127.0.0.1:8000",
    ]
    
    # Logging
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "sqlite:///./daena.db"
    
    # Security
    SECRET_KEY: str = "your-secret-key-here"
    API_KEY_HEADER: str = "X-API-Key"
    TEST_API_KEY: str = "test-api-key"
    
    # Rate limiting
    RATE_LIMIT_PER_MINUTE: int = 60
    
    react_app_ws_url: str = "ws://localhost:8000/ws"
    react_app_api_url: Optional[str] = None
    openai_api_key: Optional[str] = None
    anthropic_api_key: Optional[str] = None
    claude_api_key: Optional[str] = None
    deepseek_path: Optional[str] = None
    qwen_path: Optional[str] = None
    yi_path: Optional[str] = None
    daena_path: Optional[str] = None
    webui_path: Optional[str] = None
    gemini_api_key: Optional[str] = None
    grok_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None
    del_path_r2: Optional[str] = None
    model_path_qwen: Optional[str] = None
    model_path_yi: Optional[str] = None
    model_path_daena: Optional[str] = None
    model_path_webui: Optional[str] = None
    pythonpath: Optional[str] = None
    llm_api_url: Optional[str] = None
    port: Optional[str] = None
    llm_api_key: Optional[str] = None
    
    class Config:
        env_file = ".env"
        extra = "ignore"  # Ignore extra fields from environment variables

def get_settings() -> Settings:
    return Settings() 

# Create a global settings instance
settings = get_settings()

def validate_llm_providers() -> dict:
    """Validate and return available LLM providers"""
    providers = {}
    
    if settings.openai_api_key:
        providers["openai"] = {"status": "available", "key": "configured"}
    else:
        providers["openai"] = {"status": "unavailable", "key": "not configured"}
    
    if settings.anthropic_api_key:
        providers["anthropic"] = {"status": "available", "key": "configured"}
    else:
        providers["anthropic"] = {"status": "unavailable", "key": "not configured"}
    
    if settings.gemini_api_key:
        providers["gemini"] = {"status": "available", "key": "configured"}
    else:
        providers["gemini"] = {"status": "unavailable", "key": "not configured"}
    
    return providers

def get_cors_origins() -> List[str]:
    """Get CORS origins from settings"""
    return settings.BACKEND_CORS_ORIGINS 