#!/usr/bin/env python3
"""
Quick fix script to initialize missing compliance and tracking files
Run this before your campaign execution
"""

import json
from pathlib import Path
from datetime import datetime

def initialize_compliance_files():
    """Create all required compliance and tracking files"""
    
    print("🔧 Initializing compliance and tracking files...")
    
    # 1. Create contacts directory
    contacts_dir = Path("contacts")
    contacts_dir.mkdir(exist_ok=True)
    print(f"✅ Created {contacts_dir}")
    
    # 2. Create suppression list
    suppression_file = contacts_dir / "suppression_list.json"
    if not suppression_file.exists():
        suppression_data = {
            "suppressed_emails": [],
            "last_updated": datetime.now().isoformat(),
            "count": 0,
            "version": "1.0"
        }
        with open(suppression_file, 'w') as f:
            json.dump(suppression_data, f, indent=2)
        print(f"✅ Created {suppression_file}")
    else:
        print(f"ℹ️  {suppression_file} already exists")
    
    # 3. Create suppression log
    suppression_log = contacts_dir / "suppression_log.jsonl"
    if not suppression_log.exists():
        suppression_log.touch()
        print(f"✅ Created {suppression_log}")
    
    # 4. Create reply log
    reply_log = contacts_dir / "reply_log.jsonl"
    if not reply_log.exists():
        reply_log.touch()
        print(f"✅ Created {reply_log}")
    
    # 5. Create tracking directory
    tracking_dir = Path("tracking")
    tracking_dir.mkdir(exist_ok=True)
    print(f"✅ Created {tracking_dir}")
    
    # 6. Create rate limits file
    rate_limits_file = tracking_dir / "rate_limits.json"
    today = datetime.now().date().isoformat()
    
    rate_data = {
        "daily_sent": 0,
        "last_reset": today,
        "domain_counts": {},
        "last_updated": datetime.now().isoformat(),
        "version": "1.0"
    }
    
    with open(rate_limits_file, 'w') as f:
        json.dump(rate_data, f, indent=2)
    print(f"✅ Created {rate_limits_file}")
    
    # 7. Create unsubscribed list
    unsubscribed_file = tracking_dir / "unsubscribed.json"
    if not unsubscribed_file.exists():
        unsubscribed_data = {}
        with open(unsubscribed_file, 'w') as f:
            json.dump(unsubscribed_data, f, indent=2)
        print(f"✅ Created {unsubscribed_file}")
    
    print("\n✅ All compliance files initialized successfully!")
    return True

if __name__ == "__main__":
    try:
        initialize_compliance_files()
        print("\n🎉 Setup complete - ready for campaign execution")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()
        exit(1)
