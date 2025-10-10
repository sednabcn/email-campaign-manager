"""
Enhanced Contact Validator with Opt-out Management
Validates contacts, manages suppression list, and enforces rate limits
"""

import json
import csv
import hashlib
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional
import time

class ContactValidator:
    def __init__(self, 
                 suppression_file: str = "contacts/suppression_list.json",
                 rate_limit_file: str = "tracking/rate_limits.json",
                 max_daily_sends: int = 50,
                 max_per_domain: int = 5):
        """
        Initialize validator with suppression list and rate limits
        
        Args:
            suppression_file: Path to opt-out/suppression list
            rate_limit_file: Path to rate limit tracking
            max_daily_sends: Maximum emails per day total
            max_per_domain: Maximum emails per domain per day
        """
        self.suppression_file = Path(suppression_file)
        self.rate_limit_file = Path(rate_limit_file)
        self.max_daily_sends = max_daily_sends
        self.max_per_domain = max_per_domain
        
        # Load suppression list
        self.suppression_list = self._load_suppression_list()
        
        # Load rate limit data
        self.rate_limits = self._load_rate_limits()
        
    def _load_suppression_list(self) -> Set[str]:
        """Load email addresses that have opted out"""
        if not self.suppression_file.exists():
            self.suppression_file.parent.mkdir(parents=True, exist_ok=True)
            self._save_suppression_list(set())
            return set()
        
        try:
            with open(self.suppression_file, 'r') as f:
                data = json.load(f)
                return set(data.get('suppressed_emails', []))
        except Exception as e:
            print(f"Error loading suppression list: {e}")
            return set()
    
    def _save_suppression_list(self, suppression_list: Set[str]):
        """Save suppression list to file"""
        self.suppression_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.suppression_file, 'w') as f:
            json.dump({
                'suppressed_emails': list(suppression_list),
                'last_updated': datetime.now().isoformat(),
                'count': len(suppression_list)
            }, f, indent=2)
    
    def _load_rate_limits(self) -> Dict:
        """Load rate limit tracking data"""
        if not self.rate_limit_file.exists():
            return {'date': datetime.now().date().isoformat(), 'total_sent': 0, 'domain_counts': {}}
        
        try:
            with open(self.rate_limit_file, 'r') as f:
                data = json.load(f)
                
                # Reset if it's a new day
                if data.get('date') != datetime.now().date().isoformat():
                    return {'date': datetime.now().date().isoformat(), 'total_sent': 0, 'domain_counts': {}}
                
                return data
        except Exception as e:
            print(f"Error loading rate limits: {e}")
            return {'date': datetime.now().date().isoformat(), 'total_sent': 0, 'domain_counts': {}}
    
    def _save_rate_limits(self):
        """Save rate limit tracking data"""
        self.rate_limit_file.parent.mkdir(parents=True, exist_ok=True)
        with open(self.rate_limit_file, 'w') as f:
            json.dump(self.rate_limits, f, indent=2)
    
    def add_to_suppression_list(self, email: str, reason: str = "opt-out"):
        """
        Add email to suppression list
        
        Args:
            email: Email address to suppress
            reason: Reason for suppression (opt-out, bounce, complaint)
        """
        email = email.lower().strip()
        self.suppression_list.add(email)
        self._save_suppression_list(self.suppression_list)
        
        # Log the suppression
        log_file = self.suppression_file.parent / "suppression_log.jsonl"
        with open(log_file, 'a') as f:
            json.dump({
                'email': email,
                'reason': reason,
                'timestamp': datetime.now().isoformat()
            }, f)
            f.write('\n')
        
        print(f"Added {email} to suppression list (reason: {reason})")
    
    def is_suppressed(self, email: str) -> bool:
        """Check if email is on suppression list"""
        return email.lower().strip() in self.suppression_list
    
    def can_send_today(self) -> bool:
        """Check if daily send limit has been reached"""
        return self.rate_limits.get('total_sent', 0) < self.max_daily_sends
    
    def can_send_to_domain(self, email: str) -> bool:
        """Check if domain send limit has been reached"""
        domain = email.split('@')[-1].lower()
        domain_count = self.rate_limits.get('domain_counts', {}).get(domain, 0)
        return domain_count < self.max_per_domain
    
    def record_send(self, email: str):
        """Record that an email was sent (for rate limiting)"""
        domain = email.split('@')[-1].lower()
        
        # Update totals
        self.rate_limits['total_sent'] = self.rate_limits.get('total_sent', 0) + 1
        
        # Update domain counts
        if 'domain_counts' not in self.rate_limits:
            self.rate_limits['domain_counts'] = {}
        
        self.rate_limits['domain_counts'][domain] = \
            self.rate_limits['domain_counts'].get(domain, 0) + 1
        
        self._save_rate_limits()
    
    def validate_contact(self, contact: Dict) -> tuple[bool, str]:
        """
        Validate a single contact for sending
        
        Args:
            contact: Dictionary with contact information
            
        Returns:
            Tuple of (is_valid, reason)
        """
        email = contact.get('email', '').lower().strip()
        
        if not email:
            return False, "No email address"
        
        # Check suppression list
        if self.is_suppressed(email):
            return False, "Email on suppression list"
        
        # Check daily limit
        if not self.can_send_today():
            return False, f"Daily send limit reached ({self.max_daily_sends})"
        
        # Check domain limit
        if not self.can_send_to_domain(email):
            return False, f"Domain send limit reached ({self.max_per_domain})"
        
        # Check for basic email validity
        if '@' not in email or '.' not in email.split('@')[-1]:
            return False, "Invalid email format"
        
        return True, "Valid"
    
    def validate_contacts(self, contacts: List[Dict]) -> Dict:
        """
        Validate a list of contacts
        
        Returns:
            Dictionary with validation results
        """
        valid_contacts = []
        invalid_contacts = []
        
        for contact in contacts:
            is_valid, reason = self.validate_contact(contact)
            
            if is_valid:
                valid_contacts.append(contact)
            else:
                invalid_contacts.append({
                    'contact': contact,
                    'reason': reason
                })
        
        return {
            'valid': valid_contacts,
            'invalid': invalid_contacts,
            'valid_count': len(valid_contacts),
            'invalid_count': len(invalid_contacts),
            'total_count': len(contacts),
            'daily_remaining': self.max_daily_sends - self.rate_limits.get('total_sent', 0)
        }
    
    def get_suppression_stats(self) -> Dict:
        """Get statistics about suppression list"""
        return {
            'total_suppressed': len(self.suppression_list),
            'suppression_file': str(self.suppression_file),
            'last_updated': datetime.now().isoformat()
        }
    
    def get_rate_limit_stats(self) -> Dict:
        """Get statistics about today's sending"""
        return {
            'date': self.rate_limits.get('date'),
            'total_sent': self.rate_limits.get('total_sent', 0),
            'daily_limit': self.max_daily_sends,
            'remaining': self.max_daily_sends - self.rate_limits.get('total_sent', 0),
            'domains': self.rate_limits.get('domain_counts', {}),
            'per_domain_limit': self.max_per_domain
        }


def main():
    """Example usage"""
    # Initialize validator with conservative limits
    validator = ContactValidator(
        max_daily_sends=50,  # Only 50 emails per day
        max_per_domain=5     # Max 5 emails to same domain
    )
    
    # Example: Add some emails to suppression list
    # validator.add_to_suppression_list("noreply@example.com", "bounce")
    
    # Example: Validate contacts
    test_contacts = [
        {'name': 'John Doe', 'email': 'john@example.com', 'domain': 'education'},
        {'name': 'Jane Smith', 'email': 'jane@test.org', 'domain': 'healthcare'},
    ]
    
    results = validator.validate_contacts(test_contacts)
    
    print("Validation Results:")
    print(f"Valid: {results['valid_count']}")
    print(f"Invalid: {results['invalid_count']}")
    print(f"Daily remaining: {results['daily_remaining']}")
    
    print("\nRate Limit Stats:")
    print(json.dumps(validator.get_rate_limit_stats(), indent=2))
    
    print("\nSuppression Stats:")
    print(json.dumps(validator.get_suppression_stats(), indent=2))


if __name__ == "__main__":
    main()
