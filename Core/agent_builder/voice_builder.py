"""Advanced Voice-Guided Agent Builder - Creates agents through natural voice conversation."""

import asyncio
import json
import logging
from typing import Dict, List, Optional, Any, Callable
from dataclasses import dataclass
from enum import Enum
import speech_recognition as sr
import pyttsx3
from pydantic import BaseModel
from Core.agent_builder.nl_parser import NLToAgentParser, ParsedIntent
from Core.agent_builder.agent_blueprint import AgentBlueprint, AgentType

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ConversationState(str, Enum):
    """States of the voice conversation."""
    INITIAL = "initial"
    GATHERING_REQUIREMENTS = "gathering_requirements"
    CONFIRMING_INTEGRATIONS = "confirming_integrations"
    SETTING_PREFERENCES = "setting_preferences"
    REVIEWING_BLUEPRINT = "reviewing_blueprint"
    CONFIRMING_DEPLOYMENT = "confirming_deployment"
    COMPLETED = "completed"
    ERROR = "error"

class VoiceCommand(BaseModel):
    """Voice command structure."""
    text: str
    confidence: float
    timestamp: float
    intent: Optional[str] = None
    entities: List[Dict[str, Any]] = []

@dataclass
class ConversationContext:
    """Context for the voice conversation."""
    state: ConversationState
    user_input: str = ""
    requirements: List[str] = None
    integrations: List[str] = None
    preferences: Dict[str, Any] = None
    blueprint: Optional[AgentBlueprint] = None
    conversation_history: List[Dict[str, Any]] = None
    
    def __post_init__(self):
        if self.requirements is None:
            self.requirements = []
        if self.integrations is None:
            self.integrations = []
        if self.preferences is None:
            self.preferences = {}
        if self.conversation_history is None:
            self.conversation_history = []

