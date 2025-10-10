#!/bin/bash

echo "Applying critical fixes..."

# 1. Add missing functions to data_loader.py
cat >> utils/data_loader.py << 'EOF'

def load_contacts_directory(directory):
    """Load contacts from all files in a directory"""
    import os
    import pandas as pd
    from pathlib import Path
    
    contacts = []
    directory = Path(directory)
    
    if not directory.exists():
        return []
    
    for csv_file in directory.glob('*.csv'):
        try:
            df = pd.read_csv(csv_file)
            contacts.extend(df.to_dict('records'))
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
    
    return contacts

def validate_contact_data(contacts):
    """Validate contact data"""
    valid = [c for c in contacts if c.get('email') and '@' in str(c.get('email'))]
    return {
        'total': len(contacts),
        'valid_emails': len(valid),
        'valid': len(valid)
    }, valid
EOF

# 2. Ensure contacts directory exists
mkdir -p contacts scheduled-campaigns tracking

# 3. Create test data
cat > contacts/test_contacts.csv << 'EOF'
name,email,organization
John Doe,john.doe@example.com,Test Org
Jane Smith,jane.smith@test.org,Sample Inc
EOF

echo "Fixes applied. Commit and push changes."
