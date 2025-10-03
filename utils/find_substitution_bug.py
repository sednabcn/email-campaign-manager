#!/usr/bin/env python3
"""
Find the template substitution bug in docx_parser.py
"""

import re
from pathlib import Path

def find_substitution_code(file_path):
    """Find and display the substitution logic"""
    print(f"\n{'='*70}")
    print(f"SEARCHING FOR SUBSTITUTION CODE IN: {file_path}")
    print(f"{'='*70}\n")
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        # Search for common substitution patterns
        patterns_to_find = [
            (r'\.replace\(', 'String replace operations'),
            (r'contact_mapping', 'Contact mapping usage'),
            (r'for.*mapping', 'Mapping iteration'),
            (r'personalize|substitute', 'Personalization functions'),
            (r'def.*process.*template', 'Template processing functions'),
        ]
        
        findings = {}
        
        for pattern, description in patterns_to_find:
            findings[description] = []
            for i, line in enumerate(lines, 1):
                if re.search(pattern, line, re.IGNORECASE):
                    findings[description].append((i, line.rstrip()))
        
        # Display findings
        for description, matches in findings.items():
            if matches:
                print(f"🔍 {description}:")
                for line_num, line in matches[:5]:  # Show first 5 matches
                    print(f"   Line {line_num}: {line[:100]}")
                if len(matches) > 5:
                    print(f"   ... and {len(matches) - 5} more matches")
                print()
        
        # Find the main template processing section
        print(f"{'='*70}")
        print("LOOKING FOR TEMPLATE PROCESSING LOGIC")
        print(f"{'='*70}\n")
        
        in_template_section = False
        section_lines = []
        section_start = 0
        
        for i, line in enumerate(lines, 1):
            # Look for function that processes templates
            if re.search(r'def.*process.*campaign|def.*send.*campaign|def.*personalize', line, re.IGNORECASE):
                in_template_section = True
                section_start = i
                section_lines = []
            
            if in_template_section:
                section_lines.append((i, line.rstrip()))
                
                # Stop at next function or after 50 lines
                if len(section_lines) > 1 and (re.match(r'^def ', line) or len(section_lines) > 50):
                    print(f"📋 Function starting at line {section_start}:")
                    for ln, l in section_lines[:30]:
                        print(f"   {ln:4d}: {l}")
                    if len(section_lines) > 30:
                        print(f"   ... (showing first 30 of {len(section_lines)} lines)")
                    print()
                    in_template_section = False
                    section_lines = []
        
        # Look for where contact_mapping is used
        print(f"{'='*70}")
        print("CONTACT_MAPPING USAGE ANALYSIS")
        print(f"{'='*70}\n")
        
        for i, line in enumerate(lines, 1):
            if 'contact_mapping' in line.lower() and not line.strip().startswith('#'):
                # Show context (3 lines before and after)
                start = max(0, i-4)
                end = min(len(lines), i+3)
                print(f"📍 Context around line {i}:")
                for j in range(start, end):
                    marker = ">>> " if j == i-1 else "    "
                    print(f"   {marker}{j+1:4d}: {lines[j].rstrip()}")
                print()
        
        return True
        
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def suggest_fix():
    """Suggest the correct substitution code"""
    print(f"\n{'='*70}")
    print("CORRECT SUBSTITUTION CODE SHOULD LOOK LIKE:")
    print(f"{'='*70}\n")
    
    print("""
# When processing each contact:
for contact in contacts:
    # Get the template content (from DOCX)
    content = get_template_content(template_path)
    
    # Iterate through the contact_mapping
    for template_placeholder, csv_field in contact_mapping.items():
        # Get the value from the contact data
        value = contact.get(csv_field, '')
        
        # Replace [Template Placeholder] with actual value
        content = content.replace(f'[{template_placeholder}]', str(value))
    
    # Now content should have all placeholders replaced
    send_email(contact['email'], subject, content)

# Example with your data:
# contact_mapping = {
#     "Recipient Name": "name",
#     "Title / Position": "position"
# }
# contact = {
#     "name": "Shabnam Beheshti",
#     "position": "School of Science & Technology"
# }
#
# The code should do:
# content.replace('[Recipient Name]', 'Shabnam Beheshti')
# content.replace('[Title / Position]', 'School of Science & Technology')
""")

if __name__ == "__main__":
    parser_file = "utils/docx_parser.py"
    
    print("\n" + "="*70)
    print("TEMPLATE SUBSTITUTION BUG FINDER")
    print("="*70)
    
    if Path(parser_file).exists():
        found = find_substitution_code(parser_file)
        if found:
            suggest_fix()
    else:
        print(f"\n❌ File not found: {parser_file}")
        print("Please run this script from the project root directory")
    
    print("\n" + "="*70)
    print("ANALYSIS COMPLETE")
    print("="*70)
    print("\n💡 TIP: Look for where the code processes 'contact_mapping'")
    print("         and verify it's using the KEYS (template placeholders)")
    print("         not the VALUES (CSV fields) for substitution")
