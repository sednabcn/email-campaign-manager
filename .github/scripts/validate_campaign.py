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

def validate_config(config_path):
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
            issues.append(f"Missing required field: {field}")
    
    # 4. Check contacts file
    print("\n4. Contacts File:")
    contacts = config.get('contacts', '')
    if contacts:
        exists, msg = check_file(contacts, "csv")
        print(f"   {msg}: {contacts}")
        if not exists:
            issues.append(f"Contacts file not found: {contacts}")
            
            # Suggest alternatives
            csv_files = list(Path('contacts').glob('*.csv')) if Path('contacts').exists() else []
            if csv_files:
                print("\n   Alternative CSV files found:")
                for csv_file in csv_files[:5]:
                    print(f"     - {csv_file}")
    else:
        print("   ⚠️  No contacts file specified")
        warnings.append("No contacts file specified")
    
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
    smtp_fields = ['host', 'port', 'username', 'password']
    
    for field in smtp_fields:
        if field in smtp:
            if field == 'password':
                print(f"   ✅ {field}: {'*' * len(str(smtp[field]))}")
            else:
                print(f"   ✅ {field}: {smtp[field]}")
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
    if len(sys.argv) < 2:
        print("Usage: python validate_campaign.py <config_file>")
        print("\nExample:")
        print("  python validate_campaign.py configs/campaign1.json")
        sys.exit(1)
    
    config_path = sys.argv[1]
    
    success = validate_config(config_path)
    
    print("\n" + "="*70)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
