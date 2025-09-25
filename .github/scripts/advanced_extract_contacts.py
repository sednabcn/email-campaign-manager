#!/usr/bin/env python3
"""
Advanced Universal Contact Extraction System
Enterprise-grade contact extraction with advanced features:
- Multi-language support
- Fuzzy matching & deduplication
- Quality scoring & validation
- CRM export formats
- Regional adaptations
- Corporate hierarchy detection
"""

import os
import sys
import csv
import re
import json
import unicodedata
from datetime import datetime
from pathlib import Path
from collections import defaultdict, Counter
from difflib import SequenceMatcher
import hashlib

# Configuration
class ContactConfig:
    """Configuration for contact extraction"""
    
    # Regional settings
    REGION = 'UK'  # UK, US, EU, INTERNATIONAL
    
    # Quality thresholds
    MIN_QUALITY_SCORE = 30
    HIGH_QUALITY_THRESHOLD = 80
    
    # Fuzzy matching thresholds
    NAME_SIMILARITY_THRESHOLD = 0.85
    EMAIL_DOMAIN_SIMILARITY = 0.9
    
    # Export formats
    EXPORT_FORMATS = ['csv', 'vcard', 'json', 'salesforce', 'hubspot']
    
    # Custom sector definitions
    CUSTOM_SECTORS = {
        'Academic': [
            'university', 'college', 'school', 'professor', 'lecturer', 'research', 
            'academic', 'dean', 'faculty', 'phd', 'doctorate', 'campus'
        ],
        'Healthcare': [
            'hospital', 'clinic', 'medical', 'doctor', 'nurse', 'physician', 'health', 
            'nhs', 'surgery', 'practice', 'consultant', 'specialist', 'ward', 'patient'
        ],
        'Finance': [
            'bank', 'financial', 'insurance', 'investment', 'trading', 'analyst', 'fund',
            'wealth', 'portfolio', 'credit', 'loan', 'mortgage', 'equity', 'asset'
        ],
        'Technology': [
            'software', 'developer', 'engineer', 'tech', 'digital', 'it', 'programming',
            'coding', 'data', 'cloud', 'ai', 'machine learning', 'blockchain', 'cybersecurity'
        ],
        'Legal': [
            'law', 'legal', 'solicitor', 'barrister', 'lawyer', 'court', 'judicial',
            'litigation', 'contract', 'compliance', 'regulatory', 'chambers'
        ],
        'Government': [
            'government', 'ministry', 'department', 'public', 'civil service', 'council',
            'municipal', 'federal', 'state', 'local authority', 'parliament', 'senate'
        ],
        'Retail': [
            'retail', 'shop', 'store', 'sales', 'customer', 'merchandise', 'commerce',
            'shopping', 'outlet', 'franchise', 'chain', 'boutique'
        ],
        'Manufacturing': [
            'manufacturing', 'factory', 'production', 'industrial', 'plant', 'assembly',
            'operations', 'supply chain', 'logistics', 'warehouse'
        ],
        'Media': [
            'media', 'journalism', 'reporter', 'editor', 'broadcaster', 'news', 'publishing',
            'television', 'radio', 'press', 'communications', 'pr', 'marketing'
        ],
        'Consulting': [
            'consulting', 'consultant', 'advisory', 'strategy', 'management', 'professional services',
            'expertise', 'specialist', 'advisor', 'practice'
        ]
    }
    
    # Seniority levels
    SENIORITY_LEVELS = {
        'C-Level': ['ceo', 'cfo', 'cto', 'coo', 'cmo', 'chief', 'president', 'chairman', 'founder'],
        'Senior': ['director', 'vp', 'vice president', 'head of', 'senior', 'principal', 'lead'],
        'Management': ['manager', 'supervisor', 'team lead', 'coordinator', 'administrator'],
        'Professional': ['analyst', 'specialist', 'consultant', 'engineer', 'developer', 'designer'],
        'Associate': ['associate', 'assistant', 'junior', 'trainee', 'intern', 'entry']
    }
    
    # Regional phone patterns
    PHONE_PATTERNS = {
        'UK': [
            r'\+44\s?\(0\)\d{2,4}\s?\d{4}\s?\d{4}',
            r'\+44\s?\d{2,4}\s?\d{4}\s?\d{4}',
            r'0\d{2,4}\s?\d{4}\s?\d{4}',
            r'\(\d{3,4}\)\s?\d{3,4}\s?\d{4}'
        ],
        'US': [
            r'\+1[-.\s]?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\(\d{3}\)[-.\s]?\d{3}[-.\s]?\d{4}',
            r'\d{3}[-.\s]\d{3}[-.\s]\d{4}'
        ],
        'EU': [
            r'\+\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}',
            r'00\d{1,3}[-.\s]?\d{1,4}[-.\s]?\d{1,4}[-.\s]?\d{1,9}'
        ]
    }
    
    # Placeholder email patterns
    PLACEHOLDER_EMAILS = [
        'alerts@modelphysmat.com',
        'info@company.com',
        'contact@example.com',
        'noreply@',
        'admin@',
        'support@',
        'info@',
        'hello@',
        'mail@',
        'office@'
    ]

