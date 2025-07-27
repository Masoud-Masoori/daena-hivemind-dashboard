import pytest
from fastapi import status
import json
import os
import tempfile
from pathlib import Path

def test_voice_synthesis(client):
    """Test text-to-speech synthesis."""
    response = client.post(
        "/api/v1/voice/synthesize",
        json={
            "text": "Hello, this is a test of Daena's voice synthesis.",
            "voice_id": "default",
            "emotion": "happy",
            "style": "neutral"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "audio_url" in data
    assert "duration" in data
    assert "voice_id" in data
    print(f"\nGenerated audio file: {data['audio_url']}")

def test_emotion_detection(client):
    """Test emotion detection from text."""
    response = client.post(
        "/api/v1/voice/detect-emotion",
        json={
            "text": "I am feeling very happy today!"
        }
    )
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert "emotion" in data
    assert "confidence" in data
    print(f"\nDetected emotion: {data['emotion']} (confidence: {data['confidence']})")

def test_style_transfer(client):
    """Test voice style transfer."""
    # Create a test audio file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(b"dummy audio content")
        temp_audio_path = temp_audio.name

    try:
        response = client.post(
            "/api/v1/voice/style-transfer",
            json={
                "audio_file": temp_audio_path,
                "target_style": "happy"
            }
        )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "transformed_audio_url" in data
        assert "original_style" in data
        assert "target_style" in data
        print(f"\nStyle transfer completed: {data['transformed_audio_url']}")
    
    finally:
        os.unlink(temp_audio_path)

def test_voice_profiles(client):
    """Test voice profile management."""
    response = client.get("/api/v1/voice/profiles")
    assert response.status_code == status.HTTP_200_OK
    data = response.json()
    assert isinstance(data, list)
    assert len(data) > 0
    assert all("id" in profile and "name" in profile and "gender" in profile for profile in data)
    print(f"\nAvailable voice profiles: {data}")

def test_voice_upload(client):
    """Test voice profile upload."""
    # Create a test audio file
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as temp_audio:
        temp_audio.write(b"dummy audio content")
        temp_audio_path = temp_audio.name

    try:
        # Test profile upload
        with open(temp_audio_path, "rb") as audio_file:
            response = client.post(
                "/api/v1/voice/upload",
                files={"file": ("test.wav", audio_file, "audio/wav")}
            )
        
        assert response.status_code == status.HTTP_200_OK
        data = response.json()
        assert "filename" in data
        assert "size" in data
        print(f"\nUploaded file: {data['filename']} (size: {data['size']} bytes)")
    
    finally:
        os.unlink(temp_audio_path) 