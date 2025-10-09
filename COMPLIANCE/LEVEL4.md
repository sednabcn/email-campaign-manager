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
name: Campaign with Compliance

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
      dry_run:
        description: 'Dry run mode'
        required: true
        type: boolean
        default: true

jobs:
  campaign_with_compliance:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v3
    
    - name: Set up Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
    
    - name: Install dependencies
      run: |
        pip install -r requirements.txt
    
    # COMPLIANCE STEP 1: Load suppression list
    - name: Load suppression list
      run: |
        echo "📋 Current suppression list:"
        if [ -f contacts/suppression_list.json ]; then
          cat contacts/suppression_list.json
        else
          echo "No suppression list found - creating empty one"
          mkdir -p contacts
          echo '{"suppressed_emails": [], "last_updated": "'$(date -Iseconds)'", "count": 0}' > contacts/suppression_list.json
        fi
    
    # COMPLIANCE STEP 2: Check reply emails for unsubscribe requests
    - name: Check for unsubscribe requests
      env:
        IMAP_SERVER: ${{ secrets.IMAP_SERVER }}
        SMTP_USER: ${{ secrets.SMTP_USER }}
        SMTP_PASS: ${{ secrets.SMTP_PASS }}
      run: |
        echo "📧 Checking for unsubscribe requests..."
        python utils/reply_handler.py --days 7 || echo "⚠️  Reply checking skipped (IMAP not configured)"
    
    # COMPLIANCE STEP 3: Show compliance stats
    - name: Show compliance stats
      run: |
        echo "📊 Compliance Statistics:"
        python3 << 'EOF'
        from compliance_wrapper import MinimalCompliance
        compliance = MinimalCompliance()
        stats = compliance.get_stats()
        for key, value in stats.items():
            print(f"   {key}: {value}")
        EOF
    
    # MAIN CAMPAIGN STEP
    - name: Run campaign with compliance
      env:
        SMTP_HOST: ${{ secrets.SMTP_HOST }}
        SMTP_PORT: ${{ secrets.SMTP_PORT }}
        SMTP_USER: ${{ secrets.SMTP_USER }}
        SMTP_PASS: ${{ secrets.SMTP_PASS }}
      run: |
        echo "🚀 Running campaign for domain: ${{ inputs.domain }}"
        
        python utils/integrated_runner.py \
          --contacts contacts \
          --scheduled campaign-templates/${{ inputs.domain }} \
          --tracking tracking \
          --alerts ${{ secrets.ALERTS_EMAIL }} \
          ${{ inputs.dry_run && '--dry-run' || '' }}
    
    # COMPLIANCE STEP 4: Post-campaign compliance report
    - name: Compliance report
      if: always()
      run: |
        echo "📊 Post-Campaign Compliance Report"
        echo "=================================="
        
        # Show updated stats
        python3 << 'EOF'
        from compliance_wrapper import MinimalCompliance
        compliance = MinimalCompliance()
        stats = compliance.get_stats()
        
        print("\nCompliance Status:")
        print(f"  Suppressed emails: {stats['suppressed_count']}")
        print(f"  Sent today: {stats['sent_today']}/{stats['daily_limit']}")
        print(f"  Remaining today: {stats['remaining_today']}")
        print(f"  Domains contacted: {stats['domains_contacted']}")
        
        # Check for violations
        if stats['sent_today'] > stats['daily_limit']:
            print("\n⚠️  WARNING: Daily limit exceeded!")
        
        if stats['remaining_today'] < 10:
            print(f"\n⚠️  WARNING: Only {stats['remaining_today']} sends remaining today")
        EOF
        
        # Show rate limit file
        if [ -f tracking/rate_limits.json ]; then
          echo -e "\nRate Limits Detail:"
          cat tracking/rate_limits.json | python -m json.tool
        fi
    
    # COMPLIANCE STEP 5: Save artifacts
    - name: Upload compliance logs
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: compliance-logs-${{ inputs.domain }}-${{ github.run_number }}
        path: |
          contacts/suppression_list.json
          contacts/suppression_log.jsonl
          contacts/reply_log.jsonl
          tracking/rate_limits.json
        retention-days: 90
    
    # COMPLIANCE STEP 6: Alert if issues
    - name: Compliance alert
      if: failure()
      run: |
        echo "🚨 COMPLIANCE ALERT: Campaign may have failed compliance checks"
        echo "Check the logs and suppression list"

