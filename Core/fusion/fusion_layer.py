### File: core/fusion/fusion_layer.py

from openai import OpenAI
from google.generativeai import GenerativeModel

def query_openai(prompt):
    client = OpenAI()
    return client.chat.completions.create(
        model="gpt-4",
        messages=[{"role": "user", "content": prompt}]
    ).choices[0].message.content

def query_gemini(prompt):
    model = GenerativeModel("gemini-1.5-pro-latest")
    return model.generate_content(prompt).text

def fuse_response(prompt):
    openai_response = query_openai(prompt)
    gemini_response = query_gemini(prompt)

    if len(openai_response) > len(gemini_response):
        return openai_response.strip()
    elif "code" in gemini_response.lower():
        return gemini_response.strip()
    else:
        return openai_response.strip() + "\n\n(Gemini adds: " + gemini_response.strip() + ")"
