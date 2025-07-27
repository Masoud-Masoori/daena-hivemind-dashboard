"""
Initialize Daena database with proper schema and sample data
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.database import Base, engine, SessionLocal, User, Agent, Consultation, Message
import sqlite3
from datetime import datetime, timedelta
import uuid

def init_database():
    """Initialize the database with proper schema and sample data"""
    
    print("🗄️  Initializing Daena database...")
    
    # Drop all tables and recreate them
    Base.metadata.drop_all(bind=engine)
    print("  ✓ Dropped existing tables")
    
    # Create all tables
    Base.metadata.create_all(bind=engine)
    print("  ✓ Created new tables")
    
    # Create database session
    db = SessionLocal()
    
    try:
        # Create sample users
        print("  📝 Creating sample users...")
        users = [
            User(
                username="founder",
                email="founder@daena.ai",
                password_hash="hashed_password_here",
                role="founder"
            ),
            User(
                username="ceo",
                email="ceo@daena.ai", 
                password_hash="hashed_password_here",
                role="admin"
            ),
            User(
                username="manager",
                email="manager@daena.ai",
                password_hash="hashed_password_here", 
                role="manager"
            )
        ]
        
        for user in users:
            db.add(user)
        db.commit()
        print("  ✓ Created 3 sample users")
        
        # Create 12 AI Agents
        print("  🤖 Creating 12 AI Agents...")
        agents = [
            Agent(
                name="Daena VP",
                department="executive",
                status="active",
                type="vp",
                capabilities="Strategic planning, decision making, team coordination",
                description="AI Vice President - Strategic leader and decision maker"
            ),
            Agent(
                name="Alex Finance",
                department="finance",
                status="active", 
                type="specialist",
                capabilities="Financial analysis, budgeting, forecasting",
                description="Finance specialist agent"
            ),
            Agent(
                name="Sam Marketing",
                department="marketing",
                status="active",
                type="specialist", 
                capabilities="Marketing strategy, campaign management, analytics",
                description="Marketing specialist agent"
            ),
            Agent(
                name="Jordan Sales",
                department="sales",
                status="active",
                type="specialist",
                capabilities="Sales strategy, lead generation, customer relations",
                description="Sales specialist agent"
            ),
            Agent(
                name="Casey Operations",
                department="operations",
                status="active",
                type="specialist",
                capabilities="Process optimization, logistics, quality control",
                description="Operations specialist agent"
            ),
            Agent(
                name="Taylor HR",
                department="hr",
                status="active",
                type="specialist",
                capabilities="Recruitment, employee relations, compliance",
                description="Human Resources specialist agent"
            ),
            Agent(
                name="Riley Tech",
                department="technology",
                status="active",
                type="specialist",
                capabilities="Software development, infrastructure, security",
                description="Technology specialist agent"
            ),
            Agent(
                name="Morgan Legal",
                department="legal",
                status="active",
                type="specialist",
                capabilities="Contract review, compliance, risk management",
                description="Legal specialist agent"
            ),
            Agent(
                name="Parker Research",
                department="research",
                status="active",
                type="specialist",
                capabilities="Market research, data analysis, innovation",
                description="Research specialist agent"
            ),
            Agent(
                name="Quinn Customer",
                department="customer_success",
                status="active",
                type="specialist",
                capabilities="Customer support, satisfaction, retention",
                description="Customer Success specialist agent"
            ),
            Agent(
                name="Avery Product",
                department="product",
                status="active",
                type="specialist",
                capabilities="Product strategy, development, lifecycle",
                description="Product specialist agent"
            ),
            Agent(
                name="Blake Analytics",
                department="analytics",
                status="active",
                type="specialist",
                capabilities="Data analysis, reporting, insights",
                description="Analytics specialist agent"
            )
        ]
        
        for agent in agents:
            db.add(agent)
        db.commit()
        print("  ✓ Created 12 AI agents")
        
        # Create sample consultations
        print("  💬 Creating sample consultations...")
        consultations = [
            Consultation(
                user_id=1,
                topic="Q4 Strategy Planning",
                start_time=datetime.now() - timedelta(hours=2),
                duration=60,
                notes="Discussed Q4 goals and resource allocation",
                status="completed"
            ),
            Consultation(
                user_id=2,
                topic="Budget Review",
                start_time=datetime.now() - timedelta(hours=1),
                duration=45,
                notes="Reviewed current budget vs projections",
                status="in_progress"
            )
        ]
        
        for consultation in consultations:
            db.add(consultation)
        db.commit()
        print("  ✓ Created sample consultations")
        
        # Create sample messages
        print("  💭 Creating sample messages...")
        messages = [
            Message(
                consultation_id=1,
                sender="Daena VP",
                content="Let's review the Q4 strategic objectives",
                message_type="text"
            ),
            Message(
                consultation_id=1,
                sender="founder",
                content="I'd like to focus on market expansion",
                message_type="text"
            ),
            Message(
                consultation_id=2,
                sender="Alex Finance",
                content="Current budget shows 15% overrun in marketing",
                message_type="text"
            )
        ]
        
        for message in messages:
            db.add(message)
        db.commit()
        print("  ✓ Created sample messages")
        
        # Verify the database structure
        print("\n📋 Database schema verification:")
        conn = sqlite3.connect('./daena.db')
        cursor = conn.cursor()
        
        # Check tables
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = cursor.fetchall()
        print("  Tables created:")
        for table in tables:
            print(f"    - {table[0]}")
        
        # Check agents table
        cursor.execute("PRAGMA table_info(agents)")
        columns = cursor.fetchall()
        print("  Agents table columns:")
        for col in columns:
            print(f"    - {col[1]} ({col[2]})")
        
        # Check data counts
        cursor.execute("SELECT COUNT(*) FROM agents")
        agent_count = cursor.fetchone()[0]
        print(f"  ✓ {agent_count} agents in database")
        
        cursor.execute("SELECT COUNT(*) FROM users")
        user_count = cursor.fetchone()[0]
        print(f"  ✓ {user_count} users in database")
        
        cursor.execute("SELECT COUNT(*) FROM consultations")
        consultation_count = cursor.fetchone()[0]
        print(f"  ✓ {consultation_count} consultations in database")
        
        conn.close()
        
    except Exception as e:
        print(f"  ❌ Error populating database: {e}")
        db.rollback()
    finally:
        db.close()
    
    print("\n✅ Database initialization complete!")
    print("📊 Sample data includes:")
    print("  - 3 users (founder, ceo, manager)")
    print("  - 12 AI agents across all departments")
    print("  - Sample consultations and messages")
    print("\n🚀 Ready for testing!")

if __name__ == "__main__":
    init_database() 