# Compliance Quick Reference

## Daily Checklist

### Before Sending Campaigns
```bash
# 1. Check suppression list
cat contacts/suppression_list.json | grep count

# 2. Check today's send count
cat tracking/rate_limits.json | grep total_sent

# 3. Check for new unsubscribe requests
python utils/reply_handler.py --show-stats
```

### After Sending Campaigns
```bash
# 1. Verify send counts
python3 << 'EOF'
from compliance_wrapper import MinimalCompliance
compliance = MinimalCompliance()
print(compliance.get_stats())
EOF

# 2. Check for bounces/errors in logs
grep -i "bounce\|error\|failed" tracking/*.log

# 3. Process any replies
python utils/reply_handler.py --days 1
```

---

## Common Tasks

### Add Email to Suppression List
```bash
python3 << 'EOF'
from compliance_wrapper import MinimalCompliance
compliance = MinimalCompliance()
compliance.add_to_suppression("email@example.com", reason="manual opt-out")
EOF
```

### View Suppression List
```bash
cat contacts/suppression_list.json | python -m json.tool
```

### Check If Email Is Suppressed
```bash
python3 << 'EOF'
from compliance_wrapper import MinimalCompliance
compliance = MinimalCompliance()
email = "test@example.com"
can_send, reason = compliance.can_send(email)
print(f"Can send to {email}: {can_send} ({reason})")
EOF
```

### Reset Daily Limits (new day)
```bash
# Happens automatically, but you can force it:
rm tracking/rate_limits.json
```

### View Today's Domain Counts
```bash
cat tracking/rate_limits.json | python -m json.tool | grep -A 20 domain_counts
```

---

## Current Limits

| Limit Type | Default Value | Change In |
|------------|---------------|-----------|
| Daily total | 50 emails | `MinimalCompliance(max_daily=50)` |
| Per domain | 5 emails | `MinimalCompliance(max_per_domain=5)` |
| Minimum delay | 30 seconds | `MinimalCompliance(min_delay=30)` |

---

## Error Messages & Solutions

### "suppressed"
**Meaning:** Email is on suppression list (opted out)  
**Action:** DO NOT send. Remove from contacts or respect opt-out

### "daily_limit"
**Meaning:** Sent 50 emails today already  
**Action:** Wait until tomorrow

### "domain_limit_example.com"
**Meaning:** Sent 5 emails to example.com today  
**Action:** Wait until tomorrow or target different domain

### "wait_30"
**Meaning:** Need to wait 30 seconds before next send  
**Action:** Automatic - system will wait

---

## Integration Code

### Minimal (3 lines)
```python
from compliance_wrapper import MinimalCompliance
compliance = MinimalCompliance()

for contact in contacts:
    email = contact['email']
    
    # CHECK
    can_send, reason = compliance.can_send(email)
    if not can_send:
        print(f"Skip {email}: {reason}")
        continue
    
    # SEND (your existing code)
    send_email(email, subject, body)
    
    # RECORD
    compliance.record_send(email)
```

### With Auto-Wait
```python
from compliance_wrapper import MinimalCompliance
import time

compliance = MinimalCompliance()

for contact in contacts:
    email = contact['email']
    
    # CHECK WITH AUTO-WAIT
    can_send, reason = compliance.can_send(email)
    if not can_send:
        if reason.startswith('wait_'):
            wait = int(reason.split('_')[1])
            time.sleep(wait)
            can_send, reason = compliance.can_send(email)
        
        if not can_send:
            print(f"Skip {email}: {reason}")
            continue
    
    # SEND
    body = compliance.add_footer(body, email, 
                                 from_name="Your Name",
                                 physical_address="Your Address")
    send_email(email, subject, body)
    
    # RECORD
    compliance.record_send(email)
```

