#!/usr/bin/env python3
"""
Campaign Configuration Validator and Auto-Fixer
Validates campaign JSON and contact files, provides fixes
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import csv

class CampaignValidator:
    def __init__(self, campaign_file):
        self.campaign_file = Path(campaign_file)
        self.config = None
        self.issues = []
        self.warnings = []
        self.fixes_applied = []
        
    def load_config(self):
        """Load and parse campaign configuration"""
        print(f"📄 Loading campaign configuration: {self.campaign_file}")
        
        if not self.campaign_file.exists():
            self.issues.append(f"Campaign file not found: {self.campaign_file}")
            return False
        
        try:
            with open(self.campaign_file, 'r') as f:
                content = f.read()
                
            # Check for incomplete JSON
            if content.count('{') != content.count('}'):
                self.issues.append("JSON is incomplete - mismatched braces")
                print("   ❌ Incomplete JSON detected")
                
                # Try to fix
                if content.count('{') > content.count('}'):
                    content += '\n}'
                    print("   🔧 Auto-fixing: Adding missing closing brace")
                    self.fixes_applied.append("Added missing closing brace")
            
            self.config = json.loads(content)
            print("   ✅ JSON parsed successfully")
            return True
            
        except json.JSONDecodeError as e:
            self.issues.append(f"Invalid JSON: {e}")
            print(f"   ❌ JSON parse error: {e}")
            return False
        except Exception as e:
            self.issues.append(f"Error loading config: {e}")
            return False
    
    def validate_required_fields(self):
        """Check for required configuration fields"""
        print("\n📋 Validating required fields...")
        
        required_fields = {
            'name': str,
            'sector': str,
            'templates': list,
            'contacts': str,
            'mode': str,
            'date': str,
            'from_email': str,
            'subject': str
        }
        
        if not self.config:
            self.issues.append("No configuration loaded")
            return False
        
        for field, field_type in required_fields.items():
            if field not in self.config:
                self.issues.append(f"Missing required field: {field}")
                print(f"   ❌ Missing field: {field}")
            elif not isinstance(self.config[field], field_type):
                self.warnings.append(f"Field '{field}' has incorrect type: expected {field_type.__name__}")
                print(f"   ⚠️  Field '{field}' type mismatch")
            else:
                print(f"   ✅ {field}")
        
        return len(self.issues) == 0
    
    def validate_email_format(self):
        """Validate email address formats"""
        print("\n📧 Validating email formats...")
        
        email_fields = ['from_email']
        if 'reply_to' in self.config:
            email_fields.append('reply_to')
        
        for field in email_fields:
            if field in self.config:
                email = self.config[field]
                if not self._is_valid_email(email):
                    self.issues.append(f"Invalid email format in '{field}': {email}")
                    print(f"   ❌ Invalid email: {email}")
                else:
                    print(f"   ✅ {field}: {email}")
    
    def validate_contact_file(self):
        """Validate that contact directory exists and contains CSV files"""
        print("\n👥 Validating contacts directory...")
        
        if 'contacts' not in self.config:
            self.issues.append("Contacts directory not specified")
            return False
        
        contact_path = Path(self.config['contacts'])
        
        if not contact_path.exists():
            self.issues.append(f"Contacts directory not found: {contact_path}")
            print(f"   ❌ Contacts directory not found: {contact_path}")
            return False
        
        if not contact_path.is_dir():
            self.issues.append(f"Contacts path is not a directory: {contact_path}")
            print(f"   ❌ Contacts path is not a directory: {contact_path}")
            return False
        
        try:
            csv_files = list(contact_path.glob('*.csv'))
            
            if not csv_files:
                self.warnings.append(f"No CSV files found in contacts directory: {contact_path}")
                print(f"   ⚠️  No CSV files found in contacts directory")
                return True
            
            print(f"   ✅ Contacts directory found ({len(csv_files)} CSV files)")
            
            total_contacts = 0
            invalid_emails_total = 0
            
            # Validate each CSV file
            for csv_file in csv_files:
                try:
                    with open(csv_file, 'r') as f:
                        reader = csv.DictReader(f)
                        rows = list(reader)
                    
                    if not rows:
                        self.warnings.append(f"CSV file is empty: {csv_file.name}")
                        continue
                    
                    required_columns = {'email', 'name'}
                    headers = set(reader.fieldnames or [])
                    
                    if not required_columns.issubset(headers):
                        missing = required_columns - headers
                        self.issues.append(f"CSV file '{csv_file.name}' missing columns: {missing}")
                        print(f"   ❌ {csv_file.name}: Missing columns {missing}")
                        continue
                    
                    total_contacts += len(rows)
                    
                    # Validate email addresses
                    invalid_emails = []
                    for idx, row in enumerate(rows, 1):
                        if not self._is_valid_email(row.get('email', '')):
                            invalid_emails.append(f"Row {idx}: {row.get('email', 'EMPTY')}")
                    
                    if invalid_emails:
                        invalid_emails_total += len(invalid_emails)
                        self.warnings.append(f"File '{csv_file.name}': {len(invalid_emails)} invalid emails")
                        print(f"   ⚠️  {csv_file.name}: {len(invalid_emails)} invalid emails")
                    else:
                        print(f"   ✅ {csv_file.name}: {len(rows)} valid contacts")
                
                except Exception as e:
                    self.issues.append(f"Error reading CSV file '{csv_file.name}': {e}")
                    print(f"   ❌ Error reading {csv_file.name}: {e}")
            
            if invalid_emails_total > 0:
                self.warnings.append(f"Total invalid emails found: {invalid_emails_total}")
            
            return len(self.issues) == 0
            
        except Exception as e:
            self.issues.append(f"Error reading contacts directory: {e}")
            print(f"   ❌ Error reading contacts directory: {e}")
            return False
    
    def validate_date_format(self):
        """Validate scheduled date format"""
        print("\n📅 Validating date format...")
        
        if 'date' not in self.config:
            return True
        
        scheduled_date = self.config['date']
        
        try:
            dt = datetime.fromisoformat(scheduled_date)
            print(f"   ✅ Date valid: {dt}")
            return True
        except ValueError:
            self.issues.append(f"Invalid date format: {scheduled_date} (expected ISO format: YYYY-MM-DD)")
            print(f"   ❌ Invalid date format: {scheduled_date}")
            return False
    
    def validate_template_file(self):
        """Check if template files exist"""
        print("\n📝 Validating template files...")
        
        if 'templates' not in self.config:
            self.issues.append("Template files not specified")
            return False
        
        templates = self.config['templates']
        
        if not isinstance(templates, list):
            self.issues.append("Templates must be a list")
            return False
        
        if not templates:
            self.issues.append("Templates list is empty")
            return False
        
        all_valid = True
        for template in templates:
            template_path = Path(template)
            
            if not template_path.exists():
                self.issues.append(f"Template file not found: {template_path}")
                print(f"   ❌ Template file not found: {template_path}")
                all_valid = False
            else:
                print(f"   ✅ Template file found: {template_path}")
        
        return all_valid
    
    def _is_valid_email(self, email):
        """Simple email validation"""
        if not email or not isinstance(email, str):
            return False
        return '@' in email and '.' in email.split('@')[-1]
    
    def run_validation(self):
        """Run all validation checks"""
        print("=" * 60)
        print("Campaign Configuration Validator")
        print("=" * 60)
        
        if not self.load_config():
            return False
        
        self.validate_required_fields()
        self.validate_email_format()
        self.validate_contact_file()
        self.validate_date_format()
        self.validate_template_file()
        
        return self._print_summary()
    
    def _print_summary(self):
        """Print validation summary"""
        print("\n" + "=" * 60)
        print("VALIDATION SUMMARY")
        print("=" * 60)
        
        if self.fixes_applied:
            print(f"\n🔧 Fixes Applied ({len(self.fixes_applied)}):")
            for fix in self.fixes_applied:
                print(f"   ✓ {fix}")
        
        if self.issues:
            print(f"\n❌ Issues Found ({len(self.issues)}):")
            for issue in self.issues:
                print(f"   ✗ {issue}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"   ! {warning}")
        
        if not self.issues and not self.warnings:
            print("\n✅ All validations passed!")
        
        return len(self.issues) == 0


def main():
    if len(sys.argv) < 2:
        print("Usage: python campaign_validate_config.py <campaign_file>")
        sys.exit(1)
    
    campaign_file = sys.argv[1]
    validator = CampaignValidator(campaign_file)
    success = validator.run_validation()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
 
