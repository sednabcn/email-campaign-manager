"""
Enhanced Compliance Wrapper - Production Ready
Combines best features from all versions with improvements
"""

import json
import time
from pathlib import Path
from datetime import datetime, date
from typing import Tuple, Dict, Set, Optional


class MinimalCompliance:
    """
    Production-ready compliance wrapper for email campaigns
    
    Features:
    - Suppression list management (opt-outs)
    - Rate limiting (daily + per-domain)
    - Minimum delays between sends
    - Compliance footer generation
    - Comprehensive logging
    """
    
    def __init__(self,
                 daily_limit: int = 50,
                 per_domain_limit: int = 5,
                 min_delay_seconds: int = 30,
                 tracking_dir: str = "tracking",
                 contacts_dir: str = "contacts"):
        """
        Initialize compliance wrapper
        
        Args:
            daily_limit: Max emails per day (default: 50)
            per_domain_limit: Max per domain per day (default: 5)
            min_delay_seconds: Min seconds between sends (default: 30)
            tracking_dir: Directory for tracking files
            contacts_dir: Directory for contact lists
        """
        self.daily_limit = daily_limit
        self.per_domain_limit = per_domain_limit
        self.min_delay = min_delay_seconds
        
        # Setup directories
        self.tracking_dir = Path(tracking_dir)
        self.contacts_dir = Path(contacts_dir)
        self.tracking_dir.mkdir(exist_ok=True)
        self.contacts_dir.mkdir(exist_ok=True)
        
        # Initialize files
        self.suppression_file = self.contacts_dir / "suppression_list.json"
        self.rate_limit_file = self.tracking_dir / "rate_limits.json"
        self.send_log_file = self.tracking_dir / "send_log.jsonl"
        
        # Load data
        self.suppressed: Set[str] = self._load_suppression_list()
        self.rate_data: Dict = self._load_rate_limits()
        self.last_send_time: Optional[datetime] = None
        
        print(f"✅ Compliance initialized:")
        print(f"   Suppressed: {len(self.suppressed)}")
        print(f"   Sent today: {self.rate_data['total_sent']}/{self.daily_limit}")
        print(f"   Min delay: {self.min_delay}s between sends")
    
    def _load_suppression_list(self) -> Set[str]:
        """Load emails that have opted out"""
        if not self.suppression_file.exists():
            self._save_suppression_list(set())
            return set()
        
        try:
            with open(self.suppression_file, 'r') as f:
                data = json.load(f)
                return set(email.lower() for email in data.get('suppressed_emails', []))
        except Exception as e:
            print(f"⚠️  Warning: Could not load suppression list: {e}")
            return set()
    
    def _save_suppression_list(self, emails: Set[str]):
        """Save suppression list to file"""
        with open(self.suppression_file, 'w') as f:
            json.dump({
                'suppressed_emails': sorted(list(emails)),
                'last_updated': datetime.now().isoformat(),
                'count': len(emails)
            }, f, indent=2)
    
    def _load_rate_limits(self) -> Dict:
        """Load today's rate limit data"""
        today = str(date.today())
        
        if not self.rate_limit_file.exists():
            return {
                'date': today,
                'total_sent': 0,
                'domain_counts': {},
                'last_updated': None
            }
        
        try:
            with open(self.rate_limit_file, 'r') as f:
                data = json.load(f)
                
                # Reset if new day
                if data.get('date') != today:
                    return {
                        'date': today,
                        'total_sent': 0,
                        'domain_counts': {},
                        'last_updated': None
                    }
                
                return data
        except Exception as e:
            print(f"⚠️  Warning: Could not load rate limits: {e}")
            return {
                'date': today,
                'total_sent': 0,
                'domain_counts': {},
                'last_updated': None
            }
    
    def _save_rate_limits(self):
        """Save rate limit data to file"""
        self.rate_data['last_updated'] = datetime.now().isoformat()
        with open(self.rate_limit_file, 'w') as f:
            json.dump(self.rate_data, f, indent=2)
    
    def can_send(self, email: str) -> Tuple[bool, str]:
        """
        Check if we can send to this email address
        
        Args:
            email: Email address to check
            
        Returns:
            Tuple of (can_send: bool, reason: str)
            - If can_send is True, reason is "ok"
            - If False, reason explains why (suppressed, daily_limit, domain_limit, wait_X)
        """
        email = email.lower().strip()
        
        # Check suppression list
        if email in self.suppressed:
            return False, "suppressed"
        
        # Check daily limit
        if self.rate_data['total_sent'] >= self.daily_limit:
            return False, "daily_limit"
        
        # Check domain limit
        domain = email.split('@')[-1] if '@' in email else 'unknown'
        domain_count = self.rate_data['domain_counts'].get(domain, 0)
        
        if domain_count >= self.per_domain_limit:
            return False, f"domain_limit"
        
        # Check minimum delay
        if self.last_send_time:
            elapsed = (datetime.now() - self.last_send_time).total_seconds()
            if elapsed < self.min_delay:
                wait_time = int(self.min_delay - elapsed) + 1
                return False, f"wait_{wait_time}"
        
        return True, "ok"
    
    def record_send(self, email: str, success: bool = True, 
                   metadata: Optional[Dict] = None):
        """
        Record that we sent (or attempted to send) an email
        
        Args:
            email: Email address
            success: Whether send was successful
            metadata: Optional metadata to log (subject, template, etc.)
        """
        email = email.lower().strip()
        domain = email.split('@')[-1] if '@' in email else 'unknown'
        
        # Update rate limits
        self.rate_data['total_sent'] += 1
        if 'domain_counts' not in self.rate_data:
            self.rate_data['domain_counts'] = {}
        self.rate_data['domain_counts'][domain] = \
            self.rate_data['domain_counts'].get(domain, 0) + 1
        
        self._save_rate_limits()
        self.last_send_time = datetime.now()
        
        # Log the send
        log_entry = {
            'timestamp': datetime.now().isoformat(),
            'email': email,
            'domain': domain,
            'success': success
        }
        if metadata:
            log_entry['metadata'] = metadata
        
        with open(self.send_log_file, 'a') as f:
            f.write(json.dumps(log_entry) + '\n')
    
    def add_to_suppression(self, email: str, reason: str = "opt-out"):
        """
        Add email to suppression list
        
        Args:
            email: Email to suppress
            reason: Reason for suppression (opt-out, bounce, complaint, etc.)
        """
        email = email.lower().strip()
        self.suppressed.add(email)
        self._save_suppression_list(self.suppressed)
        
        # Log suppression
        log_file = self.contacts_dir / 'suppression_log.jsonl'
        with open(log_file, 'a') as f:
            json.dump({
                'email': email,
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            }, f)
            f.write('\n')
        
        print(f"✅ Added {email} to suppression list ({reason})")
    
    def add_footer(self, body: str, 
                   sender_name: str = "Professional Outreach",
                   physical_address: Optional[str] = None,
                   unsubscribe_email: Optional[str] = None) -> str:
        """
        Add CAN-SPAM compliant footer to email
        
        Args:
            body: Email body text
            sender_name: Name of sender/organization
            physical_address: Physical mailing address (recommended)
            unsubscribe_email: Email for unsubscribe requests
            
        Returns:
            Email body with footer appended
        """
        footer = f"\n\n{'─' * 60}\n\n"
        footer += f"You received this as professional outreach from {sender_name}.\n\n"
        
        if unsubscribe_email:
            footer += f"To unsubscribe: Reply to {unsubscribe_email} with 'UNSUBSCRIBE' in the subject.\n"
        else:
            footer += "To unsubscribe: Reply with 'UNSUBSCRIBE' in the subject line.\n"
        
        if physical_address:
            footer += f"\nPhysical Address: {physical_address}\n"
        
        footer += "\nWe respect your preferences and honor all opt-out requests immediately."
        
        return body + footer
    
    def get_stats(self) -> Dict:
        """Get current compliance statistics"""
        return {
            'suppressed_count': len(self.suppressed),
            'sent_today': self.rate_data['total_sent'],
            'daily_limit': self.daily_limit,
            'remaining_today': max(0, self.daily_limit - self.rate_data['total_sent']),
            'domains_contacted': len(self.rate_data['domain_counts']),
            'per_domain_limit': self.per_domain_limit,
            'date': self.rate_data['date']
        }
    
    def wait_if_needed(self):
        """Wait if minimum delay hasn't elapsed since last send"""
        if self.last_send_time:
            elapsed = (datetime.now() - self.last_send_time).total_seconds()
            if elapsed < self.min_delay:
                wait_time = self.min_delay - elapsed
                print(f"⏱️  Waiting {wait_time:.1f}s for rate limit...")
                time.sleep(wait_time)


