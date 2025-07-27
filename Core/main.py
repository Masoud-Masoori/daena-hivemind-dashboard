from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
from typing import Dict, List, Optional
import os
import sys

# Add the project root to Python path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our core components
from Agents.core import PsychologicalTechniques, DaenaConsultation, DaenaTTS

app = FastAPI(title="Daena API", version="1.0.0")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, replace with specific origins
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize core components
psychological_techniques = PsychologicalTechniques()
daena_consultation = DaenaConsultation()
daena_tts = DaenaTTS()

@app.get("/")
async def root():
    return {"message": "Welcome to Daena API", "status": "operational"}

@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "components": {
            "psychological_techniques": "operational",
            "daena_consultation": "operational",
            "daena_tts": "operational"
        }
    }

@app.post("/consultation/start")
async def start_consultation(pod_id: str, consultation_type: str):
    try:
        result = daena_consultation.start_consultation(pod_id, consultation_type)
        return {"status": "success", "data": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/tts/synthesize")
async def synthesize_speech(text: str, voice_profile: str = "default", emotion: Optional[str] = None):
    try:
        output_file = await daena_tts.synthesize_speech(text, voice_profile, emotion)
        return {"status": "success", "output_file": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/techniques/list")
async def list_techniques():
    try:
        techniques = psychological_techniques.list_techniques()
        return {"status": "success", "data": techniques}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True) 