class VoiceAgentBuilder:
    """Advanced Voice-Guided Agent Builder."""
    
    def __init__(self, 
                 openai_api_key: Optional[str] = None,
                 voice_enabled: bool = True,
                 text_fallback: bool = True):
        """Initialize the voice agent builder."""
        self.openai_api_key = openai_api_key
        self.voice_enabled = voice_enabled
        self.text_fallback = text_fallback
        
        # Initialize components
        self.nl_parser = NLToAgentParser(openai_api_key)
        
        # Voice components
        if voice_enabled:
            self.recognizer = sr.Recognizer()
            self.tts_engine = pyttsx3.init()
            self._configure_voice()
        
        # Conversation templates
        self.conversation_templates = self._load_conversation_templates()
        
        # Callbacks
        self.on_state_change: Optional[Callable] = None
        self.on_blueprint_created: Optional[Callable] = None
        self.on_error: Optional[Callable] = None

    def _configure_voice(self):
        """Configure voice recognition and synthesis."""
        try:
            # Configure speech recognition
            self.recognizer.energy_threshold = 4000
            self.recognizer.dynamic_energy_threshold = True
            self.recognizer.pause_threshold = 0.8
            
            # Configure text-to-speech
            voices = self.tts_engine.getProperty('voices')
            if voices:
                self.tts_engine.setProperty('voice', voices[0].id)
            self.tts_engine.setProperty('rate', 150)
            self.tts_engine.setProperty('volume', 0.9)
            
        except Exception as e:
            logger.warning(f"Voice configuration failed: {e}")
            self.voice_enabled = False

    def _load_conversation_templates(self) -> Dict[str, List[str]]:
        """Load conversation templates for different states."""
        return {
            ConversationState.INITIAL: [
                "Hello! I'm here to help you create an AI agent. What would you like your agent to do?",
                "Welcome to Daena's Agent Builder! Tell me what kind of assistant you need.",
                "I can help you build an AI agent. What's your vision for this assistant?"
            ],
            ConversationState.GATHERING_REQUIREMENTS: [
                "Great! Let me understand your needs better. What specific tasks should this agent handle?",
                "I see you want {type} functionality. Can you tell me more about the specific requirements?",
                "That sounds interesting! What are the main features you need in this agent?"
            ],
            ConversationState.CONFIRMING_INTEGRATIONS: [
                "I can connect your agent to {integrations}. Would you like me to set up these integrations?",
                "Based on your requirements, I suggest connecting to {integrations}. Should I proceed?",
                "Your agent will need access to {integrations}. Shall I configure these connections?"
            ],
            ConversationState.SETTING_PREFERENCES: [
                "Let me customize your agent. How would you like it to behave?",
                "I can personalize your agent. What's your preferred communication style?",
                "Let's set up your preferences. How should your agent interact with you?"
            ],
            ConversationState.REVIEWING_BLUEPRINT: [
                "Perfect! I've created your agent blueprint. Let me show you what I've designed:",
                "Here's what your AI agent will be able to do:",
                "I've designed your agent with these capabilities:"
            ],
            ConversationState.CONFIRMING_DEPLOYMENT: [
                "Your agent is ready! Should I deploy it now?",
                "Everything looks good! Ready to activate your new AI agent?",
                "Your agent blueprint is complete. Shall I create and deploy it?"
            ]
        }

    async def start_conversation(self) -> AgentBlueprint:
        """Start the voice-guided agent creation conversation."""
        context = ConversationContext(state=ConversationState.INITIAL)
        
        try:
            # Welcome message
            await self._speak(self._get_random_template(ConversationState.INITIAL))
            
            # Main conversation loop
            while context.state != ConversationState.COMPLETED:
                context = await self._handle_conversation_state(context)
                
                if self.on_state_change:
                    self.on_state_change(context.state, context)
            
            return context.blueprint
            
        except Exception as e:
            logger.error(f"Conversation error: {e}")
            context.state = ConversationState.ERROR
            await self._speak("I encountered an error. Let me start over.")
            
            if self.on_error:
                self.on_error(e, context)
            
            raise

    async def _handle_conversation_state(self, context: ConversationContext) -> ConversationContext:
        """Handle the current conversation state."""
        if context.state == ConversationState.INITIAL:
            return await self._handle_initial_state(context)
        elif context.state == ConversationState.GATHERING_REQUIREMENTS:
            return await self._handle_gathering_requirements(context)
        elif context.state == ConversationState.CONFIRMING_INTEGRATIONS:
            return await self._handle_confirming_integrations(context)
        elif context.state == ConversationState.SETTING_PREFERENCES:
            return await self._handle_setting_preferences(context)
        elif context.state == ConversationState.REVIEWING_BLUEPRINT:
            return await self._handle_reviewing_blueprint(context)
        elif context.state == ConversationState.CONFIRMING_DEPLOYMENT:
            return await self._handle_confirming_deployment(context)
        else:
            return context

    async def _handle_initial_state(self, context: ConversationContext) -> ConversationContext:
        """Handle the initial state - getting user's basic request."""
        user_input = await self._listen_for_input("Tell me what you need:")
        
        if not user_input:
            await self._speak("I didn't catch that. Could you please repeat?")
            return context
        
        context.user_input = user_input
        context.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # Parse the initial request
        parsed_intent = self.nl_parser.parse_user_request(user_input)
        
        # Move to gathering requirements
        context.state = ConversationState.GATHERING_REQUIREMENTS
        
        # Generate follow-up question
        template = self._get_random_template(ConversationState.GATHERING_REQUIREMENTS)
        question = template.format(type=parsed_intent.primary_intent.value.replace('_', ' '))
        await self._speak(question)
        
        return context

    async def _handle_gathering_requirements(self, context: ConversationContext) -> ConversationContext:
        """Handle gathering detailed requirements."""
        user_input = await self._listen_for_input("What specific features do you need?")
        
        if not user_input:
            await self._speak("Could you please provide more details?")
            return context
        
        # Add to requirements
        context.requirements.append(user_input)
        context.conversation_history.append({
            "role": "user",
            "content": user_input,
            "timestamp": asyncio.get_event_loop().time()
        })
        
        # Ask for more requirements or move to next state
        if len(context.requirements) < 3:
            await self._speak("What else should your agent be able to do?")
            return context
        else:
            # Move to confirming integrations
            context.state = ConversationState.CONFIRMING_INTEGRATIONS
            
            # Detect integrations from requirements
            all_requirements = " ".join(context.requirements)
            integrations = self.nl_parser._detect_integrations(all_requirements)
            context.integrations = integrations
            
            if integrations:
                template = self._get_random_template(ConversationState.CONFIRMING_INTEGRATIONS)
                question = template.format(integrations=", ".join(integrations))
                await self._speak(question)
            else:
                await self._speak("Your agent doesn't need external integrations. Let's set up preferences.")
                context.state = ConversationState.SETTING_PREFERENCES
            
            return context

    async def _handle_confirming_integrations(self, context: ConversationContext) -> ConversationContext:
        """Handle confirming integrations."""
        user_input = await self._listen_for_input("Should I set up these integrations?")
        
        if not user_input:
            await self._speak("Please confirm if you want these integrations.")
            return context
        
        # Parse user response
        if any(word in user_input.lower() for word in ["yes", "sure", "okay", "proceed", "go ahead"]):
            await self._speak("Great! I'll configure those integrations.")
            context.state = ConversationState.SETTING_PREFERENCES
        elif any(word in user_input.lower() for word in ["no", "not", "remove", "skip"]):
            # Ask which integrations to remove
            await self._speak("Which integrations would you like to remove?")
            user_input = await self._listen_for_input("Tell me which ones to remove:")
            
            if user_input:
                # Simple removal logic
                words_to_remove = user_input.lower().split()
                context.integrations = [i for i in context.integrations 
                                      if not any(word in i.lower() for word in words_to_remove)]
            
            context.state = ConversationState.SETTING_PREFERENCES
        
        await self._speak("Now let's set up your preferences.")
        return context

    async def _handle_setting_preferences(self, context: ConversationContext) -> ConversationContext:
        """Handle setting user preferences."""
        await self._speak("How would you like your agent to communicate with you?")
        user_input = await self._listen_for_input("Describe your preferred style:")
        
        if user_input:
            context.preferences["communication_style"] = user_input
            context.conversation_history.append({
                "role": "user",
                "content": user_input,
                "timestamp": asyncio.get_event_loop().time()
            })
        
        await self._speak("What's your preferred security level? Basic, enhanced, or enterprise?")
        user_input = await self._listen_for_input("Choose security level:")
        
        if user_input:
            context.preferences["security_level"] = user_input.lower()
        
        # Generate the blueprint
        context.state = ConversationState.REVIEWING_BLUEPRINT
        context.blueprint = await self._generate_blueprint(context)
        
        return context

    async def _handle_reviewing_blueprint(self, context: ConversationContext) -> ConversationContext:
        """Handle reviewing the generated blueprint."""
        if not context.blueprint:
            await self._speak("I couldn't generate a blueprint. Let me try again.")
            context.state = ConversationState.INITIAL
            return context
        
        # Present the blueprint
        template = self._get_random_template(ConversationState.REVIEWING_BLUEPRINT)
        await self._speak(template)
        
        # Describe the agent
        description = f"Your agent '{context.blueprint.name}' will be a {context.blueprint.type.value.replace('_', ' ')} "
        description += f"with {len(context.blueprint.capabilities)} capabilities including {', '.join(context.blueprint.capabilities[:3])}."
        
        if context.blueprint.tasks:
            description += f" It will handle {len(context.blueprint.tasks)} main tasks."
        
        await self._speak(description)
        
        # Ask for confirmation
        await self._speak("Does this sound right to you?")
        user_input = await self._listen_for_input("Confirm the blueprint:")
        
        if user_input and any(word in user_input.lower() for word in ["yes", "sure", "good", "perfect", "right"]):
            context.state = ConversationState.CONFIRMING_DEPLOYMENT
        else:
            await self._speak("Let me adjust the blueprint. What would you like to change?")
            user_input = await self._listen_for_input("What should I modify?")
            
            if user_input:
                # Simple modification logic
                context.blueprint = await self._modify_blueprint(context.blueprint, user_input)
            
            context.state = ConversationState.REVIEWING_BLUEPRINT
        
        return context

    async def _handle_confirming_deployment(self, context: ConversationContext) -> ConversationContext:
        """Handle confirming deployment."""
        template = self._get_random_template(ConversationState.CONFIRMING_DEPLOYMENT)
        await self._speak(template)
        
        user_input = await self._listen_for_input("Deploy the agent?")
        
        if user_input and any(word in user_input.lower() for word in ["yes", "deploy", "create", "activate"]):
            await self._speak("Perfect! I'm creating your AI agent now.")
            context.state = ConversationState.COMPLETED
            
            if self.on_blueprint_created:
                self.on_blueprint_created(context.blueprint)
        else:
            await self._speak("I'll save the blueprint for later. You can deploy it anytime.")
            context.state = ConversationState.COMPLETED
        
        return context

    async def _generate_blueprint(self, context: ConversationContext) -> AgentBlueprint:
        """Generate the agent blueprint from conversation context."""
        try:
            # Combine all user inputs
            full_input = f"{context.user_input} {' '.join(context.requirements)}"
            
            # Generate blueprint using NL parser
            blueprint = self.nl_parser.create_agent_from_text(full_input)
            
            # Apply preferences
            if context.preferences.get("communication_style"):
                blueprint.communication_style = {
                    "style": context.preferences["communication_style"],
                    "tone": "friendly",
                    "formality": "casual"
                }
            
            if context.preferences.get("security_level"):
                security_level = context.preferences["security_level"]
                if "enhanced" in security_level:
                    blueprint.security.level = "enhanced"
                elif "enterprise" in security_level:
                    blueprint.security.level = "enterprise"
            
            # Add conversation metadata
            blueprint.metadata["conversation_history"] = context.conversation_history
            blueprint.metadata["voice_created"] = True
            
            return blueprint
            
        except Exception as e:
            logger.error(f"Error generating blueprint: {e}")
            await self._speak("I encountered an error while creating your agent. Let me try a different approach.")
            return None

    async def _modify_blueprint(self, blueprint: AgentBlueprint, modification_request: str) -> AgentBlueprint:
        """Modify the blueprint based on user feedback."""
        try:
            # Simple modification logic
            modification_request = modification_request.lower()
            
            if "name" in modification_request or "call" in modification_request:
                # Extract new name
                words = modification_request.split()
                for i, word in enumerate(words):
                    if word in ["name", "call"] and i + 1 < len(words):
                        new_name = words[i + 1].title()
                        blueprint.name = new_name
                        break
            
            elif "add" in modification_request or "include" in modification_request:
                # Add new capability
                if "email" in modification_request:
                    blueprint.capabilities.append("email_processing")
                if "calendar" in modification_request:
                    blueprint.capabilities.append("calendar_management")
                if "chat" in modification_request:
                    blueprint.capabilities.append("chat_support")
            
            elif "remove" in modification_request or "delete" in modification_request:
                # Remove capability
                if "email" in modification_request:
                    blueprint.capabilities = [c for c in blueprint.capabilities if "email" not in c]
                if "calendar" in modification_request:
                    blueprint.capabilities = [c for c in blueprint.capabilities if "calendar" not in c]
            
            return blueprint
            
        except Exception as e:
            logger.error(f"Error modifying blueprint: {e}")
            return blueprint

    async def _listen_for_input(self, prompt: str = "") -> str:
        """Listen for voice input and convert to text."""
        if not self.voice_enabled:
            if self.text_fallback:
                return input(prompt + " ")
            return ""
        
        try:
            await self._speak(prompt)
            
            with sr.Microphone() as source:
                self.recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = self.recognizer.listen(source, timeout=10, phrase_time_limit=15)
            
            text = self.recognizer.recognize_google(audio)
            logger.info(f"Recognized: {text}")
            return text
            
        except sr.WaitTimeoutError:
            await self._speak("I didn't hear anything. Please try again.")
            return ""
        except sr.UnknownValueError:
            await self._speak("I couldn't understand that. Could you please repeat?")
            return ""
        except sr.RequestError as e:
            logger.error(f"Speech recognition error: {e}")
            await self._speak("I'm having trouble with speech recognition. Please try again.")
            return ""
        except Exception as e:
            logger.error(f"Voice input error: {e}")
            return ""

    async def _speak(self, text: str):
        """Convert text to speech."""
        if not self.voice_enabled:
            print(f"Daena: {text}")
            return
        
        try:
            self.tts_engine.say(text)
            self.tts_engine.runAndWait()
        except Exception as e:
            logger.error(f"Text-to-speech error: {e}")
            print(f"Daena: {text}")

    def _get_random_template(self, state: ConversationState) -> str:
        """Get a random template for the given state."""
        import random
        templates = self.conversation_templates.get(state, ["Please continue."])
        return random.choice(templates)

    def create_agent_from_voice(self, voice_file_path: Optional[str] = None) -> AgentBlueprint:
        """Create an agent from a voice file or live recording."""
        try:
            if voice_file_path:
                # Process voice file
                with sr.AudioFile(voice_file_path) as source:
                    audio = self.recognizer.record(source)
                    text = self.recognizer.recognize_google(audio)
            else:
                # Start live conversation
                return asyncio.run(self.start_conversation())
            
            # Use NL parser to create blueprint
            return self.nl_parser.create_agent_from_text(text)
            
        except Exception as e:
            logger.error(f"Error creating agent from voice: {e}")
            raise

    def set_callbacks(self, 
                     on_state_change: Optional[Callable] = None,
                     on_blueprint_created: Optional[Callable] = None,
                     on_error: Optional[Callable] = None):
        """Set callback functions for the voice builder."""
        self.on_state_change = on_state_change
        self.on_blueprint_created = on_blueprint_created
        self.on_error = on_error 