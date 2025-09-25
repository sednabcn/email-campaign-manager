#!/usr/bin/env python3
"""
Universal Contact Extraction Script
Handles contacts from multiple sectors: academic, healthcare, industry, business, finance, etc.
"""

import os
import sys
import csv
import re
from datetime import datetime
from pathlib import Path

def extract_name_from_text(text):
    """Extract person's name from various contact formats"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    if not lines:
        return ""
    
    # Check first few lines for name patterns
    for line in lines[:5]:
        # Skip obvious non-name lines
        if any(skip in line.lower() for skip in 
               ['email:', 'phone:', 'tel:', 'fax:', 'website:', 'address:', 'www.', 'http', '@']):
            continue
        
        # Pattern 1: Title + Name (Academic, Medical, Business)
        title_patterns = [
            r'^(?:Professor|Prof\.?|Dr\.?|Doctor|Mr\.?|Ms\.?|Mrs\.?|Miss|Sir|Dame)\s+(.+?)(?:\s*$)',
            r'^(?:CEO|CTO|CFO|COO|Director|Manager|Head|Lead|Chief|President|VP|Vice President)\s+(.+?)(?:\s*$)',
            r'^(?:Consultant|Specialist|Analyst|Engineer|Developer|Designer|Coordinator)\s+(.+?)(?:\s*$)'
        ]
        
        for pattern in title_patterns:
            match = re.search(pattern, line, re.IGNORECASE)
            if match:
                name = match.group(1).strip()
                # Validate name format
                words = name.split()
                if 2 <= len(words) <= 4 and all(len(w) > 1 for w in words):
                    # Check it's not a department/company name
                    if not any(indicator in name.lower() for indicator in 
                              ['ltd', 'inc', 'corp', 'company', 'department', 'school', 'hospital', 'clinic']):
                        return name
        
        # Pattern 2: Name followed by position/title on same or next line
        if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s*,|\s*$)', line):
            name_candidate = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', line)
            if name_candidate:
                name = name_candidate.group(1).strip()
                # Check next line for position confirmation
                if len(lines) > lines.index(line) + 1:
                    next_line = lines[lines.index(line) + 1].lower()
                    if any(pos in next_line for pos in 
                           ['director', 'manager', 'head', 'lead', 'chief', 'officer', 'consultant', 
                            'specialist', 'analyst', 'engineer', 'coordinator', 'supervisor']):
                        return name
                # Or if line ends with comma (suggesting title follows)
                if line.endswith(','):
                    return name.rstrip(',')
        
        # Pattern 3: Standard name format (2-3 capitalized words)
        if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?(?:\s*$)', line):
            words = line.split()
            if 2 <= len(words) <= 3:
                # Not a company or department
                if not any(indicator in line.lower() for indicator in 
                          ['hospital', 'clinic', 'university', 'college', 'company', 'corporation', 
                           'ltd', 'inc', 'llc', 'department', 'division', 'office']):
                    return line
    
    return ""

def extract_position_title(text):
    """Extract job title/position from various sectors"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Common position indicators across sectors
    position_patterns = [
        # Academic
        r'(?:professor|lecturer|researcher|dean|head of)',
        # Healthcare  
        r'(?:doctor|consultant|specialist|nurse|surgeon|physician|therapist)',
        # Business/Finance
        r'(?:ceo|cfo|cto|coo|director|manager|analyst|executive|president|vp|vice president)',
        # Industry/Tech
        r'(?:engineer|developer|designer|architect|lead|senior|junior|coordinator)',
        # General
        r'(?:head of|chief|officer|supervisor|administrator|representative)'
    ]
    
    for line in lines:
        line_lower = line.lower()
        
        # Direct position match
        for pattern in position_patterns:
            if re.search(pattern, line_lower):
                # Clean up the position
                position = line.strip()
                # Remove prefixes like "Position:" or "Title:"
                position = re.sub(r'^(?:position|title|role|job):\s*', '', position, flags=re.IGNORECASE)
                if len(position) > 3:  # Avoid very short matches
                    return position
    
    return ""

