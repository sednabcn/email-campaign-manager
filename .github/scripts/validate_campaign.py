#!/usr/bin/env python3
"""
.github/scripts/validate_campaign.py - Campaign Configuration Validator

Validates JSON campaign configurations for:
- Required fields and structure
- Template file existence
- Contact directory existence
- SMTP configuration
- Schedule validity
- Contact mapping
- Feedback configuration
- Rate limiting settings
"""

import json
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime, date


class CampaignValidator:
    """Comprehensive campaign configuration validator"""
    
    def __init__(self, config_path, allow_env_vars=False, skip_contacts_check=False):
        self.config_path = Path(config_path)
        self.allow_env_vars = allow_env_vars
        self.skip_contacts_check = skip_contacts_check
        self.errors = []
        self.warnings = []
        self.config = None
        
    def load_config(self):
        """Load and parse JSON configuration"""
        try:
            with open(self.config_path, 'r', encoding='utf-8') as f:
                self.config = json.load(f)
            print(f"✅ Loaded configuration: {self.config_path}")
            return True
        except FileNotFoundError:
            self.errors.append(f"Configuration file not found: {self.config_path}")
            return False
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON: {e}")
            return False
        except Exception as e:
            self.errors.append(f"Error loading config: {e}")
            return False
    
    def validate_required_fields(self):
        """Validate presence of required fields"""
        required_fields = [
            'name',
            'templates',
            'contacts',
            'from_email',
            'subject'
        ]
        
        print("\n📋 Validating required fields...")
        
        for field in required_fields:
            if field not in self.config:
                self.errors.append(f"Missing required field: {field}")
            else:
                print(f"  ✅ {field}: present")
        
        # Check templates is a list
        if 'templates' in self.config:
            if not isinstance(self.config['templates'], list):
                self.errors.append("'templates' must be a list")
            elif len(self.config['templates']) == 0:
                self.errors.append("'templates' list is empty")
        
        return len(self.errors) == 0
    
    def validate_schedule(self):
        """Validate campaign schedule (mode and date)"""
        print("\n📅 Validating schedule...")
        
        mode = self.config.get('mode', 'immediate')
        campaign_date_str = self.config.get('date')
        
        print(f"  Mode: {mode}")
        print(f"  Date: {campaign_date_str}")
        
        valid_modes = ['immediate', 'schedule', 'schedule_now']
        if mode not in valid_modes:
            self.errors.append(f"Invalid mode '{mode}'. Must be one of: {valid_modes}")
            return False
        
        # Parse and validate date
        if campaign_date_str:
            try:
                campaign_date = datetime.strptime(campaign_date_str, "%Y-%m-%d").date()
                today = date.today()
                
                if mode == 'immediate':
                    if campaign_date < today:
                        self.errors.append(f"Immediate mode: date {campaign_date} is in the past")
                    else:
                        print(f"  ✅ Valid for immediate mode")
                
                elif mode == 'schedule_now':
                    if campaign_date != today:
                        self.errors.append(f"Schedule_now mode requires today's date (got {campaign_date}, today is {today})")
                    else:
                        print(f"  ✅ Valid for schedule_now mode")
                
                elif mode == 'schedule':
                    if campaign_date < today:
                        self.errors.append(f"Scheduled date {campaign_date} has passed")
                    elif campaign_date > today:
                        self.warnings.append(f"Campaign scheduled for future: {campaign_date}")
                    else:
                        print(f"  ✅ Valid for schedule mode")
                
            except ValueError:
                self.errors.append(f"Invalid date format '{campaign_date_str}'. Expected YYYY-MM-DD")
                return False
        else:
            if mode != 'immediate':
                self.errors.append(f"Date required for mode '{mode}'")
                return False
        
        return len(self.errors) == 0
    
    def validate_templates(self):
        """Validate template files exist and are accessible"""
        print("\n📄 Validating templates...")
        
        templates = self.config.get('templates', [])
        
        for i, template_path in enumerate(templates, 1):
            template_file = Path(template_path)
            
            print(f"  Template {i}: {template_path}")
            
            # Check existence
            if not template_file.exists():
                self.errors.append(f"Template file not found: {template_path}")
                continue
            
            # Check file extension
            valid_extensions = ['.docx', '.txt', '.html', '.md', '.json']
            if template_file.suffix.lower() not in valid_extensions:
                self.warnings.append(f"Template has unusual extension: {template_file.suffix}")
            
            # Check file size
            file_size = template_file.stat().st_size
            if file_size == 0:
                self.errors.append(f"Template file is empty: {template_path}")
            else:
                print(f"    ✅ Exists ({file_size / 1024:.2f} KB)")
            
            # For DOCX files, check if valid ZIP structure
            if template_file.suffix.lower() == '.docx':
                try:
                    import zipfile
                    if zipfile.is_zipfile(template_file):
                        print(f"    ✅ Valid DOCX structure")
                    else:
                        self.errors.append(f"DOCX file is not a valid ZIP archive: {template_path}")
                except ImportError:
                    self.warnings.append("Cannot validate DOCX structure (zipfile not available)")
        
        return len(self.errors) == 0
    
    def validate_contacts(self):
        """Validate contacts directory/file exists"""
        if self.skip_contacts_check:
            print("\n👥 Skipping contacts validation (--skip-contacts-check)")
            return True
        
        print("\n👥 Validating contacts...")
        
        contacts_path = self.config.get('contacts', '')
        
        if not contacts_path:
            self.errors.append("Contacts path not specified")
            return False
        
        contacts = Path(contacts_path)
        
        print(f"  Contacts path: {contacts_path}")
        
        # Check if exists
        if not contacts.exists():
            self.errors.append(f"Contacts path does not exist: {contacts_path}")
            return False
        
        # If directory, check for contact files
        if contacts.is_dir():
            contact_extensions = ['.csv', '.xlsx', '.xls', '.url', '.json', '.docx', '.txt']
            contact_files = []
            
            for ext in contact_extensions:
                contact_files.extend(list(contacts.rglob(f'*{ext}')))
            
            if contact_files:
                print(f"    ✅ Directory contains {len(contact_files)} contact file(s)")
                
                # Show file types
                file_types = {}
                for f in contact_files:
                    ext = f.suffix.lower()
                    file_types[ext] = file_types.get(ext, 0) + 1
                
                for ext, count in sorted(file_types.items()):
                    print(f"       {ext}: {count} file(s)")
            else:
                self.warnings.append(f"Contacts directory is empty: {contacts_path}")
        
        # If file, check it's a valid format
        elif contacts.is_file():
            valid_extensions = ['.csv', '.xlsx', '.xls', '.json']
            if contacts.suffix.lower() in valid_extensions:
                file_size = contacts.stat().st_size
                print(f"    ✅ File ({file_size / 1024:.2f} KB)")
            else:
                self.warnings.append(f"Unusual contacts file extension: {contacts.suffix}")
        
        return True
    
    def validate_smtp_config(self):
        """Validate SMTP configuration"""
        print("\n📧 Validating SMTP configuration...")
        
        smtp = self.config.get('smtp', {})
        
        required_smtp = ['host', 'port', 'user', 'password']
        
        for field in required_smtp:
            value = smtp.get(field, '')
            
            # Check if it's an environment variable placeholder
            if isinstance(value, str) and value.startswith('${') and value.endswith('}'):
                env_var = value[2:-1]
                
                if self.allow_env_vars:
                    print(f"  {field}: ${{{env_var}}} (environment variable - allowed)")
                    
                    # Check if env var is actually set
                    if os.getenv(env_var):
                        print(f"    ✅ Environment variable is set")
                    else:
                        self.warnings.append(f"Environment variable not set: {env_var}")
                else:
                    actual_value = os.getenv(env_var)
                    if actual_value:
                        print(f"  ✅ {field}: resolved from ${{{env_var}}}")
                    else:
                        self.errors.append(f"SMTP {field} uses undefined environment variable: ${{{env_var}}}")
            
            elif value:
                # Mask password
                if field == 'password':
                    print(f"  ✅ {field}: *** (set)")
                else:
                    print(f"  ✅ {field}: {value}")
            else:
                self.errors.append(f"Missing SMTP {field}")
        
        # Validate port is numeric
        port = smtp.get('port')
        if port and not isinstance(port, str):
            if not isinstance(port, int) or port < 1 or port > 65535:
                self.errors.append(f"Invalid SMTP port: {port}")
        
        return len(self.errors) == 0
    
    def validate_email_addresses(self):
        """Validate email address formats"""
        print("\n✉️  Validating email addresses...")
        
        email_fields = {
            'from_email': self.config.get('from_email'),
            'reply_to': self.config.get('reply_to'),
            'feedback.email': self.config.get('feedback', {}).get('email') if isinstance(self.config.get('feedback'), dict) else None
        }
        
        import re
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        
        for field_name, email in email_fields.items():
            if email:
                if email_pattern.match(email):
                    print(f"  ✅ {field_name}: {email}")
                else:
                    self.errors.append(f"Invalid email format for {field_name}: {email}")
            elif field_name == 'from_email':
                self.errors.append(f"Required field missing: {field_name}")
        
        return len(self.errors) == 0
    
    def validate_contact_mapping(self):
        """Validate contact field mapping"""
        print("\n🗺️  Validating contact mapping...")
        
        contact_mapping = self.config.get('contact_mapping')
        
        if not contact_mapping:
            self.warnings.append("No contact_mapping defined - using default field names")
            return True
        
        if not isinstance(contact_mapping, dict):
            self.errors.append("contact_mapping must be a dictionary")
            return False
        
        print(f"  Mapping defined for {len(contact_mapping)} fields:")
        
        for template_field, csv_field in contact_mapping.items():
            print(f"    [{template_field}] → {csv_field}")
        
        return True
    
    def validate_feedback_config(self):
        """Validate feedback configuration"""
        print("\n💬 Validating feedback configuration...")
        
        feedback = self.config.get('feedback')
        
        if not feedback:
            self.warnings.append("No feedback configuration - feedback features disabled")
            return True
        
        if not isinstance(feedback, dict):
            self.errors.append("feedback must be a dictionary")
            return False
        
        # Check feedback email
        feedback_email = feedback.get('email')
        if feedback_email:
            print(f"  ✅ Feedback email: {feedback_email}")
        else:
            self.warnings.append("Feedback email not specified")
        
        # Check injection type
        injection_type = feedback.get('injection_type', 'footer_signature')
        valid_types = ['footer_signature', 'header', 'inline']
        if injection_type not in valid_types:
            self.warnings.append(f"Unusual injection type: {injection_type}")
        else:
            print(f"  ✅ Injection type: {injection_type}")
        
        # Check response categories
        categories = feedback.get('response_categories', [])
        if categories:
            print(f"  ✅ Response categories: {len(categories)}")
        
        return True
    
    def validate_rate_limiting(self):
        """Validate rate limiting configuration"""
        print("\n⏱️  Validating rate limiting...")
        
        rate_limiting = self.config.get('rate_limiting')
        
        if not rate_limiting:
            self.warnings.append("No rate_limiting configuration - using defaults")
            return True
        
        # Check numeric fields
        numeric_fields = {
            'emails_per_minute': (1, 100),
            'delay_between_emails': (0, 60),
            'batch_size': (1, 1000)
        }
        
        for field, (min_val, max_val) in numeric_fields.items():
            value = rate_limiting.get(field)
            
            if value is not None:
                if isinstance(value, (int, float)):
                    if min_val <= value <= max_val:
                        print(f"  ✅ {field}: {value}")
                    else:
                        self.warnings.append(f"{field} value {value} outside recommended range [{min_val}-{max_val}]")
                else:
                    self.errors.append(f"{field} must be numeric")
        
        return True
    
    def validate_tracking_config(self):
        """Validate tracking configuration"""
        print("\n📊 Validating tracking configuration...")
        
        tracking = self.config.get('tracking')
        
        if not tracking:
            self.warnings.append("No tracking configuration - using defaults")
            return True
        
        if not isinstance(tracking, dict):
            self.errors.append("tracking must be a dictionary")
            return False
        
        boolean_fields = ['enabled', 'domain_separated', 'analytics', 'response_tracking', 'feedback_tracking']
        
        for field in boolean_fields:
            value = tracking.get(field)
            if value is not None:
                if isinstance(value, bool):
                    status = "enabled" if value else "disabled"
                    print(f"  ✅ {field}: {status}")
                else:
                    self.warnings.append(f"{field} should be boolean")
        
        return True
    
    def validate_sector_domain(self):
        """Validate sector and domain configuration"""
        print("\n🏢 Validating sector/domain...")
        
        sector = self.config.get('sector')
        domain = self.config.get('domain')
        subdomain = self.config.get('subdomain')
        
        if sector:
            print(f"  ✅ Sector: {sector}")
        else:
            self.warnings.append("No sector specified")
        
        if domain:
            print(f"  ✅ Domain: {domain}")
        else:
            self.warnings.append("No domain specified")
        
        if subdomain:
            print(f"  ✅ Subdomain: {subdomain}")
        
        # Check consistency
        if sector and domain and sector != domain:
            self.warnings.append(f"Sector '{sector}' differs from domain '{domain}' - ensure this is intentional")
        
        return True
    
    def validate_all(self):
        """Run all validations"""
        print(f"\n{'='*70}")
        print(f"CAMPAIGN CONFIGURATION VALIDATION")
        print(f"{'='*70}")
        print(f"File: {self.config_path}")
        print(f"{'='*70}")
        
        # Load config
        if not self.load_config():
            return False
        
        # Run all validations
        validations = [
            self.validate_required_fields,
            self.validate_schedule,
            self.validate_templates,
            self.validate_contacts,
            self.validate_smtp_config,
            self.validate_email_addresses,
            self.validate_contact_mapping,
            self.validate_feedback_config,
            self.validate_rate_limiting,
            self.validate_tracking_config,
            self.validate_sector_domain
        ]
        
        for validation in validations:
            try:
                validation()
            except Exception as e:
                self.errors.append(f"Validation error in {validation.__name__}: {e}")
        
        # Print summary
        self.print_summary()
        
        return len(self.errors) == 0
    
    def print_summary(self):
        """Print validation summary"""
        print(f"\n{'='*70}")
        print(f"VALIDATION SUMMARY")
        print(f"{'='*70}")
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ ALL VALIDATIONS PASSED")
        elif not self.errors:
            print(f"\n✅ PASSED (with {len(self.warnings)} warning(s))")
        else:
            print(f"\n❌ FAILED ({len(self.errors)} error(s), {len(self.warnings)} warning(s))")
        
        print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Validate campaign JSON configuration',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic validation
  python validate_campaign.py campaign.json
  
  # CI/CD mode (allow environment variables)
  python validate_campaign.py campaign.json --allow-env-vars
  
  # Skip contacts check (useful in CI where contacts aren't committed)
  python validate_campaign.py campaign.json --skip-contacts-check
  
  # Verbose output
  python validate_campaign.py campaign.json --verbose
        """
    )
    
    parser.add_argument('config_file', 
                       help='Path to campaign JSON configuration file')
    
    parser.add_argument('--allow-env-vars', 
                       action='store_true',
                       help='Allow environment variable placeholders like ${SMTP_HOST}')
    
    parser.add_argument('--skip-contacts-check', 
                       action='store_true',
                       help='Skip validation of contacts directory existence')
    
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Create validator
    validator = CampaignValidator(
        args.config_file,
        allow_env_vars=args.allow_env_vars,
        skip_contacts_check=args.skip_contacts_check
    )
    
    # Run validation
    success = validator.validate_all()
    
    # Exit with appropriate code
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()
