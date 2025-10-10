import imaplib
import email
import json
import re
from datetime import datetime, timedelta
from pathlib import Path
import sys
import os

def check_for_unsubscribes(imap_server, username, password, days=7):
    """Check emails for unsubscribe requests"""
    
    suppression_file = Path('contacts/suppression_list.json')
    reply_log = Path('contacts/reply_log.jsonl')
    
    # Load existing suppressions
    suppressed = set()
    if suppression_file.exists():
        with open(suppression_file) as f:
            data = json.load(f)
            suppressed = set(data.get('suppressed_emails', []))
    
    # Connect to IMAP
    try:
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        mail.select('inbox')
        
        # Search for recent emails
        since_date = (datetime.now() - timedelta(days=days)).strftime('%d-%b-%Y')
        _, message_ids = mail.search(None, f'SINCE {since_date}')
        
        unsubscribe_keywords = [
            'unsubscribe', 'opt out', 'remove me', 'stop sending',
            'take me off', 'no longer interested', 'stop emails'
        ]
        
        new_suppressions = []
        
        for msg_id in message_ids[0].split():
            _, msg_data = mail.fetch(msg_id, '(RFC822)')
            email_body = msg_data[0][1]
            msg = email.message_from_bytes(email_body)
            
            # Get sender
            from_addr = email.utils.parseaddr(msg['From'])[1]
            subject = msg.get('Subject', '')
            
            # Get body
            body = ''
            if msg.is_multipart():
                for part in msg.walk():
                    if part.get_content_type() == 'text/plain':
                        body = part.get_payload(decode=True).decode('utf-8', errors='ignore')
                        break
            else:
                body = msg.get_payload(decode=True).decode('utf-8', errors='ignore')
            
            # Check for unsubscribe keywords
            text_to_check = (subject + ' ' + body).lower()
            if any(keyword in text_to_check for keyword in unsubscribe_keywords):
                if from_addr and from_addr not in suppressed:
                    print(f"🚫 Unsubscribe request detected from: {from_addr}")
                    suppressed.add(from_addr.lower())
                    new_suppressions.append(from_addr)
                    
                    # Log the reply
                    reply_log.parent.mkdir(parents=True, exist_ok=True)
                    with open(reply_log, 'a') as f:
                        log_entry = {
                            'email': from_addr,
                            'type': 'unsubscribe',
                            'subject': subject,
                            'timestamp': datetime.now().isoformat()
                        }
                        f.write(json.dumps(log_entry) + '\n')
        
        mail.close()
        mail.logout()
        
        # Save updated suppression list
        if new_suppressions:
            suppression_file.parent.mkdir(parents=True, exist_ok=True)
            data = {
                'suppressed_emails': sorted(list(suppressed)),
                'last_updated': datetime.now().isoformat(),
                'count': len(suppressed)
            }
            with open(suppression_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            print(f"✅ Added {len(new_suppressions)} new suppressions")
        else:
            print("✅ No new unsubscribe requests found")
        
        return len(new_suppressions)
        
    except Exception as e:
        print(f"⚠️  Could not check emails: {e}")
        return 0

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--days', type=int, default=7)
    args = parser.parse_args()
    
    imap_server = os.getenv('IMAP_SERVER', 'imap.gmail.com')
    username = os.getenv('SMTP_USER')
    password = os.getenv('SMTP_PASS')
    
    if not username or not password:
        print("⚠️  SMTP credentials not set - skipping reply check")
        sys.exit(0)
    
    check_for_unsubscribes(imap_server, username, password, args.days)
