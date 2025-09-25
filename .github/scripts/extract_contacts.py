#!/usr/bin/env python3
"""
Universal Contact Extraction Script - FIXED VERSION
Properly handles BOM characters and improved regex patterns
"""

import os
import sys
import csv
import re
from datetime import datetime
from pathlib import Path

ORG_KEYWORDS = [
    'university', 'college', 'department', 'school', 'institute', 'bank', 'agency',
    'house', 'centre', 'center', 'trust', 'hospital', 'office', 'building', 'services',
    'group', 'ltd', 'limited', 'company', 'street', 'square', 'road', 'avenue', 'london', 'kingdom'
]
def clean_text(text):
    """Remove BOM and other problematic characters but keep newlines"""
    if not text:
        return text
    text = text.replace('\ufeff', '').replace('ï»¿', '')
    text = text.replace('\xa0', ' ').replace('â€™', "'")
    # Normalise multiple blank lines but keep newlines
    text = re.sub(r'\r\n', '\n', text)
    return text.strip()

def _is_probable_name(text):
    """Return True if text looks like a personal name (1–3 capitalised words)."""
    if not text:
        return False
    text = clean_text(text)
    if any(k in text.lower() for k in ORG_KEYWORDS):
        return False
    tokens = text.strip().split()
    if not (1 <= len(tokens) <= 3):
        return False
    return all(re.match(r'^[A-Z][a-z\-\']+$', t) for t in tokens)