class ContactQualityAnalyzer:
    """Analyze and score contact quality"""
    
    @staticmethod
    def calculate_quality_score(contact):
        """Calculate contact quality score (0-100)"""
        score = 0
        
        # Name quality (25 points)
        if contact.get('name') and contact['name'] != "Unknown Contact":
            name_words = len(contact['name'].split())
            if name_words >= 2:
                score += 25
            elif name_words == 1:
                score += 15
        
        # Email quality (30 points)
        email = contact.get('email', '')
        if email:
            if '[PLACEHOLDER]' not in email:
                score += 30
            elif any(placeholder in email.lower() for placeholder in ContactConfig.PLACEHOLDER_EMAILS):
                score += 10
            else:
                score += 20
        
        # Phone quality (20 points)
        if contact.get('phone'):
            phone = re.sub(r'[^\d+]', '', contact['phone'])
            if len(phone) >= 10:
                score += 20
            elif len(phone) >= 7:
                score += 10
        
        # Position quality (15 points)
        if contact.get('position'):
            score += 15
        
        # Organization quality (10 points)
        if contact.get('organization') and contact['organization'] != "Unknown Organization":
            score += 10
        
        return min(score, 100)
    
    @staticmethod
    def validate_email(email):
        """Validate email address"""
        if not email or '[PLACEHOLDER]' in email:
            return False, "Placeholder or missing email"
        
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return False, "Invalid email format"
        
        # Check for suspicious patterns
        suspicious_patterns = ['test', 'example', 'dummy', 'fake']
        for pattern in suspicious_patterns:
            if pattern in email.lower():
                return False, f"Suspicious email ({pattern})"
        
        return True, "Valid email"
    
    @staticmethod
    def validate_phone(phone, region='UK'):
        """Validate phone number for specific region"""
        if not phone:
            return False, "Missing phone number"
        
        patterns = ContactConfig.PHONE_PATTERNS.get(region, ContactConfig.PHONE_PATTERNS['UK'])
        phone_clean = re.sub(r'\s+', ' ', phone.strip())
        
        for pattern in patterns:
            if re.match(pattern, phone_clean):
                return True, "Valid phone number"
        
        return False, f"Invalid phone format for {region}"

class FuzzyMatcher:
    """Advanced fuzzy matching for deduplication"""
    
    @staticmethod
    def similarity_ratio(str1, str2):
        """Calculate similarity ratio between two strings"""
        if not str1 or not str2:
            return 0.0
        
        str1 = str1.lower().strip()
        str2 = str2.lower().strip()
        
        return SequenceMatcher(None, str1, str2).ratio()
    
    @staticmethod
    def normalize_name(name):
        """Normalize name for comparison"""
        # Remove accents
        name = unicodedata.normalize('NFD', name)
        name = ''.join(char for char in name if unicodedata.category(char) != 'Mn')
        
        # Convert to lowercase, remove punctuation
        name = re.sub(r'[^\w\s]', '', name.lower())
        
        # Handle initials: "John A Smith" -> "john a smith"
        return ' '.join(name.split())
    
    @staticmethod
    def names_match(name1, name2, threshold=0.85):
        """Check if two names likely refer to the same person"""
        if not name1 or not name2:
            return False
        
        norm1 = FuzzyMatcher.normalize_name(name1)
        norm2 = FuzzyMatcher.normalize_name(name2)
        
        # Exact match
        if norm1 == norm2:
            return True
        
        # Similarity ratio
        if FuzzyMatcher.similarity_ratio(norm1, norm2) >= threshold:
            return True
        
        # Check if one is initials of the other
        words1 = norm1.split()
        words2 = norm2.split()
        
        # "john smith" vs "j smith" or "john s"
        if len(words1) == len(words2):
            matches = 0
            for w1, w2 in zip(words1, words2):
                if w1 == w2 or (len(w1) == 1 and w1 == w2[0]) or (len(w2) == 1 and w2 == w1[0]):
                    matches += 1
            if matches == len(words1):
                return True
        
        return False
    
    @staticmethod
    def emails_match(email1, email2):
        """Check if emails belong to same person"""
        if not email1 or not email2:
            return False
        
        # Remove placeholder indicators
        email1_clean = email1.replace(' [PLACEHOLDER]', '').lower()
        email2_clean = email2.replace(' [PLACEHOLDER]', '').lower()
        
        if email1_clean == email2_clean:
            return True
        
        # Same domain, similar local parts
        if '@' in email1_clean and '@' in email2_clean:
            local1, domain1 = email1_clean.split('@', 1)
            local2, domain2 = email2_clean.split('@', 1)
            
            if domain1 == domain2:
                # Similar local parts: john.smith vs j.smith
                if FuzzyMatcher.similarity_ratio(local1, local2) >= 0.8:
                    return True
        
        return False

