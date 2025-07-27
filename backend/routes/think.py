from fastapi import APIRouter, Request, WebSocket, WebSocketDisconnect
from pydantic import BaseModel
from Core.cmp import cmp_llm_manager

router = APIRouter()

class ThinkRequest(BaseModel):
    query: str
    models: list = []

@router.post("/api/think")
async def think_api(request: ThinkRequest):
    query = request.query
    models = request.models or ["deepseek", "yi", "qwen"]
    responses = {}

    for model in models:
        # Simulate multi-LLM response (replace with real inference calls)
        responses[model] = {"text": f"{model} simulated response to: {query}"}

    merged = cmp_llm_manager.score_and_merge_responses(query, responses)
    return {"merged": merged, "raw": responses}

@router.websocket("/ws/think")
async def websocket_think(ws: WebSocket):
    await ws.accept()
    try:
        while True:
            data = await ws.receive_json()
            query = data.get("query", "")
            models = data.get("models", ["deepseek", "yi", "qwen"])

            responses = {}
            for model in models:
                responses[model] = {"text": f"{model} simulated response to: {query}"}

            merged = cmp_llm_manager.score_and_merge_responses(query, responses)
            await ws.send_json({"merged": merged, "raw": responses})
    except WebSocketDisconnect:
        await ws.close()
