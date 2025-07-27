"""
LLM Service for Daena AI System
Handles integration with multiple AI providers (OpenAI, Gemini, Anthropic, etc.)
"""

import asyncio
import json
import logging
import os
from typing import Dict, List, Optional, Any, Union
from enum import Enum

try:
    import openai
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False

try:
    import google.generativeai as genai
    GEMINI_AVAILABLE = True
except ImportError:
    GEMINI_AVAILABLE = False

try:
    import anthropic
    ANTHROPIC_AVAILABLE = True
except ImportError:
    ANTHROPIC_AVAILABLE = False

from backend.config.settings import settings

logger = logging.getLogger(__name__)

class LLMProvider(str, Enum):
    OPENAI = "openai"
    GEMINI = "gemini"
    ANTHROPIC = "anthropic"
    DEEPSEEK = "deepseek"
    GROK = "grok"

class LLMService:
    def __init__(self):
        self.providers = {}
        self.setup_providers()
    
    def setup_providers(self):
        """Initialize available LLM providers"""
        
        # OpenAI Setup
        self.openai_key = (getattr(settings, 'openai_api_key', None) or 
                          getattr(settings, 'OPENAI_API_KEY', None) or
                          os.getenv('OPENAI_API_KEY'))
        
        # Validate OpenAI key format and not placeholder
        if (OPENAI_AVAILABLE and self.openai_key and 
            len(self.openai_key) > 20 and 
            not self.openai_key.startswith("your_") and
            not self.openai_key.endswith("_here")):
            try:
                # New OpenAI v1.0+ format - no need to set api_key globally
                self.providers[LLMProvider.OPENAI] = True
                logger.info("✅ OpenAI provider configured")
            except Exception as e:
                logger.error(f"❌ OpenAI setup failed: {e}")
        else:
            logger.warning("⚠️ OpenAI API key not configured or invalid")
        
        # Gemini Setup
        if (GEMINI_AVAILABLE and settings.gemini_api_key and 
            len(settings.gemini_api_key) > 10 and 
            not settings.gemini_api_key.startswith("your_") and
            not settings.gemini_api_key.endswith("_here")):
            try:
                genai.configure(api_key=settings.gemini_api_key)
                self.providers[LLMProvider.GEMINI] = True
                logger.info("✅ Gemini provider configured")
            except Exception as e:
                logger.error(f"❌ Gemini setup failed: {e}")
        else:
            logger.warning("⚠️ Gemini API key not configured or invalid")
        
        # Anthropic Setup  
        if (ANTHROPIC_AVAILABLE and settings.anthropic_api_key and 
            len(settings.anthropic_api_key) > 10 and 
            not settings.anthropic_api_key.startswith("your_") and
            not settings.anthropic_api_key.endswith("_here")):
            try:
                self.anthropic_client = anthropic.Anthropic(api_key=settings.anthropic_api_key)
                self.providers[LLMProvider.ANTHROPIC] = True
                logger.info("✅ Anthropic provider configured")
            except Exception as e:
                logger.error(f"❌ Anthropic setup failed: {e}")
        else:
            logger.warning("⚠️ Anthropic API key not configured or invalid")
        
        # Add a fallback mock provider if no real providers available
        if not self.providers:
            logger.warning("⚠️ No LLM providers configured. Using fallback response system.")
            self.providers["fallback"] = True
    
    async def generate_response(
        self, 
        prompt: str, 
        provider: Optional[LLMProvider] = None,
        model: Optional[str] = None,
        temperature: float = 0.7,
        max_tokens: int = 1000,
        context: Optional[Dict] = None
    ) -> str:
        """Generate response using specified or best available provider"""
        
        if not self.providers:
            return "I'm currently unable to connect to AI services. Please check the configuration."
        
        # Auto-select provider if not specified
        if not provider:
            provider = self.get_best_provider()
        
        try:
            if provider == LLMProvider.OPENAI and LLMProvider.OPENAI in self.providers:
                try:
                    return await self._openai_generate(prompt, model, temperature, max_tokens)
                except Exception as e:
                    logger.error(f"OpenAI failed, trying fallback: {e}")
                    return await self._fallback_generate(prompt)
            
            elif provider == LLMProvider.GEMINI and LLMProvider.GEMINI in self.providers:
                try:
                    return await self._gemini_generate(prompt, temperature, max_tokens)
                except Exception as e:
                    logger.error(f"Gemini failed, trying fallback: {e}")
                    return await self._fallback_generate(prompt)
            
            elif provider == LLMProvider.ANTHROPIC and LLMProvider.ANTHROPIC in self.providers:
                try:
                    return await self._anthropic_generate(prompt, model, temperature, max_tokens)
                except Exception as e:
                    logger.error(f"Anthropic failed, trying fallback: {e}")
                    return await self._fallback_generate(prompt)
            
            else:
                # Check if we have the fallback provider
                if "fallback" in self.providers:
                    return await self._fallback_generate(prompt)
                
                # Fallback to any available provider
                for available_provider in self.providers.keys():
                    if available_provider == "fallback":
                        continue
                    try:
                        return await self.generate_response(prompt, available_provider, model, temperature, max_tokens, context)
                    except Exception as e:
                        logger.error(f"Provider {available_provider} failed: {e}")
                        continue
                
                # Final fallback
                return await self._fallback_generate(prompt)
        
        except Exception as e:
            logger.error(f"LLM generation failed: {e}")
            return await self._fallback_generate(prompt)
    
    async def _openai_generate(self, prompt: str, model: Optional[str], temperature: float, max_tokens: int) -> str:
        """Generate response using OpenAI"""
        if not model:
            model = "gpt-4o-mini"
        
        try:
            from openai import AsyncOpenAI
            client = AsyncOpenAI(api_key=self.openai_key)
            
            response = await client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": "You are Daena, an AI Vice President for MAS-AI Company. You manage 8 departments with 25 active agents. You are professional, strategic, and helpful. Provide clear, executive-level responses."},
                    {"role": "user", "content": prompt}
                ],
                temperature=temperature,
                max_tokens=max_tokens
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            logger.error(f"OpenAI API error: {e}")
            raise
    
    async def _gemini_generate(self, prompt: str, temperature: float, max_tokens: int) -> str:
        """Generate response using Gemini"""
        try:
            model = genai.GenerativeModel('gemini-pro')
            
            generation_config = genai.types.GenerationConfig(
                temperature=temperature,
                max_output_tokens=max_tokens
            )
            
            response = await model.generate_content_async(
                prompt,
                generation_config=generation_config
            )
            return response.text.strip()
        except Exception as e:
            logger.error(f"Gemini API error: {e}")
            raise
    
    async def _anthropic_generate(self, prompt: str, model: Optional[str], temperature: float, max_tokens: int) -> str:
        """Generate response using Anthropic"""
        if not model:
            model = "claude-3-haiku-20240307"
        
        try:
            response = await self.anthropic_client.messages.create(
                model=model,
                max_tokens=max_tokens,
                temperature=temperature,
                messages=[{"role": "user", "content": prompt}]
            )
            return response.content[0].text.strip()
        except Exception as e:
            logger.error(f"Anthropic API error: {e}")
            raise
    
    async def _fallback_generate(self, prompt: str) -> str:
        """Fallback response when no AI providers are available"""
        responses = {
            "hello": "Hello! I'm Daena, your AI Vice President. I'm currently running in demonstration mode. To unlock full AI capabilities, please configure your API keys in the settings.",
            "status": "System Status: ✅ All core systems operational. Currently running in demonstration mode. 8 departments managed, 25 agents coordinated.",
            "help": "I'm here to help you manage your business operations. Available commands: status, dashboard, agents, departments, projects, meetings. Configure API keys for full AI capabilities.",
            "dashboard": "📊 Executive Dashboard: Revenue trending positive, all departments operational, 5 active projects on track. Configure AI providers for detailed analytics.",
            "agents": "🤖 Agent Status: 25 agents active across 8 departments. Engineering (5), Marketing (3), Sales (4), Operations (3), Finance (2), HR (2), Legal (2), Research (4).",
            "departments": "🏢 Departments: All 8 departments operational - Engineering, Marketing, Sales, Operations, Finance, HR, Legal, Research. Each department has specialized AI agents.",
            "projects": "📋 Active Projects: 5 projects in progress. 2 in development phase, 2 in testing, 1 ready for deployment. All on schedule.",
            "meetings": "📅 Strategic Meetings: Next meeting scheduled. Agenda: Q4 planning, resource allocation, performance review. All stakeholders notified."
        }
        
        # Simple keyword matching for demonstration
        prompt_lower = prompt.lower()
        for keyword, response in responses.items():
            if keyword in prompt_lower:
                return response
        
        # Default professional response
        return f"I'm Daena, your AI Vice President. I understand you're asking about: '{prompt[:50]}...'. I'm currently in demonstration mode. Please configure your API keys (OpenAI, Gemini, or Anthropic) in the settings to unlock my full AI capabilities for detailed business analysis and strategic guidance."
    
    def get_best_provider(self) -> LLMProvider:
        """Get the best available provider based on priority"""
        priority = [LLMProvider.OPENAI, LLMProvider.GEMINI, LLMProvider.ANTHROPIC]
        
        for provider in priority:
            if provider in self.providers:
                return provider
        
        # Return first available if none in priority list
        if self.providers:
            return list(self.providers.keys())[0]
        
        return LLMProvider.OPENAI  # Fallback
    
    def get_synthesizer_provider(self) -> LLMProvider:
        """Get the best provider for synthesizer tasks (prefer Claude)"""
        if LLMProvider.ANTHROPIC in self.providers:
            return LLMProvider.ANTHROPIC  # Prefer Claude for synthesis
        elif LLMProvider.OPENAI in self.providers:
            return LLMProvider.OPENAI
        elif LLMProvider.GEMINI in self.providers:
            return LLMProvider.GEMINI
        else:
            return None
    
    def get_load_based_provider(self, task_type: str = "general") -> LLMProvider:
        """Get provider based on current load and task type"""
        # Check current load (mock implementation)
        current_load = self._get_current_load()
        
        if task_type == "synthesis" and LLMProvider.ANTHROPIC in self.providers:
            return LLMProvider.ANTHROPIC  # Always prefer Claude for synthesis
        
        if current_load > 80:  # High load
            # Distribute to different providers
            if LLMProvider.GEMINI in self.providers:
                return LLMProvider.GEMINI
            elif LLMProvider.ANTHROPIC in self.providers:
                return LLMProvider.ANTHROPIC
            else:
                return LLMProvider.OPENAI
        else:
            # Normal load - use best available
            return self.get_best_provider()
    
    def _get_current_load(self) -> int:
        """Get current system load (mock implementation)"""
        # In a real implementation, this would check actual system metrics
        import random
        return random.randint(20, 90)  # Mock load between 20-90%
    
    def get_available_providers(self) -> List[str]:
        """Get list of available providers"""
        return [provider.value for provider in self.providers.keys()]
    
    def is_provider_available(self, provider: LLMProvider) -> bool:
        """Check if provider is available"""
        return provider in self.providers

# Global LLM service instance
llm_service = LLMService() 