from fastapi import APIRouter

router = APIRouter()

@router.get("/profiles")
async def voice_profiles():
    return {"voices": ["daena_default", "swift_like"]}