def extract_email_addresses(text):
    """Extract all email addresses, prioritizing real ones"""
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = re.findall(email_pattern, text, re.IGNORECASE)
    
    # Known placeholder/generic emails to flag
    placeholder_patterns = [
        'alerts@modelphysmat.com',
        'info@company.com',
        'contact@example.com', 
        'noreply@',
        'admin@',
        'support@'
    ]
    
    real_emails = []
    placeholder_emails = []
    
    for email in emails:
        email_lower = email.lower()
        is_placeholder = any(pattern.lower() in email_lower for pattern in placeholder_patterns)
        
        if is_placeholder:
            placeholder_emails.append(email + " [PLACEHOLDER]")
        else:
            real_emails.append(email.lower().strip())
    
    # Return best email (real first, then placeholder)
    if real_emails:
        return real_emails[0]
    elif placeholder_emails:
        return placeholder_emails[0]
    
    return ""

def extract_phone_numbers(text):
    """Extract phone numbers in various international formats"""
    phone_patterns = [
        r'\+\d{1,3}[-.\s]?\(?\d{1,4}\)?[-.\s]?\d{1,4}[-.\s]?\d{1,9}',  # International
        r'\+44\s?\(0\)\d{2,4}\s?\d{4}\s?\d{4}',  # UK format
        r'\+1[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',  # US format
        r'\(\d{3,4}\)[-.\s]?\d{3,4}[-.\s]?\d{4}',  # (xxx) xxx-xxxx
        r'\d{3,4}[-.\s]\d{3,4}[-.\s]\d{4,6}',  # xxx-xxx-xxxx
        r'\d{10,15}',  # Plain digits (10-15 digits)
    ]
    
    for pattern in phone_patterns:
        phones = re.findall(pattern, text)
        if phones:
            # Clean up the first phone found
            phone = phones[0].strip()
            # Remove extra characters but keep formatting
            phone = re.sub(r'[^\d\+\(\)\s-]', '', phone)
            if len(phone) >= 10:  # Minimum valid phone length
                return phone
    
    return ""

