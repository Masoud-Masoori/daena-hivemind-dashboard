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
from .psychological_techniques import PsychologicalTechniques

class DaenaConsultation(AgentBase):
    def __init__(self):
        super().__init__(AgentType.CORE)
        self.techniques = PsychologicalTechniques()
        self.consultation_history = []
        self.active_consultations = {}
        self.consultation_types = {
            "general": {
                "name": "General Consultation",
                "description": "General purpose consultation for various topics",
                "duration": 30  # minutes
            },
            "technical": {
                "name": "Technical Consultation",
                "description": "Technical and implementation focused consultation",
                "duration": 45  # minutes
            },
            "strategic": {
                "name": "Strategic Consultation",
                "description": "High-level strategic planning consultation",
                "duration": 60  # minutes
            }
        }
        self.initialize_consultation_system()
        
    def initialize_consultation_system(self):
        """Initialize the consultation system with default settings"""
        self.config = {
            "consultation_types": {
                "strategy": {
                    "description": "Strategic planning and decision making",
                    "techniques": ["framing", "anchoring"],
                    "metrics": ["clarity", "confidence", "actionability"],
                    "team_integration": ["product_dev", "finance", "marketing"]
                },
                "relationship": {
                    "description": "Building and maintaining relationships",
                    "techniques": ["rapport_development", "emotional_intelligence"],
                    "metrics": ["trust", "engagement", "satisfaction"],
                    "team_integration": ["hr", "sales", "marketing"]
                },
                "negotiation": {
                    "description": "Negotiation and conflict resolution",
                    "techniques": ["reciprocity", "commitment_consistency"],
                    "metrics": ["outcome", "relationship_preservation", "future_cooperation"],
                    "team_integration": ["sales", "finance", "product_dev"]
                }
            },
            "consultation_flow": {
                "initial_assessment": {
                    "steps": [
                        "context_gathering",
                        "goal_identification",
                        "technique_selection",
                        "team_collaboration_setup"
                    ]
                },
                "main_consultation": {
                    "steps": [
                        "technique_application",
                        "feedback_collection",
                        "adjustment_making",
                        "team_collaboration_review"
                    ]
                },
                "follow_up": {
                    "steps": [
                        "outcome_evaluation",
                        "learning_integration",
                        "future_planning",
                        "team_collaboration_planning"
                    ]
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
            }
        }
        
    def start_consultation(self, pod_id, consultation_type):
        if consultation_type not in self.consultation_types:
            raise ValueError(f"Invalid consultation type: {consultation_type}")
        
        consultation = {
            "id": pod_id,
            "type": consultation_type,
            "status": "active",
            "start_time": "2024-02-20T10:00:00Z",  # In real implementation, use actual timestamp
            "duration": self.consultation_types[consultation_type]["duration"]
        }
        
        self.active_consultations[pod_id] = consultation
        return consultation

    def end_consultation(self, pod_id):
        if pod_id not in self.active_consultations:
            raise ValueError(f"No active consultation found for pod: {pod_id}")
        
        consultation = self.active_consultations[pod_id]
        consultation["status"] = "completed"
        consultation["end_time"] = "2024-02-20T10:30:00Z"  # In real implementation, use actual timestamp
        
        return consultation

    def get_consultation(self, pod_id):
        return self.active_consultations.get(pod_id)

    def list_consultation_types(self):
        return self.consultation_types
        
    def setup_team_collaboration(self, consultation_type):
        """Setup team collaboration for consultation"""
        if consultation_type not in self.config["consultation_types"]:
            return None
            
        teams = self.config["consultation_types"][consultation_type]["team_integration"]
        return {
            "involved_teams": teams,
            "collaboration_type": "cross_team" if len(teams) > 1 else "single_team",
            "status": "initialized",
            "progress": 0
        }
        
    def select_techniques(self, available_techniques, context):
        """Select the most appropriate techniques for the consultation"""
        selected = []
        for technique in available_techniques:
            # Analyze technique effectiveness
            analysis = self.techniques.analyze_technique_effectiveness(
                self.get_technique_category(technique),
                technique
            )
            
            if analysis and analysis["success_rate"] > 0.6:
                selected.append({
                    "name": technique,
                    "category": self.get_technique_category(technique),
                    "confidence": analysis["success_rate"],
                    "team_collaboration": analysis.get("team_collaboration_impact", {})
                })
                
        return selected
        
    def get_technique_category(self, technique_name):
        """Get the category of a technique"""
        for category, techniques in self.techniques.techniques.items():
            if technique_name in techniques:
                return category
        return None
        
    def apply_consultation_technique(self, consultation_id, technique_name, application_context):
        """Apply a technique during consultation"""
        consultation = self.get_consultation(consultation_id)
        if not consultation:
            return None
            
        technique_category = self.get_technique_category(technique_name)
        if not technique_category:
            return None
            
        result = self.techniques.apply_technique(
            consultation["pod"],
            technique_category,
            technique_name,
            application_context
        )
        
        if result:
            consultation["techniques_applied"].append(result)
            self.update_team_collaboration(consultation, result)
            
        return result
        
    def update_team_collaboration(self, consultation, technique_result):
        """Update team collaboration progress"""
        if "team_collaboration" not in consultation:
            return
            
        if "team_collaboration" in technique_result:
            consultation["team_collaboration"]["progress"] += 1
            consultation["team_collaboration"]["last_update"] = datetime.now().isoformat()
            
    def collect_feedback(self, consultation_id, feedback_data):
        """Collect feedback during consultation"""
        consultation = self.get_consultation(consultation_id)
        if not consultation:
            return None
            
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "data": feedback_data,
            "metrics": self.calculate_feedback_metrics(feedback_data),
            "team_collaboration_feedback": self.collect_team_feedback(consultation, feedback_data)
        }
        
        consultation["feedback"].append(feedback)
        return feedback
        
    def collect_team_feedback(self, consultation, feedback_data):
        """Collect feedback specific to team collaboration"""
        if "team_collaboration" not in consultation:
            return None
            
        return {
            "teams": consultation["team_collaboration"]["involved_teams"],
            "collaboration_effectiveness": feedback_data.get("collaboration_effectiveness", 0),
            "team_satisfaction": feedback_data.get("team_satisfaction", 0)
        }
        
    def calculate_feedback_metrics(self, feedback_data):
        """Calculate metrics from feedback data"""
        metrics = {}
        for metric, value in feedback_data.items():
            if isinstance(value, (int, float)):
                metrics[metric] = value
            elif isinstance(value, str):
                # Convert text feedback to numerical metrics
                metrics[metric] = self.analyze_text_feedback(value)
                
        return metrics
        
    def analyze_text_feedback(self, text):
        """Analyze text feedback to extract numerical metrics"""
        # Simple sentiment analysis (can be enhanced with more sophisticated NLP)
        positive_words = ["good", "great", "excellent", "helpful", "effective"]
        negative_words = ["bad", "poor", "ineffective", "unhelpful", "difficult"]
        
        text = text.lower()
        positive_count = sum(1 for word in positive_words if word in text)
        negative_count = sum(1 for word in negative_words if word in text)
        
        if positive_count + negative_count == 0:
            return 0.5  # Neutral
            
        return positive_count / (positive_count + negative_count)
        
    def integrate_consultation_learning(self, consultation):
        """Integrate learning from the consultation into the system"""
        insights = []
        
        # Analyze technique effectiveness
        for technique in consultation["techniques_applied"]:
            analysis = self.techniques.analyze_technique_effectiveness(
                technique["category"],
                technique["technique"]
            )
            if analysis:
                insights.extend(analysis["recommendations"])
                
        # Add team collaboration insights
        if "team_collaboration" in consultation:
            insights.append({
                "type": "team_collaboration",
                "teams": consultation["team_collaboration"]["involved_teams"],
                "effectiveness": consultation["team_collaboration"].get("final_progress", 0)
            })
                
        # Add insights to learning sources
        if insights:
            self.techniques.integrate_learning(
                "case_studies",
                f"Consultation_{consultation['pod']}_{consultation['start_time']}",
                insights
            )
            
    def generate_consultation_report(self, consultation_id):
        """Generate a comprehensive report for a consultation"""
        consultation = self.get_consultation(consultation_id)
        if not consultation:
            return None
            
        report = {
            "consultation_id": consultation_id,
            "pod": consultation["pod"],
            "type": consultation["type"],
            "duration": self.calculate_duration(consultation),
            "techniques_applied": consultation["techniques_applied"],
            "feedback_summary": self.summarize_feedback(consultation),
            "outcomes": consultation["outcomes"],
            "recommendations": self.generate_recommendations(consultation),
            "team_collaboration_summary": self.summarize_team_collaboration(consultation)
        }
        
        return report
        
    def summarize_team_collaboration(self, consultation):
        """Summarize team collaboration results"""
        if "team_collaboration" not in consultation:
            return None
            
        return {
            "teams": consultation["team_collaboration"]["involved_teams"],
            "type": consultation["team_collaboration"]["collaboration_type"],
            "progress": consultation["team_collaboration"].get("final_progress", 0),
            "status": consultation["team_collaboration"]["status"]
        }
        
    def calculate_duration(self, consultation):
        """Calculate the duration of a consultation"""
        start = datetime.fromisoformat(consultation["start_time"])
        end = datetime.fromisoformat(consultation["end_time"])
        return (end - start).total_seconds() / 60  # Duration in minutes
        
    def summarize_feedback(self, consultation):
        """Summarize feedback from a consultation"""
        if not consultation["feedback"]:
            return None
            
        summary = {
            "average_metrics": {},
            "key_insights": [],
            "team_collaboration_metrics": {}
        }
        
        # Calculate average metrics
        metrics = defaultdict(list)
        team_metrics = defaultdict(list)
        
        for feedback in consultation["feedback"]:
            for metric, value in feedback["metrics"].items():
                metrics[metric].append(value)
                
            if "team_collaboration_feedback" in feedback:
                team_feedback = feedback["team_collaboration_feedback"]
                team_metrics["collaboration_effectiveness"].append(
                    team_feedback.get("collaboration_effectiveness", 0)
                )
                team_metrics["team_satisfaction"].append(
                    team_feedback.get("team_satisfaction", 0)
                )
                
        for metric, values in metrics.items():
            summary["average_metrics"][metric] = np.mean(values)
            
        for metric, values in team_metrics.items():
            summary["team_collaboration_metrics"][metric] = np.mean(values)
            
        # Extract key insights
        for feedback in consultation["feedback"]:
            if "data" in feedback and isinstance(feedback["data"], str):
                summary["key_insights"].append(feedback["data"])
                
        return summary
        
    def generate_recommendations(self, consultation):
        """Generate recommendations based on consultation outcomes"""
        recommendations = []
        
        # Analyze technique effectiveness
        for technique in consultation["techniques_applied"]:
            analysis = self.techniques.analyze_technique_effectiveness(
                technique["category"],
                technique["technique"]
            )
            if analysis and analysis["improvement_areas"]:
                recommendations.extend(analysis["recommendations"])
                
        # Add team collaboration recommendations
        if "team_collaboration" in consultation:
            team_summary = self.summarize_team_collaboration(consultation)
            if team_summary:
                recommendations.append({
                    "type": "team_collaboration",
                    "suggestion": "Schedule follow-up team collaboration",
                    "teams": team_summary["teams"],
                    "timing": "2 weeks"
                })
                
        return recommendations

if __name__ == "__main__":
    # Test the consultation system
    consultation_system = DaenaConsultation()
    
    # Start a consultation
    consultation = consultation_system.start_consultation(
        "apollo_creative",
        "strategy"
    )
    print("Started Consultation:", json.dumps(consultation, indent=2))
    
    # Apply a technique
    result = consultation_system.apply_consultation_technique(
        consultation["id"],
        "framing",
        {"context": "team_meeting", "focus": "collaboration_benefits"}
    )
    print("Applied Technique:", json.dumps(result, indent=2))
    
    # Collect feedback
    feedback = consultation_system.collect_feedback(
        consultation["id"],
        {
            "effectiveness": 0.8,
            "clarity": 0.9,
            "text_feedback": "The framing technique was very effective in improving team understanding",
            "collaboration_effectiveness": 0.85,
            "team_satisfaction": 0.9
        }
    )
    print("Collected Feedback:", json.dumps(feedback, indent=2))
    
    # End consultation
    ended_consultation = consultation_system.end_consultation(consultation["id"])
    print("Ended Consultation:", json.dumps(ended_consultation, indent=2))
    
    # Generate report
    report = consultation_system.generate_consultation_report(consultation["id"])
    print("Consultation Report:", json.dumps(report, indent=2)) 