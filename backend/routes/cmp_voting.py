from fastapi import APIRouter, HTTPException, BackgroundTasks
from typing import List, Optional, Dict, Any
from pydantic import BaseModel, ConfigDict
import json
import asyncio
import uuid
from datetime import datetime
import hashlib

router = APIRouter(prefix="/cmp-voting", tags=["CMP LLM Voting System"])

# CMP Voting Models
class LLMVote(BaseModel):
    model_config = ConfigDict(protected_namespaces=())
    
    model_name: str  # "gpt-4", "claude-3", "yi-34b"
    response: str
    confidence_score: float
    reasoning: str
    timestamp: datetime
    processing_time: float
    cost: Optional[float] = None

class CMPVotingSession(BaseModel):
    id: str
    question: str
    context: Optional[str] = None
    models_consulted: List[str]
    votes: List[LLMVote]
    daena_summary: Optional[str] = None
    consensus_decision: Optional[str] = None
    confidence_threshold: float = 0.7
    status: str  # "pending", "voting", "completed", "failed"
    created_at: datetime
    completed_at: Optional[datetime] = None
    web3_transaction_hash: Optional[str] = None

class VotingResult(BaseModel):
    session_id: str
    question: str
    individual_votes: List[LLMVote]
    consensus_decision: str
    daena_summary: str
    confidence_score: float
    agreement_level: str  # "high", "medium", "low"
    timestamp: datetime

# Mock LLM responses for demonstration
async def simulate_llm_response(model_name: str, question: str) -> LLMVote:
    """Simulate LLM response for demonstration"""
    await asyncio.sleep(0.5)  # Simulate processing time
    
    responses = {
        "gpt-4": {
            "response": f"GPT-4 Analysis: {question} requires strategic consideration with focus on scalability and market positioning.",
            "reasoning": "Based on current market trends and technological capabilities, this approach aligns with best practices.",
            "confidence": 0.92
        },
        "claude-3": {
            "response": f"Claude-3 Analysis: {question} should be evaluated through the lens of ethical AI deployment and long-term sustainability.",
            "reasoning": "Considering the ethical implications and long-term impact on stakeholders, this direction shows promise.",
            "confidence": 0.88
        },
        "yi-34b": {
            "response": f"Yi-34B Analysis: {question} presents opportunities for innovation and competitive advantage in emerging markets.",
            "reasoning": "From a technical and market perspective, this initiative aligns with current industry trajectories.",
            "confidence": 0.85
        }
    }
    
    model_response = responses.get(model_name, {
        "response": f"{model_name} Analysis: {question} requires further investigation.",
        "reasoning": "Standard analysis approach recommended.",
        "confidence": 0.75
    })
    
    return LLMVote(
        model_name=model_name,
        response=model_response["response"],
        confidence_score=model_response["confidence"],
        reasoning=model_response["reasoning"],
        timestamp=datetime.now(),
        processing_time=0.5,
        cost=0.02
    )

async def generate_daena_summary(votes: List[LLMVote], question: str) -> str:
    """Generate Daena's summary based on LLM votes"""
    # Analyze consensus and generate executive summary
    avg_confidence = sum(v.confidence_score for v in votes) / len(votes)
    
    # Determine agreement level
    if avg_confidence > 0.85:
        agreement = "high"
    elif avg_confidence > 0.75:
        agreement = "medium"
    else:
        agreement = "low"
    
    summary = f"""Daena Executive Summary:

Question: {question}

LLM Consensus Analysis:
- Models Consulted: {', '.join(v.model_name for v in votes)}
- Average Confidence: {avg_confidence:.2f}
- Agreement Level: {agreement.title()}

Key Insights:
{chr(10).join(f"• {v.model_name}: {v.response[:100]}..." for v in votes)}

Executive Recommendation:
Based on the consensus analysis, I recommend proceeding with this initiative with {agreement} confidence. The models show {agreement} agreement on the strategic direction.

Next Steps:
1. Implement the recommended approach
2. Monitor progress and adjust as needed
3. Schedule follow-up review in 30 days"""
    
    return summary

# Mock storage for voting sessions
voting_sessions: Dict[str, CMPVotingSession] = {}

@router.post("/session")
async def create_voting_session(
    question: str,
    context: Optional[str] = None,
    models: List[str] = ["gpt-4", "claude-3", "yi-34b"],
    confidence_threshold: float = 0.7
) -> Dict[str, Any]:
    """Create a new CMP voting session"""
    session_id = f"cmp-{uuid.uuid4().hex[:8]}"
    
    session = CMPVotingSession(
        id=session_id,
        question=question,
        context=context,
        models_consulted=models,
        votes=[],
        confidence_threshold=confidence_threshold,
        status="pending",
        created_at=datetime.now()
    )
    
    voting_sessions[session_id] = session
    
    return {
        "session_id": session_id,
        "message": "Voting session created",
        "session": session
    }

@router.post("/session/{session_id}/vote")
async def trigger_voting(session_id: str, background_tasks: BackgroundTasks) -> Dict[str, Any]:
    """Trigger the voting process for all models"""
    if session_id not in voting_sessions:
        raise HTTPException(status_code=404, detail="Voting session not found")
    
    session = voting_sessions[session_id]
    session.status = "voting"
    
    # Start background voting process
    background_tasks.add_task(execute_voting, session_id)
    
    return {
        "session_id": session_id,
        "message": "Voting process initiated",
        "status": "voting"
    }

