from fastapi import APIRouter

router = APIRouter()

@router.get("/agents")
def list_agents():
    return {"agents": ["Daena", "Guardian", "FreelanceAgent"]}