def extract_name_and_rank(text):
    """Extract person name and rank/title from contact text."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    if not lines:
        return "", ""
    
    # Enhanced title pattern - complete version
    title_pattern = re.compile(
    r'^(Professor|Prof\.?|Dr\.?|Mr\.?|Mrs\.?|Ms\.?|Manager|Director|Head|Dean|Chief|Lecturer|Senior|Principal|Associate|Assistant)\b\.?\s+([A-Z][a-z\'\-]+(?:\s+[A-Z][a-z\'\-]+){0,3})',
    re.IGNORECASE
)

    #title_pattern = re.compile(
    #    r'^(Professor|Prof\.?|Dr\.?|Mr\.?|Mrs\.?|Ms\.?|Manager|Director|Head|Dean|Chief|Lecturer|Senior|Principal|Associate|Assistant)\b\.?\s+([A-Z][a-z\-\']+(?: [A-Z][a-z\-\']+){0,2})\s*$',
     #   re.IGNORECASE
    #)
    
    # Try to match the pattern in the first few lines
    for line in lines[:3]:  # Check first 3 lines for title/name
        match = title_pattern.match(line)
        if match:
            title = match.group(1)
            name = match.group(2)
            return name, title
    
    # Fallback: look for standalone name pattern if no title found
    name_pattern = re.compile(r'^[A-Z][a-z\-\']+(?: [A-Z][a-z\-\']+){1,2}$')
    for line in lines[:2]:
        if name_pattern.match(line):
            return line, ""
    
    return "", ""

def extract_position_title(text, name="", rank=""):
    """Extract position/job title separate from rank."""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    position_indicators = [
        'head of', 'director of', 'chief of', 'dean of', 'school of', 'department of', 
        'head of school', 'head of department', 'professor of', 'lecturer in'
    ]
    
    # Look for explicit position fields first
    for line in lines:
        if line.lower().startswith(('position:', 'title:', 'role:', 'job title:')):
            clean = re.sub(r'^(position|title|role|job title):\s*', '', line, flags=re.IGNORECASE).strip()
            if clean and (not name or name.lower() not in clean.lower()):
                return clean
    
    # Look for specific position patterns that are NOT just title+name combinations
    for line in lines:
        line_lower = line.lower()
        
        # Skip lines that contain the person's name (avoid extracting "Manager John Doe" as position)
        if name and name.lower() in line_lower:
            continue
            
        # Skip if this is just the rank we already extracted
        if rank and line_lower.strip() == rank.lower():
            continue
            
        # Skip lines that are clearly title + name patterns
        title_name_pattern = r'^(professor|dr\.?|mr\.?|mrs\.?|ms\.?|manager|director|head|dean|chief|lecturer)\s+[A-Z][a-z\-\']+(?:\s+[A-Z][a-z\-\']+)*\s*$'
        if re.match(title_name_pattern, line, re.IGNORECASE):
            continue
        
        # Skip addresses, emails, phones
        if re.search(r'(address|email|phone|tel|fax|@|\+\d+|street|road|avenue|building)', line_lower):
            continue
            
        # Look for position indicators first (most specific)
        for indicator in position_indicators:
            if indicator in line_lower:
                return line.strip()
        
        # Look for department/school positions
        if re.search(r'school of|department of|faculty of|college of|institute of', line_lower):
            return line.strip()
        
        # Look for common job titles/positions (not personal titles)
        position_patterns = [
            r'^(academic|research|senior|principal|lead|chief|head)\s+(manager|director|coordinator|specialist|analyst|engineer|developer|administrator|officer|supervisor|scientist|fellow|researcher)$',
            r'^(senior|junior|lead|principal|associate|assistant)\s+\w+(?: \w+)?$',
            r'^(head|chief|dean|director)\s+of\s+.+$',
            r'^\w+\s+(head|chief|dean|manager|director|coordinator)$',
            r'^(professor|lecturer|reader)\s+(of|in)\s+.+$'
        ]
        
        for pattern in position_patterns:
            if re.match(pattern, line, re.IGNORECASE):
                return line.strip()
    
    return ""

def process_contact_data(text_content):
    """Process contact data and return structured information."""
    name, rank = extract_name_and_rank(text_content)
    position = extract_position_title(text_content, name, rank)
    
    # If name is generic or incomplete, try to fix it
    if name in ["of School", "Unknown Contact", "Contact"] or len(name.strip()) < 3:
        # Try alternative extraction for problematic cases
        lines = [line.strip() for line in text_content.split('\n') if line.strip()]
        
        # Look for patterns like "Head of School" and try to find the actual name
        for i, line in enumerate(lines):
            if "head of school" in line.lower() and i > 0:
                # Check previous lines for a name
                for j in range(max(0, i-3), i):
                    potential_name = lines[j]
                    if re.match(r'^[A-Z][a-z\-\']+(?: [A-Z][a-z\-\']+){1,3}$', potential_name):
                        name = potential_name
                        break
                break
    
    return {
        'name': name or "Unknown Contact",
        'rank': rank,
        'position': position
    }

def split_multiple_contacts(text):
    """Split text containing multiple contacts into individual blocks."""
    text = clean_text(text)
    
    # Enhanced patterns that indicate the start of a new contact
    contact_patterns = [
        r'\n(?=Professor [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s|$))',
        r'\n(?=Dr\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s|$))',
        r'\n(?=Manager [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s|$))',
        r'\n(?=Director [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s|$))',
        r'\n(?=Mr\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s|$))',
        r'\n(?=Ms\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s|$))',
        r'\n(?=Mrs\.?\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s|$))',
        r'\n(?=Head [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s|$))',
        r'\n(?=Chief [A-Z][a-z]+(?:\s+[A-Z][a-z]+)*(?:\s|$))',
    ]
    
    # Try each pattern
    for pattern in contact_patterns:
        parts = re.split(pattern, text)
        if len(parts) > 1:
            result = []
            for part in parts:
                part = part.strip()
                if len(part) > 30:  # Minimum viable contact length
                    result.append(part)
            if len(result) > 1:
                return result
    
    return [text]

def extract_email_addresses(text):
    text = clean_text(text)
    pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(pattern, text, re.IGNORECASE)
    return emails[0].lower().strip() if emails else ""

def extract_phone_numbers(text):
    text = clean_text(text)
    patterns = [
        r'\+44\s*\(0\)\s*\d{2,4}\s+\d{3,4}\s+\d{4}',
        r'\+44\s*\d{2,4}\s+\d{3,4}\s+\d{4}',
        r'0\d{2,4}\s+\d{3,4}\s+\d{4}',
        r'\+44\s*\d{4}\s+\d{6}',
        r'0\d{10}'
    ]
    for p in patterns:
        match = re.search(p, text)
        if match:
            return re.sub(r'\s+', ' ', match.group().strip())
    return ""

def extract_address(text):
    text = clean_text(text)
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    indicators = ['address', 'located in', 'university address', 'house', 'street', 'road', 'avenue', 'building', 'london', 'kingdom']
    address_lines = []
    for line in lines:
        if any(ind in line.lower() for ind in indicators):
            address_lines.append(line)
    return ", ".join(address_lines) if address_lines else ""

def get_organization_from_filename(filename):
    filename_lower = filename.lower().replace('.txt', '').replace('-contacts', '')
    mappings = {
        'birkbeck': 'Birkbeck, University of London',
        'birbeck': 'Birkbeck, University of London',  # Handle typo
        'open-univ': 'The Open University',
        'st.george': "St George's, University of London",
        'st.george\'s': "St George's, University of London",
        'cambridge': 'University of Cambridge',
        'oxford': 'University of Oxford',
        'barclays': 'Barclays Bank',
        'hsbc': 'HSBC Bank',
        'lloyds': 'Lloyds Bank',
        'natwest': 'NatWest Bank',
    }
    for key, org in mappings.items():
        if key in filename_lower:
            return org
    return filename.replace('=', ' ').replace('_', ' ').replace('-', ' ')

def determine_sector(file_path):
    parts = [p.lower() for p in Path(file_path).parts]
    if 'education' in parts:
        return 'education'
    if 'finance' in parts or 'bank' in parts:
        return 'finance'
    return 'general'

def parse_contact_block(contact_text, source_filename, file_path):
    """Parse contact block using the working process_contact_data function."""
  
    contact_data = process_contact_data(contact_text)
  
    result = {
        'name': contact_data['name'],
        'rank/title': contact_data['rank'],
        'position': contact_data['position'],
        'email': extract_email_addresses(contact_text),
        'phone': extract_phone_numbers(contact_text),
        'organization': get_organization_from_filename(source_filename),
        'address': extract_address(contact_text),
        'source': source_filename,
        'sector': determine_sector(file_path)
    }
    
    return result

def extract_contacts_from_file(file_path):
    contacts = []
    filename = os.path.basename(file_path)

    with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read().strip()

    if len(content) < 15:
        return contacts

    blocks = split_multiple_contacts(content)   # instead of re.split(...)

    for block in blocks:
        block = block.strip()
        if len(block) < 15:
            continue
        contact = parse_contact_block(block, filename, file_path)
        if contact["name"] != "Unknown Contact" or contact["email"] or contact["phone"]:
            contacts.append(contact)
    return contacts
    
def main():
    if len(sys.argv) < 3:
        print("Usage: python fixed_extract.py <source_directory> <output_directory>")
        sys.exit(1)

    source_dir, output_dir = sys.argv[1], sys.argv[2]
    Path(output_dir).mkdir(parents=True, exist_ok=True)

    txt_files = list(Path(source_dir).rglob("*.txt"))
    if not txt_files:
        print("No .txt files found")
        sys.exit(1)
    
    all_contacts = []
    for txt in txt_files:
        all_contacts.extend(extract_contacts_from_file(txt))
    
  
    contacts_by_sector = {}
    for c in all_contacts:
        sector = c.get('sector', 'general')
        contacts_by_sector.setdefault(sector, []).append(c)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    fieldnames = ['name', 'rank/title', 'position', 'email', 'phone', 'organization', 'sector', 'address', 'source']

    created_files = []
    for sector, contacts in contacts_by_sector.items():
        if not contacts:
            continue

        # Deduplication
        unique = {}
        for c in contacts:
            key = (c['name'].lower().strip(), c['organization'].lower())
            if key not in unique:
                unique[key] = c
            else:
                existing = unique[key]
                # Keep the contact with more complete information
                if (c['email'] and not existing['email']) or \
                   (c['position'] and not existing['position']) or \
                   (c['address'] and not existing['address']):
                    unique[key] = c
        final_contacts = list(unique.values())

        if sector == 'education':
            csv_filename = f"edu_adults_contacts_{timestamp}.csv"
        elif sector == 'finance':
            csv_filename = f"banks_contacts_{timestamp}.csv"
        else:
            csv_filename = f"{sector}_contacts_{timestamp}.csv"

        csv_path = Path(output_dir) / csv_filename
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            for c in final_contacts:
                writer.writerow(c)

        created_files.append((csv_filename, len(final_contacts)))

    print(f"\n✅ Extraction completed: {len(created_files)} files")
    for filename, count in created_files:
        print(f"  📊 {filename}: {count} contacts")
        with open(Path(output_dir)/filename, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 3: break
                print(f"    📄 {row['name']} | {row['rank/title']} | {row['position']} | {row['email']} | {row['phone']} | {row['organization']} | {row['sector']} | {row['address']} | {row['source']}")

if __name__ == "__main__":
    main()
