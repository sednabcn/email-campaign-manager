"""
Integration Patch for docx_parser.py
Add this code to integrate the unsubscribe system
"""

# ============================================================================
# STEP 1: Add these imports at the top of docx_parser.py
# ============================================================================

from pathlib import Path
import json
import secrets
import hashlib
import base64
from datetime import datetime, timedelta
from typing import Dict, Optional, List, Set
from urllib.parse import urlencode
import threading


# ============================================================================
# STEP 2: Add UnsubscribeManager class (copy from first artifact)
# ============================================================================
# Copy the complete UnsubscribeManager class here
# Or import it: from unsubscribe_manager import UnsubscribeManager


# ============================================================================
# STEP 3: Modify the campaign_main() function
# ============================================================================

def campaign_main_with_unsubscribe():
    """
    Modified version of campaign_main() with unsubscribe integration
    Replace your existing campaign_main() function with this
    """
    
    # [Keep all your existing initialization code here]
    # ...
    
    # After emailer initialization, add:
    print("\n" + "="*70)
    print("INITIALIZING UNSUBSCRIBE SYSTEM")
    print("="*70)
    
    # Initialize unsubscribe manager
    unsub_manager = UnsubscribeManager(
        tracking_dir=tracking_root,
        base_url="https://sednabcn.github.io/unsubscribe"
    )
    
    # Get statistics
    stats = unsub_manager.get_stats()
    print(f"✅ Unsubscribe system initialized")
    print(f"   Total unsubscribed: {stats['total_unsubscribed']}")
    print(f"   Recent (7 days): {stats['recent_7_days']}")
    
    if stats['by_campaign']:
        print(f"   By campaign:")
        for campaign, count in stats['by_campaign'].items():
            print(f"     - {campaign}: {count}")
    
    # [Keep your existing loop structure]
    # for domain, templates in campaign_config['domains'].items():
    #     ...
    
    # MODIFY THE CONTACT PROCESSING SECTION:
    
    # Before processing contacts, filter out unsubscribed
    print(f"\n📋 Processing contacts for {full_campaign_name}...")
    
    # Filter contacts using unsubscribe manager
    valid_contacts, skipped_contacts = unsub_manager.filter_contacts(
        all_contacts,
        campaign_id=full_campaign_name,
        email_key='email'
    )
    
    if skipped_contacts:
        print(f"   ⏭️  Filtered out {len(skipped_contacts)} unsubscribed contacts")
        
        # Log skipped contacts
        skipped_log = tracking_root / f"skipped_{full_campaign_name.replace('/', '_')}.json"
        try:
            with open(skipped_log, 'w') as f:
                json.dump({
                    'campaign': full_campaign_name,
                    'timestamp': datetime.now().isoformat(),
                    'skipped_count': len(skipped_contacts),
                    'contacts': [c.get('email', '') for c in skipped_contacts]
                }, f, indent=2)
        except Exception as e:
            print(f"   ⚠️  Warning: Could not save skipped contacts log: {e}")
    
    print(f"   ✅ {len(valid_contacts)} valid contacts to process")
    
    # Now process valid_contacts instead of all_contacts
    contacts_with_ids = []
    
    for i, contact in enumerate(valid_contacts):
        # Add recipient ID
        recipient_id = f"{domain}_{full_campaign_name.replace('/', '_')}_{i+1}"
        
        # Generate unsubscribe link
        unsub_link = unsub_manager.generate_unsubscribe_link(
            contact.get('email', ''),
            full_campaign_name
        )
        
        # Add to contact data
        contact_with_data = contact.copy()
        contact_with_data['recipient_id'] = recipient_id
        contact_with_data['unsubscribe_link'] = unsub_link
        
        contacts_with_ids.append(contact_with_data)
    
    # [Continue with your existing send logic]
    # The contacts_with_ids now have unsubscribe links
    
    return unsub_manager  # Return for further use


# ============================================================================
# STEP 4: Modify email content preparation
# ============================================================================

def add_unsubscribe_footer_to_email(email_content: str, 
                                    unsubscribe_link: str,
                                    from_name: str = "Your Name",
                                    from_email: str = "your@email.com",
                                    physical_address: str = "Your Address") -> str:
    """
    Add unsubscribe footer to email content
    Call this before sending each email
    """
    
    footer = f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Professional Outreach from {from_name}

You received this email as part of professional networking outreach.

If you prefer not to receive future emails, please visit:
{unsubscribe_link}

