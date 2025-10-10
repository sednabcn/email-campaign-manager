"""
Smart Rate Limiter and Targeting System
Prevents spam classification and ensures respectful sending patterns
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional
from collections import defaultdict

class SmartRateLimiter:
    def __init__(self,
                 tracking_dir: str = "tracking",
                 max_hourly: int = 10,
                 max_daily: int = 50,
                 max_per_domain_daily: int = 5,
                 min_delay_seconds: int = 30,
                 burst_protection: bool = True):
        """
        Initialize smart rate limiter with conservative defaults
        
        Args:
            tracking_dir: Directory for tracking files
            max_hourly: Maximum emails per hour
            max_daily: Maximum emails per day
            max_per_domain_daily: Maximum per domain per day
            min_delay_seconds: Minimum seconds between emails
            burst_protection: Enable burst protection (spreading sends)
        """
        self.tracking_dir = Path(tracking_dir)
        self.tracking_dir.mkdir(exist_ok=True)
        
        self.max_hourly = max_hourly
        self.max_daily = max_daily
        self.max_per_domain_daily = max_per_domain_daily
        self.min_delay_seconds = min_delay_seconds
        self.burst_protection = burst_protection
        
        self.send_log_file = self.tracking_dir / "send_log.jsonl"
        self.last_send_time = None
        
        # Load recent send history
        self.send_history = self._load_send_history()
    
    def _load_send_history(self) -> List[Dict]:
        """Load recent send history from log"""
        if not self.send_log_file.exists():
            return []
        
        history = []
        cutoff = datetime.now() - timedelta(days=1)
        
        try:
            with open(self.send_log_file, 'r') as f:
                for line in f:
                    if line.strip():
                        record = json.loads(line)
                        record_time = datetime.fromisoformat(record['timestamp'])
                        
                        # Only keep recent records
                        if record_time > cutoff:
                            history.append(record)
        except Exception as e:
            print(f"Error loading send history: {e}")
        
        return history
    
    def _log_send(self, recipient: str, domain: str, campaign_id: str):
        """Log an email send"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'recipient': recipient,
            'domain': domain,
            'campaign_id': campaign_id
        }
        
        with open(self.send_log_file, 'a') as f:
            json.dump(record, f)
            f.write('\n')
        
        self.send_history.append(record)
        self.last_send_time = datetime.now()
    
    def _count_sends_in_period(self, hours: int = 1) -> int:
        """Count sends in the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        count = 0
        
        for record in self.send_history:
            record_time = datetime.fromisoformat(record['timestamp'])
            if record_time > cutoff:
                count += 1
        
        return count
    
    def _count_domain_sends_today(self, domain: str) -> int:
        """Count sends to a domain today"""
        today = datetime.now().date()
        count = 0
        
        for record in self.send_history:
            record_time = datetime.fromisoformat(record['timestamp'])
            if record_time.date() == today and record['domain'] == domain:
                count += 1
        
        return count
    
    def can_send_now(self, recipient_email: str) -> tuple[bool, str, Optional[int]]:
        """
        Check if we can send an email now
        
        Args:
            recipient_email: Email address to check
            
        Returns:
            Tuple of (can_send, reason, wait_seconds)
        """
        domain = recipient_email.split('@')[-1].lower()
        
        # Check daily limit
        daily_count = self._count_sends_in_period(hours=24)
        if daily_count >= self.max_daily:
            return False, f"Daily limit reached ({self.max_daily})", None
        
        # Check hourly limit
        hourly_count = self._count_sends_in_period(hours=1)
        if hourly_count >= self.max_hourly:
            # Calculate wait time
            oldest_in_hour = min([
                datetime.fromisoformat(r['timestamp'])
                for r in self.send_history
                if datetime.fromisoformat(r['timestamp']) > datetime.now() - timedelta(hours=1)
            ])
            wait_until = oldest_in_hour + timedelta(hours=1)
            wait_seconds = int((wait_until - datetime.now()).total_seconds())
            return False, f"Hourly limit reached ({self.max_hourly})", wait_seconds
        
        # Check per-domain limit
        domain_count = self._count_domain_sends_today(domain)
        if domain_count >= self.max_per_domain_daily:
            return False, f"Domain limit reached for {domain} ({self.max_per_domain_daily})", None
        
        # Check minimum delay
        if self.last_send_time:
            time_since_last = (datetime.now() - self.last_send_time).total_seconds()
            if time_since_last < self.min_delay_seconds:
                wait_seconds = int(self.min_delay_seconds - time_since_last)
                return False, f"Minimum delay not met ({self.min_delay_seconds}s)", wait_seconds
        
        return True, "OK", 0
    
    def wait_if_needed(self, recipient_email: str, max_wait: int = 300) -> bool:
        """
        Wait if necessary before sending
        
        Args:
            recipient_email: Email to send to
            max_wait: Maximum seconds to wait
            
        Returns:
            True if ready to send, False if exceeded max_wait
        """
        can_send, reason, wait_seconds = self.can_send_now(recipient_email)
        
        if can_send:
            return True
        
        if wait_seconds is None or wait_seconds > max_wait:
            print(f"Cannot send: {reason}")
            return False
        
        if wait_seconds > 0:
            print(f"Waiting {wait_seconds}s ({reason})...")
            time.sleep(wait_seconds)
            return True
        
        return False
    
    def record_send(self, recipient: str, campaign_id: str = "general"):
        """Record that an email was sent"""
        domain = recipient.split('@')[-1].lower()
        self._log_send(recipient, domain, campaign_id)
    
    def get_sending_stats(self) -> Dict:
        """Get current sending statistics"""
        hourly = self._count_sends_in_period(hours=1)
        daily = self._count_sends_in_period(hours=24)
        
        # Count per domain
        domain_counts = defaultdict(int)
        today = datetime.now().date()
        for record in self.send_history:
            record_time = datetime.fromisoformat(record['timestamp'])
            if record_time.date() == today:
                domain_counts[record['domain']] += 1
        
        return {
            'hourly_sent': hourly,
            'hourly_limit': self.max_hourly,
            'hourly_remaining': max(0, self.max_hourly - hourly),
            'daily_sent': daily,
            'daily_limit': self.max_daily,
            'daily_remaining': max(0, self.max_daily - daily),
            'domains_contacted_today': len(domain_counts),
            'domain_counts': dict(domain_counts),
            'min_delay': self.min_delay_seconds,
            'last_send': self.last_send_time.isoformat() if self.last_send_time else None
        }
    
    def suggest_optimal_schedule(self, total_emails: int) -> Dict:
        """
        Suggest optimal sending schedule for a batch
        
        Args:
            total_emails: Number of emails to send
            
        Returns:
            Suggested schedule
        """
        # Calculate how many days needed
        days_needed = (total_emails + self.max_daily - 1) // self.max_daily
        
        # Calculate optimal delay between emails
        if total_emails <= self.max_daily:
            # Can send all today
            optimal_delay = max(
                self.min_delay_seconds,
                3600 // min(total_emails, self.max_hourly)  # Spread across hour
            )
            
            estimated_time = total_emails * optimal_delay
            
            return {
                'can_send_today': True,
                'days_needed': 1,
                'emails_per_day': total_emails,
                'optimal_delay_seconds': optimal_delay,
                'estimated_completion_hours': estimated_time / 3600,
                'recommendation': f"Send {total_emails} emails with {optimal_delay}s delay"
            }
        else:
            # Need multiple days
            emails_per_day = self.max_daily
            optimal_delay = max(
                self.min_delay_seconds,
                3600 // min(emails_per_day, self.max_hourly)
            )
            
            return {
                'can_send_today': False,
                'days_needed': days_needed,
                'emails_per_day': emails_per_day,
                'optimal_delay_seconds': optimal_delay,
                'estimated_completion_hours': (emails_per_day * optimal_delay * days_needed) / 3600,
                'recommendation': f"Split into {days_needed} days, {emails_per_day} per day with {optimal_delay}s delay"
            }


class TargetingOptimizer:
    """Optimize recipient targeting to avoid annoying people"""
    
    def __init__(self, tracking_dir: str = "tracking"):
        self.tracking_dir = Path(tracking_dir)
        self.tracking_dir.mkdir(exist_ok=True)
        self.contact_history_file = self.tracking_dir / "contact_history.json"
        self.contact_history = self._load_contact_history()
    
    def _load_contact_history(self) -> Dict:
        """Load history of contacts"""
        if not self.contact_history_file.exists():
            return {}
        
        try:
            with open(self.contact_history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading contact history: {e}")
            return {}
    
    def _save_contact_history(self):
        """Save contact history"""
        with open(self.contact_history_file, 'w') as f:
            json.dump(self.contact_history, f, indent=2)
    
    def should_contact(self, email: str, campaign_id: str, 
                      min_days_between: int = 90) -> tuple[bool, str]:
        """
        Determine if we should contact this person
        
        Args:
            email: Email address
            campaign_id: Campaign identifier
            min_days_between: Minimum days between contacts
            
        Returns:
            Tuple of (should_contact, reason)
        """
        email = email.lower().strip()
        
        if email not in self.contact_history:
            return True, "New contact"
        
        history = self.contact_history[email]
        
        # Check if already contacted for this campaign
        if campaign_id in history.get('campaigns', []):
            return False, f"Already contacted for {campaign_id}"
        
        # Check last contact date
        last_contact = history.get('last_contact')
        if last_contact:
            last_date = datetime.fromisoformat(last_contact)
            days_since = (datetime.now() - last_date).days
            
            if days_since < min_days_between:
                return False, f"Recently contacted ({days_since} days ago, min {min_days_between})"
        
        # Check if they responded negatively
        if history.get('opted_out', False):
            return False, "Previously opted out"
        
        if history.get('bounced', False):
            return False, "Previous bounce"
        
        return True, "OK to contact"
    
    def record_contact(self, email: str, campaign_id: str, 
                      result: str = "sent"):
        """
        Record that we contacted someone
        
        Args:
            email: Email address
            campaign_id: Campaign identifier
            result: Result (sent, bounced, opted_out)
        """
        email = email.lower().strip()
        
        if email not in self.contact_history:
            self.contact_history[email] = {
                'first_contact': datetime.now().isoformat(),
                'campaigns': [],
                'contact_count': 0
            }
        
        history = self.contact_history[email]
        history['last_contact'] = datetime.now().isoformat()
        history['contact_count'] = history.get('contact_count', 0) + 1
        
        if campaign_id not in history.get('campaigns', []):
            if 'campaigns' not in history:
                history['campaigns'] = []
            history['campaigns'].append(campaign_id)
        
        if result == "bounced":
            history['bounced'] = True
        elif result == "opted_out":
            history['opted_out'] = True
        
        self._save_contact_history()
    
    def get_contact_stats(self, email: str) -> Optional[Dict]:
        """Get statistics for a contact"""
        email = email.lower().strip()
        return self.contact_history.get(email)
    
    def filter_contacts(self, contacts: List[Dict], 
                       campaign_id: str) -> Dict:
        """
        Filter contacts based on targeting rules
        
        Args:
            contacts: List of contact dictionaries
            campaign_id: Campaign identifier
            
        Returns:
            Dictionary with filtered results
        """
        targeted = []
        skipped = []
        
        for contact in contacts:
            email = contact.get('email', '').lower().strip()
            should_contact, reason = self.should_contact(email, campaign_id)
            
            if should_contact:
                targeted.append(contact)
            else:
                skipped.append({
                    'contact': contact,
                    'reason': reason
                })
        
        return {
            'targeted': targeted,
            'skipped': skipped,
            'targeted_count': len(targeted),
            'skipped_count': len(skipped),
            'total_count': len(contacts)
        }


def main():
    """Example usage"""
    print("Smart Rate Limiter Example")
    print("=" * 50)
    
    # Initialize rate limiter with conservative settings
    limiter = SmartRateLimiter(
        max_hourly=10,
        max_daily=50,
        max_per_domain_daily=5,
        min_delay_seconds=30
    )
    
    # Get current stats
    stats = limiter.get_sending_stats()
    print("\nCurrent Stats:")
    print(json.dumps(stats, indent=2))
    
    # Get schedule suggestion
    schedule = limiter.suggest_optimal_schedule(75)
    print("\nSchedule for 75 emails:")
    print(json.dumps(schedule, indent=2))
    
    print("\n" + "=" * 50)
    print("Targeting Optimizer Example")
    print("=" * 50)
    
    # Initialize targeting optimizer
    optimizer = TargetingOptimizer()
    
    # Example contacts
    test_contacts = [
        {'name': 'John Doe', 'email': 'john@example.com'},
        {'name': 'Jane Smith', 'email': 'jane@test.org'},
    ]
    
    # Filter contacts
    results = optimizer.filter_contacts(test_contacts, 'education_outreach')
    print("\nTargeting Results:")
    print(f"Targeted: {results['targeted_count']}")
    print(f"Skipped: {results['skipped_count']}")


if __name__ == "__main__":
    main()
