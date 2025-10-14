#!/usr/bin/env python3
"""
Campaign Manager: Config-Driven Workflow
Scans scheduled-campaigns for config, loads templates and contacts
by domain/subdomain, converts TXT files to CSV, validates, and generates reports
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import csv
import re


class CampaignManager:
    def __init__(self, workflow_root="scheduled-campaigns"):
        self.workflow_root = Path(workflow_root)
        self.campaigns = []
        self.errors = []
        self.warnings = []
        
    def scan_campaign_configs(self):
        """Scan workflow_root for all JSON config files"""
        print(f"📁 Scanning campaign configs: {self.workflow_root}")
        
        if not self.workflow_root.exists():
            self.errors.append(f"Workflow root not found: {self.workflow_root}")
            return False
        
        config_files = list(self.workflow_root.glob("*.json"))
        
        if not config_files:
            self.errors.append("No JSON config files found in workflow root")
            return False
        
        print(f"   ✅ Found {len(config_files)} config file(s)")
        
        for config_file in config_files:
            campaign = self.load_campaign_config(config_file)
            if campaign:
                self.campaigns.append(campaign)
        
        return len(self.campaigns) > 0
    
    def load_campaign_config(self, config_file):
        """Load and parse a campaign configuration file"""
        try:
            with open(config_file, 'r') as f:
                config = json.load(f)
            
            campaign = {
                'config_file': config_file,
                'config': config,
                'name': config.get('name', config_file.stem),
                'sector': config.get('sector', 'general'),
                'mode': config.get('mode', 'immediate'),
                'date': config.get('date'),
                'templates': config.get('templates', []),
                'contacts_path': config.get('contacts'),
                'subject': config.get('subject'),
                'from_email': config.get('from_email'),
                'contact_mapping': config.get('contact_mapping', {})
            }
            
            print(f"   ✅ Loaded: {campaign['name']} (sector: {campaign['sector']})")
            return campaign
            
        except json.JSONDecodeError as e:
            self.errors.append(f"Invalid JSON in {config_file.name}: {e}")
            return None
        except Exception as e:
            self.errors.append(f"Error loading {config_file.name}: {e}")
            return None
    
    def resolve_domain_path(self, campaign):
        """Resolve domain and subdomain from campaign config"""
        sector = campaign['sector']
        
        # Extract subdomain from contacts_path if available
        if campaign['contacts_path']:
            parts = campaign['contacts_path'].split('/')
            if len(parts) >= 2:
                domain = parts[0]  # e.g., "education"
                subdomain = parts[-1]  # e.g., "adult_education"
                return domain, subdomain
        
        # Fallback: use sector as domain
        return sector, None
    
    def load_txt_contacts(self, txt_file):
        """Load contacts from TXT file and parse into structured data"""
        print(f"      📄 Loading: {txt_file.name}")
        
        contacts = []
        
        try:
            with open(txt_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Parse TXT - assume each line is a contact with fields
            # Format options: email,name | email | name <email> | etc.
            lines = [line.strip() for line in content.split('\n') if line.strip()]
            
            for line_num, line in enumerate(lines, 1):
                contact = self.parse_contact_line(line, line_num)
                if contact:
                    contacts.append(contact)
                else:
                    self.warnings.append(f"{txt_file.name}:{line_num}: Could not parse '{line}'")
            
            if contacts:
                print(f"         ✅ Parsed {len(contacts)} contacts from {txt_file.name}")
            
            return contacts
            
        except Exception as e:
            self.errors.append(f"Error reading {txt_file}: {e}")
            return []
    
    def parse_contact_line(self, line, line_num):
        """Parse a single contact line from TXT file"""
        contact = {}
        
        # Try format: email,name
        if ',' in line:
            parts = [p.strip() for p in line.split(',', 1)]
            if len(parts) == 2:
                email, name = parts
                if self.is_valid_email(email):
                    return {'email': email, 'name': name}
        
        # Try format: name <email>
        match = re.match(r'^(.+?)\s*<(.+?)>$', line)
        if match:
            name, email = match.groups()
            if self.is_valid_email(email):
                return {'email': email, 'name': name.strip()}
        
        # Try format: email@domain.com (just email)
        if self.is_valid_email(line):
            name = line.split('@')[0].title()
            return {'email': line, 'name': name}
        
        return None
    
    def is_valid_email(self, email):
        """Validate email format"""
        email = email.strip()
        return '@' in email and '.' in email.split('@')[-1] and len(email) > 5
    
    def save_contacts_as_csv(self, contacts, output_file):
        """Convert parsed contacts to CSV file"""
        if not contacts:
            self.warnings.append(f"No contacts to save for {output_file}")
            return False
        
        try:
            with open(output_file, 'w', newline='', encoding='utf-8') as f:
                writer = csv.DictWriter(f, fieldnames=['email', 'name'])
                writer.writeheader()
                writer.writerows(contacts)
            
            print(f"      ✅ Saved {len(contacts)} contacts to {output_file.name}")
            return True
            
        except Exception as e:
            self.errors.append(f"Error saving CSV {output_file}: {e}")
            return False
    
    def process_campaign(self, campaign):
        """Process a single campaign: resolve paths, load files, convert formats"""
        print(f"\n📋 Processing Campaign: {campaign['name']}")
        print(f"   Sector: {campaign['sector']}")
        print(f"   Mode: {campaign['mode']}")
        print(f"   Date: {campaign['date']}")
        
        domain, subdomain = self.resolve_domain_path(campaign)
        print(f"   Domain: {domain}")
        if subdomain:
            print(f"   Subdomain: {subdomain}")
        
        # Resolve template path
        templates_info = self.scan_templates(domain, subdomain, campaign['templates'])
        
        # Resolve contacts path and convert TXT to CSV
        contacts_info = self.scan_and_convert_contacts(domain, subdomain, campaign['contacts_path'])
        
        return {
            'campaign': campaign,
            'domain': domain,
            'subdomain': subdomain,
            'templates': templates_info,
            'contacts': contacts_info
        }
    
    def scan_templates(self, domain, subdomain, template_list):
        """Scan campaign-templates directory for templates"""
        print(f"\n   🎨 Scanning templates...")
        
        templates_root = self.workflow_root.parent / "campaign-templates"
        
        if not templates_root.exists():
            self.warnings.append(f"Templates root not found: {templates_root}")
            return {'found': [], 'missing': template_list}
        
        found_templates = []
        missing_templates = []
        
        for template_path in template_list:
            # Resolve template path: domain/subdomain/template_file
            if subdomain:
                full_path = templates_root / domain / subdomain / Path(template_path).name
            else:
                full_path = templates_root / domain / Path(template_path).name
            
            if full_path.exists():
                print(f"      ✅ Found: {template_path}")
                found_templates.append({
                    'path': str(full_path),
                    'name': Path(template_path).name,
                    'size': full_path.stat().st_size
                })
            else:
                print(f"      ❌ Missing: {template_path}")
                missing_templates.append(template_path)
        
        return {
            'found': found_templates,
            'missing': missing_templates,
            'root': str(templates_root)
        }
    
    def scan_and_convert_contacts(self, domain, subdomain, contacts_path):
        """Scan contact-details directory, find TXT files, convert to CSV"""
        print(f"\n   👥 Scanning contacts...")
        
        contacts_root = self.workflow_root.parent / "contact-details"
        
        if not contacts_root.exists():
            self.errors.append(f"Contacts root not found: {contacts_root}")
            return {'converted': [], 'errors': []}
        
        # Build contact directory path: contact-details/domain/subdomain
        if subdomain:
            contact_dir = contacts_root / domain / subdomain
        else:
            contact_dir = contacts_root / domain
        
        print(f"      Looking in: {contact_dir}")
        
        if not contact_dir.exists():
            self.errors.append(f"Contact directory not found: {contact_dir}")
            return {'converted': [], 'source_dir': str(contact_dir)}
        
        # Find all TXT files
        txt_files = list(contact_dir.glob("*.txt"))
        
        if not txt_files:
            self.errors.append(f"No TXT files found in {contact_dir}")
            return {'converted': [], 'source_dir': str(contact_dir)}
        
        print(f"      ✅ Found {len(txt_files)} TXT file(s)")
        
        converted_files = []
        
        for txt_file in txt_files:
            # Load contacts from TXT
            contacts = self.load_txt_contacts(txt_file)
            
            if not contacts:
                continue
            
            # Save as CSV in the same directory
            csv_file = txt_file.with_suffix('.csv')
            
            if self.save_contacts_as_csv(contacts, csv_file):
                converted_files.append({
                    'txt_source': str(txt_file),
                    'csv_output': str(csv_file),
                    'contact_count': len(contacts)
                })
        
        return {
            'converted': converted_files,
            'source_dir': str(contact_dir),
            'total_contacts': sum(c['contact_count'] for c in converted_files)
        }
    
    def generate_report(self):
        """Generate comprehensive processing report"""
        print(f"\n\n{'='*70}")
        print(f"CAMPAIGN PROCESSING REPORT")
        print(f"{'='*70}\n")
        
        print(f"📊 Summary:")
        print(f"   Total campaigns: {len(self.campaigns)}")
        print(f"   Errors: {len(self.errors)}")
        print(f"   Warnings: {len(self.warnings)}")
        
        if self.errors:
            print(f"\n❌ Errors:")
            for error in self.errors:
                print(f"   - {error}")
        
        if self.warnings:
            print(f"\n⚠️  Warnings:")
            for warning in self.warnings:
                print(f"   - {warning}")
        
        if not self.errors and not self.warnings:
            print(f"\n✅ All validations passed!")
        
        return len(self.errors) == 0
    
    def run(self):
        """Execute full campaign management workflow"""
        print("="*70)
        print("Campaign Manager: Config-Driven Workflow")
        print("="*70)
        
        if not self.scan_campaign_configs():
            self.generate_report()
            return False
        
        print(f"\n{'='*70}")
        print(f"PROCESSING CAMPAIGNS")
        print(f"{'='*70}")
        
        campaign_results = []
        
        for campaign in self.campaigns:
            result = self.process_campaign(campaign)
            campaign_results.append(result)
        
        success = self.generate_report()
        
        print(f"\n{'='*70}")
        print(f"CAMPAIGN DETAILS")
        print(f"{'='*70}\n")
        
        for result in campaign_results:
            campaign = result['campaign']
            print(f"Campaign: {campaign['name']}")
            print(f"  Domain: {result['domain']}")
            if result['subdomain']:
                print(f"  Subdomain: {result['subdomain']}")
            
            templates = result['templates']
            print(f"  Templates: {len(templates['found'])} found, {len(templates['missing'])} missing")
            
            contacts = result['contacts']
            print(f"  Contacts: {contacts['total_contacts']} total, {len(contacts['converted'])} CSV file(s)")
            
            print()
        
        return success


def main():
    if len(sys.argv) > 1:
        workflow_root = sys.argv[1]
    else:
        workflow_root = "scheduled-campaigns"
    
    manager = CampaignManager(workflow_root)
    success = manager.run()
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
