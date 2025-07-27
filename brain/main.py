import os
import json
import openai
import httpx
import asyncio
import websockets
from fastapi import FastAPI
from dotenv import load_dotenv
from datetime import datetime
import google.generativeai as genai

load_dotenv()
app = FastAPI()

openai.api_key = os.getenv("OPENAI_API_KEY")
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

MEMORY_DIR = os.path.join(os.getcwd(), '..', 'memory')
LOGS_DIR = os.path.join(os.getcwd(), '..', 'logs')

def append_memory(agent, role, content):
    path = os.path.join(MEMORY_DIR, f"{agent}.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps({"role": role, "content": content}) + "\n")

def log_decision(question, responses, chosen):
    log = {
        "timestamp": datetime.utcnow().isoformat(),
        "question": question,
        "chosen_model": chosen,
        "responses": responses
    }
    path = os.path.join(LOGS_DIR, "decision_log.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(log) + "\n")

async def query_openai(msg):
    try:
        res = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{ "role": "user", "content": msg }],
            temperature=0.7
        )
        return res['choices'][0]['message']['content']
    except Exception as e:
        return f"OpenAI error: {str(e)}"

async def query_gemini(msg):
    try:
        model = genai.GenerativeModel("gemini-pro")
        chat = model.start_chat()
        res = chat.send_message(msg)
        return res.text
    except Exception as e:
        return f"Gemini error: {str(e)}"

async def query_llm_api(url, msg):
    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            res = await client.post(url, json={ "prompt": msg })
            return res.json().get("text", "No output.")
    except Exception as e:
        return f"Error: {str(e)}"

async def ask_all(msg):
    tasks = [
        query_openai(msg),
        query_gemini(msg),
        query_llm_api(os.getenv("DEEPSEEK_API_URL"), msg),
        query_llm_api(os.getenv("QWEN_API_URL"), msg),
        query_llm_api(os.getenv("YI_API_URL"), msg)
    ]
    results = await asyncio.gather(*tasks)
    return {
        "OpenAI": results[0],
        "Gemini": results[1],
        "DeepSeek": results[2],
        "Qwen": results[3],
        "Yi": results[4]
    }

@app.websocket("/ws")
async def websocket_endpoint(websocket):
    await websocket.accept()
    while True:
        try:
            data = await websocket.receive_text()
            if data.strip().startswith("{"):
                payload = json.loads(data)
                if payload.get("type") == "voice":
                    print("Voice Toggle:", payload["enabled"])
                    continue
            msg = data.strip()
            agent = "General"
            print(" User asked:", msg)
            answers = await ask_all(msg)

            # Simple logic: pick the longest response
            chosen_model = max(answers, key=lambda k: len(answers[k]))
            chosen_response = answers[chosen_model]

            append_memory(agent, "user", msg)
            append_memory(agent, "daena", chosen_response)
            log_decision(msg, answers, chosen_model)

            await websocket.send_text(json.dumps({
                "type": "llm",
                "responses": {
                    "DeepSeek": answers["DeepSeek"],
                    "Qwen": answers["Qwen"],
                    "Yi": answers["Yi"]
                }
            }))
        except Exception as e:
            await websocket.send_text(f"[Backend Error] {str(e)}")
