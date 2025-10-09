# Compliance Implementation Checklist

## Phase 1: Basic Setup (15 minutes)

### Step 1: Copy Files
- [ ] Copy `compliance_wrapper.py` to `utils/compliance_wrapper.py`
- [ ] Copy `reply_handler.py` to `utils/reply_handler.py`
- [ ] Make scripts executable: `chmod +x utils/*.py`

### Step 2: Create Directories
```bash
mkdir -p contacts
mkdir -p tracking
```

### Step 3: Initialize Suppression List
```bash
cat > contacts/suppression_list.json << 'EOF'
{
  "suppressed_emails": [],
  "last_updated": "2025-10-09T16:00:00",
  "count": 0
}
EOF
```

### Step 4: Test Compliance Module
```bash
python utils/compliance_wrapper.py
# Should show: "✅ Compliance initialized: 0 suppressed, 0/50 sent today"
```

---

## Phase 2: Code Integration (20 minutes)

### Step 5: Modify Campaign Script

Find your main campaign file (likely `utils/integrated_runner.py` or similar).

#### Add Import (at top of file)
```python
from compliance_wrapper import MinimalCompliance
import time
```

#### Initialize Compliance (before email loop)
```python
# Initialize compliance with your limits
compliance = MinimalCompliance(
    max_daily=50,        # Maximum 50 emails per day
    max_per_domain=5,    # Maximum 5 per domain per day
    min_delay=30         # Minimum 30 seconds between sends
)

# Show initial stats
print("\n📊 Compliance Status:")
stats = compliance.get_stats()
for key, value in stats.items():
    print(f"   {key}: {value}")
```

#### Modify Email Loop
**BEFORE:**
```python
for contact in contacts:
    email = contact['email']
    # ... prepare email ...
    send_email(to=email, subject=subject, body=body)
```

**AFTER:**
```python
for contact in contacts:
    email = contact['email']
    
    # 🔒 COMPLIANCE CHECK
    can_send, reason = compliance.can_send(email)
    if not can_send:
        # Handle wait periods
        if reason.startswith('wait_'):
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
    
    # 🔒 ADD FOOTER
    body = compliance.add_footer(
        body, 
        email,
        from_name="Your Full Name",  # Change this
        physical_address="Your Street, City, State, Country, Postal Code"  # Change this
    )
    
    # ... your existing send_email() call ...
    send_email(to=email, subject=subject, body=body)
    
    # 🔒 RECORD SEND
    compliance.record_send(email)
    print(f"✅ Sent to {email}")
```

### Step 6: Update Your Information

Edit the `add_footer` call to include YOUR real information:

```python
body = compliance.add_footer(
    body, 
    email,
    from_name="John Doe",  # Your real name
    physical_address="123 Main St, London, UK, SW1A 1AA"  # Your real address
)
```

⚠️ **IMPORTANT:** Physical address is REQUIRED by law in many jurisdictions.

---

## Phase 3: Testing (30 minutes)

### Step 7: Dry Run Test
```bash
python utils/integrated_runner.py \
  --contacts contacts/edu_adults_contacts_20251004_121252.csv \
  --scheduled scheduled-campaigns \
  --tracking tracking \
  --alerts your.email@example.com \
  --dry-run
```

**Check for:**
- [ ] Compliance stats shown at start
- [ ] No errors about missing compliance module
- [ ] Footer appears in emails
- [ ] Rate limits displayed

### Step 8: Test Suppression
```bash
# Add a test email to suppression
python3 << 'EOF'
from compliance_wrapper import MinimalCompliance
compliance = MinimalCompliance()
compliance.add_to_suppression("test@example.com", reason="testing")
print("✅ Test email suppressed")
EOF

# Verify it's in the list
cat contacts/suppression_list.json
```

### Step 9: Test Rate Limiting
```bash
# Create a small test with 3 emails
# Run your campaign
# Check that delays are enforced

cat tracking/rate_limits.json
# Should show 3 sends and domain counts
```

### Step 10: Self-Test
```bash
# Create a test file with YOUR email
cat > contacts/self_test.csv << EOF
name,email,organization
Your Name,your.email@domain.com,Test Org
EOF

# Send to yourself (LIVE, not dry-run)
python utils/integrated_runner.py \
  --contacts contacts/self_test.csv \
  --scheduled scheduled-campaigns \
  --tracking tracking \
  --alerts your.email@example.com

# Check your inbox - verify:
# - Footer is present
# - Your address is included
# - Unsubscribe instructions are clear
# - Email looks professional
```

---

## Phase 4: GitHub Actions (20 minutes)

### Step 11: Update Workflow File

Edit `.github/workflows/campaign_prod_domain_run.yml`:

