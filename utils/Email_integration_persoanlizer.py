"""
Complete Integration: Unsubscribe System with Email Campaign
Drop-in replacement for your existing email_personalizer.py
"""

import re
import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional, List
from urllib.parse import urlencode


class ImprovedEmailPersonalizer:
    """Enhanced email personalizer with integrated unsubscribe management"""
    
    def __init__(self, 
                 unsubscribe_manager,  # Pass the UnsubscribeManager instance
                 from_name: str = "Your Name",
                 from_email: str = "your.email@domain.com",
                 physical_address: str = "Your Address, City, Country",
                 company_name: str = "Your Company"):
        """
        Initialize email personalizer
        
        Args:
            unsubscribe_manager: UnsubscribeManager instance
            from_name: Sender's full name
            from_email: Sender's email address
            physical_address: Physical mailing address (CAN-SPAM requirement)
            company_name: Your company/organization name
        """
        self.unsub_manager = unsubscribe_manager
        self.from_name = from_name
        self.from_email = from_email
        self.physical_address = physical_address
        self.company_name = company_name
        
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
        
        # Replace all template variables from contact
        for key, value in contact.items():
            if value is not None:  # Skip None values
                placeholder = f"{{{{{key}}}}}"
                personalized = personalized.replace(placeholder, str(value))
        
        # Smart defaults for common fields
        defaults = {
            '{{name}}': self._get_name(contact),
            '{{first_name}}': self._get_first_name(contact),
            '{{last_name}}': self._get_last_name(contact),
            '{{email}}': contact.get('email', ''),
            '{{organization}}': contact.get('organization', contact.get('company', 'your organization')),
            '{{role}}': contact.get('role', contact.get('title', 'professional')),
            '{{domain}}': contact.get('domain', 'industry'),
            '{{company}}': contact.get('company', contact.get('organization', 'your organization')),
            '{{title}}': contact.get('title', contact.get('role', 'professional')),
        }
        
        for placeholder, default in defaults.items():
            if placeholder in personalized:
                personalized = personalized.replace(placeholder, default)
        
        # Add unsubscribe link if placeholder exists
        if '{{unsubscribe_link}}' in personalized:
            unsub_link = self.unsub_manager.generate_unsubscribe_link(
                contact.get('email', ''), 
                campaign_id
            )
            personalized = personalized.replace('{{unsubscribe_link}}', unsub_link)
        
        return personalized
    
    def _get_name(self, contact: Dict) -> str:
        """Extract full name from contact"""
        if contact.get('name'):
            return contact['name']
        
        first = contact.get('first_name', '')
        last = contact.get('last_name', '')
        
        if first and last:
            return f"{first} {last}"
        elif first:
            return first
        elif last:
            return last
        
        return "there"
    
    def _get_first_name(self, contact: Dict) -> str:
        """Extract first name from contact"""
        if contact.get('first_name'):
            return contact['first_name']
        
        if contact.get('name'):
            return contact['name'].split()[0]
        
        return "there"
    
    def _get_last_name(self, contact: Dict) -> str:
        """Extract last name from contact"""
        if contact.get('last_name'):
            return contact['last_name']
        
        if contact.get('name'):
            parts = contact['name'].split()
            return parts[-1] if len(parts) > 1 else ""
        
        return ""
    
    def add_footer(self, 
                   email_body: str, 
                   recipient_email: str,
                   campaign_id: str = "general",
                   is_html: bool = False) -> str:
        """
        Add CAN-SPAM compliant footer with unsubscribe link
        
        Args:
            email_body: Email content
            recipient_email: Recipient's email address
            campaign_id: Campaign identifier
            is_html: Whether email is HTML format
            
        Returns:
            Email with footer added
        """
        unsub_link = self.unsub_manager.generate_unsubscribe_link(
            recipient_email, 
            campaign_id
        )
        
        if is_html:
            footer = f"""
<div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #e0e0e0; font-family: Arial, sans-serif;">
    <table width="100%" cellpadding="0" cellspacing="0" style="font-size: 12px; color: #666;">
        <tr>
            <td style="padding-bottom: 15px;">
                <strong style="color: #333; font-size: 13px;">Professional Outreach from {self.from_name}</strong>
            </td>
        </tr>
        <tr>
            <td style="padding-bottom: 10px;">
                You received this email as part of professional networking outreach.
            </td>
        </tr>
        <tr>
            <td style="padding-bottom: 15px;">
                If you prefer not to receive future emails, you can 
                <a href="{unsub_link}" style="color: #0066cc; text-decoration: underline;">unsubscribe here</a>.
            </td>
        </tr>
        <tr>
            <td style="padding-bottom: 10px;">
                <strong>Contact:</strong> {self.from_email}<br>
                <strong>Address:</strong> {self.physical_address}
            </td>
        </tr>
        <tr>
            <td style="padding-top: 10px; font-size: 11px; color: #999;">
                {self.company_name} respects your privacy and preferences. 
                All opt-out requests are honored immediately.
            </td>
        </tr>
    </table>
</div>
"""
        else:
            footer = f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Professional Outreach from {self.from_name}