class AdvancedContactExtractor:
    """Advanced contact extraction with enterprise features"""
    
    def __init__(self, config=None):
        self.config = config or ContactConfig()
        self.quality_analyzer = ContactQualityAnalyzer()
        self.fuzzy_matcher = FuzzyMatcher()
        self.extracted_contacts = []
        self.statistics = defaultdict(int)
    
    def extract_name_advanced(self, text):
        """Advanced name extraction with multi-language support"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        if not lines:
            return ""
        
        # Try different name extraction strategies
        strategies = [
            self._extract_title_name,
            self._extract_business_card_name,
            self._extract_signature_name,
            self._extract_standard_name
        ]
        
        for strategy in strategies:
            name = strategy(lines)
            if name:
                return name
        
        return ""
    
    def _extract_title_name(self, lines):
        """Extract name with professional titles"""
        title_patterns = [
            r'^(?:Professor|Prof\.?|Dr\.?|Doctor|Mr\.?|Ms\.?|Mrs\.?|Miss|Sir|Dame)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
            r'^(?:CEO|CTO|CFO|COO|Director|Manager|Head|Lead|Chief|President|VP|Vice President)\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})',
        ]
        
        for line in lines[:3]:
            for pattern in title_patterns:
                match = re.search(pattern, line, re.IGNORECASE)
                if match:
                    return match.group(1).strip()
        
        return ""
    
    def _extract_business_card_name(self, lines):
        """Extract name from business card format: Name, Title"""
        for line in lines[:3]:
            # "John Smith, Director of Operations"
            if ',' in line:
                parts = line.split(',', 1)
                name_part = parts[0].strip()
                if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?$', name_part):
                    return name_part
        
        return ""
    
    def _extract_signature_name(self, lines):
        """Extract name from email signature format"""
        for line in lines:
            # Look for lines that start with name pattern
            if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+', line):
                # Extract just the name part
                name_match = re.match(r'^([A-Z][a-z]+(?:\s+[A-Z][a-z]+){1,3})', line)
                if name_match:
                    return name_match.group(1)
        
        return ""
    
    def _extract_standard_name(self, lines):
        """Extract standard capitalized name"""
        for line in lines[:5]:
            # Skip lines with obvious non-name content
            if any(skip in line.lower() for skip in 
                   ['email:', 'phone:', 'tel:', 'address:', 'www.', 'http', '@']):
                continue
            
            # Standard name pattern
            if re.match(r'^[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?$', line.strip()):
                return line.strip()
        
        return ""
    
    def detect_seniority_level(self, position):
        """Detect seniority level from position"""
        if not position:
            return "Unknown"
        
        position_lower = position.lower()
        
        for level, indicators in self.config.SENIORITY_LEVELS.items():
            if any(indicator in position_lower for indicator in indicators):
                return level
        
        return "Professional"
    
    def detect_sector_advanced(self, text, filename):
        """Advanced sector detection with scoring"""
        text_lower = text.lower()
        filename_lower = filename.lower()
        combined_text = f"{text_lower} {filename_lower}"
        
        sector_scores = {}
        
        for sector, keywords in self.config.CUSTOM_SECTORS.items():
            score = 0
            for keyword in keywords:
                # Weight longer keywords higher
                keyword_weight = max(1, len(keyword.split()))
                score += combined_text.count(keyword) * keyword_weight
            
            if score > 0:
                sector_scores[sector] = score
        
        if sector_scores:
            return max(sector_scores, key=sector_scores.get)
        
        return "General"
    
    def extract_company_info(self, text, filename):
        """Extract detailed company/organization information"""
        lines = [line.strip() for line in text.split('\n') if line.strip()]
        
        # Look for organization patterns
        org_patterns = [
            r'((?:[A-Z][a-z]*\s*){1,5}(?:University|College|School|Institute))',
            r'((?:[A-Z][a-z]*\s*){1,5}(?:Hospital|Clinic|Medical Center))',
            r'((?:[A-Z][a-z]*\s*){1,5}(?:Company|Corporation|Corp|Ltd|LLC|Inc))',
            r'((?:[A-Z][a-z]*\s*){1,5}(?:Bank|Financial|Insurance))',
            r'((?:[A-Z][a-z]*\s*){1,5}(?:Department|Ministry|Council))',
        ]
        
        for line in lines:
            if '@' in line or 'phone' in line.lower() or 'tel' in line.lower():
                continue
            
            for pattern in org_patterns:
                match = re.search(pattern, line)
                if match:
                    return match.group(1).strip()
        
        # Fallback to filename mapping
        return self.get_organization_from_filename(filename)
    
    def get_organization_from_filename(self, filename):
        """Enhanced filename to organization mapping"""
        filename_lower = filename.lower().replace('.txt', '').replace('-contacts', '')
        
        # Extended organization mappings
        org_mappings = {
            'birbeck': 'Birkbeck, University of London',
            'open-univ': 'The Open University', 
            'st.george': "St George's, University of London",
            'cambridge': 'University of Cambridge',
            'oxford': 'University of Oxford',
            'imperial': 'Imperial College London',
            'lse': 'London School of Economics',
            'nhs': 'National Health Service (NHS)',
            'hsbc': 'HSBC Holdings',
            'barclays': 'Barclays Bank',
            'lloyds': 'Lloyds Banking Group',
            'goldman': 'Goldman Sachs',
            'jp-morgan': 'JPMorgan Chase',
            'microsoft': 'Microsoft Corporation',
            'google': 'Google Inc.',
            'amazon': 'Amazon.com Inc.',
            'apple': 'Apple Inc.',
            'facebook': 'Meta Platforms Inc.',
            'government': 'UK Government',
            'parliament': 'UK Parliament',
            'ministry': 'Government Ministry'
        }
        
        for key, org in org_mappings.items():
            if key in filename_lower:
                return org
        
        # Generic cleanup
        org = filename_lower.replace('=', ' ').replace('-', ' ').replace('_', ' ')
        org = ' '.join(word.capitalize() for word in org.split())
        
        return org if org else "Unknown Organization"
    
    def advanced_deduplication(self, contacts):
        """Advanced deduplication using fuzzy matching"""
        print(f"🔄 Advanced deduplication of {len(contacts)} contacts...")
        
        unique_contacts = []
        duplicate_groups = []
        processed_indices = set()
        
        for i, contact in enumerate(contacts):
            if i in processed_indices:
                continue
            
            # Find potential duplicates
            duplicates = [contact]
            duplicate_indices = {i}
            
            for j, other_contact in enumerate(contacts[i+1:], i+1):
                if j in processed_indices:
                    continue
                
                if self._contacts_are_duplicates(contact, other_contact):
                    duplicates.append(other_contact)
                    duplicate_indices.add(j)
            
            # Merge duplicate group
            if len(duplicates) > 1:
                merged_contact = self._merge_contacts(duplicates)
                duplicate_groups.append(duplicates)
                print(f"  🔗 Merged {len(duplicates)} duplicates: {merged_contact['name']}")
            else:
                merged_contact = contact
            
            unique_contacts.append(merged_contact)
            processed_indices.update(duplicate_indices)
        
        print(f"  ✨ Result: {len(unique_contacts)} unique contacts ({len(duplicate_groups)} groups merged)")
        return unique_contacts
    
    def _contacts_are_duplicates(self, contact1, contact2):
        """Check if two contacts are duplicates using multiple criteria"""
        # Name matching
        if self.fuzzy_matcher.names_match(
            contact1.get('name', ''), 
            contact2.get('name', ''), 
            threshold=ContactConfig.NAME_SIMILARITY_THRESHOLD
        ):
            return True
        
        # Email matching
        if self.fuzzy_matcher.emails_match(
            contact1.get('email', ''), 
            contact2.get('email', '')
        ):
            return True
        
        # Same organization + similar name
        if (contact1.get('organization', '').lower() == contact2.get('organization', '').lower() and
            self.fuzzy_matcher.similarity_ratio(
                contact1.get('name', ''), 
                contact2.get('name', '')
            ) >= 0.7):
            return True
        
        return False
    
    def _merge_contacts(self, duplicates):
        """Merge duplicate contacts, keeping the best information"""
        merged = duplicates[0].copy()
        
        # Score each contact and use the highest quality one as base
        best_contact = max(duplicates, key=self.quality_analyzer.calculate_quality_score)
        merged.update(best_contact)
        
        # Merge fields from all contacts (prefer non-empty, non-placeholder values)
        for contact in duplicates:
            for field in ['position', 'phone', 'address']:
                if not merged.get(field) and contact.get(field):
                    merged[field] = contact[field]
            
            # Prefer real email over placeholder
            if ('[PLACEHOLDER]' in merged.get('email', '') and 
                '[PLACEHOLDER]' not in contact.get('email', '')):
                merged['email'] = contact['email']
        
        # Combine raw data
        raw_data_parts = [c.get('raw_data', '') for c in duplicates if c.get('raw_data')]
        merged['raw_data'] = ' | '.join(raw_data_parts)[:500]
        
        return merged
    
    def generate_statistics(self, contacts):
        """Generate comprehensive statistics"""
        stats = {
            'total_contacts': len(contacts),
            'quality_distribution': defaultdict(int),
            'sector_breakdown': defaultdict(int),
            'seniority_breakdown': defaultdict(int),
            'email_analysis': defaultdict(int),
            'phone_analysis': defaultdict(int),
            'source_file_breakdown': defaultdict(int)
        }
        
        for contact in contacts:
            # Quality distribution
            score = self.quality_analyzer.calculate_quality_score(contact)
            if score >= ContactConfig.HIGH_QUALITY_THRESHOLD:
                stats['quality_distribution']['High (80-100)'] += 1
            elif score >= 50:
                stats['quality_distribution']['Medium (50-79)'] += 1
            else:
                stats['quality_distribution']['Low (0-49)'] += 1
            
            # Sector breakdown
            stats['sector_breakdown'][contact.get('sector', 'Unknown')] += 1
            
            # Seniority breakdown
            seniority = self.detect_seniority_level(contact.get('position', ''))
            stats['seniority_breakdown'][seniority] += 1
            
            # Email analysis
            email = contact.get('email', '')
            if '[PLACEHOLDER]' in email:
                stats['email_analysis']['Placeholder'] += 1
            elif email:
                stats['email_analysis']['Real'] += 1
            else:
                stats['email_analysis']['Missing'] += 1
            
            # Phone analysis
            if contact.get('phone'):
                stats['phone_analysis']['Present'] += 1
            else:
                stats['phone_analysis']['Missing'] += 1
            
            # Source file breakdown
            stats['source_file_breakdown'][contact.get('source_file', 'Unknown')] += 1
        
        return stats
    
    def export_contacts(self, contacts, output_path, formats=['csv']):
        """Export contacts in multiple formats"""
        output_path = Path(output_path)
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        exported_files = []
        
        for format_type in formats:
            if format_type == 'csv':
                file_path = self._export_csv(contacts, output_path, timestamp)
            elif format_type == 'vcard':
                file_path = self._export_vcard(contacts, output_path, timestamp)
            elif format_type == 'json':
                file_path = self._export_json(contacts, output_path, timestamp)
            elif format_type == 'salesforce':
                file_path = self._export_salesforce(contacts, output_path, timestamp)
            elif format_type == 'hubspot':
                file_path = self._export_hubspot(contacts, output_path, timestamp)
            else:
                continue
            
            exported_files.append((format_type, file_path))
        
        return exported_files
    
    def _export_csv(self, contacts, output_path, timestamp):
        """Export to CSV format"""
        csv_filename = f"contacts_advanced_{timestamp}.csv"
        csv_path = output_path / csv_filename
        
        fieldnames = [
            'name', 'position', 'email', 'phone', 'organization', 'address', 
            'sector', 'seniority_level', 'quality_score', 'email_valid', 
            'phone_valid', 'raw_data', 'source_file'
        ]
        
        with open(csv_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for contact in contacts:
                # Add computed fields
                contact['seniority_level'] = self.detect_seniority_level(contact.get('position', ''))
                contact['quality_score'] = self.quality_analyzer.calculate_quality_score(contact)
                contact['email_valid'] = self.quality_analyzer.validate_email(contact.get('email', ''))[0]
                contact['phone_valid'] = self.quality_analyzer.validate_phone(contact.get('phone', ''), ContactConfig.REGION)[0]
                
                writer.writerow(contact)
        
        return csv_path
    
    def _export_vcard(self, contacts, output_path, timestamp):
        """Export to VCard format"""
        vcard_filename = f"contacts_{timestamp}.vcf"
        vcard_path = output_path / vcard_filename
        
        with open(vcard_path, 'w', encoding='utf-8') as f:
            for contact in contacts:
                vcard = f"""BEGIN:VCARD
