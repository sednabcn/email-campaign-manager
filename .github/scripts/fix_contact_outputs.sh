#!/bin/bash
# Fix for contact analysis outputs

set -e  # Exit on error

# Ensure we're in the right directory
cd "$GITHUB_WORKSPACE" || exit 1

echo "Enhanced contact source analysis..."
echo "Working directory: $(pwd)"

CONTACTS_DIR="${CONTACTS_DIR:-contacts}"
CONTACT_SOURCE_FILTER="${CONTACT_SOURCE_FILTER:-}"

# Create the analysis script inline
python3 << 'PYTHON_SCRIPT'
import os
import sys
import json
from pathlib import Path

contacts_dir = Path(os.environ.get('CONTACTS_DIR', 'contacts'))
filter_source = os.environ.get('CONTACT_SOURCE_FILTER', '')

print(f"Analyzing contacts from: {contacts_dir}")
print(f"Contact source filter: {filter_source if filter_source else 'None'}")

# Ensure contacts directory exists
if not contacts_dir.exists():
    print(f"⚠️ Contacts directory does not exist: {contacts_dir}")
    print("Creating empty contacts directory...")
    contacts_dir.mkdir(parents=True, exist_ok=True)
    # Create subdirectories to match structure
    for subdir in ['csv', 'excel', 'docx', 'urls']:
        (contacts_dir / subdir).mkdir(exist_ok=True)

# Load contacts
all_contacts = []
sources = set()
loader_used = 'none'

try:
    sys.path.insert(0, 'utils')
    from data_loader import load_contacts_directory, validate_contact_data
    
    all_contacts = load_contacts_directory(str(contacts_dir))
    if all_contacts:
        stats, all_contacts = validate_contact_data(all_contacts)
        loader_used = 'professional_data_loader'
        print(f"✅ Professional data_loader loaded {len(all_contacts)} contacts")
except Exception as e:
    print(f"Professional data_loader not available: {e}")
    print("Using enhanced fallback loader...")
    loader_used = 'enhanced_fallback_loader'
    
    # Fallback loader
    import csv
    
    # Load from all CSV files in contacts/ and subdirectories
    csv_files = list(contacts_dir.rglob('*.csv'))
    
    for csv_file in csv_files:
        try:
            with open(csv_file, 'r', encoding='utf-8') as f:
                reader = csv.DictReader(f)
                for row in reader:
                    if row.get('email') and '@' in row.get('email', ''):
                        all_contacts.append(dict(row))
                        sources.add(str(csv_file.relative_to(contacts_dir)))
            print(f"Loading CSV: {csv_file.relative_to(contacts_dir)}")
        except Exception as e:
            print(f"⚠️ Error loading {csv_file.name}: {e}")

# Analyze domains
domains = set()
domain_counts = {}

for contact in all_contacts:
    email = contact.get('email', '')
    if '@' in email:
        domain = email.split('@')[1]
        domains.add(domain)
        domain_counts[domain] = domain_counts.get(domain, 0) + 1

# Get top domain
top_domain = max(domain_counts.items(), key=lambda x: x[1])[0] if domain_counts else "none"

# Create analysis data
analysis = {
    'total_contacts': len(all_contacts),
    'sources': len(sources) if sources else len(list(contacts_dir.glob('*.csv'))),
    'unique_domains': len(domains),
    'top_domain': top_domain,
    'loader_used': loader_used,
    'timestamp': '2025-10-14T16:29:16Z',
    'contacts_dir': str(contacts_dir),
    'domain_distribution': domain_counts
}

# CRITICAL: Write JSON file with error handling
try:
    with open('contact_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"\n✅ Successfully created contact_analysis.json")
except Exception as e:
    print(f"\n❌ ERROR writing contact_analysis.json: {e}")
    sys.exit(1)

print(f"\nSuccessfully loaded {len(all_contacts)} contacts using {loader_used}")
print(f"Sources: {analysis['sources']}")
print(f"Domains: {analysis['unique_domains']}")
print(f"Top domain: {top_domain}")

# CRITICAL: Write to GITHUB_OUTPUT with validation
try:
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"count={len(all_contacts)}\n")
        print(f"Set GITHUB_OUTPUT count={len(all_contacts)}")
    else:
        print("⚠️ GITHUB_OUTPUT not set in environment")
except Exception as e:
    print(f"⚠️ Error writing to GITHUB_OUTPUT: {e}")

print(f"\nContact analysis complete:")
print(f"  - Total contacts: {len(all_contacts)}")
print(f"  - Sources: {analysis['sources']}")
print(f"  - Domains: {analysis['unique_domains']}")
print(f"  - Top domain: {top_domain}")

PYTHON_SCRIPT

# Verify JSON was created
if [ ! -f "contact_analysis.json" ]; then
  echo "❌ ERROR: contact_analysis.json not created"
  # Set safe default
  {
    echo "count=0"
    echo "status=error"
    echo "message=Analysis failed"
  } >> "$GITHUB_OUTPUT"
  exit 1
fi

# Extract count with comprehensive error handling
COUNT=$(python3 -c "
import json
import sys
try:
    with open('contact_analysis.json') as f:
        data = json.load(f)
    count = data.get('total_contacts', 0)
    # Ensure it's an integer
    print(int(count))
except Exception as e:
    print(f'Error reading JSON: {e}', file=sys.stderr)
    print(0)
" 2>&1 | tail -1)

# Validate COUNT is a number
if ! [[ "$COUNT" =~ ^[0-9]+$ ]]; then
  echo "⚠️ WARNING: Invalid count '$COUNT', defaulting to 0"
  COUNT=0
fi

# Verify the output was set
echo "✅ contact_analysis.json verified"
echo "Contact count: $COUNT"

# Display sample of JSON
echo ""
echo "Sample of contact_analysis.json:"
head -10 contact_analysis.json || echo "Could not display JSON sample"

echo ""
echo "Contact count set to: $COUNT"
