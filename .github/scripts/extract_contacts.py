#!/usr/bin/env python3
"""
Fixed Universal Contact Extraction Script
Handles academic contact formats properly
"""

import os
import sys
import csv
import re
from datetime import datetime
from pathlib import Path

def extract_name_and_rank(text):
    """Extract name and academic/professional rank separately"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if not lines:
        return "", ""
    
    # Look for title + name patterns
    for line in lines[:5]:
        if any(skip in line.lower() for skip in ['email:', 'phone:', 'tel:', 'address:', 'www.', 'http', '@', 'position:', 'school of', 'university']):
            continue
        
        # Academic title patterns - capture name without title
        title_patterns = [
            (r'^(Professor)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'Professor'),
            (r'^(Prof\.?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'Professor'),
            (r'^(Dr\.?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'Dr'),
            (r'^(Mr\.?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'Mr'),
            (r'^(Ms\.?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'Ms'),
            (r'^(Mrs\.?)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'Mrs'),
        ]
        
        for pattern, rank in title_patterns:
            match = re.search(pattern, line)
            if match:
                name = match.group(2).strip()  # Just the name without title
                print(f"    Found: rank='{rank}', name='{name}' from line: '{line}'")
                return name, rank
        
        # Business title patterns
        business_patterns = [
            (r'^(CEO)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'CEO'),
            (r'^(CTO)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'CTO'),
            (r'^(CFO)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'CFO'),
            (r'^(Director)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'Director'),
            (r'^(Manager)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', 'Manager'),
        ]
        
        for pattern, rank in business_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                name = match.group(2).strip()  # Just the name without title
                print(f"    Found: rank='{rank}', name='{name}' from line: '{line}'")
                return name, rank
    
    # Fallback: Look for standalone name in first line
    first_line = lines[0]
    if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?$', first_line):
        if not any(indicator in first_line.lower() for indicator in 
                  ['university', 'college', 'hospital', 'school', 'company']):
            print(f"    Found standalone name: '{first_line}'")
            return first_line, ""
    
    print(f"    No name found in text preview: '{text[:100].replace(chr(10), ' ')}...'")
    return "", ""

def extract_position_title(text):
    """Enhanced position extraction"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Look for position patterns
    position_patterns = [
        r'Head of (?:the )?(.+)',
        r'Professor of (.+)',
        r'Director of (.+)',
        r'Manager of (.+)',
        r'Chief (.+)',
    ]
    
    for line in lines:
        line_clean = line.strip()
        
        # Remove "Position:" prefix if present
        if line_clean.lower().startswith('position:'):
            line_clean = re.sub(r'^position:\s*', '', line_clean, flags=re.IGNORECASE)
        
        # Direct position indicators
        if any(indicator in line.lower() for indicator in 
               ['head of school', 'head of department', 'head of the department', 'professor', 'director', 'manager', 'chief']):
            print(f"    Found position: '{line_clean}'")
            return line_clean
    
    return ""

def extract_email_addresses(text):
    """Extract clean email addresses without placeholder markers"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text, re.IGNORECASE)
    
    if not emails:
        return ""
    
    # Return the first email found, clean (no placeholder markers)
    return emails[0].lower().strip()

def extract_phone_numbers(text):
    """Enhanced phone extraction for UK numbers"""
    # UK-specific patterns
    uk_patterns = [
        r'\+44\s?\(0\)\d{2,4}\s?\d{4}\s?\d{4}',    # +44 (0)20 1234 5678
        r'\+44\s?\d{2,4}\s?\d{4}\s?\d{4}',         # +44 20 1234 5678
        r'0\d{2,4}\s?\d{4}\s?\d{4}',               # 020 1234 5678
        r'\+44\s?\d{4}\s?\d{6}',                   # +44 1234 567890
    ]
    
    for pattern in uk_patterns:
        phones = re.findall(pattern, text)
        if phones:
            phone = phones[0].strip()
            print(f"    Found phone: '{phone}'")
            return phone
    
    return ""

def get_organization_from_filename(filename):
    """Enhanced filename mapping"""
    filename_lower = filename.lower().replace('.txt', '').replace('-contacts', '')
    
    org_mappings = {
        'birbeck': 'Birkbeck, University of London',
        'open-univ': 'The Open University', 
        'st.george': "St George's, University of London",
        'cambridge': 'University of Cambridge',
        'oxford': 'University of Oxford',
        'barclays': 'Barclays Bank',
    }
    
    for key, org in org_mappings.items():
        if key in filename_lower:
            return org
    
    # Generic cleanup
    org = filename_lower.replace('=', ' ').replace('-', ' ').replace('_', ' ')
    org = ' '.join(word.capitalize() for word in org.split())
    return org if org else "Unknown Organization"

def get_category_from_path(file_path):
    """Extract category from file path structure"""
    path_parts = Path(file_path).parts
    
    # Look for meaningful directory names
    categories = []
    for part in path_parts:
        part_lower = part.lower()
        if part_lower in ['education', 'finance', 'healthcare', 'technology', 'business', 'government']:
            categories.append(part_lower)
        elif part_lower in ['adult_education', 'banks', 'hospitals', 'universities']:
            categories.append(part_lower)
    
    if categories:
        return '_'.join(categories)
    
    # Fallback to parent directory name
    parent = Path(file_path).parent.name.lower()
    if parent and parent != 'contacts':
        return parent
    
    return 'general'

def extract_address_info(text):
    """Enhanced address extraction"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    address_lines = []
    capture_address = False
    
    for line in lines:
        # Start capturing after address indicators
        if re.search(r'\b(address|location|office):', line, re.IGNORECASE):
            capture_address = True
            # Include the cleaned line
            clean_line = re.sub(r'^.*?(?:address|location|office):\s*', '', line, flags=re.IGNORECASE)
            if clean_line and len(clean_line) > 5:
                address_lines.append(clean_line)
            continue
        
        # Stop at contact info
        if capture_address and re.search(r'[@📧📞]|email:|phone:|tel:', line, re.IGNORECASE):
            break
        
        # Capture lines while in address mode
        if capture_address:
            if not any(skip in line.lower() for skip in ['email:', 'phone:', 'tel:', 'profile:']):
                if len(line) > 5:
                    address_lines.append(line)
        
        # Also capture obvious address lines
        elif not capture_address:
            if (re.search(r'\b\d+\s+\w+\s+(street|road|avenue|lane)', line, re.IGNORECASE) or
                re.search(r'\b[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}\b', line)):  # UK postcode
                address_lines.append(line)
    
    return ' | '.join(address_lines) if address_lines else ""

