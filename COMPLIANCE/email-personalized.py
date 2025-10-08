"""
Enhanced Email Personalizer with Unsubscribe Links
Adds proper personalization and opt-out mechanisms to email campaigns
"""

import re
import json
import hashlib
import base64
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from urllib.parse import urlencode

class EmailPersonalizer:
    def __init__(self, 
                 unsubscribe_base_url: str = "https://your-domain.com/unsubscribe",
                 from_name: str = "Your Name",
                 from_email: str = "your.email@domain.com",
                 physical_address: str = "Your Address, City, Country"):
        """
        Initialize email personalizer
        
        Args:
            unsubscribe_base_url: Base URL for unsubscribe page
            from_name: Sender's full name
            from_email: Sender's email address
            physical_address: Physical mailing address (required by CAN-SPAM)
        """
        self.unsubscribe_base_url = unsubscribe_base_url
        self.from_name = from_name
        self.from_email = from_email
        self.physical_address = physical_address
        
    def generate_unsubscribe_token(self, email: str, campaign_id: str) -> str:
        """
        Generate a secure unsubscribe token
        
        Args:
            email: Recipient email
            campaign_id: Campaign identifier
            
        Returns:
            Base64 encoded token
        """
        data = f"{email}:{campaign_id}:{datetime.now().date().isoformat()}"
        token = hashlib.sha256(data.encode()).hexdigest()[:16]
        
        # Encode email and token together
        payload = json.dumps({'email': email, 'token': token, 'campaign': campaign_id})
        return base64.urlsafe_b64encode(payload.encode()).decode()
    
    def create_unsubscribe_link(self, email: str, campaign_id: str) -> str:
        """
        Create unsubscribe URL with token
        
        Args:
            email: Recipient email
            campaign_id: Campaign identifier
            
        Returns:
            Full unsubscribe URL
        """
        token = self.generate_unsubscribe_token(email, campaign_id)
        params = urlencode({'token': token})
        return f"{self.unsubscribe_base_url}?{params}"
    
    def personalize_template(self, 
                           template: str, 
                           contact: Dict,
                           campaign_id: str = "general") -> str:
        """
        Personalize email template with contact data
        
        Args:
            template: Email template with {{variable}} placeholders
            contact: Contact dictionary with personalization data
            campaign_id: Campaign identifier
            
        Returns:
            Personalized email content
        """
        personalized = template
        
        # Replace all template variables
        for key, value in contact.items():
            placeholder = f"{{{{{key}}}}}"
            personalized = personalized.replace(placeholder, str(value))
        
        # Add common defaults if not present
        defaults = {
            '{{name}}': contact.get('name', 'there'),
            '{{first_name}}': contact.get('name', 'there').split()[0] if contact.get('name') else 'there',
            '{{email}}': contact.get('email', ''),
            '{{organization}}': contact.get('organization', 'your organization'),
            '{{role}}': contact.get('role', 'professional'),
            '{{domain}}': contact.get('domain', 'industry'),
        }
        
        for placeholder, default in defaults.items():
            if placeholder in personalized:
                personalized = personalized.replace(placeholder, default)
        
        return personalized
    
    def add_unsubscribe_footer(self, 
                              email_body: str, 
                              recipient_email: str,
                              campaign_id: str = "general",
                              is_html: bool = False) -> str:
        """
        Add compliant unsubscribe footer to email
        
        Args:
            email_body: Email content
            recipient_email: Recipient's email address
            campaign_id: Campaign identifier
            is_html: Whether email is HTML format
            
        Returns:
            Email with footer added
        """
        unsubscribe_link = self.create_unsubscribe_link(recipient_email, campaign_id)
        
        if is_html:
            footer = f"""
<hr style="margin-top: 30px; border: none; border-top: 1px solid #ccc;">
<div style="font-size: 11px; color: #666; margin-top: 15px;">
    <p><strong>Professional Outreach from {self.from_name}</strong></p>
    <p>You received this email as part of professional networking outreach.</p>
    <p>
        If you prefer not to receive future emails, you can 
        <a href="{unsubscribe_link}" style="color: #0066cc;">unsubscribe here</a>.
    </p>
    <p>Contact: {self.from_email}<br>
    Address: {self.physical_address}</p>
    <p style="font-size: 10px; color: #999;">
        This is a one-time professional outreach. We respect your preferences and will honor all opt-out requests immediately.
    </p>
</div>
"""
        else:
            footer = f"""

---
Professional Outreach from {self.from_name}

You received this email as part of professional networking outreach.

If you prefer not to receive future emails, please visit:
{unsubscribe_link}

Or reply with "UNSUBSCRIBE" in the subject line.

Contact: {self.from_email}
Address: {self.physical_address}

This is a one-time professional outreach. We respect your preferences 
and will honor all opt-out requests immediately.
"""
        
        return email_body + footer
    
    def create_personalized_email(self,
                                 template: str,
                                 contact: Dict,
                                 campaign_id: str = "general",
                                 is_html: bool = False) -> Dict:
        """
        Create complete personalized email with all compliance features
        
        Args:
            template: Email template
            contact: Contact information
            campaign_id: Campaign identifier
            is_html: Whether email is HTML
            
        Returns:
            Dictionary with complete email data
        """
        # Personalize content
        personalized_body = self.personalize_template(template, contact, campaign_id)
        
        # Add unsubscribe footer
        final_body = self.add_unsubscribe_footer(
            personalized_body,
            contact.get('email', ''),
            campaign_id,
            is_html
        )
        
        # Extract or create subject
        subject_match = re.search(r'Subject:\s*(.+?)(?:\n|$)', final_body, re.IGNORECASE)
        if subject_match:
            subject = subject_match.group(1).strip()
            # Remove subject line from body
            final_body = re.sub(r'Subject:\s*.+?(?:\n|$)', '', final_body, count=1, flags=re.IGNORECASE)
        else:
            subject = f"Professional Outreach - {self.from_name}"
        
        # Create unsubscribe link for headers
        unsubscribe_link = self.create_unsubscribe_link(contact.get('email', ''), campaign_id)
        
        return {
            'to': contact.get('email', ''),
            'to_name': contact.get('name', ''),
            'subject': subject,
            'body': final_body.strip(),
            'from_email': self.from_email,
            'from_name': self.from_name,
            'campaign_id': campaign_id,
            'unsubscribe_url': unsubscribe_link,
            'headers': {
                'List-Unsubscribe': f'<{unsubscribe_link}>',
                'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
                'X-Campaign-ID': campaign_id,
                'Precedence': 'bulk'
            },
            'metadata': {
                'personalized_at': datetime.now().isoformat(),
                'recipient_domain': contact.get('domain', 'unknown'),
                'template_used': campaign_id
            }
        }
    
    def validate_personalization(self, email_content: str) -> Dict:
        """
        Validate that email is properly personalized
        
        Args:
            email_content: Email content to validate
            
        Returns:
            Validation results
        """
        issues = []
        
        # Check for remaining template variables
        remaining_vars = re.findall(r'\{\{([^}]+)\}\}', email_content)
        if remaining_vars:
            issues.append(f"Unpersonalized variables: {', '.join(remaining_vars)}")
        
        # Check for unsubscribe link
        if 'unsubscribe' not in email_content.lower():
            issues.append("Missing unsubscribe link")
        
        # Check for physical address
        if self.physical_address not in email_content:
            issues.append("Missing physical address")
        
        # Check for sender identification
        if self.from_name not in email_content:
            issues.append("Missing sender identification")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'has_unsubscribe': 'unsubscribe' in email_content.lower(),
            'has_address': self.physical_address in email_content,
            'personalization_complete': len(remaining_vars) == 0
        }


