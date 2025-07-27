from fastapi import APIRouter, WebSocket
router = APIRouter()

@router.websocket("/ws/agent")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        data = await websocket.receive_text()
        print(f"Received: {data}")
        await websocket.send_text(f"Agent Ack: {data}")