def detect_sector(text, filename):
    """Detect sector from content"""
    text_lower = text.lower()
    filename_lower = filename.lower()
    combined = f"{text_lower} {filename_lower}"
    
    sectors = {
        'Academic': ['university', 'college', 'school', 'professor', 'lecturer', 'research'],
        'Healthcare': ['hospital', 'clinic', 'medical', 'doctor', 'nhs'],
        'Finance': ['bank', 'financial', 'insurance', 'investment'],
        'Technology': ['software', 'tech', 'digital', 'IT'],
        'Business': ['company', 'corporation', 'business', 'executive'],
        'Government': ['government', 'ministry', 'department', 'council'],
    }
    
    sector_scores = {}
    for sector, keywords in sectors.items():
        score = sum(1 for keyword in keywords if keyword in combined)
        if score > 0:
            sector_scores[sector] = score
    
    return max(sector_scores, key=sector_scores.get) if sector_scores else "General"

def parse_contact_block(contact_text, source_filename, file_path):
    """Parse contact block with name/rank separation and better categorization"""
    print(f"  Parsing contact block from {source_filename}:")
    
    # Extract components
    name, rank = extract_name_and_rank(contact_text)
    position = extract_position_title(contact_text)
    email = extract_email_addresses(contact_text)
    phone = extract_phone_numbers(contact_text)
    organization = get_organization_from_filename(source_filename)
    address = extract_address_info(contact_text)
    sector = detect_sector(contact_text, source_filename)
    category = get_category_from_path(file_path)
    
    # Clean raw data
    raw_data = ' '.join(contact_text.split()).strip()[:500]
    
    contact = {
        'name': name if name else "Unknown Contact",
        'rank': rank,
        'position': position,
        'email': email,
        'phone': phone,
        'organization': organization,
        'address': address,
        'sector': sector,
        'category': category,
        'raw_data': raw_data,
        'source_file': source_filename
    }
    
    print(f"    Result: {contact['name']} | {contact['rank']} | {contact['position']} | {contact['email']}")
    return contact

def extract_contacts_from_file(file_path):
    """Extract contacts with better content splitting"""
    contacts = []
    filename = os.path.basename(file_path)
    
    print(f"📄 Processing: {file_path}")
    
    try:
        # Read file with encoding detection
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"  ✅ Read with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"  ❌ Could not decode file")
            return contacts
        
        print(f"  📝 File content preview: {content[:200].replace(chr(10), ' ')}...")
        
        # Split content into blocks
        contact_blocks = []
        
        # Method 1: Split by horizontal lines
        if re.search(r'^[-=*]{3,}$', content, re.MULTILINE):
            contact_blocks = re.split(r'^[-=*]{3,}$', content, flags=re.MULTILINE)
            print(f"  🔗 Split by separators: {len(contact_blocks)} blocks")
        
        # Method 2: Split by multiple newlines
        elif re.search(r'\n\s*\n\s*\n', content):
            contact_blocks = re.split(r'\n\s*\n\s*\n+', content)
            print(f"  🔗 Split by blank lines: {len(contact_blocks)} blocks")
        
        # Method 3: Split by "Professor" occurrences (for academic files)
        elif content.count('Professor') > 1:
            # Split on Professor but keep it in the result
            parts = re.split(r'(?=Professor)', content)
            contact_blocks = [part for part in parts if part.strip()]
            print(f"  🔗 Split by 'Professor': {len(contact_blocks)} blocks")
        
        # Fallback: single contact
        else:
            contact_blocks = [content]
            print(f"  🔗 Single contact block")
        
        # Process each block
        for i, block in enumerate(contact_blocks):
            block = block.strip()
            if len(block) < 20:
                continue
            
            print(f"  📋 Block {i+1}:")
            print(f"    Content: {block[:100].replace(chr(10), ' ')}...")
            
            contact = parse_contact_block(block, filename, file_path)
            
            # Quality check
            if (contact['name'] != "Unknown Contact" or 
                (contact['email'] and contact['email'] != "") or
                contact['phone']):
                contacts.append(contact)
                print(f"    ✅ Added contact: {contact['name']}")
            else:
                print(f"    ❌ Skipped: insufficient data")
    
    except Exception as e:
        print(f"  ❌ Error: {e}")
    
    return contacts

