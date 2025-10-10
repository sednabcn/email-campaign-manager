#!/usr/bin/env python3
"""
Email Reply Handler - Process unsubscribe requests from email replies
Run this regularly to check for unsubscribe requests
"""

import imaplib
import email
import json
from datetime import datetime
from pathlib import Path
import os
import re

class ReplyHandler:
    """Handle email replies and process unsubscribe requests"""
    
    def __init__(self,
                 imap_server: str = None,
                 imap_user: str = None,
                 imap_password: str = None,
                 suppression_file: str = "contacts/suppression_list.json"):
        """
        Initialize reply handler
        
        Args:
            imap_server: IMAP server address
            imap_user: Email username
            imap_password: Email password
            suppression_file: Path to suppression list
        """
        self.imap_server = imap_server or os.getenv('IMAP_SERVER')
        self.imap_user = imap_user or os.getenv('SMTP_USER')
        self.imap_password = imap_password or os.getenv('SMTP_PASS')
        
        self.suppression_file = Path(suppression_file)
        self.log_file = self.suppression_file.parent / "reply_log.jsonl"
    
    def _load_suppression_list(self) -> set:
        """Load current suppression list"""
        if not self.suppression_file.exists():
            return set()
        
        try:
            with open(self.suppression_file, 'r') as f:
                data = json.load(f)
                return set(data.get('suppressed_emails', []))
        except Exception as e:
            print(f"Error loading suppression list: {e}")
            return set()
    
    def _save_suppression_list(self, emails: set):
        """Save updated suppression list"""
        with open(self.suppression_file, 'w') as f:
            json.dump({
                'suppressed_emails': list(emails),
                'last_updated': datetime.now().isoformat(),
                'count': len(emails)
            }, f, indent=2)
    
    def _log_reply(self, from_email: str, subject: str, action: str):
        """Log a reply for tracking"""
        with open(self.log_file, 'a') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'from': from_email,
                'subject': subject,
                'action': action
            }, f)
            f.write('\n')
    
    def _is_unsubscribe_request(self, subject: str, body: str) -> bool:
        """Check if email is an unsubscribe request"""
        unsubscribe_keywords = [
            'unsubscribe',
            'opt out',
            'opt-out',
            'remove me',
            'stop sending',
            'no more emails',
            'take me off'
        ]
        
        combined = f"{subject} {body}".lower()
        
        return any(keyword in combined for keyword in unsubscribe_keywords)
    
    def check_replies(self, days_back: int = 7, mark_read: bool = False) -> dict:
        """
        Check email inbox for replies and process unsubscribe requests
        
        Args:
            days_back: How many days back to check
            mark_read: Whether to mark processed emails as read
            
        Returns:
            Dictionary with processing results
        """
        if not all([self.imap_server, self.imap_user, self.imap_password]):
            print("❌ IMAP credentials not configured")
            return {'error': 'IMAP not configured'}
        
        results = {
            'checked': 0,
            'unsubscribe_requests': 0,
            'new_suppressions': [],
            'errors': []
        }
        
        try:
            # Connect to IMAP
            print(f"📧 Connecting to {self.imap_server}...")
            mail = imaplib.IMAP4_SSL(self.imap_server)
            mail.login(self.imap_user, self.imap_password)
            mail.select('inbox')
            
            # Search for unread emails
            status, messages = mail.search(None, 'UNSEEN')
            
            if status != 'OK':
                return {'error': 'Could not search mailbox'}
            
            email_ids = messages[0].split()
            results['checked'] = len(email_ids)
            
            print(f"Found {len(email_ids)} unread messages")
            
            # Load current suppression list
            suppression_list = self._load_suppression_list()
            
            # Process each email
            for email_id in email_ids:
                try:
                    # Fetch email
                    status, msg_data = mail.fetch(email_id, '(RFC822)')
                    
                    if status != 'OK':
                        continue
                    
                    # Parse email
                    raw_email = msg_data[0][1]
                    msg = email.message_from_bytes(raw_email)
                    
                    # Extract sender
                    from_header = msg.get('From', '')
                    # Extract email from "Name <email@domain.com>" format
                    email_match = re.search(r'<(.+?)>', from_header)
                    from_email = email_match.group(1) if email_match else from_header
                    from_email = from_email.lower().strip()
                    
                    # Extract subject
                    subject = msg.get('Subject', '')
                    
                    # Extract body
                    body = ''
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                break
                    else:
                        body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                    
                    # Check if unsubscribe request
                    if self._is_unsubscribe_request(subject, body):
                        print(f"📭 Unsubscribe request from {from_email}")
                        
                        if from_email not in suppression_list:
                            suppression_list.add(from_email)
                            results['new_suppressions'].append(from_email)
                        
                        results['unsubscribe_requests'] += 1
                        self._log_reply(from_email, subject, 'unsubscribe')
                        
                        # Mark as read if requested
                        if mark_read:
                            mail.store(email_id, '+FLAGS', '\\Seen')
                    else:
                        # Log other replies
                        self._log_reply(from_email, subject, 'reply')
                
                except Exception as e:
                    results['errors'].append(str(e))
                    print(f"⚠️  Error processing email: {e}")
            
            # Save updated suppression list
            if results['new_suppressions']:
                self._save_suppression_list(suppression_list)
                print(f"✅ Added {len(results['new_suppressions'])} emails to suppression list")
            
            # Logout
            mail.logout()
            
        except Exception as e:
            results['errors'].append(str(e))
            print(f"❌ Error connecting to email: {e}")
        
        return results


def main():
    """Run reply handler from command line"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Check email replies for unsubscribe requests')
    parser.add_argument('--days', type=int, default=7, help='Days back to check')
    parser.add_argument('--mark-read', action='store_true', help='Mark processed emails as read')
    parser.add_argument('--show-stats', action='store_true', help='Show suppression list stats')
    
    args = parser.parse_args()
    
    handler = ReplyHandler()
    
    if args.show_stats:
        suppression_list = handler._load_suppression_list()
        print(f"📊 Suppression List Stats:")
        print(f"   Total suppressed: {len(suppression_list)}")
        if suppression_list:
            print(f"   Recent additions:")
            for email in list(suppression_list)[-10:]:
                print(f"      - {email}")
    else:
        print("🔍 Checking for email replies...")
        results = handler.check_replies(days_back=args.days, mark_read=args.mark_read)
        
        print("\n📊 Results:")
        print(f"   Emails checked: {results['checked']}")
        print(f"   Unsubscribe requests: {results['unsubscribe_requests']}")
        print(f"   New suppressions: {len(results['new_suppressions'])}")
        
        if results['new_suppressions']:
            print(f"\n📭 New unsubscribe requests:")
            for email in results['new_suppressions']:
                print(f"      - {email}")
        
        if results['errors']:
            print(f"\n⚠️  Errors: {len(results['errors'])}")


if __name__ == "__main__":
    main()