**Add before the campaign step:**
```yaml
    - name: Load suppression list
      run: |
        echo "📋 Current suppression list:"
        if [ -f contacts/suppression_list.json ]; then
          cat contacts/suppression_list.json
        else
          echo "Creating suppression list..."
          mkdir -p contacts
          echo '{"suppressed_emails": [], "last_updated": "'$(date -Iseconds)'", "count": 0}' > contacts/suppression_list.json
        fi

    - name: Check compliance status
      run: |
        python3 << 'EOF'
        from compliance_wrapper import MinimalCompliance
        compliance = MinimalCompliance()
        stats = compliance.get_stats()
        print("\n📊 Compliance Status:")
        for key, value in stats.items():
            print(f"   {key}: {value}")
        EOF
```

**Add after the campaign step:**
```yaml
    - name: Save compliance logs
      if: always()
      uses: actions/upload-artifact@v3
      with:
        name: compliance-logs
        path: |
          contacts/suppression_list.json
          tracking/rate_limits.json
        retention-days: 90
```

### Step 12: Add Secrets

In GitHub Settings → Secrets, add:
- [ ] `SMTP_HOST` - Your SMTP server
- [ ] `SMTP_PORT` - Usually 587
- [ ] `SMTP_USER` - Your email
- [ ] `SMTP_PASS` - Your password
- [ ] `ALERTS_EMAIL` - Where to send alerts

Optional (for reply handling):
- [ ] `IMAP_SERVER` - Your IMAP server

### Step 13: Test GitHub Actions
```bash
# Commit changes
git add utils/compliance_wrapper.py
git add utils/reply_handler.py
git add contacts/suppression_list.json
git add .github/workflows/campaign_prod_domain_run.yml
git commit -m "Add compliance system"
git push

# Run workflow manually
# Go to Actions → Select workflow → Run workflow
# Use dry-run=true first
```

---

## Phase 5: Ongoing Maintenance (Daily)

### Daily Tasks

#### Morning Routine (5 minutes)
```bash
# 1. Check for unsubscribe requests
python utils/reply_handler.py --show-stats

# 2. Process any new requests
python utils/reply_handler.py --days 1

# 3. View compliance status
./show_stats.sh  # Or use the Python one-liner below
```

Quick status check:
```bash
python3 << 'EOF'
from compliance_wrapper import MinimalCompliance
compliance = MinimalCompliance()
stats = compliance.get_stats()
print(f"Suppressed: {stats['suppressed_count']}")
print(f"Sent today: {stats['sent_today']}/{stats['daily_limit']}")
print(f"Remaining: {stats['remaining_today']}")
EOF
```

#### After Campaign (5 minutes)
```bash
# 1. Check final counts
cat tracking/rate_limits.json | python -m json.tool

# 2. Check for errors
grep -i "error\|failed\|bounce" tracking/*.log

# 3. Verify no limit violations
python3 << 'EOF'
from compliance_wrapper import MinimalCompliance
import json

compliance = MinimalCompliance()
stats = compliance.get_stats()

if stats['sent_today'] > stats['daily_limit']:
    print("⚠️  WARNING: Daily limit exceeded!")
else:
    print("✅ All limits respected")
EOF
```

### Weekly Tasks

#### Monday Morning (10 minutes)
```bash
# 1. Review last week's activity
ls -la tracking/

# 2. Check suppression growth rate
python3 << 'EOF'
import json
with open('contacts/suppression_list.json') as f:
    data = json.load(f)
print(f"Total suppressed: {data['count']}")
print(f"Last updated: {data['last_updated']}")
EOF

# 3. Clean old logs (keep 30 days)
find tracking/ -name "*.log" -mtime +30 -delete
```

### Monthly Tasks

#### First of Month (20 minutes)
```bash
# 1. Generate compliance report
python3 << 'EOF'
import json
from datetime import datetime
from pathlib import Path

print("="*60)
print("MONTHLY COMPLIANCE REPORT")
print(f"Generated: {datetime.now().strftime('%Y-%m-%d')}")
print("="*60)

# Suppression stats
with open('contacts/suppression_list.json') as f:
    supp_data = json.load(f)
print(f"\nSuppression List: {supp_data['count']} emails")

# Check all contact files
contacts_dir = Path('contacts')
csv_files = list(contacts_dir.glob('*.csv'))
total_contacts = 0
for csv_file in csv_files:
    with open(csv_file) as f:
        lines = len(f.readlines()) - 1  # Minus header
        total_contacts += lines

if total_contacts > 0:
    suppression_rate = (supp_data['count'] / total_contacts) * 100
    print(f"Suppression Rate: {suppression_rate:.2f}%")
    
    if suppression_rate > 10:
        print("⚠️  WARNING: High suppression rate")

# Check log files exist
log_files = {
    'Suppression Log': 'contacts/suppression_log.jsonl',
    'Reply Log': 'contacts/reply_log.jsonl',
    'Send Log': 'tracking/send_log.jsonl'
}

print("\nLog Files:")
for name, path in log_files.items():
    if Path(path).exists():
        lines = len(open(path).readlines())
        print(f"  {name}: {lines} entries")
    else:
        print(f"  {name}: Not found")

print("\n" + "="*60)
EOF

# 2. Archive old logs
mkdir -p tracking/archive
mv tracking/*.log tracking/archive/ 2>/dev/null || true

# 3. Backup suppression list
cp contacts/suppression_list.json \
   contacts/suppression_list_backup_$(date +%Y%m).json
```