VERSION:3.0
FN:{contact.get('name', '')}
ORG:{contact.get('organization', '')}
TITLE:{contact.get('position', '')}
EMAIL:{contact.get('email', '').replace(' [PLACEHOLDER]', '')}
TEL:{contact.get('phone', '')}
ADR:;;{contact.get('address', '')};;;;
NOTE:{contact.get('sector', '')} - Quality Score: {self.quality_analyzer.calculate_quality_score(contact)}
END:VCARD

"""
                f.write(vcard)
        
        return vcard_path
    
    def _export_json(self, contacts, output_path, timestamp):
        """Export to JSON format"""
        json_filename = f"contacts_{timestamp}.json"
        json_path = output_path / json_filename
        
        # Add computed fields
        export_contacts = []
        for contact in contacts:
            export_contact = contact.copy()
            export_contact['seniority_level'] = self.detect_seniority_level(contact.get('position', ''))
            export_contact['quality_score'] = self.quality_analyzer.calculate_quality_score(contact)
            export_contact['email_validation'] = self.quality_analyzer.validate_email(contact.get('email', ''))
            export_contact['phone_validation'] = self.quality_analyzer.validate_phone(contact.get('phone', ''), ContactConfig.REGION)
            export_contacts.append(export_contact)
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump({
                'contacts': export_contacts,
                'metadata': {
                    'extraction_date': datetime.now().isoformat(),
                    'total_contacts': len(contacts),
                    'region': ContactConfig.REGION
                }
            }, f, indent=2, ensure_ascii=False)
        
        return json_path
    
    def _export_salesforce(self, contacts, output_path, timestamp):
        """Export in Salesforce-compatible CSV format"""
        sf_filename = f"contacts_salesforce_{timestamp}.csv"
        sf_path = output_path / sf_filename
        
        # Salesforce standard fields
        fieldnames = [
            'First Name', 'Last Name', 'Email', 'Phone', 'Title', 'Account Name',
            'Mailing Street', 'Mailing City', 'Mailing State', 'Mailing Country',
            'Description', 'Lead Source'
        ]
        
        with open(sf_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for contact in contacts:
                name_parts = contact.get('name', '').split()
                first_name = name_parts[0] if name_parts else ''
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                
                sf_contact = {
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Email': contact.get('email', '').replace(' [PLACEHOLDER]', ''),
                    'Phone': contact.get('phone', ''),
                    'Title': contact.get('position', ''),
                    'Account Name': contact.get('organization', ''),
                    'Mailing Street': contact.get('address', ''),
                    'Mailing City': '',
                    'Mailing State': '',
                    'Mailing Country': 'United Kingdom' if ContactConfig.REGION == 'UK' else '',
                    'Description': f"Sector: {contact.get('sector', '')} | Quality Score: {self.quality_analyzer.calculate_quality_score(contact)}",
                    'Lead Source': 'Contact Extraction'
                }
                
                writer.writerow(sf_contact)
        
        return sf_path
    
    def _export_hubspot(self, contacts, output_path, timestamp):
        """Export in HubSpot-compatible CSV format"""
        hs_filename = f"contacts_hubspot_{timestamp}.csv"
        hs_path = output_path / hs_filename
        
        # HubSpot standard properties
        fieldnames = [
            'First Name', 'Last Name', 'Email', 'Phone Number', 'Job Title', 'Company',
            'Address', 'City', 'State', 'Country', 'Industry', 'Lead Status',
            'Contact Source', 'Notes'
        ]
        
        with open(hs_path, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for contact in contacts:
                name_parts = contact.get('name', '').split()
                first_name = name_parts[0] if name_parts else ''
                last_name = ' '.join(name_parts[1:]) if len(name_parts) > 1 else ''
                
                hs_contact = {
                    'First Name': first_name,
                    'Last Name': last_name,
                    'Email': contact.get('email', '').replace(' [PLACEHOLDER]', ''),
                    'Phone Number': contact.get('phone', ''),
                    'Job Title': contact.get('position', ''),
                    'Company': contact.get('organization', ''),
                    'Address': contact.get('address', ''),
                    'City': '',
                    'State': '',
                    'Country': 'United Kingdom' if ContactConfig.REGION == 'UK' else '',
                    'Industry': contact.get('sector', ''),
                    'Lead Status': 'New',
                    'Contact Source': 'Automated Extraction',
                    'Notes': f"Quality Score: {self.quality_analyzer.calculate_quality_score(contact)} | Source: {contact.get('source_file', '')}"
                }
                
                writer.writerow(hs_contact)
        
        return hs_path

def main():
    """Main execution function with advanced features"""
    if len(sys.argv) < 3:
        print("""
