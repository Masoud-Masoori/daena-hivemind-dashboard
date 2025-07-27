"""Advanced Natural Language to Agent Parser - Converts user descriptions into detailed agent blueprints."""

import re
import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import spacy
from transformers import pipeline
import openai
from Core.agent_builder.agent_blueprint import (
    AgentBlueprint, AgentType, AgentTask, AgentIntegration, 
    IntegrationType, SecurityLevel, TaskPriority
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntentType(str, Enum):
    """Types of user intents."""
    EMAIL_MANAGEMENT = "email_management"
    CALENDAR_SCHEDULING = "calendar_scheduling"
    CUSTOMER_SERVICE = "customer_service"
    DATA_ANALYSIS = "data_analysis"
    CONTENT_CREATION = "content_creation"
    PROJECT_MANAGEMENT = "project_management"
    RESEARCH = "research"
    SOCIAL_MEDIA = "social_media"
    FINANCIAL = "financial"
    PERSONAL_ASSISTANT = "personal_assistant"
    CUSTOM = "custom"

@dataclass
class ParsedIntent:
    """Parsed user intent."""
    primary_intent: IntentType
    confidence: float
    entities: List[Dict[str, Any]]
    requirements: List[str]
    constraints: List[str]
    integrations_needed: List[str]

class NLToAgentParser:
    """Advanced Natural Language to Agent Parser."""
    
    def __init__(self, openai_api_key: Optional[str] = None):
        """Initialize the parser with necessary models."""
        self.openai_api_key = openai_api_key
        if openai_api_key:
            openai.api_key = openai_api_key
        
        # Initialize NLP models
        try:
            self.nlp = spacy.load("en_core_web_sm")
        except OSError:
            logger.warning("spaCy model not found, using basic text processing")
            self.nlp = None
        
        # Intent classification patterns
        self.intent_patterns = {
            IntentType.EMAIL_MANAGEMENT: [
                r"email", r"inbox", r"gmail", r"outlook", r"reply", r"respond",
                r"sort", r"organize", r"filter", r"spam", r"priority"
            ],
            IntentType.CALENDAR_SCHEDULING: [
                r"calendar", r"schedule", r"meeting", r"appointment", r"booking",
                r"reminder", r"event", r"availability", r"time slot"
            ],
            IntentType.CUSTOMER_SERVICE: [
                r"customer", r"support", r"help", r"service", r"chat", r"ticket",
                r"inquiry", r"complaint", r"assist", r"resolve"
            ],
            IntentType.DATA_ANALYSIS: [
                r"analyze", r"data", r"report", r"insights", r"metrics", r"dashboard",
                r"statistics", r"trends", r"performance", r"kpi"
            ],
            IntentType.CONTENT_CREATION: [
                r"content", r"write", r"create", r"blog", r"article", r"post",
                r"social media", r"marketing", r"copy", r"creative"
            ],
            IntentType.PROJECT_MANAGEMENT: [
                r"project", r"task", r"deadline", r"team", r"collaboration",
                r"timeline", r"milestone", r"progress", r"coordinate"
            ],
            IntentType.RESEARCH: [
                r"research", r"find", r"search", r"investigate", r"gather",
                r"information", r"study", r"analysis", r"discover"
            ],
            IntentType.SOCIAL_MEDIA: [
                r"social", r"facebook", r"twitter", r"instagram", r"linkedin",
                r"post", r"engage", r"followers", r"brand"
            ],
            IntentType.FINANCIAL: [
                r"financial", r"budget", r"expense", r"invoice", r"payment",
                r"accounting", r"money", r"cost", r"revenue"
            ],
            IntentType.PERSONAL_ASSISTANT: [
                r"assistant", r"help", r"organize", r"manage", r"personal",
                r"daily", r"routine", r"tasks", r"reminders"
            ]
        }
        
        # Integration detection patterns
        self.integration_patterns = {
            "gmail": [r"gmail", r"google mail", r"email"],
            "outlook": [r"outlook", r"microsoft", r"office 365"],
            "slack": [r"slack", r"team chat", r"messaging"],
            "teams": [r"teams", r"microsoft teams"],
            "discord": [r"discord"],
            "whatsapp": [r"whatsapp", r"whats app"],
            "calendar": [r"calendar", r"google calendar", r"outlook calendar"],
            "notion": [r"notion"],
            "trello": [r"trello", r"kanban"],
            "asana": [r"asana"],
            "jira": [r"jira"],
            "github": [r"github", r"git"],
            "salesforce": [r"salesforce", r"crm"],
            "hubspot": [r"hubspot"],
            "stripe": [r"stripe", r"payment"],
            "paypal": [r"paypal"],
            "twitter": [r"twitter", r"tweet"],
            "facebook": [r"facebook"],
            "instagram": [r"instagram"],
            "linkedin": [r"linkedin"],
            "youtube": [r"youtube"],
            "dropbox": [r"dropbox"],
            "google_drive": [r"google drive", r"gdrive"],
            "onedrive": [r"onedrive", r"one drive"],
            "database": [r"database", r"sql", r"mysql", r"postgresql"],
            "api": [r"api", r"rest", r"webhook"]
        }

    def parse_user_request(self, user_input: str) -> ParsedIntent:
        """Parse user input to extract intent and requirements."""
        user_input = user_input.lower().strip()
        
        # Extract primary intent
        primary_intent, confidence = self._classify_intent(user_input)
        
        # Extract entities and requirements
        entities = self._extract_entities(user_input)
        requirements = self._extract_requirements(user_input)
        constraints = self._extract_constraints(user_input)
        integrations_needed = self._detect_integrations(user_input)
        
        return ParsedIntent(
            primary_intent=primary_intent,
            confidence=confidence,
            entities=entities,
            requirements=requirements,
            constraints=constraints,
            integrations_needed=integrations_needed
        )

    def _classify_intent(self, text: str) -> Tuple[IntentType, float]:
        """Classify the primary intent of the user request."""
        scores = {}
        
        for intent_type, patterns in self.intent_patterns.items():
            score = 0
            for pattern in patterns:
                matches = len(re.findall(pattern, text, re.IGNORECASE))
                score += matches
            scores[intent_type] = score
        
        # Find the highest scoring intent
        if scores:
            max_intent = max(scores, key=scores.get)
            max_score = scores[max_intent]
            total_score = sum(scores.values())
            confidence = max_score / total_score if total_score > 0 else 0.0
            
            # If confidence is too low, default to personal assistant
            if confidence < 0.3:
                return IntentType.PERSONAL_ASSISTANT, 0.5
            
            return max_intent, confidence
        
        return IntentType.PERSONAL_ASSISTANT, 0.5

    def _extract_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract named entities from the text."""
        entities = []
        
        if self.nlp:
            doc = self.nlp(text)
            for ent in doc.ents:
                entities.append({
                    "text": ent.text,
                    "label": ent.label_,
                    "start": ent.start_char,
                    "end": ent.end_char
                })
        
        # Extract custom entities using regex
        custom_entities = self._extract_custom_entities(text)
        entities.extend(custom_entities)
        
        return entities

    def _extract_custom_entities(self, text: str) -> List[Dict[str, Any]]:
        """Extract custom entities using regex patterns."""
        entities = []
        
        # Time patterns
        time_patterns = [
            (r"(\d{1,2}):(\d{2})\s*(am|pm)?", "TIME"),
            (r"(\d{1,2})\s*(am|pm)", "TIME"),
            (r"(morning|afternoon|evening|night)", "TIME_PERIOD"),
            (r"(daily|weekly|monthly|yearly)", "FREQUENCY")
        ]
        
        # Date patterns
        date_patterns = [
            (r"(\d{1,2})/(\d{1,2})/(\d{2,4})", "DATE"),
            (r"(monday|tuesday|wednesday|thursday|friday|saturday|sunday)", "DAY"),
            (r"(january|february|march|april|may|june|july|august|september|october|november|december)", "MONTH")
        ]
        
        # Priority patterns
        priority_patterns = [
            (r"(urgent|critical|important|high priority)", "PRIORITY_HIGH"),
            (r"(low priority|not urgent|when possible)", "PRIORITY_LOW")
        ]
        
        all_patterns = time_patterns + date_patterns + priority_patterns
        
        for pattern, label in all_patterns:
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    "text": match.group(),
                    "label": label,
                    "start": match.start(),
                    "end": match.end()
                })
        
        return entities

    def _extract_requirements(self, text: str) -> List[str]:
        """Extract functional requirements from the text."""
        requirements = []
        
        # Common requirement patterns
        requirement_patterns = [
            r"should\s+(\w+(?:\s+\w+)*)",
            r"must\s+(\w+(?:\s+\w+)*)",
            r"need\s+to\s+(\w+(?:\s+\w+)*)",
            r"want\s+to\s+(\w+(?:\s+\w+)*)",
            r"would\s+like\s+to\s+(\w+(?:\s+\w+)*)",
            r"(\w+(?:\s+\w+)*)\s+automatically",
            r"(\w+(?:\s+\w+)*)\s+every\s+(\w+)",
            r"(\w+(?:\s+\w+)*)\s+when\s+(\w+(?:\s+\w+)*)"
        ]
        
        for pattern in requirement_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    requirements.append(" ".join(match))
                else:
                    requirements.append(match)
        
        return list(set(requirements))

    def _extract_constraints(self, text: str) -> List[str]:
        """Extract constraints and limitations from the text."""
        constraints = []
        
        constraint_patterns = [
            r"only\s+(\w+(?:\s+\w+)*)",
            r"except\s+(\w+(?:\s+\w+)*)",
            r"not\s+(\w+(?:\s+\w+)*)",
            r"avoid\s+(\w+(?:\s+\w+)*)",
            r"don't\s+(\w+(?:\s+\w+)*)",
            r"never\s+(\w+(?:\s+\w+)*)",
            r"(\w+(?:\s+\w+)*)\s+only",
            r"(\w+(?:\s+\w+)*)\s+but\s+(\w+(?:\s+\w+)*)"
        ]
        
        for pattern in constraint_patterns:
            matches = re.findall(pattern, text, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    constraints.append(" ".join(match))
                else:
                    constraints.append(match)
        
        return list(set(constraints))

    def _detect_integrations(self, text: str) -> List[str]:
        """Detect required integrations from the text."""
        integrations = []
        
        for integration_name, patterns in self.integration_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text, re.IGNORECASE):
                    integrations.append(integration_name)
                    break
        
        return list(set(integrations))

    def generate_agent_blueprint(self, parsed_intent: ParsedIntent, user_input: str) -> AgentBlueprint:
        """Generate a complete agent blueprint from parsed intent."""
        
        # Map intent to agent type
        intent_to_type = {
            IntentType.EMAIL_MANAGEMENT: AgentType.EMAIL_MANAGER,
            IntentType.CALENDAR_SCHEDULING: AgentType.CALENDAR_ASSISTANT,
            IntentType.CUSTOMER_SERVICE: AgentType.CUSTOMER_SERVICE,
            IntentType.DATA_ANALYSIS: AgentType.DATA_ANALYST,
            IntentType.CONTENT_CREATION: AgentType.CONTENT_CREATOR,
            IntentType.PROJECT_MANAGEMENT: AgentType.PROJECT_MANAGER,
            IntentType.RESEARCH: AgentType.RESEARCH_ASSISTANT,
            IntentType.SOCIAL_MEDIA: AgentType.SOCIAL_MEDIA_MANAGER,
            IntentType.FINANCIAL: AgentType.FINANCIAL_ADVISOR,
            IntentType.PERSONAL_ASSISTANT: AgentType.PERSONAL_ASSISTANT
        }
        
        agent_type = intent_to_type.get(parsed_intent.primary_intent, AgentType.CUSTOM)
        
        # Generate agent name
        agent_name = self._generate_agent_name(user_input, agent_type)
        
        # Generate description
        description = self._generate_description(user_input, parsed_intent)
        
        # Generate tasks
        tasks = self._generate_tasks(parsed_intent, user_input)
        
        # Generate integrations
        integrations = self._generate_integrations(parsed_intent.integrations_needed)
        
        # Generate capabilities
        capabilities = self._generate_capabilities(parsed_intent, agent_type)
        
        # Generate security configuration
        security = self._generate_security_config(parsed_intent)
        
        # Create the blueprint
        blueprint = AgentBlueprint(
            name=agent_name,
            description=description,
            type=agent_type,
            capabilities=capabilities,
            tasks=tasks,
            integrations=integrations,
            security=security,
            tags=[parsed_intent.primary_intent.value, "ai_generated"],
            category=agent_type.value,
            difficulty_level=self._assess_difficulty(parsed_intent),
            estimated_cost=self._estimate_cost(parsed_intent),
            custom_config={
                "source_request": user_input,
                "parsed_intent": parsed_intent.primary_intent.value,
                "confidence": parsed_intent.confidence,
                "entities": parsed_intent.entities,
                "requirements": parsed_intent.requirements,
                "constraints": parsed_intent.constraints
            }
        )
        
        return blueprint

    def _generate_agent_name(self, user_input: str, agent_type: AgentType) -> str:
        """Generate a descriptive name for the agent."""
        # Extract key words from user input
        words = re.findall(r'\b\w+\b', user_input.lower())
        
        # Filter out common words
        common_words = {'the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by', 'is', 'are', 'was', 'were', 'be', 'been', 'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 'may', 'might', 'can', 'must', 'shall'}
        key_words = [word for word in words if word not in common_words and len(word) > 3]
        
        if key_words:
            # Use the first few key words
            name_parts = key_words[:3]
            agent_name = " ".join(name_parts).title() + " Assistant"
        else:
            # Fallback to type-based name
            type_name = agent_type.value.replace('_', ' ').title()
            agent_name = f"Smart {type_name}"
        
        return agent_name

    def _generate_description(self, user_input: str, parsed_intent: ParsedIntent) -> str:
        """Generate a description for the agent."""
        base_description = f"AI-powered {parsed_intent.primary_intent.value.replace('_', ' ')} agent"
        
        if parsed_intent.requirements:
            req_text = ", ".join(parsed_intent.requirements[:3])
            return f"{base_description} that {req_text}."
        
        return f"{base_description} designed to help with your specific needs."

    def _generate_tasks(self, parsed_intent: ParsedIntent, user_input: str) -> List[AgentTask]:
        """Generate tasks based on the parsed intent."""
        tasks = []
        
        # Generate tasks based on intent type
        if parsed_intent.primary_intent == IntentType.EMAIL_MANAGEMENT:
            tasks.extend([
                AgentTask(
                    name="Email Monitoring",
                    description="Monitor incoming emails and categorize them",
                    priority=TaskPriority.HIGH,
                    triggers=["new_email_received"],
                    actions=[{"action": "categorize_email", "params": {}}]
                ),
                AgentTask(
                    name="Smart Reply Generation",
                    description="Generate contextual replies to emails",
                    priority=TaskPriority.MEDIUM,
                    triggers=["email_categorized"],
                    actions=[{"action": "generate_reply", "params": {}}]
                ),
                AgentTask(
                    name="Email Prioritization",
                    description="Prioritize emails based on importance and urgency",
                    priority=TaskPriority.HIGH,
                    triggers=["email_analyzed"],
                    actions=[{"action": "set_priority", "params": {}}]
                )
            ])
        
        elif parsed_intent.primary_intent == IntentType.CALENDAR_SCHEDULING:
            tasks.extend([
                AgentTask(
                    name="Schedule Management",
                    description="Monitor and manage calendar events",
                    priority=TaskPriority.HIGH,
                    triggers=["calendar_update"],
                    actions=[{"action": "update_schedule", "params": {}}]
                ),
                AgentTask(
                    name="Meeting Coordination",
                    description="Coordinate meeting times and participants",
                    priority=TaskPriority.MEDIUM,
                    triggers=["meeting_request"],
                    actions=[{"action": "coordinate_meeting", "params": {}}]
                ),
                AgentTask(
                    name="Reminder System",
                    description="Send timely reminders for upcoming events",
                    priority=TaskPriority.MEDIUM,
                    triggers=["event_approaching"],
                    actions=[{"action": "send_reminder", "params": {}}]
                )
            ])
        
        # Add custom tasks based on requirements
        for i, requirement in enumerate(parsed_intent.requirements[:5]):
            tasks.append(AgentTask(
                name=f"Custom Task {i+1}",
                description=f"Handle: {requirement}",
                priority=TaskPriority.MEDIUM,
                triggers=["user_request"],
                actions=[{"action": "custom_action", "params": {"requirement": requirement}}]
            ))
        
        return tasks

    def _generate_integrations(self, integration_names: List[str]) -> List[AgentIntegration]:
        """Generate integration configurations."""
        integrations = []
        
        integration_mapping = {
            "gmail": IntegrationType.EMAIL,
            "outlook": IntegrationType.EMAIL,
            "calendar": IntegrationType.CALENDAR,
            "slack": IntegrationType.CHAT,
            "teams": IntegrationType.CHAT,
            "discord": IntegrationType.CHAT,
            "whatsapp": IntegrationType.CHAT,
            "notion": IntegrationType.FILE_STORAGE,
            "trello": IntegrationType.PROJECT_MANAGEMENT,
            "asana": IntegrationType.PROJECT_MANAGEMENT,
            "jira": IntegrationType.PROJECT_MANAGEMENT,
            "github": IntegrationType.API,
            "salesforce": IntegrationType.CRM,
            "hubspot": IntegrationType.CRM,
            "stripe": IntegrationType.API,
            "paypal": IntegrationType.API,
            "twitter": IntegrationType.SOCIAL_MEDIA,
            "facebook": IntegrationType.SOCIAL_MEDIA,
            "instagram": IntegrationType.SOCIAL_MEDIA,
            "linkedin": IntegrationType.SOCIAL_MEDIA,
            "youtube": IntegrationType.SOCIAL_MEDIA,
            "dropbox": IntegrationType.FILE_STORAGE,
            "google_drive": IntegrationType.FILE_STORAGE,
            "onedrive": IntegrationType.FILE_STORAGE,
            "database": IntegrationType.DATABASE,
            "api": IntegrationType.API
        }
        
        for integration_name in integration_names:
            integration_type = integration_mapping.get(integration_name, IntegrationType.API)
            integrations.append(AgentIntegration(
                type=integration_type,
                name=integration_name.replace('_', ' ').title(),
                config={"enabled": True, "auto_connect": True},
                permissions=["read", "write"],
                oauth_config={"required": True, "scopes": ["basic"]}
            ))
        
        return integrations

    def _generate_capabilities(self, parsed_intent: ParsedIntent, agent_type: AgentType) -> List[str]:
        """Generate capabilities based on intent and type."""
        base_capabilities = {
            AgentType.EMAIL_MANAGER: ["email_processing", "smart_categorization", "auto_reply"],
            AgentType.CALENDAR_ASSISTANT: ["schedule_management", "meeting_coordination", "reminder_system"],
            AgentType.CUSTOMER_SERVICE: ["chat_support", "ticket_management", "knowledge_base"],
            AgentType.DATA_ANALYST: ["data_processing", "report_generation", "trend_analysis"],
            AgentType.CONTENT_CREATOR: ["content_generation", "editing", "publishing"],
            AgentType.PROJECT_MANAGER: ["task_tracking", "team_coordination", "progress_monitoring"],
            AgentType.RESEARCH_ASSISTANT: ["information_gathering", "source_analysis", "summary_generation"],
            AgentType.SOCIAL_MEDIA_MANAGER: ["content_scheduling", "engagement_monitoring", "analytics"],
            AgentType.FINANCIAL_ADVISOR: ["expense_tracking", "budget_analysis", "financial_reporting"],
            AgentType.PERSONAL_ASSISTANT: ["task_management", "information_retrieval", "scheduling"]
        }
        
        capabilities = base_capabilities.get(agent_type, ["general_assistance"])
        
        # Add capabilities based on requirements
        for requirement in parsed_intent.requirements:
            if "automate" in requirement.lower():
                capabilities.append("automation")
            if "analyze" in requirement.lower():
                capabilities.append("analysis")
            if "communicate" in requirement.lower():
                capabilities.append("communication")
            if "organize" in requirement.lower():
                capabilities.append("organization")
        
        return list(set(capabilities))

    def _generate_security_config(self, parsed_intent: ParsedIntent) -> 'AgentSecurity':
        """Generate security configuration."""
        from Core.agent_builder.agent_blueprint import AgentSecurity, SecurityLevel
        
        # Determine security level based on integrations and requirements
        security_level = SecurityLevel.BASIC
        
        if any(integration in parsed_intent.integrations_needed for integration in ["database", "api", "financial"]):
            security_level = SecurityLevel.ENHANCED
        
        if "financial" in parsed_intent.integrations_needed or "enterprise" in str(parsed_intent.requirements).lower():
            security_level = SecurityLevel.ENTERPRISE
        
        return AgentSecurity(
            level=security_level,
            encryption_enabled=True,
            audit_logging=True,
            data_retention_days=90 if security_level == SecurityLevel.BASIC else 365,
            threat_detection=security_level in [SecurityLevel.ENHANCED, SecurityLevel.ENTERPRISE],
            sandbox_mode=True,
            api_rate_limiting=True
        )

    def _assess_difficulty(self, parsed_intent: ParsedIntent) -> str:
        """Assess the difficulty level of the agent."""
        complexity_score = 0
        
        # Add points for integrations
        complexity_score += len(parsed_intent.integrations_needed) * 2
        
        # Add points for requirements
        complexity_score += len(parsed_intent.requirements) * 1
        
        # Add points for constraints
        complexity_score += len(parsed_intent.constraints) * 1
        
        if complexity_score <= 3:
            return "beginner"
        elif complexity_score <= 8:
            return "intermediate"
        else:
            return "advanced"

    def _estimate_cost(self, parsed_intent: ParsedIntent) -> float:
        """Estimate the monthly cost of running this agent."""
        base_cost = 10.0  # Base monthly cost
        
        # Add cost for integrations
        integration_cost = len(parsed_intent.integrations_needed) * 5.0
        
        # Add cost for complexity
        complexity_cost = len(parsed_intent.requirements) * 2.0
        
        return base_cost + integration_cost + complexity_cost

    def create_agent_from_text(self, user_input: str) -> AgentBlueprint:
        """Main method to create an agent from natural language input."""
        try:
            # Parse the user input
            parsed_intent = self.parse_user_request(user_input)
            
            # Generate the blueprint
            blueprint = self.generate_agent_blueprint(parsed_intent, user_input)
            
            logger.info(f"Generated agent blueprint: {blueprint.name} (Type: {blueprint.type})")
            
            return blueprint
            
        except Exception as e:
            logger.error(f"Error creating agent from text: {e}")
            # Return a basic fallback agent
            return AgentBlueprint(
                name="Basic Assistant",
                description="A basic AI assistant to help with your needs.",
                type=AgentType.PERSONAL_ASSISTANT,
                capabilities=["general_assistance"],
                tasks=[
                    AgentTask(
                        name="General Help",
                        description="Provide general assistance and support",
                        priority=TaskPriority.MEDIUM,
                        triggers=["user_request"],
                        actions=[{"action": "general_help", "params": {}}]
                    )
                ]
            ) 