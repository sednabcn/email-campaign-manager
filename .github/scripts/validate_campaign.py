#!/usr/bin/env python3
"""
Validate campaign setup before running
"""
import json
import os
import sys
from pathlib import Path

def check_file(path, file_type="file"):
    """Check if a file exists"""
    if os.path.exists(path):
        if file_type == "csv":
            lines = sum(1 for _ in open(path, 'r', encoding='utf-8'))
            return True, f"✅ Found ({lines} lines)"
        elif file_type == "docx":
            size = os.path.getsize(path)
            return True, f"✅ Found ({size} bytes)"
        else:
            return True, "✅ Found"
    else:
        return False, "❌ Not found"


def validate_config(config_path, allow_env_vars=False, allow_missing_contacts=False):
    """Validate configuration file"""
    print("="*70)
    print("  Campaign Setup Validation")
    print("="*70)
    print()
    
    issues = []
    warnings = []
    
    # 1. Check config file exists
    print(f"1. Configuration File: {config_path}")
    if not os.path.exists(config_path):
        print(f"   ❌ Configuration file not found: {config_path}")
        return False
    print("   ✅ Found")
    
    # 2. Load and parse config
    print("\n2. Parsing Configuration...")
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        print("   ✅ Valid JSON")
    except json.JSONDecodeError as e:
        print(f"   ❌ Invalid JSON: {e}")
        return False
    
    # 3. Check required fields
    print("\n3. Required Fields:")
    required_fields = {
        'name': 'Campaign name',
        'contacts': 'Contacts file path',
        'templates': 'Template file(s)',
        'subject': 'Email subject',
        'from_email': 'Sender email',
        'smtp': 'SMTP configuration'
    }
    
    for field, description in required_fields.items():
        if field in config:
            print(f"   ✅ {description}: {config[field]}")
        else:
            print(f"   ❌ Missing {description}")

            if allow_missing_contacts:
                print(f"   ⚠️  Allowing missing contacts (CI/CD mode)")
                warnings.append(f"Contacts not found but allowed: {contacts}")
            else:
                issues.append(f"Contacts path not found: {contacts}")
                issues.append(f"Missing required field: {field}")

    # 4. Check contacts file or directory
    print("\n4. Contacts Source:")
    contacts = config.get('contacts', '')
    if contacts:
        contacts_path = Path(contacts)
        
        if contacts_path.exists():
            if contacts_path.is_dir():
                # Check for TXT or CSV files in directory
                csv_files = list(contacts_path.glob("*.csv"))
                txt_files = list(contacts_path.glob("*.txt"))
                
                if csv_files:
                    print(f"   ✅ Directory with {len(csv_files)} CSV file(s): {contacts}")
                elif txt_files:
                    print(f"   ✅ Directory with {len(txt_files)} TXT file(s): {contacts}")
                    print(f"      (will be converted to CSV at runtime)")
                else:
                    print(f"   ❌ Directory exists but no contact files found: {contacts}")
                    issues.append(f"No CSV or TXT files in contacts directory: {contacts}")
            elif contacts_path.suffix.lower() == '.csv':
                print(f"   ✅ CSV file exists: {contacts}")
            elif contacts_path.suffix.lower() == '.txt':
                print(f"   ✅ TXT file exists: {contacts}")
                print(f"      (will be converted to CSV at runtime)")
            else:
                print(f"   ⚠️  Unexpected file type: {contacts}")
                warnings.append(f"Contacts file has unexpected extension: {contacts_path.suffix}")
        else:
            # Path doesn't exist - try to find alternatives
            print(f"   ❌ Path not found: {contacts}")
            
            contact_dir = contacts_path.parent
            if contact_dir.exists():
                # Look for any contact files in parent directory
                csv_files = list(contact_dir.glob("*.csv"))
                txt_files = list(contact_dir.glob("*.txt"))
                
                if csv_files or txt_files:
                    print(f"\n   💡 Alternative contact files found in {contact_dir}:")
                    for f in (csv_files + txt_files)[:5]:
                        print(f"      - {f}")
                    warnings.append(f"Contacts path not found, but alternatives exist in {contact_dir}")
                else:
                    issues.append(f"Contacts path not found and no alternatives: {contacts}")
            else:
                issues.append(f"Contacts path not found: {contacts}")
    else:
        print("   ⚠️  No contacts source specified")
        warnings.append("No contacts source specified in config")
    
    
    # 5. Check template files
    print("\n5. Template Files:")
    templates = config.get('templates', [])
    if isinstance(templates, str):
        templates = [templates]
    
    if templates:
        for template in templates:
            exists, msg = check_file(template, "docx")
            print(f"   {msg}: {template}")
            if not exists:
                issues.append(f"Template file not found: {template}")
                
                # Suggest alternatives
                docx_files = list(Path('templates').glob('*.docx')) if Path('templates').exists() else []
                if docx_files:
                    print("\n   Alternative template files found:")
                    for docx_file in docx_files[:5]:
                        print(f"     - {docx_file}")
    else:
        print("   ⚠️  No template files specified")
        warnings.append("No template files specified")
    
    # 6. Check SMTP configuration
    print("\n6. SMTP Configuration:")
    smtp = config.get('smtp', {})
    smtp_fields = {
        'host': 'host',
        'port': 'port', 
        'username': ['username', 'user'],  # Allow 'user' as alternative
        'password': ['password', 'pass']    # Allow 'pass' as alternative
    }
    
    for field, alternatives in smtp_fields.items():
        alt_list = alternatives if isinstance(alternatives, list) else [alternatives]
        found = False
        value = None
        
        for alt in alt_list:
            if alt in smtp:
                found = True
                value = smtp[alt]
                break
        
        if found:
            # Check if it's an environment variable placeholder
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                print(f"   ℹ️  {field}: {value} (will be substituted at runtime)")
                warnings.append(f"SMTP {field} uses environment variable: {value}")
            elif field == 'password':
                print(f"   ✅ {field}: {'*' * min(len(str(value)), 16)}")
            else:
                print(f"   ✅ {field}: {value}")
        else:
            print(f"   ❌ Missing SMTP {field}")
            issues.append(f"Missing SMTP configuration: {field}")
    
    # 7. Validate email format
    print("\n7. Email Validation:")
    from_email = config.get('from_email', '')
    if from_email:
        if '@' in from_email and '.' in from_email.split('@')[1]:
            print(f"   ✅ Valid format: {from_email}")
        else:
            print(f"   ⚠️  Invalid format: {from_email}")
            warnings.append(f"Invalid email format: {from_email}")
    
    # 8. Check subject line
    print("\n8. Subject Line:")
    subject = config.get('subject', '')
    if subject:
        if len(subject) > 78:
            print(f"   ⚠️  Subject is long ({len(subject)} chars): {subject[:50]}...")
            warnings.append(f"Subject line is longer than recommended (78 chars)")
        else:
            print(f"   ✅ Length OK ({len(subject)} chars): {subject}")
    
    # 9. Check optional fields
    print("\n9. Optional Settings:")
    optional_fields = {
        'reply_to': 'Reply-to email',
        'delay': 'Delay between emails (seconds)',
        'test_mode': 'Test mode enabled',
        'max_recipients': 'Maximum recipients'
    }
    
    for field, description in optional_fields.items():
        if field in config:
            print(f"   ✅ {description}: {config[field]}")
        else:
            print(f"   ℹ️  {description}: Not set (using default)")
    
    # Summary
    print("\n" + "="*70)
    print("  Validation Summary")
    print("="*70)
    
    if not issues and not warnings:
        print("\n✅ All checks passed! Campaign is ready to run.")
        return True
    else:
        if issues:
            print(f"\n❌ Found {len(issues)} critical issue(s):")
            for i, issue in enumerate(issues, 1):
                print(f"   {i}. {issue}")
        
        if warnings:
            print(f"\n⚠️  Found {len(warnings)} warning(s):")
            for i, warning in enumerate(warnings, 1):
                print(f"   {i}. {warning}")
        
        if issues:
            print("\n❌ Please fix critical issues before running the campaign.")
            return False
        else:
            print("\n⚠️  Campaign can run but please review warnings.")
            return True

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Validate campaign configuration')
    parser.add_argument('config_file', help='Path to campaign configuration JSON file')
    parser.add_argument('--allow-env-vars', action='store_true', 
                       help='Allow environment variable placeholders (e.g., ${SMTP_HOST})')
    parser.add_argument('--skip-contacts-check', action='store_true',
                       help='Skip strict contact file validation (useful for dynamic files)')
    parser.add_argument('--allow-missing-contacts', action='store_true',
                       help='Allow validation even if contacts not found (for CI/CD)')
    
    args = parser.parse_args()
    
    if not args.config_file:
        print("Usage: python validate_campaign.py <config_file> [--allow-env-vars] [--skip-contacts-check]")
        print("\nExample:")
        print("  python validate_campaign.py configs/campaign1.json")
        print("  python validate_campaign.py configs/campaign1.json --allow-env-vars --skip-contacts-check")
        sys.exit(1)

    success = validate_config(
    args.config_file,
    allow_env_vars=args.allow_env_vars,
    allow_missing_contacts=args.allow_missing_contacts
)
 
    
    print("\n" + "="*70)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
