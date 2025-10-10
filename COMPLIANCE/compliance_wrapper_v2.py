"""
Minimal Compliance Wrapper - Easy integration with existing code
Add just 3 lines to your existing campaign script for basic compliance
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, Tuple, Optional

class MinimalCompliance:
    """
    Minimal compliance wrapper that prevents the worst violations
    
    Features:
    - Suppression list (opt-outs)
    - Rate limiting (50/day, 5/domain)
    - Minimum delays (30s between sends)
    - Simple integration (3 lines of code)
    """
    
    def __init__(self,
                 max_daily: int = 50,
                 max_per_domain: int = 5,
                 min_delay: int = 30,
                 tracking_dir: str = "tracking"):
        """
        Initialize minimal compliance
        
        Args:
            max_daily: Maximum emails per day (default: 50)
            max_per_domain: Maximum per domain per day (default: 5)
            min_delay: Minimum seconds between emails (default: 30)
            tracking_dir: Directory for tracking files
        """
        self.max_daily = max_daily
        self.max_per_domain = max_per_domain
        self.min_delay = min_delay
        
        # Setup directories
        self.tracking_dir = Path(tracking_dir)
        self.tracking_dir.mkdir(exist_ok=True)
        
        self.contacts_dir = Path("contacts")
        self.contacts_dir.mkdir(exist_ok=True)
        
        # Load suppression list
        self.suppression_file = self.contacts_dir / "suppression_list.json"
        self.suppression_list = self._load_suppression_list()
        
        # Load rate limits
        self.rate_file = self.tracking_dir / "rate_limits.json"
        self.rate_data = self._load_rate_data()
        
        self.last_send_time = None
        
        print(f"✅ Compliance initialized: {len(self.suppression_list)} suppressed, {self.rate_data.get('total_sent', 0)}/{max_daily} sent today")
    
    def _load_suppression_list(self) -> set:
        """Load emails that have opted out"""
        if not self.suppression_file.exists():
            # Create empty suppression list
            self._save_suppression_list(set())
            return set()
        
        try:
            with open(self.suppression_file, 'r') as f:
                data = json.load(f)
                return set(data.get('suppressed_emails', []))
        except Exception as e:
            print(f"⚠️  Warning: Could not load suppression list: {e}")
            return set()
    
    def _save_suppression_list(self, emails: set):
        """Save suppression list"""
        with open(self.suppression_file, 'w') as f:
            json.dump({
                'suppressed_emails': list(emails),
                'last_updated': datetime.now().isoformat(),
                'count': len(emails)
            }, f, indent=2)
    
    def _load_rate_data(self) -> Dict:
        """Load today's rate limit data"""
        today = datetime.now().date().isoformat()
        
        if not self.rate_file.exists():
            return {
                'date': today,
                'total_sent': 0,
                'domain_counts': {}
            }
        
        try:
            with open(self.rate_file, 'r') as f:
                data = json.load(f)
                
                # Reset if new day
                if data.get('date') != today:
                    return {
                        'date': today,
                        'total_sent': 0,
                        'domain_counts': {}
                    }
                
                return data
        except Exception as e:
            print(f"⚠️  Warning: Could not load rate data: {e}")
            return {
                'date': today,
                'total_sent': 0,
                'domain_counts': {}
            }
    
    def _save_rate_data(self):
        """Save rate limit data"""
        with open(self.rate_file, 'w') as f:
            json.dump(self.rate_data, f, indent=2)
    
    def can_send(self, email: str) -> Tuple[bool, str]:
        """
        Check if we can send to this email
        
        Args:
            email: Email address to check
            
        Returns:
            Tuple of (can_send: bool, reason: str)
        """
        email = email.lower().strip()
        
        # Check suppression list
        if email in self.suppression_list:
            return False, "suppressed"
        
        # Check daily limit
        if self.rate_data.get('total_sent', 0) >= self.max_daily:
            return False, "daily_limit"
        
        # Check domain limit
        domain = email.split('@')[-1] if '@' in email else 'unknown'
        domain_count = self.rate_data.get('domain_counts', {}).get(domain, 0)
        
        if domain_count >= self.max_per_domain:
            return False, f"domain_limit_{domain}"
        
        # Check minimum delay
        if self.last_send_time:
            elapsed = (datetime.now() - self.last_send_time).total_seconds()
            if elapsed < self.min_delay:
                wait = int(self.min_delay - elapsed)
                return False, f"wait_{wait}"
        
        return True, "ok"
    
    def record_send(self, email: str):
        """
        Record that we sent to this email
        
        Args:
            email: Email address we sent to
        """
        email = email.lower().strip()
        domain = email.split('@')[-1] if '@' in email else 'unknown'
        
        # Update counters
        self.rate_data['total_sent'] = self.rate_data.get('total_sent', 0) + 1
        
        if 'domain_counts' not in self.rate_data:
            self.rate_data['domain_counts'] = {}
        
        self.rate_data['domain_counts'][domain] = \
            self.rate_data['domain_counts'].get(domain, 0) + 1
        
        # Save
        self._save_rate_data()
        self.last_send_time = datetime.now()
    
    def add_to_suppression(self, email: str, reason: str = "opt-out"):
        """
        Add email to suppression list
        
        Args:
            email: Email to suppress
            reason: Reason for suppression
        """
        email = email.lower().strip()
        self.suppression_list.add(email)
        self._save_suppression_list(self.suppression_list)
        
        # Log it
        log_file = self.contacts_dir / "suppression_log.jsonl"
        with open(log_file, 'a') as f:
            json.dump({
                'email': email,
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            }, f)
            f.write('\n')
        
        print(f"✅ Added {email} to suppression list ({reason})")
    
    def add_footer(self, body: str, recipient_email: str, 
                   from_name: str = "Professional Outreach",
                   physical_address: str = None) -> str:
        """
        Add compliance footer to email
        
        Args:
            body: Email body
            recipient_email: Recipient's email
            from_name: Sender's name
            physical_address: Physical mailing address (required by CAN-SPAM)
            
        Returns:
            Email with footer added
        """
        footer = f"""

---

You received this email as part of professional networking outreach from {from_name}.

If you prefer not to receive future emails, reply with "UNSUBSCRIBE" in the subject line.

"""
        
        if physical_address:
            footer += f"Physical Address: {physical_address}\n"
        
        footer += """
This is a one-time professional outreach. We respect your preferences and will honor
all opt-out requests immediately.
"""
        return body + footer
    
    def get_stats(self) -> Dict:
        """Get current compliance statistics"""
        return {
            'suppressed_count': len(self.suppression_list),
            'sent_today': self.rate_data.get('total_sent', 0),
            'daily_limit': self.max_daily,
            'remaining_today': self.max_daily - self.rate_data.get('total_sent', 0),
            'domains_contacted': len(self.rate_data.get('domain_counts', {})),
            'per_domain_limit': self.max_per_domain
        }


# Quick test
if __name__ == "__main__":
    compliance = MinimalCompliance()
    
    print("\n📊 Compliance Stats:")
    stats = compliance.get_stats()
    for key, value in stats.items():
        print(f"   {key}: {value}")
    
    # Test an email
    test_email = "test@example.com"
    can_send, reason = compliance.can_send(test_email)
    print(f"\n🔍 Can send to {test_email}? {can_send} ({reason})")
