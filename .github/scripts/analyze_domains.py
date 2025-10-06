#!/usr/bin/env python3
"""
Enhanced campaign template and domain analysis script for GitHub Actions workflow.
"""

import sys
import json
import os
import re
from pathlib import Path
from datetime import datetime


def analyze_templates(templates_dir, scheduled_dir, target_domain_filter='all_domains'):
    """Analyze campaign templates across domains."""
    
    # Enhanced template analysis
    domains = ['education', 'finance', 'healthcare', 'industry', 'technology', 'government']
    domain_stats = {}
    total_templates = 0

    templates_path = Path(templates_dir)
    scheduled_path = Path(scheduled_dir)

    print('Analyzing enhanced template structure...')

    # Check domain-based structure
    for domain in domains:
        domain_path = templates_path / domain
        if domain_path.exists():
            # Enhanced file type detection
            docx_files = list(domain_path.glob('*.docx'))
            doc_files = list(domain_path.glob('*.doc'))
            json_files = list(domain_path.glob('*.json'))
            txt_files = list(domain_path.glob('*.txt'))
            html_files = list(domain_path.glob('*.html'))
            md_files = list(domain_path.glob('*.md'))
            
            all_templates = docx_files + doc_files + json_files + txt_files + html_files + md_files

            domain_stats[domain] = {
                'template_count': len(all_templates),
                'docx_count': len(docx_files),
                'json_count': len(json_files),
                'txt_count': len(txt_files),
                'html_count': len(html_files),
                'md_count': len(md_files),
                'other_count': len(doc_files),
                'templates': [t.name for t in all_templates]
            }
            total_templates += len(all_templates)
            print(f'  - {domain}: {len(all_templates)} templates '
                  f'({len(docx_files)} DOCX, {len(json_files)} JSON, '
                  f'{len(txt_files)} TXT, {len(html_files)} HTML)')
        else:
            domain_stats[domain] = {
                'template_count': 0,
                'docx_count': 0,
                'json_count': 0,
                'txt_count': 0,
                'html_count': 0,
                'md_count': 0,
                'other_count': 0,
                'templates': []
            }

    # Enhanced scheduled campaign analysis
    scheduled_campaigns = 0
    scheduled_by_type = {}
    if scheduled_path.exists():
        for ext in ['*.json', '*.docx', '*.txt', '*.html', '*.md']:
            files = list(scheduled_path.glob(ext))
            scheduled_by_type[ext[2:]] = len(files)  # Remove *.
            scheduled_campaigns += len(files)

    # Enhanced template content analysis
    template_variables_found = {}
    if scheduled_path.exists():
        for template_file in scheduled_path.iterdir():
            if template_file.suffix in ['.txt', '.json', '.html', '.md']:
                try:
                    content = template_file.read_text()
                    # Look for template variables like {{Contact Name}}
                    variables = re.findall(r'{{([^}]+)}}', content)
                    if variables:
                        template_variables_found[template_file.name] = variables
                except Exception as e:
                    print(f'Could not analyze template {template_file.name}: {e}')

    # Create enhanced analysis
    domain_analysis = {
        'domain_count': len([d for d in domain_stats.values() if d['template_count'] > 0]),
        'template_count': total_templates,
        'scheduled_campaigns': scheduled_campaigns,
        'scheduled_by_type': scheduled_by_type,
        'template_variables_found': template_variables_found,
        'domains': domain_stats,
        'analysis_method': 'enhanced_filesystem_scan',
        'analysis_timestamp': datetime.now().isoformat(),
        'target_domain_filter': target_domain_filter
    }

    return domain_analysis, total_templates, scheduled_campaigns, template_variables_found


def main():
    """Main execution function."""
    templates_dir = os.environ.get('TEMPLATES_DIR', 'campaign-templates')
    scheduled_dir = os.environ.get('SCHEDULED_DIR', 'scheduled-campaigns')
    target_domain_filter = os.environ.get('TARGET_DOMAIN_FILTER', 'all_domains')

    try:
        domain_analysis, total_templates, scheduled_campaigns, template_variables_found = \
            analyze_templates(templates_dir, scheduled_dir, target_domain_filter)

        # Save analysis to file
        with open('domain_analysis.json', 'w') as f:
            json.dump(domain_analysis, f, indent=2)

        # CRITICAL: Write output to GITHUB_OUTPUT
        github_output = os.environ.get('GITHUB_OUTPUT', '')
        if github_output:
            with open(github_output, 'a') as f:
                f.write(f'campaigns={total_templates}\n')
            print(f'Set GITHUB_OUTPUT campaigns={total_templates}')
        else:
            print('WARNING: GITHUB_OUTPUT environment variable not set!')
            print(f'Template count: {total_templates}')
        
        print(f'Enhanced template analysis completed: {total_templates} templates, '
              f'{scheduled_campaigns} scheduled campaigns')
        
        if template_variables_found:
            print('Template variables detected in:')
            for template, vars in template_variables_found.items():
                if len(vars) > 3:
                    print(f'  - {template}: {vars[:3]}...')
                else:
                    print(f'  - {template}: {vars}')
        
        return 0

    except Exception as e:
        print(f'Error in domain analysis: {e}')
        import traceback
        traceback.print_exc()
        return 1


if __name__ == '__main__':
    sys.exit(main())
