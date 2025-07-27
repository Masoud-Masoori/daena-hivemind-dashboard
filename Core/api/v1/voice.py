from fastapi import APIRouter
from Agents.core.daena_tts import DaenaTTS

router = APIRouter()

# Add placeholder endpoints or import actual routes here later
# @router.get("/voice/profiles")
# async def get_voice_profiles():
#     return []

@router.get("/profiles")
async def get_voice_profiles():
    tts_system = DaenaTTS()
    return tts_system.get_available_voices() 