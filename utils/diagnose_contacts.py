#!/usr/bin/env python3
"""
Diagnostic script to identify why contacts aren't being loaded properly
"""

import sys
import json
from pathlib import Path

def diagnose_contact_loading():
    """Diagnose contact loading issues"""
    
    print("=" * 70)
    print("CONTACT LOADING DIAGNOSTIC")
    print("=" * 70)
    print()
    
    issues = []
    warnings = []
    
    # 1. Check contacts directory
    contacts_dir = Path("contacts")
    if not contacts_dir.exists():
        issues.append(f"Contacts directory not found: {contacts_dir}")
        return issues, warnings
    
    print(f"✅ Contacts directory exists: {contacts_dir}")
    
    # 2. Find all contact files
    csv_files = list(contacts_dir.glob("**/*.csv"))
    excel_files = list(contacts_dir.glob("**/*.xlsx")) + list(contacts_dir.glob("**/*.xls"))
    url_files = list(contacts_dir.glob("**/*.url"))
    
    print(f"\n📁 Contact Files Found:")
    print(f"   CSV files: {len(csv_files)}")
    print(f"   Excel files: {len(excel_files)}")
    print(f"   URL files (Google Sheets): {len(url_files)}")
    
    if not (csv_files or excel_files or url_files):
        issues.append("No contact files found in contacts/ directory")
        return issues, warnings
    
    # 3. Analyze CSV files
    if csv_files:
        print(f"\n📊 CSV File Analysis:")
        for csv_file in csv_files:
            print(f"\n   File: {csv_file}")
            try:
                import csv
                with open(csv_file, 'r', encoding='utf-8') as f:
                    reader = csv.DictReader(f)
                    headers = reader.fieldnames
                    rows = list(reader)
                    
                    print(f"      Rows: {len(rows)}")
                    print(f"      Headers: {headers}")
                    
                    # Check for required fields
                    has_email = any('email' in h.lower() for h in headers)
                    has_name = any('name' in h.lower() for h in headers)
                    
                    if not has_email:
                        issues.append(f"{csv_file.name}: Missing 'email' column")
                    else:
                        print(f"      ✅ Has email column")
                    
                    if not has_name:
                        warnings.append(f"{csv_file.name}: No 'name' column (will use email)")
                    else:
                        print(f"      ✅ Has name column")
                    
                    # Check for valid emails
                    valid_emails = 0
                    for row in rows:
                        email = None
                        for h in headers:
                            if 'email' in h.lower():
                                email = row.get(h, '').strip()
                                break
                        if email and '@' in email:
                            valid_emails += 1
                    
                    print(f"      Valid emails: {valid_emails}/{len(rows)}")
                    
                    if valid_emails == 0:
                        issues.append(f"{csv_file.name}: No valid email addresses found")
                    
            except Exception as e:
                issues.append(f"Error reading {csv_file.name}: {e}")
    
    # 4. Check scheduled campaigns
    scheduled_dir = Path("scheduled-campaigns")
    if not scheduled_dir.exists():
        warnings.append(f"Scheduled campaigns directory not found: {scheduled_dir}")
    else:
        campaign_files = list(scheduled_dir.glob("**/*.json"))
        print(f"\n📋 Campaign Files: {len(campaign_files)}")
        
        for campaign_file in campaign_files:
            try:
                with open(campaign_file, 'r') as f:
                    config = json.load(f)
                
                print(f"\n   Campaign: {campaign_file.name}")
                
                # Check mode and date
                mode = config.get('mode', 'immediate')
                date = config.get('date')
                print(f"      Mode: {mode}")
                print(f"      Date: {date}")
                
                # Check contacts path
                contacts_path = config.get('contacts')
                if contacts_path:
                    print(f"      Contacts: {contacts_path}")
                    if not Path(contacts_path).exists():
                        issues.append(f"{campaign_file.name}: Contacts path doesn't exist: {contacts_path}")
                else:
                    warnings.append(f"{campaign_file.name}: No contacts path specified (will use default)")
                
                # Check templates
                templates = config.get('templates', [])
                if templates:
                    print(f"      Templates: {len(templates)}")
                    for template in templates:
                        if not Path(template).exists():
                            issues.append(f"{campaign_file.name}: Template not found: {template}")
                else:
                    warnings.append(f"{campaign_file.name}: No templates specified")
                
            except Exception as e:
                issues.append(f"Error reading {campaign_file.name}: {e}")
    
    # 5. Check data_loader module
    print(f"\n🔧 Module Check:")
    try:
        sys.path.insert(0, 'utils')
        from data_loader import load_contacts_directory
        print(f"   ✅ data_loader module available")
        print(f"   ✅ load_contacts_directory function found")
    except ImportError as e:
        warnings.append(f"data_loader module not available: {e}")
        print(f"   ⚠️  data_loader module not found (will use fallback)")
    
    # Summary
    print("\n" + "=" * 70)
    print("DIAGNOSTIC SUMMARY")
    print("=" * 70)
    
    if issues:
        print(f"\n❌ ISSUES FOUND ({len(issues)}):")
        for i, issue in enumerate(issues, 1):
            print(f"   {i}. {issue}")
    else:
        print(f"\n✅ No critical issues found")
    
    if warnings:
        print(f"\n⚠️  WARNINGS ({len(warnings)}):")
        for i, warning in enumerate(warnings, 1):
            print(f"   {i}. {warning}")
    
    print("\n" + "=" * 70)
    
    return issues, warnings

if __name__ == "__main__":
    try:
        issues, warnings = diagnose_contact_loading()
        
        if issues:
            print("\n🔧 Recommended Actions:")
            print("1. Fix the issues listed above")
            print("2. Ensure CSV files have 'email' column with valid addresses")
            print("3. Check campaign JSON configs point to correct contact files")
            print("4. Verify file paths are relative to project root")
            sys.exit(1)
        else:
            print("\n✅ Contact loading system looks healthy!")
            sys.exit(0)
            
    except Exception as e:
        print(f"\n❌ Diagnostic failed: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
