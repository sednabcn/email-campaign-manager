#!/bin/bash
# Fix for domain analysis outputs

cd "$GITHUB_WORKSPACE"

# Run analysis
python .github/scripts/analyze_domains.py

# Verify JSON was created
if [ ! -f "domain_analysis.json" ]; then
  echo "ERROR: domain_analysis.json not created"
  {
    echo "campaigns=0"
    echo "status=error"
  } >> "$GITHUB_OUTPUT"
  exit 0
fi

# Extract campaign count with error handling
CAMPAIGNS=$(python3 -c "
import json
import sys
try:
    with open('domain_analysis.json') as f:
        data = json.load(f)
    count = data.get('template_count', 0)
    print(int(count))
except Exception as e:
    print(f'Error: {e}', file=sys.stderr)
    print(0)
" 2>&1)

# Validate CAMPAIGNS is a number
if ! [[ "$CAMPAIGNS" =~ ^[0-9]+$ ]]; then
  echo "WARNING: Invalid campaigns '$CAMPAIGNS', defaulting to 0"
  CAMPAIGNS=0
fi

# Write outputs
{
  echo "campaigns=${CAMPAIGNS}"
  echo "status=success"
} >> "$GITHUB_OUTPUT"

echo "Template count set to: $CAMPAIGNS"
