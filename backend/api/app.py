from fastapi import FastAPI, WebSocket
from core.agent_controller import handle_prompt

app = FastAPI()

@app.get("/")
def root():
    return {"status": "Daena API is live."}

@app.post("/ask")
def ask_daena(prompt: str):
    return {"reply": handle_prompt(prompt)}

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    while True:
        prompt = await websocket.receive_text()
        response = handle_prompt(prompt)
        await websocket.send_text(response)
