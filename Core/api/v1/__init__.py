from fastapi import APIRouter, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from typing import Dict, Any

# Create main API router
api_router = APIRouter(prefix="/api/v1")

# Import and include all endpoint routers
from .agents import router as agents_router
from .models import router as models_router
from .voice import router as voice_router
from .consultation import router as consultation_router

# Include all routers
api_router.include_router(agents_router, prefix="/agents", tags=["agents"])
api_router.include_router(models_router, prefix="/models", tags=["models"])
api_router.include_router(voice_router, prefix="/voice", tags=["voice"])
api_router.include_router(consultation_router, prefix="/consultation", tags=["consultation"])

def create_app() -> FastAPI:
    """Create and configure the FastAPI application."""
    app = FastAPI(
        title="Daena API",
        description="Daena Hybrid AI System API",
        version="1.0.0"
    )
    
    # Configure CORS
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],  # Update this in production
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    
    # Include API router
    app.include_router(api_router)
    
    return app 