You received this email as part of professional networking outreach.

If you prefer not to receive future emails, please visit:
{unsub_link}

Or reply with "UNSUBSCRIBE" in the subject line.

Contact: {self.from_email}
Address: {self.physical_address}

{self.company_name} respects your privacy and preferences. 
All opt-out requests are honored immediately.
"""
        
        return email_body + footer
    
    def create_email(self,
                    template: str,
                    contact: Dict,
                    campaign_id: str = "general",
                    is_html: bool = False,
                    include_footer: bool = True) -> Dict:
        """
        Create complete personalized email with all compliance features
        
        Args:
            template: Email template
            contact: Contact information
            campaign_id: Campaign identifier
            is_html: Whether email is HTML
            include_footer: Whether to add unsubscribe footer
            
        Returns:
            Dictionary with complete email data
        """
        recipient_email = contact.get('email', '').strip().lower()
        
        # Check if unsubscribed
        if self.unsub_manager.is_unsubscribed(recipient_email, campaign_id):
            return {
                'status': 'skipped',
                'reason': 'unsubscribed',
                'email': recipient_email
            }
        
        # Personalize content
        personalized_body = self.personalize_template(template, contact, campaign_id)
        
        # Extract subject line
        subject = self._extract_subject(personalized_body)
        personalized_body = self._remove_subject_line(personalized_body)
        
        # Add footer if requested
        if include_footer:
            personalized_body = self.add_footer(
                personalized_body,
                recipient_email,
                campaign_id,
                is_html
            )
        
        # Create unsubscribe link
        unsub_link = self.unsub_manager.generate_unsubscribe_link(
            recipient_email, 
            campaign_id
        )
        
        return {
            'status': 'ready',
            'to': recipient_email,
            'to_name': self._get_name(contact),
            'subject': subject or f"Professional Outreach - {self.from_name}",
            'body': personalized_body.strip(),
            'from_email': self.from_email,
            'from_name': self.from_name,
            'campaign_id': campaign_id,
            'unsubscribe_url': unsub_link,
            'headers': {
                'List-Unsubscribe': f'<{unsub_link}>',
                'List-Unsubscribe-Post': 'List-Unsubscribe=One-Click',
                'X-Campaign-ID': campaign_id,
                'Precedence': 'bulk',
                'X-Auto-Response-Suppress': 'OOF, AutoReply'
            },
            'metadata': {
                'personalized_at': datetime.now().isoformat(),
                'recipient_domain': contact.get('domain', 'unknown'),
                'template_used': campaign_id,
                'recipient_info': {
                    'name': self._get_name(contact),
                    'organization': contact.get('organization', ''),
                    'role': contact.get('role', '')
                }
            }
        }
    
    def _extract_subject(self, content: str) -> Optional[str]:
        """Extract subject line from email content"""
        match = re.search(r'^Subject:\s*(.+?)(?:\n|$)', content, re.IGNORECASE | re.MULTILINE)
        return match.group(1).strip() if match else None
    
    def _remove_subject_line(self, content: str) -> str:
        """Remove subject line from email content"""
        return re.sub(r'^Subject:\s*.+?(?:\n|$)', '', content, count=1, flags=re.IGNORECASE | re.MULTILINE)
    
    def batch_create_emails(self,
                           template: str,
                           contacts: List[Dict],
                           campaign_id: str = "general",
                           is_html: bool = False) -> Dict[str, List]:
        """
        Create emails for multiple contacts
        
        Args:
            template: Email template
            contacts: List of contact dictionaries
            campaign_id: Campaign identifier
            is_html: Whether email is HTML
            
        Returns:
            Dictionary with 'ready' and 'skipped' lists
        """
        results = {
            'ready': [],
            'skipped': [],
            'errors': []
        }
        
        for contact in contacts:
            try:
                email_data = self.create_email(
                    template,
                    contact,
                    campaign_id,
                    is_html
                )
                
                if email_data['status'] == 'ready':
                    results['ready'].append(email_data)
                else:
                    results['skipped'].append(email_data)
                    
            except Exception as e:
                results['errors'].append({
                    'contact': contact.get('email', 'unknown'),
                    'error': str(e)
                })
        
        return results
    
    def validate_email(self, email_data: Dict) -> Dict:
        """
        Validate that email is properly constructed
        
        Args:
            email_data: Email data dictionary
            
        Returns:
            Validation results
        """
        issues = []
        warnings = []
        
        # Check required fields
        required = ['to', 'subject', 'body', 'from_email']
        for field in required:
            if not email_data.get(field):
                issues.append(f"Missing required field: {field}")
        
        body = email_data.get('body', '')
        
        # Check for remaining template variables
        remaining_vars = re.findall(r'\{\{([^}]+)\}\}', body)
        if remaining_vars:
            warnings.append(f"Unpersonalized variables: {', '.join(set(remaining_vars))}")
        
        # Check for unsubscribe link
        if 'unsubscribe' not in body.lower():
            issues.append("Missing unsubscribe link")
        
        # Check for physical address
        if self.physical_address not in body:
            issues.append("Missing physical address (CAN-SPAM requirement)")
        
        # Check for sender identification
        if self.from_name not in body:
            warnings.append("Sender name not mentioned in body")
        
        # Check subject length
        subject_len = len(email_data.get('subject', ''))
        if subject_len > 100:
            warnings.append(f"Subject line very long ({subject_len} chars)")
        elif subject_len < 10:
            warnings.append(f"Subject line very short ({subject_len} chars)")
        
        return {
            'is_valid': len(issues) == 0,
            'issues': issues,
            'warnings': warnings,
            'has_unsubscribe': 'unsubscribe' in body.lower(),
            'has_address': self.physical_address in body,
            'personalization_complete': len(remaining_vars) == 0,
            'subject_length': subject_len
        }


# Integration helper functions
def integrate_with_existing_system(tracking_dir: Path, 
                                   base_url: str,
                                   from_name: str,
                                   from_email: str,
                                   physical_address: str) -> tuple:
    """
    Initialize complete email system with unsubscribe
    
    Returns:
        Tuple of (UnsubscribeManager, ImprovedEmailPersonalizer)
    """
    from pathlib import Path
    
    # Import the UnsubscribeManager from the first artifact
    # (In practice, save the first artifact as unsubscribe_manager.py)
    # from unsubscribe_manager import UnsubscribeManager
    
    # Initialize unsubscribe manager
    unsub_manager = UnsubscribeManager(
        tracking_dir=tracking_dir,
        base_url=base_url
    )
    
    # Initialize personalizer
    personalizer = ImprovedEmailPersonalizer(
        unsubscribe_manager=unsub_manager,
        from_name=from_name,
        from_email=from_email,
        physical_address=physical_address
    )
    
    return unsub_manager, personalizer


# Example usage
def example_usage():
    """Complete example of using the system"""
    
    # Initialize system
    unsub_manager, personalizer = integrate_with_existing_system(
        tracking_dir=Path("tracking"),
        base_url="https://sednabcn.github.io/unsubscribe",
        from_name="John Doe",
        from_email="john.doe@example.com",
        physical_address="123 Main St, City, ST 12345, USA"
    )
    
    # Email template
    template = """Subject: Quick Question - {{name}}

