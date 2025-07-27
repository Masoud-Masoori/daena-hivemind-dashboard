import pytest
from fastapi import status
import json

def test_basic_chat(client):
    """Test basic chat functionality with Daena."""
    # Test a simple prompt
    response = client.post(
        "/api/v1/llm/completion",
        json={
            "prompt": "Hello, I'm testing Daena. Can you respond?",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 100,
            "top_p": 1.0
        }
    )
    
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "text" in data
    assert len(data["text"]) > 0
    print(f"\nDaena's response: {data['text']}")

def test_chat_context(client):
    """Test chat with context/memory."""
    # First message
    response1 = client.post(
        "/api/v1/llm/completion",
        json={
            "prompt": "My name is TestUser. Remember this.",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 100,
            "top_p": 1.0
        }
    )
    assert response1.status_code == status.HTTP_200_OK
    
    # Follow-up question
    response2 = client.post(
        "/api/v1/llm/completion",
        json={
            "prompt": "What's my name?",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 100,
            "top_p": 1.0
        }
    )
    assert response2.status_code == status.HTTP_200_OK
    data = response2.json()
    assert "text" in data
    print(f"\nDaena's response to follow-up: {data['text']}")

def test_chat_streaming(client):
    """Test streaming chat responses."""
    response = client.post(
        "/api/v1/llm/stream",
        json={
            "prompt": "Tell me a very short story.",
            "model": "gpt-3.5-turbo",
            "temperature": 0.7,
            "max_tokens": 100,
            "top_p": 1.0
        }
    )
    assert response.status_code == status.HTTP_200_OK
    
    # Parse streaming response
    lines = response.content.splitlines()
    chunks = [json.loads(line)["text"] for line in lines if line]
    print("\nDaena's streaming response:")
    print("".join(chunks)) 