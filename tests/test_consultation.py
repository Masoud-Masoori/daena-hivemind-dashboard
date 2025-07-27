import pytest
from fastapi import status
from datetime import datetime, timedelta, timezone
from unittest.mock import patch, MagicMock

def test_create_consultation(client, test_user):
    consultation_data = {
        "userId": test_user["username"],
        "topic": "Test Consultation",
        "startTime": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat(),
        "duration": 30  # minutes
    }
    
    response = client.post(
        "/api/v1/consultation/",
        json=consultation_data
    )
    if response.status_code != status.HTTP_201_CREATED:
        print(f"Test create consultation failed with status {response.status_code}: {response.text}")
    print(f"Consultation create response: {response.json()}")
    assert response.status_code == status.HTTP_201_CREATED
    assert response.json()["topic"] == consultation_data["topic"]
    assert "id" in response.json()

def test_get_consultation(client, test_user):
    # First create a consultation
    consultation_data = {
        "userId": test_user["username"],
        "topic": "Test Consultation",
        "startTime": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }
    
    create_response = client.post(
        "/api/v1/consultation/",
        json=consultation_data
    )
    if create_response.status_code != status.HTTP_201_CREATED:
        print(f"Create consultation failed in test_get_consultation: {create_response.status_code} - {create_response.text}")
    consultation_id = create_response.json()["id"]
    
    # Then get it
    response = client.get(f"/api/v1/consultation/{consultation_id}")
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["id"] == consultation_id
    assert response.json()["topic"] == consultation_data["topic"]

def test_update_consultation(client, test_user):
    # First create a consultation
    consultation_data = {
        "userId": test_user["username"],
        "topic": "Original Topic",
        "startTime": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }
    
    create_response = client.post(
        "/api/v1/consultation/",
        json=consultation_data
    )
    if create_response.status_code != status.HTTP_201_CREATED:
        print(f"Create consultation failed in test_update_consultation: {create_response.status_code} - {create_response.text}")
    consultation_id = create_response.json()["id"]
    
    # Update it
    update_data = {
        "topic": "Updated Topic",
        "notes": "Some notes"
    }
    
    response = client.patch(
        f"/api/v1/consultation/{consultation_id}",
        json=update_data
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["topic"] == update_data["topic"]
    assert response.json()["notes"] == update_data["notes"]

def test_cancel_consultation(client, test_user):
    # First create a consultation
    consultation_data = {
        "userId": test_user["username"],
        "topic": "Test Consultation",
        "startTime": (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    }
    
    create_response = client.post(
        "/api/v1/consultation/",
        json=consultation_data
    )
    if create_response.status_code != status.HTTP_201_CREATED:
        print(f"Create consultation failed in test_cancel_consultation: {create_response.status_code} - {create_response.text}")
    consultation_id = create_response.json()["id"]
    
    # Cancel it
    response = client.post(
        f"/api/v1/consultation/{consultation_id}/cancel"
    )
    
    assert response.status_code == status.HTTP_200_OK
    assert response.json()["status"] == "cancelled"

def test_consultation_validation(client, test_user):
    # Test past start time
    past_time = (datetime.now(timezone.utc) - timedelta(hours=1)).isoformat()
    response = client.post(
        "/api/v1/consultation/",
        json={
            "userId": test_user["username"],
            "topic": "Test",
            "startTime": past_time
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Test missing required fields
    response = client.post(
        "/api/v1/consultation/",
        json={
            "userId": test_user["username"]
            # Missing topic and startTime
        }
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_consultation_scheduling(client, test_user):
    # Test scheduling conflict
    start_time = (datetime.now(timezone.utc) + timedelta(hours=1)).isoformat()
    
    # Create first consultation
    consultation1 = {
        "userId": test_user["username"],
        "topic": "First Consultation",
        "startTime": start_time,
        "duration": 60
    }
    client.post("/api/v1/consultation/", json=consultation1)
    
    # Try to create overlapping consultation
    consultation2 = {
        "userId": test_user["username"],
        "topic": "Second Consultation",
        "startTime": start_time,
        "duration": 30
    }
    response = client.post("/api/v1/consultation/", json=consultation2)
    
    assert response.status_code == status.HTTP_409_CONFLICT
    assert "scheduling conflict" in response.json()["detail"].lower() 