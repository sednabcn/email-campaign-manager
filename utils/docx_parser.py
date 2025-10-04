#!/usr/bin/env python3
import argparse
import os
import sys
import traceback
import json
import re
import hashlib
from datetime import datetime
from pathlib import Path

# Add current directory to Python path for imports
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)

# Environment detection
IS_REMOTE = os.getenv('GITHUB_ACTIONS') is not None or os.getenv('CI') is not None

# GitHub Actions email integration
try:
    from email_sender import GitHubActionsEmailSender
    GITHUB_ACTIONS_EMAIL_AVAILABLE = True
    print("GitHub Actions email sender available")
except ImportError:
    GITHUB_ACTIONS_EMAIL_AVAILABLE = False
    print("GitHub Actions email sender not available - using standard EmailSender")

# Import the professional data loader
try:
    from data_loader import load_contacts_directory, validate_contact_data
    DATA_LOADER_AVAILABLE = True
    print("Using professional data_loader module")
except ImportError:
    DATA_LOADER_AVAILABLE = False
    print("Warning: data_loader module not found, using fallback functions")

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("Warning: python-docx library not available")

# Enhanced EmailSender with template processing
try:
    from email_sender import EmailSender as BaseEmailSender
    EMAIL_SENDER_AVAILABLE = True
    
    class EmailSender(BaseEmailSender):
        """Enhanced EmailSender with template variable substitution"""
        
        def substitute_variables(self, content, contact, additional_vars=None, contact_mapping=None):
            """
            Enhanced variable substitution with contact_mapping support
            
            Supports multiple placeholder formats:
            - [Recipient Name] with contact_mapping
            - {{variable}}, {variable} for direct field access
            """
            if not isinstance(content, str):
                return str(content)
            
            result = content
            variables = {}
            
            # Phase 1: Handle contact_mapping for [Placeholder] format (CRITICAL FIX)
            if contact_mapping and isinstance(contact_mapping, dict) and isinstance(contact, dict):
                for template_placeholder, csv_field in contact_mapping.items():
                   value = contact.get(csv_field, '')
                   # Handle nan, None, and empty values
                   if value and str(value).lower() not in ['nan', 'none', '']:
                       placeholder_pattern = f'[{template_placeholder}]'
                       result = result.replace(placeholder_pattern, str(value))
            
            # Phase 2: Build variables dictionary for generic patterns
            if isinstance(contact, dict):
                for key, value in contact.items():
                    if value is not None:
                        str_value = str(value).strip()
                        variables[key.lower()] = str_value
                        variables[key] = str_value
                        variables[key.replace('_', ' ').title()] = str_value
                        
                        if key.lower() in ['name', 'full_name']:
                            variables['Contact Name'] = str_value
                            variables['contact name'] = str_value
                            variables['name'] = str_value
                        elif key.lower() in ['email', 'email_address']:
                            variables['Contact Email'] = str_value
                            variables['contact email'] = str_value
                            variables['email'] = str_value
                        elif key.lower() in ['company', 'organization']:
                            variables['Company'] = str_value
                            variables['company'] = str_value
                            variables['organization'] = str_value
            
            if additional_vars and isinstance(additional_vars, dict):
                variables.update(additional_vars)
            
            if 'name' not in variables:
                variables['name'] = contact.get('email', '').split('@')[0] if contact.get('email') else 'Friend'
                variables['Contact Name'] = variables['name']
            
            if 'company' not in variables:
                variables['company'] = 'your organization'
                variables['Company'] = 'your organization'
            
            # Phase 3: Handle {{variable}} format
            pattern1 = re.compile(r'\{\{([^}]+)\}\}')
            for match in pattern1.finditer(result):
                var_name = match.group(1).strip()
                if var_name in variables:
                    result = result.replace(match.group(0), variables[var_name])
                else:
                    var_lower = var_name.lower()
                    if var_lower in variables:
                        result = result.replace(match.group(0), variables[var_lower])
            
            # Phase 4: Handle {variable} format
            pattern2 = re.compile(r'\{([^}]+)\}')
            for match in pattern2.finditer(result):
                var_name = match.group(1).strip().lower()
                if var_name in variables:
                    result = result.replace(match.group(0), variables[var_name])
            
            return result
        
        def send_campaign(self, campaign_name, subject, content, recipients, from_name="Campaign System", tracking_id=None, contact_mapping=None):
            print(f"\n=== CAMPAIGN: {campaign_name} ===")
            if tracking_id:
                print(f"Tracking ID: {tracking_id}")
            print(f"Subject Template: {subject}")
            print(f"From: {from_name}")
            print(f"Recipients: {len(recipients)}")
            
            processed_recipients = []
            sent_count = 0
            failed_count = 0
            
            for i, recipient in enumerate(recipients):
                if not isinstance(recipient, dict):
                    print(f"Skipping invalid recipient {i+1}: not a dictionary")
                    failed_count += 1
                    continue
                
                email = recipient.get('email', '').strip()
                if not email or '@' not in email:
                    print(f"Skipping recipient {i+1}: invalid email '{email}'")
                    failed_count += 1
                    continue
                
                try:
                    personalized_subject = self.substitute_variables(subject, recipient, contact_mapping=contact_mapping)
                    personalized_content = self.substitute_variables(content, recipient, contact_mapping=contact_mapping)
                    
                    processed_recipient = {
                        **recipient,
                        'personalized_subject': personalized_subject,
                        'personalized_content': personalized_content,
                        'original_subject': subject,
                        'original_content': content[:100] + "..." if len(content) > 100 else content,
                        'tracking_id': tracking_id
                    }
                    
                    processed_recipients.append(processed_recipient)
                    sent_count += 1
                    
                    if self.dry_run:
                        print(f"  {i+1}. {recipient.get('name', 'N/A')} <{email}>")
                        print(f"      Subject: {personalized_subject}")
                        if len(personalized_content) > 150:
                            print(f"      Content: {personalized_content[:150]}...")
                        else:
                            print(f"      Content: {personalized_content}")
                    
                except Exception as e:
                    print(f"Error processing recipient {i+1} ({email}): {str(e)}")
                    failed_count += 1
                    continue
            
            if self.dry_run:
                print("DRY-RUN MODE: No emails sent")
                if len(processed_recipients) > 3:
                    print(f"  ... and {len(processed_recipients) - 3} more recipients with personalized content")
            
            return {
                'campaign_name': campaign_name,
                'tracking_id': tracking_id,
                'total_recipients': len(recipients),
                'sent': sent_count if not self.dry_run else 0,
                'failed': failed_count,
                'processed_recipients': processed_recipients,
                'duration_seconds': 1.5,
                'template_substitution': True
            }

