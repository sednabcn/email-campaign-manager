#!/bin/bash
# Fix for contact analysis outputs

# Ensure we're in the right directory
cd "$GITHUB_WORKSPACE"

# Run analysis
python .github/scripts/analyze_contacts.py

# Verify JSON was created
if [ ! -f "contact_analysis.json" ]; then
  echo "ERROR: contact_analysis.json not created"
  # Set safe default
  {
    echo "count=0"
    echo "status=error"
    echo "message=Analysis failed"
  } >> "$GITHUB_OUTPUT"
  exit 0
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
" 2>&1)

# Validate COUNT is a number
if ! [[ "$COUNT" =~ ^[0-9]+$ ]]; then
  echo "WARNING: Invalid count '$COUNT', defaulting to 0"
  COUNT=0
fi

# Write outputs in correct format
{
  echo "count=${COUNT}"
  echo "status=success"
} >> "$GITHUB_OUTPUT"

echo "Contact count set to: $COUNT"