---

## Phase 6: Monitoring & Alerts

### Set Up Monitoring Script

Save as `monitor_compliance.sh`:
```bash
#!/bin/bash

# Compliance monitoring script - run after each campaign

echo "🔍 COMPLIANCE MONITORING"
echo "======================="

# Check if we exceeded limits
sent=$(cat tracking/rate_limits.json 2>/dev/null | python -m json.tool | grep '"total_sent"' | grep -o '[0-9]*' || echo "0")

if [ "$sent" -gt 50 ]; then
    echo "🚨 ALERT: Daily limit exceeded! ($sent/50)"
    exit 1
fi

if [ "$sent" -gt 45 ]; then
    echo "⚠️  WARNING: Approaching daily limit ($sent/50)"
fi

# Check suppression rate
total_contacts=$(wc -l < contacts/*.csv 2>/dev/null | head -1 || echo "100")
suppressed=$(cat contacts/suppression_list.json 2>/dev/null | python -m json.tool | grep '"count"' | grep -o '[0-9]*' || echo "0")

if [ "$total_contacts" -gt 0 ]; then
    rate=$((suppressed * 100 / total_contacts))
    echo "📊 Suppression rate: $rate%"
    
    if [ "$rate" -gt 10 ]; then
        echo "🚨 ALERT: High suppression rate!"
        exit 1
    fi
fi

# Check for recent unsubscribe requests
if [ -f contacts/suppression_log.jsonl ]; then
    recent=$(tail -10 contacts/suppression_log.jsonl | wc -l)
    if [ "$recent" -gt 5 ]; then
        echo "⚠️  WARNING: $recent recent unsubscribe requests"
    fi
fi

echo "✅ Compliance check passed"
```

Make executable:
```bash
chmod +x monitor_compliance.sh
```

Run after campaigns:
```bash
./monitor_compliance.sh || echo "Compliance issues detected!"
```

---

## Troubleshooting Guide

### Issue: "ModuleNotFoundError: No module named 'compliance_wrapper'"

**Solution:**
```bash
# Check file exists
ls -la utils/compliance_wrapper.py

# Add utils to Python path
export PYTHONPATH="${PYTHONPATH}:$(pwd)/utils"

# Or use absolute import in your script
import sys
sys.path.insert(0, 'utils')
from compliance_wrapper import MinimalCompliance
```

### Issue: Suppression list not working

**Solution:**
```bash
# Verify JSON is valid
cat contacts/suppression_list.json | python -m json.tool

# Recreate if corrupted
cat > contacts/suppression_list.json << 'EOF'
{
  "suppressed_emails": [],
  "last_updated": "2025-10-09T16:00:00",
  "count": 0
}
EOF

# Test directly
python3 << 'EOF'
from compliance_wrapper import MinimalCompliance
c = MinimalCompliance()
c.add_to_suppression("test@test.com")
print(c.can_send("test@test.com"))  # Should print (False, 'suppressed')
EOF
```

### Issue: Rate limits not enforcing

**Solution:**
```bash
# Check rate file
cat tracking/rate_limits.json | python -m json.tool

# Verify date is correct
python3 << 'EOF'
import json
from datetime import datetime

with open('tracking/rate_limits.json') as f:
    data = json.load(f)

print(f"Rate file date: {data.get('date')}")
print(f"Today's date: {datetime.now().date().isoformat()}")

if data.get('date') != datetime.now().date().isoformat():
    print("⚠️  Rate file has old date - will reset on next send")
EOF
```

### Issue: Footer not appearing

**Solution:**
```python
# Check you're calling add_footer
body = compliance.add_footer(
    body, 
    email,
    from_name="Your Name",
    physical_address="Your Address"
)

# Verify footer is added
print("Footer check:")
print("Has 'unsubscribe':", 'unsubscribe' in body.lower())
print("Has address:", 'Your Address' in body)
```

---

## Success Criteria

After implementation, verify:

- [ ] Suppression list file exists and is valid JSON
- [ ] Rate limits file is created after first send
- [ ] Emails include footer with unsubscribe instructions
- [ ] Physical address appears in all emails
- [ ] System respects suppression list (test this)
- [ ] Daily limits are enforced (test with limit=5)
- [ ] Delays between sends are enforced
- [ ] GitHub Actions workflow runs successfully
- [ ] Compliance logs are saved as artifacts
- [ ] You can add emails to suppression manually
- [ ] Reply handler can process unsubscribe requests

---

## Next Steps

Once basic compliance is working:

1. **Week 1:** Monitor closely, fix any issues
2. **Week 2:** Add reply handler automation
3. **Week 3:** Set up automated monitoring
4. **Week 4:** Review metrics and adjust limits if needed

**Remember:** Compliance is ongoing, not one-time setup!