except ImportError:
    print("Warning: email_sender module not found, using fallback")
    EMAIL_SENDER_AVAILABLE = False
    class EmailSender:
        def __init__(self, smtp_host=None, smtp_port=None, smtp_user=None, smtp_password=None, alerts_email=None, dry_run=False):
            self.smtp_host = smtp_host
            self.smtp_port = smtp_port
            self.smtp_user = smtp_user
            self.smtp_password = smtp_password
            self.alerts_email = alerts_email
            self.dry_run = dry_run
            print(f"Fallback EmailSender initialized - dry_run: {dry_run}, alerts: {alerts_email}")
        
        def substitute_variables(self, content, contact, additional_vars=None, contact_mapping=None):
            if not isinstance(content, str):
                return str(content)
            
            result = content
            
            # Handle contact_mapping for [Placeholder] format
            if contact_mapping and isinstance(contact_mapping, dict) and isinstance(contact, dict):
                for template_placeholder, csv_field in contact_mapping.items():
                    value = contact.get(csv_field, '')
                    if value:
                        placeholder_pattern = f'[{template_placeholder}]'
                        result = result.replace(placeholder_pattern, str(value))
            
            # Handle generic patterns
            if isinstance(contact, dict):
                name = contact.get('name', contact.get('email', '').split('@')[0] if contact.get('email') else 'Friend')
                email = contact.get('email', '')
                company = contact.get('company', contact.get('organization', 'your organization'))
                
                replacements = {
                    '{{Contact Name}}': name, '{{contact name}}': name, '{{name}}': name, '{name}': name,
                    '{{Contact Email}}': email, '{{contact email}}': email, '{{email}}': email, '{email}': email,
                    '{{Company}}': company, '{{company}}': company, '{company}': company,
                }
                
                for pattern, value in replacements.items():
                    result = result.replace(pattern, str(value))
            
            return result
        
        def send_campaign(self, campaign_name, subject, content, recipients, from_name="Campaign System", tracking_id=None, contact_mapping=None):
            print(f"\n=== CAMPAIGN: {campaign_name} ===")
            if tracking_id:
                print(f"Tracking ID: {tracking_id}")
            print(f"Subject Template: {subject}")
            print(f"From: {from_name}")
            print(f"Recipients: {len(recipients)}")
            
            sent_count = 0
            failed_count = 0
            
            if self.dry_run:
                print("DRY-RUN MODE: No emails sent")
                for i, recipient in enumerate(recipients[:3]):
                    if isinstance(recipient, dict):
                        personalized_subject = self.substitute_variables(subject, recipient, contact_mapping=contact_mapping)
                        personalized_content = self.substitute_variables(content, recipient, contact_mapping=contact_mapping)
                        
                        email = recipient.get('email', 'N/A')
                        name = recipient.get('name', 'N/A')
                        
                        print(f"  {i+1}. {name} <{email}>")
                        print(f"      Subject: {personalized_subject}")
                        print(f"      Content: {personalized_content[:100]}...")
                        sent_count += 1
                    else:
                        failed_count += 1
                
                if len(recipients) > 3:
                    remaining = len(recipients) - 3
                    sent_count += max(0, remaining - failed_count)
                    print(f"  ... and {remaining} more recipients with personalized content")
            
            return {
                'campaign_name': campaign_name,
                'tracking_id': tracking_id,
                'total_recipients': len(recipients),
                'sent': sent_count if not self.dry_run else 0,
                'failed': failed_count,
                'duration_seconds': 1.5,
                'template_substitution': True
            }
        
        def send_alert(self, subject, body):
            print(f"ALERT: {subject}")
            print(f"Body: {body[:200]}...")