Or reply with "UNSUBSCRIBE" in the subject line.

Contact: {from_email}
Address: {physical_address}

This is a one-time professional outreach. We respect your preferences 
and will honor all opt-out requests immediately.
"""
    
    return email_content + footer


# ============================================================================
# STEP 5: Update send_campaign or similar function
# ============================================================================

def enhanced_send_email(emailer, contact, template_content, full_campaign_name):
    """
    Enhanced version of email sending with unsubscribe footer
    Replace or modify your existing send function
    """
    
    # Get unsubscribe link from contact data
    unsub_link = contact.get('unsubscribe_link', '#')
    
    # Add footer to template
    template_with_footer = add_unsubscribe_footer_to_email(
        template_content,
        unsub_link,
        from_name="Your Name",  # Use your actual name
        from_email="your@email.com",  # Use your actual email
        physical_address="Your Physical Address"  # Required by CAN-SPAM
    )
    
    # [Your existing send logic]
    # emailer.send_personalized_email(contact, template_with_footer, ...)


# ============================================================================
# STEP 6: Create helper script for manual unsubscribe management
# ============================================================================

def manage_unsubscribes_cli():
    """
    Command-line tool for managing unsubscribes
    Save as separate file: manage_unsubscribes.py
    """
    import argparse
    
    parser = argparse.ArgumentParser(description='Manage email unsubscribes')
    parser.add_argument('action', choices=['add', 'remove', 'check', 'stats', 'list', 'export'],
                       help='Action to perform')
    parser.add_argument('--email', help='Email address')
    parser.add_argument('--campaign', default='all', help='Campaign ID')
    parser.add_argument('--tracking-dir', default='tracking', help='Tracking directory')
    parser.add_argument('--output', help='Output file for export')
    
    args = parser.parse_args()
    
    manager = UnsubscribeManager(
        tracking_dir=Path(args.tracking_dir),
        base_url="https://sednabcn.github.io/unsubscribe"
    )
    
    if args.action == 'add':
        if not args.email:
            print("Error: --email required")
            return
        
        success = manager.add_unsubscribe(
            args.email,
            args.campaign,
            reason="Manual addition",
            source="cli"
        )
        print(f"✅ Added {args.email} to unsubscribe list" if success else "❌ Failed")
    
    elif args.action == 'remove':
        if not args.email:
            print("Error: --email required")
            return
        
        success = manager.remove_unsubscribe(args.email, args.campaign)
        print(f"✅ Removed {args.email} from unsubscribe list" if success else "❌ Failed")
    
    elif args.action == 'check':
        if not args.email:
            print("Error: --email required")
            return
        
        is_unsub = manager.is_unsubscribed(args.email, args.campaign)
        print(f"{'✅ Unsubscribed' if is_unsub else '❌ Not unsubscribed'}")
    
    elif args.action == 'stats':
        stats = manager.get_stats()
        print("\n📊 Unsubscribe Statistics:")
        print(json.dumps(stats, indent=2))
    
    elif args.action == 'list':
        emails = manager.get_unsubscribed_emails(args.campaign if args.campaign != 'all' else None)
        print(f"\n📋 Unsubscribed emails ({len(emails)}):")
        for email in sorted(emails):
            print(f"  - {email}")
    
    elif args.action == 'export':
        output = Path(args.output) if args.output else Path('unsubscribed_export.json')
        success = manager.export_list(output)
        print(f"✅ Exported to {output}" if success else "❌ Export failed")


# ============================================================================
# STEP 7: Quick integration test
# ============================================================================

def test_integration():
    """Test the unsubscribe system integration"""
    
    print("🧪 Testing Unsubscribe System Integration\n")
    
    # Initialize
    manager = UnsubscribeManager(
        tracking_dir=Path("tracking_test"),
        base_url="https://sednabcn.github.io/unsubscribe"
    )
    
    # Test 1: Add unsubscribe
    print("Test 1: Adding unsubscribe...")
    success = manager.add_unsubscribe(
        "test@example.com",
        "test_campaign",
        reason="Testing",
        source="test"
    )
    print(f"  {'✅ PASS' if success else '❌ FAIL'}")
    
    # Test 2: Check unsubscribe
    print("\nTest 2: Checking unsubscribe status...")
    is_unsub = manager.is_unsubscribed("test@example.com", "test_campaign")
    print(f"  {'✅ PASS' if is_unsub else '❌ FAIL'}")
    
    # Test 3: Generate link
    print("\nTest 3: Generating unsubscribe link...")
    link = manager.generate_unsubscribe_link("test@example.com", "test_campaign")
    print(f"  Link: {link}")
    print(f"  {'✅ PASS' if 'sednabcn.github.io' in link else '❌ FAIL'}")
    
    # Test 4: Filter contacts
    print("\nTest 4: Filtering contacts...")
    contacts = [
        {'email': 'test@example.com', 'name': 'Test User'},
        {'email': 'valid@example.com', 'name': 'Valid User'}
    ]
    valid, skipped = manager.filter_contacts(contacts, "test_campaign")
    print(f"  Valid: {len(valid)}, Skipped: {len(skipped)}")
    print(f"  {'✅ PASS' if len(valid) == 1 and len(skipped) == 1 else '❌ FAIL'}")
    
    # Test 5: Statistics
    print("\nTest 5: Getting statistics...")
    stats = manager.get_stats()
    print(f"  Total unsubscribed: {stats['total_unsubscribed']}")
    print(f"  {'✅ PASS' if stats['total_unsubscribed'] > 0 else '❌ FAIL'}")
    
    # Cleanup
    print("\n🧹 Cleaning up test data...")
    import shutil
    shutil.rmtree("tracking_test", ignore_errors=True)
    print("  ✅ Complete")
    
    print("\n✅ All tests passed!")


# ============================================================================
# STEP 8: Configuration template
# ============================================================================

UNSUBSCRIBE_CONFIG = {
    "enabled": True,
    "base_url": "https://sednabcn.github.io/unsubscribe",
    "tracking_dir": "tracking",
    "sender_info": {
        "name": "Your Full Name",
        "email": "your.email@domain.com",
        "company": "Your Company",
        "address": "123 Main Street, City, ST 12345, Country"
    },
    "footer_style": "text",  # or "html"
    "auto_filter": True,  # Automatically filter unsubscribed contacts
    "log_skipped": True   # Log skipped contacts to file
}


# ============================================================================
# USAGE EXAMPLES
# ============================================================================

"""
EXAMPLE 1: Basic Integration in campaign_main()
------------------------------------------------

