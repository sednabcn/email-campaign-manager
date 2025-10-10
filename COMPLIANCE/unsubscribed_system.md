# Email Unsubscribe System - Complete Setup Guide

Production-ready unsubscribe system for email campaigns with CAN-SPAM compliance.

## 🎯 Features

- ✅ **Secure token-based unsubscribe links** - Cryptographically signed tokens
- ✅ **CAN-SPAM compliant** - Required footer and headers
- ✅ **Thread-safe** - Safe for concurrent operations
- ✅ **Campaign-specific unsubscribes** - Granular control
- ✅ **Statistics and reporting** - Track unsubscribe rates
- ✅ **Easy integration** - Drop-in replacement for existing systems
- ✅ **Static hosting friendly** - Works with GitHub Pages

## 📋 Prerequisites

- Python 3.7+
- GitHub account (for hosting unsubscribe page)
- Email sending capability (SMTP, API, etc.)

## 🚀 Quick Start (5 minutes)

### Step 1: Setup GitHub Pages Unsubscribe Page

```bash
# Clone your GitHub Pages repo
cd sednabcn.github.io

# Create unsubscribe directory
mkdir unsubscribe

# Copy the unsubscribe page HTML
# (Use the HTML artifact provided)
# Save as: unsubscribe/index.html

# Commit and push
git add unsubscribe/index.html
git commit -m "Add unsubscribe page"
git push origin main
```

Your page will be live at: `https://sednabcn.github.io/unsubscribe`

### Step 2: Add Python Code to Your Project

```bash
# Create the unsubscribe manager file
touch unsubscribe_manager.py

# Copy the UnsubscribeManager class code
# (From the first Python artifact)
```

### Step 3: Integrate with Your Email System

```python
from pathlib import Path
from unsubscribe_manager import UnsubscribeManager

# Initialize
manager = UnsubscribeManager(
    tracking_dir=Path("tracking"),
    base_url="https://sednabcn.github.io/unsubscribe"
)

# Filter contacts before sending
valid_contacts, skipped = manager.filter_contacts(
    all_contacts, 
    campaign_id="my_campaign"
)

# Add unsubscribe links
for contact in valid_contacts:
    contact['unsubscribe_link'] = manager.generate_unsubscribe_link(
        contact['email'], 
        "my_campaign"
    )

# Send emails (your existing code)
```

## 📁 Project Structure

```
your-project/
├── unsubscribe_manager.py      # Core unsubscribe logic
├── email_personalizer.py        # Email personalization with unsubscribe
├── docx_parser.py              # Your main script (modified)
├── manage_unsubscribes.py      # CLI tool for management
├── tracking/
│   ├── unsubscribed.json       # Unsubscribe list (auto-created)
│   └── .secret_key             # Encryption key (auto-created)
└── config.json                 # Your campaign config

sednabcn.github.io/             # Separate repo
└── unsubscribe/
    └── index.html              # Unsubscribe page
```

## 🔧 Integration Options

### Option A: Minimal Integration (Recommended for Testing)

Just filter contacts and add links:

```python
# Filter unsubscribed contacts
valid, skipped = manager.filter_contacts(contacts, campaign_id)
print(f"Sending to {len(valid)} contacts, skipped {len(skipped)}")

# Add unsubscribe links
for contact in valid:
    contact['unsub'] = manager.generate_unsubscribe_link(
        contact['email'], 
        campaign_id
    )
```

### Option B: Full Integration (Production-Ready)

Use the enhanced personalizer:

```python
from email_personalizer import ImprovedEmailPersonalizer

# Initialize
personalizer = ImprovedEmailPersonalizer(
    unsubscribe_manager=manager,
    from_name="John Doe",
    from_email="john@example.com",
    physical_address="123 Main St, City, ST 12345"
)

# Create personalized emails
results = personalizer.batch_create_emails(
    template, 
    contacts, 
    campaign_id
)

# Send ready emails
for email_data in results['ready']:
    send_email(email_data)
```

### Option C: Modify Existing Code

Patch your `docx_parser.py`:

```python
# In campaign_main(), after emailer initialization:
unsub_manager = UnsubscribeManager(
    tracking_dir=tracking_root,
    base_url="https://sednabcn.github.io/unsubscribe"
)

# Filter contacts
valid_contacts, skipped = unsub_manager.filter_contacts(
    all_contacts, 
    full_campaign_name
)

# Add unsubscribe links
for i, contact in enumerate(valid_contacts):
    contact['unsubscribe_link'] = unsub_manager.generate_unsubscribe_link(
        contact['email'], 
        full_campaign_name
    )
```

## 📝 Email Footer Requirements

Every email **must** include an unsubscribe footer. Here's the template:

### Plain Text Footer

```
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

Professional Outreach from [Your Name]

You received this email as part of professional networking outreach.

If you prefer not to receive future emails, please visit:
[UNSUBSCRIBE_LINK]

Contact: your@email.com
Address: Your Physical Address

This is a one-time professional outreach. We respect your preferences 
and will honor all opt-out requests immediately.
```

### HTML Footer

```html
<div style="margin-top: 40px; padding-top: 20px; border-top: 2px solid #e0e0e0;">
    <p><strong>Professional Outreach from [Your Name]</strong></p>
    <p>You received this email as part of professional networking outreach.</p>
    <p>
        If you prefer not to receive future emails, you can 
        <a href="[UNSUBSCRIBE_LINK]">unsubscribe here</a>.
    </p>
    <p>Contact: your@email.com<br>Address: Your Physical Address</p>
</div>
```

