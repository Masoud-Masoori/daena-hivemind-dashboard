import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional, Dict, Any
import os
import json
from datetime import datetime
import logging

logger = logging.getLogger(__name__)

class EmailService:
    def __init__(self):
        self.gmail_user = "masoud.masoori@gmail.com"
        self.gmail_password = os.getenv("GMAIL_APP_PASSWORD", "")
        self.smtp_server = "smtp.gmail.com"
        self.smtp_port = 587
        
    def send_email(self, to_email: str, subject: str, body: str, 
                   from_name: str = "Masoud Masoori", 
                   reply_to: str = "investors@daena-ai.com") -> Dict[str, Any]:
        """
        Send email via Gmail SMTP
        
        Args:
            to_email: Recipient email address
            subject: Email subject
            body: Email body (HTML or plain text)
            from_name: Sender name
            reply_to: Reply-to email address
            
        Returns:
            Dict with status and message
        """
        try:
            if not self.gmail_password:
                logger.warning("Gmail password not configured - simulating email send")
                return self._simulate_email_send(to_email, subject, body)
            
            # Create message
            msg = MIMEMultipart('alternative')
            msg['Subject'] = subject
            msg['From'] = f"{from_name} <{self.gmail_user}>"
            msg['To'] = to_email
            msg['Reply-To'] = reply_to
            
            # Add body
            html_part = MIMEText(body, 'html')
            msg.attach(html_part)
            
            # Create secure SSL context
            context = ssl.create_default_context()
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls(context=context)
                server.login(self.gmail_user, self.gmail_password)
                server.send_message(msg)
            
            # Log successful send
            self._log_email_send(to_email, subject, "sent")
            
            return {
                "status": "success",
                "message": "Email sent successfully",
                "to": to_email,
                "subject": subject,
                "sent_at": datetime.now().isoformat()
            }
            
        except Exception as e:
            logger.error(f"Failed to send email: {e}")
            self._log_email_send(to_email, subject, "failed", str(e))
            
            return {
                "status": "error",
                "message": f"Failed to send email: {str(e)}",
                "to": to_email,
                "subject": subject,
                "error": str(e)
            }
    
    def _simulate_email_send(self, to_email: str, subject: str, body: str) -> Dict[str, Any]:
        """Simulate email sending for demo purposes"""
        logger.info(f"Simulating email send to {to_email}: {subject}")
        
        # Log the simulated send
        self._log_email_send(to_email, subject, "simulated")
        
        return {
            "status": "success",
            "message": "Email sent successfully (simulated)",
            "to": to_email,
            "subject": subject,
            "sent_at": datetime.now().isoformat(),
            "simulated": True
        }
    
    def _log_email_send(self, to_email: str, subject: str, status: str, error: str = None):
        """Log email send attempt"""
        try:
            log_entry = {
                "to": to_email,
                "subject": subject,
                "status": status,
                "sent_at": datetime.now().isoformat(),
                "from": self.gmail_user
            }
            
            if error:
                log_entry["error"] = error
            
            # Ensure logs directory exists
            os.makedirs("logs", exist_ok=True)
            
            # Append to log file
            with open("logs/email_log.jsonl", "a", encoding="utf-8") as f:
                f.write(json.dumps(log_entry) + "\n")
                
        except Exception as e:
            logger.error(f"Failed to log email send: {e}")
    
    def get_email_history(self, limit: int = 50) -> list:
        """Get recent email history"""
        try:
            emails = []
            log_file = "logs/email_log.jsonl"
            
            if os.path.exists(log_file):
                with open(log_file, "r", encoding="utf-8") as f:
                    lines = f.readlines()
                    for line in lines[-limit:]:  # Get last N lines
                        try:
                            email_data = json.loads(line.strip())
                            emails.append(email_data)
                        except json.JSONDecodeError:
                            continue
            
            return emails[::-1]  # Reverse to show newest first
            
        except Exception as e:
            logger.error(f"Failed to get email history: {e}")
            return []
    
    def send_investor_outreach(self, investor_info: Dict[str, str], 
                             email_content: Dict[str, str]) -> Dict[str, Any]:
        """
        Send investor outreach email with proper formatting
        
        Args:
            investor_info: Dict with investor details
            email_content: Dict with subject and body
            
        Returns:
            Dict with send status
        """
        try:
            # Format email body as HTML
            html_body = f"""
            <html>
            <body style="font-family: Arial, sans-serif; line-height: 1.6; color: #333;">
                <div style="max-width: 600px; margin: 0 auto; padding: 20px;">
                    {email_content['body'].replace('\n', '<br>')}
                    
                    <hr style="margin: 30px 0; border: none; border-top: 1px solid #eee;">
                    <p style="font-size: 12px; color: #666;">
                        This email was sent by Daena AI VP System - The World's First AI Vice President<br>
                        For more information, visit: <a href="https://daena-ai.com">daena-ai.com</a>
                    </p>
                </div>
            </body>
            </html>
            """
            
            return self.send_email(
                to_email=investor_info['email'],
                subject=email_content['subject'],
                body=html_body,
                from_name="Masoud Masoori - Daena AI VP",
                reply_to="investors@daena-ai.com"
            )
            
        except Exception as e:
            logger.error(f"Failed to send investor outreach: {e}")
            return {
                "status": "error",
                "message": f"Failed to send investor outreach: {str(e)}"
            }

# Global email service instance
email_service = EmailService() 