"""
Daena AI VP Demo - Simplified Main File
Only includes demo functionality to avoid dependency issues
"""

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import os
import sys

# Add current directory to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Create FastAPI app
app = FastAPI(
    title="Daena AI VP Demo",
    description="AI Vice President Demo System",
    version="1.0.0"
)

# Mount static files
app.mount("/static", StaticFiles(directory="../frontend/static"), name="static")

# Configure templates
templates = Jinja2Templates(directory="../frontend/templates")

# Import demo routes
try:
    from routes.demo import router as demo_router
    app.include_router(demo_router, prefix="/demo")
    print("✅ Successfully included demo router")
except Exception as e:
    print(f"❌ Failed to include demo router: {e}")

# Basic health check
@app.get("/health")
async def health_check():
    """Basic health check"""
    return {
        "status": "healthy",
        "service": "Daena Demo",
        "version": "1.0.0"
    }

# Root redirect to demo
@app.get("/")
async def root():
    """Redirect to demo"""
    return {"message": "Daena AI VP Demo", "demo_url": "/demo"}

# API documentation
@app.get("/docs")
async def docs():
    """API documentation"""
    return {"message": "API documentation available at /docs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001) 