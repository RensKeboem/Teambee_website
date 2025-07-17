"""
Email Service

Handles email sending functionality including contact form emails.
"""

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import logging


class EmailService:
    """Service for sending emails."""
    
    def __init__(self):
        """Initialize email service with SMTP configuration."""
        self.logger = logging.getLogger(__name__)
        
        # Email configuration
        self.email_user = os.getenv("EMAIL_USER")
        self.email_password = os.getenv("EMAIL_PASSWORD")
        self.from_email = os.getenv("FROM_EMAIL", self.email_user)
        self.to_email = os.getenv("TO_EMAIL", self.email_user)
        
        # SMTP configuration
        self.smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
        self.smtp_port = int(os.getenv("SMTP_PORT", "587"))
    
    def send_contact_email(self, first_name: str, last_name: str, club_name: str, 
                          email: str, phone: str, identifier: str = "Contact") -> tuple[bool, str]:
        """Send contact form email."""
        try:
            if not all([self.email_user, self.email_password, self.to_email]):
                self.logger.warning("Email configuration incomplete")
                return False, "Email configuration incomplete"
            
            # Create message
            msg = MIMEMultipart()
            msg['From'] = self.from_email
            msg['To'] = self.to_email
            msg['Subject'] = f"Teambee {identifier} Form Submission - {club_name}"
            
            # Create email body
            body = f"""
New contact form submission from Teambee website:

Name: {first_name} {last_name}
Club: {club_name}
Email: {email}
Phone: {phone}
Form Type: {identifier}

This message was sent from the Teambee contact form.
"""
            
            msg.attach(MIMEText(body, 'plain'))
            
            # Send email
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.email_user, self.email_password)
                server.send_message(msg)
            
            self.logger.info(f"Contact email sent successfully for {email}")
            return True, "Email sent successfully"
            
        except Exception as e:
            self.logger.error(f"Error sending contact email: {e}")
            return False, f"Error sending email: {str(e)}" 