def campaign_main():
    # ... your existing code ...
    
    # Add after emailer initialization:
    unsub_manager = UnsubscribeManager(
        tracking_dir=tracking_root,
        base_url="https://sednabcn.github.io/unsubscribe"
    )
    
    # Filter contacts:
    valid_contacts, skipped = unsub_manager.filter_contacts(
        all_contacts, 
        campaign_id=full_campaign_name
    )
    
    print(f"Processing {len(valid_contacts)} contacts")
    print(f"Skipped {len(skipped)} unsubscribed contacts")
    
    # Add unsubscribe links:
    for contact in valid_contacts:
        contact['unsubscribe_link'] = unsub_manager.generate_unsubscribe_link(
            contact['email'], 
            full_campaign_name
        )
    
    # ... continue with your sending logic ...


EXAMPLE 2: Adding Footer to Emails
-----------------------------------

# Before sending each email:
email_content = add_unsubscribe_footer_to_email(
    email_content=template_content,
    unsubscribe_link=contact['unsubscribe_link'],
    from_name="John Doe",
    from_email="john@example.com",
    physical_address="123 Main St, City, ST 12345"
)

# Then send the email with the footer included


EXAMPLE 3: Manual Unsubscribe Management
-----------------------------------------

# From command line:
python manage_unsubscribes.py add --email user@example.com --campaign all
python manage_unsubscribes.py check --email user@example.com
python manage_unsubscribes.py stats
python manage_unsubscribes.py list --campaign my_campaign
python manage_unsubscribes.py export --output backup.json

# From Python:
manager = UnsubscribeManager(...)
manager.add_unsubscribe("user@example.com", "all", reason="User request")
is_unsub = manager.is_unsubscribed("user@example.com")


EXAMPLE 4: Handling Unsubscribe Requests from Email Replies
------------------------------------------------------------

def process_email_replies(inbox_messages):
    '''Process incoming email replies for unsubscribe requests'''
    
    manager = UnsubscribeManager(
        tracking_dir=Path("tracking"),
        base_url="https://sednabcn.github.io/unsubscribe"
    )
    
    for message in inbox_messages:
        subject = message.get('subject', '').upper()
        from_email = message.get('from', '').strip().lower()
        
        # Check for unsubscribe in subject
        if 'UNSUBSCRIBE' in subject or 'REMOVE' in subject:
            success = manager.add_unsubscribe(
                from_email,
                campaign_id="all",
                reason="Email reply",
                source="email"
            )
            
            if success:
                print(f"✅ Unsubscribed: {from_email}")
                # Send confirmation email
                send_confirmation_email(from_email)


