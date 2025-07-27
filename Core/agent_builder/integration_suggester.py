"""Advanced Integration Suggester - Intelligently recommends and configures integrations for agents."""

import json
import logging
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass
from enum import Enum
import re
from pydantic import BaseModel
from Core.agent_builder.agent_blueprint import AgentBlueprint, AgentType, IntegrationType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class IntegrationCategory(str, Enum):
    """Categories of integrations."""
    COMMUNICATION = "communication"
    PRODUCTIVITY = "productivity"
    STORAGE = "storage"
    ANALYTICS = "analytics"
    FINANCIAL = "financial"
    SOCIAL = "social"
    DEVELOPMENT = "development"
    CUSTOM = "custom"

class IntegrationComplexity(str, Enum):
    """Complexity levels for integrations."""
    SIMPLE = "simple"
    MODERATE = "moderate"
    COMPLEX = "complex"
    ENTERPRISE = "enterprise"

@dataclass
class IntegrationSuggestion:
    """Suggestion for an integration."""
    name: str
    type: IntegrationType
    category: IntegrationCategory
    complexity: IntegrationComplexity
    confidence: float
    reasoning: str
    required_permissions: List[str]
    estimated_setup_time: int  # in minutes
    cost_per_month: float
    alternatives: List[str]
    prerequisites: List[str]
    benefits: List[str]
    risks: List[str]

class IntegrationConfig(BaseModel):
    """Configuration for an integration."""
    name: str
    type: IntegrationType
    api_endpoint: Optional[str] = None
    auth_method: str = "oauth2"
    required_scopes: List[str] = []
    rate_limits: Dict[str, Any] = {}
    webhook_support: bool = False
    webhook_events: List[str] = []
    custom_fields: Dict[str, Any] = {}
    security_requirements: Dict[str, Any] = {}

