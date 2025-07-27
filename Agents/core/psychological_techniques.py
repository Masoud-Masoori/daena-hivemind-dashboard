import os
import json
import numpy as np
from datetime import datetime
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModel
import networkx as nx
from collections import defaultdict
from ..common import AgentBase, AgentType

class PsychologicalTechniques(AgentBase):
    def __init__(self):
        super().__init__(AgentType.CORE)
        self.config = self.load_config()
        self.techniques = {}
        self.initialize_techniques()
        self.team_collaborations = {}
        
    def load_config(self):
        config_file = "psychological_techniques_config.json"
        default_config = {
            "techniques": {
                "persuasion": {
                    "reciprocity": {
                        "description": "Give before you take",
                        "implementation": "Offer value before asking for something",
                        "success_metrics": ["response_rate", "engagement_level"],
                        "team_integration": ["marketing", "sales", "hr"]
                    },
                    "commitment_consistency": {
                        "description": "Get small commitments that lead to larger ones",
                        "implementation": "Start with small agreements",
                        "success_metrics": ["commitment_rate", "follow_through"],
                        "team_integration": ["product_dev", "finance", "hr"]
                    },
                    "social_proof": {
                        "description": "Show others' success stories",
                        "implementation": "Share relevant case studies",
                        "success_metrics": ["adoption_rate", "trust_level"],
                        "team_integration": ["marketing", "sales", "product_dev"]
                    }
                },
                "negotiation": {
                    "anchoring": {
                        "description": "Set initial reference points",
                        "implementation": "Present initial terms strategically",
                        "success_metrics": ["agreement_rate", "value_achieved"],
                        "team_integration": ["sales", "finance", "product_dev"]
                    },
                    "framing": {
                        "description": "Present information in specific contexts",
                        "implementation": "Use positive framing for benefits",
                        "success_metrics": ["acceptance_rate", "perception_change"],
                        "team_integration": ["marketing", "hr", "sales"]
                    }
                },
                "relationship_building": {
                    "rapport_development": {
                        "description": "Build trust and connection",
                        "implementation": "Match communication style",
                        "success_metrics": ["trust_level", "engagement_duration"],
                        "team_integration": ["hr", "sales", "marketing"]
                    },
                    "emotional_intelligence": {
                        "description": "Understand and respond to emotions",
                        "implementation": "Adapt responses to emotional cues",
                        "success_metrics": ["satisfaction_rate", "conflict_resolution"],
                        "team_integration": ["hr", "product_dev", "sales"]
                    }
                }
            },
            "team_collaboration": {
                "cross_team_projects": {
                    "description": "Projects involving multiple teams",
                    "techniques": ["rapport_development", "emotional_intelligence"],
                    "success_metrics": ["project_completion", "team_satisfaction"]
                },
                "knowledge_sharing": {
                    "description": "Sharing expertise across teams",
                    "techniques": ["social_proof", "reciprocity"],
                    "success_metrics": ["knowledge_transfer", "team_growth"]
                }
            },
            "learning_sources": {
                "books": [
                    "Influence: The Psychology of Persuasion",
                    "Never Split the Difference",
                    "The Art of War",
                    "Thinking, Fast and Slow",
                    "The 48 Laws of Power"
                ],
                "case_studies": [
                    "Apple's Marketing Strategy",
                    "Amazon's Customer Obsession",
                    "Tesla's Innovation Approach",
                    "Google's Decision Making",
                    "Microsoft's Transformation"
                ]
            },
            "meeting_structure": {
                "frequency": "weekly",
                "duration": "60 minutes",
                "participants": ["daena_core", "all_pods"],
                "agenda_items": [
                    "Progress Review",
                    "Technique Effectiveness",
                    "New Learning Integration",
                    "Strategy Adjustment",
                    "Cross-Pod Collaboration"
                ]
            }
        }
        
        if os.path.exists(config_file):
            with open(config_file, 'r') as f:
                return json.load(f)
        return default_config

    def initialize_techniques(self):
        """Initialize psychological techniques for each pod"""
        for category, techniques in self.config["techniques"].items():
            self.techniques[category] = {}
            for technique_name, technique_data in techniques.items():
                self.techniques[category][technique_name] = {
                    "data": technique_data,
                    "success_history": [],
                    "adaptations": {},
                    "learning_sources": self.config["learning_sources"],
                    "team_collaborations": []
                }

    def apply_technique(self, pod_name, technique_category, technique_name, context):
        """Apply a specific psychological technique"""
        if technique_category not in self.techniques:
            return None
            
        technique = self.techniques[technique_category].get(technique_name)
        if not technique:
            return None
            
        # Apply the technique based on context
        result = {
            "technique": technique_name,
            "category": technique_category,
            "pod": pod_name,
            "timestamp": datetime.now().isoformat(),
            "context": context,
            "implementation": technique["data"]["implementation"],
            "metrics": {},
            "team_collaboration": self.check_team_collaboration(pod_name, technique)
        }
        
        # Record the application
        technique["success_history"].append(result)
        
        return result

    def check_team_collaboration(self, pod_name, technique):
        """Check if technique involves team collaboration"""
        if "team_integration" in technique["data"]:
            return {
                "involved_teams": technique["data"]["team_integration"],
                "collaboration_type": "cross_team" if len(technique["data"]["team_integration"]) > 1 else "single_team"
            }
        return None

    def analyze_technique_effectiveness(self, technique_category, technique_name):
        """Analyze the effectiveness of a technique"""
        if technique_category not in self.techniques:
            return None
            
        technique = self.techniques[technique_category].get(technique_name)
        if not technique:
            return None
            
        history = technique["success_history"]
        if not history:
            return None
            
        analysis = {
            "technique": technique_name,
            "category": technique_category,
            "total_applications": len(history),
            "success_rate": self.calculate_success_rate(history),
            "improvement_areas": self.identify_improvement_areas(history),
            "recommendations": self.generate_recommendations(history),
            "team_collaboration_impact": self.analyze_team_collaboration(history)
        }
        
        return analysis

    def analyze_team_collaboration(self, history):
        """Analyze the impact of team collaborations"""
        collaboration_metrics = defaultdict(list)
        
        for record in history:
            if "team_collaboration" in record:
                collab = record["team_collaboration"]
                if collab["collaboration_type"] == "cross_team":
                    collaboration_metrics["cross_team_success"].append(
                        record.get("metrics", {}).get("success", 0)
                    )
                else:
                    collaboration_metrics["single_team_success"].append(
                        record.get("metrics", {}).get("success", 0)
                    )
                    
        return {
            "cross_team_effectiveness": np.mean(collaboration_metrics["cross_team_success"]) if collaboration_metrics["cross_team_success"] else 0,
            "single_team_effectiveness": np.mean(collaboration_metrics["single_team_success"]) if collaboration_metrics["single_team_success"] else 0
        }

    def calculate_success_rate(self, history):
        """Calculate success rate from technique history"""
        if not history:
            return 0.0
            
        success_count = sum(1 for h in history if h.get("metrics", {}).get("success", False))
        return success_count / len(history)

    def identify_improvement_areas(self, history):
        """Identify areas for technique improvement"""
        if not history:
            return []
            
        metrics = defaultdict(list)
        for h in history:
            for metric, value in h.get("metrics", {}).items():
                metrics[metric].append(value)
                
        improvements = []
        for metric, values in metrics.items():
            avg = np.mean(values)
            if avg < 0.7:  # Threshold for improvement
                improvements.append({
                    "metric": metric,
                    "current_average": avg,
                    "target": 0.8
                })
                
        return improvements

    def generate_recommendations(self, history):
        """Generate recommendations for technique improvement"""
        if not history:
            return []
            
        recommendations = []
        improvements = self.identify_improvement_areas(history)
        
        for imp in improvements:
            metric = imp["metric"]
            current = imp["current_average"]
            
            # Generate specific recommendations based on metric
            if metric == "response_rate":
                recommendations.append({
                    "metric": metric,
                    "suggestion": "Increase personalization in approach",
                    "expected_improvement": "15%"
                })
            elif metric == "engagement_level":
                recommendations.append({
                    "metric": metric,
                    "suggestion": "Enhance emotional connection",
                    "expected_improvement": "20%"
                })
                
        return recommendations

    def schedule_meeting(self):
        """Schedule a technique review meeting"""
        meeting = {
            "timestamp": datetime.now().isoformat(),
            "duration": self.config["meeting_structure"]["duration"],
            "participants": self.config["meeting_structure"]["participants"],
            "agenda": self.config["meeting_structure"]["agenda_items"],
            "technique_reviews": [],
            "team_collaboration_review": self.review_team_collaborations()
        }
        
        # Add technique reviews to agenda
        for category in self.techniques:
            for technique_name in self.techniques[category]:
                analysis = self.analyze_technique_effectiveness(category, technique_name)
                if analysis:
                    meeting["technique_reviews"].append(analysis)
                    
        return meeting

    def review_team_collaborations(self):
        """Review team collaboration effectiveness"""
        review = {
            "cross_team_projects": [],
            "knowledge_sharing": [],
            "recommendations": []
        }
        
        for category, techniques in self.techniques.items():
            for technique_name, technique in techniques.items():
                if "team_integration" in technique["data"]:
                    analysis = self.analyze_technique_effectiveness(category, technique_name)
                    if analysis and "team_collaboration_impact" in analysis:
                        review["cross_team_projects"].append({
                            "technique": technique_name,
                            "effectiveness": analysis["team_collaboration_impact"]
                        })
                        
        return review

    def integrate_learning(self, source_type, source_name, insights):
        """Integrate new learning from books or case studies"""
        if source_type not in self.config["learning_sources"]:
            return False
            
        # Add new insights to technique adaptations
        for category in self.techniques:
            for technique_name in self.techniques[category]:
                technique = self.techniques[category][technique_name]
                if "adaptations" not in technique:
                    technique["adaptations"] = {}
                    
                technique["adaptations"][source_name] = {
                    "source_type": source_type,
                    "insights": insights,
                    "integration_date": datetime.now().isoformat()
                }
                
        return True

    def list_techniques(self):
        return self.techniques

    def get_technique(self, technique_id):
        return self.techniques.get(technique_id)

    def apply_technique(self, technique_id, context):
        technique = self.get_technique(technique_id)
        if not technique:
            raise ValueError(f"Technique {technique_id} not found")
        
        # In a real implementation, this would apply the technique to the context
        return {
            "technique": technique,
            "applied_context": context,
            "result": "Technique applied successfully"
        }

if __name__ == "__main__":
    # Test the psychological techniques system
    techniques = PsychologicalTechniques()
    
    # Test technique application
    result = techniques.apply_technique(
        "apollo_creative",
        "persuasion",
        "social_proof",
        {"context": "marketing_campaign", "target": "potential_customers"}
    )
    print("Technique Application Result:", json.dumps(result, indent=2))
    
    # Test technique analysis
    analysis = techniques.analyze_technique_effectiveness("persuasion", "social_proof")
    print("Technique Analysis:", json.dumps(analysis, indent=2))
    
    # Test meeting scheduling
    meeting = techniques.schedule_meeting()
    print("Scheduled Meeting:", json.dumps(meeting, indent=2))
    
    # Test learning integration
    techniques.integrate_learning(
        "books",
        "Influence: The Psychology of Persuasion",
        ["New insight 1", "New insight 2"]
    ) 