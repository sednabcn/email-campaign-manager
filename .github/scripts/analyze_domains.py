#!/usr/bin/env python3
"""
Enhanced domain and template analysis script
Analyzes campaign templates across different domains and formats
"""

import os
import sys
import json
from pathlib import Path
import re
from datetime import datetime

def analyze_domains(templates_dir='campaign-templates', scheduled_dir='scheduled-campaigns', domain_filter=None):
    """
    Analyze domain structure and count templates
    
    Args:
        templates_dir: Path to templates directory
        scheduled_dir: Path to scheduled campaigns directory
        domain_filter: Optional domain to filter analysis
    
    Returns:
        dict: Analysis results
    """
    templates_path = Path(templates_dir)
    scheduled_path = Path(scheduled_dir)
    
    # Ensure directories exist
    templates_path.mkdir(parents=True, exist_ok=True)
    scheduled_path.mkdir(parents=True, exist_ok=True)
    
    # Define domains
    domains = ['education', 'finance', 'healthcare', 'industry', 'technology', 'government']
    
    total_templates = 0
    domain_data = {}
    
    print(f"Analyzing templates in: {templates_path}")
    
    for domain in domains:
        # Skip if filter is set and doesn't match
        if domain_filter and domain != domain_filter:
            continue
        
        domain_path = templates_path / domain
        
        if not domain_path.exists():
            domain_path.mkdir(parents=True, exist_ok=True)
        
        # Count different file types
        docx_files = list(domain_path.glob('**/*.docx'))
        json_files = list(domain_path.glob('**/*.json'))
        txt_files = list(domain_path.glob('**/*.txt'))
        html_files = list(domain_path.glob('**/*.html'))
        md_files = list(domain_path.glob('**/*.md'))
        
        all_files = docx_files + json_files + txt_files + html_files + md_files
        domain_total = len(all_files)
        total_templates += domain_total
        
        domain_data[domain] = {
            'total': domain_total,
            'docx': len(docx_files),
            'json': len(json_files),
            'txt': len(txt_files),
            'html': len(html_files),
            'md': len(md_files),
            'files': [f.name for f in all_files],
            'subdirectories': [d.name for d in domain_path.iterdir() if d.is_dir() and not d.name.startswith('.')]
        }
        
        print(f"  {domain}: {domain_total} templates")
    
    # Analyze scheduled campaigns
    scheduled_files = []
    for pattern in ['*.txt', '*.json', '*.html', '*.md', '*.docx']:
        scheduled_files.extend(list(scheduled_path.glob(pattern)))
    
    scheduled_count = len(scheduled_files)
    print(f"\nScheduled campaigns: {scheduled_count}")
    
    # Detect template variables
    template_vars = {}
    variable_pattern = re.compile(r'\{\{([^}]+)\}\}')
    
    for scheduled_file in scheduled_path.glob('*.txt'):
        try:
            content = scheduled_file.read_text(encoding='utf-8')
            vars_found = variable_pattern.findall(content)
            if vars_found:
                unique_vars = list(set(vars_found))[:5]
                template_vars[scheduled_file.name] = unique_vars
        except Exception as e:
            print(f"Warning: Could not read {scheduled_file.name}: {e}")
    
    # Create analysis result
    analysis = {
        'template_count': total_templates,
        'scheduled_count': scheduled_count,
        'domains': domain_data,
        'template_variables': template_vars,
        'scheduled_files': [f.name for f in scheduled_files],
        'templates_dir': str(templates_path),
        'scheduled_dir': str(scheduled_path),
        'domain_filter': domain_filter or 'none',
        'timestamp': datetime.now().isoformat()
    }
    
    return analysis

def main():
    """Main execution function"""
    templates_dir = os.environ.get('TEMPLATES_DIR', 'campaign-templates')
    scheduled_dir = os.environ.get('SCHEDULED_DIR', 'scheduled-campaigns')
    domain_filter = os.environ.get('TARGET_DOMAIN_FILTER', None)
    
    print("=" * 70)
    print("DOMAIN AND TEMPLATE ANALYSIS")
    print("=" * 70)
    print()
    
    try:
        analysis = analyze_domains(templates_dir, scheduled_dir, domain_filter)
        
        # Write JSON output
        output_file = 'domain_analysis.json'
        with open(output_file, 'w') as f:
            json.dump(analysis, f, indent=2)
        
        print()
        print(f"✅ Analysis complete")
        print(f"   Total templates: {analysis['template_count']}")
        print(f"   Scheduled campaigns: {analysis['scheduled_count']}")
        print(f"   Output written to: {output_file}")
        
        # Write to GITHUB_OUTPUT if available
        github_output = os.environ.get('GITHUB_OUTPUT')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f"campaigns={analysis['template_count']}\n")
                f.write(f"scheduled={analysis['scheduled_count']}\n")
        
        return 0
        
    except Exception as e:
        print(f"❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
        return 1

if __name__ == '__main__':
    sys.exit(main())