## 🛠️ Management Tools

### Command Line Interface

```bash
# Add unsubscribe
python manage_unsubscribes.py add --email user@example.com --campaign all

# Check status
python manage_unsubscribes.py check --email user@example.com

# View statistics
python manage_unsubscribes.py stats

# List all unsubscribed emails
python manage_unsubscribes.py list

# Export to file
python manage_unsubscribes.py export --output backup.json

# Remove from list (resubscribe)
python manage_unsubscribes.py remove --email user@example.com
```

### Python API

```python
# Add unsubscribe
manager.add_unsubscribe(
    "user@example.com",
    campaign_id="all",
    reason="User request",
    source="web"
)

# Check if unsubscribed
if manager.is_unsubscribed("user@example.com", "campaign_id"):
    print("Skip this contact")

# Get statistics
stats = manager.get_stats()
print(f"Total unsubscribed: {stats['total_unsubscribed']}")

# Get all unsubscribed emails
emails = manager.get_unsubscribed_emails()

# Export/import
manager.export_list(Path("backup.json"))
manager.import_list(Path("backup.json"))
```

## 📊 Monitoring and Reporting

### View Statistics

```python
stats = manager.get_stats()
```

Returns:
```json
{
  "total_unsubscribed": 45,
  "global_unsubscribes": 12,
  "recent_7_days": 3,
  "by_campaign": {
    "campaign1": 15,
    "campaign2": 18,
    "all": 12
  },
  "last_updated": "2025-10-10T10:30:00"
}
```

### Weekly Report Script

```python
def weekly_report():
    stats = manager.get_stats()
    
    print(f"""
    📊 WEEKLY REPORT
    ================
    Total Unsubscribed: {stats['total_unsubscribed']}
    New This Week: {stats['recent_7_days']}
    
    Unsubscribe Rate: {stats['recent_7_days'] / sent_emails * 100:.2f}%
    """)
```

## 🔒 Security Features

1. **Secure Token Generation**
   - Uses cryptographically secure random numbers
   - HMAC-style verification
   - Token expiration (90 days)

2. **Secret Key Management**
   - Auto-generated on first run
   - Stored with restricted permissions (600)
   - Never transmitted

3. **Email Validation**
   - Lowercase normalization
   - Format validation
   - Duplicate prevention

## ✅ CAN-SPAM Compliance Checklist

- [x] Clear "From" information
- [x] Accurate subject line
- [x] Physical postal address in footer
- [x] Clear unsubscribe mechanism
- [x] Honor opt-outs within 10 business days
- [x] Label message as advertisement (if applicable)
- [x] Monitor what others are doing on your behalf

## 🐛 Troubleshooting

### Issue: Unsubscribe page not loading

**Solution:**
```bash
# Check GitHub Pages is enabled
# Go to: repo Settings > Pages > Source: main branch

# Verify URL
curl https://sednabcn.github.io/unsubscribe
```

### Issue: Contacts not being filtered

**Solution:**
```python
# Check if email is in the unsubscribe list
is_unsub = manager.is_unsubscribed("email@example.com")
print(f"Unsubscribed: {is_unsub}")

# Check the data file
import json
with open("tracking/unsubscribed.json") as f:
    data = json.load(f)
    print(json.dumps(data, indent=2))
```

### Issue: Token validation failing

**Solution:**
```python
# Regenerate secret key
import os
os.remove("tracking/.secret_key")

# Re-initialize manager
manager = UnsubscribeManager(...)
```

### Issue: Permission denied on .secret_key

**Solution:**
```bash
chmod 600 tracking/.secret_key
```

## 📚 Advanced Usage

### Custom Unsubscribe Reasons

```python
manager.add_unsubscribe(
    "user@example.com",
    campaign_id="all",
    reason="Content not relevant",
    source="web"
)

# View history
data = manager._load_unsubscribed()
history = data["user@example.com"]["history"]
for event in history:
    print(f"{event['timestamp']}: {event['reason']}")
```

### Campaign-Specific Unsubscribes

```python
# Unsubscribe from specific campaign
manager.add_unsubscribe("user@example.com", "newsletter")

# Still subscribed to other campaigns
manager.is_unsubscribed("user@example.com", "updates")  # False

# Unsubscribe from all
manager.add_unsubscribe("user@example.com", "all")
```

### Bulk Operations

```python
# Bulk add from list
emails = ["user1@example.com", "user2@example.com"]
for email in emails:
    manager.add_unsubscribe(email, "all")

# Bulk check
contacts = [{"email": e} for e in emails]
valid, skipped = manager.filter_contacts(contacts)
```

## 🔄 Migration from Old System

If you have an existing unsubscribe list:

```python
# From CSV
import csv

old_list = []
with open("old_unsubscribes.csv") as f:
    reader = csv.DictReader(f)
    old_list = [row['email'] for row in reader]

# Import
for email in old_list:
    manager.add_unsubscribe(
        email, 
        "all", 
        reason="Migrated from old system",
        source="migration"
    )

print(f"Migrated {len(old_list)} emails")
```

## 📄 Testing

Run the integration test:

```python
python -c "from docx_integration import test_integration; test_integration()"
```

Expected output:
```
🧪 Testing Unsubscribe