# ==============================================================================
# INTEGRATION EXAMPLE - Add to your existing campaign script
# ==============================================================================

def example_integration():
    """
    How to integrate with your existing email campaign code
    """
    
    # 1. Initialize at start of script
    compliance = ComplianceWrapper(
        daily_limit=50,
        per_domain_limit=5,
        min_delay_seconds=30
    )
    
    # 2. In your email loop, check before sending
    recipients = ["user1@example.com", "user2@example.com"]
    
    for email in recipients:
        # Check if we can send
        can_send, reason = compliance.can_send(email)
        
        if not can_send:
            if reason.startswith('wait_'):
                # Wait and retry
                wait_seconds = int(reason.split('_')[1])
                print(f"Waiting {wait_seconds}s before sending to {email}")
                time.sleep(wait_seconds)
                # Check again
                can_send, reason = compliance.can_send(email)
            
            if not can_send:
                print(f"❌ Skipping {email}: {reason}")
                continue
        
        # Send your email here
        email_body = "Your message here"
        email_body_with_footer = compliance.add_footer(
            email_body,
            sender_name="Your Name",
            physical_address="123 Main St, City, State 12345"
        )
        
        # YOUR EMAIL SENDING CODE HERE
        # success = send_email(email, subject, email_body_with_footer)
        success = True  # placeholder
        
        # Record the send
        compliance.record_send(email, success=success)
        
        print(f"✅ Sent to {email}")
    
    # 3. Show final stats
    stats = compliance.get_stats()
    print(f"\n📊 Campaign complete: {stats['sent_today']}/{stats['daily_limit']} sent")


if __name__ == "__main__":
    # Quick test
    compliance = ComplianceWrapper()
    
    print("\n📊 Compliance Stats:")
    stats = compliance.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test sending
    test_email = "test@example.com"
    can_send, reason = compliance.can_send(test_email)
    print(f"\n🔍 Can send to {test_email}? {can_send} ({reason})")
    
    if can_send:
        # Example with footer
        body = "Hi there,\n\nThis is a test email."
        body_with_footer = compliance.add_footer(
            body,
            sender_name="Test Campaign",
            physical_address="123 Test St, City, ST 12345"
        )
        print(f"\n📧 Email with footer:\n{body_with_footer}")
