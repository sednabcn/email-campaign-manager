#!/usr/bin/env python3
"""
Enhanced Contact Analysis Script for GitHub Actions
Analyzes contact sources and sets GitHub Actions outputs
"""

import os
import sys
import json
from pathlib import Path
from datetime import datetime

def load_contacts_from_csv(file_path):
    """Load contacts from CSV file"""
    try:
        import pandas as pd
        df = pd.read_csv(file_path)
        # Convert to dict and handle NaN values
        contacts = df.fillna('').to_dict('records')
        return contacts
    except Exception as e:
        print(f"Error loading CSV {file_path}: {e}")
        return []

def load_contacts_from_excel(file_path):
    """Load contacts from Excel file"""
    try:
        import pandas as pd
        df = pd.read_excel(file_path)
        # Convert to dict and handle NaN values
        contacts = df.fillna('').to_dict('records')
        return contacts
    except Exception as e:
        print(f"Error loading Excel {file_path}: {e}")
        return []

def load_contacts_from_google_sheets(url_file):
    """Load contacts from Google Sheets URL"""
    try:
        with open(url_file, 'r') as f:
            url = f.read().strip()
        
        if 'docs.google.com/spreadsheets' in url:
            # Extract sheet ID and convert to CSV export URL
            import re
            match = re.search(r'/d/([a-zA-Z0-9-_]+)', url)
            if match:
                sheet_id = match.group(1)
                csv_url = f"https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0"
                
                import pandas as pd
                df = pd.read_csv(csv_url)
                contacts = df.fillna('').to_dict('records')
                return contacts
    except Exception as e:
        print(f"Error loading Google Sheets from {url_file}: {e}")
    return []

def safe_string(value):
    """Safely convert any value to string, handling NaN and None"""
    if value is None:
        return ''
    if isinstance(value, float):
        import math
        if math.isnan(value):
            return ''
    return str(value)

def analyze_contacts():
    """Main contact analysis function"""
    contacts_dir = os.environ.get('CONTACTS_DIR', 'contacts')
    contact_source_filter = os.environ.get('CONTACT_SOURCE_FILTER', '')
    
    print(f"Analyzing contacts from: {contacts_dir}")
    print(f"Contact source filter: {contact_source_filter or 'None'}")
    
    all_contacts = []
    sources_breakdown = {}
    domain_breakdown = {}
    file_types = {'csv': 0, 'excel': 0, 'google_sheets': 0, 'json': 0}
    loader_used = 'enhanced_fallback_loader'
    
    # Try to use professional data_loader if available
    try:
        sys.path.insert(0, 'utils')
        from data_loader import load_contacts
        print("Using professional data_loader.py")
        all_contacts = load_contacts(contacts_dir)
        loader_used = 'professional_data_loader'
    except ImportError:
        print("Professional data_loader not available, using enhanced fallback")
        
        # Enhanced fallback: scan directory for contact files
        contacts_path = Path(contacts_dir)
        if contacts_path.exists():
            # Process CSV files
            for csv_file in contacts_path.glob('**/*.csv'):
                file_str = str(csv_file)
                if contact_source_filter and contact_source_filter not in file_str:
                    continue
                print(f"Loading CSV: {csv_file}")
                contacts = load_contacts_from_csv(csv_file)
                all_contacts.extend(contacts)
                sources_breakdown[file_str] = len(contacts)
                file_types['csv'] += 1
            
            # Process Excel files
            for excel_file in contacts_path.glob('**/*.xlsx'):
                file_str = str(excel_file)
                if contact_source_filter and contact_source_filter not in file_str:
                    continue
                print(f"Loading Excel: {excel_file}")
                contacts = load_contacts_from_excel(excel_file)
                all_contacts.extend(contacts)
                sources_breakdown[file_str] = len(contacts)
                file_types['excel'] += 1
            
            for excel_file in contacts_path.glob('**/*.xls'):
                file_str = str(excel_file)
                if contact_source_filter and contact_source_filter not in file_str:
                    continue
                print(f"Loading Excel: {excel_file}")
                contacts = load_contacts_from_excel(excel_file)
                all_contacts.extend(contacts)
                sources_breakdown[file_str] = len(contacts)
                file_types['excel'] += 1
            
            # Process Google Sheets URL files
            for url_file in contacts_path.glob('**/*.url'):
                file_str = str(url_file)
                if contact_source_filter and contact_source_filter not in file_str:
                    continue
                print(f"Loading Google Sheets: {url_file}")
                contacts = load_contacts_from_google_sheets(url_file)
                all_contacts.extend(contacts)
                sources_breakdown[file_str] = len(contacts)
                file_types['google_sheets'] += 1
    
    # Analyze domains from email addresses - with safe string handling
    for contact in all_contacts:
        email = safe_string(contact.get('email', ''))
        if email and '@' in email:
            domain = email.split('@')[1]
            domain_breakdown[domain] = domain_breakdown.get(domain, 0) + 1
    
    contact_count = len(all_contacts)
    
    print(f"\nSuccessfully loaded {contact_count} contacts using {loader_used}")
    print(f"Sources: {len(sources_breakdown)}")
    print(f"Domains: {len(domain_breakdown)}")
    if domain_breakdown:
        top_domain = max(domain_breakdown.items(), key=lambda x: x[1])
        print(f"Top domain: {top_domain[0]}")
    
    # CRITICAL: Set GitHub Actions output
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f'count={contact_count}\n')
        print(f"Set GITHUB_OUTPUT count={contact_count}")
    else:
        print("WARNING: GITHUB_OUTPUT not set, cannot set output variable")
    
    # Save detailed analysis to JSON
    analysis_data = {
        'total_contacts': contact_count,
        'sources_breakdown': sources_breakdown,
        'domain_breakdown': domain_breakdown,
        'file_types': file_types,
        'loaded_with': loader_used,
        'contact_source_filter': contact_source_filter,
        'analysis_timestamp': datetime.now().isoformat(),
        'contacts_dir': contacts_dir
    }
    
    with open('contact_analysis.json', 'w') as f:
        json.dump(analysis_data, f, indent=2)
    
    print("Contact analysis complete:")
    print(f"  - Total contacts: {contact_count}")
    print(f"  - Sources: {len(sources_breakdown)}")
    print(f"  - Domains: {len(domain_breakdown)}")
    if domain_breakdown:
        print(f"  - Top domain: {max(domain_breakdown.items(), key=lambda x: x[1])[0]}")
    
    return contact_count

if __name__ == '__main__':
    try:
        contact_count = analyze_contacts()
        sys.exit(0)
    except Exception as e:
        print(f"ERROR in contact analysis: {e}")
        import traceback
        traceback.print_exc()
        
        # Set count to 0 on error
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write('count=0\n')
        
        sys.exit(1)