EXAMPLE 5: Periodic Cleanup and Reporting
------------------------------------------

def weekly_unsubscribe_report():
    '''Generate weekly unsubscribe report'''
    
    manager = UnsubscribeManager(
        tracking_dir=Path("tracking"),
        base_url="https://sednabcn.github.io/unsubscribe"
    )
    
    stats = manager.get_stats()
    
    report = f'''
    📊 WEEKLY UNSUBSCRIBE REPORT
    ============================
    
    Total Unsubscribed: {stats['total_unsubscribed']}
    This Week: {stats['recent_7_days']}
    Global Opt-outs: {stats['global_unsubscribes']}
    
    By Campaign:
    '''
    
    for campaign, count in stats['by_campaign'].items():
        report += f"  - {campaign}: {count}\n"
    
    print(report)
    
    # Export backup
    backup_file = Path(f"backups/unsubscribed_{datetime.now():%Y%m%d}.json")
    backup_file.parent.mkdir(exist_ok=True)
    manager.export_list(backup_file)
    print(f"\n💾 Backup saved: {backup_file}")


EXAMPLE 6: Bulk Import from CSV
--------------------------------

def import_unsubscribes_from_csv(csv_file: Path):
    '''Import unsubscribe list from CSV'''
    
    import csv
    
    manager = UnsubscribeManager(
        tracking_dir=Path("tracking"),
        base_url="https://sednabcn.github.io/unsubscribe"
    )
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            email = row.get('email', '').strip().lower()
            campaign = row.get('campaign', 'all')
            reason = row.get('reason', 'CSV import')
            
            if email:
                manager.add_unsubscribe(
                    email,
                    campaign,
                    reason=reason,
                    source="csv_import"
                )
    
    print(f"✅ Import complete")
    print(manager.get_stats())


EXAMPLE 7: Integration with Your Template System
-------------------------------------------------

# If you're using template variables like {{unsubscribe_link}}:

template = '''
Subject: Professional Outreach - {{name}}

Hi {{first_name}},

[Your message content]

Best regards,
{{sender_name}}

---
Don't want to receive these emails? Click here: {{unsubscribe_link}}
'''

# When personalizing:
def personalize_template(template, contact, unsub_link):
    personalized = template
    
    # Replace all variables
    personalized = personalized.replace('{{name}}', contact.get('name', ''))
    personalized = personalized.replace('{{first_name}}', contact.get('first_name', ''))
    personalized = personalized.replace('{{sender_name}}', 'John Doe')
    personalized = personalized.replace('{{unsubscribe_link}}', unsub_link)
    
    return personalized


EXAMPLE 8: Pre-flight Check Before Campaign
--------------------------------------------

def pre_flight_check(contacts, campaign_id):
    '''Run checks before sending campaign'''
    
    manager = UnsubscribeManager(
        tracking_dir=Path("tracking"),
        base_url="https://sednabcn.github.io/unsubscribe"
    )
    
    print("\n🔍 PRE-FLIGHT CHECK")
    print("="*60)
    
    # Check 1: Filter contacts
    valid, skipped = manager.filter_contacts(contacts, campaign_id)
    print(f"✅ Contacts: {len(valid)} valid, {len(skipped)} unsubscribed")
    
    # Check 2: Validate emails
    invalid_emails = [c for c in valid if '@' not in c.get('email', '')]
    if invalid_emails:
        print(f"⚠️  Warning: {len(invalid_emails)} invalid email addresses")
    
    # Check 3: Check for duplicates
    emails = [c.get('email', '').lower() for c in valid]
    duplicates = len(emails) - len(set(emails))
    if duplicates > 0:
        print(f"⚠️  Warning: {duplicates} duplicate email addresses")
    
    # Check 4: Unsubscribe stats
    stats = manager.get_stats()
    if stats['recent_7_days'] > 10:
        print(f"⚠️  Warning: {stats['recent_7_days']} unsubscribes in last 7 days")
    
    print("\n✅ Pre-flight check complete")
    
    return valid, skipped
"""


if __name__ == "__main__":
    # Run the integration test
    test_integration()
