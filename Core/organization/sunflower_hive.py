from typing import Dict, List, Optional
from datetime import datetime
from memory.secure_recall import log_event

class SunflowerHive:
    def __init__(self):
        self.core = {
            'id': 'core',
            'name': 'Hive Core',
            'type': 'core',
            'connections': [],
            'metrics': {
                'collective_intelligence': 0,
                'knowledge_flow': 0,
                'decision_efficiency': 0,
                'adaptability': 0
            }
        }
        self.departments = {}
        self.connections = []
        self.initialize_structure()

    def initialize_structure(self):
        """Initialize the sunflower-hive structure with departments and connections."""
        # Define core departments (petals)
        self.departments = {
            'intelligence': {
                'id': 'intelligence',
                'name': 'Intelligence Hub',
                'type': 'department',
                'subdepartments': ['ai', 'research'],
                'metrics': {
                    'knowledge_processing': 0,
                    'pattern_recognition': 0,
                    'learning_rate': 0
                }
            },
            'operations': {
                'id': 'operations',
                'name': 'Operations Hub',
                'type': 'department',
                'subdepartments': ['execution', 'optimization'],
                'metrics': {
                    'efficiency': 0,
                    'resource_utilization': 0,
                    'process_optimization': 0
                }
            },
            'innovation': {
                'id': 'innovation',
                'name': 'Innovation Hub',
                'type': 'department',
                'subdepartments': ['research', 'development'],
                'metrics': {
                    'creativity_index': 0,
                    'innovation_rate': 0,
                    'experimentation': 0
                }
            },
            'analytics': {
                'id': 'analytics',
                'name': 'Analytics Hub',
                'type': 'department',
                'subdepartments': ['data_science', 'business_intelligence'],
                'metrics': {
                    'data_processing': 0,
                    'insight_generation': 0,
                    'prediction_accuracy': 0
                }
            }
        }

        # Initialize connections
        self.connections = [
            # Core connections
            {'source': 'core', 'target': 'intelligence', 'strength': 90},
            {'source': 'core', 'target': 'operations', 'strength': 85},
            {'source': 'core', 'target': 'innovation', 'strength': 95},
            {'source': 'core', 'target': 'analytics', 'strength': 88},
            # Inter-department connections
            {'source': 'intelligence', 'target': 'operations', 'strength': 75},
            {'source': 'intelligence', 'target': 'innovation', 'strength': 85},
            {'source': 'operations', 'target': 'analytics', 'strength': 80},
            {'source': 'innovation', 'target': 'analytics', 'strength': 90}
        ]

    def update_metrics(self, department_id: str, metrics: Dict) -> bool:
        """Update metrics for a specific department."""
        try:
            if department_id in self.departments:
                self.departments[department_id]['metrics'].update(metrics)
                self._recalculate_core_metrics()
                log_event("sunflower_hive", {
                    "action": "metrics_updated",
                    "department": department_id,
                    "metrics": metrics
                })
                return True
            return False
        except Exception as e:
            log_event("sunflower_hive", {
                "action": "metrics_update_error",
                "department": department_id,
                "error": str(e)
            })
            return False

    def _recalculate_core_metrics(self):
        """Recalculate core metrics based on department performance."""
        try:
            # Calculate collective intelligence
            intelligence_scores = [
                dept['metrics'].get('knowledge_processing', 0) +
                dept['metrics'].get('pattern_recognition', 0) +
                dept['metrics'].get('learning_rate', 0)
                for dept in self.departments.values()
            ]
            self.core['metrics']['collective_intelligence'] = sum(intelligence_scores) / len(intelligence_scores)

            # Calculate knowledge flow
            connection_strengths = [conn['strength'] for conn in self.connections]
            self.core['metrics']['knowledge_flow'] = sum(connection_strengths) / len(connection_strengths)

            # Calculate decision efficiency
            efficiency_scores = [
                dept['metrics'].get('efficiency', 0) +
                dept['metrics'].get('process_optimization', 0)
                for dept in self.departments.values()
            ]
            self.core['metrics']['decision_efficiency'] = sum(efficiency_scores) / len(efficiency_scores)

            # Calculate adaptability
            adaptability_scores = [
                dept['metrics'].get('creativity_index', 0) +
                dept['metrics'].get('innovation_rate', 0) +
                dept['metrics'].get('experimentation', 0)
                for dept in self.departments.values()
            ]
            self.core['metrics']['adaptability'] = sum(adaptability_scores) / len(adaptability_scores)

            log_event("sunflower_hive", {
                "action": "core_metrics_recalculated",
                "metrics": self.core['metrics']
            })
        except Exception as e:
            log_event("sunflower_hive", {
                "action": "core_metrics_recalculation_error",
                "error": str(e)
            })

    def add_connection(self, source: str, target: str, strength: int) -> bool:
        """Add a new connection between departments."""
        try:
            if source in self.departments and target in self.departments:
                connection = {
                    'source': source,
                    'target': target,
                    'strength': strength
                }
                self.connections.append(connection)
                self._recalculate_core_metrics()
                log_event("sunflower_hive", {
                    "action": "connection_added",
                    "connection": connection
                })
                return True
            return False
        except Exception as e:
            log_event("sunflower_hive", {
                "action": "connection_add_error",
                "source": source,
                "target": target,
                "error": str(e)
            })
            return False

    def get_department_insights(self, department_id: str) -> Optional[Dict]:
        """Get insights and recommendations for a department."""
        try:
            if department_id in self.departments:
                dept = self.departments[department_id]
                connections = [conn for conn in self.connections 
                             if conn['source'] == department_id or conn['target'] == department_id]
                
                insights = {
                    'department': dept,
                    'connections': connections,
                    'recommendations': self._generate_recommendations(dept, connections),
                    'performance_trends': self._analyze_performance_trends(dept)
                }
                
                log_event("sunflower_hive", {
                    "action": "insights_generated",
                    "department": department_id,
                    "insights": insights
                })
                return insights
            return None
        except Exception as e:
            log_event("sunflower_hive", {
                "action": "insights_generation_error",
                "department": department_id,
                "error": str(e)
            })
            return None

    def _generate_recommendations(self, department: Dict, connections: List[Dict]) -> List[str]:
        """Generate recommendations based on department metrics and connections."""
        recommendations = []
        
        # Analyze connection strengths
        weak_connections = [conn for conn in connections if conn['strength'] < 70]
        if weak_connections:
            recommendations.append(
                f"Strengthen connections with {', '.join(conn['target'] for conn in weak_connections)}"
            )

        # Analyze department metrics
        metrics = department['metrics']
        for metric, value in metrics.items():
            if value < 70:
                recommendations.append(f"Improve {metric.replace('_', ' ')} performance")
            elif value > 90:
                recommendations.append(f"Share {metric.replace('_', ' ')} best practices with other departments")

        return recommendations

    def _analyze_performance_trends(self, department: Dict) -> Dict:
        """Analyze performance trends for a department."""
        return {
            'trend': 'improving' if sum(department['metrics'].values()) / len(department['metrics']) > 80 else 'needs_attention',
            'key_strengths': [
                metric for metric, value in department['metrics'].items()
                if value > 85
            ],
            'areas_for_improvement': [
                metric for metric, value in department['metrics'].items()
                if value < 70
            ]
        }

    def get_hive_state(self) -> Dict:
        """Get the current state of the entire hive structure."""
        return {
            'core': self.core,
            'departments': self.departments,
            'connections': self.connections,
            'timestamp': datetime.now().isoformat()
        }

    def get_departments(self) -> List[Dict]:
        """Get list of all departments with their current state."""
        try:
            departments_list = []
            for dept_id, dept in self.departments.items():
                dept_data = {
                    'id': dept['id'],
                    'name': dept['name'],
                    'type': dept['type'],
                    'subdepartments': dept['subdepartments'],
                    'metrics': dept['metrics'],
                    'connections': [
                        conn for conn in self.connections 
                        if conn['source'] == dept_id or conn['target'] == dept_id
                    ]
                }
                departments_list.append(dept_data)
            
            log_event("sunflower_hive", {
                "action": "departments_retrieved",
                "count": len(departments_list)
            })
            return departments_list
        except Exception as e:
            log_event("sunflower_hive", {
                "action": "departments_retrieval_error",
                "error": str(e)
            })
            return [] 