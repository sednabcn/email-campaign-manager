# utils/data_loader.py
def load_contacts_directory(directory):
    """Load contacts from all files in a directory"""
    import os
    import pandas as pd
    from pathlib import Path
    
    contacts = []
    directory = Path(directory)
    
    if not directory.exists():
        print(f"Directory not found: {directory}")
        return []
    
    # Load CSV files
    for csv_file in directory.glob('*.csv'):
        try:
            df = pd.read_csv(csv_file)
            for _, row in df.iterrows():
                contact = row.to_dict()
                contact['source'] = csv_file.name
                contacts.append(contact)
        except Exception as e:
            print(f"Error loading {csv_file}: {e}")
    
    # Load Excel files
    for excel_file in list(directory.glob('*.xlsx')) + list(directory.glob('*.xls')):
        try:
            df = pd.read_excel(excel_file)
            for _, row in df.iterrows():
                contact = row.to_dict()
                contact['source'] = excel_file.name
                contacts.append(contact)
        except Exception as e:
            print(f"Error loading {excel_file}: {e}")
    
    return contacts

def validate_contact_data(contacts):
    """Validate contact data and return stats"""
    stats = {
        'total': len(contacts),
        'valid_emails': 0,
        'missing_email': 0,
        'missing_name': 0,
        'valid': 0
    }
    
    valid_contacts = []
    
    for contact in contacts:
        email = str(contact.get('email', '')).strip()
        name = str(contact.get('name', '')).strip()
        
        if not email or '@' not in email:
            stats['missing_email'] += 1
            continue
            
        if not name:
            stats['missing_name'] += 1
            # Use email prefix as fallback name
            contact['name'] = email.split('@')[0]
        
        stats['valid_emails'] += 1
        stats['valid'] += 1
        valid_contacts.append(contact)
    
    return stats, valid_contacts
   
def validate_contact_data(contacts):
    """Validate and clean contact data with improved error handling"""
    import pandas as pd
    
    stats = {
        'total': len(contacts),
        'valid': 0,
        'missing_names': 0,
        'missing_emails': 0,
        'missing_phones': 0,
        'valid_emails': 0,
        'invalid_emails': [],
        'unique_domains': 0
    }
   
    if not contacts:
        print("⚠️  WARNING: No contacts provided to validate_contact_data()")
        return stats, []
    
    valid_contacts = []
    email_domains = set()
    
    for idx, contact in enumerate(contacts):
        try:
            # Ensure contact is a dict
            if not isinstance(contact, dict):
                print(f"⚠️  Skipping non-dict contact at index {idx}: {type(contact)}")
                continue
            
            # Handle NaN/float values safely
            name = contact.get('name', '')
            if pd.isna(name) or not isinstance(name, str):
                name = ''
            else:
                name = str(name).strip()
                
            email = contact.get('email', '')
            if pd.isna(email) or not isinstance(email, str):
                email = ''
            else:
                email = str(email).strip()
                
            phone = contact.get('phone', '')
            if pd.isna(phone):
                phone = ''
            else:
                phone = str(phone).strip()
            
            # Update contact with cleaned values
            contact['name'] = name
            contact['email'] = email
            contact['phone'] = phone
            
            # Validate email format
            if email:
                if '@' in email and '.' in email.split('@')[-1]:
                    stats['valid_emails'] += 1
                    domain = email.split('@')[-1].lower()
                    email_domains.add(domain)
                else:
                    stats['invalid_emails'].append(email)
            
            # Track statistics
            if not name:
                stats['missing_names'] += 1
            if not email:
                stats['missing_emails'] += 1
            if not phone:
                stats['missing_phones'] += 1
                
            # A contact is valid if it has at least a name AND email
            if name and email:
                stats['valid'] += 1
                valid_contacts.append(contact)
            elif email:
                # Allow contacts with just email
                stats['valid'] += 1
                contact['name'] = email.split('@')[0]  # Use email prefix as name
                valid_contacts.append(contact)
                
        except Exception as e:
            print(f"⚠️  Error processing contact at index {idx}: {e}")
            print(f"   Contact data: {contact}")
            continue
    
    stats['unique_domains'] = len(email_domains)
    
    print(f"\n=== VALIDATION SUMMARY ===")
    print(f"Total contacts: {stats['total']}")
    print(f"Valid contacts: {stats['valid']}")
    print(f"Valid emails: {stats['valid_emails']}")
    print(f"Missing emails: {stats['missing_emails']}")
    print(f"Missing names: {stats['missing_names']}")
    print(f"Unique domains: {stats['unique_domains']}")
    if stats['invalid_emails']:
        print(f"Invalid emails (first 5): {stats['invalid_emails'][:5]}")
    
    return stats, valid_contacts
