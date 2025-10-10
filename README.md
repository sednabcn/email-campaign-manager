# Services - Email Campaign Management System

A comprehensive email campaign management system with personalization, tracking, and compliance features for managing outreach across multiple sectors.

## 📋 Overview

This repository provides a complete solution for managing personalized email campaigns with built-in tracking, compliance checking, and response handling. It supports multiple industry sectors including education, finance, and healthcare.

## 🌟 Key Features

- **Multi-Sector Campaign Management**: Pre-configured templates for education, finance, and healthcare sectors
- **Email Personalization**: Dynamic content replacement using contact data
- **Compliance Checking**: Built-in validation against regulatory requirements
- **Campaign Tracking**: Comprehensive analytics and response monitoring
- **Unsubscribe Management**: Automated handling of opt-out requests
- **DOCX Template Processing**: Parse and personalize Microsoft Word templates
- **Rate Limiting**: Smart throttling to prevent email service overload
- **GitHub Integration**: Automated notifications and workflow management

## 📁 Project Structure

```
services/
├── campaign-templates/       # Email templates by sector
│   ├── education/           # Education sector templates
│   ├── finance/            # Finance sector templates
│   └── healthcare/         # Healthcare sector templates
├── contact-details/         # Organized contact information
├── contacts/               # CSV contact databases
├── scheduled-campaigns/    # Campaign configurations
├── tracking/              # Campaign analytics and responses
├── utils/                 # Core utilities and tools
└── debug/                 # Debugging and diagnostics
```

## 🚀 Getting Started

### Prerequisites

- Python 3.13+
- SMTP server credentials
- Microsoft Word (.docx) template files

### Installation

1. Clone the repository:
```bash
git clone https://github.com/sednabcn/services.git
cd services
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Configure compliance settings:
```bash
# Edit compliance_config.json with your regulatory requirements
```

### Configuration

Create or modify `compliance_config.json` to set your compliance rules, SMTP settings, and campaign parameters.

## 💡 Usage

### Running a Campaign

```bash
# Use the integrated runner for complete campaign execution
python utils/integrated_runner.py

# Or use the email campaign system directly
python utils/email_campaign_system.py
```

### Creating Templates

1. Place your `.docx` template in the appropriate sector folder under `campaign-templates/`
2. Use placeholder syntax: `{{FirstName}}`, `{{Company}}`, etc.
3. Run the validator to check template compliance:
```bash
python utils/campaign_validator.py
```

### Managing Contacts

1. Add contacts to CSV files in the `contacts/` directory
2. Organize sector-specific contacts in `contact-details/`
3. Validate contact data:
```bash
python utils/contact_validator.py
```

### Tracking Campaigns

Campaign data is automatically tracked in `tracking/default/`:
- `campaigns/` - Campaign metadata and configurations
- `analytics/` - Performance metrics
- `responses/` - Reply tracking
- `unsubscribed.json` - Opt-out list

## 🛠️ Core Utilities

### Email Processing
- `email_personalizer.py` - Personalize email content
- `email_sender.py` - Send emails with rate limiting
- `reply_handler.py` - Process incoming replies
- `unsubscribe_manager.py` - Handle opt-out requests

### Document Processing
- `docx_parser.py` - Parse Word documents with compliance
- `docx_validator.py` - Validate document structure
- `fix_corrupted_docx.py` - Repair damaged Word files

### Campaign Management
- `campaign_summary.py` - Generate campaign reports
- `campaign_diagnostics.py` - Troubleshoot issues
- `smart_rate_limit.py` - Intelligent email throttling

### Integration
- `github_adapter.py` - GitHub API integration
- `github_notifier.py` - Automated GitHub notifications

## 📊 Tracking & Analytics

The system automatically tracks:
- Email delivery status
- Open rates and engagement
- Response handling
- Unsubscribe requests
- Campaign performance metrics

Access analytics in `tracking/default/analytics/`

## 🔒 Compliance

Built-in compliance features:
- GDPR consent validation
- CAN-SPAM compliance checking
- Unsubscribe link enforcement
- Data protection validation

Configure compliance rules in `compliance_config.json`

## 🐛 Debugging

Diagnostic tools available in `utils/`:
- `campaign_diagnostics.py` - Full system diagnostics
- `docx_diagnostic.py` - Document parsing issues
- `test-smtp-local.py` - SMTP configuration testing
- `find_substitution_bug.py` - Template variable issues

## 📝 Campaign Templates

Pre-built templates for:
- **Education**: Adult education institutions, universities
- **Finance**: Banks and financial services
- **Healthcare**: Medical facilities and providers

Each sector includes customized outreach templates with appropriate tone and compliance.

## 🔄 Automated Workflows

GitHub Actions workflows included for:
- Cleanup of old workflow runs
- Daily CSV file cleaning
- Enhanced email campaign production
- Automated testing and validation

## 📄 License

See [LICENSE](LICENSE) file for details.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request

## 📞 Support

For issues and questions:
- Check the debug logs in `log.txt`
- Review campaign diagnostics
- Consult the compliance configuration

## ⚠️ Important Notes

- Always test campaigns with small batches first
- Maintain an up-to-date suppression list
- Respect unsubscribe requests immediately
- Follow all applicable email marketing regulations
- Backup contact data regularly

## 🔧 Maintenance

Regular maintenance tasks:
- Clean old campaign data with `cleanup_duplicates.py`
- Validate contact lists periodically
- Update compliance rules as regulations change
- Monitor rate limits and adjust as needed
- Review and archive old campaigns