async def execute_voting(session_id: str):
    """Execute voting process for all models"""
    session = voting_sessions[session_id]
    
    try:
        # Collect votes from all models concurrently
        voting_tasks = [
            simulate_llm_response(model, session.question)
            for model in session.models_consulted
        ]
        
        votes = await asyncio.gather(*voting_tasks)
        session.votes = votes
        
        # Generate Daena summary
        session.daena_summary = await generate_daena_summary(votes, session.question)
        
        # Determine consensus
        avg_confidence = sum(v.confidence_score for v in votes) / len(votes)
        session.consensus_decision = "approved" if avg_confidence >= session.confidence_threshold else "requires_review"
        
        session.status = "completed"
        session.completed_at = datetime.now()
        
        # Generate Web3 transaction hash
        consensus_data = {
            "session_id": session_id,
            "question": session.question,
            "votes": [v.model_dump() for v in votes],
            "consensus": session.consensus_decision,
            "timestamp": session.completed_at.isoformat()
        }
        session.web3_transaction_hash = hashlib.sha256(
            json.dumps(consensus_data, sort_keys=True).encode()
        ).hexdigest()
        
    except Exception as e:
        session.status = "failed"
        print(f"Voting failed for session {session_id}: {e}")

@router.get("/session/{session_id}")
async def get_voting_session(session_id: str) -> CMPVotingSession:
    """Get voting session details"""
    if session_id not in voting_sessions:
        raise HTTPException(status_code=404, detail="Voting session not found")
    
    return voting_sessions[session_id]

@router.get("/sessions")
async def get_all_voting_sessions() -> Dict[str, Any]:
    """Get all voting sessions"""
    return {
        "sessions": list(voting_sessions.values()),
        "total_sessions": len(voting_sessions),
        "completed_sessions": len([s for s in voting_sessions.values() if s.status == "completed"]),
        "pending_sessions": len([s for s in voting_sessions.values() if s.status == "pending"])
    }

@router.get("/session/{session_id}/result")
async def get_voting_result(session_id: str) -> VotingResult:
    """Get detailed voting result"""
    if session_id not in voting_sessions:
        raise HTTPException(status_code=404, detail="Voting session not found")
    
    session = voting_sessions[session_id]
    
    if session.status != "completed":
        raise HTTPException(status_code=400, detail="Voting session not completed")
    
    avg_confidence = sum(v.confidence_score for v in session.votes) / len(session.votes)
    
    if avg_confidence > 0.85:
        agreement_level = "high"
    elif avg_confidence > 0.75:
        agreement_level = "medium"
    else:
        agreement_level = "low"
    
    return VotingResult(
        session_id=session_id,
        question=session.question,
        individual_votes=session.votes,
        consensus_decision=session.consensus_decision,
        daena_summary=session.daena_summary,
        confidence_score=avg_confidence,
        agreement_level=agreement_level,
        timestamp=session.completed_at
    )

@router.post("/session/{session_id}/override")
async def override_voting_result(
    session_id: str,
    override_decision: str,
    reason: str
) -> Dict[str, Any]:
    """Override voting result (founder/admin only)"""
    if session_id not in voting_sessions:
        raise HTTPException(status_code=404, detail="Voting session not found")
    
    session = voting_sessions[session_id]
    session.consensus_decision = override_decision
    
    # Add override note to summary
    override_note = f"\n\nOVERRIDE APPLIED:\nDecision: {override_decision}\nReason: {reason}\nTimestamp: {datetime.now().isoformat()}"
    session.daena_summary += override_note
    
    return {
        "session_id": session_id,
        "message": "Voting result overridden",
        "new_decision": override_decision,
        "reason": reason
    }

@router.get("/analytics")
async def get_voting_analytics() -> Dict[str, Any]:
    """Get voting analytics"""
    completed_sessions = [s for s in voting_sessions.values() if s.status == "completed"]
    
    if not completed_sessions:
        return {
            "total_sessions": 0,
            "average_confidence": 0,
            "consensus_breakdown": {},
            "model_performance": {}
        }
    
    # Calculate analytics
    total_sessions = len(completed_sessions)
    avg_confidence = sum(
        sum(v.confidence_score for v in s.votes) / len(s.votes)
        for s in completed_sessions
    ) / total_sessions
    
    consensus_breakdown = {}
    for session in completed_sessions:
        decision = session.consensus_decision
        consensus_breakdown[decision] = consensus_breakdown.get(decision, 0) + 1
    
    # Model performance analysis
    model_performance = {}
    for session in completed_sessions:
        for vote in session.votes:
            if vote.model_name not in model_performance:
                model_performance[vote.model_name] = {
                    "total_votes": 0,
                    "total_confidence": 0,
                    "average_processing_time": 0
                }
            
            model_performance[vote.model_name]["total_votes"] += 1
            model_performance[vote.model_name]["total_confidence"] += vote.confidence_score
            model_performance[vote.model_name]["average_processing_time"] += vote.processing_time
    
    # Calculate averages
    for model in model_performance:
        total_votes = model_performance[model]["total_votes"]
        model_performance[model]["average_confidence"] = model_performance[model]["total_confidence"] / total_votes
        model_performance[model]["average_processing_time"] = model_performance[model]["average_processing_time"] / total_votes
    
    return {
        "total_sessions": total_sessions,
        "average_confidence": avg_confidence,
        "consensus_breakdown": consensus_breakdown,
        "model_performance": model_performance
    } 