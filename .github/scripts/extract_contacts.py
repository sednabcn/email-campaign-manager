#!/usr/bin/env python3
"""
Contact Details Extractor
Extracts contact information from text files and converts to CSV format.
Supports hierarchical directory structure: contacts/subdir_contacts_DATE.csv

This script should be placed at: .github/scripts/extract_contacts.py
"""

import os
import sys
import csv
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict, Optional, Tuple
import logging

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(levelname)s: %(message)s')
logger = logging.getLogger(__name__)

class ContactExtractor:
    """Extracts and processes contact information from text files."""
    
    def __init__(self):
        self.email_pattern = re.compile(r'📧\s*([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})', re.IGNORECASE)
        self.phone_pattern = re.compile(r'📞\s*([+]?[\d\s\-\(\)\.]{8,20})', re.IGNORECASE)
        self.website_pattern = re.compile(r'🌐\s*(https?://[^\s]+|www\.[^\s]+)', re.IGNORECASE)
        
        # Alternative patterns without emojis
        self.email_fallback = re.compile(r'\b([a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,})\b')
        self.phone_fallback = re.compile(r'(?:phone|tel|mobile|call):\s*([+]?[\d\s\-\(\)\.]{8,20})', re.IGNORECASE)
        self.website_fallback = re.compile(r'(?:website|web|url):\s*(https?://[^\s]+|www\.[^\s]+)', re.IGNORECASE)

    def extract_contact_from_text(self, text: str, filename: str) -> Dict[str, str]:
        """Extract contact information from a text block."""
        lines = [line.strip() for line in text.strip().split('\n') if line.strip()]
        
        if not lines:
            return {}
        
        contact = {
            'source_file': filename,
            'name': '',
            'title': '',
            'organization': '',
            'department': '',
            'email': '',
            'phone': '',
            'website': '',
            'address': '',
            'notes': ''
        }
        
        # Extract email (priority: emoji pattern, then fallback)
        email_match = self.email_pattern.search(text) or self.email_fallback.search(text)
        if email_match:
            contact['email'] = email_match.group(1)
        
        # Extract phone
        phone_match = self.phone_pattern.search(text) or self.phone_fallback.search(text)
        if phone_match:
            contact['phone'] = phone_match.group(1).strip()
        
        # Extract website
        website_match = self.website_pattern.search(text) or self.website_fallback.search(text)
        if website_match:
            contact['website'] = website_match.group(1)
        
        # Process lines to extract structured information
        current_section = []
        
        for i, line in enumerate(lines):
            # Skip lines with contact info we've already extracted
            if any(pattern.search(line) for pattern in [
                self.email_pattern, self.phone_pattern, self.website_pattern,
                self.email_fallback, self.phone_fallback, self.website_fallback
            ]):
                continue
            
            # First non-empty line is likely the name
            if i == 0 or (not contact['name'] and not any(keyword in line.lower() for keyword in 
                ['school', 'university', 'college', 'department', 'faculty', 'institute'])):
                if not contact['name'] and not line.startswith(('Prof', 'Dr', 'Mr', 'Ms', 'Mrs')):
                    # Check if this looks like a name (not an organization)
                    if not any(org_keyword in line.lower() for org_keyword in 
                        ['school', 'university', 'college', 'department', 'ltd', 'inc', 'corp']):
                        contact['name'] = line
                        continue
            
            # Detect titles
            if any(title in line for title in ['Professor', 'Prof', 'Dr', 'Head of', 'Director', 'Manager', 'Coordinator']):
                if not contact['title']:
                    contact['title'] = line
                else:
                    contact['title'] += f" / {line}"
                continue
            
            # Detect organizations/departments
            if any(keyword in line.lower() for keyword in 
                ['school', 'university', 'college', 'department', 'faculty', 'institute']):
                if 'school' in line.lower() or 'department' in line.lower():
                    if not contact['department']:
                        contact['department'] = line
                    else:
                        contact['department'] += f" / {line}"
                else:
                    if not contact['organization']:
                        contact['organization'] = line
                    else:
                        contact['organization'] += f" / {line}"
                continue
            
            # Everything else goes to notes or address
            current_section.append(line)
        
        # Process remaining lines as notes/address
        if current_section:
            # Try to identify address vs notes
            address_lines = []
            notes_lines = []
            
            for line in current_section:
                # Simple heuristic: lines with postal codes, street numbers, or common address terms
                if re.search(r'\d{4,5}|\d+\s+\w+\s+(street|road|avenue|lane|drive)|postcode|zip', 
                           line.lower()):
                    address_lines.append(line)
                else:
                    notes_lines.append(line)
            
            contact['address'] = ' | '.join(address_lines)
            contact['notes'] = ' | '.join(notes_lines)
        
        # Clean up the contact - remove empty fields and trim
        for key in contact:
            if isinstance(contact[key], str):
                contact[key] = contact[key].strip()
        
        return contact

    def process_text_file(self, file_path: Path) -> List[Dict[str, str]]:
        """Process a single text file and extract all contacts."""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            try:
                with open(file_path, 'r', encoding='latin-1') as f:
                    content = f.read()
            except Exception as e:
                logger.warning(f"Could not read file {file_path}: {e}")
                return []
        except Exception as e:
            logger.warning(f"Error reading file {file_path}: {e}")
            return []
        
        if not content.strip():
            logger.warning(f"File {file_path} is empty")
            return []
        
        contacts = []
        
        # Split by double newlines or other clear separators
        contact_blocks = re.split(r'\n\s*\n|---+|\*\*\*+|===+', content)
        
        for block in contact_blocks:
            block = block.strip()
            if not block:
                continue
                
            # Skip blocks that don't look like contacts (too short or no key info)
            if len(block) < 20 and not any(pattern.search(block) for pattern in 
                [self.email_pattern, self.email_fallback]):
                continue
            
            contact = self.extract_contact_from_text(block, file_path.name)
            
            # Only add if we extracted meaningful information
            if contact and (contact['email'] or contact['name'] or contact['organization']):
                contacts.append(contact)
        
        # If no contacts found but file has content, treat whole file as one contact
        if not contacts and content.strip():
            contact = self.extract_contact_from_text(content, file_path.name)
            if contact and (contact['email'] or contact['name'] or contact['organization']):
                contacts.append(contact)
        
        logger.info(f"Extracted {len(contacts)} contacts from {file_path.name}")
        return contacts

    def generate_csv_filename(self, path_parts: List[str]) -> str:
        """Generate CSV filename based on directory structure."""
        date_str = datetime.now().strftime("%Y%m%d")
        
        if len(path_parts) >= 2:
            # For structure like education/adult_education -> edu_adults_contacts_DATE.csv
            main_category = path_parts[0][:3]  # First 3 chars of main category
            sub_category = path_parts[1].replace('_', '').replace('-', '')
            
            # Simplify subcategory name
            if 'adult' in sub_category.lower():
                sub_short = 'adults'
            elif 'child' in sub_category.lower():
                sub_short = 'children'
            else:
                sub_short = sub_category[:6]  # First 6 chars
                
            filename = f"{main_category}_{sub_short}_contacts_{date_str}.csv"
        else:
            # Fallback for single directory
            category = path_parts[0] if path_parts else 'general'
            filename = f"{category}_contacts_{date_str}.csv"
        
        return filename

    def save_to_csv(self, contacts: List[Dict[str, str]], output_path: Path):
        """Save contacts to CSV file."""
        if not contacts:
            logger.warning("No contacts to save")
            return
        
        # Ensure output directory exists
        output_path.parent.mkdir(parents=True, exist_ok=True)
        
        fieldnames = [
            'source_file', 'name', 'title', 'organization', 'department',
            'email', 'phone', 'website', 'address', 'notes'
        ]
        
        try:
            with open(output_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(contacts)
            
            logger.info(f"Successfully saved {len(contacts)} contacts to {output_path}")
            
            # Print sample of what was saved
            print(f"\n📊 Sample from {output_path.name}:")
            print("-" * 50)
            for i, contact in enumerate(contacts[:3]):  # Show first 3 contacts
                print(f"Contact {i+1}:")
                print(f"  Name: {contact['name']}")
                print(f"  Email: {contact['email']}")
                print(f"  Organization: {contact['organization']}")
                print(f"  Title: {contact['title']}")
                if i < len(contacts) - 1:
                    print()
            
            if len(contacts) > 3:
                print(f"... and {len(contacts) - 3} more contacts")
            
        except Exception as e:
            logger.error(f"Error saving CSV to {output_path}: {e}")
            raise

def main():
    if len(sys.argv) < 3:
        print("Usage: python extract_contacts.py <source_directory> <output_directory>")
        print("Example: python extract_contacts.py contact_details contacts")
        sys.exit(1)
    
    source_dir = Path(sys.argv[1])
    output_dir = Path(sys.argv[2])
    
    if not source_dir.exists():
        logger.error(f"Source directory {source_dir} does not exist")
        sys.exit(1)
    
    extractor = ContactExtractor()
    
    # Find all .txt files recursively
    txt_files = list(source_dir.rglob("*.txt"))
    
    if not txt_files:
        logger.warning(f"No .txt files found in {source_dir}")
        # Create a sample file structure
        sample_dir = source_dir / "education" / "adult_education"
        sample_dir.mkdir(parents=True, exist_ok=True)
        sample_file = sample_dir / "sample-contacts.txt"
        
        with open(sample_file, 'w') as f:
            f.write("""Professor Rachel Hilliam
Head of School
School of Mathematics & Statistics
The Open University
📧 rachel.hilliam@open.ac.uk
📞 +44 1908 274066

Dr. Sarah Johnson
Senior Lecturer
Department of Computer Science
Birkbeck College
📧 s.johnson@bbk.ac.uk
📞 +44 20 7631 6000
""")
        
        logger.info(f"Created sample file: {sample_file}")
        txt_files = [sample_file]
    
    logger.info(f"Found {len(txt_files)} .txt files to process")
    
    # Group files by their directory structure
    grouped_files = {}
    for txt_file in txt_files:
        # Get relative path from source directory
        rel_path = txt_file.relative_to(source_dir)
        path_parts = rel_path.parts[:-1]  # Exclude filename
        
        key = tuple(path_parts) if path_parts else ('general',)
        if key not in grouped_files:
            grouped_files[key] = []
        grouped_files[key].append(txt_file)
    
    logger.info(f"Processing {len(grouped_files)} directory groups")
    
    total_contacts = 0
    
    for path_parts, files in grouped_files.items():
        logger.info(f"Processing directory: {' / '.join(path_parts)}")
        
        all_contacts = []
        for file_path in files:
            logger.info(f"  Processing file: {file_path.name}")
            contacts = extractor.process_text_file(file_path)
            all_contacts.extend(contacts)
        
        if all_contacts:
            csv_filename = extractor.generate_csv_filename(list(path_parts))
            csv_path = output_dir / csv_filename
            
            extractor.save_to_csv(all_contacts, csv_path)
            total_contacts += len(all_contacts)
        else:
            logger.warning(f"No contacts found in directory: {' / '.join(path_parts)}")
    
    print(f"\n🎉 Extraction completed!")
    print(f"📊 Total contacts extracted: {total_contacts}")
    print(f"📁 Output directory: {output_dir}")
    
    # List generated CSV files
    csv_files = list(output_dir.glob("*.csv"))
    if csv_files:
        print(f"📄 Generated CSV files:")
        for csv_file in csv_files:
            file_size = csv_file.stat().st_size
            print(f"  - {csv_file.name} ({file_size} bytes)")

if __name__ == "__main__":
    main()