def extract_organization_info(text, filename):
    """Extract organization/company information"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    
    # Organization indicators
    org_patterns = [
        r'(?:university|college|school|institute)',
        r'(?:hospital|clinic|medical center|health)',
        r'(?:company|corporation|corp|ltd|llc|inc)',
        r'(?:bank|financial|insurance)',
        r'(?:department|division|office)',
        r'(?:group|organization|association)'
    ]
    
    # Look for organization in text
    for line in lines:
        line_lower = line.lower()
        for pattern in org_patterns:
            if re.search(pattern, line_lower):
                # Clean organization name
                org = line.strip()
                if len(org) > 5 and not '@' in org:  # Avoid email lines
                    return org
    
    # Fallback: extract from filename
    return get_organization_from_filename(filename)

def get_organization_from_filename(filename):
    """Map filename to organization name"""
    filename_lower = filename.lower().replace('.txt', '').replace('-contacts', '')
    
    # Known mappings
    org_mappings = {
        'birbeck': 'Birkbeck, University of London',
        'open-univ': 'The Open University', 
        'st.george': "St George's, University of London",
        'nhs': 'NHS',
        'hsbc': 'HSBC',
        'barclays': 'Barclays',
        'goldman': 'Goldman Sachs',
        'microsoft': 'Microsoft',
        'google': 'Google',
        'amazon': 'Amazon'
    }
    
    for key, org in org_mappings.items():
        if key in filename_lower:
            return org
    
    # Generic cleanup
    org = filename_lower.replace('=', ' ').replace('-', ' ').replace('_', ' ')
    org = ' '.join(word.capitalize() for word in org.split())
    
    return org if org else "Unknown Organization"

def extract_address_info(text):
    """Extract address information from various formats"""
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    address_lines = []
    capture_address = False
    
    for line in lines:
        # Start capturing after "Address:", "Location:", etc.
        if re.search(r'\b(address|location|office|building):', line, re.IGNORECASE):
            capture_address = True
            # Include cleaned line
            clean_line = re.sub(r'^.*?(?:address|location|office):\s*', '', line, flags=re.IGNORECASE)
            if clean_line and len(clean_line) > 3:
                address_lines.append(clean_line)
            continue
        
        # Stop capturing at email, phone, or other contact info
        if capture_address and re.search(r'[@📧📞🔗http]|email:|phone:|tel:|website:', line, re.IGNORECASE):
            break
        
        # Capture address lines
        if capture_address:
            # Skip obvious non-address lines
            if not any(skip in line.lower() for skip in 
                      ['email:', 'phone:', 'tel:', 'website:', 'profile:', '---', 'fax:']):
                if len(line) > 3:
                    address_lines.append(line)
        
        # Also capture lines that look like addresses (postcodes, street numbers)
        elif not capture_address:
            if re.search(r'\b\d+\s+\w+\s+(street|road|avenue|lane|drive|way|close)', line, re.IGNORECASE):
                address_lines.append(line)
            elif re.search(r'\b[A-Z]{1,2}\d{1,2}[A-Z]?\s?\d[A-Z]{2}\b', line):  # UK postcode
                address_lines.append(line)
    
    return ' | '.join(address_lines) if address_lines else ""

def detect_sector(text, filename):
    """Detect the sector/industry from content"""
    text_lower = text.lower()
    filename_lower = filename.lower()
    
    # Sector keywords
    sectors = {
        'Academic': ['university', 'college', 'school', 'professor', 'lecturer', 'research', 'academic'],
        'Healthcare': ['hospital', 'clinic', 'medical', 'doctor', 'nurse', 'physician', 'health', 'nhs'],
        'Finance': ['bank', 'financial', 'insurance', 'investment', 'trading', 'analyst', 'fund'],
        'Technology': ['software', 'developer', 'engineer', 'tech', 'digital', 'IT', 'programming'],
        'Business': ['company', 'corporation', 'business', 'executive', 'manager', 'director', 'ceo'],
        'Government': ['government', 'ministry', 'department', 'public', 'civil service', 'council'],
        'Legal': ['law', 'legal', 'solicitor', 'barrister', 'lawyer', 'court', 'judicial']
    }
    
    sector_scores = {}
    combined_text = text_lower + ' ' + filename_lower
    
    for sector, keywords in sectors.items():
        score = sum(1 for keyword in keywords if keyword in combined_text)
        if score > 0:
            sector_scores[sector] = score
    
    if sector_scores:
        return max(sector_scores, key=sector_scores.get)
    
    return "General"

def parse_contact_block(contact_text, source_filename):
    """Parse a contact block from any sector"""
    # Extract all components
    name = extract_name_from_text(contact_text)
    position = extract_position_title(contact_text)
    email = extract_email_addresses(contact_text)
    phone = extract_phone_numbers(contact_text)
    organization = extract_organization_info(contact_text, source_filename)
    address = extract_address_info(contact_text)
    sector = detect_sector(contact_text, source_filename)
    
    # Clean raw data for storage
    raw_data = ' '.join(contact_text.split()).strip()[:500]
    
    return {
        'name': name if name else "Unknown Contact",
        'position': position,
        'email': email,
        'phone': phone,
        'organization': organization,
        'address': address,
        'sector': sector,
        'raw_data': raw_data,
        'source_file': source_filename
    }

def extract_contacts_from_file(file_path):
    """Extract contacts from any type of contact file"""
    contacts = []
    filename = os.path.basename(file_path)
    
    print(f"  📄 Processing: {file_path}")
    
    try:
        # Try different encodings
        encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252', 'iso-8859-1']
        content = None
        
        for encoding in encodings:
            try:
                with open(file_path, 'r', encoding=encoding) as f:
                    content = f.read()
                print(f"     ✅ Read successfully with {encoding} encoding")
                break
            except UnicodeDecodeError:
                continue
        
        if content is None:
            print(f"     ❌ Could not decode file with any encoding")
            return contacts
        
        # Detect separator and split content
        contact_blocks = []
        
        # Method 1: Split by separator lines (----, ===, etc.)
        if re.search(r'^[-=*]{3,}$', content, re.MULTILINE):
            contact_blocks = re.split(r'^[-=*]{3,}$', content, flags=re.MULTILINE)
            print(f"     🔗 Split by separators: {len(contact_blocks)} blocks")
        
        # Method 2: Split by multiple blank lines
        elif re.search(r'\n\s*\n\s*\n', content):
            contact_blocks = re.split(r'\n\s*\n\s*\n+', content)
            print(f"     🔗 Split by blank lines: {len(contact_blocks)} blocks")
        
        # Method 3: Split by repeated patterns (names, emails)
        elif len(re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)) > 1:
            # Split by email pattern (assuming each contact has an email)
            email_positions = [m.start() for m in re.finditer(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', content)]
            if len(email_positions) > 1:
                blocks = []
                for i, pos in enumerate(email_positions):
                    if i == 0:
                        start = 0
                    else:
                        # Find a good break point before this email
                        prev_newlines = [m.start() for m in re.finditer(r'\n\s*\n', content[:pos])]
                        start = prev_newlines[-1] if prev_newlines else 0
                    
                    if i < len(email_positions) - 1:
                        next_pos = email_positions[i + 1]
                        next_newlines = [m.start() for m in re.finditer(r'\n\s*\n', content[pos:next_pos])]
                        end = pos + next_newlines[0] if next_newlines else next_pos
                    else:
                        end = len(content)
                    
                    blocks.append(content[start:end])
                
                contact_blocks = blocks
                print(f"     🔗 Split by email patterns: {len(contact_blocks)} blocks")
        
        # Fallback: treat as single contact
        if len(contact_blocks) <= 1:
            contact_blocks = [content]
            print(f"     🔗 Treating as single contact")
        
        # Process each block
        for i, block in enumerate(contact_blocks):
            block = block.strip()
            if len(block) < 20:  # Skip very short blocks
                continue
            
            print(f"     🔍 Processing block {i+1}:")
            print(f"       Preview: {block[:80].replace(chr(10), ' ')}...")
            
            contact = parse_contact_block(block, filename)
            
            # Quality check - only add if we have meaningful info
            has_name = contact['name'] != "Unknown Contact"
            has_email = contact['email'] and not contact['email'].isspace()
            has_phone = contact['phone'] and not contact['phone'].isspace()
            
            if has_name or has_email or has_phone:
                contacts.append(contact)
                print(f"       ✅ Extracted: {contact['name']} ({contact['sector']})")
                print(f"          📧 {contact['email']}")
                print(f"          📞 {contact['phone']}")
                print(f"          🏢 {contact['organization']}")
            else:
                print(f"       ❌ Skipped: insufficient contact information")
    
    except Exception as e:
        print(f"     ❌ ERROR: {str(e)}")
    
    return contacts

def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_contacts.py <source_directory> <output_directory>")
        print("Example: python extract_contacts.py contact_details contacts")
        sys.exit(1)
    
    source_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    print(f"🌐 Universal Contact Extraction Script")
    print(f"📂 Source Directory: {source_dir}")
    print(f"📁 Output Directory: {output_dir}")
    print(f"🕒 Timestamp: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 70)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory ready: {output_path.absolute()}")
    
    # Find all .txt files recursively
    txt_files = []
    source_path = Path(source_dir)
    
    if source_path.exists():
        txt_files = list(source_path.rglob("*.txt"))
        print(f"🔍 Searching recursively in: {source_path.absolute()}")
    else:
        print(f"⚠️  Source directory does not exist: {source_dir}")
    
    if not txt_files:
        print(f"📭 No .txt files found in {source_dir}")
        # Create empty CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        csv_filename = f"contacts_extracted_{timestamp}.csv"
        csv_path = output_path / csv_filename
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'position', 'email', 'phone', 'organization', 'address', 'sector', 'raw_data', 'source_file']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
        
        print(f"📄 Created empty CSV file: {csv_path}")
        return
    
    print(f"📋 Found {len(txt_files)} text files:")
    for txt_file in sorted(txt_files):
        file_size = txt_file.stat().st_size if txt_file.exists() else 0
        print(f"  📄 {txt_file.name} ({file_size:,} bytes)")
        print(f"     📁 Path: {txt_file}")
    print()
    
    # Extract contacts from all files
    all_contacts = []
    sector_counts = {}
    
    for txt_file in sorted(txt_files):
        print(f"🔄 Processing: {txt_file.name}")
        file_contacts = extract_contacts_from_file(txt_file)
        all_contacts.extend(file_contacts)
        
        # Count sectors
        for contact in file_contacts:
            sector = contact['sector']
            sector_counts[sector] = sector_counts.get(sector, 0) + 1
        
        print(f"  ✅ Extracted {len(file_contacts)} contacts from {txt_file.name}")
        for contact in file_contacts:
            print(f"     👤 {contact['name']} ({contact['sector']}) - {contact['organization']}")
            print(f"        📧 {contact['email']} | 📞 {contact['phone']}")
        print()
    
    print(f"🔄 Deduplicating {len(all_contacts)} contacts...")
    
    # Deduplicate contacts
    unique_contacts = {}
    for contact in all_contacts:
        # Create key for deduplication
        email_key = contact['email'].replace(" [PLACEHOLDER]", "").lower().strip()
        name_key = contact['name'].strip().lower()
        org_key = contact['organization'].strip().lower()
        
        key = (email_key, name_key, org_key)
        
        if key not in unique_contacts:
            unique_contacts[key] = contact
        else:
            # Merge data (prefer real emails, complete info)
            existing = unique_contacts[key]
            
            # Prefer real emails over placeholders
            if "[PLACEHOLDER]" in existing['email'] and "[PLACEHOLDER]" not in contact['email']:
                existing['email'] = contact['email']
            
            # Fill in missing fields
            for field in ['phone', 'position', 'address']:
                if not existing[field] and contact[field]:
                    existing[field] = contact[field]
    
    final_contacts = list(unique_contacts.values())
    print(f"✨ After deduplication: {len(final_contacts)} unique contacts")
    
    # Create output CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    csv_filename = f"contacts_extracted_{timestamp}.csv"
    csv_path = output_path / csv_filename
    
    print(f"💾 Creating CSV file: {csv_filename}")
    
    try:
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['name', 'position', 'email', 'phone', 'organization', 'address', 'sector', 'raw_data', 'source_file']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for contact in final_contacts:
                writer.writerow(contact)
        
        # Success verification
        if csv_path.exists():
            file_size = csv_path.stat().st_size
            print(f"✅ CSV file created successfully!")
            print(f"   📄 File: {csv_filename}")
            print(f"   📏 Size: {file_size:,} bytes")
            print(f"   📊 Records: {len(final_contacts)}")
            
            # Email analysis
            placeholder_count = sum(1 for c in final_contacts if "[PLACEHOLDER]" in c.get('email', ''))
            real_email_count = len(final_contacts) - placeholder_count
            print(f"   📧 Real emails: {real_email_count}")
            print(f"   🏷️  Placeholder emails: {placeholder_count}")
        else:
            print(f"❌ CSV file creation failed")
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Error writing CSV: {e}")
        sys.exit(1)
    
    # Final summary
    print("=" * 70)
    print(f"📊 Extraction Summary:")
    print(f"   📄 Files processed: {len(txt_files)}")
    print(f"   👥 Total contacts: {len(all_contacts)}")
    print(f"   ✨ Unique contacts: {len(final_contacts)}")
    print(f"   💾 Output file: {csv_filename}")
    
    # Sector breakdown
    final_sector_counts = {}
    for contact in final_contacts:
        sector = contact['sector']
        final_sector_counts[sector] = final_sector_counts.get(sector, 0) + 1
    
    print(f"\n🏢 Sector Breakdown:")
    for sector, count in sorted(final_sector_counts.items()):
        print(f"   {sector}: {count} contacts")
    
    # Source file breakdown
    source_counts = {}
    for contact in final_contacts:
        source = contact['source_file']
        source_counts[source] = source_counts.get(source, 0) + 1
    
    print(f"\n📂 Source File Breakdown:")
    for source, count in sorted(source_counts.items()):
        print(f"   📄 {source}: {count} contacts")
    
    print(f"\n👀 Sample Extracted Contacts:")
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for i, row in enumerate(reader):
                if i >= 3:  # Show first 3 contacts
                    break
                print(f"  📝 Contact {i+1}:")
                print(f"    👤 Name: '{row['name']}'")
                print(f"    💼 Position: '{row['position']}'")
                print(f"    📧 Email: '{row['email']}'")
                print(f"    📞 Phone: '{row['phone']}'")
                print(f"    🏢 Organization: '{row['organization']}'")
                print(f"    🏷️  Sector: '{row['sector']}'")
                print(f"    📍 Address: '{row['address'][:60]}{'...' if len(row['address']) > 60 else ''}'")
                print(f"    📄 Source: '{row['source_file']}'")
                print()
    except Exception as e:
        print(f"Error reading preview: {e}")
    
    print(f"🎉 Extraction completed successfully!")
    print(f"📁 Full path: {csv_path}")

if __name__ == "__main__":
    main()
