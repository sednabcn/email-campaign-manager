#!/usr/bin/env python3
"""
Enhanced Campaign Configuration Validator
Gracefully handles past dates with warnings instead of errors
"""

import json
import sys
import os
import argparse
from pathlib import Path
from datetime import datetime, date


class CampaignValidator:
    """Enhanced campaign configuration validator with graceful date handling"""
    
    def __init__(self, config_path, allow_env_vars=False, skip_contacts_check=False, graceful_dates=True):
        self.config_path = Path(config_path)
        self.allow_env_vars = allow_env_vars
        self.skip_contacts_check = skip_contacts_check
        self.graceful_dates = graceful_dates  # NEW: Allow past dates with warning
        self.errors = []
        self.warnings = []
        self.info_messages = []
        self.config = None
        self.skip_execution = False  # NEW: Flag to skip execution gracefully
        
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
        """
        Validate campaign schedule with GRACEFUL date handling
        Past dates generate warnings and skip flags, not errors
        """
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
                        # GRACEFUL HANDLING: Warning instead of error
                        if self.graceful_dates:
                            self.warnings.append(
                                f"⚠️  Campaign date {campaign_date} is in the past (today: {today})"
                            )
                            self.info_messages.append(
                                f"🔔 ALERT: NO CAMPAIGN TO EXECUTE - DATE IS IN THE PAST"
                            )
                            self.skip_execution = True
                            print(f"  ⚠️  Date in past - will skip execution gracefully")
                            return True  # Valid config, just won't execute
                        else:
                            self.errors.append(f"Immediate mode: date {campaign_date} is in the past")
                            return False
                    else:
                        print(f"  ✅ Valid for immediate mode")
                
                elif mode == 'schedule_now':
                    if campaign_date != today:
                        if self.graceful_dates and campaign_date < today:
                            self.warnings.append(
                                f"⚠️  Campaign date {campaign_date} is in the past (today: {today})"
                            )
                            self.info_messages.append(
                                f"🔔 ALERT: NO CAMPAIGN TO EXECUTE - SCHEDULED DATE HAS PASSED"
                            )
                            self.skip_execution = True
                            print(f"  ⚠️  Date in past - will skip execution gracefully")
                            return True
                        else:
                            self.errors.append(
                                f"Schedule_now mode requires today's date (got {campaign_date}, today is {today})"
                            )
                            return False
                    else:
                        print(f"  ✅ Valid for schedule_now mode")
                
                elif mode == 'schedule':
                    if campaign_date < today:
                        if self.graceful_dates:
                            self.warnings.append(
                                f"⚠️  Scheduled date {campaign_date} has passed (today: {today})"
                            )
                            self.info_messages.append(
                                f"🔔 ALERT: NO CAMPAIGN TO EXECUTE - SCHEDULED DATE HAS PASSED"
                            )
                            self.skip_execution = True
                            print(f"  ⚠️  Date in past - will skip execution gracefully")
                            return True
                        else:
                            self.errors.append(f"Scheduled date {campaign_date} has passed")
                            return False
                    elif campaign_date > today:
                        self.warnings.append(f"Campaign scheduled for future: {campaign_date}")
                        self.info_messages.append(
                            f"📅 Campaign scheduled for: {campaign_date} (not executing today)"
                        )
                        self.skip_execution = True
                        print(f"  📅 Scheduled for future - will skip today")
                        return True
                    else:
                        print(f"  ✅ Valid for schedule mode")
                
            except ValueError:
                self.errors.append(f"Invalid date format '{campaign_date_str}'. Expected YYYY-MM-DD")
                return False
        else:
            if mode != 'immediate':
                self.errors.append(f"Date required for mode '{mode}'")
                return False
        
        return True
    
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
    
    def validate_all(self):
        """Run all validations"""
        print(f"\n{'='*70}")
        print(f"CAMPAIGN CONFIGURATION VALIDATION")
        print(f"{'='*70}")
        print(f"File: {self.config_path}")
        print(f"Graceful date handling: {'ENABLED' if self.graceful_dates else 'DISABLED'}")
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
        ]
        
        for validation in validations:
            try:
                validation()
            except Exception as e:
                self.errors.append(f"Validation error in {validation.__name__}: {e}")
        
        # Print summary
        self.print_summary()
        
        # Return success if no ERRORS (warnings are OK)
        return len(self.errors) == 0
    
    def print_summary(self):
        """Print validation summary with enhanced messaging"""
        print(f"\n{'='*70}")
        print(f"VALIDATION SUMMARY")
        print(f"{'='*70}")
        
        # Info messages first (alerts)
        if self.info_messages:
            print(f"\n📢 EXECUTION STATUS:")
            for i, info in enumerate(self.info_messages, 1):
                print(f"  {i}. {info}")
        
        # Errors
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for i, error in enumerate(self.errors, 1):
                print(f"  {i}. {error}")
        
        # Warnings
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for i, warning in enumerate(self.warnings, 1):
                print(f"  {i}. {warning}")
        
        # Final status
        print(f"\n{'='*70}")
        if self.skip_execution:
            print("✅ VALIDATION PASSED")
            print("📋 EXECUTION STATUS: NO CAMPAIGNS TO EXECUTE")
            print("   (Date is in the past or scheduled for future)")
        elif not self.errors and not self.warnings:
            print("✅ ALL VALIDATIONS PASSED")
            print("📋 EXECUTION STATUS: READY TO EXECUTE")
        elif not self.errors:
            print(f"✅ PASSED (with {len(self.warnings)} warning(s))")
            print("📋 EXECUTION STATUS: READY TO EXECUTE (check warnings)")
        else:
            print(f"❌ FAILED ({len(self.errors)} error(s), {len(self.warnings)} warning(s))")
            print("📋 EXECUTION STATUS: CANNOT EXECUTE")
        
        print(f"{'='*70}\n")


def main():
    parser = argparse.ArgumentParser(
        description='Validate campaign JSON configuration with graceful date handling',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Basic validation with graceful date handling (default)
  python validate_campaign.py campaign.json
  
  # CI/CD mode (allow environment variables)
  python validate_campaign.py campaign.json --allow-env-vars
  
  # Strict mode (past dates are errors)
  python validate_campaign.py campaign.json --strict-dates
  
  # Skip contacts check
  python validate_campaign.py campaign.json --skip-contacts-check
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
    
    parser.add_argument('--strict-dates', 
                       action='store_true',
                       help='Treat past dates as errors (default: graceful warnings)')
    
    parser.add_argument('--verbose', '-v',
                       action='store_true',
                       help='Enable verbose output')
    
    args = parser.parse_args()
    
    # Create validator with graceful date handling (unless strict mode)
    validator = CampaignValidator(
        args.config_file,
        allow_env_vars=args.allow_env_vars,
        skip_contacts_check=args.skip_contacts_check,
        graceful_dates=not args.strict_dates  # Graceful by default
    )
    
    # Run validation
    success = validator.validate_all()
    
    # Exit with 0 if validation passed (even if execution should be skipped)
    # This allows the workflow to continue gracefully
    sys.exit(0 if success else 1)


if __name__ == '__main__':
    main()



    
