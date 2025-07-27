import pytest
from fastapi import status, HTTPException
from fastapi.testclient import TestClient
from backend.main import app
from datetime import datetime, timedelta, timezone

def test_healthcheck(client):
    response = client.get("/")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "healthy"
    assert "version" in response.json()
    assert "service" in response.json()

def test_rate_limit():
    # Create a client without the test API key
    test_client = TestClient(app)
    
    # Make requests up to the limit
    for _ in range(60):  # Up to the limit
        response = test_client.get("/")
        assert response.status_code == status.HTTP_200_OK

    # The next request should trigger the rate limit
    with pytest.raises(HTTPException) as excinfo:
        test_client.get("/")
    assert excinfo.value.status_code == status.HTTP_429_TOO_MANY_REQUESTS
    assert "Too many requests" in excinfo.value.detail

def test_websocket_connection(client):
    with client.websocket_connect("/ws") as websocket:
        # Test sending a message
        websocket.send_text('{"message": "test"}')
        response = websocket.receive_text()
        assert "Echo" in response

def test_agent_endpoints(client, test_agent):
    # Test creating an agent
    response = client.post(
        "/api/v1/agents/",
        json=test_agent
    )
    assert response.status_code == status.HTTP_201_CREATED
    agent_id = response.json()["id"]
    
    # Test getting the agent
    response = client.get(f"/api/v1/agents/{agent_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == test_agent["name"]
    
    # Test updating the agent
    update_data = {"name": "UpdatedAgent"}
    response = client.patch(
        f"/api/v1/agents/{agent_id}",
        json=update_data
    )
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["name"] == "UpdatedAgent"
    
    # Test deleting the agent
    response = client.delete(f"/api/v1/agents/{agent_id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT

def test_voice_endpoints(client):
    # Test voice synthesis
    test_text = "Hello, this is a test."
    response = client.post(
        "/api/v1/voice/synthesize",
        json={"text": test_text}
    )
    assert response.status_code == status.HTTP_200_OK
    assert "audio_url" in response.json()

def test_consultation_endpoints(client, test_user):
    # Test creating a consultation
    consultation_data = {
        "userId": test_user["username"],
        "topic": "Test Consultation",
        "startTime": (datetime.now(timezone.utc) + timedelta(minutes=5)).isoformat() # Ensure future and timezone aware
    }
    response = client.post(
        "/api/v1/consultation/",
        json=consultation_data
    )
    if response.status_code != status.HTTP_201_CREATED:
        print(f"Consultation creation failed with status {response.status_code}: {response.text}")
    assert response.status_code == status.HTTP_201_CREATED
    consultation_id = response.json()["id"]
    
    # Test getting consultation status
    response = client.get(f"/api/v1/consultation/{consultation_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["topic"] == consultation_data["topic"] 