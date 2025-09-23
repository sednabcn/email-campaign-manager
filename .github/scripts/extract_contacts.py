#!/usr/bin/env python3
"""
Fixed Contact Extraction Script for GitHub Actions
Handles your specific directory structure: contact_details/education/adult_education/
"""

import os
import sys
import csv
import re
from datetime import datetime
from pathlib import Path

def extract_email_from_line(line):
    """Extract email addresses from a text line"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    return re.findall(email_pattern, line)

def extract_phone_from_line(line):
    """Extract phone numbers from a text line"""
    phone_patterns = [
        r'\+?1?[-.\s]?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}',  # US format
        r'\+?[0-9]{1,3}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}[-.\s]?[0-9]{3,4}',  # International
        r'\([0-9]{3}\)\s?[0-9]{3}-[0-9]{4}',  # (xxx) xxx-xxxx
        r'\+44\s?[0-9]{4}\s?[0-9]{6}',  # UK format
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, line)
        if phones:
            return phones[0].strip()
    return ""

def extract_name_from_line(line, email):
    """Extract name from line containing email"""
    # Remove email from line to get potential name
    line_without_email = line.replace(email, '').strip()
    
    # Remove common separators and clean up
    name = re.sub(r'[<>\[\](){}:;,\-\|]+', ' ', line_without_email).strip()
    name = ' '.join(name.split())  # Normalize whitespace
    
    # If name is too short or seems invalid, return empty
    if len(name) < 2 or name.isdigit() or not name.replace(' ', '').replace('.', '').isalpha():
        return ""
    
    return name

def get_organization_from_filename(filename):
    """Extract organization name from filename - handles your specific naming convention"""
    # Remove file extension
    org = filename.replace('-contacts.txt', '').replace('.txt', '')
    
    # Handle special cases in your files
    if 'St.George' in org:
        org = org.replace("St.George's=Univ", "St. George's University")
    elif 'Birbeck' in org:
        org = "Birkbeck College"
    elif 'open-univ' in org:
        org = "The Open University"
    else:
        # General cleanup
        org = org.replace('=', ' ')
        org = org.replace('-', ' ')
        org = org.replace('_', ' ')
        org = ' '.join(word.capitalize() for word in org.split())
    
    return org

def extract_contacts_from_file(file_path):
    """Extract contacts from a single text file"""
    contacts = []
    filename = os.path.basename(file_path)
    organization = get_organization_from_filename(filename)
    
    print(f"  Processing: {file_path}")
    print(f"  Organization: {organization}")
    
    try:
        # Try different encodings to handle various file formats
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"  Successfully read with encoding: {encoding}")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"  ERROR: Could not decode file with any encoding")
            return contacts
        
        line_number = 0
        for line in content.splitlines():
            line_number += 1
            line = line.strip()
            
            # Skip empty lines, comments, and lines that are too short
            if not line or line.startswith('#') or line.startswith('//') or len(line) < 5:
                continue
            
            # Look for email addresses in the line
            emails = extract_email_from_line(line)
            
            for email in emails:
                # Extract associated information
                name = extract_name_from_line(line, email)
                phone = extract_phone_from_line(line)
                
                # Create contact record
                contact = {
                    'name': name if name else f"Contact {len(contacts) + 1}",
                    'email': email.lower().strip(),
                    'phone': phone,
                    'organization': organization,
                    'source_file': filename
                }
                
                contacts.append(contact)
                print(f"    Found: {contact['name']} <{contact['email']}> at {organization}")
    
    except Exception as e:
        print(f"  ERROR processing {file_path}: {str(e)}")
    
    return contacts

def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_contacts.py <source_directory> <output_directory>")
        print("Example: python extract_contacts.py contact_details contacts")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    print(f"Contact Extraction Script - Fixed Version")
    print(f"Source: {source_dir}")
    print(f"Output: {output_dir}")
    print("-" * 60)
    
    # Ensure output directory exists
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"Created/verified output directory: {output_path.absolute()}")
    
    # Find all .txt files recursively
    txt_files = []
    source_path = Path(source_dir)
    
    if source_path.exists():
        txt_files = list(source_path.rglob("*.txt"))
        print(f"Searching recursively in: {source_path.absolute()}")
    else:
        print(f"WARNING: Source directory {source_dir} does not exist")
    
    if not txt_files:
        print(f"No .txt files found in {source_dir}")
        # Create empty CSV file to avoid pipeline failure
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"edu_adults_contacts_{timestamp}.csv"
        csv_path = output_path / csv_filename
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'email', 'phone', 'organization', 'source_file']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        
        print(f"Created empty CSV file: {csv_path}")
        return
    
    print(f"Found {len(txt_files)} text files:")
    for txt_file in sorted(txt_files):
        print(f"  - {txt_file}")
    print()
    
    # Extract contacts from all files
    all_contacts = []
    for txt_file in sorted(txt_files):
        file_contacts = extract_contacts_from_file(txt_file)
        all_contacts.extend(file_contacts)
    
    # Remove duplicates based on email
    print(f"Removing duplicates from {len(all_contacts)} contacts...")
    unique_contacts = {}
    for contact in all_contacts:
        email = contact['email']
        if email not in unique_contacts:
            unique_contacts[email] = contact
        else:
            # Keep the contact with more complete information
            existing = unique_contacts[email]
            if not existing['name'] or existing['name'].startswith('Contact '):
                if contact['name'] and not contact['name'].startswith('Contact '):
                    existing['name'] = contact['name']
            if not existing['phone'] and contact['phone']:
                existing['phone'] = contact['phone']
    
    final_contacts = list(unique_contacts.values())
    print(f"After deduplication: {len(final_contacts)} unique contacts")
    
    # Generate output CSV filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"edu_adults_contacts_{timestamp}.csv"
    csv_path = output_path / csv_filename
    
    print(f"Creating CSV file: {csv_path.absolute()}")
    
    # Write to CSV
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'email', 'phone', 'organization', 'source_file']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for contact in final_contacts:
                writer.writerow(contact)
        
        # Verify file was created
        if csv_path.exists():
            file_size = csv_path.stat().st_size
            print(f"SUCCESS: CSV file created successfully!")
            print(f"  File path: {csv_path.absolute()}")
            print(f"  File size: {file_size} bytes")
            print(f"  Records written: {len(final_contacts)}")
        else:
            print(f"ERROR: CSV file was not created at {csv_path}")
            sys.exit(1)
            
    except Exception as e:
        print(f"ERROR writing CSV file: {e}")
        sys.exit(1)
    
    # Summary
    print("-" * 60)
    print(f"Extraction completed successfully!")
    print(f"Summary:")
    print(f"  - Files processed: {len(txt_files)}")
    print(f"  - Contacts extracted: {len(all_contacts)}")
    print(f"  - Unique contacts: {len(final_contacts)}")
    print(f"  - Output file: {csv_filename}")
    print(f"  - Full path: {csv_path.absolute()}")
    
    # Show preview
    print(f"\nCSV Preview (first 5 records):")
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if i < 6:  # Header + 5 records
                    print(f"  {line.strip()}")
                else:
                    break
    except Exception as e:
        print(f"Error reading preview: {e}")

if __name__ == "__main__":
    main()
