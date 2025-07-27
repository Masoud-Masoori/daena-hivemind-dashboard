import os
import json
import numpy as np
from datetime import datetime
from pathlib import Path
import torch
from transformers import AutoTokenizer, AutoModel
import networkx as nx
from collections import defaultdict
from .psychological_techniques import PsychologicalTechniques

class DaenaConsultation:
    def __init__(self):
        self.techniques = PsychologicalTechniques()
        self.consultation_history = []
        self.initialize_consultation_system()
        
    def initialize_consultation_system(self):
        """Initialize the consultation system with default settings"""
        self.config = {
            "consultation_types": {
                "strategy": {
                    "description": "Strategic planning and decision making",
                    "techniques": ["framing", "anchoring"],
                    "metrics": ["clarity", "confidence", "actionability"]
                },
                "relationship": {
                    "description": "Building and maintaining relationships",
                    "techniques": ["rapport_development", "emotional_intelligence"],
                    "metrics": ["trust", "engagement", "satisfaction"]
                },
                "negotiation": {
                    "description": "Negotiation and conflict resolution",
                    "techniques": ["reciprocity", "commitment_consistency"],
                    "metrics": ["outcome", "relationship_preservation", "future_cooperation"]
                }
            },
            "consultation_flow": {
                "initial_assessment": {
                    "steps": [
                        "context_gathering",
                        "goal_identification",
                        "technique_selection"
                    ]
                },
                "main_consultation": {
                    "steps": [
                        "technique_application",
                        "feedback_collection",
                        "adjustment_making"
                    ]
                },
                "follow_up": {
                    "steps": [
                        "outcome_evaluation",
                        "learning_integration",
                        "future_planning"
                    ]
                }
            }
        }
        
    def start_consultation(self, pod_name, consultation_type, context):
        """Start a new consultation session"""
        if consultation_type not in self.config["consultation_types"]:
            return None
            
        consultation = {
            "pod": pod_name,
            "type": consultation_type,
            "start_time": datetime.now().isoformat(),
            "context": context,
            "status": "in_progress",
            "techniques_applied": [],
            "feedback": [],
            "outcomes": {}
        }
        
        # Select appropriate techniques
        available_techniques = self.config["consultation_types"][consultation_type]["techniques"]
        selected_techniques = self.select_techniques(available_techniques, context)
        
        consultation["selected_techniques"] = selected_techniques
        self.consultation_history.append(consultation)
        
        return consultation
        
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
                    "confidence": analysis["success_rate"]
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
            
        return result
        
    def get_consultation(self, consultation_id):
        """Get a consultation by ID"""
        for consultation in self.consultation_history:
            if consultation.get("id") == consultation_id:
                return consultation
        return None
        
    def collect_feedback(self, consultation_id, feedback_data):
        """Collect feedback during consultation"""
        consultation = self.get_consultation(consultation_id)
        if not consultation:
            return None
            
        feedback = {
            "timestamp": datetime.now().isoformat(),
            "data": feedback_data,
            "metrics": self.calculate_feedback_metrics(feedback_data)
        }
        
        consultation["feedback"].append(feedback)
        return feedback
        
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
        
    def end_consultation(self, consultation_id, outcomes):
        """End a consultation session"""
        consultation = self.get_consultation(consultation_id)
        if not consultation:
            return None
            
        consultation["end_time"] = datetime.now().isoformat()
        consultation["status"] = "completed"
        consultation["outcomes"] = outcomes
        
        # Integrate learning from the consultation
        self.integrate_consultation_learning(consultation)
        
        return consultation
        
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
            "recommendations": self.generate_recommendations(consultation)
        }
        
        return report
        
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
            "key_insights": []
        }
        
        # Calculate average metrics
        metrics = defaultdict(list)
        for feedback in consultation["feedback"]:
            for metric, value in feedback["metrics"].items():
                metrics[metric].append(value)
                
        for metric, values in metrics.items():
            summary["average_metrics"][metric] = np.mean(values)
            
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
                
        # Add pod-specific recommendations
        if consultation["outcomes"]:
            recommendations.append({
                "type": "pod_specific",
                "suggestion": "Schedule follow-up consultation",
                "timing": "2 weeks"
            })
            
        return recommendations

if __name__ == "__main__":
    # Test the consultation system
    consultation_system = DaenaConsultation()
    
    # Start a consultation
    consultation = consultation_system.start_consultation(
        "apollo_creative",
        "strategy",
        {"goal": "improve_team_collaboration", "challenges": ["communication", "alignment"]}
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
            "text_feedback": "The framing technique was very effective in improving team understanding"
        }
    )
    print("Collected Feedback:", json.dumps(feedback, indent=2))
    
    # End consultation
    ended_consultation = consultation_system.end_consultation(
        consultation["id"],
        {
            "goal_achievement": 0.85,
            "team_satisfaction": 0.9,
            "next_steps": ["schedule_follow_up", "implement_suggestions"]
        }
    )
    print("Ended Consultation:", json.dumps(ended_consultation, indent=2))
    
    # Generate report
    report = consultation_system.generate_consultation_report(consultation["id"])
    print("Consultation Report:", json.dumps(report, indent=2)) 