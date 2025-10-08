#!/usr/bin/env python3
"""
Run email campaign from JSON configuration file
Reads config and executes using existing docx_parser.py or send_personalized_emails.py
"""
import json
import os
import sys
import argparse
import subprocess
from pathlib import Path
from datetime import datetime

def load_config(config_path):
    """Load and parse JSON configuration"""
    try:
        with open(config_path, 'r', encoding='utf-8') as f:
            config = json.load(f)
        print(f"✅ Loaded configuration: {config_path}")
        return config
    except FileNotFoundError:
        print(f"❌ Configuration file not found: {config_path}")
        sys.exit(1)
    except json.JSONDecodeError as e:
        print(f"❌ Invalid JSON in configuration file: {e}")
        sys.exit(1)

def expand_env_vars(value):
    """Expand environment variables in string values"""
    if isinstance(value, str):
        # Handle ${VAR} and $VAR syntax
        import re
        pattern = r'\$\{([^}]+)\}|\$([A-Za-z_][A-Za-z0-9_]*)'
        
        def replace(match):
            var_name = match.group(1) or match.group(2)
            return os.environ.get(var_name, match.group(0))
        
        return re.sub(pattern, replace, value)
    return value

def setup_smtp_env(smtp_config):
    """Setup SMTP environment variables from config"""
    print("\n🔧 Setting up SMTP configuration...")
    
    # Map config keys to environment variable names
    env_mapping = {
        'host': 'SMTP_SERVER',
        'port': 'SMTP_PORT',
        'user': 'SMTP_USER',
        'password': 'SMTP_PASSWORD'
    }
    
    for config_key, env_var in env_mapping.items():
        value = smtp_config.get(config_key, '')
        value = expand_env_vars(value)
        
        if value:
            os.environ[env_var] = str(value)
            masked = '*' * 8 if 'pass' in config_key.lower() else value
            print(f"  ✅ {env_var}: {masked}")
        else:
            # Check if already set in environment
            if os.environ.get(env_var):
                print(f"  ✅ {env_var}: (from environment)")
            else:
                print(f"  ⚠️  {env_var}: Not set")
    
    # Validate required variables
    required = ['SMTP_SERVER', 'SMTP_PORT', 'SMTP_USER', 'SMTP_PASSWORD']
    missing = [var for var in required if not os.environ.get(var)]
    
    if missing:
        print(f"\n❌ Missing required SMTP variables: {', '.join(missing)}")
        return False
    
    return True

def setup_mail_from(config):
    """Setup MAIL_FROM environment variable"""
    from_email = config.get('from_email', '')
    from_email = expand_env_vars(from_email)
    
    if from_email:
        os.environ['MAIL_FROM'] = from_email
        print(f"  ✅ MAIL_FROM: {from_email}")
        return True
    else:
        # Check if already in environment
        if os.environ.get('MAIL_FROM'):
            print(f"  ✅ MAIL_FROM: (from environment)")
            return True
        print("  ⚠️  MAIL_FROM: Not set")
        return False

def validate_files(config):
    """Validate that required files exist"""
    print("\n📁 Validating files...")
    
    issues = []
    
    # Check contacts file
    contacts = config.get('contacts', '')
    if contacts:
        if os.path.exists(contacts):
            try:
                with open(contacts, 'r', encoding='utf-8') as f:
                    line_count = sum(1 for _ in f)
                print(f"  ✅ Contacts: {contacts} ({line_count} lines)")
            except Exception as e:
                print(f"  ⚠️  Contacts: {contacts} (error reading: {e})")
        else:
            issues.append(f"Contacts file not found: {contacts}")
            print(f"  ❌ Contacts: {contacts} (not found)")
            
            # Try to find alternatives
            print("     Looking for alternative CSV files...")
            csv_files = list(Path('contacts').glob('*.csv')) if Path('contacts').exists() else []
            if csv_files:
                print(f"     Found {len(csv_files)} CSV files in contacts/:")
                for csv_file in csv_files[:3]:
                    print(f"       - {csv_file}")
    else:
        issues.append("No contacts file specified in config")
    
    # Check templates
    templates = config.get('templates', [])
    if isinstance(templates, str):
        templates = [templates]
    
    found_templates = []
    for template in templates:
        if os.path.exists(template):
            size = os.path.getsize(template)
            print(f"  ✅ Template: {template} ({size} bytes)")
            found_templates.append(template)
        else:
            print(f"  ⚠️  Template: {template} (not found)")
            
            # Try to find alternatives
            template_dir = os.path.dirname(template)
            if os.path.exists(template_dir):
                docx_files = list(Path(template_dir).glob('*.docx'))
                if docx_files:
                    print(f"     Found {len(docx_files)} DOCX files in {template_dir}:")
                    for docx_file in docx_files[:3]:
                        print(f"       - {docx_file}")
                        if docx_file not in found_templates:
                            found_templates.append(str(docx_file))
    
    if not found_templates:
        issues.append("No valid template files found")
    
    return issues, found_templates

