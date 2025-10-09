#!/usr/bin/env python3
"""
Compliance System Test Script
Run this to verify your compliance setup is working correctly
"""

import sys
import json
from pathlib import Path

def test_files():
    """Test that all required files exist"""
    print("\n📁 Testing File Structure...")
    
    required_files = {
        'utils/compliance_wrapper.py': 'Compliance module',
        'contacts/suppression_list.json': 'Suppression list',
    }
    
    optional_files = {
        'utils/reply_handler.py': 'Reply handler',
        'tracking/rate_limits.json': 'Rate limits (created on first send)',
    }
    
    all_good = True
    
    for file_path, description in required_files.items():
        if Path(file_path).exists():
            print(f"  ✅ {description}: {file_path}")
        else:
            print(f
