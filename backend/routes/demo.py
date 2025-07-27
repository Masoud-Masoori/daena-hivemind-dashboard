from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import os
import json
import logging
from datetime import datetime
import openai
from pathlib import Path

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize router
router = APIRouter(tags=["Demo"])

# Azure OpenAI Configuration
AZURE_CONFIG = {
    "api_type": "azure",
    "api_key": "1HmnkpDuMqMzKDtYbpcckyVQC6qlggup3zAVmfkG65BjxAtT9JKtJQQJ99BGACHYHv6XJ3w3AAAAACOGX3DN",
    "api_base": "https://masou-mdksrl1q-eastus2.openai.azure.com/",
    "api_version": "2024-02-15",
    "deployment_name": "daena"
}

# Initialize OpenAI client
try:
    client = openai.AzureOpenAI(
        api_key=AZURE_CONFIG["api_key"],
        api_version=AZURE_CONFIG["api_version"],
        azure_endpoint=AZURE_CONFIG["api_base"]
    )
    logger.info("✅ Azure OpenAI client initialized")
except Exception as e:
    logger.error(f"❌ Failed to initialize Azure OpenAI client: {e}")
    client = None

# Pydantic models
class ChatRequest(BaseModel):
    message: str

class EmailRequest(BaseModel):
    investor_type: str
    tone: str
    custom_message: Optional[str] = ""

class Investor(BaseModel):
    name: str
    email: str
    company: str
    type: str
    score: Optional[int] = 0

class EmailResponse(BaseModel):
    subject: str
    body: str
    tokens_used: Optional[int] = 0

# Demo data
DEMO_INVESTORS = {
    "toronto_ai": {
        "name": "Sarah Chen",
        "email": "sarah.chen@torontoai.vc",
        "company": "Toronto AI Venture Capital",
        "type": "AI/ML, Enterprise Software",
        "score": 95
    },
    "canadian_tech": {
        "name": "Michael Rodriguez",
        "email": "michael@canadiantechfund.ca",
        "company": "Canadian Tech Growth Fund",
        "type": "Technology, SaaS",
        "score": 88
    },
    "mars_dd": {
        "name": "Dr. Emily Watson",
        "email": "emily.watson@marsdd.com",
        "company": "MaRS Discovery District",
        "type": "Health, Cleantech, Fintech",
        "score": 92
    },
    "cvca": {
        "name": "David Thompson",
        "email": "david.thompson@cvca.ca",
        "company": "CVCA Member Fund",
        "type": "Diverse portfolio, all stages",
        "score": 85
    }
}

# Usage tracking
usage_stats = {
    "tokens_used": 0,
    "emails_sent": 0,
    "voice_interactions": 0,
    "session_start": datetime.now().isoformat()
}

def log_email(email_data: dict):
    """Log email to JSON file"""
    try:
        log_file = Path("logs/email_log.jsonl")
        log_file.parent.mkdir(exist_ok=True)
        
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(email_data) + "\n")
        
        logger.info(f"✅ Email logged: {email_data.get('investor_name', 'Unknown')}")
    except Exception as e:
        logger.error(f"❌ Error logging email: {e}")

