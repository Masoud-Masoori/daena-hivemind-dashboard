"""
Initialize Daena Company data with departments and sample agents
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import get_db, Agent as DBAgent
from sqlalchemy.orm import Session
import json

def init_departments_and_agents():
    """Initialize departments and sample agents"""
    
    # Sample departments and their agents
    departments_data = {
        "hr": {
            "name": "Human Resources",
            "description": "Manages employee relations, recruitment, and HR processes",
            "agents": [
                {
                    "name": "HR Assistant",
                    "description": "Handles employee inquiries, leave requests, and HR documentation",
                    "capabilities": "employee_management,leave_processing,hr_documentation",
                    "type": "hr_assistant",
                    "status": "active"
                },
                {
                    "name": "Recruitment Bot",
                    "description": "Manages job postings, candidate screening, and interview scheduling",
                    "capabilities": "job_posting,candidate_screening,interview_scheduling",
                    "type": "recruitment",
                    "status": "active"
                }
            ]
        },
        "finance": {
            "name": "Finance",
            "description": "Manages financial operations, accounting, and budget planning",
            "agents": [
                {
                    "name": "Finance Assistant",
                    "description": "Handles expense reports, invoice processing, and financial queries",
                    "capabilities": "expense_processing,invoice_management,financial_reporting",
                    "type": "finance_assistant",
                    "status": "active"
                },
                {
                    "name": "Budget Tracker",
                    "description": "Monitors budgets, tracks spending, and generates financial reports",
                    "capabilities": "budget_monitoring,spending_tracking,financial_analysis",
                    "type": "budget_tracker",
                    "status": "active"
                }
            ]
        },
        "security": {
            "name": "Security",
            "description": "Manages cybersecurity, access control, and security monitoring",
            "agents": [
                {
                    "name": "Security Monitor",
                    "description": "Monitors system security, detects threats, and manages access control",
                    "capabilities": "threat_detection,access_control,security_monitoring",
                    "type": "security_monitor",
                    "status": "active"
                },
                {
                    "name": "Incident Response",
                    "description": "Handles security incidents, coordinates responses, and generates reports",
                    "capabilities": "incident_response,coordination,security_reporting",
                    "type": "incident_response",
                    "status": "active"
                }
            ]
        },
        "legal": {
            "name": "Legal",
            "description": "Manages legal compliance, contract review, and legal documentation",
            "agents": [
                {
                    "name": "Legal Assistant",
                    "description": "Handles contract review, legal research, and compliance monitoring",
                    "capabilities": "contract_review,legal_research,compliance_monitoring",
                    "type": "legal_assistant",
                    "status": "active"
                },
                {
                    "name": "Compliance Tracker",
                    "description": "Monitors regulatory compliance, tracks deadlines, and generates reports",
                    "capabilities": "compliance_monitoring,deadline_tracking,regulatory_reporting",
                    "type": "compliance_tracker",
                    "status": "active"
                }
            ]
        },
        "marketing": {
            "name": "Marketing",
            "description": "Manages marketing campaigns, content creation, and brand management",
            "agents": [
                {
                    "name": "Content Creator",
                    "description": "Creates marketing content, manages social media, and tracks engagement",
                    "capabilities": "content_creation,social_media_management,engagement_tracking",
                    "type": "content_creator",
                    "status": "active"
                },
                {
                    "name": "Campaign Manager",
                    "description": "Manages marketing campaigns, tracks performance, and optimizes strategies",
                    "capabilities": "campaign_management,performance_tracking,strategy_optimization",
                    "type": "campaign_manager",
                    "status": "active"
                }
            ]
        },
        "sales": {
            "name": "Sales",
            "description": "Manages sales operations, lead generation, and customer relationships",
            "agents": [
                {
                    "name": "Sales Assistant",
                    "description": "Handles lead qualification, sales follow-ups, and customer inquiries",
                    "capabilities": "lead_qualification,sales_followup,customer_support",
                    "type": "sales_assistant",
                    "status": "active"
                },
                {
                    "name": "Lead Generator",
                    "description": "Generates leads, qualifies prospects, and manages sales pipeline",
                    "capabilities": "lead_generation,prospect_qualification,pipeline_management",
                    "type": "lead_generator",
                    "status": "active"
                }
            ]
        },
        "it": {
            "name": "Information Technology",
            "description": "Manages IT infrastructure, system maintenance, and technical support",
            "agents": [
                {
                    "name": "IT Support",
                    "description": "Handles technical support, system troubleshooting, and user assistance",
                    "capabilities": "technical_support,system_troubleshooting,user_assistance",
                    "type": "it_support",
                    "status": "active"
                },
                {
                    "name": "System Monitor",
                    "description": "Monitors system performance, detects issues, and manages infrastructure",
                    "capabilities": "system_monitoring,issue_detection,infrastructure_management",
                    "type": "system_monitor",
                    "status": "active"
                }
            ]
        },
        "operations": {
            "name": "Operations",
            "description": "Manages day-to-day operations, process optimization, and workflow management",
            "agents": [
                {
                    "name": "Operations Coordinator",
                    "description": "Coordinates daily operations, manages workflows, and tracks performance",
                    "capabilities": "operations_coordination,workflow_management,performance_tracking",
                    "type": "operations_coordinator",
                    "status": "active"
                },
                {
                    "name": "Process Optimizer",
                    "description": "Analyzes processes, identifies improvements, and implements optimizations",
                    "capabilities": "process_analysis,improvement_identification,optimization_implementation",
                    "type": "process_optimizer",
                    "status": "active"
                }
            ]
        }
    }
    
    # Create database session
    db = next(get_db())
    
    try:
        # Create agents for each department
        for dept_id, dept_data in departments_data.items():
            print(f"Creating agents for {dept_data['name']} department...")
            
            for agent_data in dept_data["agents"]:
                # Check if agent already exists
                existing_agent = db.query(DBAgent).filter(
                    DBAgent.name == agent_data["name"],
                    DBAgent.department == dept_id
                ).first()
                
                if not existing_agent:
                    # Create new agent
                    db_agent = DBAgent(
                        name=agent_data["name"],
                        description=agent_data["description"],
                        capabilities=agent_data["capabilities"],
                        type=agent_data["type"],
                        department=dept_id,
                        status=agent_data["status"],
                        is_active=True
                    )
                    db.add(db_agent)
                    print(f"  ✓ Created agent: {agent_data['name']}")
                else:
                    print(f"  - Agent already exists: {agent_data['name']}")
        
        # Commit changes
        db.commit()
        print("\n✅ Successfully initialized departments and agents!")
        
        # Display summary
        total_agents = db.query(DBAgent).count()
        print(f"\n📊 Summary:")
        print(f"  Total agents: {total_agents}")
        print(f"  Departments: {len(departments_data)}")
        
        for dept_id, dept_data in departments_data.items():
            agent_count = db.query(DBAgent).filter(DBAgent.department == dept_id).count()
            print(f"  - {dept_data['name']}: {agent_count} agents")
            
    except Exception as e:
        db.rollback()
        print(f"❌ Error initializing data: {e}")
        raise
    finally:
        db.close()

if __name__ == "__main__":
    init_departments_and_agents() 