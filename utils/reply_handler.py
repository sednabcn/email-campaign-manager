#!/usr/bin/env python3
"""
Enhanced Reply Handler - Process unsubscribe requests and replies
Integrates seamlessly with ComplianceWrapper
"""

import imaplib
import email
import json
import re
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Set, Optional, Tuple
import os


class ReplyHandler:
    """
    Handle email replies and process unsubscribe requests
    
    Features:
    - Automatic unsubscribe detection
    - Integration with ComplianceWrapper
    - Bounce detection
    - Reply categorization
    - Comprehensive logging
    """
    
    def __init__(self,
                 imap_server: Optional[str] = None,
                 imap_user: Optional[str] = None,
                 imap_password: Optional[str] = None,
                 imap_port: int = 993,
                 contacts_dir: str = "contacts",
                 tracking_dir: str = "tracking"):
        """
        Initialize reply handler
        
        Args:
            imap_server: IMAP server (e.g., 'imap.gmail.com')
            imap_user: Email username
            imap_password: Email password
            imap_port: IMAP port (default: 993 for SSL)
            contacts_dir: Directory for contact lists
            tracking_dir: Directory for tracking files
        """
        # Get credentials from environment if not provided
        self.imap_server = imap_server or os.getenv('IMAP_SERVER')
        self.imap_user = imap_user or os.getenv('SMTP_USER') or os.getenv('IMAP_USER')
        self.imap_password = imap_password or os.getenv('SMTP_PASS') or os.getenv('IMAP_PASS')
        self.imap_port = imap_port
        
        # Setup directories
        self.contacts_dir = Path(contacts_dir)
        self.tracking_dir = Path(tracking_dir)
        self.contacts_dir.mkdir(exist_ok=True)
        self.tracking_dir.mkdir(exist_ok=True)
        
        # File paths
        self.suppression_file = self.contacts_dir / "suppression_list.json"
        self.reply_log_file = self.tracking_dir / "reply_log.jsonl"
        self.bounce_log_file = self.tracking_dir / "bounce_log.jsonl"
        
        # Unsubscribe keywords
        self.unsubscribe_keywords = [
            'unsubscribe', 'opt out', 'opt-out', 'remove me',
            'stop sending', 'no more emails', 'take me off',
            'stop emailing', 'unsubscribe me', 'remove from list',
            'take me off your list', 'no longer interested',
            'stop contacting', 'do not contact', 'cease contact'
        ]
        
        # Bounce indicators
        self.bounce_indicators = [
            'delivery failed', 'undeliverable', 'mail delivery failed',
            'returned mail', 'delivery status notification',
            'user unknown', 'mailbox full', 'address not found',
            'recipient address rejected', 'smtp error', 'permanent error'
        ]
    
    def _load_suppression_list(self) -> Set[str]:
        """Load current suppression list"""
        if not self.suppression_file.exists():
            return set()
        
        try:
            with open(self.suppression_file, 'r') as f:
                data = json.load(f)
                return set(email.lower() for email in data.get('suppressed_emails', []))
        except Exception as e:
            print(f"⚠️  Warning: Could not load suppression list: {e}")
            return set()
    
    def _save_suppression_list(self, emails: Set[str]):
        """Save updated suppression list"""
        with open(self.suppression_file, 'w') as f:
            json.dump({
                'suppressed_emails': sorted(list(emails)),
                'last_updated': datetime.now().isoformat(),
                'count': len(emails)
            }, f, indent=2)
    
    def _log_reply(self, from_email: str, subject: str, 
                   category: str, body_preview: str = ""):
        """Log a reply for tracking"""
        with open(self.reply_log_file, 'a') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'from': from_email,
                'subject': subject,
                'category': category,
                'body_preview': body_preview[:200] if body_preview else ""
            }, f)
            f.write('\n')
    
    def _log_bounce(self, email_addr: str, reason: str):
        """Log a bounced email"""
        with open(self.bounce_log_file, 'a') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'email': email_addr,
                'reason': reason
            }, f)
            f.write('\n')
    
    def _extract_email_address(self, from_header: str) -> str:
        """Extract email address from 'Name <email@domain.com>' format"""
        # Try to find email in angle brackets
        match = re.search(r'<([^>]+)>', from_header)
        if match:
            return match.group(1).lower().strip()
        
        # Try to find email pattern
        match = re.search(r'[\w\.-]+@[\w\.-]+\.\w+', from_header)
        if match:
            return match.group(0).lower().strip()
        
        return from_header.lower().strip()
    
    def _is_unsubscribe_request(self, subject: str, body: str) -> bool:
        """Check if email is an unsubscribe request"""
        combined = f"{subject} {body}".lower()
        return any(keyword in combined for keyword in self.unsubscribe_keywords)
    
    def _is_bounce(self, subject: str, body: str, from_email: str) -> Tuple[bool, str]:
        """
        Check if email is a bounce notification
        
        Returns:
            Tuple of (is_bounce: bool, reason: str)
        """
        combined = f"{subject} {body}".lower()
        
        # Check sender (bounces often come from MAILER-DAEMON)
        if 'mailer-daemon' in from_email.lower() or 'postmaster' in from_email.lower():
            for indicator in self.bounce_indicators:
                if indicator in combined:
                    return True, indicator
        
        # Check for bounce indicators in subject/body
        for indicator in self.bounce_indicators:
            if indicator in combined:
                return True, indicator
        
        return False, ""
    
    def _extract_bounced_email(self, body: str) -> Optional[str]:
        """Try to extract the email address that bounced from bounce message"""
        # Look for common patterns in bounce messages
        patterns = [
            r'(?:to|for|recipient|address)[\s:]+<?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?',
            r'<?([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)>?.*(?:not found|unknown|rejected)',
        ]
        
        for pattern in patterns:
            match = re.search(pattern, body, re.IGNORECASE)
            if match:
                return match.group(1).lower()
        
        return None
    
    def _categorize_reply(self, subject: str, body: str, from_email: str) -> str:
        """Categorize the reply type"""
        if self._is_unsubscribe_request(subject, body):
            return "unsubscribe"
        
        is_bounce, _ = self._is_bounce(subject, body, from_email)
        if is_bounce:
            return "bounce"
        
        # Check for out-of-office
        ooo_keywords = ['out of office', 'automatic reply', 'away from office', 
                        'vacation', 'auto-reply', 'out of the office']
        combined = f"{subject} {body}".lower()
        if any(keyword in combined for keyword in ooo_keywords):
            return "out_of_office"
        
        # Check for interested replies
        interested_keywords = ['interested', 'tell me more', 'sounds good', 
                              'let\'s talk', 'schedule', 'call me']
        if any(keyword in combined for keyword in interested_keywords):
            return "interested"
        
        # Check for not interested
        not_interested_keywords = ['not interested', 'no thank', 'not at this time',
                                   'no thanks', 'pass on this']
        if any(keyword in combined for keyword in not_interested_keywords):
            return "not_interested"
        
        return "general_reply"
    
    def check_replies(self, 
                     days_back: int = 7,
                     mark_read: bool = False,
                     folder: str = 'INBOX',
                     process_bounces: bool = True) -> Dict:
        """
        Check email inbox for replies and process them
        
        Args:
            days_back: How many days back to check (0 = only unread)
            mark_read: Whether to mark processed emails as read
            folder: Email folder to check (default: 'INBOX')
            process_bounces: Whether to suppress bounced emails
            
        Returns:
            Dictionary with processing results
        """
        if not all([self.imap_server, self.imap_user, self.imap_password]):
            print("❌ IMAP credentials not configured")
            print("   Set IMAP_SERVER, SMTP_USER/IMAP_USER, and SMTP_PASS/IMAP_PASS environment variables")
            return {'error': 'IMAP not configured'}
        
        results = {
            'checked': 0,
            'unsubscribes': 0,
            'bounces': 0,
            'interested': 0,
            'out_of_office': 0,
            'not_interested': 0,
            'general_replies': 0,
            'new_suppressions': [],
            'interested_emails': [],
            'errors': []
        }
        
        try:
            # Connect to IMAP
            print(f"📧 Connecting to {self.imap_server}:{self.imap_port}...")
            mail = imaplib.IMAP4_SSL(self.imap_server, self.imap_port)
            mail.login(self.imap_user, self.imap_password)
            
            # Select folder
            status, _ = mail.select(folder)
            if status != 'OK':
                return {'error': f'Could not select folder: {folder}'}
            
            # Build search criteria
            if days_back > 0:
                since_date = (datetime.now() - timedelta(days=days_back)).strftime('%d-%b-%Y')
                search_criteria = f'SINCE {since_date}'
            else:
                search_criteria = 'UNSEEN'
            
            # Search for emails
            status, messages = mail.search(None, search_criteria)
            
            if status != 'OK':
                return {'error': 'Could not search mailbox'}
            
            email_ids = messages[0].split()
            results['checked'] = len(email_ids)
            
            if not email_ids:
                print("✅ No emails to process")
                mail.logout()
                return results
            
            print(f"📬 Found {len(email_ids)} emails to process")
            
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
                    from_email = self._extract_email_address(from_header)
                    
                    # Extract subject
                    subject = msg.get('Subject', '')
                    
                    # Extract body
                    body = ''
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == 'text/plain':
                                try:
                                    body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                                    break
                                except:
                                    pass
                    else:
                        try:
                            body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
                        except:
                            body = str(msg.get_payload())
                    
                    # Categorize the reply
                    category = self._categorize_reply(subject, body, from_email)
                    
                    # Handle based on category
                    if category == "unsubscribe":
                        print(f"🚫 Unsubscribe: {from_email}")
                        if from_email not in suppression_list:
                            suppression_list.add(from_email)
                            results['new_suppressions'].append(from_email)
                        results['unsubscribes'] += 1
                        
                    elif category == "bounce" and process_bounces:
                        print(f"📛 Bounce detected: {from_email}")
                        # Try to extract the actual bounced email
                        bounced_email = self._extract_bounced_email(body)
                        if bounced_email:
                            print(f"   Bounced email: {bounced_email}")
                            if bounced_email not in suppression_list:
                                suppression_list.add(bounced_email)
                                results['new_suppressions'].append(bounced_email)
                            self._log_bounce(bounced_email, "bounce")
                        results['bounces'] += 1
                        
                    elif category == "interested":
                        print(f"✨ Interested reply: {from_email}")
                        results['interested_emails'].append({
                            'email': from_email,
                            'subject': subject,
                            'body_preview': body[:200]
                        })
                        results['interested'] += 1
                        
                    elif category == "not_interested":
                        print(f"👎 Not interested: {from_email}")
                        # Optionally suppress these too
                        if from_email not in suppression_list:
                            suppression_list.add(from_email)
                            results['new_suppressions'].append(from_email)
                        results['not_interested'] += 1
                        
                    elif category == "out_of_office":
                        print(f"🏖️  Out of office: {from_email}")
                        results['out_of_office'] += 1
                        
                    else:
                        print(f"💬 General reply: {from_email}")
                        results['general_replies'] += 1
                    
                    # Log the reply
                    self._log_reply(from_email, subject, category, body[:200])
                    
                    # Mark as read if requested
                    if mark_read:
                        mail.store(email_id, '+FLAGS', '\\Seen')
                        
                except Exception as e:
                    results['errors'].append(f"Error processing email: {str(e)}")
                    print(f"⚠️  Error processing email: {e}")
            
            # Save updated suppression list
            if results['new_suppressions']:
                self._save_suppression_list(suppression_list)
                print(f"\n✅ Added {len(results['new_suppressions'])} emails to suppression list")
            
            # Logout
            mail.logout()
            print("\n✅ Done processing emails")
            
        except Exception as e:
            results['errors'].append(str(e))
            print(f"❌ Error connecting to email: {e}")
        
        return results
    
    def add_suppression(self, email_addr: str, reason: str = "manual"):
        """Manually add an email to suppression list"""
        suppression_list = self._load_suppression_list()
        email_addr = email_addr.lower().strip()
        
        if email_addr not in suppression_list:
            suppression_list.add(email_addr)
            self._save_suppression_list(suppression_list)
            self._log_reply(email_addr, "", f"suppressed_{reason}", "")
            print(f"✅ Added {email_addr} to suppression list ({reason})")
        else:
            print(f"ℹ️  {email_addr} already in suppression list")


