import json
from pathlib import Path
from datetime import datetime, date

class MinimalCompliance:
    def __init__(self, 
                 suppression_file='contacts/suppression_list.json',
                 rate_limit_file='tracking/rate_limits.json',
                 daily_limit=50,
                 per_domain_limit=5):
        self.suppression_file = Path(suppression_file)
        self.rate_limit_file = Path(rate_limit_file)
        self.daily_limit = daily_limit
        self.per_domain_limit = per_domain_limit
        
        # Load suppression list
        self.suppressed = self._load_suppression_list()
        
        # Load rate limits
        self.rate_limits = self._load_rate_limits()
    
    def _load_suppression_list(self):
        """Load list of suppressed emails"""
        if self.suppression_file.exists():
            with open(self.suppression_file) as f:
                data = json.load(f)
                return set(data.get('suppressed_emails', []))
        return set()
    
    def _load_rate_limits(self):
        """Load current rate limit tracking"""
        if self.rate_limit_file.exists():
            with open(self.rate_limit_file) as f:
                data = json.load(f)
                # Check if it's today's data
                if data.get('date') == str(date.today()):
                    return data
        
        # Return fresh data for today
        return {
            'date': str(date.today()),
            'total_sent': 0,
            'domain_counts': {},
            'last_updated': datetime.now().isoformat()
        }
    
    def is_suppressed(self, email):
        """Check if email is suppressed"""
        return email.lower() in self.suppressed
    
    def can_send_today(self):
        """Check if we can send more emails today"""
        return self.rate_limits['total_sent'] < self.daily_limit
    
    def can_send_to_domain(self, domain):
        """Check if we can send to this domain"""
        current = self.rate_limits['domain_counts'].get(domain, 0)
        return current < self.per_domain_limit
    
    def record_send(self, email, domain):
        """Record that we sent an email"""
        # Update counts
        self.rate_limits['total_sent'] += 1
        self.rate_limits['domain_counts'][domain] = \
            self.rate_limits['domain_counts'].get(domain, 0) + 1
        self.rate_limits['last_updated'] = datetime.now().isoformat()
        
        # Save to file
        self.rate_limit_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.rate_limit_file, 'w') as f:
            json.dump(self.rate_limits, f, indent=2)
    
    def add_suppression(self, email, reason='unsubscribe'):
        """Add email to suppression list"""
        self.suppressed.add(email.lower())
        
        # Save to file
        self.suppression_file.parent.mkdir(parents=True, exist_ok=True)
        data = {
            'suppressed_emails': sorted(list(self.suppressed)),
            'last_updated': datetime.now().isoformat(),
            'count': len(self.suppressed)
        }
        with open(self.suppression_file, 'w') as f:
            json.dump(data, f, indent=2)
        
        # Log the suppression
        log_file = self.suppression_file.parent / 'suppression_log.jsonl'
        with open(log_file, 'a') as f:
            log_entry = {
                'email': email,
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            }
            f.write(json.dumps(log_entry) + '\n')
    
    def get_stats(self):
        """Get compliance statistics"""
        return {
            'suppressed_count': len(self.suppressed),
            'sent_today': self.rate_limits['total_sent'],
            'daily_limit': self.daily_limit,
            'remaining_today': self.daily_limit - self.rate_limits['total_sent'],
            'domains_contacted': len(self.rate_limits['domain_counts']),
            'per_domain_limit': self.per_domain_limit
        }
