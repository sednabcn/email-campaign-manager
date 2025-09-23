#!/usr/bin/env python3
"""
Gmail-based Email Feedback and Tracking System
Monitors replies, unsubscribes, bounces, and engagement
"""

import imaplib
import email
import smtplib
import ssl
import json
import re
import time
from datetime import datetime, timedelta
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from pathlib import Path
import pandas as pd
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

class GmailFeedbackTracker:
    """Gmail-based feedback tracking system"""
    
    def __init__(self, email_user, email_pass, smtp_host='smtp.gmail.com', imap_host='imap.gmail.com'):
        self.email_user = email_user
        self.email_pass = email_pass
        self.smtp_host = smtp_host
        self.imap_host = imap_host
        self.tracking_data = {
            'replies': [],
            'unsubscribes': [],
            'bounces': [],
            'engagement': [],
            'errors': []
        }
        
    def connect_imap(self):
        """Connect to Gmail IMAP server"""
        try:
            context = ssl.create_default_context()
            imap = imaplib.IMAP4_SSL(self.imap_host, 993, ssl_context=context)
            imap.login(self.email_user, self.email_pass)
            logger.info(f"Connected to IMAP: {self.imap_host}")
            return imap
        except Exception as e:
            logger.error(f"IMAP connection failed: {e}")
            return None
    
    def connect_smtp(self):
        """Connect to Gmail SMTP server"""
        try:
            context = ssl.create_default_context()
            smtp = smtplib.SMTP(self.smtp_host, 587)
            smtp.starttls(context=context)
            smtp.login(self.email_user, self.email_pass)
            logger.info(f"Connected to SMTP: {self.smtp_host}")
            return smtp
        except Exception as e:
            logger.error(f"SMTP connection failed: {e}")
            return None
    
    def parse_email_content(self, msg):
        """Extract email content and metadata"""
        email_data = {
            'from': msg.get('From', ''),
            'to': msg.get('To', ''),
            'subject': msg.get('Subject', ''),
            'date': msg.get('Date', ''),
            'message_id': msg.get('Message-ID', ''),
            'in_reply_to': msg.get('In-Reply-To', ''),
            'references': msg.get('References', ''),
            'content': '',
            'is_html': False
        }
        
        # Extract body content
        if msg.is_multipart():
            for part in msg.walk():
                content_type = part.get_content_type()
                if content_type == "text/plain":
                    try:
                        email_data['content'] = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                    except:
                        email_data['content'] = part.get_payload()
                elif content_type == "text/html":
                    email_data['is_html'] = True
        else:
            try:
                email_data['content'] = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            except:
                email_data['content'] = msg.get_payload()
        
        return email_data
    
    def classify_email_type(self, email_data):
        """Classify email as reply, unsubscribe, bounce, etc."""
        subject = email_data['subject'].lower()
        content = email_data['content'].lower()
        from_addr = email_data['from'].lower()
        
        # Check for bounce indicators
        bounce_indicators = [
            'mailer-daemon', 'postmaster', 'undelivered', 'delivery failed',
            'returned mail', 'bounce', 'permanent error', 'temporary failure'
        ]
        
        if any(indicator in from_addr or indicator in subject for indicator in bounce_indicators):
            return 'bounce'
        
        # Check for unsubscribe requests
        unsubscribe_keywords = [
            'unsubscribe', 'remove me', 'opt out', 'stop sending',
            'take me off', 'no longer interested', 'cancel subscription'
        ]
        
        if any(keyword in subject or keyword in content for keyword in unsubscribe_keywords):
            return 'unsubscribe'
        
        # Check for auto-replies
        auto_reply_indicators = [
            'auto-reply', 'out of office', 'vacation', 'automatic reply',
            'away message', 'currently unavailable'
        ]
        
        if any(indicator in subject or indicator in content for indicator in auto_reply_indicators):
            return 'auto_reply'
        
        # Check if it's a reply to our campaign
        if email_data['in_reply_to'] or 're:' in subject:
            return 'reply'
        
        return 'unknown'
    
    def extract_original_recipient(self, email_data):
        """Extract original campaign recipient from email headers or content"""
        # Try to extract from In-Reply-To or References headers
        references = email_data.get('references', '') + ' ' + email_data.get('in_reply_to', '')
        
        # Look for email addresses in the content (for forwards/bounces)
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails_in_content = re.findall(email_pattern, email_data['content'])
        
        # Filter out our sending email
        original_recipients = [email for email in emails_in_content if email != self.email_user]
        
        return original_recipients[0] if original_recipients else email_data['from']
    
    def process_unsubscribe(self, email_data, smtp_connection):
        """Process unsubscribe request"""
        requester_email = email_data['from']
        
        try:
            # Send confirmation email
            confirmation_msg = MIMEMultipart()
            confirmation_msg['From'] = self.email_user
            confirmation_msg['To'] = requester_email
            confirmation_msg['Subject'] = 'Unsubscribe Confirmation'
            
            confirmation_body = f"""
Dear Subscriber,

Your unsubscribe request has been processed successfully.

You will no longer receive marketing emails from us at: {requester_email}

If you did not request this change, please contact us immediately.

Best regards,
Email Campaign System
            """
            
            confirmation_msg.attach(MIMEText(confirmation_body, 'plain'))
            smtp_connection.send_message(confirmation_msg)
            
            logger.info(f"Sent unsubscribe confirmation to {requester_email}")
            
            return {
                'status': 'processed',
                'confirmed': True,
                'confirmation_sent': True
            }
            
        except Exception as e:
            logger.error(f"Failed to send unsubscribe confirmation: {e}")
            return {
                'status': 'processed',
                'confirmed': True,
                'confirmation_sent': False,
                'error': str(e)
            }
    
    def analyze_engagement(self, email_data):
        """Analyze engagement level from reply content"""
        content = email_data['content'].lower()
        
        # Positive engagement indicators
        positive_keywords = [
            'interested', 'yes', 'please', 'more information', 'tell me more',
            'schedule', 'meeting', 'call me', 'sounds good', 'thank you'
        ]
        
        # Negative engagement indicators  
        negative_keywords = [
            'not interested', 'no thanks', 'stop', 'spam', 'annoying',
            'remove', 'unsubscribe', 'never contact'
        ]
        
        positive_score = sum(1 for keyword in positive_keywords if keyword in content)
        negative_score = sum(1 for keyword in negative_keywords if keyword in content)
        
        if positive_score > negative_score:
            return 'positive'
        elif negative_score > positive_score:
            return 'negative'
        else:
            return 'neutral'
    
    def monitor_inbox(self, hours_back=24, folder='INBOX'):
        """Monitor Gmail inbox for feedback"""
        imap = self.connect_imap()
        smtp = self.connect_smtp()
        
        if not imap or not smtp:
            logger.error("Failed to establish connections")
            return False
        
        try:
            # Select folder
            imap.select(folder)
            
            # Search for emails from last N hours
            since_date = (datetime.now() - timedelta(hours=hours_back)).strftime('%d-%b-%Y')
            search_criteria = f'SINCE {since_date}'
            
            status, messages = imap.search(None, search_criteria)
            
            if status != 'OK':
                logger.error(f"Search failed: {status}")
                return False
            
            message_ids = messages[0].split()
            logger.info(f"Found {len(message_ids)} emails to process")
            
            for msg_id in message_ids:
                try:
                    # Fetch email
                    status, msg_data = imap.fetch(msg_id, '(RFC822)')
                    
                    if status != 'OK':
                        continue
                        
                    email_message = email.message_from_bytes(msg_data[0][1])
                    email_data = self.parse_email_content(email_message)
                    
                    # Skip emails from ourselves
                    if self.email_user in email_data['from']:
                        continue
                    
                    # Classify email type
                    email_type = self.classify_email_type(email_data)
                    original_recipient = self.extract_original_recipient(email_data)
                    
                    # Process based on type
                    feedback_entry = {
                        'timestamp': datetime.now().isoformat(),
                        'type': email_type,
                        'from': email_data['from'],
                        'subject': email_data['subject'],
                        'original_recipient': original_recipient,
                        'message_id': email_data['message_id'],
                        'content_preview': email_data['content'][:200] + '...' if len(email_data['content']) > 200 else email_data['content']
                    }
                    
                    if email_type == 'reply':
                        engagement = self.analyze_engagement(email_data)
                        feedback_entry['engagement'] = engagement
                        self.tracking_data['replies'].append(feedback_entry)
                        
                    elif email_type == 'unsubscribe':
                        result = self.process_unsubscribe(email_data, smtp)
                        feedback_entry['processing_result'] = result
                        self.tracking_data['unsubscribes'].append(feedback_entry)
                        
                    elif email_type == 'bounce':
                        self.tracking_data['bounces'].append(feedback_entry)
                        
                    else:
                        self.tracking_data['engagement'].append(feedback_entry)
                    
                    logger.info(f"Processed {email_type} from {email_data['from']}")
                    
                except Exception as e:
                    logger.error(f"Error processing message {msg_id}: {e}")
                    self.tracking_data['errors'].append({
                        'timestamp': datetime.now().isoformat(),
                        'message_id': msg_id.decode(),
                        'error': str(e)
                    })
            
            # Close connections
            imap.logout()
            smtp.quit()
            
            return True
            
        except Exception as e:
            logger.error(f"Inbox monitoring failed: {e}")
            return False
    
    def generate_feedback_report(self, output_file='feedback_report.json'):
        """Generate comprehensive feedback report"""
        
        # Add summary statistics
        summary = {
            'total_replies': len(self.tracking_data['replies']),
            'total_unsubscribes': len(self.tracking_data['unsubscribes']),
            'total_bounces': len(self.tracking_data['bounces']),
            'total_engagement': len(self.tracking_data['engagement']),
            'total_errors': len(self.tracking_data['errors'])
        }
        
        # Analyze engagement
        positive_engagement = sum(1 for reply in self.tracking_data['replies'] if reply.get('engagement') == 'positive')
        negative_engagement = sum(1 for reply in self.tracking_data['replies'] if reply.get('engagement') == 'negative')
        
        summary['positive_engagement'] = positive_engagement
        summary['negative_engagement'] = negative_engagement
        summary['engagement_rate'] = round((positive_engagement / max(1, summary['total_replies'])) * 100, 2)
        
        report = {
            'report_timestamp': datetime.now().isoformat(),
            'summary': summary,
            'tracking_data': self.tracking_data
        }
        
        # Save to file
        with open(output_file, 'w') as f:
            json.dump(report, f, indent=2)
        
        logger.info(f"Feedback report saved to {output_file}")
        return report
    
    def update_contact_database(self, contacts_file='validated_contacts.csv'):
        """Update contact database with feedback information"""
        try:
            # Load existing contacts
            if Path(contacts_file).exists():
                contacts_df = pd.read_csv(contacts_file)
            else:
                logger.warning(f"Contacts file not found: {contacts_file}")
                return False
            
            # Add feedback columns if they don't exist
            feedback_columns = ['last_reply', 'unsubscribed', 'bounced', 'engagement_level']
            for col in feedback_columns:
                if col not in contacts_df.columns:
                    contacts_df[col] = ''
            
            # Update based on tracking data
            for unsubscribe in self.tracking_data['unsubscribes']:
                email = unsubscribe['from']
                contacts_df.loc[contacts_df['email'] == email, 'unsubscribed'] = 'yes'
                contacts_df.loc[contacts_df['email'] == email, 'last_reply'] = unsubscribe['timestamp']
            
            for bounce in self.tracking_data['bounces']:
                email = bounce.get('original_recipient', bounce['from'])
                contacts_df.loc[contacts_df['email'] == email, 'bounced'] = 'yes'
            
            for reply in self.tracking_data['replies']:
                email = reply['from']
                contacts_df.loc[contacts_df['email'] == email, 'last_reply'] = reply['timestamp']
                contacts_df.loc[contacts_df['email'] == email, 'engagement_level'] = reply.get('engagement', 'neutral')
            
            # Save updated contacts
            contacts_df.to_csv(contacts_file, index=False)
            logger.info(f"Updated contact database: {contacts_file}")
            
            return True
            
        except Exception as e:
            logger.error(f"Failed to update contact database: {e}")
            return False