---

## File Locations

```
contacts/
├── suppression_list.json       # Opt-outs (CRITICAL)
├── suppression_log.jsonl       # Opt-out history
└── reply_log.jsonl             # All replies

tracking/
├── rate_limits.json            # Today's send counts
└── send_log.jsonl              # Send history

utils/
├── compliance_wrapper.py       # Main compliance code
└── reply_handler.py            # Process unsubscribe emails
```

---

## Monitoring Commands

### Quick Status
```bash
echo "Suppressed: $(cat contacts/suppression_list.json | python -m json.tool | grep count)"
echo "Sent Today: $(cat tracking/rate_limits.json | python -m json.tool | grep total_sent)"
```

### Detailed Report
```bash
python3 << 'EOF'
from compliance_wrapper import MinimalCompliance
import json

compliance = MinimalCompliance()
stats = compliance.get_stats()

print("\n" + "="*50)
print("COMPLIANCE REPORT")
print("="*50)

print(f"\nSuppression List:")
print(f"  Total suppressed: {stats['suppressed_count']}")

print(f"\nToday's Activity:")
print(f"  Sent: {stats['sent_today']}/{stats['daily_limit']}")
print(f"  Remaining: {stats['remaining_today']}")

print(f"\nDomain Distribution:")
print(f"  Domains contacted: {stats['domains_contacted']}")
print(f"  Per-domain limit: {stats['per_domain_limit']}")

# Load rate data for details
try:
    with open('tracking/rate_limits.json') as f:
        rate_data = json.load(f)
        if rate_data.get('domain_counts'):
            print(f"\n  Domain breakdown:")
            for domain, count in sorted(rate_data['domain_counts'].items(), 
                                       key=lambda x: x[1], reverse=True):
                print(f"    {domain}: {count}")
except:
    pass

print("\n" + "="*50)
EOF
```

### Watch for Issues
```bash
# Check for high suppression rate
total=$(wc -l < contacts/edu_adults_contacts_20251004_121252.csv)
suppressed=$(cat contacts/suppression_list.json | python -m json.tool | grep count | grep -o '[0-9]*')
percent=$((suppressed * 100 / total))
echo "Suppression rate: $percent%"
if [ $percent -gt 10 ]; then
    echo "⚠️  WARNING: High suppression rate!"
fi
```

---

## Troubleshooting

### Problem: Suppression list not working
```bash
# Check file exists and is valid JSON
cat contacts/suppression_list.json | python -m json.tool

# Check permissions
ls -la contacts/suppression_list.json

# Recreate if corrupted
cat > contacts/suppression_list.json << 'EOF'
{
  "suppressed_emails": [],
  "last_updated": "2025-10-09T16:00:00",
  "count": 0
}
EOF
```

### Problem: Rate limits not enforcing
```bash
# Check rate file
cat tracking/rate_limits.json

# Check date is today
date -I

# Force reset if wrong date
rm tracking/rate_limits.json
```

### Problem: Compliance module not found
```bash
# Check file exists
ls -la utils/compliance_wrapper.py

# Check Python path
python3 -c "import sys; print('\n'.join(sys.path))"

# Add to path if needed
export PYTHONPATH="${PYTHONPATH}:$(pwd)/utils"
```

---

## Emergency Stop

If you need to stop all campaigns immediately:

