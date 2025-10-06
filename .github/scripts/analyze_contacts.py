#!/usr/bin/env python3
"""
Enhanced contact source analysis script for GitHub Actions workflow.
"""

import sys
import os
import json
from datetime import datetime

# Add paths for imports
sys.path.append('.')
sys.path.append('utils')


def main():
    contacts_dir = os.environ.get('CONTACTS_DIR', 'contacts')
    contact_source_filter = os.environ.get('CONTACT_SOURCE_FILTER', 'all_sources')
    
    contact_count = 0
    analysis = {
        'total_contacts': 0,
        'sources_breakdown': {},
        'domain_breakdown': {},
        'contact_types': {},
        'top_domains': [],
        'sample_contacts': [],
        'loaded_with': 'enhanced_system',
        'analysis_timestamp': datetime.now().isoformat(),
        'contact_source_filter': contact_source_filter
    }

    try:
        # Try using professional data_loader if available
        try:
            from data_loader import load_contacts
            print('Using professional data_loader.py')
            contacts = load_contacts(contacts_dir)
            analysis['loaded_with'] = 'professional_data_loader.py'
        except ImportError:
            print('Professional data_loader not available, using enhanced fallback')
            # Enhanced fallback contact loading
            import pandas as pd
            import glob
            
            contacts = []
            
            # Load CSV files
            csv_files = glob.glob(os.path.join(contacts_dir, '*.csv'))
            for csv_file in csv_files:
                try:
                    df = pd.read_csv(csv_file)
                    for _, row in df.iterrows():
                        contact = row.to_dict()
                        contact['source'] = os.path.basename(csv_file)
                        contact['source_type'] = 'csv'
                        contacts.append(contact)
                except Exception as e:
                    print(f'Error loading CSV {csv_file}: {e}')
            
            # Load Excel files
            excel_files = glob.glob(os.path.join(contacts_dir, '*.xlsx')) + \
                         glob.glob(os.path.join(contacts_dir, '*.xls'))
            for excel_file in excel_files:
                try:
                    df = pd.read_excel(excel_file)
                    for _, row in df.iterrows():
                        contact = row.to_dict()
                        contact['source'] = os.path.basename(excel_file)
                        contact['source_type'] = 'excel'
                        contacts.append(contact)
                except Exception as e:
                    print(f'Error loading Excel {excel_file}: {e}')
            
            # Load Google Sheets URLs
            url_files = glob.glob(os.path.join(contacts_dir, '*.url'))
            for url_file in url_files:
                try:
                    with open(url_file, 'r') as f:
                        sheets_url = f.read().strip()
                    
                    if 'docs.google.com/spreadsheets' in sheets_url:
                        # Extract sheet ID and create CSV export URL
                        sheet_id = sheets_url.split('/d/')[-1].split('/')[0]
                        csv_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/export?format=csv&gid=0'
                        
                        df = pd.read_csv(csv_url)
                        for _, row in df.iterrows():
                            contact = row.to_dict()
                            contact['source'] = os.path.basename(url_file)
                            contact['source_type'] = 'google_sheets'
                            contacts.append(contact)
                except Exception as e:
                    print(f'Error loading Google Sheet {url_file}: {e}')
            
            analysis['loaded_with'] = 'enhanced_fallback_loader'

        contact_count = len(contacts)
        print(f'Successfully loaded {contact_count} contacts using {analysis["loaded_with"]}')
        
        if contacts:
            # Analyze sources
            sources = {}
            domains = {}
            contact_types = {}
            
            for contact in contacts:
                # Source analysis
                source = contact.get('source', 'unknown')
                sources[source] = sources.get(source, 0) + 1
        
                # Domain analysis
                email = str(contact.get('email', '')).lower()
                if '@' in email:
                    domain = email.split('@')[-1]
                    domains[domain] = domains.get(domain, 0) + 1
                    
                # Contact type analysis
                if 'source_type' in contact:
                    contact_types[contact['source_type']] = contact_types.get(contact['source_type'], 0) + 1
    
            analysis.update({
                'total_contacts': contact_count,
                'sources_breakdown': sources,
                'domain_breakdown': domains,
                'contact_types': contact_types,
                'top_domains': sorted(domains.items(), key=lambda x: x[1], reverse=True)[:10],
                'sample_contacts': contacts[:3] if contacts else []
            })
    
            print(f'Contact analysis complete:')
            print(f'  - Total contacts: {contact_count}')
            print(f'  - Sources: {len(sources)}')
            print(f'  - Domains: {len(domains)}')
            print(f'  - Top domain: {max(domains.items(), key=lambda x: x[1])[0] if domains else "none"}')

    except Exception as e:
        print(f'Error in contact analysis: {e}')
        import traceback
        traceback.print_exc()
        analysis['error'] = str(e)

    # Save analysis file
    with open('contact_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2, default=str)
    
    # CRITICAL: Write output to GITHUB_OUTPUT
    github_output = os.environ.get('GITHUB_OUTPUT', '')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f'count={contact_count}\n')
        print(f'Set GITHUB_OUTPUT count={contact_count}')
    else:
        print('WARNING: GITHUB_OUTPUT environment variable not set!')
        print(f'Contact count: {contact_count}')
    
    if contact_count == 0:
        print('::warning::No contacts loaded - check contact directory and files')
    
    return 0 if contact_count >= 0 else 1


if __name__ == '__main__':
    sys.exit(main())