def main():
    if len(sys.argv) < 3:
        print("Usage: python fixed_extract_contacts.py <source_directory> <output_directory>")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    print(f"🌐 Fixed Universal Contact Extraction Script")
    print(f"📂 Source: {source_dir}")
    print(f"📁 Output: {output_dir}")
    print(f"🕒 Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    
    # Find source files
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"❌ Source directory not found: {source_dir}")
        sys.exit(1)
    
    txt_files = list(source_path.rglob("*.txt"))
    if not txt_files:
        print(f"📭 No .txt files found")
        sys.exit(1)
    
    print(f"📋 Found {len(txt_files)} files:")
    for txt_file in sorted(txt_files):
        size = txt_file.stat().st_size
        print(f"  📄 {txt_file.name} ({size:,} bytes)")
    print()
    
    # Extract contacts
    all_contacts = []
    for txt_file in sorted(txt_files):
        file_contacts = extract_contacts_from_file(txt_file)
        all_contacts.extend(file_contacts)
        print(f"  → {len(file_contacts)} contacts extracted")
        print()
    
    # Deduplication (improved to avoid repetition)
    print(f"🔄 Deduplicating {len(all_contacts)} contacts...")
    unique_contacts = {}
    
    for contact in all_contacts:
        # Create more specific dedup key to avoid over-merging
        key = (
            contact['email'].replace(' [PLACEHOLDER]', '').lower() if contact['email'] else 'no_email',
            contact['name'].lower(),
            contact['organization'].lower(),
            contact['category']  # Add category to avoid merging contacts from different categories
        )
        
        if key not in unique_contacts or key[0] == 'no_email':
            # Always add if no duplicate or if no email (to avoid losing valid contacts)
            unique_key = f"{key}_{len([k for k in unique_contacts.keys() if k[:3] == key[:3]])}"
            unique_contacts[unique_key] = contact
        else:
            # Merge: prefer contact with more complete data
            existing = unique_contacts[key]
            if (len(contact['email']) > len(existing['email']) or
                contact['name'] != "Unknown Contact" and existing['name'] == "Unknown Contact"):
                unique_contacts[key] = contact
    
    final_contacts = list(unique_contacts.values())
    print(f"✨ Final contacts: {len(final_contacts)}")
    
    # Generate category-based filename
    categories = set()
    for contact in final_contacts:
        if contact.get('category'):
            categories.add(contact['category'])
    
    if len(categories) == 1:
        category_name = list(categories)[0]
    elif categories:
        category_name = '_'.join(sorted(categories))
    else:
        category_name = 'general'
    
    # Export to CSV with category-based filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"{category_name}_contacts_{timestamp}.csv"
    csv_path = output_path / csv_filename
    
    fieldnames = ['name', 'rank', 'position', 'email', 'phone', 'organization', 'address', 'sector', 'category', 'raw_data', 'source_file']
    
    with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()
        for contact in final_contacts:
            writer.writerow(contact)
    
    print(f"💾 Created: {csv_filename}")
    print(f"📏 Size: {csv_path.stat().st_size:,} bytes")
    print(f"📊 Records: {len(final_contacts)}")
    
    # Preview results
    print(f"\n👀 Preview:")
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for i, row in enumerate(reader):
            if i >= 3:
                break
            print(f"  📝 {i+1}. {row['name']} ({row['sector']})")
            print(f"     🗂️  Category: {row['category']}")
            print(f"     🎖️  Rank: {row['rank']}")
            print(f"     💼 Position: {row['position']}")
            print(f"     📧 Email: {row['email']}")
            print(f"     📞 Phone: {row['phone']}")
            print(f"     🏢 Organization: {row['organization']}")
            print(f"     📄 Source: {row['source_file']}")
            print()
    
    print(f"🎉 Extraction completed!")

if __name__ == "__main__":
    main()

