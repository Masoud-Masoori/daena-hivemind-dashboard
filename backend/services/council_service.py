import os
import json
from datetime import datetime
from typing import List, Dict, Any
from backend.models.council import AdvisorModel, ScoutModel, SynthesizerModel, DebateRecordModel, SynthesisRecordModel, CouncilStateModel
from backend.models.database import get_session, CouncilConclusion, CouncilDebate, DebateArgument, CouncilMember, Department
#from backend.services.llm_service import llm_service  # Use ModelIntegration for now

# Real LLM integration
import openai
import os
from typing import Optional

class RealLLM:
    def __init__(self):
        self.openai_client = openai.AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY", "your-openai-key")
        )
    
    async def generate(self, prompt: str, persona: Optional[str] = None, model: str = "gpt-4") -> str:
        """Generate response using OpenAI API"""
        try:
            # Enhance prompt with persona context
            enhanced_prompt = self._build_persona_prompt(prompt, persona)
            
            response = await self.openai_client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": enhanced_prompt},
                    {"role": "user", "content": prompt}
                ],
                max_tokens=500,
                temperature=0.7
            )
            
            return response.choices[0].message.content
        except Exception as e:
            # Fallback to mock response if API fails
            return f"[{persona or 'Agent'}] {prompt} (simulated response - API error: {str(e)})"
    
    def _build_persona_prompt(self, prompt: str, persona: Optional[str] = None) -> str:
        """Build system prompt with persona context"""
        base_prompt = "You are an expert business advisor in the Daena AI Council system."
        
        if persona:
            persona_prompts = {
                "Visionary": "You think like Steve Jobs - focus on innovation, user experience, and bold vision. Be concise and inspiring.",
                "Empathetic Leader": "You think like Satya Nadella - focus on empathy, collaboration, and sustainable growth. Be thoughtful and inclusive.",
                "Operational Excellence": "You think like Sheryl Sandberg - focus on execution, process improvement, and measurable results. Be practical and data-driven.",
                "Bold Innovator": "You think like Elon Musk - focus on breakthrough technology, rapid iteration, and ambitious goals. Be bold and forward-thinking.",
                "Strategic Thinker": "You think like Indra Nooyi - focus on long-term strategy, stakeholder value, and sustainable business models. Be strategic and balanced.",
                "Technical Architect": "You think like Linus Torvalds - focus on system design, code quality, and technical excellence. Be precise and logical.",
                "Product Visionary": "You think like Jeff Bezos - focus on customer obsession, long-term thinking, and operational excellence. Be customer-centric.",
                "Marketing Genius": "You think like Seth Godin - focus on storytelling, brand building, and customer psychology. Be creative and persuasive.",
                "Financial Strategist": "You think like Warren Buffett - focus on value creation, risk management, and sustainable growth. Be analytical and prudent.",
                "HR Innovator": "You think like Patty McCord - focus on culture, talent development, and organizational effectiveness. Be people-focused.",
                "Sales Master": "You think like Grant Cardone - focus on relationship building, value proposition, and closing strategies. Be results-driven.",
                "Legal Expert": "You think like Ruth Bader Ginsburg - focus on justice, precedent, and legal strategy. Be principled and thorough.",
                "Security Specialist": "You think like Kevin Mitnick - focus on threat assessment, risk mitigation, and security architecture. Be vigilant and thorough.",
                "Operations Leader": "You think like Jack Welch - focus on efficiency, quality, and continuous improvement. Be systematic and results-oriented."
            }
            base_prompt += f" {persona_prompts.get(persona, 'Provide expert business advice.')}"
        
        base_prompt += " Respond in a clear, professional manner suitable for executive decision-making."
        return base_prompt

# Use real LLM if API key is available, otherwise fallback to mock
if os.getenv("OPENAI_API_KEY"):
    llm = RealLLM()
else:
    # Fallback mock LLM
    class MockLLM:
        async def generate(self, prompt, persona=None):
            return f"[{persona or 'Agent'}] {prompt} (simulated response)"
    llm = MockLLM()

