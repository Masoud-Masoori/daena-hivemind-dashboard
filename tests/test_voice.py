import pytest
from fastapi import status
from unittest.mock import patch, MagicMock
import os
import tempfile

def test_voice_synthesis(client):
    test_text = "Hello, this is a test message."
    expected_audio_path = "/tmp/test_audio.wav"
    
    # Mock the voice synthesis
    with patch('backend.routes.voice.synthesize_speech') as mock_synth:
        mock_synth.return_value = expected_audio_path
        
        response = client.post(
            "/api/v1/voice/synthesize",
            json={"text": test_text}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert "audio_url" in response.json()
        mock_synth.assert_called_once_with(test_text)

def test_voice_emotion(client):
    test_text = "I am happy!"
    emotion = "happy"
    
    # Mock emotion detection
    with patch('backend.routes.voice.detect_emotion') as mock_emotion:
        mock_emotion.return_value = emotion
        
        response = client.post(
            "/api/v1/voice/detect-emotion",
            json={"text": test_text}
        )
        
        assert response.status_code == status.HTTP_200_OK
        assert response.json()["emotion"] == emotion
        mock_emotion.assert_called_once_with(test_text)

def test_voice_style_transfer(client):
    test_audio = "test_audio.wav"
    target_style = "professional"

    # Create a temporary audio file
    with open(test_audio, "wb") as f:
        f.write(b"RIFF....WAVEfmt ")  # Minimal WAV header

    try:
        # Mock style transfer
        with patch('backend.routes.voice.transfer_voice_style') as mock_transfer:
            mock_transfer.return_value = "transformed_audio.wav"

            response = client.post(
                "/api/v1/voice/style-transfer",
                json={
                    "audio_file": test_audio,
                    "target_style": target_style
                }
            )

            assert response.status_code == status.HTTP_200_OK
            assert "transformed_audio_url" in response.json()
            mock_transfer.assert_called_once_with(test_audio, target_style)
    finally:
        if os.path.exists(test_audio):
            os.remove(test_audio)

def test_voice_validation(client):
    # Test empty text
    response = client.post(
        "/api/v1/voice/synthesize",
        json={"text": ""}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    
    # Test text too long
    long_text = "a" * 1001  # Assuming 1000 is max length
    response = client.post(
        "/api/v1/voice/synthesize",
        json={"text": long_text}
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY

def test_voice_file_handling(client):
    # Test invalid file format
    response = client.post(
        "/api/v1/voice/style-transfer",
        json={
            "audio_file": "test.txt",
            "target_style": "professional"
        }
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST
    
    # Test file not found
    response = client.post(
        "/api/v1/voice/style-transfer",
        json={
            "audio_file": "nonexistent.wav",
            "target_style": "professional"
        }
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND 