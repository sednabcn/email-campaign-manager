#!/bin/bash
# Test script to diagnose why outputs are 0

echo "Testing GitHub Actions Scripts"
echo "==============================="

# Set environment
export CONTACTS_DIR=contacts
export TEMPLATES_DIR=campaign-templates
export SCHEDULED_DIR=scheduled-campaigns

echo ""
echo "1. Testing analyze_contacts.py"
echo "--------------------------------"
python .github/scripts/analyze_contacts.py
if [ -f "contact_analysis.json" ]; then
    echo "✅ contact_analysis.json created"
    cat contact_analysis.json | python3 -m json.tool
    COUNT=$(python3 -c "import json; print(json.load(open('contact_analysis.json')).get('total_contacts', 0))")
    echo "Total contacts found: $COUNT"
else
    echo "❌ contact_analysis.json NOT created"
fi

echo ""
echo "2. Testing analyze_domains.py"
echo "--------------------------------"
python .github/scripts/analyze_domains.py
if [ -f "domain_analysis.json" ]; then
    echo "✅ domain_analysis.json created"
    cat domain_analysis.json | python3 -m json.tool
    TEMPLATES=$(python3 -c "import json; print(json.load(open('domain_analysis.json')).get('template_count', 0))")
    echo "Total templates found: $TEMPLATES"
else
    echo "❌ domain_analysis.json NOT created"
fi

echo ""
echo "3. Testing diagnose_data.py"
echo "--------------------------------"
python .github/scripts/diagnose_data.py

echo ""
echo "4. Checking directory structure"
echo "--------------------------------"
echo "Contacts directory:"
ls -lh contacts/ | head -10

echo ""
echo "Templates directory:"
ls -lh campaign-templates/education/adult_education/ 2>/dev/null || echo "Path not found"

echo ""
echo "5. Manual contact count"
echo "--------------------------------"
echo "CSV files in contacts/:"
find contacts -name "*.csv" -type f | wc -l

echo ""
echo "Manual row count from first CSV:"
CSV_FILE=$(find contacts -name "*.csv" -type f | head -1)
if [ -n "$CSV_FILE" ]; then
    echo "File: $CSV_FILE"
    wc -l "$CSV_FILE"
    head -3 "$CSV_FILE"
fi