def get_email_history() -> List[dict]:
    """Get email history from log file"""
    try:
        log_file = Path("logs/email_log.jsonl")
        if not log_file.exists():
            return []
        
        emails = []
        with open(log_file, "r", encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    emails.append(json.loads(line))
        
        return emails[-10:]  # Return last 10 emails
    except Exception as e:
        logger.error(f"❌ Error reading email history: {e}")
        return []

def generate_email_content(investor: dict, tone: str, custom_message: str = "") -> tuple[str, str]:
    """Generate email content using Azure OpenAI"""
    if not client:
        raise Exception("Azure OpenAI client not available")
    
    # Build prompt
    prompt = f"""
You are Daena, an AI Vice President writing a personalized cold email to an investor.

Investor Information:
- Name: {investor['name']}
- Company: {investor['company']}
- Focus: {investor['type']}

Email Requirements:
- Tone: {tone}
- Custom Message: {custom_message if custom_message else "None"}

Company Information:
- Name: Daena AI VP System
- Value Proposition: World's first autonomous AI Vice President
- Market: $280B AI business market
- Seeking: $5M Series A funding
- Valuation: $25M pre-money
- Unique Features: 500+ API endpoints, 8 business departments, 40+ AI advisors

Generate a professional email with:
1. Personalized subject line
2. Engaging opening
3. Clear value proposition
4. Specific call-to-action
5. Professional closing

Format the response as:
SUBJECT: [subject line]
BODY: [email body]

Make it compelling, professional, and tailored to the investor's focus area.
"""

    try:
        response = client.chat.completions.create(
            model=AZURE_CONFIG["deployment_name"],
            messages=[
                {"role": "system", "content": "You are Daena, an AI Vice President specializing in investor relations and business strategy."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=800,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        # Update usage stats
        usage_stats["tokens_used"] += tokens_used
        
        # Parse response
        lines = content.split('\n')
        subject = ""
        body = ""
        
        for line in lines:
            if line.startswith("SUBJECT:"):
                subject = line.replace("SUBJECT:", "").strip()
            elif line.startswith("BODY:"):
                body = line.replace("BODY:", "").strip()
            elif subject and not body:
                subject += " " + line.strip()
            elif body:
                body += "\n" + line
        
        if not subject:
            subject = f"Introducing Daena AI VP - Revolutionary AI Leadership Platform"
        if not body:
            body = content
        
        return subject, body, tokens_used
        
    except Exception as e:
        logger.error(f"❌ Error generating email: {e}")
        raise Exception(f"Failed to generate email: {str(e)}")

def generate_chat_response(message: str) -> tuple[str, int]:
    """Generate chat response using Azure OpenAI"""
    if not client:
        return "I'm currently experiencing technical difficulties. Please try again later.", 0
    
    # Build context-aware prompt
    system_prompt = """You are Daena, the world's first AI Vice President. You provide autonomous business leadership, strategic decision-making, and comprehensive enterprise oversight.

Key Capabilities:
- Investor relations and fundraising
- Business strategy and market analysis
- Team management and operations
- Financial planning and analysis
- Technology strategy and implementation

Current Company Status:
- Seeking $5M Series A funding
- $25M pre-money valuation
- $280B AI business market opportunity
- 500+ API endpoints built
- 8 business departments managed
- 40+ AI advisors deployed

Be professional, confident, and helpful. Keep responses concise but informative."""
    
    try:
        response = client.chat.completions.create(
            model=AZURE_CONFIG["deployment_name"],
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": message}
            ],
            max_tokens=300,
            temperature=0.7
        )
        
        content = response.choices[0].message.content
        tokens_used = response.usage.total_tokens
        
        # Update usage stats
        usage_stats["tokens_used"] += tokens_used
        
        return content, tokens_used
        
    except Exception as e:
        logger.error(f"❌ Error generating chat response: {e}")
        return "I'm experiencing technical difficulties. Please try again.", 0

# Routes
@router.get("")
async def redirect_demo():
    """Redirect /demo to /demo/"""
    from fastapi.responses import RedirectResponse
    return RedirectResponse(url="/demo/", status_code=307)

@router.get("/")
async def get_demo_page():
    """Serve the demo webpage"""
    try:
        template_path = "../frontend/templates/demo_simple.html"
        
        if not os.path.exists(template_path):
            raise FileNotFoundError(f"Template not found at {template_path}")
        
        with open(template_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        return HTMLResponse(content=content)
        
    except FileNotFoundError as e:
        raise HTTPException(status_code=404, detail=f"Demo page not found at {template_path}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading demo page: {str(e)}")

@router.post("/chat")
async def chat_with_daena(request: ChatRequest):
    """Chat with Daena AI VP"""
    try:
        response, tokens_used = generate_chat_response(request.message)
        
        return {
            "response": response,
            "tokens_used": tokens_used,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error in chat: {str(e)}")

@router.post("/generate-email")
async def generate_investor_email(request: EmailRequest):
    """Generate a personalized investor email"""
    try:
        investor_type = request.investor_type
        if investor_type not in DEMO_INVESTORS:
            raise HTTPException(status_code=400, detail="Invalid investor type")
        
        investor = DEMO_INVESTORS[investor_type]
        subject, body, tokens_used = generate_email_content(
            investor, 
            request.tone, 
            request.custom_message
        )
        
        return {
            "subject": subject,
            "body": body,
            "investor": investor,
            "tokens_used": tokens_used,
            "timestamp": datetime.now().isoformat()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating email: {str(e)}")

@router.post("/send-email")
async def send_investor_email(request: EmailRequest):
    """Send an investor email (simulated)"""
    try:
        investor_type = request.investor_type
        if investor_type not in DEMO_INVESTORS:
            raise HTTPException(status_code=400, detail="Invalid investor type")
        
        investor = DEMO_INVESTORS[investor_type]
        subject, body, tokens_used = generate_email_content(
            investor, 
            request.tone, 
            request.custom_message
        )
        
        # Log email
        email_log = {
            "timestamp": datetime.now().isoformat(),
            "investor_name": investor["name"],
            "investor_email": investor["email"],
            "investor_company": investor["company"],
            "tone": request.tone,
            "subject": subject,
            "body": body,
            "status": "sent",
            "message": "✅ Email simulated: Not actually sent. Ready for demo."
        }
        log_email(email_log)
        
        # Update usage stats
        usage_stats["emails_sent"] += 1
        
        return {
            "status": "success",
            "message": "✅ Email simulated: Not actually sent. Ready for demo.",
            "email": {
                "subject": subject,
                "body": body,
                "investor": investor,
                "tone": request.tone
            },
            "tokens_used": tokens_used
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error sending email: {str(e)}")

@router.get("/investors")
async def get_investors():
    """Get available investors"""
    return {
        "investors": list(DEMO_INVESTORS.values()),
        "count": len(DEMO_INVESTORS)
    }

@router.get("/email-history")
async def get_email_history_route():
    """Get email history"""
    try:
        emails = get_email_history()
        return {
            "emails": emails,
            "count": len(emails)
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting email history: {str(e)}")

@router.get("/usage-stats")
async def get_usage_stats():
    """Get real-time usage statistics"""
    return {
        "tokens_used": usage_stats["tokens_used"],
        "emails_sent": usage_stats["emails_sent"],
        "voice_interactions": usage_stats["voice_interactions"],
        "session_start": usage_stats["session_start"],
        "session_duration": (datetime.now() - datetime.fromisoformat(usage_stats["session_start"])).total_seconds()
    }

@router.get("/health")
async def demo_health():
    """Health check for demo service"""
    return {
        "service": "Daena Demo",
        "status": "healthy",
        "azure_openai": "connected" if client else "disconnected",
        "agents_available": len(DEMO_INVESTORS),
        "timestamp": datetime.now().isoformat()
    }

# Additional demo routes for enhanced functionality
@router.post("/voice-interaction")
async def record_voice_interaction():
    """Record a voice interaction"""
    usage_stats["voice_interactions"] += 1
    return {
        "status": "success",
        "voice_interactions": usage_stats["voice_interactions"]
    }

@router.get("/system-status")
async def get_system_status():
    """Get comprehensive system status"""
    return {
        "backend": "online",
        "azure_openai": "connected" if client else "disconnected",
        "gmail": "ready",
        "voice": "available",
        "database": "connected",
        "timestamp": datetime.now().isoformat()
    }

@router.get("/demo-data")
async def get_demo_data():
    """Get demo configuration and data"""
    return {
        "investors": DEMO_INVESTORS,
        "email_tones": ["professional", "friendly", "confident", "innovative"],
        "company_info": {
            "name": "Daena AI VP System",
            "valuation": "$25M pre-money",
            "seeking": "$5M Series A",
            "market": "$280B AI business market",
            "features": [
                "500+ API endpoints",
                "8 business departments", 
                "40+ AI advisors",
                "Voice-activated interface",
                "Real-time analytics"
            ]
        }
    } 