class IntegrationSuggester:
    """Advanced Integration Suggester for intelligent integration recommendations."""
    
    def __init__(self):
        """Initialize the integration suggester."""
        self.integration_database = self._load_integration_database()
        self.agent_type_patterns = self._load_agent_type_patterns()
        self.integration_relationships = self._load_integration_relationships()
        
    def _load_integration_database(self) -> Dict[str, Dict[str, Any]]:
        """Load the integration database with detailed information."""
        return {
            "gmail": {
                "name": "Gmail",
                "type": IntegrationType.EMAIL,
                "category": IntegrationCategory.COMMUNICATION,
                "complexity": IntegrationComplexity.SIMPLE,
                "api_endpoint": "https://gmail.googleapis.com/gmail/v1",
                "auth_method": "oauth2",
                "required_scopes": ["https://www.googleapis.com/auth/gmail.readonly", "https://www.googleapis.com/auth/gmail.send"],
                "rate_limits": {"requests_per_day": 1000000, "requests_per_second": 250},
                "webhook_support": True,
                "webhook_events": ["message_received", "message_sent"],
                "setup_time": 5,
                "cost_per_month": 0.0,
                "alternatives": ["outlook", "yahoo_mail"],
                "prerequisites": ["google_account"],
                "benefits": ["Reliable", "Widely used", "Good API"],
                "risks": ["Rate limits", "OAuth complexity"]
            },
            "outlook": {
                "name": "Microsoft Outlook",
                "type": IntegrationType.EMAIL,
                "category": IntegrationCategory.COMMUNICATION,
                "complexity": IntegrationComplexity.SIMPLE,
                "api_endpoint": "https://graph.microsoft.com/v1.0",
                "auth_method": "oauth2",
                "required_scopes": ["Mail.Read", "Mail.Send"],
                "rate_limits": {"requests_per_minute": 1000},
                "webhook_support": True,
                "webhook_events": ["message_received", "message_sent"],
                "setup_time": 5,
                "cost_per_month": 0.0,
                "alternatives": ["gmail", "yahoo_mail"],
                "prerequisites": ["microsoft_account"],
                "benefits": ["Enterprise integration", "Office 365 ecosystem"],
                "risks": ["Complex permissions", "Corporate policies"]
            },
            "slack": {
                "name": "Slack",
                "type": IntegrationType.CHAT,
                "category": IntegrationCategory.COMMUNICATION,
                "complexity": IntegrationComplexity.SIMPLE,
                "api_endpoint": "https://slack.com/api",
                "auth_method": "oauth2",
                "required_scopes": ["chat:write", "channels:read", "users:read"],
                "rate_limits": {"requests_per_minute": 50},
                "webhook_support": True,
                "webhook_events": ["message", "reaction_added", "user_joined"],
                "setup_time": 3,
                "cost_per_month": 0.0,
                "alternatives": ["teams", "discord"],
                "prerequisites": ["slack_workspace"],
                "benefits": ["Real-time communication", "Rich API"],
                "risks": ["Rate limits", "Workspace permissions"]
            },
            "google_calendar": {
                "name": "Google Calendar",
                "type": IntegrationType.CALENDAR,
                "category": IntegrationCategory.PRODUCTIVITY,
                "complexity": IntegrationComplexity.SIMPLE,
                "api_endpoint": "https://www.googleapis.com/calendar/v3",
                "auth_method": "oauth2",
                "required_scopes": ["https://www.googleapis.com/auth/calendar"],
                "rate_limits": {"requests_per_day": 1000000},
                "webhook_support": True,
                "webhook_events": ["event_created", "event_updated", "event_deleted"],
                "setup_time": 3,
                "cost_per_month": 0.0,
                "alternatives": ["outlook_calendar", "apple_calendar"],
                "prerequisites": ["google_account"],
                "benefits": ["Reliable", "Good API", "Wide adoption"],
                "risks": ["OAuth complexity", "Calendar permissions"]
            },
            "notion": {
                "name": "Notion",
                "type": IntegrationType.FILE_STORAGE,
                "category": IntegrationCategory.PRODUCTIVITY,
                "complexity": IntegrationComplexity.MODERATE,
                "api_endpoint": "https://api.notion.com/v1",
                "auth_method": "api_key",
                "required_scopes": ["read", "write"],
                "rate_limits": {"requests_per_second": 3},
                "webhook_support": True,
                "webhook_events": ["page_created", "page_updated"],
                "setup_time": 8,
                "cost_per_month": 0.0,
                "alternatives": ["confluence", "evernote"],
                "prerequisites": ["notion_workspace", "api_key"],
                "benefits": ["Rich content", "Flexible structure"],
                "risks": ["Rate limits", "Complex API"]
            },
            "trello": {
                "name": "Trello",
                "type": IntegrationType.PROJECT_MANAGEMENT,
                "category": IntegrationCategory.PRODUCTIVITY,
                "complexity": IntegrationComplexity.SIMPLE,
                "api_endpoint": "https://api.trello.com/1",
                "auth_method": "api_key",
                "required_scopes": ["read", "write"],
                "rate_limits": {"requests_per_10_seconds": 100},
                "webhook_support": True,
                "webhook_events": ["card_created", "card_updated", "list_updated"],
                "setup_time": 4,
                "cost_per_month": 0.0,
                "alternatives": ["asana", "jira"],
                "prerequisites": ["trello_account", "api_key"],
                "benefits": ["Simple API", "Visual interface"],
                "risks": ["Limited features", "Rate limits"]
            },
            "salesforce": {
                "name": "Salesforce",
                "type": IntegrationType.CRM,
                "category": IntegrationCategory.ANALYTICS,
                "complexity": IntegrationComplexity.COMPLEX,
                "api_endpoint": "https://your-instance.salesforce.com/services/data/v58.0",
                "auth_method": "oauth2",
                "required_scopes": ["api", "refresh_token"],
                "rate_limits": {"requests_per_day": 15000},
                "webhook_support": True,
                "webhook_events": ["lead_created", "opportunity_updated"],
                "setup_time": 15,
                "cost_per_month": 25.0,
                "alternatives": ["hubspot", "pipedrive"],
                "prerequisites": ["salesforce_account", "admin_access"],
                "benefits": ["Comprehensive CRM", "Enterprise features"],
                "risks": ["Complex setup", "High cost", "Steep learning curve"]
            },
            "stripe": {
                "name": "Stripe",
                "type": IntegrationType.API,
                "category": IntegrationCategory.FINANCIAL,
                "complexity": IntegrationComplexity.MODERATE,
                "api_endpoint": "https://api.stripe.com/v1",
                "auth_method": "api_key",
                "required_scopes": ["read", "write"],
                "rate_limits": {"requests_per_second": 100},
                "webhook_support": True,
                "webhook_events": ["payment_intent.succeeded", "invoice.payment_succeeded"],
                "setup_time": 10,
                "cost_per_month": 0.0,
                "alternatives": ["paypal", "square"],
                "prerequisites": ["stripe_account", "api_keys"],
                "benefits": ["Reliable payments", "Good documentation"],
                "risks": ["Financial data", "Compliance requirements"]
            },
            "twitter": {
                "name": "Twitter",
                "type": IntegrationType.SOCIAL_MEDIA,
                "category": IntegrationCategory.SOCIAL,
                "complexity": IntegrationComplexity.MODERATE,
                "api_endpoint": "https://api.twitter.com/2",
                "auth_method": "oauth2",
                "required_scopes": ["tweet.read", "tweet.write", "users.read"],
                "rate_limits": {"requests_per_15_minutes": 300},
                "webhook_support": True,
                "webhook_events": ["tweet_created", "mention"],
                "setup_time": 8,
                "cost_per_month": 0.0,
                "alternatives": ["facebook", "linkedin"],
                "prerequisites": ["twitter_account", "developer_account"],
                "benefits": ["Real-time updates", "Wide reach"],
                "risks": ["Rate limits", "Content policies"]
            },
            "github": {
                "name": "GitHub",
                "type": IntegrationType.API,
                "category": IntegrationCategory.DEVELOPMENT,
                "complexity": IntegrationComplexity.MODERATE,
                "api_endpoint": "https://api.github.com",
                "auth_method": "oauth2",
                "required_scopes": ["repo", "user"],
                "rate_limits": {"requests_per_hour": 5000},
                "webhook_support": True,
                "webhook_events": ["push", "pull_request", "issue"],
                "setup_time": 6,
                "cost_per_month": 0.0,
                "alternatives": ["gitlab", "bitbucket"],
                "prerequisites": ["github_account"],
                "benefits": ["Version control", "CI/CD integration"],
                "risks": ["Code security", "Repository access"]
            }
        }

    def _load_agent_type_patterns(self) -> Dict[AgentType, List[str]]:
        """Load patterns for agent types to suggest integrations."""
        return {
            AgentType.EMAIL_MANAGER: ["gmail", "outlook", "slack", "teams"],
            AgentType.CALENDAR_ASSISTANT: ["google_calendar", "outlook_calendar", "slack", "teams"],
            AgentType.CUSTOMER_SERVICE: ["slack", "teams", "gmail", "outlook", "salesforce"],
            AgentType.DATA_ANALYST: ["notion", "google_drive", "dropbox", "salesforce"],
            AgentType.CONTENT_CREATOR: ["notion", "twitter", "facebook", "linkedin", "wordpress"],
            AgentType.PROJECT_MANAGER: ["trello", "asana", "jira", "slack", "teams"],
            AgentType.RESEARCH_ASSISTANT: ["notion", "google_drive", "dropbox", "github"],
            AgentType.SOCIAL_MEDIA_MANAGER: ["twitter", "facebook", "instagram", "linkedin", "buffer"],
            AgentType.FINANCIAL_ADVISOR: ["stripe", "paypal", "quickbooks", "excel"],
            AgentType.PERSONAL_ASSISTANT: ["gmail", "google_calendar", "slack", "notion", "trello"]
        }

    def _load_integration_relationships(self) -> Dict[str, List[str]]:
        """Load relationships between integrations."""
        return {
            "gmail": ["google_calendar", "google_drive"],
            "outlook": ["outlook_calendar", "onedrive"],
            "slack": ["trello", "github", "jira"],
            "teams": ["outlook", "onedrive", "sharepoint"],
            "salesforce": ["gmail", "outlook", "slack"],
            "stripe": ["gmail", "slack", "notion"],
            "github": ["slack", "trello", "jira"],
            "notion": ["slack", "gmail", "google_calendar"],
            "trello": ["slack", "github", "gmail"]
        }

    def suggest_integrations(self, 
                           agent_blueprint: AgentBlueprint,
                           user_preferences: Optional[Dict[str, Any]] = None) -> List[IntegrationSuggestion]:
        """Suggest integrations for an agent blueprint."""
        suggestions = []
        
        # Get base suggestions from agent type
        base_integrations = self.agent_type_patterns.get(agent_blueprint.type, [])
        
        # Analyze requirements for additional integrations
        requirements_text = " ".join(agent_blueprint.capabilities + agent_blueprint.skills)
        detected_integrations = self._detect_integrations_from_text(requirements_text)
        
        # Combine and deduplicate
        all_integration_names = list(set(base_integrations + detected_integrations))
        
        # Generate suggestions
        for integration_name in all_integration_names:
            if integration_name in self.integration_database:
                suggestion = self._create_integration_suggestion(
                    integration_name, 
                    agent_blueprint, 
                    user_preferences
                )
                suggestions.append(suggestion)
        
        # Sort by confidence and relevance
        suggestions.sort(key=lambda x: x.confidence, reverse=True)
        
        # Add related integrations
        related_suggestions = self._suggest_related_integrations(suggestions, agent_blueprint)
        suggestions.extend(related_suggestions)
        
        return suggestions[:10]  # Return top 10 suggestions

    def _detect_integrations_from_text(self, text: str) -> List[str]:
        """Detect integrations mentioned in text."""
        detected = []
        text_lower = text.lower()
        
        for integration_name, integration_data in self.integration_database.items():
            # Check if integration name is mentioned
            if integration_name in text_lower:
                detected.append(integration_name)
                continue
            
            # Check alternative names
            if "gmail" in text_lower or "google mail" in text_lower:
                detected.append("gmail")
            elif "outlook" in text_lower or "microsoft" in text_lower:
                detected.append("outlook")
            elif "slack" in text_lower or "team chat" in text_lower:
                detected.append("slack")
            elif "calendar" in text_lower:
                detected.append("google_calendar")
            elif "notion" in text_lower:
                detected.append("notion")
            elif "trello" in text_lower or "kanban" in text_lower:
                detected.append("trello")
            elif "salesforce" in text_lower or "crm" in text_lower:
                detected.append("salesforce")
            elif "stripe" in text_lower or "payment" in text_lower:
                detected.append("stripe")
            elif "twitter" in text_lower or "tweet" in text_lower:
                detected.append("twitter")
            elif "github" in text_lower or "git" in text_lower:
                detected.append("github")
        
        return list(set(detected))

    def _create_integration_suggestion(self, 
                                     integration_name: str,
                                     agent_blueprint: AgentBlueprint,
                                     user_preferences: Optional[Dict[str, Any]] = None) -> IntegrationSuggestion:
        """Create an integration suggestion."""
        integration_data = self.integration_database[integration_name]
        
        # Calculate confidence based on agent type and requirements
        confidence = self._calculate_confidence(integration_name, agent_blueprint, user_preferences)
        
        # Get related integrations
        related = self.integration_relationships.get(integration_name, [])
        
        # Filter alternatives based on agent type
        alternatives = [alt for alt in integration_data["alternatives"] 
                       if alt in self.agent_type_patterns.get(agent_blueprint.type, [])]
        
        return IntegrationSuggestion(
            name=integration_data["name"],
            type=integration_data["type"],
            category=integration_data["category"],
            complexity=integration_data["complexity"],
            confidence=confidence,
            reasoning=self._generate_reasoning(integration_name, agent_blueprint),
            required_permissions=integration_data["required_scopes"],
            estimated_setup_time=integration_data["setup_time"],
            cost_per_month=integration_data["cost_per_month"],
            alternatives=alternatives,
            prerequisites=integration_data["prerequisites"],
            benefits=integration_data["benefits"],
            risks=integration_data["risks"]
        )

    def _calculate_confidence(self, 
                            integration_name: str,
                            agent_blueprint: AgentBlueprint,
                            user_preferences: Optional[Dict[str, Any]] = None) -> float:
        """Calculate confidence score for an integration suggestion."""
        confidence = 0.5  # Base confidence
        
        # Agent type match
        if integration_name in self.agent_type_patterns.get(agent_blueprint.type, []):
            confidence += 0.3
        
        # Capability match
        capabilities_text = " ".join(agent_blueprint.capabilities).lower()
        integration_data = self.integration_database[integration_name]
        
        if integration_data["type"] == IntegrationType.EMAIL and "email" in capabilities_text:
            confidence += 0.2
        elif integration_data["type"] == IntegrationType.CALENDAR and "calendar" in capabilities_text:
            confidence += 0.2
        elif integration_data["type"] == IntegrationType.CHAT and "chat" in capabilities_text:
            confidence += 0.2
        elif integration_data["type"] == IntegrationType.CRM and "customer" in capabilities_text:
            confidence += 0.2
        
        # User preferences
        if user_preferences:
            if "prefer_free" in user_preferences and self.integration_database[integration_name]["cost_per_month"] == 0:
                confidence += 0.1
            if "prefer_simple" in user_preferences and self.integration_database[integration_name]["complexity"] == IntegrationComplexity.SIMPLE:
                confidence += 0.1
        
        return min(confidence, 1.0)

    def _generate_reasoning(self, integration_name: str, agent_blueprint: AgentBlueprint) -> str:
        """Generate reasoning for why this integration is suggested."""
        integration_data = self.integration_database[integration_name]
        agent_type = agent_blueprint.type.value.replace('_', ' ')
        
        reasoning_templates = {
            IntegrationType.EMAIL: f"Essential for {agent_type} to handle email communications",
            IntegrationType.CALENDAR: f"Required for {agent_type} to manage scheduling and appointments",
            IntegrationType.CHAT: f"Enables {agent_type} to communicate in real-time",
            IntegrationType.CRM: f"Provides {agent_type} with customer relationship data",
            IntegrationType.FILE_STORAGE: f"Allows {agent_type} to store and access documents",
            IntegrationType.PROJECT_MANAGEMENT: f"Helps {agent_type} organize tasks and projects",
            IntegrationType.SOCIAL_MEDIA: f"Enables {agent_type} to manage social media presence",
            IntegrationType.API: f"Provides {agent_type} with programmatic access to data"
        }
        
        return reasoning_templates.get(integration_data["type"], f"Useful for {agent_type} functionality")

    def _suggest_related_integrations(self, 
                                    current_suggestions: List[IntegrationSuggestion],
                                    agent_blueprint: AgentBlueprint) -> List[IntegrationSuggestion]:
        """Suggest related integrations based on current suggestions."""
        related_suggestions = []
        suggested_names = [s.name.lower() for s in current_suggestions]
        
        for suggestion in current_suggestions:
            integration_name = suggestion.name.lower().replace(" ", "_")
            related = self.integration_relationships.get(integration_name, [])
            
            for related_name in related:
                if related_name not in suggested_names and related_name in self.integration_database:
                    related_suggestion = self._create_integration_suggestion(
                        related_name, 
                        agent_blueprint
                    )
                    related_suggestion.confidence *= 0.7  # Lower confidence for related suggestions
                    related_suggestions.append(related_suggestion)
                    suggested_names.append(related_name)
        
        return related_suggestions

    def get_integration_config(self, integration_name: str) -> IntegrationConfig:
        """Get configuration for a specific integration."""
        if integration_name not in self.integration_database:
            raise ValueError(f"Integration '{integration_name}' not found")
        
        integration_data = self.integration_database[integration_name]
        
        return IntegrationConfig(
            name=integration_data["name"],
            type=integration_data["type"],
            api_endpoint=integration_data.get("api_endpoint"),
            auth_method=integration_data["auth_method"],
            required_scopes=integration_data["required_scopes"],
            rate_limits=integration_data["rate_limits"],
            webhook_support=integration_data["webhook_support"],
            webhook_events=integration_data["webhook_events"],
            custom_fields=integration_data.get("custom_fields", {}),
            security_requirements={
                "encryption": True,
                "audit_logging": True,
                "rate_limiting": True
            }
        )

    def validate_integration_setup(self, 
                                 integration_name: str,
                                 setup_data: Dict[str, Any]) -> Tuple[bool, List[str]]:
        """Validate integration setup data."""
        if integration_name not in self.integration_database:
            return False, [f"Integration '{integration_name}' not found"]
        
        integration_data = self.integration_database[integration_name]
        errors = []
        
        # Check required fields
        if integration_data["auth_method"] == "oauth2":
            if "client_id" not in setup_data:
                errors.append("OAuth2 client_id is required")
            if "client_secret" not in setup_data:
                errors.append("OAuth2 client_secret is required")
        elif integration_data["auth_method"] == "api_key":
            if "api_key" not in setup_data:
                errors.append("API key is required")
        
        # Check prerequisites
        for prerequisite in integration_data["prerequisites"]:
            if prerequisite not in setup_data.get("prerequisites_met", []):
                errors.append(f"Prerequisite '{prerequisite}' not met")
        
        return len(errors) == 0, errors

    def get_integration_alternatives(self, integration_name: str) -> List[Dict[str, Any]]:
        """Get alternative integrations for a given integration."""
        if integration_name not in self.integration_database:
            return []
        
        integration_data = self.integration_database[integration_name]
        alternatives = []
        
        for alt_name in integration_data["alternatives"]:
            if alt_name in self.integration_database:
                alt_data = self.integration_database[alt_name]
                alternatives.append({
                    "name": alt_data["name"],
                    "type": alt_data["type"],
                    "complexity": alt_data["complexity"],
                    "cost_per_month": alt_data["cost_per_month"],
                    "setup_time": alt_data["setup_time"],
                    "benefits": alt_data["benefits"],
                    "risks": alt_data["risks"]
                })
        
        return alternatives

    def estimate_setup_complexity(self, integration_names: List[str]) -> Dict[str, Any]:
        """Estimate the complexity of setting up multiple integrations."""
        total_setup_time = 0
        total_cost = 0.0
        complexity_levels = []
        risks = []
        
        for integration_name in integration_names:
            if integration_name in self.integration_database:
                data = self.integration_database[integration_name]
                total_setup_time += data["setup_time"]
                total_cost += data["cost_per_month"]
                complexity_levels.append(data["complexity"])
                risks.extend(data["risks"])
        
        # Determine overall complexity
        if IntegrationComplexity.ENTERPRISE in complexity_levels:
            overall_complexity = IntegrationComplexity.ENTERPRISE
        elif IntegrationComplexity.COMPLEX in complexity_levels:
            overall_complexity = IntegrationComplexity.COMPLEX
        elif IntegrationComplexity.MODERATE in complexity_levels:
            overall_complexity = IntegrationComplexity.MODERATE
        else:
            overall_complexity = IntegrationComplexity.SIMPLE
        
        return {
            "total_setup_time": total_setup_time,
            "total_monthly_cost": total_cost,
            "overall_complexity": overall_complexity,
            "complexity_breakdown": complexity_levels,
            "combined_risks": list(set(risks)),
            "estimated_success_rate": self._calculate_success_rate(complexity_levels)
        }

    def _calculate_success_rate(self, complexity_levels: List[IntegrationComplexity]) -> float:
        """Calculate estimated success rate based on complexity levels."""
        success_rates = {
            IntegrationComplexity.SIMPLE: 0.95,
            IntegrationComplexity.MODERATE: 0.85,
            IntegrationComplexity.COMPLEX: 0.70,
            IntegrationComplexity.ENTERPRISE: 0.50
        }
        
        if not complexity_levels:
            return 0.0
        
        total_rate = sum(success_rates[level] for level in complexity_levels)
        return total_rate / len(complexity_levels) 