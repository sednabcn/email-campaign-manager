#!/bin/bash
# Fix for domain analysis outputs

set -e  # Exit on error

# Ensure we're in the right directory
cd "$GITHUB_WORKSPACE" || exit 1

echo "Enhanced campaign template and domain analysis..."
echo "Working directory: $(pwd)"

TEMPLATES_DIR="${TEMPLATES_DIR:-campaign-templates}"
SCHEDULED_DIR="${SCHEDULED_DIR:-scheduled-campaigns}"
TARGET_DOMAIN_FILTER="${TARGET_DOMAIN_FILTER:-}"

# Create the analysis script inline
python3 << 'PYTHON_SCRIPT'
import os
import sys
import json
from pathlib import Path
import re

templates_dir = Path(os.environ.get('TEMPLATES_DIR', 'campaign-templates'))
scheduled_dir = Path(os.environ.get('SCHEDULED_DIR', 'scheduled-campaigns'))
target_filter = os.environ.get('TARGET_DOMAIN_FILTER', '')

print(f"Analyzing templates from: {templates_dir}")
print(f"Analyzing scheduled from: {scheduled_dir}")
print(f"Domain filter: {target_filter if target_filter else 'None'}")

# Ensure directories exist
if not templates_dir.exists():
    print(f"⚠️ Templates directory does not exist: {templates_dir}")
    print("Creating templates directory structure...")
    templates_dir.mkdir(parents=True, exist_ok=True)
    for domain in ['education', 'finance', 'healthcare', 'industry', 'technology', 'government']:
        (templates_dir / domain).mkdir(exist_ok=True)

if not scheduled_dir.exists():
    print(f"⚠️ Scheduled directory does not exist: {scheduled_dir}")
    scheduled_dir.mkdir(parents=True, exist_ok=True)

# Define domains to analyze
domains = ['education', 'finance', 'healthcare', 'industry', 'technology', 'government']
total_templates = 0
domain_data = {}

print("\nAnalyzing enhanced template structure...")

