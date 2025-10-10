#!/usr/bin/env python3
"""
Minimal Compliance Wrapper
Add this to utils/ and import it in your existing campaign script
"""

import json
import time
from pathlib import Path
from datetime import datetime

class MinimalCompliance:
    """Lightweight compliance wrapper - add to existing code"""
    
    def __init__(self, max_daily=50, max_per_domain=5, min_delay=30):
        self.max_daily = max_daily
        self.max_per_domain = max_per_domain
        self.min_delay = min_delay
        
        # Load suppression list
        self.suppressed = self._load_suppressed()
        
        # Load rate limits
        self.limits = self._load_limits()
        
        self.last_send = None
    
    def _load_suppressed(self):
        """Load suppression list"""
        supp_file = Path("contacts/suppression_list.json")
        if not supp_file.exists():
            return set()
        
        try:
            with open(supp_file) as f:
                data = json.load(f)
                return set(data.get('suppressed_emails', []))
        except:
            return set()
    
    def _load_limits(self):
        """Load rate limits"""
        limit_file = Path("tracking/rate_limits.json")
        today = datetime.now().date().isoformat()
        
        if not limit_file.exists():
            return {'date': today, 'total_sent': 0, 'domain_counts': {}}
        
        try:
            with open(limit_file) as f:
                data = json.load(f)
                
            # Reset if new day
            if data.get('date') != today:
                return {'date': today, 'total_sent': 0, 'domain_counts': {}}
            
            return data
        except:
            return {'date': today, 'total_sent': 0, 'domain_counts': {}}
    
    def _save_limits(self):
        """Save rate limits"""
        limit_file = Path("tracking/rate_limits.json")
        limit_file.parent.mkdir(exist_ok=True)
        
        with open(limit_file, 'w') as f:
            json.dump(self.limits, f, indent=2)
    
    def can_send(self, email):
        """Check if we can send to this email"""
        email = email.lower().strip()
        
        # Check suppression
        if email in self.suppressed:
            return False, "suppressed"
        
        # Check daily limit
        if self.limits['total_sent'] >= self.max_daily:
            return False, "daily_limit"
        
        # Check domain limit
        domain = email.split('@')[-1]
        if self.limits['domain_counts'].get(domain, 0) >= self.max_per_domain:
            return False, "domain_limit"
        
        # Check delay
        if self.last_send:
            elapsed = (datetime.now() - self.last_send).total_seconds()
            if elapsed < self.min_delay:
                return False, f"wait_{int(self.min_delay - elapsed)}"
        
        return True, "ok"
    
    def record_send(self, email):
        """Record that email was sent"""
        domain = email.split('@')[-1].lower()
        
        self.limits['total_sent'] += 1
        self.limits['domain_counts'][domain] = \
            self.limits['domain_counts'].get(domain, 0) + 1
        
        self.last_send = datetime.now()
        self._save_limits()
    
    def add_footer(self, body, email):
        """Add minimal compliance footer"""
        footer = f"""

---
To unsubscribe: https://github.com/{email}/issues/new?labels=unsubscribe
This is professional outreach. We respect opt-out requests.
"""
        return body + footer


# ==============================================================
# USAGE: Add these 3 lines to your existing campaign script
# ==============================================================

def integrate_with_existing_code():
    """
    Example of how to integrate with your existing code
    """
    
    # 1. At the top of your existing script, add:
    from compliance_wrapper import MinimalCompliance
    compliance = MinimalCompliance(max_daily=50, max_per_domain=5, min_delay=30)
    
    # 2. Before sending each email, add this check:
    # can_send, reason = compliance.can_send(recipient_email)
    # if not can_send:
    #     print(f"Skipping {recipient_email}: {reason}")
    #     if reason.startswith('wait_'):
    #         time.sleep(int(reason.split('_')[1]))
    #     continue
    
    # 3. After successfully sending, add:
    # compliance.record_send(recipient_email)
    
    # 4. (Optional) Add footer to email body:
    # email_body = compliance.add_footer(original_body, recipient_email)
    
    pass


if __name__ == "__main__":
    # Quick test
    compliance = MinimalCompliance()
    
    test_email = "test@example.com"
    can_send, reason = compliance.can_send(test_email)
    
    print(f"Can send to {test_email}: {can_send} ({reason})")
    print(f"Current limits: {compliance.limits}")
    print(f"Suppressed count: {len(compliance.suppressed)}")