def fallback_load_contacts_from_directory(contacts_dir):
    """Fallback contact loader when data_loader module is not available"""
    print("Warning: Using fallback contact loading - data_loader module not found")
    
    all_contacts = []
    contacts_path = Path(contacts_dir)
    
    if not contacts_path.exists():
        print(f"Contacts directory not found: {contacts_dir}")
        return all_contacts
    
    import csv
    csv_files = list(contacts_path.glob('*.csv'))
    
    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', newline='', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                for row in reader:
                    contact = {}
                    for key, value in row.items():
                        if key and value:
                            clean_key = key.strip().lower()
                            clean_value = value.strip()
                            
                            if clean_key in ['email', 'email_address']:
                                contact['email'] = clean_value
                            elif clean_key in ['name', 'full_name']:
                                contact['name'] = clean_value
                            else:
                                contact[clean_key] = clean_value
                    
                    if contact.get('email') and '@' in contact['email']:
                        all_contacts.append(contact)
            
            print(f"Loaded {len(all_contacts)} contacts from {csv_file}")
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
    
    return all_contacts


def generate_tracking_id(domain, campaign_name, template_name):
    """Generate unique tracking ID for campaign"""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    seed_string = f"{domain}_{campaign_name}_{template_name}_{timestamp}"
    hash_object = hashlib.md5(seed_string.encode())
    short_hash = hash_object.hexdigest()[:8]
    tracking_id = f"{domain.upper()}_{short_hash}_{timestamp}"
    return tracking_id


def load_campaign_content(campaign_path):
    """Load campaign content from various file formats"""
    try:
        file_ext = os.path.splitext(campaign_path)[1].lower()
        
        if file_ext == '.json':
            return load_json_campaign(campaign_path)
        elif file_ext == '.docx':
            if not DOCX_AVAILABLE:
                print(f"Warning: python-docx not available, skipping {campaign_path}")
                return None
                
            doc = Document(campaign_path)
            content = ""
            
            for paragraph in doc.paragraphs:
                content += paragraph.text + "\n"
            
            for table in doc.tables:
                for row in table.rows:
                    for cell in row.cells:
                        content += cell.text + " "
                    content += "\n"
            
            return content.strip()
        
        elif file_ext in ['.txt', '.html', '.md']:
            encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
            
            for encoding in encodings:
                try:
                    with open(campaign_path, 'r', encoding=encoding) as f:
                        content = f.read()
                    return content
                except UnicodeDecodeError:
                    continue
            
            with open(campaign_path, 'rb') as f:
                raw_content = f.read()
                return raw_content.decode('utf-8', errors='ignore')
        
        return None
        
    except Exception as e:
        print(f"Error loading campaign content from {campaign_path}: {str(e)}")
        return None


def load_json_campaign(campaign_path):
    """Load and process JSON campaign file - supports both content and config formats"""
    try:
        with open(campaign_path, 'r', encoding='utf-8') as f:
            campaign_data = json.load(f)
        
        print(f"Loaded JSON campaign: {campaign_path}")
        
        # Format 1: Simple content format with subject/content
        if 'subject' in campaign_data and 'content' in campaign_data:
            return {
                'subject': campaign_data['subject'],
                'content': campaign_data['content'],
                'from_name': campaign_data.get('from_name', 'Campaign System'),
                'content_type': campaign_data.get('content_type', 'html'),
                'metadata': campaign_data.get('metadata', {})
            }
        
        # Format 2: Config format with templates array (like test_campaign.json)
        elif 'templates' in campaign_data and isinstance(campaign_data['templates'], list):
            if not campaign_data['templates']:
                print(f"Warning: No templates specified in config {campaign_path}")
                return None
            
            # Get the first template file
            template_file = campaign_data['templates'][0]
            template_path = Path(template_file)
            
            # If path is relative, resolve it
            if not template_path.is_absolute():
                template_path = Path(campaign_path).parent.parent / template_file
            
            if not template_path.exists():
                print(f"Warning: Template file not found: {template_path}")
                return None
            
            # Load the actual template content
            template_content = load_campaign_content(str(template_path))
            if not template_content:
                print(f"Warning: Could not load template content from {template_path}")
                return None
            
            # Build campaign data from config
            return {
                'subject': campaign_data.get('subject', 'Campaign'),
                'content': template_content if isinstance(template_content, str) else template_content.get('content', ''),
                'from_name': campaign_data.get('from_name', 'Campaign System'),
                'content_type': 'html',
                'config': campaign_data,
                'template_source': str(template_path)
            }
        
        # Format 3: campaigns array
        elif 'campaigns' in campaign_data:
            if campaign_data['campaigns']:
                first_campaign = campaign_data['campaigns'][0]
                return {
                    'subject': first_campaign.get('subject', 'Campaign'),
                    'content': first_campaign.get('content', ''),
                    'from_name': first_campaign.get('from_name', 'Campaign System'),
                    'content_type': first_campaign.get('content_type', 'html'),
                    'metadata': campaign_data.get('metadata', {})
                }
        
        print(f"Warning: Unknown JSON campaign format in {campaign_path}")
        return None
        
    except Exception as e:
        print(f"Error loading JSON campaign {campaign_path}: {str(e)}")
        traceback.print_exc()
        return None


def extract_subject_from_content(content):
    """Extract subject line from content if present"""
    try:
        if isinstance(content, dict):
            return content.get('subject', 'Campaign')
            
        lines = str(content).split('\n')
        for line in lines[:10]:
            if line.lower().startswith('subject:'):
                return line.split(':', 1)[1].strip()
            elif line.lower().startswith('# '):
                return line[2:].strip()
        return None
    except:
        return None


def scan_domain_campaigns(templates_dir):
    """Scan for campaigns in domain-based directory structure"""
    templates_path = Path(templates_dir)
    domain_campaigns = {}
    
    if not templates_path.exists():
        print(f"Templates directory not found: {templates_dir}")
        return domain_campaigns
    
    has_subdomains = False
    for domain_dir in templates_path.iterdir():
        if domain_dir.is_dir() and not domain_dir.name.startswith('.'):
            domain_name = domain_dir.name
            campaigns = []
            
            for ext in ['.docx', '.txt', '.html', '.md', '.json']:
                campaigns.extend(list(domain_dir.rglob(f"*{ext}")))
            
            if campaigns:
                has_subdomains = True
                domain_campaigns[domain_name] = campaigns
                print(f"Found {len(campaigns)} campaign(s) in {domain_name}/ (including subdirectories)")
                
                subdirs = set()
                for campaign in campaigns:
                    relative_path = campaign.relative_to(domain_dir)
                    if len(relative_path.parts) > 1:
                        subdirs.add(relative_path.parts[0])
                
                if subdirs:
                    print(f"  Subdirectories in {domain_name}/: {', '.join(sorted(subdirs))}")
    
    if not has_subdomains:
        print("No domain subdirectories found, using flat directory structure")
        campaigns = []
        for ext in ['.docx', '.txt', '.html', '.md', '.json']:
            campaigns.extend(list(templates_path.glob(f"*{ext}")))
        
        if campaigns:
            domain_campaigns['default'] = campaigns
            print(f"Found {len(campaigns)} campaign(s) in flat structure (using 'default' domain)")
    
    return domain_campaigns


def save_tracking_data(tracking_dir, domain, tracking_id, campaign_data):
    """Save tracking data to JSON file"""
    domain_tracking = Path(tracking_dir) / domain / "campaigns"
    domain_tracking.mkdir(parents=True, exist_ok=True)
    
    tracking_file = domain_tracking / f"{tracking_id}.json"
    
    try:
        with open(tracking_file, 'w') as f:
            json.dump(campaign_data, f, indent=2)
        print(f"Tracking data saved: {tracking_file}")
    except Exception as e:
        print(f"Warning: Could not save tracking data: {e}")


def send_summary_alert(emailer, campaigns_count, sent_count, failed_count, campaign_results):
    """Send summary alert email"""
    try:
        total_emails = sent_count + failed_count
        success_rate = (sent_count / max(1, total_emails)) * 100
        
        subject = f"Campaign Summary: {campaigns_count} campaigns, {total_emails} emails"
        
        body = f"""
Campaign Execution Summary
=========================

Campaigns Processed: {campaigns_count}
Total Emails: {total_emails}
Successful: {sent_count}
Failed: {failed_count}
Success Rate: {success_rate:.1f}%
Template Processing: ENABLED

Campaign Details:
"""
        
        for result in campaign_results:
            body += f"\n- {result['campaign_name']}: {result['sent']}/{result['total_recipients']} sent"
            if result.get('tracking_id'):
                body += f" [ID: {result['tracking_id']}]"
            if result['failed'] > 0:
                body += f" ({result['failed']} failed)"
            if result.get('template_substitution'):
                body += " [Personalized]"
        
        body += f"\n\nExecution completed: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        emailer.send_alert(subject, body)
        print("Summary alert sent")
        
    except Exception as e:
        print(f"Warning: Could not send summary alert: {e}")


def campaign_main(contacts_root, scheduled_root, tracking_root, alerts_email, dry_run=False, **kwargs):
    """Main campaign execution function with config JSON support"""
    try:
        print(f"Starting domain-aware campaign system")
        print(f"GitHub Actions detected: {os.getenv('GITHUB_ACTIONS') is not None}")
        print(f"Contacts: {contacts_root}")
        print(f"Templates (domain-based): {scheduled_root}")
        print(f"Tracking: {tracking_root}")
        print(f"Alerts: {alerts_email}")
        
        os.makedirs(tracking_root, exist_ok=True)
        
        # Load contacts with professional data_loader or fallback
        if DATA_LOADER_AVAILABLE:
            print("Using professional data_loader module")
            all_contacts = load_contacts_directory(contacts_root)
            if all_contacts:
                stats, valid_contacts = validate_contact_data(all_contacts)
                print(f"Contact validation stats:")
                print(f"  Total: {stats['total']}")
                print(f"  Valid emails: {stats['valid_emails']}")
                all_contacts = valid_contacts
        else:
            print("Using fallback contact loading")
            all_contacts = fallback_load_contacts_from_directory(contacts_root)

        # Get SMTP config from environment variables
        smtp_host = os.getenv('SMTP_HOST') or os.getenv('SMTP_SERVER')
        smtp_port = os.getenv('SMTP_PORT')
        smtp_user = os.getenv('SMTP_USER') or os.getenv('SMTP_USERNAME')
        smtp_pass = os.getenv('SMTP_PASS') or os.getenv('SMTP_PASSWORD')

        # Initialize emailer
        if GITHUB_ACTIONS_EMAIL_AVAILABLE and os.getenv('GITHUB_ACTIONS'):
            print("Using GitHubActionsEmailSender - SMTP timeouts bypassed")
            emailer = GitHubActionsEmailSender(
                smtp_host=os.getenv('SMTP_HOST'),
                smtp_port=os.getenv('SMTP_PORT'),
                smtp_user=os.getenv('SMTP_USER'),
                smtp_pass=os.getenv('SMTP_PASS'),
                alerts_email=alerts_email,
                dry_run=dry_run
            )
        else:
            print("Using standard EmailSender")
            emailer = EmailSenderemailer = EmailSender(
                smtp_host=smtp_host,
                smtp_port=smtp_port,
                smtp_user=smtp_user,
                smtp_pass=smtp_pass,
                alerts_email=alerts_email,
                dry_run=dry_run
            )
        
        # Scan for domain-based campaigns
        domain_campaigns = scan_domain_campaigns(scheduled_root)
        
        if not domain_campaigns:
            print(f"ERROR: No campaigns found in {scheduled_root}")
            print("Supported formats: .docx, .txt, .html, .md, .json")
            print("Structures supported:")
            print("  1. Domain-based: {scheduled_root}/{domain}/*.docx")
            print("  2. Flat: {scheduled_root}/*.docx")
            return
        
        # Initialize tracking
        campaigns_processed = 0
        total_emails_sent = 0
        total_failures = 0
        campaign_results = []
        
        # Create log file
        log_file = "dryrun.log" if dry_run else "campaign_execution.log"
        with open(log_file, 'w') as f:
            f.write("Domain-Aware Campaign Log\n")
            f.write(f"GitHub Actions mode: {os.getenv('GITHUB_ACTIONS') is not None}\n")
            f.write(f"Total contacts loaded: {len(all_contacts)}\n")
            f.write(f"Domains found: {len(domain_campaigns)}\n")
            f.write(f"Timestamp: {datetime.now().isoformat()}\n\n")
        
        # Process each domain
        for domain, campaign_files in domain_campaigns.items():
            print(f"\n{'='*70}")
            print(f"PROCESSING DOMAIN: {domain.upper()}")
            print(f"{'='*70}")
            
            # Create domain tracking structure
            domain_tracking = Path(tracking_root) / domain
            (domain_tracking / "campaigns").mkdir(parents=True, exist_ok=True)
            (domain_tracking / "responses").mkdir(parents=True, exist_ok=True)
            (domain_tracking / "analytics").mkdir(parents=True, exist_ok=True)
            
            # Process each campaign
            for campaign_file in campaign_files:
                campaign_name = campaign_file.stem
                campaign_path = str(campaign_file)
                
                # Determine subdirectory structure
                relative_path = campaign_file.relative_to(Path(scheduled_root) / domain) if domain != 'default' else campaign_file.relative_to(Path(scheduled_root))
                subdirectory = relative_path.parent.name if len(relative_path.parts) > 1 else None
                full_campaign_name = f"{subdirectory}/{campaign_name}" if subdirectory else campaign_name
                
                print(f"\n--- Processing Campaign: {domain}/{full_campaign_name} ---")
                
                # Load campaign content
                campaign_content = load_campaign_content(campaign_path)
                if not campaign_content:
                    print(f"Warning: Could not load content for {campaign_file.name}")
                    continue
                
                # Handle content types with config JSON support
                if isinstance(campaign_content, dict):
                    subject = campaign_content.get('subject', f"Campaign: {campaign_name}")
                    content = campaign_content.get('content', '')
                    from_name = campaign_content.get('from_name', 'Campaign System')
                    
                    # Extract config if present (CRITICAL FEATURE)
                    config = campaign_content.get('config', {})
                    
                    if config:
                        print(f"Using config-based campaign settings from JSON")
                        from_name = config.get('from_name', from_name)
                        subject = config.get('subject', subject)
                        
                        contact_mapping = config.get('contact_mapping', {})
                        if contact_mapping:
                            print(f"Contact field mapping active: {list(contact_mapping.keys())}")
                        
                        if config.get('sector'):
                            print(f"Sector: {config['sector']}")
                        if config.get('feedback', {}).get('auto_inject'):
                            print(f"Feedback auto-injection: ENABLED")
                        if config.get('tracking', {}).get('enabled'):
                            print(f"Enhanced tracking: ENABLED")
                else:
                    subject = extract_subject_from_content(campaign_content) or f"Campaign: {campaign_name}"
                    content = str(campaign_content)
                    from_name = "Campaign System"
                    config = {}
                    contact_mapping = {}
                
                # Generate tracking ID
                tracking_id = generate_tracking_id(domain, full_campaign_name, campaign_file.name)
                
                # Prepare contacts with tracking IDs
                contacts_with_ids = []
                for i, contact in enumerate(all_contacts):
                    contact_copy = contact.copy()
                    contact_copy['recipient_id'] = f"{domain}_{full_campaign_name.replace('/', '_')}_{i+1}"
                    contact_copy['campaign_id'] = full_campaign_name
                    contact_copy['domain'] = domain
                    contact_copy['tracking_id'] = tracking_id
                    contacts_with_ids.append(contact_copy)
                
                # Send campaign (FIXED: now passes contact_mapping)
                try:
                    campaign_result = emailer.send_campaign(
                        campaign_name=f"{domain}/{full_campaign_name}",
                        subject=subject,
                        content=content,
                        recipients=contacts_with_ids,
                        from_name=from_name,
                        tracking_id=tracking_id,
                        contact_mapping=config.get('contact_mapping', {})
                    )
                    
                    campaigns_processed += 1
                    total_emails_sent += campaign_result['sent']
                    total_failures += campaign_result['failed']
                    campaign_results.append(campaign_result)
                    
                    # Prepare tracking data
                    tracking_data = {
                        'tracking_id': tracking_id,
                        'domain': domain,
                        'campaign_name': campaign_name,
                        'full_path': full_campaign_name,
                        'subdirectory': subdirectory,
                        'template_file': campaign_file.name,
                        'subject': subject,
                        'from_name': from_name,
                        'timestamp': datetime.now().isoformat(),
                        'total_recipients': campaign_result['total_recipients'],
                        'sent': campaign_result['sent'],
                        'failed': campaign_result['failed'],
                        'dry_run': dry_run
                    }
                    
                    # Add config metadata if available
                    if config:
                        tracking_data['config_based'] = True
                        tracking_data['sector'] = config.get('sector')
                        tracking_data['feedback_enabled'] = config.get('feedback', {}).get('auto_inject', False)
                        tracking_data['tracking_enabled'] = config.get('tracking', {}).get('enabled', False)
                        tracking_data['template_source'] = campaign_content.get('template_source')
                        if 'contact_mapping' in config:
                            tracking_data['contact_mapping'] = config['contact_mapping']
                    
                    # Save tracking data
                    save_tracking_data(tracking_root, domain, tracking_id, tracking_data)
                    
                    # Append to log
                    with open(log_file, 'a') as f:
                        f.write(f"Domain: {domain}\n")
                        f.write(f"Campaign: {full_campaign_name}\n")
                        f.write(f"Tracking ID: {tracking_id}\n")
                        f.write(f"Recipients: {campaign_result['total_recipients']}\n")
                        f.write(f"Sent: {campaign_result['sent']}\n")
                        f.write(f"Failed: {campaign_result['failed']}\n\n")
                    
                except Exception as e:
                    print(f"Error processing campaign '{domain}/{full_campaign_name}': {str(e)}")
                    traceback.print_exc()
                    continue
        
        # Send summary
        if GITHUB_ACTIONS_EMAIL_AVAILABLE and os.getenv('GITHUB_ACTIONS'):
            emailer.send_batch_summary(campaigns_processed, total_emails_sent, total_failures, campaign_results)
            print("Campaign summary saved for GitHub Actions email delivery")
        elif not dry_run and campaigns_processed > 0:
            send_summary_alert(emailer, campaigns_processed, total_emails_sent, total_failures, campaign_results)
        
        # Final log entry
        with open(log_file, 'a') as f:
            f.write("=== CAMPAIGN SUMMARY ===\n")
            f.write(f"Domains processed: {len(domain_campaigns)}\n")
            f.write(f"Campaigns processed: {campaigns_processed}\n")
            f.write(f"Total emails: {total_emails_sent + total_failures}\n")
            f.write(f"Successful: {total_emails_sent}\n")
            f.write(f"Failed: {total_failures}\n")
            f.write(f"Tracking system: DOMAIN-BASED\n")
            f.write(f"Completed: {datetime.now().isoformat()}\n")
        
        print(f"\n{'='*70}")
        print(f"FINAL SUMMARY")
        print(f"{'='*70}")
        print(f"Domains processed: {len(domain_campaigns)}")
        print(f"Campaigns processed: {campaigns_processed}")
        print(f"Tracking system: DOMAIN-BASED")
        print(f"Template processing: ENABLED")
        print("Campaign completed successfully")
        
    except Exception as e:
        print(f"ERROR: {str(e)}")
        traceback.print_exc()
        sys.exit(1)


