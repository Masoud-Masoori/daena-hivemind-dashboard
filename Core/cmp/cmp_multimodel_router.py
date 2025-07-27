import os
import openai
import requests
from core.cmp.cmp_vault_ai import get_api_key
from datetime import datetime

def decide_and_route(question):
    log_dir = "D:/Ideas/Daena/logs"
    os.makedirs(log_dir, exist_ok=True)
    with open(os.path.join(log_dir, "model_choices.log"), "a") as f:
        f.write(f"{datetime.now()} | Question: {question}\n")

    # Prefer offline brain if loaded
    if os.path.exists("E:/Daena/models/llm/daena-reflex-v2"):
        with open(os.path.join(log_dir, "model_choices.log"), "a") as f:
            f.write(f"{datetime.now()} | Chosen: Local Reflex\n")
        return "[Local Reflex] Response: 'Answer simulated based on daena-reflex-v2'"

    # Otherwise use API fallback (ranked)
    try:
        openai.api_key = get_api_key("OPENAI_API_KEY")
        with open(os.path.join(log_dir, "model_choices.log"), "a") as f:
            f.write(f"{datetime.now()} | Chosen: OpenAI GPT-4\n")
        return openai.ChatCompletion.create(model="gpt-4", messages=[{"role": "user", "content": question}])
    except:
        with open(os.path.join(log_dir, "model_choices.log"), "a") as f:
            f.write(f"{datetime.now()} | Chosen: Fallback (No online model available)\n")
        return "[Fallback] No online model available."
