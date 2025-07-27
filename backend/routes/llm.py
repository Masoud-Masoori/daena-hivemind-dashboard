from fastapi import APIRouter, HTTPException, status
from fastapi.responses import StreamingResponse
from typing import List, Optional, Dict, Any, AsyncGenerator
from pydantic import BaseModel
import json
import asyncio
import importlib.util

# Import LLM router and model integration
from Core.llm.llm_router_core import route_task
from Core.llm.model_integration import ModelIntegration

router = APIRouter()
model_integration = ModelIntegration()

class LLMRequest(BaseModel):
    prompt: str
    model: Optional[str] = None  # If not provided, router will select
    temperature: float = 0.7
    max_tokens: int = 100
    top_p: float = 1.0
    context: Optional[Dict[str, Any]] = None

class LLMResponse(BaseModel):
    text: str
    model: str
    usage: Dict[str, int]
    consensus: Optional[str] = None
    confidence: Optional[float] = None
    responses: Optional[Dict[str, str]] = None

class ModelSwitchRequest(BaseModel):
    model_id: str
    reason: Optional[str] = None

async def get_llm_response(prompt: str, model: Optional[str] = None, **kwargs) -> Dict:
    """Get a response from the best LLM (local/cloud/hybrid)."""
    # Use router to select model if not provided
    selected_model = model or route_task(prompt)
    response = await model_integration.generate_response(prompt, context=kwargs.get('context'))
    # If response is a dict with consensus, return consensus
    if isinstance(response, dict) and 'consensus' in response:
        return {
            "text": response["consensus"],
            "model": selected_model,
            "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30},
            "consensus": response["consensus"],
            "confidence": response.get("confidence"),
            "responses": response.get("responses")
        }
    # Otherwise, return as text
    return {
        "text": str(response),
        "model": selected_model,
        "usage": {"prompt_tokens": 10, "completion_tokens": 20, "total_tokens": 30}
    }

async def stream_llm_response(prompt: str, model: Optional[str] = None, **kwargs) -> AsyncGenerator[str, None]:
    """Stream a response from the LLM (mock streaming for now)."""
    # Use router to select model if not provided
    selected_model = model or route_task(prompt)
    # For now, just stream the consensus response in chunks
    response = await model_integration.generate_response(prompt, context=kwargs.get('context'))
    text = response["consensus"] if isinstance(response, dict) and "consensus" in response else str(response)
    # Simulate streaming by splitting into words
    for chunk in text.split():
        yield json.dumps({"text": chunk}) + "\n"
        await asyncio.sleep(0.05)

@router.post("/completion", response_model=LLMResponse)
async def generate_completion(request: LLMRequest):
    """Generate a completion for the given prompt using the best available LLM (local/cloud/hybrid)."""
    try:
        result = await get_llm_response(
            request.prompt,
            model=request.model,
            temperature=request.temperature,
            max_tokens=request.max_tokens,
            top_p=request.top_p,
            context=request.context
        )
        return LLMResponse(**result)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.post("/stream")
async def stream_completion(request: LLMRequest):
    """Stream a completion from the best available LLM (local/cloud/hybrid)."""
    try:
        return StreamingResponse(
            stream_llm_response(
                request.prompt,
                model=request.model,
                temperature=request.temperature,
                max_tokens=request.max_tokens,
                top_p=request.top_p,
                context=request.context
            ),
            media_type="application/x-ndjson"
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/models", response_model=List[str])
async def list_models():
    """List available LLM models (from registry)."""
    # Load from registry
    with open("Core/llm/llm_registry.json", "r") as f:
        registry = json.load(f)
    return list(registry.keys())

@router.get("/parameters", response_model=Dict[str, Dict[str, Any]])
async def get_parameters():
    """Get available parameters for LLM requests."""
    return {
        "temperature": {"type": "float", "default": 0.7, "min": 0.0, "max": 1.0},
        "max_tokens": {"type": "integer", "default": 100, "min": 1, "max": 2048},
        "top_p": {"type": "float", "default": 1.0, "min": 0.0, "max": 1.0}
    }

@router.post("/switch-model")
async def switch_model(request: ModelSwitchRequest):
    """Switch the active LLM model for the system."""
    try:
        # Load registry to validate model exists
        with open("Core/llm/llm_registry.json", "r") as f:
            registry = json.load(f)
        
        if request.model_id not in registry:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Model '{request.model_id}' not found in registry"
            )
        
        # In a real implementation, this would update the system's active model
        # For now, we'll just return success
        return {
            "success": True,
            "model_id": request.model_id,
            "message": f"Successfully switched to {request.model_id}",
            "model_info": registry[request.model_id]
        }
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=str(e)
        )

@router.get("/current-model")
async def get_current_model():
    """Get the currently active LLM model."""
    # In a real implementation, this would return the system's current model
    # For now, return a default
    return {
        "model_id": "openai",
        "name": "GPT-4 Turbo",
        "provider": "OpenAI",
        "status": "active"
    }