for domain in domains:
    # Skip if domain filter is set and doesn't match
    if target_filter and domain != target_filter:
        continue
    
    domain_path = templates_dir / domain
    
    if domain_path.exists():
        # Count different file types
        docx_files = list(domain_path.glob('**/*.docx'))
        json_files = list(domain_path.glob('**/*.json'))
        txt_files = list(domain_path.glob('**/*.txt'))
        html_files = list(domain_path.glob('**/*.html'))
        md_files = list(domain_path.glob('**/*.md'))
        
        domain_total = len(docx_files) + len(json_files) + len(txt_files) + len(html_files) + len(md_files)
        total_templates += domain_total
        
        domain_data[domain] = {
            'total': domain_total,
            'docx': len(docx_files),
            'json': len(json_files),
            'txt': len(txt_files),
            'html': len(html_files),
            'md': len(md_files),
            'files': [f.name for f in (docx_files + json_files + txt_files + html_files + md_files)]
        }
        
        print(f"  - {domain}: {domain_total} templates ({len(docx_files)} DOCX, {len(json_files)} JSON, {len(txt_files)} TXT, {len(html_files)} HTML, {len(md_files)} MD)")
        
        # Show subdirectories if any
        subdirs = [d.name for d in domain_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        if subdirs:
            print(f"    Subdirectories: {', '.join(subdirs)}")
    else:
        domain_data[domain] = {
            'total': 0,
            'docx': 0,
            'json': 0,
            'txt': 0,
            'html': 0,
            'md': 0,
            'files': []
        }
        print(f"  - {domain}: 0 templates (directory not found)")

# Count scheduled campaigns
scheduled_count = 0
scheduled_files = []

if scheduled_dir.exists():
    for ext in ['*.txt', '*.json', '*.html', '*.md', '*.docx']:
        scheduled_files.extend(list(scheduled_dir.glob(ext)))
    scheduled_count = len(scheduled_files)
    print(f"\nScheduled campaigns: {scheduled_count}")
    for f in scheduled_files[:5]:  # Show first 5
        print(f"  - {f.name}")
    if scheduled_count > 5:
        print(f"  ... and {scheduled_count - 5} more")

# Detect template variables in scheduled campaigns
template_vars = {}
variable_pattern = re.compile(r'\{\{([^}]+)\}\}')

for scheduled_file in scheduled_dir.glob('*.txt'):
    try:
        content = scheduled_file.read_text(encoding='utf-8')
        vars_found = variable_pattern.findall(content)
        if vars_found:
            # Get unique variables
            unique_vars = list(set(vars_found))[:5]  # First 5 unique
            template_vars[scheduled_file.name] = unique_vars
    except Exception as e:
        print(f"⚠️ Could not read {scheduled_file.name}: {e}")

# Create comprehensive analysis data
analysis = {
    'template_count': total_templates,
    'scheduled_count': scheduled_count,
    'domains': domain_data,
    'template_variables': template_vars,
    'scheduled_files': [f.name for f in scheduled_files],
    'templates_dir': str(templates_dir),
    'scheduled_dir': str(scheduled_dir),
    'domain_filter': target_filter if target_filter else 'none',
    'timestamp': '2025-10-14T16:29:16Z'
}

# CRITICAL: Write JSON file with error handling
try:
    with open('domain_analysis.json', 'w') as f:
        json.dump(analysis, f, indent=2)
    print(f"\n✅ Successfully created domain_analysis.json")
except Exception as e:
    print(f"\n❌ ERROR writing domain_analysis.json: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)

print(f"\nTemplate analysis summary:")
print(f"  - Total templates: {total_templates}")
print(f"  - Scheduled campaigns: {scheduled_count}")
print(f"  - Domains analyzed: {len([d for d in domain_data if domain_data[d]['total'] > 0])}")

# CRITICAL: Write to GITHUB_OUTPUT with validation
try:
    github_output = os.environ.get('GITHUB_OUTPUT')
    if github_output:
        with open(github_output, 'a') as f:
            f.write(f"campaigns={total_templates}\n")
        print(f"Set GITHUB_OUTPUT campaigns={total_templates}")
    else:
        print("⚠️ GITHUB_OUTPUT not set in environment")
except Exception as e:
    print(f"⚠️ Error writing to GITHUB_OUTPUT: {e}")

if template_vars:
    print(f"\nTemplate variables detected in {len(template_vars)} files:")
    for filename, vars_list in list(template_vars.items())[:3]:
        print(f"  - {filename}: {vars_list}")
    if len(template_vars) > 3:
        print(f"  ... and {len(template_vars) - 3} more files with variables")

print(f"\nEnhanced template analysis completed")

PYTHON_SCRIPT

# Verify JSON was created
if [ ! -f "domain_analysis.json" ]; then
  echo "❌ ERROR: domain_analysis.json not created"
  {
    echo "campaigns=0"
    echo "status=error"
    echo "message=Analysis failed"
  } >> "$GITHUB_OUTPUT"
  exit 1
fi

# Extract campaign count with comprehensive error handling
CAMPAIGNS=$(python3 -c "
import json
import sys
try:
    with open('domain_analysis.json') as f:
        data = json.load(f)
    count = data.get('template_count', 0)
    # Ensure it's an integer
    print(int(count))
except Exception as e:
    print(f'Error reading JSON: {e}', file=sys.stderr)
    print(0)
" 2>&1 | tail -1)

# Validate CAMPAIGNS is a number
if ! [[ "$CAMPAIGNS" =~ ^[0-9]+$ ]]; then
  echo "⚠️ WARNING: Invalid campaigns '$CAMPAIGNS', defaulting to 0"
  CAMPAIGNS=0
fi

# Verify the output was set
echo "✅ domain_analysis.json verified"
echo "Template count: $CAMPAIGNS"

# Display sample of JSON
echo ""
echo "Sample of domain_analysis.json:"
python3 -c "
import json
try:
    with open('domain_analysis.json') as f:
        data = json.load(f)
    print(f\"  Total templates: {data.get('template_count', 0)}\")
    print(f\"  Scheduled campaigns: {data.get('scheduled_count', 0)}\")
    print(f\"  Domains with templates: {len([d for d, v in data.get('domains', {}).items() if v.get('total', 0) > 0])}\")
    
    # Show domain breakdown
    domains = data.get('domains', {})
    for domain, info in domains.items():
        if info.get('total', 0) > 0:
            print(f\"    - {domain}: {info['total']} templates\")
except Exception as e:
    print(f'Could not display JSON sample: {e}')
"

echo ""
echo "Template count set to: $CAMPAIGNS"
