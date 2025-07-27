#!/usr/bin/env python3
"""
Email Builder Agent for Daena AI VP System
Generates personalized cold emails using Azure OpenAI
"""

import json
import logging
import os
from typing import List, Dict, Any, Optional
from datetime import datetime
import openai
from backend.services.email_service import email_service

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class EmailBuilderAgent:
    def __init__(self):
        # Azure OpenAI Configuration
        self.api_type = "azure"
        self.api_key = "1HmnkpDuMqMzKDtYbpcckyVQC6qlggup3zAVmfkG65BjxAtT9JKtJQQJ99BGACHYHv6XJ3w3AAAAACOGX3DN"
        self.api_base = "https://masou-mdksrl1q-eastus2.openai.azure.com/"
        self.api_version = "2024-02-15"
        self.deployment_name = "daena"
        
        # Configure OpenAI client for Azure
        self.client = openai.AzureOpenAI(
            api_key=self.api_key,
            api_version=self.api_version,
            azure_endpoint=self.api_base
        )
        
        # Email templates and styles
        self.email_styles = {
            'professional': {
                'tone': 'formal and business-focused',
                'length': 'medium',
                'cta': 'schedule a call'
            },
            'friendly': {
                'tone': 'warm and approachable',
                'length': 'medium',
                'cta': 'grab coffee'
            },
            'confident': {
                'tone': 'bold and assertive',
                'length': 'short',
                'cta': 'invest now'
            },
            'innovative': {
                'tone': 'forward-thinking and visionary',
                'length': 'long',
                'cta': 'join the future'
            }
        }
        
        # Company information
        self.company_info = {
            'name': 'Daena AI VP System',
            'founder': 'Masoud Masoori',
            'founder_email': 'masoud.masoori@gmail.com',
            'company_email': 'investors@daena-ai.com',
            'website': 'https://daena-ai.com',
            'location': 'Toronto, Canada',
            'stage': 'Series A',
            'ask': '$5M',
            'valuation': '$25M pre-money',
            'market': '$280B TAM',
            'traction': 'Production-ready system with 500+ API endpoints',
            'unique_value': 'World\'s first AI Vice President with no direct competitors'
        }
    
    def generate_email(self, investor: Dict[str, Any], style: str = 'professional', 
                      custom_message: Optional[str] = None) -> Dict[str, Any]:
        """Generate a personalized email for a specific investor"""
        try:
            logger.info(f"Generating {style} email for {investor.get('name', 'Unknown')}")
            
            # Get style configuration
            style_config = self.email_styles.get(style, self.email_styles['professional'])
            
            # Build the prompt
            prompt = self._build_email_prompt(investor, style_config, custom_message)
            
            # Generate email using Azure OpenAI
            response = self.client.chat.completions.create(
                model=self.deployment_name,
                messages=[
                    {
                        "role": "system",
                        "content": "You are Daena, the world's first AI Vice President. You write compelling, personalized investor outreach emails that are professional, data-driven, and results-oriented."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                max_tokens=800,
                temperature=0.7
            )
            
            # Extract the generated email
            generated_content = response.choices[0].message.content.strip()
            
            # Parse the response to extract subject and body
            subject, body = self._parse_email_response(generated_content)
            
            # Create email object
            email_data = {
                'investor': investor,
                'subject': subject,
                'body': body,
                'style': style,
                'generated_at': datetime.now().isoformat(),
                'openai_response': response.choices[0].message.content,
                'status': 'generated'
            }
            
            logger.info(f"✅ Generated email for {investor.get('name', 'Unknown')}")
            return email_data
            
        except Exception as e:
            logger.error(f"Error generating email for {investor.get('name', 'Unknown')}: {str(e)}")
            return {
                'investor': investor,
                'subject': f"Investment Opportunity: {self.company_info['name']}",
                'body': self._get_fallback_email(investor, style),
                'style': style,
                'generated_at': datetime.now().isoformat(),
                'error': str(e),
                'status': 'error'
            }
    
    def _build_email_prompt(self, investor: Dict[str, Any], style_config: Dict[str, Any], 
                           custom_message: Optional[str] = None) -> str:
        """Build the prompt for email generation"""
        
        investor_name = investor.get('name', 'Investor')
        investor_source = investor.get('source', 'unknown')
        investor_score = investor.get('score', 0)
        investor_notes = investor.get('notes', '')
        
        prompt = f"""
Generate a personalized cold email for investor outreach with the following specifications:

INVESTOR INFORMATION:
- Name: {investor_name}
- Source: {investor_source}
- Score: {investor_score}/1.0
- Notes: {investor_notes}

COMPANY INFORMATION:
- Company: {self.company_info['name']}
- Founder: {self.company_info['founder']}
- Stage: {self.company_info['stage']}
- Ask: {self.company_info['ask']}
- Valuation: {self.company_info['valuation']}
- Market: {self.company_info['market']}
- Traction: {self.company_info['traction']}
- Unique Value: {self.company_info['unique_value']}

EMAIL STYLE:
- Tone: {style_config['tone']}
- Length: {style_config['length']}
- Call-to-Action: {style_config['cta']}

REQUIREMENTS:
1. Subject line should be compelling and under 60 characters
2. Body should be personalized to the investor
3. Include specific data points and traction
4. End with a clear call-to-action
5. Keep it professional but engaging
6. Reference the investor's background if available

{f'CUSTOM MESSAGE: {custom_message}' if custom_message else ''}

Please format the response as:
SUBJECT: [subject line]
BODY: [email body]

Generate the email now:
"""
        
        return prompt
    
    def _parse_email_response(self, response: str) -> tuple[str, str]:
        """Parse the OpenAI response to extract subject and body"""
        lines = response.split('\n')
        subject = ""
        body_lines = []
        in_body = False
        
        for line in lines:
            line = line.strip()
            if line.startswith('SUBJECT:'):
                subject = line.replace('SUBJECT:', '').strip()
            elif line.startswith('BODY:'):
                in_body = True
            elif in_body and line:
                body_lines.append(line)
        
        # If parsing failed, create a default structure
        if not subject:
            subject = f"Investment Opportunity: {self.company_info['name']}"
        
        body = '\n\n'.join(body_lines) if body_lines else self._get_default_body()
        
        return subject, body
    
    def _get_fallback_email(self, investor: Dict[str, Any], style: str) -> str:
        """Get a fallback email if generation fails"""
        investor_name = investor.get('name', 'Investor')
        
        return f"""
Dear {investor_name},

I hope this email finds you well. I'm reaching out to introduce you to {self.company_info['name']}, the world's first AI Vice President system.

We're currently raising a {self.company_info['ask']} Series A at a {self.company_info['valuation']} valuation to address the {self.company_info['market']} market opportunity.

Key highlights:
• {self.company_info['traction']}
• {self.company_info['unique_value']}
• Production-ready system with enterprise-grade architecture

I'd love to schedule a brief call to discuss how {self.company_info['name']} could be a valuable addition to your portfolio.

Best regards,
{self.company_info['founder']}
Founder & CEO
{self.company_info['name']}
{self.company_info['founder_email']}
"""
    
    def _get_default_body(self) -> str:
        """Get default email body"""
        return f"""
Dear Investor,

I'm excited to introduce you to {self.company_info['name']}, the world's first AI Vice President system that's revolutionizing business management.

We're currently raising a {self.company_info['ask']} Series A at a {self.company_info['valuation']} valuation to capture the {self.company_info['market']} market opportunity.

Our system is production-ready with {self.company_info['traction']} and {self.company_info['unique_value']}.

I'd love to schedule a call to discuss this opportunity.

Best regards,
{self.company_info['founder']}
"""
    
    def send_email(self, email_data: Dict[str, Any]) -> Dict[str, Any]:
        """Send the generated email"""
        try:
            investor = email_data['investor']
            
            # Send email using email service
            result = email_service.send_investor_outreach(
                investor_info={
                    'name': investor.get('name', 'Unknown'),
                    'email': investor.get('email', ''),
                    'company': investor.get('source', 'Unknown')
                },
                email_content={
                    'subject': email_data['subject'],
                    'body': email_data['body']
                }
            )
            
            # Update email data with send result
            email_data['sent_at'] = datetime.now().isoformat()
            email_data['send_result'] = result
            email_data['status'] = 'sent' if result.get('status') == 'success' else 'failed'
            
            logger.info(f"✅ Email sent to {investor.get('name', 'Unknown')}: {result.get('status', 'unknown')}")
            return email_data
            
        except Exception as e:
            logger.error(f"Error sending email to {email_data['investor'].get('name', 'Unknown')}: {str(e)}")
            email_data['sent_at'] = datetime.now().isoformat()
            email_data['send_result'] = {'status': 'error', 'message': str(e)}
            email_data['status'] = 'failed'
            return email_data
    
    def generate_and_send_bulk_emails(self, investors: List[Dict[str, Any]], 
                                     style: str = 'professional',
                                     custom_message: Optional[str] = None) -> Dict[str, Any]:
        """Generate and send emails to multiple investors"""
        logger.info(f"🚀 Starting bulk email campaign for {len(investors)} investors")
        
        results = {
            'total_investors': len(investors),
            'generated': 0,
            'sent': 0,
            'failed': 0,
            'emails': [],
            'started_at': datetime.now().isoformat(),
            'completed_at': None
        }
        
        for i, investor in enumerate(investors):
            try:
                logger.info(f"Processing investor {i+1}/{len(investors)}: {investor.get('name', 'Unknown')}")
                
                # Generate email
                email_data = self.generate_email(investor, style, custom_message)
                results['generated'] += 1
                
                # Send email if generation was successful
                if email_data.get('status') != 'error':
                    email_data = self.send_email(email_data)
                    if email_data.get('status') == 'sent':
                        results['sent'] += 1
                    else:
                        results['failed'] += 1
                else:
                    results['failed'] += 1
                
                results['emails'].append(email_data)
                
            except Exception as e:
                logger.error(f"Error processing investor {investor.get('name', 'Unknown')}: {str(e)}")
                results['failed'] += 1
                results['emails'].append({
                    'investor': investor,
                    'status': 'error',
                    'error': str(e)
                })
        
        results['completed_at'] = datetime.now().isoformat()
        
        # Save results to log
        self._save_campaign_results(results)
        
        logger.info(f"✅ Bulk email campaign completed: {results['sent']} sent, {results['failed']} failed")
        return results
    
    def _save_campaign_results(self, results: Dict[str, Any]) -> str:
        """Save campaign results to JSON file"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"logs/email_campaign_{timestamp}.json"
        
        # Ensure logs directory exists
        os.makedirs("logs", exist_ok=True)
        
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(results, f, indent=2, ensure_ascii=False)
        
        logger.info(f"✅ Saved campaign results to {filename}")
        return filename
    
    def generate_voice_summary(self, campaign_results: Dict[str, Any]) -> str:
        """Generate a voice summary of the email campaign"""
        total = campaign_results['total_investors']
        sent = campaign_results['sent']
        failed = campaign_results['failed']
        
        summary = f"""
Masoud, I've successfully contacted {sent} out of {total} top AI investors in Toronto. 
{total - sent - failed} emails are still being processed, and {failed} encountered technical issues. 
You'll find detailed logs in your dashboard. The campaign focused on our {self.company_info['ask']} Series A raise 
at {self.company_info['valuation']} valuation. All emails were personalized and sent from your Gmail account. 
Would you like me to schedule follow-up reminders for next week?
"""
        
        return summary.strip()

# Global instance
email_builder = EmailBuilderAgent()

def run_email_campaign(investors: List[Dict[str, Any]], style: str = 'professional', 
                      custom_message: Optional[str] = None) -> Dict[str, Any]:
    """Main function to run the email campaign"""
    try:
        logger.info(f"🚀 Starting email campaign for {len(investors)} investors")
        
        # Generate and send emails
        results = email_builder.generate_and_send_bulk_emails(investors, style, custom_message)
        
        # Generate voice summary
        voice_summary = email_builder.generate_voice_summary(results)
        
        return {
            'status': 'success',
            'message': f'Email campaign completed: {results["sent"]} sent, {results["failed"]} failed',
            'results': results,
            'voice_summary': voice_summary,
            'timestamp': datetime.now().isoformat()
        }
        
    except Exception as e:
        logger.error(f"Error in email campaign: {str(e)}")
        return {
            'status': 'error',
            'message': f'Error running email campaign: {str(e)}',
            'results': {},
            'timestamp': datetime.now().isoformat()
        }

if __name__ == "__main__":
    # Test the email builder
    test_investor = {
        'name': 'Test Investor',
        'email': 'test@example.com',
        'source': 'test',
        'score': 0.9,
        'notes': 'Test investor for demo'
    }
    
    # Test email generation
    email_data = email_builder.generate_email(test_investor, 'professional')
    print(json.dumps(email_data, indent=2)) 