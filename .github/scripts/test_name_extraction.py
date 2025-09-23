#!/usr/bin/env python3
"""
Quick test script to debug name extraction from your contact files
"""

import re
from pathlib import Path

class NameExtractor:
    def looks_like_name(self, text):
        """Check if text looks like it could be a person's name"""
        if not text or len(text.strip()) < 3:
            return False
        
        text = text.strip()
        
        # Skip if contains obvious non-name indicators
        skip_indicators = [
            '@', 'http', 'www', '.com', '.org', '.edu', '.ac.uk',
            'phone', 'tel', 'mobile', 'email', 'address',
            'street', 'road', 'avenue', 'building', 'room',
            'department', 'school', 'university', 'college'
        ]
        
        if any(indicator in text.lower() for indicator in skip_indicators):
            return False
        
        # Skip if mostly numbers
        if sum(c.isdigit() for c in text) > len(text) // 2:
            return False
        
        # Skip if too many special characters
        special_chars = sum(1 for c in text if not (c.isalnum() or c.isspace() or c in ".,'-"))
        if special_chars > len(text) // 3:
            return False
        
        # Should have at least some letters
        if sum(c.isalpha() for c in text) < len(text) // 2:
            return False
        
        return True

    def is_valid_name(self, name):
        """Validate if extracted text is a reasonable name"""
        if not name or len(name.strip()) < 3:
            return False
        
        name = name.strip()
        words = name.split()
        
        # Should have 2-5 words
        if not (2 <= len(words) <= 5):
            return False
        
        # Each word should be reasonable length
        if any(len(word) < 1 or len(word) > 20 for word in words):
            return False
        
        # Should not contain obvious non-name patterns
        invalid_patterns = [
            r'\d{3,}',  # 3+ consecutive digits
            r'[@#$%^&*()+=\[\]{}|\\:";\'<>?/]',  # Special characters
            r'(?i)\b(?:department|school|university|college|email|phone|address)\b'
        ]
        
        for pattern in invalid_patterns:
            if re.search(pattern, name):
                return False
        
        # At least one word should start with capital letter
        if not any(word[0].isupper() for word in words if word):
            return False
        
        return True

    def extract_name_debug(self, text, filename):
        """Extract name with debug output"""
        print(f"\n{'='*50}")
        print(f"DEBUGGING: {filename}")
        print(f"{'='*50}")
        
        lines = text.split('\n')
        clean_lines = [line.strip() for line in lines if line.strip()]
        
        print(f"File has {len(clean_lines)} non-empty lines")
        print("First 10 lines:")
        for i, line in enumerate(clean_lines[:10]):
            print(f"  {i+1}: {repr(line)}")
        
        # Test all patterns
        print(f"\nTesting extraction patterns...")
        
        # Pattern 1: Name labels
        name_label_patterns = [
            r'(?i)name\s*[:=]\s*(.+?)(?:\n|$)',
            r'(?i)full\s*name\s*[:=]\s*(.+?)(?:\n|$)',
            r'(?i)contact\s*name\s*[:=]\s*(.+?)(?:\n|$)',
        ]
        
        for i, pattern in enumerate(name_label_patterns):
            for line in clean_lines:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1).strip()
                    valid = self.is_valid_name(name)
                    print(f"  Pattern 1.{i+1}: Found '{name}' (valid: {valid})")
                    if valid:
                        return name
        
        # Pattern 2: Academic titles
        title_patterns = [
            r'(?i)^((?:prof(?:essor)?|dr)\.\s+[a-z]+(?:\s+[a-z]+)+)',
            r'(?i)^(professor\s+[a-z]+(?:\s+[a-z]+)+)',
            r'(?i)^(dr\s+[a-z]+(?:\s+[a-z]+)+)',
        ]
        
        for i, pattern in enumerate(title_patterns):
            for line in clean_lines[:5]:
                match = re.search(pattern, line)
                if match:
                    name = match.group(1).strip()
                    valid = self.is_valid_name(name)
                    print(f"  Pattern 2.{i+1}: Found '{name}' (valid: {valid})")
                    if valid:
                        return name
        
        # Pattern 3: Names before positions
        position_patterns = [
            r'(?i)^([a-z\s\.]+?)(?:\s*[-,]\s*)?(?:head\s+of|professor|lecturer|director|manager)',
        ]
        
        full_text = '\n'.join(clean_lines[:10])
        for i, pattern in enumerate(position_patterns):
            match = re.search(pattern, full_text, re.MULTILINE)
            if match:
                name = match.group(1).strip()
                valid = self.is_valid_name(name)
                print(f"  Pattern 3.{i+1}: Found '{name}' (valid: {valid})")
                if valid:
                    return name
        
        # Pattern 4: Name candidates (capitalised words)
        print(f"  Looking for name candidates...")
        name_candidates = []
        for line in clean_lines[:8]:
            if any(indicator in line.lower() for indicator in ['@', 'phone', 'tel', 'address', 'street']):
                continue
                
            words = line.split()
            if 2 <= len(words) <= 4:
                if all(len(word) > 1 and word[0].isupper() and word[1:].islower() for word in words):
                    name_candidates.append(line.strip())
                    print(f"    Candidate: '{line.strip()}'")
        
        for candidate in name_candidates:
            if self.is_valid_name(candidate):
                print(f"  Pattern 4: Selected '{candidate}' (valid)")
                return candidate
        
        # Pattern 5: Fallback
        for line in clean_lines[:3]:
            if self.looks_like_name(line) and len(line.split()) >= 2:
                print(f"  Pattern 5 (fallback): '{line.strip()}'")
                return line.strip()
        
        print("  No valid name found")
        return ""

def main():
    extractor = NameExtractor()
    
    # Test on your specific files
    contact_files = [
        "Birbeck-contacts.txt",
        "open-univ-contacts.txt", 
        "St.George's=Univ-contacts.txt"
    ]
    
    for filename in contact_files:
        filepath = Path(filename)
        if filepath.exists():
            try:
                with open(filepath, 'r', encoding='utf-8', errors='ignore') as f:
                    content = f.read()
                
                extracted_name = extractor.extract_name_debug(content, filename)
                print(f"\nFINAL RESULT for {filename}: '{extracted_name}'")
                
            except Exception as e:
                print(f"Error reading {filename}: {e}")
        else:
            print(f"File not found: {filename}")
    
    print(f"\n{'='*50}")
    print("DEBUGGING COMPLETE")
    print(f"{'='*50}")

if __name__ == "__main__":
    main()