def main():
    """Example usage"""
    # Initialize personalizer with your details
    personalizer = EmailPersonalizer(
        unsubscribe_base_url="https://your-domain.com/unsubscribe",
        from_name="John Doe",
        from_email="john.doe@example.com",
        physical_address="123 Main St, City, Country"
    )
    
    # Example template
    template = """Subject: Professional Connection - {{name}}

Dear {{name}},

I noticed your work in {{domain}} at {{organization}}. As a {{role}}, 
you might be interested in my background and experience.

I'm reaching out to introduce myself and explore potential collaboration 
opportunities in the {{domain}} sector.

Best regards,
John Doe"""
    
    # Example contact
    contact = {
        'name': 'Jane Smith',
        'email': 'jane.smith@university.edu',
        'organization': 'Example University',
        'role': 'Department Head',
        'domain': 'education'
    }
    
    # Create personalized email
    personalized_email = personalizer.create_personalized_email(
        template,
        contact,
        campaign_id="education_outreach"
    )
    
    print("Personalized Email:")
    print("=" * 50)
    print(f"To: {personalized_email['to']}")
    print(f"Subject: {personalized_email['subject']}")
    print(f"\n{personalized_email['body']}")
    print("\n" + "=" * 50)
    
    # Validate personalization
    validation = personalizer.validate_personalization(personalized_email['body'])
    print("\nValidation Results:")
    print(json.dumps(validation, indent=2))


if __name__ == "__main__":
    main()
