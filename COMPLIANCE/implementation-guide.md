# Minimal Integration - Add 3 Lines to Your Existing Code

## Step 1: Copy the compliance wrapper

```bash
cd ~/Downloads/GITHUB/services/utils/
# Copy the compliance_wrapper.py artifact into this directory
```

## Step 2: Modify your existing campaign script

Find your main campaign execution file (likely `utils/integrated_runner.py` or `utils/email_campaign_system.py`)

### Add at the top (after imports):

```python
from compliance_wrapper import MinimalCompliance

# Initialize compliance
compliance = MinimalCompliance(max_daily=50, max_per_domain=5, min_delay=30)
```

### Find your email sending loop (looks something like):

```python
for contact in contacts:
    email = contact['email']
    # ... prepare email ...
    send_email(to=email, subject=subject, body=body)
```

### Modify it to:

```python
for contact in contacts:
    email = contact['email']
    
    # ADD THIS - Check compliance
    can_send, reason = compliance.can_send(email)
    if not can_send:
        print(f"⏭️  Skipping {email}: {reason}")
        if reason.startswith('wait_'):
            time.sleep(int(reason.split('_')[1]))
            continue
        continue
    
    # ... your existing email preparation code ...
    
    # OPTIONAL - Add footer
    body = compliance.add_footer(body, email)
    
    # ... your existing send_email() call ...
    send_email(to=email, subject=subject, body=body)
    
    # ADD THIS - Record the send
    compliance.record_send(email)
```

## Step 3: Create suppression list file

```bash
cd ~/Downloads/GITHUB/services/
mkdir -p contacts

cat > contacts/suppression_list.json << 'EOF'
{
  "suppressed_emails": [],
  "last_updated": "2025-10-09T16:00:00",
  "count": 0
}
EOF
```

## Step 4: Test it

```bash
# Dry run to verify
python utils/integrated_runner.py \
  --contacts contacts/edu_adults_contacts_20251004_121252.csv \
  --template campaign-templates/education/outreach.docx \
  --dry-run
```

## That's it!

**You've added compliance with just 3 code additions:**

1. Import and initialize `MinimalCompliance`
2. Check `can_send()` before each email
3. Call `record_send()` after each email

**What this gives you:**

✅ Respects suppression list (opt-outs)  
✅ Enforces 50 emails/day max  
✅ Limits 5 emails per domain/day  
✅ Adds 30 second delays between sends  
✅ Automatic rate tracking  
✅ Minimal code changes  

**To add someone to suppression list:**

```bash
python3 << EOF
import json
from pathlib import Path

supp_file = Path("contacts/suppression_list.json")
with open(supp_file) as f:
    data = json.load(f)

# Add email
data['suppressed_emails'].append('someone@example.com')
data['count'] = len(data['suppressed_emails'])

with open(supp_file, 'w') as f:
    json.dump(data, f, indent=2)
    
print("✅ Added to suppression list")
EOF
```

## View current limits:

```bash
cat tracking/rate_limits.json
```

## That's really it - 3 lines of code!

Summary
The absolute minimal integration requires:

One new file: utils/compliance_wrapper.py (73 lines, simple)
Three code additions to your existing campaign script:

Initialize: compliance = MinimalCompliance()
Before send: can_send, reason = compliance.can_send(email)
After send: compliance.record_send(email)


One config file: contacts/suppression_list.json (empty list to start)
Three workflow steps (already provided in the first artifact)

What you get:

✅ Respects opt-outs automatically
✅ Rate limiting (50/day, 5/domain, 30s delays)
✅ No spam complaints
✅ Trackable metrics
✅ Legal compliance basics

Total changes: ~10 lines of code in your existing script + 1 new file
This is the absolute minimum viable compliance integration. You can always add the more sophisticated features from the full compliance files later if needed.