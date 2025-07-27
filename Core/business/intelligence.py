from typing import Dict, List, Optional
from datetime import datetime
import json
import os
from core.cmp.cmp_decision_gate import verify_risk
from memory.secure_recall import log_event

class BusinessIntelligence:
    def __init__(self):
        self.opportunities_db = "D:/Ideas/Daena/memory/vaults/opportunities.json"
        self.ensure_db_exists()

    def ensure_db_exists(self):
        if not os.path.exists(self.opportunities_db):
            with open(self.opportunities_db, 'w') as f:
                json.dump([], f)

    def detect_opportunity(self, market_data: Dict) -> Optional[Dict]:
        """Analyze market data to detect business opportunities."""
        try:
            # Implement opportunity detection logic
            opportunity = {
                "id": f"opp_{datetime.now().strftime('%Y%m%d%H%M%S')}",
                "title": market_data.get("title", "Untitled Opportunity"),
                "description": market_data.get("description", ""),
                "potential_revenue": market_data.get("revenue", 0),
                "risk_score": market_data.get("risk", 0.5),
                "departments": market_data.get("departments", []),
                "created_at": datetime.now().isoformat(),
                "status": "pending_review"
            }

            if verify_risk(opportunity):
                self.save_opportunity(opportunity)
                log_event("business_intelligence", {
                    "action": "opportunity_detected",
                    "opportunity_id": opportunity["id"]
                })
                return opportunity
            return None
        except Exception as e:
            log_event("business_intelligence", {
                "action": "error",
                "error": str(e)
            })
            return None

    def save_opportunity(self, opportunity: Dict):
        """Save detected opportunity to the database."""
        try:
            with open(self.opportunities_db, 'r') as f:
                opportunities = json.load(f)
            
            opportunities.append(opportunity)
            
            with open(self.opportunities_db, 'w') as f:
                json.dump(opportunities, f, indent=2)
        except Exception as e:
            log_event("business_intelligence", {
                "action": "save_error",
                "error": str(e)
            })

    def analyze_cost_benefit(self, opportunity: Dict) -> Dict:
        """Analyze cost-benefit ratio for an opportunity."""
        try:
            # Implement cost-benefit analysis
            costs = opportunity.get("costs", 0)
            benefits = opportunity.get("potential_revenue", 0)
            
            analysis = {
                "opportunity_id": opportunity["id"],
                "cost_benefit_ratio": benefits / costs if costs > 0 else float('inf'),
                "roi": ((benefits - costs) / costs) * 100 if costs > 0 else float('inf'),
                "payback_period": costs / (benefits / 12) if benefits > 0 else float('inf'),
                "analysis_date": datetime.now().isoformat()
            }
            
            log_event("business_intelligence", {
                "action": "cost_benefit_analysis",
                "opportunity_id": opportunity["id"],
                "analysis": analysis
            })
            
            return analysis
        except Exception as e:
            log_event("business_intelligence", {
                "action": "analysis_error",
                "error": str(e)
            })
            return {}

    def get_pending_opportunities(self) -> List[Dict]:
        """Retrieve all pending opportunities."""
        try:
            with open(self.opportunities_db, 'r') as f:
                opportunities = json.load(f)
            return [opp for opp in opportunities if opp["status"] == "pending_review"]
        except Exception as e:
            log_event("business_intelligence", {
                "action": "retrieve_error",
                "error": str(e)
            })
            return []

    def update_opportunity_status(self, opportunity_id: str, new_status: str):
        """Update the status of an opportunity."""
        try:
            with open(self.opportunities_db, 'r') as f:
                opportunities = json.load(f)
            
            for opp in opportunities:
                if opp["id"] == opportunity_id:
                    opp["status"] = new_status
                    opp["updated_at"] = datetime.now().isoformat()
                    break
            
            with open(self.opportunities_db, 'w') as f:
                json.dump(opportunities, f, indent=2)
            
            log_event("business_intelligence", {
                "action": "status_update",
                "opportunity_id": opportunity_id,
                "new_status": new_status
            })
        except Exception as e:
            log_event("business_intelligence", {
                "action": "update_error",
                "error": str(e)
            }) 