🌟 Advanced Universal Contact Extraction System
Usage: python advanced_extract_contacts.py <source_directory> <output_directory> [options]

Options:
  --region UK|US|EU          Set regional format (default: UK)
  --quality-threshold N      Minimum quality score (default: 30)
  --export csv,vcard,json    Export formats (default: csv)
  --fuzzy-threshold 0.85     Name similarity threshold (default: 0.85)
  --verbose                  Verbose output

Examples:
  python advanced_extract_contacts.py contact_details contacts
  python advanced_extract_contacts.py contact_details contacts --export csv,vcard,json --verbose
  python advanced_extract_contacts.py contact_details contacts --region US --quality-threshold 50
        """)
        sys.exit(1)
    
    # Parse arguments
    source_dir = sys.argv[1]
    output_dir = sys.argv[2]
    
    # Parse optional arguments
    config = ContactConfig()
    export_formats = ['csv']
    verbose = False
    
    for i, arg in enumerate(sys.argv[3:], 3):
        if arg == '--region' and i + 1 < len(sys.argv):
            config.REGION = sys.argv[i + 1]
        elif arg == '--quality-threshold' and i + 1 < len(sys.argv):
            config.MIN_QUALITY_SCORE = int(sys.argv[i + 1])
        elif arg == '--export' and i + 1 < len(sys.argv):
            export_formats = sys.argv[i + 1].split(',')
        elif arg == '--fuzzy-threshold' and i + 1 < len(sys.argv):
            config.NAME_SIMILARITY_THRESHOLD = float(sys.argv[i + 1])
        elif arg == '--verbose':
            verbose = True
    
    # Initialize extractor
    extractor = AdvancedContactExtractor(config)
    
    print(f"🚀 Advanced Universal Contact Extraction System")
    print(f"📂 Source Directory: {source_dir}")
    print(f"📁 Output Directory: {output_dir}")
    print(f"🌍 Region: {config.REGION}")
    print(f"⭐ Min Quality Score: {config.MIN_QUALITY_SCORE}")
    print(f"📤 Export Formats: {', '.join(export_formats)}")
    print(f"🕒 Started: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 80)
    
    # Create output directory
    output_path = Path(output_dir)
    output_path.mkdir(parents=True, exist_ok=True)
    print(f"📁 Output directory ready: {output_path.absolute()}")
    
    # Find source files
    source_path = Path(source_dir)
    if not source_path.exists():
        print(f"❌ Source directory does not exist: {source_dir}")
        sys.exit(1)
    
    txt_files = list(source_path.rglob("*.txt"))
    if not txt_files:
        print(f"📭 No .txt files found in {source_dir}")
        sys.exit(1)
    
    print(f"📋 Found {len(txt_files)} text files:")
    total_size = 0
    for txt_file in sorted(txt_files):
        file_size = txt_file.stat().st_size
        total_size += file_size
        print(f"  📄 {txt_file.name} ({file_size:,} bytes)")
        if verbose:
            print(f"     📁 Path: {txt_file}")
    print(f"  📊 Total size: {total_size:,} bytes")
    print()
    
    # Extract contacts from all files
    all_contacts = []
    file_stats = {}
    
    for txt_file in sorted(txt_files):
        print(f"🔄 Processing: {txt_file.name}")
        file_contacts = extractor.extract_contacts_from_file(txt_file)
        all_contacts.extend(file_contacts)
        
        file_stats[txt_file.name] = {
            'contacts_found': len(file_contacts),
            'sectors': list(set(c.get('sector', 'Unknown') for c in file_contacts))
        }
        
        print(f"  ✅ Extracted {len(file_contacts)} contacts")
        if verbose:
            for contact in file_contacts:
                score = extractor.quality_analyzer.calculate_quality_score(contact)
                print(f"     👤 {contact['name']} ({contact['sector']}) - Quality: {score}")
                print(f"        📧 {contact['email']} | 📞 {contact['phone']}")
                print(f"        🏢 {contact['organization']}")
        print()
    
    if not all_contacts:
        print(f"❌ No contacts extracted from any files")
        sys.exit(1)
    
    print(f"📊 Extraction Phase Complete:")
    print(f"  📄 Files processed: {len(txt_files)}")
    print(f"  👥 Total contacts found: {len(all_contacts)}")
    print()
    
    # Advanced deduplication
    unique_contacts = extractor.advanced_deduplication(all_contacts)
    
    # Filter by quality threshold
    high_quality_contacts = []
    for contact in unique_contacts:
        score = extractor.quality_analyzer.calculate_quality_score(contact)
        if score >= config.MIN_QUALITY_SCORE:
            high_quality_contacts.append(contact)
    
    filtered_count = len(unique_contacts) - len(high_quality_contacts)
    if filtered_count > 0:
        print(f"🔍 Quality Filter: Removed {filtered_count} contacts below threshold ({config.MIN_QUALITY_SCORE})")
    
    final_contacts = high_quality_contacts
    print(f"✨ Final contact count: {len(final_contacts)}")
    print()
    
    # Generate comprehensive statistics
    stats = extractor.generate_statistics(final_contacts)
    
    # Export in requested formats
    print(f"💾 Exporting contacts...")
    exported_files = extractor.export_contacts(final_contacts, output_path, export_formats)
    
    for format_type, file_path in exported_files:
        file_size = file_path.stat().st_size
        print(f"  ✅ {format_type.upper()}: {file_path.name} ({file_size:,} bytes)")
    print()
    
    # Display comprehensive statistics
    print("📊 COMPREHENSIVE STATISTICS")
    print("=" * 50)
    
    print(f"📈 Overall Metrics:")
    print(f"  📄 Files processed: {stats['total_contacts']} contacts from {len(txt_files)} files")
    print(f"  🔄 Duplicates removed: {len(all_contacts) - len(unique_contacts)}")
    print(f"  🔍 Quality filtered: {filtered_count}")
    print(f"  ✅ Final contacts: {len(final_contacts)}")
    print()
    
    print(f"⭐ Quality Distribution:")
    for quality, count in stats['quality_distribution'].items():
        percentage = (count / len(final_contacts)) * 100
        print(f"  {quality}: {count} contacts ({percentage:.1f}%)")
    print()
    
    print(f"🏢 Sector Breakdown:")
    sorted_sectors = sorted(stats['sector_breakdown'].items(), key=lambda x: x[1], reverse=True)
    for sector, count in sorted_sectors:
        percentage = (count / len(final_contacts)) * 100
        print(f"  {sector}: {count} contacts ({percentage:.1f}%)")
    print()
    
    print(f"💼 Seniority Analysis:")
    sorted_seniority = sorted(stats['seniority_breakdown'].items(), key=lambda x: x[1], reverse=True)
    for level, count in sorted_seniority:
        percentage = (count / len(final_contacts)) * 100
        print(f"  {level}: {count} contacts ({percentage:.1f}%)")
    print()
    
    print(f"📧 Email Analysis:")
    for email_type, count in stats['email_analysis'].items():
        percentage = (count / len(final_contacts)) * 100
        print(f"  {email_type}: {count} contacts ({percentage:.1f}%)")
    print()
    
    print(f"📞 Phone Analysis:")
    for phone_type, count in stats['phone_analysis'].items():
        percentage = (count / len(final_contacts)) * 100
        print(f"  {phone_type}: {count} contacts ({percentage:.1f}%)")
    print()
    
    print(f"📂 Source File Analysis:")
    for source, count in sorted(stats['source_file_breakdown'].items()):
        percentage = (count / len(final_contacts)) * 100
        sectors = ', '.join(file_stats.get(source, {}).get('sectors', ['Unknown']))
        print(f"  📄 {source}: {count} contacts ({percentage:.1f}%) - Sectors: {sectors}")
    print()
    
    # Sample contacts preview
    print(f"👀 SAMPLE EXTRACTED CONTACTS")
    print("=" * 50)
    
    # Show top quality contacts
    sorted_by_quality = sorted(final_contacts, 
                             key=lambda c: extractor.quality_analyzer.calculate_quality_score(c), 
                             reverse=True)
    
    for i, contact in enumerate(sorted_by_quality[:5]):
        quality_score = extractor.quality_analyzer.calculate_quality_score(contact)
        seniority = extractor.detect_seniority_level(contact.get('position', ''))
        
        print(f"  📝 Contact {i+1} (Quality Score: {quality_score}):")
        print(f"    👤 Name: {contact.get('name', 'N/A')}")
        print(f"    💼 Position: {contact.get('position', 'N/A')} ({seniority})")
        print(f"    📧 Email: {contact.get('email', 'N/A')}")
        print(f"    📞 Phone: {contact.get('phone', 'N/A')}")
        print(f"    🏢 Organization: {contact.get('organization', 'N/A')}")
        print(f"    🏷️  Sector: {contact.get('sector', 'N/A')}")
        print(f"    📍 Address: {contact.get('address', 'N/A')[:60]}{'...' if len(contact.get('address', '')) > 60 else ''}")
        print(f"    📄 Source: {contact.get('source_file', 'N/A')}")
        
        # Validation results
        email_valid, email_msg = extractor.quality_analyzer.validate_email(contact.get('email', ''))
        phone_valid, phone_msg = extractor.quality_analyzer.validate_phone(contact.get('phone', ''), config.REGION)
        print(f"    ✅ Email Valid: {email_valid} ({email_msg})")
        print(f"    ✅ Phone Valid: {phone_valid} ({phone_msg})")
        print()
    
    # Export summary report
    report_path = output_path / f"extraction_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    with open(report_path, 'w', encoding='utf-8') as f:
        report_data = {
            'extraction_summary': {
                'timestamp': datetime.now().isoformat(),
                'source_directory': str(source_dir),
                'output_directory': str(output_dir),
                'configuration': {
                    'region': config.REGION,
                    'min_quality_score': config.MIN_QUALITY_SCORE,
                    'name_similarity_threshold': config.NAME_SIMILARITY_THRESHOLD,
                    'export_formats': export_formats
                },
                'processing_results': {
                    'files_processed': len(txt_files),
                    'total_contacts_found': len(all_contacts),
                    'duplicates_removed': len(all_contacts) - len(unique_contacts),
                    'quality_filtered': filtered_count,
                    'final_contacts': len(final_contacts)
                }
            },
            'statistics': dict(stats),
            'file_breakdown': file_stats,
            'exported_files': [{'format': fmt, 'filename': str(path.name), 'size_bytes': path.stat().st_size} 
                              for fmt, path in exported_files]
        }
        json.dump(report_data, f, indent=2, ensure_ascii=False)
    
    print(f"📋 Extraction Report: {report_path.name}")
    print()
    
    # Final success message
    print("🎉 EXTRACTION COMPLETED SUCCESSFULLY!")
    print("=" * 50)
    print(f"✅ Processed {len(txt_files)} files")
    print(f"✅ Extracted {len(final_contacts)} high-quality contacts")
    print(f"✅ Exported in {len(export_formats)} format(s)")
    print(f"✅ Generated comprehensive statistics")
    print(f"📁 All files saved to: {output_path}")
    
    # Performance summary
    end_time = datetime.now()
    # Calculate processing time (approximation since we don't track start time)
    print(f"🕒 Completed: {end_time.strftime('%Y-%m-%d %H:%M:%S')}")

def extract_contacts_from_file(self, file_path):
    """Extract contacts from any type of contact file using advanced parsing"""
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
        
        # Advanced content splitting
        contact_blocks = self._split_content_intelligently(content)
        print(f"     🔗 Split into {len(contact_blocks)} contact blocks")
        
        # Process each block
        for i, block in enumerate(contact_blocks):
            block = block.strip()
            if len(block) < 20:  # Skip very short blocks
                continue
            
            print(f"     🔍 Processing block {i+1}:")
            if len(block) > 100:
                print(f"       Preview: {block[:80].replace(chr(10), ' ')}...")
            else:
                print(f"       Content: {block.replace(chr(10), ' ')}")
            
            contact = self._parse_contact_block_advanced(block, filename)
            
            # Quality check with detailed scoring
            quality_score = self.quality_analyzer.calculate_quality_score(contact)
            
            if quality_score >= 20:  # Very low threshold for initial extraction
                contacts.append(contact)
                print(f"       ✅ Extracted: {contact['name']} ({contact['sector']}) - Score: {quality_score}")
                print(f"          📧 {contact['email']}")
                print(f"          📞 {contact['phone']}")
                print(f"          🏢 {contact['organization']}")
            else:
                print(f"       ❌ Skipped: quality score too low ({quality_score})")
    
    except Exception as e:
        print(f"     ❌ ERROR: {str(e)}")
    
    return contacts

def _split_content_intelligently(self, content):
    """Intelligently split content into contact blocks"""
    # Method 1: Split by clear separators
    separator_patterns = [
        r'^[-=*]{3,}
                    ,  # Lines with dashes, equals, asterisks
        r'^[_]{3,}
                    ,    # Underscores
        r'^#{3,}
                           # Hash symbols
    ]
    
    for pattern in separator_patterns:
        if re.search(pattern, content, re.MULTILINE):
            blocks = re.split(pattern, content, flags=re.MULTILINE)
            if len(blocks) > 1:
                return [b.strip() for b in blocks if b.strip()]
    
    # Method 2: Split by multiple blank lines
    if re.search(r'\n\s*\n\s*\n', content):
        blocks = re.split(r'\n\s*\n\s*\n+', content)
        if len(blocks) > 1:
            return [b.strip() for b in blocks if b.strip()]
    
    # Method 3: Split by email pattern occurrences
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    emails = list(re.finditer(email_pattern, content))
    
    if len(emails) > 1:
        blocks = []
        for i, email_match in enumerate(emails):
            # Find natural break points around emails
            start = 0 if i == 0 else self._find_block_start(content, email_match.start())
            end = len(content) if i == len(emails) - 1 else self._find_block_end(content, emails[i+1].start())
            
            block = content[start:end].strip()
            if len(block) > 20:
                blocks.append(block)
        
        if len(blocks) > 1:
            return blocks
    
    # Method 4: Split by repeated name patterns
    name_pattern = r'^[A-Z][a-z]+\s+[A-Z][a-z]+(?:\s+[A-Z][a-z]+)?
                    
    name_matches = list(re.finditer(name_pattern, content, re.MULTILINE))
    
    if len(name_matches) > 1:
        blocks = []
        for i, name_match in enumerate(name_matches):
            start = name_match.start()
            end = name_matches[i+1].start() if i < len(name_matches) - 1 else len(content)
            
            block = content[start:end].strip()
            if len(block) > 20:
                blocks.append(block)
        
        if len(blocks) > 1:
            return blocks
    
    # Fallback: return entire content as single block
    return [content.strip()]

def _find_block_start(self, content, position):
    """Find natural start position for a contact block"""
    # Look backwards for double newline
    search_start = max(0, position - 200)
    section = content[search_start:position]
    
    double_newline_matches = list(re.finditer(r'\n\s*\n', section))
    if double_newline_matches:
        last_match = double_newline_matches[-1]
        return search_start + last_match.end()
    
    return search_start

def _find_block_end(self, content, position):
    """Find natural end position for a contact block"""
    # Look forwards for double newline before next contact
    search_end = min(len(content), position)
    section = content[position-100:search_end]
    
    double_newline_match = re.search(r'\n\s*\n', section)
    if double_newline_match:
        return position - 100 + double_newline_match.start()
    
    return position

def _parse_contact_block_advanced(self, contact_text, source_filename):
    """Advanced parsing of a single contact block"""
    # Extract all components using advanced methods
    name = self.extract_name_advanced(contact_text)
    position = self._extract_position_advanced(contact_text)
    email = self._extract_email_advanced(contact_text)
    phone = self._extract_phone_advanced(contact_text)
    organization = self.extract_company_info(contact_text, source_filename)
    address = self._extract_address_advanced(contact_text)
    sector = self.detect_sector_advanced(contact_text, source_filename)
    
    # Clean and limit raw data
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

# Add these methods to the AdvancedContactExtractor class
AdvancedContactExtractor.extract_contacts_from_file = extract_contacts_from_file
AdvancedContactExtractor._split_content_intelligently = _split_content_intelligently
AdvancedContactExtractor._find_block_start = _find_block_start
AdvancedContactExtractor._find_block_end = _find_block_end
AdvancedContactExtractor._parse_contact_block_advanced = _parse_contact_block_advanced

if __name__ == "__main__":
    main()
