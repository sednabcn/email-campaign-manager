def extract_name(self, text):
    """Extract person's name - improved for academic format"""
    lines = text.split('\n')
    clean_lines = [line.strip() for line in lines if line.strip()]
    
    if not clean_lines:
        return ""
    
    first_line = clean_lines[0]
    
    # Pattern 1: Professor [Name] or Dr [Name]
    title_patterns = [
        r'^Professor\s+(.+?)(?:\s*$)',
        r'^Dr\.?\s+(.+?)(?:\s*$)'
    ]
    
    for pattern in title_patterns:
        match = re.search(pattern, first_line)
        if match:
            name = match.group(1).strip()
            # Validate it's a proper name (2-4 words, capitalized)
            words = name.split()
            if 2 <= len(words) <= 4 and all(w[0].isupper() for w in words if w):
                return name
    
    # Pattern 2: Just the name without title
    # Remove title and extract name
    name = re.sub(r'^(?:Professor|Dr\.?|Mr\.?|Ms\.?|Mrs\.?)\s+', '', first_line)
    name = name.strip()
    
    # Validate name
    words = name.split()
    if 2 <= len(words) <= 4:
        if all(w[0].isupper() for w in words if w):
            if not any(indicator in name.lower() for indicator in 
                      ['school', 'head of', '@', 'university', 'department']):
                return name
    
    return ""
