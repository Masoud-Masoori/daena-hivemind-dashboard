from fastapi import APIRouter

router = APIRouter()

# Add placeholder endpoints or import actual routes here later
# @router.get("/models")
# async def list_models():
#     return []

@router.get("/", response_model=list)
async def list_models():
    """List all available models."""
    # Placeholder implementation - replace with actual logic to fetch models
    placeholder_models = [
        {"id": "deepseek", "type": "LLM", "status": "active"},
        {"id": "qwen", "type": "LLM", "status": "inactive"},
        {"id": "yi", "type": "LLM", "status": "active"},
    ]
    return placeholder_models 