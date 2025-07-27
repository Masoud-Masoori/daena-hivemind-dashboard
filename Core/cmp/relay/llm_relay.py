import os
import openai
import requests
from cmp_brain import decide_final_response
from cmp_vault_ai import get_api_keys

def ask_all_llms(prompt):
    keys = get_api_keys()
    responses = {}

    if keys.get("OPENAI_API_KEY"):
        openai.api_key = keys["OPENAI_API_KEY"]
        try:
            responses["openai"] = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[{"role": "user", "content": prompt}]
            )["choices"][0]["message"]["content"]
        except Exception as e:
            responses["openai"] = f"Error: {str(e)}"

    if keys.get("DEEPSEEK_API"):
        try:
            r = requests.post("http://localhost:8000/v1/completions", json={"messages": [{"role": "user", "content": prompt}]})
            responses["deepseek"] = r.json().get("choices", [{}])[0].get("message", {}).get("content", "")
        except Exception as e:
            responses["deepseek"] = f"Error: {str(e)}"

    # Add more as needed...
    return decide_final_response(responses)