def main():
    """Main execution function for GitHub Actions"""
    import os
    
    # Get credentials from environment
    email_user = os.getenv('SMTP_USER')
    email_pass = os.getenv('SMTP_PASS')
    
    if not email_user or not email_pass:
        logger.error("Email credentials not provided")
        return 1
    
    # Initialize tracker
    tracker = GmailFeedbackTracker(email_user, email_pass)
    
    # Monitor inbox for last 24 hours
    success = tracker.monitor_inbox(hours_back=24)
    
    if not success:
        logger.error("Inbox monitoring failed")
        return 1
    
    # Generate reports
    tracker.generate_feedback_report('tracking/feedback_report.json')
    tracker.update_contact_database('validated_contacts.csv')
    
    # Print summary
    summary = {
        'replies': len(tracker.tracking_data['replies']),
        'unsubscribes': len(tracker.tracking_data['unsubscribes']),
        'bounces': len(tracker.tracking_data['bounces']),
        'errors': len(tracker.tracking_data['errors'])
    }
    
    print(f"Feedback tracking completed:")
    print(f"  Replies: {summary['replies']}")
    print(f"  Unsubscribes: {summary['unsubscribes']}")
    print(f"  Bounces: {summary['bounces']}")
    print(f"  Errors: {summary['errors']}")
    
    return 0

if __name__ == '__main__':
    exit(main())
