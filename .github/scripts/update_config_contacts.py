#!/usr/bin/env python3
"""
Update campaign config with latest matching contact file
"""
import json
import sys
from pathlib import Path

def update_config_contacts(config_file):
    """Update config with latest contact file"""
    print(f"Processing config: {config_file}")
    
    with open(config_file, 'r') as f:
        config = json.load(f)
    
    contacts_path = config.get('contacts', '')
    if not contacts_path:
        print("⚠️  No contacts path in config")
        return False
    
    print(f"Current contacts path: {contacts_path}")
    
    contact_dir = Path(contacts_path).parent
    contact_name = Path(contacts_path).stem
    
    # Extract pattern (remove timestamp if present)
    if '_2025' in contact_name or '_2024' in contact_name:
        # Format: name_YYYYMMDD_HHMMSS
        parts = contact_name.rsplit('_', 2)
        contact_pattern = parts[0]
    else:
        contact_pattern = contact_name
    
    print(f"Contact pattern: {contact_pattern}")
    print(f"Contact directory: {contact_dir}")
    
    # Find matching files
    if not contact_dir.exists():
        print(f"❌ Contact directory doesn't exist: {contact_dir}")
        return False
    
    similar_files = list(contact_dir.glob(f"{contact_pattern}*.csv"))
    
    if not similar_files:
        print(f"⚠️  No matching contact files found for pattern: {contact_pattern}*.csv")
        print(f"Available files in {contact_dir}:")
        for f in contact_dir.glob("*.csv"):
            print(f"  - {f.name}")
        return False
    
    # Get latest file
    latest_file = max(similar_files, key=lambda p: p.stat().st_mtime)
    
    if str(latest_file) == contacts_path:
        print(f"✅ Config already uses latest file: {latest_file.name}")
        return True
    
    # Update config
    print(f"📝 Updating config to use latest file:")
    print(f"   Old: {Path(contacts_path).name}")
    print(f"   New: {latest_file.name}")
    
    config['contacts'] = str(latest_file)
    
    # Save updated config
    with open(config_file, 'w') as f:
        json.dump(config, f, indent=2)
    
    print(f"✅ Config updated successfully")
    return True

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python update_config_contacts.py <config_file>")
        sys.exit(1)
    
    config_file = sys.argv[1]
    
    try:
        success = update_config_contacts(config_file)
        sys.exit(0 if success else 1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