def main():
    """Run reply handler from command line"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Check email replies for unsubscribes and categorize responses',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Check last 7 days
  python reply_handler.py
  
  # Check only unread emails
  python reply_handler.py --days 0
  
  # Check and mark as read
  python reply_handler.py --mark-read
  
  # Show current suppression stats
  python reply_handler.py --show-stats
  
Environment variables needed:
  IMAP_SERVER - IMAP server (e.g., imap.gmail.com)
  SMTP_USER or IMAP_USER - Your email username
  SMTP_PASS or IMAP_PASS - Your email password
        """)
    
    parser.add_argument('--days', type=int, default=7, 
                       help='Days back to check (0=unread only, default: 7)')
    parser.add_argument('--mark-read', action='store_true',
                       help='Mark processed emails as read')
    parser.add_argument('--show-stats', action='store_true',
                       help='Show suppression list statistics')
    parser.add_argument('--add-suppression', type=str,
                       help='Manually add email to suppression list')
    parser.add_argument('--folder', type=str, default='INBOX',
                       help='Email folder to check (default: INBOX)')
    parser.add_argument('--no-bounces', action='store_true',
                       help='Don\'t process bounce messages')
    
    args = parser.parse_args()
    
    handler = ReplyHandler()
    
    if args.show_stats:
        # Show statistics
        suppression_list = handler._load_suppression_list()
        print(f"\n📊 Suppression List Statistics")
        print(f"{'='*50}")
        print(f"Total suppressed emails: {len(suppression_list)}")
        
        if suppression_list:
            print(f"\nRecent additions (last 10):")
            for email_addr in sorted(list(suppression_list))[-10:]:
                print(f"   • {email_addr}")
        
        # Show reply log stats if exists
        if handler.reply_log_file.exists():
            print(f"\n📈 Reply Statistics")
            print(f"{'='*50}")
            categories = {}
            with open(handler.reply_log_file, 'r') as f:
                for line in f:
                    try:
                        entry = json.loads(line)
                        cat = entry.get('category', 'unknown')
                        categories[cat] = categories.get(cat, 0) + 1
                    except:
                        pass
            
            for category, count in sorted(categories.items(), key=lambda x: x[1], reverse=True):
                print(f"   {category}: {count}")
    
    elif args.add_suppression:
        # Manually add to suppression
        handler.add_suppression(args.add_suppression, reason="manual")
    
    else:
        # Check for replies
        print(f"\n🔍 Checking for email replies...")
        print(f"{'='*50}")
        
        results = handler.check_replies(
            days_back=args.days,
            mark_read=args.mark_read,
            folder=args.folder,
            process_bounces=not args.no_bounces
        )
        
        if 'error' in results:
            print(f"\n❌ Error: {results['error']}")
            return
        
        # Display results
        print(f"\n📊 Processing Results")
        print(f"{'='*50}")
        print(f"Emails checked:        {results['checked']}")
        print(f"Unsubscribes:         {results['unsubscribes']}")
        print(f"Bounces:              {results['bounces']}")
        print(f"Interested replies:   {results['interested']}")
        print(f"Not interested:       {results['not_interested']}")
        print(f"Out of office:        {results['out_of_office']}")
        print(f"General replies:      {results['general_replies']}")
        print(f"New suppressions:     {len(results['new_suppressions'])}")
        
        if results['new_suppressions']:
            print(f"\n🚫 Newly suppressed emails:")
            for email_addr in results['new_suppressions']:
                print(f"   • {email_addr}")
        
        if results['interested_emails']:
            print(f"\n✨ Interested replies (check these!):")
            for reply in results['interested_emails']:
                print(f"   • {reply['email']}")
                print(f"     Subject: {reply['subject']}")
                print(f"     Preview: {reply['body_preview'][:100]}...")
                print()
        
        if results['errors']:
            print(f"\n⚠️  Errors encountered: {len(results['errors'])}")
            for error in results['errors'][:5]:  # Show first 5
                print(f"   • {error}")


if __name__ == "__main__":
    main()
