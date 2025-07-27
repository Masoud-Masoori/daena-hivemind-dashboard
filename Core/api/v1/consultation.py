from fastapi import APIRouter
from Agents.core.daena_consultation import DaenaConsultation

router = APIRouter()

# Add placeholder endpoints or import actual routes here later
# @router.get("/consultation/history")
# async def get_consultation_history():
#     return []

@router.get("/history")
async def get_consultation_history():
    consultation_system = DaenaConsultation()
    return consultation_system.consultation_history 