def find_email_script():
    """Find the email sending script"""
    # Priority order of scripts to try
    scripts = [
        'utils/docx_parser.py',
        'send_personalized_emails.py',
        '.github/scripts/send_personalized_emails.py',
        'docx_parser.py',
        '.github/scripts/docx_parser.py'
    ]
    
    for script in scripts:
        if os.path.exists(script):
            print(f"  ✅ Found email script: {script}")
            return script
    
    return None

def build_command(config, template_file, script_path, dry_run=False, debug=False):
    """
    Build the command to execute the email script (docx_parser.py)
    
    Args:
        config: Configuration dictionary from JSON
        template_file: Path to template file
        script_path: Path to docx_parser.py script
        dry_run: Whether to run in dry-run mode
        debug: Whether to enable debug mode
        
    Returns:
        list: Command arguments as list
    """
    
    # Extract required configuration
    contacts_file = config.get('contacts')
    
    # Extract rate limiting settings
    rate_limiting = config.get('rate_limiting', {})
    delay = rate_limiting.get('delay_between_emails', 1.0)
    batch_size = rate_limiting.get('batch_size', 50)
    
    # Extract tracking settings
    tracking_config = config.get('tracking', {})
    tracking_dir = tracking_config.get('directory', 'tracking')
    
    # Extract feedback settings
    feedback_config = config.get('feedback', {})
    feedback_email = feedback_config.get('email')
    auto_inject = feedback_config.get('auto_inject', True)
    
    # Extract other required settings
    alerts_email = config.get('alerts_email', 'alerts@modelphysmat.com')
    
    # Extract optional domain/sector filtering
    domain = config.get('domain')
    sector = config.get('sector')
    
    # Validate required fields
    if not contacts_file:
        raise ValueError("Missing required field: contacts")
    
    # Build base command with REQUIRED arguments
    # When using --templates with a specific file, we DON'T use --scheduled
    # --scheduled is only for domain-based scanning mode
    cmd = [
        'python3', script_path,
        '--contacts', contacts_file,
        '--tracking', tracking_dir,
        '--alerts', alerts_email,
    ]
    
    # Add template file (this is the primary mode for JSON campaigns)
    if template_file:
        cmd.extend(['--templates', template_file])
    
    # Add delay
    cmd.extend(['--delay', str(delay)])
    
    # Add optional feedback email
    if feedback_email and auto_inject:
        cmd.extend(['--feedback', feedback_email])
    
    # Add batch settings
    if batch_size:
        cmd.extend(['--batch-size', str(batch_size)])
    
    # Add domain/sector filtering
    if domain:
        cmd.extend(['--domain', domain])
    
    if sector:
        cmd.extend(['--filter-domain', sector])
    
    # Add mode flags
    if dry_run:
        cmd.append('--dry-run')
    
    if debug:
        cmd.append('--debug')
    
    return cmd

