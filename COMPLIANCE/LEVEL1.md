LEVEL 1: BASIC COMPLIANCE (Start Here)
This adds the absolute minimum protection with just one file and 3 lines of code.
Step 1: Create the Compliance Wrapper
Save this as utils/compliance_wrapper.py:compliance_wrapper.py - Minimal ComplianceCode """
Minimal Compliance Wrapper - Easy integration with existing code
Add just 3 lines to your existing campaign script for basic compliance
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path
from typing impStep 2: Create Empty Suppression List
Run these commands:
bashcd ~/Downloads/GITHUB/services/

# Create the file
cat > contacts/suppression_list.json << 'EOF'
{
  "suppressed_emails": [],
  "last_updated": "2025-10-09T16:00:00",
  "count": 0
}
EOF

# Verify it was created
cat contacts/suppression_list.json
Step 3: Modify Your Campaign Script
Open utils/integrated_runner.py (or wherever your main campaign loop is).
Find this section (around line 240-260):
pythonfor contact in contacts:
    email = contact['email']
    # ... prepare email ...
    send_email(to=email, subject=subject, body=body)
Replace it with this:
python# ADD THIS AT THE TOP (after other imports)
from compliance_wrapper import MinimalCompliance
import time

# ADD THIS BEFORE THE LOOP
compliance = MinimalCompliance(max_daily=50, max_per_domain=5, min_delay=30)

# MODIFY THE LOOP
for contact in contacts:
    email = contact['email']
    
    # CHECK COMPLIANCE
    can_send, reason = compliance.can_send(email)
    if not can_send:
        if reason.startswith('wait_'):
            # Extract wait time and sleep
            wait_seconds = int(reason.split('_')[1])
            print(f"⏱️  Waiting {wait_seconds}s before next send...")
            time.sleep(wait_seconds)
            # Try again after waiting
            can_send, reason = compliance.can_send(email)
            if not can_send:
                print(f"⏭️  Skipping {email}: {reason}")
                continue
        else:
            print(f"⏭️  Skipping {email}: {reason}")
            continue
    
    # ... your existing email preparation code ...
    
    # OPTIONAL: Add footer
    body = compliance.add_footer(body, email)
    
    # ... your existing send_email() call ...
    send_email(to=email, subject=subject, body=body)
    
    # RECORD THE SEND
    compliance.record_send(email)
    print(f"✅ Sent to {email}")
Step 4: Test It
bash# Test with dry-run first
python utils/integrated_runner.py \
  --contacts contacts/edu_adults_contacts_20251004_121252.csv \
  --scheduled scheduled-campaigns \
  --tracking tracking \
  --alerts your.email@example.com \
  --dry-run

# Check what was created
ls -la contacts/
ls -la tracking/
That's it! You now have basic compliance.

LEVEL 2: STANDARD COMPLIANCE (Add Later)
This adds a proper unsubscribe footer with better formatting.
Enhanced Footer
Modify the add_footer method in your compliance_wrapper.py:compliance_wrapper.py - Minimal ComplianceCode ∙ Version 2     def add_footer(self, body: str, recipient_email: str, 
                   from_name: str = "Professional Outreach",
                   physical_address: str = None) -> str:
        """
        Add compliance footer to email
        
        Args:Update Your Campaign Script
python# When calling add_footer, include your info:
body = compliance.add_footer(
    body, 
    email,
    from_name="Your Full Name",
    physical_address="Your Street, City, Country, Postal Code"
)

LEVEL 3: FULL COMPLIANCE (Optional)
For complete compliance, you'll also want to handle email replies.
Email Reply Handlerreply_handler.py - Process Unsubscribe RequestsCode #!/usr/bin/env python3
"""
Email Reply Handler - Process unsubscribe requests from email replies
Run this regularly to check for unsubscribe requests
"""

import imaplib
import email
import json
from datetime import datetime
from pathlib import Path
Usage:
bash# Check for unsubscribe requests (requires IMAP credentials)
python utils/reply_handler.py --days 7

# Show current suppression list
python utils/reply_handler.py --show-stats

# Process and mark emails as read
python utils/reply_handler.py --mark-read

GitHub Actions Integration
Add this to your .github/workflows/campaign_prod_domain_run.yml:Compliance Steps for GitHub Actions WorkflowCode name: Campaign with Compliance

on:
  workflow_dispatch:
    inputs:
      domain:
        description: 'Domain to process'
        required: true
        type: choice
        options:
          - education
          - healthcare
          - finance

Quick Reference Card
Save this as COMPLIANCE_QUICK_REF.md:Compliance Quick ReferenceDocument # Compliance Quick Reference

## Daily Checklist

### Before Sending Campaigns
```bash
# 1. Check suppression list
cat contacts/suppression_list.json | grep count

# 2. Check today's send count
cat tracking/rate_limits.json | grep total_sent

# 3. ChRetryClaude does not have the ability to run the code it generates yet.RContinueCompliance Quick ReferenceDocument ∙ Version 2 ### After Sending Campaigns
```bash
# 1. Verify send counts
python3 << 'EOF'
from compliance_wrapper import MinimalCompliance
compliance = MinimalCompliance()
print(compliance.get_stats())
EOF

# 2. Check for bounces/errors in logs
grep -i "bounce\|e
Complete Implementation Checklist
Here's your step-by-step implementation guide:Complete Implementation ChecklistDocument # Compliance Implementation Checklist

## Phase 1: Basic Setup (15 minutes)

### Step 1: Copy Files
- [ ] Copy `compliance_wrapper.py` to `utils/compliance_wrapper.py`
- [ ] Copy `reply_handler.py` to `utils/reply_handler.py`
- [ ] Make scripts execuPerfect! Now let me create one final artifact - a simple test script to verify everything is working:test_compliance.py - Verify SetupCode #!/usr/bin/env python3
"""
Compliance System Test Script
Run this to verify your compliance setup is working correctly
"""

import sys
import json
from pathlib import Path

def test_files():
    """Test that all required files exist"""
    print("\n�RetryThis response paused because Claude reached its max length for a message. Hit continue to nudge Claude along.ContinueClaude can make mistakes. Please double-check responses.