# Department-specific councilor configurations
DEPARTMENT_COUNCILORS = {
    "engineering": {
        "advisors": [
            {"name": "Linus Torvalds", "persona": "Technical Architect", "expertise": "System Architecture/Open Source"},
            {"name": "Grace Hopper", "persona": "Strategic Thinker", "expertise": "Computer Science/Innovation"},
            {"name": "Alan Kay", "persona": "Visionary", "expertise": "Software Design/UI/UX"},
            {"name": "Margaret Hamilton", "persona": "Operational Excellence", "expertise": "Software Engineering/Reliability"},
            {"name": "Dennis Ritchie", "persona": "Technical Architect", "expertise": "Programming Languages/Systems"}
        ],
        "scouts": [
            {"name": "Tech Scout Alpha", "focus_area": "Emerging Technologies", "sources": ["arxiv.org", "github.com", "techcrunch.com"]},
            {"name": "Architecture Scout Beta", "focus_area": "System Design Patterns", "sources": ["martinfowler.com", "aws.amazon.com", "microsoft.com"]}
        ]
    },
    "product": {
        "advisors": [
            {"name": "Steve Jobs", "persona": "Product Visionary", "expertise": "Product Design/User Experience"},
            {"name": "Jeff Bezos", "persona": "Strategic Thinker", "expertise": "Customer Obsession/Scale"},
            {"name": "Elon Musk", "persona": "Bold Innovator", "expertise": "Product Innovation/Execution"},
            {"name": "Reid Hoffman", "persona": "Empathetic Leader", "expertise": "Product Strategy/Growth"},
            {"name": "Marissa Mayer", "persona": "Operational Excellence", "expertise": "Product Management/Data"}
        ],
        "scouts": [
            {"name": "Product Scout Alpha", "focus_area": "User Research", "sources": ["nielsen.com", "uxmatters.com", "smashingmagazine.com"]},
            {"name": "Market Scout Beta", "focus_area": "Competitive Analysis", "sources": ["producthunt.com", "techcrunch.com", "venturebeat.com"]}
        ]
    },
    "marketing": {
        "advisors": [
            {"name": "Seth Godin", "persona": "Marketing Genius", "expertise": "Brand Building/Storytelling"},
            {"name": "Gary Vaynerchuk", "persona": "Bold Innovator", "expertise": "Social Media/Digital Marketing"},
            {"name": "Simon Sinek", "persona": "Empathetic Leader", "expertise": "Brand Strategy/Leadership"},
            {"name": "Ann Handley", "persona": "Operational Excellence", "expertise": "Content Marketing/Execution"},
            {"name": "David Ogilvy", "persona": "Strategic Thinker", "expertise": "Advertising/Creative Strategy"}
        ],
        "scouts": [
            {"name": "Trend Scout Alpha", "focus_area": "Marketing Trends", "sources": ["marketingweek.com", "adage.com", "hubspot.com"]},
            {"name": "Social Scout Beta", "focus_area": "Social Media Insights", "sources": ["socialmediaexaminer.com", "buffer.com", "hootsuite.com"]}
        ]
    },
    "sales": {
        "advisors": [
            {"name": "Grant Cardone", "persona": "Sales Master", "expertise": "Sales Strategy/Closing"},
            {"name": "Zig Ziglar", "persona": "Empathetic Leader", "expertise": "Motivation/Relationship Building"},
            {"name": "Brian Tracy", "persona": "Operational Excellence", "expertise": "Sales Process/Performance"},
            {"name": "Jill Konrath", "persona": "Strategic Thinker", "expertise": "B2B Sales/Value Selling"},
            {"name": "Tom Hopkins", "persona": "Sales Master", "expertise": "Sales Training/Techniques"}
        ],
        "scouts": [
            {"name": "Sales Scout Alpha", "focus_area": "Sales Trends", "sources": ["salesforce.com", "hubspot.com", "linkedin.com"]},
            {"name": "Market Scout Beta", "focus_area": "Lead Generation", "sources": ["crunchbase.com", "zoominfo.com", "apollo.io"]}
        ]
    },
    "finance": {
        "advisors": [
            {"name": "Warren Buffett", "persona": "Financial Strategist", "expertise": "Investment Strategy/Value Creation"},
            {"name": "Ray Dalio", "persona": "Strategic Thinker", "expertise": "Risk Management/Portfolio Theory"},
            {"name": "Jamie Dimon", "persona": "Operational Excellence", "expertise": "Banking/Financial Operations"},
            {"name": "Cathie Wood", "persona": "Bold Innovator", "expertise": "Innovation Investing/Disruption"},
            {"name": "Charlie Munger", "persona": "Strategic Thinker", "expertise": "Decision Making/Mental Models"}
        ],
        "scouts": [
            {"name": "Market Scout Alpha", "focus_area": "Financial Markets", "sources": ["bloomberg.com", "reuters.com", "wsj.com"]},
            {"name": "Tech Scout Beta", "focus_area": "Fintech Trends", "sources": ["finextra.com", "pymnts.com", "bankingtech.com"]}
        ]
    },
    "hr": {
        "advisors": [
            {"name": "Patty McCord", "persona": "HR Innovator", "expertise": "Culture/Talent Management"},
            {"name": "Laszlo Bock", "persona": "Strategic Thinker", "expertise": "People Operations/Data"},
            {"name": "Sheryl Sandberg", "persona": "Operational Excellence", "expertise": "Leadership/Organizational Development"},
            {"name": "Adam Grant", "persona": "Empathetic Leader", "expertise": "Organizational Psychology/Motivation"},
            {"name": "Kim Scott", "persona": "Empathetic Leader", "expertise": "Feedback/Radical Candor"}
        ],
        "scouts": [
            {"name": "Talent Scout Alpha", "focus_area": "Talent Trends", "sources": ["linkedin.com", "glassdoor.com", "indeed.com"]},
            {"name": "Culture Scout Beta", "focus_area": "Workplace Culture", "sources": ["cultureamp.com", "greatplacetowork.com", "fortune.com"]}
        ]
    },
    "operations": {
        "advisors": [
            {"name": "Jack Welch", "persona": "Operations Leader", "expertise": "Operational Excellence/Leadership"},
            {"name": "W. Edwards Deming", "persona": "Strategic Thinker", "expertise": "Quality Management/Process Improvement"},
            {"name": "Taiichi Ohno", "persona": "Operational Excellence", "expertise": "Lean Manufacturing/Just-in-Time"},
            {"name": "Eliyahu Goldratt", "persona": "Strategic Thinker", "expertise": "Theory of Constraints/Process Optimization"},
            {"name": "Shigeo Shingo", "persona": "Operational Excellence", "expertise": "Continuous Improvement/Kaizen"}
        ],
        "scouts": [
            {"name": "Process Scout Alpha", "focus_area": "Process Optimization", "sources": ["asq.org", "lean.org", "sixsigma.com"]},
            {"name": "Tech Scout Beta", "focus_area": "Operational Technology", "sources": ["gartner.com", "forrester.com", "idc.com"]}
        ]
    },
    "legal": {
        "advisors": [
            {"name": "Ruth Bader Ginsburg", "persona": "Legal Expert", "expertise": "Constitutional Law/Justice"},
            {"name": "Clarence Darrow", "persona": "Strategic Thinker", "expertise": "Criminal Law/Advocacy"},
            {"name": "Thurgood Marshall", "persona": "Empathetic Leader", "expertise": "Civil Rights/Constitutional Law"},
            {"name": "Oliver Wendell Holmes Jr.", "persona": "Legal Expert", "expertise": "Common Law/Judicial Philosophy"},
            {"name": "Sandra Day O'Connor", "persona": "Strategic Thinker", "expertise": "Judicial Process/Consensus Building"}
        ],
        "scouts": [
            {"name": "Legal Scout Alpha", "focus_area": "Legal Trends", "sources": ["law.com", "abajournal.com", "reuters.com"]},
            {"name": "Regulatory Scout Beta", "focus_area": "Regulatory Changes", "sources": ["federalregister.gov", "regulations.gov", "congress.gov"]}
        ]
    }
}