```bash
# Method 1: Set daily limit to 0
python3 << 'EOF'
import json
from pathlib import Path

rate_file = Path("tracking/rate_limits.json")
if rate_file.exists():
    with open(rate_file) as f:
        data = json.load(f)
    data['total_sent'] = 999  # Exceeds limit
    with open(rate_file, 'w') as f:
        json.dump(data, f)
    print("✅ Daily limit set to prevent sends")
EOF

# Method 2: Add all contacts to suppression
python3 << 'EOF'
import csv
import json
from pathlib import Path

contacts_file = "contacts/edu_adults_contacts_20251004_121252.csv"
supp_file = Path("contacts/suppression_list.json")

with open(supp_file) as f:
    data = json.load(f)

with open(contacts_file) as f:
    reader = csv.DictReader(f)
    for row in reader:
        email = row.get('email', '').strip().lower()
        if email and email not in data['suppressed_emails']:
            data['suppressed_emails'].append(email)

data['count'] = len(data['suppressed_emails'])
with open(supp_file, 'w') as f:
    json.dump(data, f, indent=2)

print(f"✅ Added all contacts to suppression list")
EOF
```

---

## Legal Requirements by Region

### United States (CAN-SPAM)
✅ Physical address in footer  
✅ Clear unsubscribe method  
✅ Honor opt-outs within 10 days  
✅ Accurate "From" information  
✅ No deceptive subject lines

### European Union (GDPR)
✅ Explicit consent BEFORE emailing  
✅ Easy opt-out mechanism  
✅ Data protection measures  
✅ Right to be forgotten  
⚠️  WARNING: Cold email may violate GDPR

### Canada (CASL)
✅ Express consent before sending  
✅ Clear identification  
✅ Unsubscribe mechanism  
⚠️  WARNING: Implied consent has limits

**YOU are responsible for compliance in your jurisdiction.**

---

## Best Practices

### ✅ DO
- Always run dry-run first
- Check suppression list daily
- Process unsubscribe requests immediately
- Keep detailed logs
- Respect all opt-outs
- Personalize every email
- Monitor response rates
- Stay under limits

### ❌ DON'T
- Ignore opt-out requests
- Exceed daily limits
- Flood single domains
- Use purchased contact lists
- Send without testing
- Ignore bounces
- Continue if response rate <1%
- Remove tracking/logging

---

## Support

If compliance checks are failing:

1. **Check files exist:**
   ```bash
   ls -la contacts/suppression_list.json
   ls -la tracking/rate_limits.json
   ls -la utils/compliance_wrapper.py
   ```

2. **Verify JSON validity:**
   ```bash
   python -m json.tool contacts/suppression_list.json
   python -m json.tool tracking/rate_limits.json
   ```

3. **Test compliance module:**
   ```bash
   python utils/compliance_wrapper.py
   ```

4. **Check integration:**
   ```bash
   python -c "from compliance_wrapper import MinimalCompliance; print('✅ Import works')"
   ```

---

## Quick Stats Dashboard

Save this as `show_stats.sh`:
```bash
#!/bin/bash
echo "=================================="
echo "COMPLIANCE DASHBOARD"
echo "=================================="
echo ""

# Suppression
supp_count=$(cat contacts/suppression_list.json 2>/dev/null | python -m json.tool | grep '"count"' | grep -o '[0-9]*' || echo "0")
echo "📋 Suppression List: $supp_count emails"

# Today's sends
sent_today=$(cat tracking/rate_limits.json 2>/dev/null | python -m json.tool | grep '"total_sent"' | grep -o '[0-9]*' || echo "0")
echo "📤 Sent Today: $sent_today/50"

# Remaining
remaining=$((50 - sent_today))
echo "⏳ Remaining Today: $remaining"

# Domains
domain_count=$(cat tracking/rate_limits.json 2>/dev/null | python -m json.tool | grep -c '"' || echo "0")
echo "🌐 Domains Contacted: $domain_count"

# Recent activity
if [ -f tracking/send_log.jsonl ]; then
    last_send=$(tail -1 tracking/send_log.jsonl | python -m json.tool | grep timestamp | cut -d'"' -f4)
    echo "🕐 Last Send: $last_send"
fi

echo ""
echo "=================================="
```

Make it executable:
```bash
chmod +x show_stats.sh
./show_stats.sh
```