Hi {{first_name}},

I noticed your work in {{domain}} at {{organization}}. As a {{role}}, 
you might be interested in my experience with [relevant topic].

Would you be open to a brief conversation?

Best regards,
John Doe"""
    
    # Sample contacts
    contacts = [
        {
            'name': 'Jane Smith',
            'email': 'jane.smith@university.edu',
            'organization': 'Example University',
            'role': 'Department Head',
            'domain': 'education'
        },
        {
            'name': 'Bob Johnson',
            'email': 'bob@company.com',
            'organization': 'Tech Corp',
            'role': 'Engineering Manager',
            'domain': 'technology'
        }
    ]
    
    # Create emails in batch
    results = personalizer.batch_create_emails(
        template,
        contacts,
        campaign_id="initial_outreach_2025"
    )
    
    print(f"\n📧 Email Creation Results:")
    print(f"  ✅ Ready to send: {len(results['ready'])}")
    print(f"  ⏭️  Skipped: {len(results['skipped'])}")
    print(f"  ❌ Errors: {len(results['errors'])}")
    
    # Process ready emails
    for email_data in results['ready']:
        print(f"\n{'='*60}")
        print(f"To: {email_data['to_name']} <{email_data['to']}>")
        print(f"Subject: {email_data['subject']}")
        print(f"Unsubscribe: {email_data['unsubscribe_url']}")
        
        # Validate
        validation = personalizer.validate_email(email_data)
        if validation['is_valid']:
            print("✅ Email passes validation")
        else:
            print(f"⚠️  Issues: {', '.join(validation['issues'])}")
        
        if validation['warnings']:
            print(f"⚠️  Warnings: {', '.join(validation['warnings'])}")
        
        # In production: send the email here
        # send_email(email_data)
    
    # Show statistics
    stats = unsub_manager.get_stats()
    print(f"\n📊 Unsubscribe Statistics:")
    print(json.dumps(stats, indent=2))


if __name__ == "__main__":
    example_usage()