class CouncilService:
    def __init__(self):
        pass

    def get_department_councilors(self, department: str) -> Dict[str, Any]:
        """Get department-specific councilors with expert AI agents"""
        councilors = DEPARTMENT_COUNCILORS.get(department, DEPARTMENT_COUNCILORS["engineering"])
        
        # Convert to proper format for API response
        advisors = []
        for advisor in councilors["advisors"]:
            advisors.append({
                "name": advisor["name"],
                "persona": advisor["persona"],
                "expertise": advisor["expertise"],
                "description": f"AI Agent trained on {advisor['name']}'s thinking patterns, expertise, and decision-making style",
                "avatar": f"https://api.dicebear.com/7.x/avataaars/svg?seed={advisor['name']}",
                "status": "active",
                "specialization": advisor["expertise"]
            })
        
        scouts = []
        for scout in councilors["scouts"]:
            scouts.append({
                "name": scout["name"],
                "focus_area": scout["focus_area"],
                "sources": scout["sources"],
                "description": f"AI Scout specialized in {scout['focus_area']} for {department} department",
                "status": "active"
            })
        
        return {
            "advisors": advisors,
            "scouts": scouts,
            "department": department,
            "department_display_name": self.get_department_display_name(department)
        }
    
    def get_department_display_name(self, department: str) -> str:
        """Get human-readable department name"""
        names = {
            "engineering": "Engineering & Technology",
            "product": "Product & Design",
            "marketing": "Marketing & Branding",
            "sales": "Sales & Business Development",
            "finance": "Finance & Investment",
            "hr": "Human Resources & Culture",
            "operations": "Operations & Process",
            "legal": "Legal & Compliance"
        }
        return names.get(department, department.title())

    async def run_debate(self, department: str, topic: str, advisors: List[AdvisorModel]) -> DebateRecordModel:
        arguments = {}
        for advisor in advisors:
            prompt = f"As {advisor.name} ({advisor.persona}), debate the topic: {topic}"
            arguments[advisor.name] = await llm.generate(prompt, persona=advisor.persona)
        debate_id = f"debate-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        return DebateRecordModel(
            debate_id=debate_id,
            topic=topic,
            arguments=arguments,
            timestamp=datetime.now().isoformat(),
            result=None
        )

    async def run_scouts(self, department: str, scouts: List[ScoutModel]) -> List[Dict[str, Any]]:
        findings = []
        for scout in scouts:
            findings.append({
                "scout": scout.name,
                "focus_area": scout.focus_area,
                "finding": f"Latest findings for {scout.focus_area} (simulated)"
            })
        return findings

    async def run_synthesis(self, department: str, debate: DebateRecordModel, scouts: List[Dict[str, Any]], synthesizer: SynthesizerModel) -> SynthesisRecordModel:
        """Run synthesis using enhanced LLM routing with Claude preference"""
        try:
            # Build synthesis prompt
            synthesis_prompt = self._build_synthesis_prompt(debate, scouts)
            
            # Get synthesis from LLM with Claude preference
            from backend.services.llm_service import llm_service, LLMProvider
            
            # Use synthesizer-specific provider (prefer Claude)
            synthesizer_provider = llm_service.get_synthesizer_provider()
            if synthesizer_provider:
                synthesis_response = await llm_service.generate_response(
                    synthesis_prompt,
                    provider=synthesizer_provider,
                    task_type="synthesis"
                )
            else:
                # Fallback to load-based selection
                load_provider = llm_service.get_load_based_provider("synthesis")
                synthesis_response = await llm_service.generate_response(
                    synthesis_prompt,
                    provider=load_provider
                )
            
            # Parse synthesis response
            synthesis_data = self._parse_synthesis_response(synthesis_response, debate)
            
            return SynthesisRecordModel(
                synthesis_id=f"synth-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                debate_id=debate.debate_id,
                summary=synthesis_data["summary"],
                confidence_scores=synthesis_data["confidence_scores"],
                followup_questions=synthesis_data["followup_questions"],
                participants=list(debate.arguments.keys()),
                timestamp=datetime.now().isoformat(),
                outcome=synthesis_data["outcome"]
            )
            
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            # Return fallback synthesis
            summary = f"Synthesized summary for topic '{debate.topic}' based on advisor arguments and scout findings."
            confidence_scores = {name: 0.9 for name in debate.arguments.keys()}
            followup_questions = [
                f"What is the main risk in '{debate.topic}'?",
                f"What would be the impact of a different approach?",
                f"How can we measure success for '{debate.topic}'?"
            ]
            return SynthesisRecordModel(
                synthesis_id=f"synth-{datetime.now().strftime('%Y%m%d%H%M%S')}",
                debate_id=debate.debate_id,
                summary=summary,
                confidence_scores=confidence_scores,
                followup_questions=followup_questions,
                participants=list(debate.arguments.keys()),
                timestamp=datetime.now().isoformat(),
                outcome=None
            )
    
    def _build_synthesis_prompt(self, debate: DebateRecordModel, scouts: List[Dict[str, Any]]) -> str:
        """Build comprehensive synthesis prompt"""
        prompt = f"""
        As an AI Synthesizer, analyze the following debate and provide strategic insights:
        
        TOPIC: {debate.topic}
        
        ADVISOR ARGUMENTS:
        """
        
        for advisor_name, argument in debate.arguments.items():
            prompt += f"\n{advisor_name}: {argument}\n"
        
        prompt += "\nSCOUT FINDINGS:\n"
        for scout in scouts:
            prompt += f"- {scout['finding']}\n"
        
        prompt += """
        
        Please provide:
        1. A comprehensive summary of the key points
        2. Strategic recommendations with confidence scores
        3. 3 critical follow-up questions
        4. Final outcome decision
        
        Format your response as structured analysis suitable for executive decision-making.
        """
        
        return prompt
    
    def _parse_synthesis_response(self, response: str, debate: DebateRecordModel) -> Dict[str, Any]:
        """Parse LLM synthesis response"""
        try:
            # Simple parsing - in production, use more sophisticated parsing
            lines = response.split('\n')
            summary = ""
            confidence_scores = {name: 0.8 for name in debate.arguments.keys()}
            followup_questions = []
            outcome = "Proceed with recommended approach"
            
            for line in lines:
                if "summary" in line.lower() or "key points" in line.lower():
                    summary = line.split(":", 1)[1].strip() if ":" in line else line.strip()
                elif "question" in line.lower() and len(followup_questions) < 3:
                    question = line.split(":", 1)[1].strip() if ":" in line else line.strip()
                    if question and not question.startswith("Please"):
                        followup_questions.append(question)
            
            if not summary:
                summary = f"Strategic analysis of '{debate.topic}' based on expert advisor input."
            
            if not followup_questions:
                followup_questions = [
                    f"What are the main risks in {debate.topic}?",
                    f"What would be the impact of alternative approaches?",
                    f"How can we measure success for {debate.topic}?"
                ]
            
            return {
                "summary": summary,
                "confidence_scores": confidence_scores,
                "followup_questions": followup_questions,
                "outcome": outcome
            }
            
        except Exception as e:
            logger.error(f"Error parsing synthesis response: {e}")
            return {
                "summary": f"Analysis of {debate.topic}",
                "confidence_scores": {name: 0.7 for name in debate.arguments.keys()},
                "followup_questions": ["What are the key concerns?", "What are the next steps?"],
                "outcome": "Further analysis required"
            }

    def save_outcome(self, department: str, synthesis: SynthesisRecordModel):
        # Save to .json
        dir_path = os.path.join("knowledge", department)
        os.makedirs(dir_path, exist_ok=True)
        file_path = os.path.join(dir_path, f"council_synthesis_{synthesis.synthesis_id}.json")
        with open(file_path, "w") as f:
            json.dump(synthesis.dict(), f, indent=2)
        # TODO: Save to DB (CouncilConclusion, KnowledgeBase)
        # session = get_session()
        # ...
        return file_path

council_service = CouncilService() 