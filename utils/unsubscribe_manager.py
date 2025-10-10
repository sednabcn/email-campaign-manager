"""
Production-Ready Email Unsubscribe System
Improved security, persistence, and compliance features
"""

import hashlib
import base64
import json
import secrets
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Set
from urllib.parse import urlencode, quote
import threading


class UnsubscribeManager:
    """Manages unsubscribe requests with thread-safe operations"""
    
    def __init__(self, 
                 tracking_dir: Path,
                 base_url: str,
                 secret_key: Optional[str] = None):
        """
        Initialize unsubscribe manager
        
        Args:
            tracking_dir: Directory for storing unsubscribe data
            base_url: Base URL for unsubscribe page
            secret_key: Secret key for token generation (auto-generated if None)
        """
        self.tracking_dir = Path(tracking_dir)
        self.tracking_dir.mkdir(parents=True, exist_ok=True)
        
        self.unsub_file = self.tracking_dir / "unsubscribed.json"
        self.base_url = base_url.rstrip('/')
        
        # Generate or load secret key
        self.secret_key = secret_key or self._load_or_create_secret()
        
        # Thread safety
        self._lock = threading.RLock()
        
        # Cache for performance
        self._cache: Dict[str, Dict] = {}
        self._cache_loaded = False
        
    def _load_or_create_secret(self) -> str:
        """Load existing secret or create new one"""
        secret_file = self.tracking_dir / ".secret_key"
        
        if secret_file.exists():
            return secret_file.read_text().strip()
        
        # Generate cryptographically secure secret
        secret = secrets.token_urlsafe(32)
        secret_file.write_text(secret)
        secret_file.chmod(0o600)  # Restrict permissions
        return secret
    
    def _load_unsubscribed(self) -> Dict[str, Dict]:
        """Load unsubscribe data from file"""
        with self._lock:
            if self._cache_loaded:
                return self._cache.copy()
            
            if not self.unsub_file.exists():
                self._cache = {}
                self._cache_loaded = True
                return {}
            
            try:
                with open(self.unsub_file, 'r') as f:
                    data = json.load(f)
                    self._cache = data
                    self._cache_loaded = True
                    return data.copy()
            except (json.JSONDecodeError, IOError) as e:
                print(f"Warning: Could not load unsubscribe data: {e}")
                return {}
    
    def _save_unsubscribed(self, data: Dict[str, Dict]) -> bool:
        """Save unsubscribe data to file"""
        with self._lock:
            try:
                # Write to temp file first (atomic operation)
                temp_file = self.unsub_file.with_suffix('.tmp')
                with open(temp_file, 'w') as f:
                    json.dump(data, f, indent=2, sort_keys=True)
                
                # Atomic rename
                temp_file.replace(self.unsub_file)
                
                # Update cache
                self._cache = data.copy()
                self._cache_loaded = True
                return True
            except IOError as e:
                print(f"Error saving unsubscribe data: {e}")
                return False
    
    def _generate_secure_token(self, email: str, campaign_id: str) -> str:
        """Generate cryptographically secure token"""
        # Use HMAC-like approach
        data = f"{email.lower()}:{campaign_id}:{self.secret_key}"
        token = hashlib.sha256(data.encode()).hexdigest()[:24]
        
        # Create payload
        payload = {
            'e': base64.urlsafe_b64encode(email.lower().encode()).decode(),
            'c': campaign_id,
            't': token,
            'exp': (datetime.now() + timedelta(days=90)).isoformat()
        }
        
        return base64.urlsafe_b64encode(json.dumps(payload).encode()).decode()
    
    def _verify_token(self, token: str) -> Optional[Dict]:
        """Verify and decode token"""
        try:
            # Decode payload
            payload_json = base64.urlsafe_b64decode(token.encode()).decode()
            payload = json.loads(payload_json)
            
            # Check expiration
            exp_date = datetime.fromisoformat(payload['exp'])
            if datetime.now() > exp_date:
                return None
            
            # Decode email
            email = base64.urlsafe_b64decode(payload['e'].encode()).decode()
            
            # Verify token
            expected_token = self._generate_secure_token(email, payload['c'])
            expected_payload = json.loads(
                base64.urlsafe_b64decode(expected_token.encode()).decode()
            )
            
            if payload['t'] != expected_payload['t']:
                return None
            
            return {'email': email, 'campaign': payload['c']}
            
        except (ValueError, KeyError, json.JSONDecodeError):
            return None
    
    def generate_unsubscribe_link(self, 
                                  email: str, 
                                  campaign_id: str = "all",
                                  include_email: bool = False) -> str:
        """
        Generate unsubscribe link with secure token
        
        Args:
            email: Recipient email
            campaign_id: Campaign identifier
            include_email: Include plain email in URL (less secure but simpler)
            
        Returns:
            Full unsubscribe URL
        """
        token = self._generate_secure_token(email, campaign_id)
        
        params = {'token': token}
        if include_email:
            params['email'] = email
        
        return f"{self.base_url}?{urlencode(params)}"
    
    def add_unsubscribe(self,
                       email: str,
                       campaign_id: str = "all",
                       reason: Optional[str] = None,
                       source: str = "manual") -> bool:
        """
        Add email to unsubscribe list
        
        Args:
            email: Email to unsubscribe
            campaign_id: Campaign to unsubscribe from
            reason: Optional reason for unsubscribing
            source: Source of unsubscribe (web, email, manual)
            
        Returns:
            True if successful
        """
        email = email.lower().strip()
        
        if not email or '@' not in email:
            return False
        
        data = self._load_unsubscribed()
        
        if email not in data:
            data[email] = {
                'campaigns': [],
                'unsubscribed_at': datetime.now().isoformat(),
                'history': []
            }
        
        # Add campaign if not already present
        if campaign_id not in data[email]['campaigns']:
            data[email]['campaigns'].append(campaign_id)
        
        # Add to history
        data[email]['history'].append({
            'campaign': campaign_id,
            'timestamp': datetime.now().isoformat(),
            'source': source,
            'reason': reason
        })
        
        # If unsubscribing from 'all', mark it
        if campaign_id == "all":
            data[email]['global_unsubscribe'] = True
        
        return self._save_unsubscribed(data)
    
    def is_unsubscribed(self, 
                       email: str, 
                       campaign_id: Optional[str] = None) -> bool:
        """
        Check if email is unsubscribed
        
        Args:
            email: Email to check
            campaign_id: Optional campaign to check (checks 'all' if None)
            
        Returns:
            True if unsubscribed
        """
        email = email.lower().strip()
        data = self._load_unsubscribed()
        
        if email not in data:
            return False
        
        # Check global unsubscribe
        if data[email].get('global_unsubscribe', False):
            return True
        
        # Check if unsubscribed from 'all' campaigns
        if 'all' in data[email]['campaigns']:
            return True
        
        # Check specific campaign
        if campaign_id and campaign_id in data[email]['campaigns']:
            return True
        
        return False
    
    def remove_unsubscribe(self, 
                          email: str, 
                          campaign_id: Optional[str] = None) -> bool:
        """
        Remove email from unsubscribe list (re-subscribe)
        
        Args:
            email: Email to re-subscribe
            campaign_id: Campaign to re-subscribe to (all if None)
            
        Returns:
            True if successful
        """
        email = email.lower().strip()
        data = self._load_unsubscribed()
        
        if email not in data:
            return False
        
        if campaign_id:
            # Remove specific campaign
            if campaign_id in data[email]['campaigns']:
                data[email]['campaigns'].remove(campaign_id)
        else:
            # Remove all unsubscribes
            data[email]['campaigns'] = []
            data[email]['global_unsubscribe'] = False
        
        # Add to history
        data[email]['history'].append({
            'action': 'resubscribe',
            'campaign': campaign_id or 'all',
            'timestamp': datetime.now().isoformat()
        })
        
        return self._save_unsubscribed(data)
    
    def get_unsubscribed_emails(self, 
                               campaign_id: Optional[str] = None) -> Set[str]:
        """
        Get set of unsubscribed emails
        
        Args:
            campaign_id: Filter by campaign (all if None)
            
        Returns:
            Set of unsubscribed emails
        """
        data = self._load_unsubscribed()
        unsubscribed = set()
        
        for email, info in data.items():
            if info.get('global_unsubscribe', False):
                unsubscribed.add(email)
            elif 'all' in info['campaigns']:
                unsubscribed.add(email)
            elif campaign_id and campaign_id in info['campaigns']:
                unsubscribed.add(email)
        
        return unsubscribed
    
    def filter_contacts(self, 
                       contacts: List[Dict],
                       campaign_id: Optional[str] = None,
                       email_key: str = 'email') -> tuple[List[Dict], List[Dict]]:
        """
        Filter contacts, removing unsubscribed ones
        
        Args:
            contacts: List of contact dictionaries
            campaign_id: Campaign identifier
            email_key: Key for email field in contact dict
            
        Returns:
            Tuple of (valid_contacts, skipped_contacts)
        """
        valid = []
        skipped = []
        
        for contact in contacts:
            email = contact.get(email_key, '').strip().lower()
            
            if self.is_unsubscribed(email, campaign_id):
                skipped.append(contact)
            else:
                valid.append(contact)
        
        return valid, skipped
    
    def get_stats(self) -> Dict:
        """Get statistics about unsubscribes"""
        data = self._load_unsubscribed()
        
        total = len(data)
        global_unsub = sum(1 for info in data.values() 
                          if info.get('global_unsubscribe', False))
        
        # Count by campaign
        campaign_counts = {}
        for info in data.values():
            for campaign in info['campaigns']:
                campaign_counts[campaign] = campaign_counts.get(campaign, 0) + 1
        
        # Recent unsubscribes (last 7 days)
        recent_cutoff = datetime.now() - timedelta(days=7)
        recent = 0
        for info in data.values():
            try:
                unsub_date = datetime.fromisoformat(info['unsubscribed_at'])
                if unsub_date > recent_cutoff:
                    recent += 1
            except (KeyError, ValueError):
                continue
        
        return {
            'total_unsubscribed': total,
            'global_unsubscribes': global_unsub,
            'recent_7_days': recent,
            'by_campaign': campaign_counts,
            'last_updated': datetime.now().isoformat()
        }
    
    def export_list(self, output_file: Path) -> bool:
        """Export unsubscribe list to file"""
        data = self._load_unsubscribed()
        
        try:
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2, sort_keys=True)
            return True
        except IOError:
            return False
    
    def import_list(self, input_file: Path, merge: bool = True) -> bool:
        """Import unsubscribe list from file"""
        try:
            with open(input_file, 'r') as f:
                imported = json.load(f)
            
            if merge:
                existing = self._load_unsubscribed()
                # Merge data
                for email, info in imported.items():
                    if email in existing:
                        # Merge campaigns
                        existing[email]['campaigns'] = list(set(
                            existing[email]['campaigns'] + info['campaigns']
                        ))
                    else:
                        existing[email] = info
                
                return self._save_unsubscribed(existing)
            else:
                return self._save_unsubscribed(imported)
                
        except (IOError, json.JSONDecodeError):
            return False


# Example usage and testing
if __name__ == "__main__":
    # Initialize manager
    manager = UnsubscribeManager(
        tracking_dir=Path("tracking"),
        base_url="https://sednabcn.github.io/unsubscribe"
    )
    
    # Example: Add unsubscribe
    manager.add_unsubscribe(
        "user@example.com",
        campaign_id="campaign1",
        reason="No longer interested",
        source="web"
    )
    
    # Check if unsubscribed
    is_unsub = manager.is_unsubscribed("user@example.com", "campaign1")
    print(f"Is unsubscribed: {is_unsub}")
    
    # Generate link
    link = manager.generate_unsubscribe_link("test@example.com", "campaign2")
    print(f"Unsubscribe link: {link}")
    
    # Get statistics
    stats = manager.get_stats()
    print(f"\nStatistics:")
    print(json.dumps(stats, indent=2))
    
    # Filter contacts
    contacts = [
        {'email': 'user@example.com', 'name': 'User 1'},
        {'email': 'valid@example.com', 'name': 'User 2'},
    ]
    
    valid, skipped = manager.filter_contacts(contacts, "campaign1")
    print(f"\nFiltered: {len(valid)} valid, {len(skipped)} skipped")
