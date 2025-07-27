import pytest
from fastapi import status
from unittest.mock import patch
import json

def test_llm_completion(client):
    test_prompt = "What is the capital of France?"
    expected_response = "The capital of France is Paris."
    with patch('backend.routes.llm.get_llm_response') as mock_llm:
        mock_llm.return_value = expected_response
        response = client.post(
            "/api/v1/llm/completion",
            json={
                "prompt": test_prompt,
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 100,
                "top_p": 1.0
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["text"] == expected_response
        assert data["model"] == "gpt-3.5-turbo"
        assert "usage" in data
        mock_llm.assert_called_once_with(
            test_prompt,
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=100,
            top_p=1.0
        )

def test_llm_streaming(client):
    test_prompt = "Tell me a short story."
    expected_chunks = ["Once", "upon", "a", "time"]
    with patch('backend.routes.llm.stream_llm_response') as mock_stream:
        # Return an async generator
        async def mock_gen(*args, **kwargs):
            for chunk in expected_chunks:
                yield json.dumps({"text": chunk}) + "\n"
        mock_stream.side_effect = mock_gen
        response = client.post(
            "/api/v1/llm/stream",
            json={
                "prompt": test_prompt,
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 100,
                "top_p": 1.0
            }
        )
        # Parse NDJSON streaming response from response.content
        lines = response.content.splitlines()
        chunks = [json.loads(line)["text"] for line in lines if line]
        assert chunks == expected_chunks
        mock_stream.assert_called_once_with(
            test_prompt,
            model="gpt-3.5-turbo",
            temperature=0.7,
            max_tokens=100,
            top_p=1.0
        )

def test_llm_error_handling(client):
    test_prompt = "Invalid prompt"
    with patch('backend.routes.llm.get_llm_response') as mock_llm:
        mock_llm.side_effect = Exception("LLM service error")
        response = client.post(
            "/api/v1/llm/completion",
            json={
                "prompt": test_prompt,
                "model": "gpt-3.5-turbo",
                "temperature": 0.7,
                "max_tokens": 100,
                "top_p": 1.0
            }
        )
        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert "detail" in response.json()

def test_llm_model_selection(client):
    test_prompt = "Test prompt"
    model_name = "gpt-4"
    with patch('backend.routes.llm.get_llm_response') as mock_llm:
        mock_llm.return_value = "Test response"
        response = client.post(
            "/api/v1/llm/completion",
            json={
                "prompt": test_prompt,
                "model": model_name,
                "temperature": 0.7,
                "max_tokens": 100,
                "top_p": 1.0
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["text"] == "Test response"
        assert data["model"] == model_name
        mock_llm.assert_called_once_with(
            test_prompt,
            model=model_name,
            temperature=0.7,
            max_tokens=100,
            top_p=1.0
        )

def test_llm_parameters(client):
    test_prompt = "Test prompt"
    parameters = {
        "temperature": 0.8,
        "max_tokens": 200,
        "top_p": 0.9
    }
    with patch('backend.routes.llm.get_llm_response') as mock_llm:
        mock_llm.return_value = "Test response"
        response = client.post(
            "/api/v1/llm/completion",
            json={
                "prompt": test_prompt,
                "model": "gpt-3.5-turbo",
                **parameters
            }
        )
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert data["text"] == "Test response"
        mock_llm.assert_called_once_with(
            test_prompt,
            model="gpt-3.5-turbo",
            temperature=parameters["temperature"],
            max_tokens=parameters["max_tokens"],
            top_p=parameters["top_p"]
        ) 