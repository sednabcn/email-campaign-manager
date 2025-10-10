"""
Enhanced Smart Rate Limiter and Targeting System
Advanced email sending optimization with spam prevention and reputation management
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Set
from collections import defaultdict
import random


class SmartRateLimiter:
    """
    Intelligent rate limiter that prevents spam classification
    
    Features:
    - Multi-tier rate limiting (hourly, daily, per-domain)
    - Adaptive delays based on sending patterns
    - Burst protection with automatic spreading
    - Time-of-day optimization
    - Weekend/holiday awareness
    - Reputation scoring
    """
    
    def __init__(self,
                 tracking_dir: str = "tracking",
                 max_hourly: int = 10,
                 max_daily: int = 50,
                 max_per_domain_hourly: int = 3,
                 max_per_domain_daily: int = 5,
                 min_delay_seconds: int = 30,
                 max_delay_seconds: int = 120,
                 burst_protection: bool = True,
                 time_aware: bool = True,
                 randomize_delays: bool = True):
        """
        Initialize smart rate limiter
        
        Args:
            tracking_dir: Directory for tracking files
            max_hourly: Maximum emails per hour (default: 10)
            max_daily: Maximum emails per day (default: 50)
            max_per_domain_hourly: Max per domain per hour (default: 3)
            max_per_domain_daily: Max per domain per day (default: 5)
            min_delay_seconds: Minimum delay between sends (default: 30)
            max_delay_seconds: Maximum delay between sends (default: 120)
            burst_protection: Enable burst protection (default: True)
            time_aware: Avoid sending at odd hours (default: True)
            randomize_delays: Add randomness to delays (default: True)
        """
        self.tracking_dir = Path(tracking_dir)
        self.tracking_dir.mkdir(exist_ok=True)
        
        # Rate limits
        self.max_hourly = max_hourly
        self.max_daily = max_daily
        self.max_per_domain_hourly = max_per_domain_hourly
        self.max_per_domain_daily = max_per_domain_daily
        self.min_delay = min_delay_seconds
        self.max_delay = max_delay_seconds
        
        # Features
        self.burst_protection = burst_protection
        self.time_aware = time_aware
        self.randomize_delays = randomize_delays
        
        # Files
        self.send_log_file = self.tracking_dir / "send_log.jsonl"
        self.reputation_file = self.tracking_dir / "sender_reputation.json"
        
        # State
        self.last_send_time: Optional[datetime] = None
        self.send_history: List[Dict] = self._load_send_history()
        self.reputation: Dict = self._load_reputation()
        
        print(f"✅ Smart Rate Limiter initialized:")
        print(f"   Hourly limit: {max_hourly} | Daily limit: {max_daily}")
        print(f"   Domain limits: {max_per_domain_hourly}/hr, {max_per_domain_daily}/day")
        print(f"   Delay range: {min_delay_seconds}-{max_delay_seconds}s")
    
    def _load_send_history(self) -> List[Dict]:
        """Load recent send history (last 24 hours)"""
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
                        
                        if record_time > cutoff:
                            history.append(record)
                            
                        # Update last send time
                        if not self.last_send_time or record_time > self.last_send_time:
                            self.last_send_time = record_time
        except Exception as e:
            print(f"⚠️  Warning: Error loading send history: {e}")
        
        return history
    
    def _load_reputation(self) -> Dict:
        """Load sender reputation data"""
        if not self.reputation_file.exists():
            return {
                'score': 100,
                'total_sent': 0,
                'bounces': 0,
                'complaints': 0,
                'successful_sends': 0,
                'last_updated': datetime.now().isoformat()
            }
        
        try:
            with open(self.reputation_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Warning: Error loading reputation: {e}")
            return {'score': 100, 'total_sent': 0}
    
    def _save_reputation(self):
        """Save reputation data"""
        self.reputation['last_updated'] = datetime.now().isoformat()
        with open(self.reputation_file, 'w') as f:
            json.dump(self.reputation, f, indent=2)
    
    def _log_send(self, recipient: str, domain: str, 
                  campaign_id: str, success: bool = True):
        """Log an email send"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'recipient': recipient,
            'domain': domain,
            'campaign_id': campaign_id,
            'success': success
        }
        
        with open(self.send_log_file, 'a') as f:
            json.dump(record, f)
            f.write('\n')
        
        self.send_history.append(record)
        self.last_send_time = datetime.now()
        
        # Update reputation
        self.reputation['total_sent'] = self.reputation.get('total_sent', 0) + 1
        if success:
            self.reputation['successful_sends'] = \
                self.reputation.get('successful_sends', 0) + 1
        
        self._update_reputation_score()
    
    def _update_reputation_score(self):
        """Update sender reputation score (0-100)"""
        total = self.reputation.get('total_sent', 1)
        bounces = self.reputation.get('bounces', 0)
        complaints = self.reputation.get('complaints', 0)
        successful = self.reputation.get('successful_sends', 0)
        
        # Calculate score based on metrics
        bounce_rate = bounces / total if total > 0 else 0
        complaint_rate = complaints / total if total > 0 else 0
        success_rate = successful / total if total > 0 else 1
        
        # Score formula (higher is better)
        score = 100
        score -= (bounce_rate * 50)  # Bounces hurt a lot
        score -= (complaint_rate * 100)  # Complaints hurt even more
        score *= success_rate
        
        self.reputation['score'] = max(0, min(100, score))
        self._save_reputation()
    
    def _count_sends_in_period(self, hours: int = 1) -> int:
        """Count sends in the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        count = sum(1 for record in self.send_history
                   if datetime.fromisoformat(record['timestamp']) > cutoff)
        return count
    
    def _count_domain_sends(self, domain: str, hours: int = 24) -> int:
        """Count sends to a domain in the last N hours"""
        cutoff = datetime.now() - timedelta(hours=hours)
        count = sum(1 for record in self.send_history
                   if record['domain'] == domain 
                   and datetime.fromisoformat(record['timestamp']) > cutoff)
        return count
    
    def _is_good_time_to_send(self) -> Tuple[bool, str]:
        """Check if current time is good for sending emails"""
        if not self.time_aware:
            return True, "Time checking disabled"
        
        now = datetime.now()
        hour = now.hour
        day_of_week = now.weekday()
        
        # Avoid weekends (Saturday=5, Sunday=6)
        if day_of_week >= 5:
            return False, "Weekend - wait until Monday"
        
        # Avoid early morning (before 8 AM)
        if hour < 8:
            next_good_time = now.replace(hour=8, minute=0, second=0)
            wait_seconds = int((next_good_time - now).total_seconds())
            return False, f"Too early - wait until 8 AM ({wait_seconds}s)"
        
        # Avoid late evening (after 8 PM)
        if hour >= 20:
            next_good_time = (now + timedelta(days=1)).replace(hour=8, minute=0, second=0)
            wait_seconds = int((next_good_time - now).total_seconds())
            return False, f"Too late - wait until tomorrow 8 AM ({wait_seconds}s)"
        
        # Avoid lunch hour (12-1 PM) for better engagement
        if 12 <= hour < 13:
            return False, "Lunch hour - better to wait for better engagement"
        
        return True, "Good time to send"
    
    def _calculate_optimal_delay(self, domain: str) -> int:
        """Calculate optimal delay based on current conditions"""
        base_delay = self.min_delay
        
        # Adjust based on hourly rate
        hourly_count = self._count_sends_in_period(hours=1)
        if hourly_count >= self.max_hourly * 0.8:
            # Near limit, slow down
            base_delay = int(base_delay * 1.5)
        
        # Adjust based on domain rate
        domain_hourly = self._count_domain_sends(domain, hours=1)
        if domain_hourly >= self.max_per_domain_hourly * 0.8:
            # Near domain limit, slow down
            base_delay = int(base_delay * 2)
        
        # Adjust based on reputation
        rep_score = self.reputation.get('score', 100)
        if rep_score < 80:
            # Low reputation, be more conservative
            base_delay = int(base_delay * 1.3)
        
        # Add randomness if enabled
        if self.randomize_delays:
            variance = base_delay * 0.2  # ±20%
            base_delay = int(random.uniform(
                base_delay - variance,
                base_delay + variance
            ))
        
        # Ensure within bounds
        return max(self.min_delay, min(self.max_delay, base_delay))
    
    def can_send_now(self, recipient_email: str, 
                    respect_time: bool = True) -> Tuple[bool, str, Optional[int]]:
        """
        Check if we can send an email now
        
        Args:
            recipient_email: Email address to check
            respect_time: Whether to check time-of-day restrictions
            
        Returns:
            Tuple of (can_send, reason, wait_seconds)
        """
        domain = recipient_email.split('@')[-1].lower()
        
        # Check time-of-day restrictions
        if respect_time:
            good_time, time_reason = self._is_good_time_to_send()
            if not good_time:
                # Extract wait time if present
                wait_match = time_reason.split('(')
                if len(wait_match) > 1:
                    wait_str = wait_match[1].replace('s)', '')
                    return False, time_reason, int(wait_str)
                return False, time_reason, None
        
        # Check daily limit
        daily_count = self._count_sends_in_period(hours=24)
        if daily_count >= self.max_daily:
            return False, f"Daily limit reached ({self.max_daily})", None
        
        # Check hourly limit
        hourly_count = self._count_sends_in_period(hours=1)
        if hourly_count >= self.max_hourly:
            # Find oldest send in current hour to calculate wait time
            hour_ago = datetime.now() - timedelta(hours=1)
            oldest_in_hour = min([
                datetime.fromisoformat(r['timestamp'])
                for r in self.send_history
                if datetime.fromisoformat(r['timestamp']) > hour_ago
            ])
            wait_until = oldest_in_hour + timedelta(hours=1)
            wait_seconds = int((wait_until - datetime.now()).total_seconds())
            return False, f"Hourly limit reached ({self.max_hourly})", wait_seconds
        
        # Check per-domain hourly limit
        domain_hourly = self._count_domain_sends(domain, hours=1)
        if domain_hourly >= self.max_per_domain_hourly:
            return False, f"Domain hourly limit for {domain} ({self.max_per_domain_hourly})", None
        
        # Check per-domain daily limit
        domain_daily = self._count_domain_sends(domain, hours=24)
        if domain_daily >= self.max_per_domain_daily:
            return False, f"Domain daily limit for {domain} ({self.max_per_domain_daily})", None
        
        # Check minimum delay
        if self.last_send_time:
            time_since_last = (datetime.now() - self.last_send_time).total_seconds()
            optimal_delay = self._calculate_optimal_delay(domain)
            
            if time_since_last < optimal_delay:
                wait_seconds = int(optimal_delay - time_since_last) + 1
                return False, f"Minimum delay ({optimal_delay}s)", wait_seconds
        
        return True, "OK", 0
    
    def wait_if_needed(self, recipient_email: str, 
                      max_wait: int = 3600,
                      respect_time: bool = True) -> bool:
        """
        Wait if necessary before sending
        
        Args:
            recipient_email: Email to send to
            max_wait: Maximum seconds to wait (default: 1 hour)
            respect_time: Whether to respect time-of-day restrictions
            
        Returns:
            True if ready to send, False if exceeded max_wait
        """
        can_send, reason, wait_seconds = self.can_send_now(
            recipient_email, respect_time=respect_time
        )
        
        if can_send:
            return True
        
        if wait_seconds is None or wait_seconds > max_wait:
            print(f"❌ Cannot send: {reason}")
            return False
        
        if wait_seconds > 0:
            print(f"⏱️  Waiting {wait_seconds}s ({reason})...")
            
            # Show progress for long waits
            if wait_seconds > 60:
                for remaining in range(wait_seconds, 0, -30):
                    time.sleep(min(30, remaining))
                    if remaining > 30:
                        print(f"   {remaining - 30}s remaining...")
            else:
                time.sleep(wait_seconds)
            
            return True
        
        return False
    
    def record_send(self, recipient: str, campaign_id: str = "general",
                   success: bool = True):
        """
        Record that an email was sent
        
        Args:
            recipient: Email address
            campaign_id: Campaign identifier
            success: Whether send was successful
        """
        domain = recipient.split('@')[-1].lower()
        self._log_send(recipient, domain, campaign_id, success)
    
    def record_bounce(self, recipient: str):
        """Record a bounced email"""
        self.reputation['bounces'] = self.reputation.get('bounces', 0) + 1
        self._update_reputation_score()
        print(f"📛 Bounce recorded for {recipient}")
    
    def record_complaint(self, recipient: str):
        """Record a spam complaint"""
        self.reputation['complaints'] = self.reputation.get('complaints', 0) + 1
        self._update_reputation_score()
        print(f"⚠️  Complaint recorded for {recipient}")
    
    def get_stats(self) -> Dict:
        """Get comprehensive sending statistics"""
        hourly = self._count_sends_in_period(hours=1)
        daily = self._count_sends_in_period(hours=24)
        
        # Count per domain
        domain_counts = defaultdict(int)
        hour_ago = datetime.now() - timedelta(hours=1)
        today = datetime.now().date()
        
        for record in self.send_history:
            record_time = datetime.fromisoformat(record['timestamp'])
            domain = record['domain']
            
            if record_time.date() == today:
                domain_counts[domain] += 1
        
        return {
            'hourly': {
                'sent': hourly,
                'limit': self.max_hourly,
                'remaining': max(0, self.max_hourly - hourly),
                'utilization': f"{(hourly/self.max_hourly*100):.1f}%"
            },
            'daily': {
                'sent': daily,
                'limit': self.max_daily,
                'remaining': max(0, self.max_daily - daily),
                'utilization': f"{(daily/self.max_daily*100):.1f}%"
            },
            'domains': {
                'contacted_today': len(domain_counts),
                'top_domains': dict(sorted(domain_counts.items(), 
                                         key=lambda x: x[1], reverse=True)[:5])
            },
            'reputation': {
                'score': self.reputation.get('score', 100),
                'total_sent': self.reputation.get('total_sent', 0),
                'bounce_rate': f"{(self.reputation.get('bounces', 0) / max(1, self.reputation.get('total_sent', 1)) * 100):.2f}%"
            },
            'timing': {
                'last_send': self.last_send_time.isoformat() if self.last_send_time else None,
                'good_time_to_send': self._is_good_time_to_send()[0]
            }
        }
    
    def suggest_schedule(self, total_emails: int, 
                        target_domain_counts: Optional[Dict[str, int]] = None) -> Dict:
        """
        Suggest optimal sending schedule
        
        Args:
            total_emails: Number of emails to send
            target_domain_counts: Optional dict of {domain: count}
            
        Returns:
            Suggested schedule with timing
        """
        # Calculate days needed
        emails_remaining_today = max(0, self.max_daily - 
                                     self._count_sends_in_period(hours=24))
        
        if total_emails <= emails_remaining_today:
            # Can send all today
            optimal_delay = self._calculate_optimal_delay("generic")
            estimated_time = total_emails * optimal_delay
            
            # Check if we have enough time today
            now = datetime.now()
            cutoff_time = now.replace(hour=20, minute=0, second=0)
            seconds_until_cutoff = (cutoff_time - now).total_seconds()
            
            can_finish_today = estimated_time <= seconds_until_cutoff
            
            return {
                'can_finish_today': can_finish_today,
                'emails_today': total_emails if can_finish_today else 
                               int(seconds_until_cutoff / optimal_delay),
                'emails_tomorrow': 0 if can_finish_today else 
                                  total_emails - int(seconds_until_cutoff / optimal_delay),
                'optimal_delay_seconds': optimal_delay,
                'estimated_completion_minutes': int(estimated_time / 60),
                'start_immediately': self._is_good_time_to_send()[0],
                'recommendation': self._generate_recommendation(
                    total_emails, can_finish_today, optimal_delay
                )
            }
        else:
            # Need multiple days
            days_needed = (total_emails + self.max_daily - 1) // self.max_daily
            emails_per_day = self.max_daily
            optimal_delay = self._calculate_optimal_delay("generic")
            
            return {
                'can_finish_today': False,
                'days_needed': days_needed,
                'emails_per_day': emails_per_day,
                'optimal_delay_seconds': optimal_delay,
                'estimated_completion_days': days_needed,
                'start_immediately': self._is_good_time_to_send()[0],
                'recommendation': f"Split across {days_needed} days: {emails_per_day} emails/day with {optimal_delay}s delays"
            }
    
    def _generate_recommendation(self, total: int, can_finish: bool, 
                                delay: int) -> str:
        """Generate human-readable recommendation"""
        if can_finish:
            time_est = (total * delay) / 60
            return f"Send all {total} emails today (~{time_est:.0f} minutes with {delay}s delays)"
        else:
            return f"Send remaining emails today, continue tomorrow with {delay}s delays"


class TargetingOptimizer:
    """
    Intelligent contact targeting to avoid annoying people
    
    Features:
    - Contact frequency management
    - Campaign deduplication
    - Response tracking
    - Engagement scoring
    - Automatic suppression of unresponsive contacts
    """
    
    def __init__(self, 
                 tracking_dir: str = "tracking",
                 min_days_between_contacts: int = 90,
                 max_lifetime_contacts: int = 3):
        """
        Initialize targeting optimizer
        
        Args:
            tracking_dir: Directory for tracking files
            min_days_between_contacts: Minimum days between contacts (default: 90)
            max_lifetime_contacts: Maximum times to contact someone ever (default: 3)
        """
        self.tracking_dir = Path(tracking_dir)
        self.tracking_dir.mkdir(exist_ok=True)
        
        self.min_days_between = min_days_between_contacts
        self.max_lifetime_contacts = max_lifetime_contacts
        
        self.contact_history_file = self.tracking_dir / "contact_history.json"
        self.engagement_file = self.tracking_dir / "engagement_scores.json"
        
        self.contact_history: Dict = self._load_contact_history()
        self.engagement_scores: Dict = self._load_engagement_scores()
        
        print(f"✅ Targeting Optimizer initialized:")
        print(f"   Min days between contacts: {min_days_between_contacts}")
        print(f"   Max lifetime contacts: {max_lifetime_contacts}")
        print(f"   Known contacts: {len(self.contact_history)}")
    
    def _load_contact_history(self) -> Dict:
        """Load contact history"""
        if not self.contact_history_file.exists():
            return {}
        
        try:
            with open(self.contact_history_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Warning: Error loading contact history: {e}")
            return {}
    
    def _save_contact_history(self):
        """Save contact history"""
        with open(self.contact_history_file, 'w') as f:
            json.dump(self.contact_history, f, indent=2)
    
    def _load_engagement_scores(self) -> Dict:
        """Load engagement scores"""
        if not self.engagement_file.exists():
            return {}
        
        try:
            with open(self.engagement_file, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"⚠️  Warning: Error loading engagement scores: {e}")
            return {}
    
    def _save_engagement_scores(self):
        """Save engagement scores"""
        with open(self.engagement_file, 'w') as f:
            json.dump(self.engagement_scores, f, indent=2)
    
    def _calculate_engagement_score(self, email: str) -> int:
        """
        Calculate engagement score (0-100)
        Higher score = more engaged
        """
        if email not in self.contact_history:
            return 50  # Neutral for new contacts
        
        history = self.contact_history[email]
        score = 50
        
        # Positive signals
        if history.get('replied', False):
            score += 30
        if history.get('interested', False):
            score += 50
        if history.get('clicked_links', 0) > 0:
            score += 20
        
        # Negative signals
        if history.get('opted_out', False):
            score = 0
        if history.get('bounced', False):
            score = 0
        if history.get('not_interested', False):
            score -= 40
        if history.get('contact_count', 0) > 0 and not history.get('replied', False):
            # Contacted but never replied - decrease score
            score -= (history.get('contact_count', 0) * 10)
        
        return max(0, min(100, score))
    
    def should_contact(self, email: str, campaign_id: str) -> Tuple[bool, str]:
        """
        Determine if we should contact this person
        
        Args:
            email: Email address
            campaign_id: Campaign identifier
            
        Returns:
            Tuple of (should_contact, reason)
        """
        email = email.lower().strip()
        
        # Check if new contact
        if email not in self.contact_history:
            return True, "New contact"
        
        history = self.contact_history[email]
        
        # Hard stops
        if history.get('opted_out', False):
            return False, "Previously opted out"
        
        if history.get('bounced', False):
            return False, "Previous bounce"
        
        if history.get('spam_complaint', False):
            return False, "Previous spam complaint"
        
        # Check if already contacted for this campaign
        if campaign_id in history.get('campaigns', []):
            return False, f"Already contacted for '{campaign_id}'"
        
        # Check lifetime contact limit
        contact_count = history.get('contact_count', 0)
        if contact_count >= self.max_lifetime_contacts:
            return False, f"Reached max lifetime contacts ({self.max_lifetime_contacts})"
        
        # Check last contact date
        last_contact = history.get('last_contact')
        if last_contact:
            last_date = datetime.fromisoformat(last_contact)
            days_since = (datetime.now() - last_date).days
            
            if days_since < self.min_days_between:
                return False, f"Too soon (last contact {days_since} days ago, min {self.min_days_between})"
        
        # Check engagement score
        engagement = self._calculate_engagement_score(email)
        self.engagement_scores[email] = engagement
        
        if engagement < 20 and contact_count > 0:
            return False, f"Low engagement score ({engagement}/100)"
        
        return True, f"OK to contact (engagement: {engagement}/100)"
    
    def record_contact(self, email: str, campaign_id: str):
        """Record that we contacted someone"""
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
        
        self._save_contact_history()
    
    def record_response(self, email: str, response_type: str):
        """
        Record a response from a contact
        
        Args:
            email: Email address
            response_type: Type of response (replied, interested, not_interested, 
                          clicked_link, bounced, opted_out, spam_complaint)
        """
        email = email.lower().strip()
        
        if email not in self.contact_history:
            self.contact_history[email] = {}
        
        history = self.contact_history[email]
        
        if response_type == "replied":
            history['replied'] = True
            history['last_reply'] = datetime.now().isoformat()
        elif response_type == "interested":
            history['interested'] = True
            history['replied'] = True
        elif response_type == "not_interested":
            history['not_interested'] = True
        elif response_type == "clicked_link":
            history['clicked_links'] = history.get('clicked_links', 0) + 1
        elif response_type == "bounced":
            history['bounced'] = True
        elif response_type == "opted_out":
            history['opted_out'] = True
        elif response_type == "spam_complaint":
            history['spam_complaint'] = True
        
        self._save_contact_history()
        
        # Update engagement score
        self.engagement_scores[email] = self._calculate_engagement_score(email)
        self._save_engagement_scores()
    
    def filter_contacts(self, contacts: List[Dict], 
                       campaign_id: str,
                       min_engagement: int = 0) -> Dict:
        """
        Filter contacts based on targeting rules
        
        Args:
            contacts: List of contact dictionaries with 'email' key
            campaign_id: Campaign identifier
            min_engagement: Minimum engagement score (0-100)
            
        Returns:
            Dictionary with filtered results
        """
        targeted = []
        skipped = []
        
        for contact in contacts:
            email = contact.get('email', '').lower().strip()
            
            if not email:
                skipped.append({
                    'contact': contact,
                    'reason': 'No email address'
                })
                continue
            
            # Check targeting rules
            should_contact, reason = self.should_contact(email, campaign_id)
            
            if not should_contact:
                skipped.append({
                    'contact': contact,
                    'reason': reason
                })
                continue
            
            # Check engagement threshold
            engagement = self._calculate_engagement_score(email)
            if engagement < min_engagement:
                skipped.append({
                    'contact': contact,
                    'reason': f'Engagement too low ({engagement}/{min_engagement})'
                })
                continue
            
            # Add to targeted list with engagement score
            contact_with_score = contact.copy()
            contact_with_score['engagement_score'] = engagement
            targeted.append(contact_with_score)
        
        return {
            'targeted': targeted,
            'skipped': skipped,
            'stats': {
                'total': len(contacts),
                'targeted': len(targeted),
                'skipped': len(skipped),
                'targeting_rate': f"{(len(targeted)/max(1, len(contacts))*100):.1f}%"
            }
        }
    
    def get_contact_stats(self, email: str) -> Dict:
        """Get statistics for a specific contact"""
        email = email.lower().strip()
        
        if email not in self.contact_history:
            return {
                'status': 'new',
                'engagement_score': 50,
                'can_contact': True
            }
        
        history = self.contact_history[email]
        engagement = self._calculate_engagement_score(email)
        
        return {
            'status': 'known',
            'first_contact': history.get('first_contact'),
            'last_contact': history.get('last_contact'),
            'contact_count': history.get('contact_count', 0),
            'campaigns': history.get('campaigns', []),
            'engagement_score': engagement,
            'replied': history.get('replied', False),
            'interested': history.get('interested', False),
            'opted_out': history.get('opted_out', False),
            'bounced': history.get('bounced', False),
            'can_contact': self.should_contact(email, "test_campaign")[0]
        }
    
    def get_summary(self) -> Dict:
        """Get summary of all contacts"""
        total = len(self.contact_history)
        
        if total == 0:
            return {
                'total_contacts': 0,
                'contactable': 0,
                'opted_out': 0,
                'bounced': 0,
                'engaged': 0
            }
        
        opted_out = sum(1 for h in self.contact_history.values() 
                       if h.get('opted_out', False))
        bounced = sum(1 for h in self.contact_history.values() 
                     if h.get('bounced', False))
        replied = sum(1 for h in self.contact_history.values() 
                     if h.get('replied', False))
        interested = sum(1 for h in self.contact_history.values() 
                        if h.get('interested', False))
        
        # Count contactable
        contactable = sum(1 for email in self.contact_history.keys()
                         if self.should_contact(email, "test_campaign")[0])
        
        return {
            'total_contacts': total,
            'contactable': contactable,
            'opted_out': opted_out,
            'bounced': bounced,
            'replied': replied,
            'interested': interested,
            'engagement': {
                'reply_rate': f"{(replied/total*100):.1f}%",
                'interest_rate': f"{(interested/total*100):.1f}%",
                'avg_score': sum(self._calculate_engagement_score(e) 
                               for e in self.contact_history.keys()) / total
            }
        }


# Example usage
if __name__ == "__main__":
    print("=== Smart Rate Limiter & Targeting System ===\n")
    
    # Initialize rate limiter
    limiter = SmartRateLimiter(
        max_hourly=10,
        max_daily=50,
        min_delay_seconds=30,
        max_delay_seconds=120
    )
    
    print("\nRate Limiter Stats:")
    stats = limiter.get_stats()
    print(f"Hourly: {stats['hourly']['sent']}/{stats['hourly']['limit']} "
          f"({stats['hourly']['utilization']})")
    print(f"Daily: {stats['daily']['sent']}/{stats['daily']['limit']} "
          f"({stats['daily']['utilization']})")
    print(f"Reputation Score: {stats['reputation']['score']}/100")
    
    # Initialize targeting optimizer
    optimizer = TargetingOptimizer(
        min_days_between_contacts=90,
        max_lifetime_contacts=3
    )
    
    print("\nTargeting Optimizer Stats:")
    summary = optimizer.get_summary()
    print(f"Total Contacts: {summary['total_contacts']}")
    print(f"Contactable: {summary['contactable']}")
    
    # Example: Check if can send
    test_email = "test@example.com"
    can_send, reason, wait = limiter.can_send_now(test_email)
    print(f"\nCan send to {test_email}? {can_send}")
    print(f"Reason: {reason}")
    
    # Example: Check targeting
    should_contact, targeting_reason = optimizer.should_contact(
        test_email, 
        "test_campaign"
    )
    print(f"\nShould contact {test_email}? {should_contact}")
    print(f"Reason: {targeting_reason}")
    
    # Example: Suggest schedule for 100 emails
    print("\n=== Schedule Suggestion for 100 Emails ===")
    schedule = limiter.suggest_schedule(100)
    print(f"Can finish today: {schedule['can_finish_today']}")
    print(f"Recommendation: {schedule['recommendation']}")