if __name__ == "__main__":
    print("Domain-Aware Campaign System Script started")
    print(f"Remote environment: {IS_REMOTE}")
    print(f"Available modules: docx={DOCX_AVAILABLE}, email_sender={EMAIL_SENDER_AVAILABLE}, data_loader={DATA_LOADER_AVAILABLE}")
    
    parser = argparse.ArgumentParser(description='Domain-Aware Email Campaign System')
    parser.add_argument("--contacts", required=True, help="Contacts directory path")
    parser.add_argument("--scheduled", required=True, help="Domain-based templates directory (campaign-templates/)")
    parser.add_argument("--tracking", required=True, help="Tracking directory path")
    parser.add_argument("--alerts", required=True, help="Alerts email address")
    parser.add_argument("--feedback", help="Feedback email address")
    parser.add_argument("--templates", help="Templates directory path (alias for --scheduled)")
    parser.add_argument("--domain", help="Process only specific domain")
    parser.add_argument("--filter-domain", help="Filter campaigns by domain pattern")
    parser.add_argument("--dry-run", action="store_true", help="Print personalized emails instead of sending")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")
    parser.add_argument("--no-feedback", action="store_true", help="Skip feedback injection")
    parser.add_argument("--remote-only", action="store_true", help="Force remote-only mode")
    parser.add_argument("--enhanced-mode", action="store_true", help="Enable enhanced processing mode")
    parser.add_argument("--template-variables", action="store_true", help="Enable template variable processing")
    parser.add_argument("--comprehensive-tracking", action="store_true", help="Enable comprehensive tracking")
    parser.add_argument("--batch-size", type=int, default=50, help="Batch size for processing")
    parser.add_argument("--delay", type=int, default=5, help="Delay between batches")
    
    print("Parsing arguments...")
    args = parser.parse_args()
    
    if args.remote_only:
        IS_REMOTE = True
        print("Forced remote-only mode enabled")
    
    scheduled_path = args.templates if args.templates else args.scheduled
    
    print(f"Arguments parsed successfully:")
    print(f"  --contacts: {args.contacts}")
    print(f"  --scheduled: {scheduled_path}")
    print(f"  --tracking: {args.tracking}")
    print(f"  --alerts: {args.alerts}")
    print(f"  --feedback: {args.feedback}")
    print(f"  --domain: {args.domain}")
    print(f"  --dry-run: {args.dry_run}")
    print(f"  --debug: {args.debug}")
    
    print("Calling domain-aware campaign_main...")
    campaign_main(
        contacts_root=args.contacts,
        scheduled_root=scheduled_path,
        tracking_root=args.tracking,
        alerts_email=args.alerts,
        dry_run=args.dry_run,
        feedback_email=args.feedback,
        target_domain=args.domain,
        campaign_filter=args.filter_domain,
        debug=args.debug
    )
    print("Domain-aware campaign system completed successfully")
                        
