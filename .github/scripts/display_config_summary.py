#!/usr/bin/env python3
"""
Display campaign configuration summary
"""
import json
import sys
import os
from pathlib import Path

def display_config_summary(config_file):
    """Display configuration summary in a formatted way"""
    
    if not config_file or not os.path.exists(config_file):
        print("❌ Configuration file not accessible")
        return False
    
    try:
        with open(config_file, 'r') as f:
            config = json.load(f)
        
        print("=" * 70)
        print("  Campaign Configuration Summary")
        print("=" * 70)
        print()
        
        # Basic Information
        print("📋 Basic Information:")
        print(f"  Campaign Name: {config.get('name', 'N/A')}")
        print(f"  Sector: {config.get('sector', 'N/A')}")
        print(f"  Mode: {config.get('mode', 'N/A')}")
        print()
        
        # Email Settings
        print("📧 Email Settings:")
        print(f"  Subject: {config.get('subject', 'N/A')}")
        print(f"  From Email: {config.get('from_email', 'N/A')}")
        print(f"  Reply-To: {config.get('reply_to', 'N/A')}")
        print()
        
        # Contacts
        print("👥 Contacts:")
        contacts_file = config.get('contacts', 'N/A')
        print(f"  Contacts File: {contacts_file}")
        
        if contacts_file != 'N/A' and os.path.exists(contacts_file):
            try:
                with open(contacts_file, 'r') as cf:
                    lines = sum(1 for _ in cf) - 1  # Subtract header
                print(f"  Contact Count: {lines} contacts")
            except:
                print(f"  Contact Count: Unable to read")
        print()
        
        # Templates
        print("📄 Templates:")
        templates = config.get('templates', [])
        if isinstance(templates, str):
            templates = [templates]
        
        print(f"  Template Count: {len(templates)} file(s)")
        for i, t in enumerate(templates, 1):
            template_path = Path(t)
            exists = "✅" if template_path.exists() else "❌"
            size = f"({template_path.stat().st_size} bytes)" if template_path.exists() else "(not found)"
            print(f"    {i}. {exists} {t} {size}")
        print()
        
        # Rate Limiting
        rate_limiting = config.get('rate_limiting', {})
        if rate_limiting:
            print("⏱️  Rate Limiting:")
            print(f"  Delay between emails: {rate_limiting.get('delay_between_emails', 1.0)}s")
            print(f"  Batch size: {rate_limiting.get('batch_size', 50)}")
            print(f"  Delay between batches: {rate_limiting.get('delay_between_batches', 5)}s")
            print()
        
        # Feedback System
        feedback = config.get('feedback', {})
        if feedback:
            print("💬 Feedback System:")
            auto_inject = feedback.get('auto_inject', False)
            print(f"  Status: {'✅ Enabled' if auto_inject else '❌ Disabled'}")
            print(f"  Feedback Email: {feedback.get('email', 'N/A')}")
            if feedback.get('tracking_id_prefix'):
                print(f"  Tracking ID Prefix: {feedback.get('tracking_id_prefix')}")
            print()
        
        # SMTP Configuration
        smtp = config.get('smtp', {})
        if smtp:
            print("📮 SMTP Configuration:")
            print(f"  Host: {smtp.get('host', 'N/A')}")
            print(f"  Port: {smtp.get('port', 'N/A')}")
            
            # Handle both 'user' and 'username'
            user = smtp.get('username') or smtp.get('user', 'N/A')
            print(f"  Username: {user}")
            
            # Show if password is set (masked)
            password = smtp.get('password') or smtp.get('pass')
            if password:
                if isinstance(password, str) and password.startswith('${'):
                    print(f"  Password: {password} (env var)")
                else:
                    print(f"  Password: {'*' * 8} (set)")
            else:
                print(f"  Password: Not set")
            
            print(f"  Use TLS: {smtp.get('use_tls', True)}")
            print(f"  Timeout: {smtp.get('timeout', 30)}s")
            print()
        
        # Additional Settings
        print("⚙️  Additional Settings:")
        
        tracking = config.get('tracking', {})
        if tracking:
            print(f"  Tracking Enabled: {tracking.get('enabled', False)}")
        
        test_mode = config.get('test_mode', False)
        print(f"  Test Mode: {test_mode}")
        
        dry_run = config.get('dry_run', False)
        print(f"  Dry Run: {dry_run}")
        
        max_recipients = config.get('max_recipients')
        if max_recipients:
            print(f"  Max Recipients: {max_recipients}")
        
        print()
        print("=" * 70)
        
        return True
        
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing JSON configuration: {e}")
        return False
    except Exception as e:
        print(f"❌ Error reading configuration: {e}")
        import traceback
        traceback.print_exc()
        return False

def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python display_config_summary.py <config_file>")
        print("\nExample:")
        print("  python display_config_summary.py scheduled-campaigns/campaign.json")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    success = display_config_summary(config_file)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