def print_campaign_info(config):
    """Print campaign information"""
    print("\n" + "="*70)
    print(f"  📧 {config.get('name', 'Email Campaign')}")
    print("="*70)
    
    info = [
        ("Campaign", config.get('name', 'Unnamed')),
        ("Sector", config.get('sector', 'N/A')),
        ("Mode", config.get('mode', 'N/A')),
        ("Date", config.get('date', 'N/A')),
        ("Subject", config.get('subject', 'N/A')),
        ("From", config.get('from_email', 'N/A')),
        ("Reply-To", config.get('reply_to', 'N/A')),
        ("Contacts", config.get('contacts', 'N/A')),
    ]
    
    for label, value in info:
        print(f"{label:20s}: {value}")
    
    # Show templates
    templates = config.get('templates', [])
    if isinstance(templates, str):
        templates = [templates]
    print(f"{'Templates':20s}: {len(templates)} file(s)")
    for i, template in enumerate(templates, 1):
        print(f"  {i}. {template}")
    
    # Show rate limiting
    rate_limiting = config.get('rate_limiting', {})
    if rate_limiting:
        print(f"\n{'Rate Limiting':20s}:")
        print(f"  Delay between emails: {rate_limiting.get('delay_between_emails', 1.0)}s")
        print(f"  Batch size: {rate_limiting.get('batch_size', 50)}")
    
    # Show feedback config
    feedback = config.get('feedback', {})
    if feedback:
        print(f"\n{'Feedback System':20s}:")
        print(f"  Enabled: {feedback.get('auto_inject', False)}")
        print(f"  Email: {feedback.get('email', 'N/A')}")
    
    print("="*70)

def run_campaign(config, dry_run=False, debug=False):
    """Execute the email campaign"""
    
    print_campaign_info(config)
    
    # Setup SMTP
    if not setup_smtp_env(config.get('smtp', {})):
        print("\n❌ SMTP configuration incomplete")
        if not dry_run:
            return False
        else:
            print("⚠️  Continuing in dry-run mode without SMTP")
    
    if not setup_mail_from(config):
        print("\n❌ MAIL_FROM configuration incomplete")
        if not dry_run:
            return False
        else:
            print("⚠️  Continuing in dry-run mode without MAIL_FROM")
    
    # Validate files
    issues, templates = validate_files(config)
    
    if issues:
        print("\n❌ Validation issues found:")
        for issue in issues:
            print(f"  - {issue}")
        
        if not templates:
            print("\n❌ Cannot proceed without template files")
            return False
        else:
            print("\n⚠️  Proceeding with available files...")
    
    # Find email script
    script_path = find_email_script()
    if not script_path:
        print("\n❌ Email script not found!")
        print("Expected locations:")
        print("  - utils/docx_parser.py")
        print("  - send_personalized_emails.py")
        print("  - .github/scripts/send_personalized_emails.py")
        return False
    
    # Use first available template
    template_file = templates[0]
    
    # Build and run command
    cmd = build_command(config, template_file, script_path, dry_run, debug)
    
    print("\n🎯 Executing command:")
    print("  " + " ".join(cmd))
    print()
    
    if dry_run:
        print("🧪 DRY RUN MODE - No emails will be sent")
        print("   Emails will be saved to outbox/ directory\n")
    else:
        print("📤 LIVE MODE - Emails will be sent\n")
    
    print("="*70)
    
    # Execute
    try:
        result = subprocess.run(cmd, check=False)
        
        print("\n" + "="*70)
        if result.returncode == 0:
            print("  ✅ Campaign completed successfully")
        else:
            print(f"  ⚠️  Campaign completed with exit code {result.returncode}")
        print("="*70)
        
        return result.returncode == 0
            
    except Exception as e:
        print(f"\n❌ Error executing campaign: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(
        description='Run email campaign from JSON configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Dry run (no emails sent)
  %(prog)s --config test_campaign.json --dry-run
  
  # Live run
  %(prog)s --config test_campaign.json
  
  # With debug output
  %(prog)s --config test_campaign.json --debug --dry-run
        """
    )
    parser.add_argument(
        '--config',
        required=True,
        help='Path to JSON configuration file'
    )
    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Run in dry-run mode (no emails sent, saved to outbox/)'
    )
    parser.add_argument(
        '--debug',
        action='store_true',
        help='Enable debug output'
    )
    
    args = parser.parse_args()
    
    # Load configuration
    config = load_config(args.config)
    
    # Run campaign
    success = run_campaign(config, dry_run=args.dry_run, debug=args.debug)
    
    sys.exit(0 if success else 1)

if __name__ == '__main__':
    main()
