#!/usr/bin/env python3
"""Diagnostic script to troubleshoot data loading issues."""

import os
import sys
from pathlib import Path

def diagnose():
    contacts_dir = os.environ.get('CONTACTS_DIR', 'contacts')
    templates_dir = os.environ.get('TEMPLATES_DIR', 'campaign-templates')
    scheduled_dir = os.environ.get('SCHEDULED_DIR', 'scheduled-campaigns')
    
    print("=== DATA PIPELINE DIAGNOSTIC ===\n")
    
    print(f"Working Directory: {os.getcwd()}\n")
    
    # Check contacts directory
    print(f"Contacts Directory: {contacts_dir}")
    contacts_path = Path(contacts_dir)
    if contacts_path.exists():
        print(f"  ✓ Exists: {contacts_path.absolute()}")
        files = list(contacts_path.glob('*'))
        print(f"  Total files: {len(files)}")
        for f in files:
            print(f"    - {f.name} ({f.stat().st_size} bytes, readable: {os.access(f, os.R_OK)})")
    else:
        print(f"  ✗ NOT FOUND: {contacts_path.absolute()}")
    
    # Check templates
    print(f"\nTemplates Directory: {templates_dir}")
    templates_path = Path(templates_dir)
    if templates_path.exists():
        print(f"  ✓ Exists: {templates_path.absolute()}")
        for domain in ['education', 'finance', 'healthcare', 'industry', 'technology', 'government']:
            domain_path = templates_path / domain
            if domain_path.exists():
                templates = list(domain_path.glob('*'))
                print(f"    - {domain}: {len(templates)} files")
    else:
        print(f"  ✗ NOT FOUND: {templates_path.absolute()}")
    
    # Check scheduled campaigns
    print(f"\nScheduled Directory: {scheduled_dir}")
    scheduled_path = Path(scheduled_dir)
    if scheduled_path.exists():
        print(f"  ✓ Exists: {scheduled_path.absolute()}")
        files = list(scheduled_path.glob('*'))
        print(f"  Total files: {len(files)}")
        for f in files[:5]:  # Show first 5
            print(f"    - {f.name}")
    else:
        print(f"  ✗ NOT FOUND: {scheduled_path.absolute()}")
    
    # Test actual loading
    print("\n=== TESTING DATA LOADING ===\n")
    
    try:
        import pandas as pd
        csv_files = list(contacts_path.glob('*.csv')) if contacts_path.exists() else []
        if csv_files:
            test_file = csv_files[0]
            print(f"Testing CSV load: {test_file.name}")
            df = pd.read_csv(test_file)
            print(f"  ✓ Loaded {len(df)} rows, columns: {list(df.columns)}")
            print(f"  Sample row: {df.iloc[0].to_dict() if len(df) > 0 else 'empty'}")
        else:
            print("  No CSV files to test")
    except Exception as e:
        print(f"  ✗ CSV load failed: {e}")
    
    return 0

if __name__ == '__main__':
    sys.exit(diagnose())
