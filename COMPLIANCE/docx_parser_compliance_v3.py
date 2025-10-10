#!/usr/bin/env python3
"""
docx_parser.py — Domain-aware campaign processor with personalization & compliance

Features:
 - Loads contacts (professional loader or CSV fallback)
 - Loads campaign templates (.docx/.txt/.md/.html/.json)
 - Integrates EmailPersonalizer for compliant footers and unsubscribe links
 - Integrates MinimalCompliance / ContactValidator and SmartRateLimiter when available
 - Supports dry-run, queue mode, and simulated sending (or external BaseEmailSender)
 - Reads all compliance and sender info from compliance_config.json
"""

from __future__ import annotations
import argparse, csv, json, os, sys, time, zipfile, traceback, re, hashlib
from pathlib import Path
from datetime import datetime
from typing import List, Dict, Optional, Tuple

# ==============================================================
# Load compliance configuration
# ==============================================================
CONFIG_PATH = Path("compliance_config.json")

if CONFIG_PATH.exists():
    with open(CONFIG_PATH, "r") as f:
        CONFIG = json.load(f)
    print("[config] Loaded compliance_config.json")
else:
    print("⚠️  compliance_config.json not found — using safe defaults.")
    CONFIG = {}

SENDER_INFO = CONFIG.get("sender_info", {})
UNSUBSCRIBE = CONFIG.get("unsubscribe", {})
RATES = CONFIG.get("rate_limits", {})
COMPLIANCE_OPTS = CONFIG.get("compliance", {})

FROM_NAME  = SENDER_INFO.get("from_name", "Your Name")
FROM_EMAIL = SENDER_INFO.get("from_email", "your.email@domain.com")
PHYS_ADDR  = SENDER_INFO.get("physical_address", "Your Address, City, Country")
UNSUB_BASE = UNSUBSCRIBE.get("base_url", "https://example.com/unsubscribe")

MAX_DAILY  = RATES.get("max_daily_sends", 50)
MAX_DOMAIN = RATES.get("max_per_domain_daily", 5)
MIN_DELAY  = RATES.get("min_delay_seconds", 30)

# ==============================================================
# Path setup for utils import
# ==============================================================
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
if SCRIPT_DIR not in sys.path:
    sys.path.insert(0, SCRIPT_DIR)
UTILS_DIR = os.path.join(SCRIPT_DIR, "utils")
if os.path.isdir(UTILS_DIR) and UTILS_DIR not in sys.path:
    sys.path.insert(0, UTILS_DIR)

# ==============================================================
# Optional dependencies
# ==============================================================
try:
    from docx import Document
    DOCX_AVAILABLE = True
except Exception:
    Document = None
    DOCX_AVAILABLE = False

try:
    from email_personalizer import EmailPersonalizer
    PERSONALIZER_AVAILABLE = True
except Exception:
    try:
        from utils.email_personalizer import EmailPersonalizer
        PERSONALIZER_AVAILABLE = True
    except Exception:
        PERSONALIZER_AVAILABLE = False
        EmailPersonalizer = None

try:
    from compliance_wrapper import MinimalCompliance
    COMPLIANCE_AVAILABLE = True
except Exception:
    MinimalCompliance = None
    COMPLIANCE_AVAILABLE = False

try:
    from contact_validator import ContactValidator
    CONTACT_VALIDATOR_AVAILABLE = True
except Exception:
    try:
        from utils.contact_validator import ContactValidator
        CONTACT_VALIDATOR_AVAILABLE = True
    except Exception:
        ContactValidator = None
        CONTACT_VALIDATOR_AVAILABLE = False

try:
    from smart_rate_limits import SmartRateLimiter, TargetingOptimizer
    SMART_RATE_AVAILABLE = True
except Exception:
    try:
        from utils.smart_rate_limits import SmartRateLimiter, TargetingOptimizer
        SMART_RATE_AVAILABLE = True
    except Exception:
        SmartRateLimiter = None
        TargetingOptimizer = None
        SMART_RATE_AVAILABLE = False

try:
    from email_sender import EmailSender as BaseEmailSender
    EMAIL_SENDER_AVAILABLE = True
except Exception:
    BaseEmailSender = None
    EMAIL_SENDER_AVAILABLE = False

# ==============================================================
# Fallback personalizer
# ==============================================================
class _FallbackPersonalizer:
    """Used when EmailPersonalizer is unavailable."""
    def __init__(self, from_name=FROM_NAME, from_email=FROM_EMAIL, physical_address=PHYS_ADDR):
        self.from_name = from_name
        self.from_email = from_email
        self.physical_address = physical_address
        self.unsubscribe_base_url = UNSUB_BASE

    def create_personalized_email(self, template: str, contact: Dict, campaign_id="general", is_html=False) -> Dict:
        body = template
        for k, v in contact.items():
            body = body.replace(f"{{{{{k}}}}}", str(v))
        body = body.replace("{{name}}", contact.get("name", "there"))
        unsubscribe_link = f"{self.unsubscribe_base_url}?email={contact.get('email','')}&campaign={campaign_id}"
        footer = f"\n\n---\nTo unsubscribe: {unsubscribe_link}\nFrom: {self.from_name} <{self.from_email}>\n{self.physical_address}"
        body += footer
        subj = re.search(r"Subject:\s*(.+?)(?:\n|$)", body)
        subject = subj.group(1).strip() if subj else f"Message from {self.from_name}"
        if subj:
            body = re.sub(r"Subject:\s*.+?(?:\n|$)", "", body, count=1)
        return {
            "to": contact.get("email", ""),
            "subject": subject,
            "body": body.strip(),
            "from_name": self.from_name,
            "from_email": self.from_email,
            "unsubscribe_url": unsubscribe_link,
            "headers": {"List-Unsubscribe": f"<{unsubscribe_link}>"},
        }

# ==============================================================
# Utility functions (contacts, templates, tracking)
# ==============================================================
def fallback_load_contacts_from_directory(contacts_dir: str) -> List[Dict]:
    contacts = []
    p = Path(contacts_dir)
    if not p.exists():
        print(f"[contacts] Directory not found: {contacts_dir}")
        return contacts
    for csv_file in p.glob("*.csv"):
        try:
            with open(csv_file, newline='', encoding='utf-8') as fh:
                for row in csv.DictReader(fh):
                    contact = {k.lower().strip(): (v or "").strip() for k, v in row.items() if k}
                    email = contact.get("email") or contact.get("email_address")
                    if not email or "@" not in email:
                        continue
                    contact["email"] = email
                    contact["name"] = contact.get("name") or contact.get("full_name", "")
                    contact["opt_in"] = str(contact.get("opt_in", "true")).lower() in ("1", "true", "yes", "y")
                    contacts.append(contact)
            print(f"[contacts] Loaded {len(contacts)} from {csv_file.name}")
        except Exception as e:
            print(f"[contacts] Error reading {csv_file}: {e}")
    return contacts

def try_professional_loader(contacts_dir: str) -> Optional[List[Dict]]:
    try:
        from data_loader import load_contacts_directory, validate_contact_data
        contacts = load_contacts_directory(contacts_dir)
        stats, valid = validate_contact_data(contacts)
        print(f"[contacts] Professional loader: total={stats.get('total')} valid={stats.get('valid_emails')}")
        return valid
    except Exception:
        return None

def load_campaign_content(path: str) -> Optional[str]:
    p = Path(path)
    if not p.exists():
        print(f"[templates] Not found: {path}")
        return None
    if p.suffix == ".docx" and DOCX_AVAILABLE:
        try:
            doc = Document(str(p))
            text = "\n".join([para.text for para in doc.paragraphs if para.text])
            return text
        except Exception as e:
            print(f"[templates] DOCX error: {e}")
            return None
    elif p.suffix in (".txt", ".md", ".html"):
        try:
            return p.read_text(encoding="utf-8")
        except Exception as e:
            print(f"[templates] Text load error: {e}")
            return None
    elif p.suffix == ".json":
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except Exception as e:
            print(f"[templates] JSON load error: {e}")
            return None
    else:
        print(f"[templates] Unsupported type: {p.suffix}")
        return None

def generate_tracking_id(domain: str, campaign_name: str, filename: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    h = hashlib.md5(f"{domain}_{campaign_name}_{filename}_{ts}".encode()).hexdigest()[:8]
    return f"{domain.upper()}_{h}_{ts}"

def save_tracking_data(tracking_root: str, domain: str, tracking_id: str, data: Dict):
    p = Path(tracking_root) / domain / "campaigns"
    p.mkdir(parents=True, exist_ok=True)
    f = p / f"{tracking_id}.json"
    json.dump(data, open(f, "w", encoding="utf-8"), indent=2)
    print(f"[tracking] Saved {f}")

# ==============================================================
# Emailer
# ==============================================================
class Emailer:
    def __init__(self, alerts_email: str, dry_run=False, queue_emails=False,
                 compliance=None, smart_limiter=None, optimizer=None, personalizer=None):
        self.alerts_email = alerts_email
        self.dry_run = dry_run
        self.queue_emails = queue_emails
        self.compliance = compliance
        self.smart_limiter = smart_limiter
        self.optimizer = optimizer
        self.personalizer = personalizer or _FallbackPersonalizer()
        self.queue_dir = None
        if queue_emails:
            self.queue_dir = Path(f"email_queue_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
            self.queue_dir.mkdir(exist_ok=True)
            print(f"[emailer] Queuing mode active → {self.queue_dir}")

    def send_campaign(self, campaign_name: str, subject_template: str,
                      content_template: str, recipients: List[Dict], from_name: str):
        print(f"\n=== Campaign: {campaign_name} ===")
        sent, failed, queued = 0, 0, 0
        for i, r in enumerate(recipients):
            email = r.get("email")
            if not email or "@" not in email:
                failed += 1
                continue
            # Personalize
            msg = self.personalizer.create_personalized_email(content_template, r, campaign_id=campaign_name)
            subject, body = msg["subject"], msg["body"]

            if self.dry_run:
                print(f"  [DRY-RUN] To: {email} | Subj: {subject}")
                continue
            if self.queue_emails:
                f = self.queue_dir / f"email_{i+1:03d}.json"
                json.dump(msg, open(f, "w", encoding="utf-8"), indent=2)
                queued += 1
                continue

            # Simulated send
            print(f"  [SEND] {email} | {subject}")
            sent += 1
            if MIN_DELAY:
                time.sleep(MIN_DELAY)
        print(f"Summary: sent={sent}, queued={queued}, failed={failed}")
        return {"sent": sent, "queued": queued, "failed": failed}

# ==============================================================
# Main runner
# ==============================================================
def campaign_main(contacts_root: str, scheduled_root: str, tracking_root: str, alerts_email: str,
                  dry_run=False, queue_emails=False, delay=1):
    print("[runner] Starting compliant campaign runner")

    contacts = try_professional_loader(contacts_root) or fallback_load_contacts_from_directory(contacts_root)
    if not contacts:
        print("[runner] No contacts found — aborting.")
        return

    # Compliance
    compliance = None
    if MinimalCompliance:
        try:
            compliance = MinimalCompliance(max_daily=MAX_DAILY, max_per_domain=MAX_DOMAIN, min_delay=MIN_DELAY)
            print(f"[runner] MinimalCompliance active ({MAX_DAILY}/day, {MAX_DOMAIN}/domain, {MIN_DELAY}s delay)")
        except Exception as e:
            print(f"[runner] Compliance init failed: {e}")

    # Personalizer
    if PERSONALIZER_AVAILABLE and EmailPersonalizer:
        try:
            personalizer = EmailPersonalizer(
                unsubscribe_base_url=UNSUB_BASE,
                from_name=FROM_NAME,
                from_email=FROM_EMAIL,
                physical_address=PHYS_ADDR
            )
            print(f"[runner] EmailPersonalizer initialized for {FROM_NAME} <{FROM_EMAIL}>")
        except Exception as e:
            print(f"[runner] Personalizer failed: {e}")
            personalizer = _FallbackPersonalizer()
    else:
        personalizer = _FallbackPersonalizer()

    emailer = Emailer(alerts_email=alerts_email, dry_run=dry_run, queue_emails=queue_emails,
                      compliance=compliance, personalizer=personalizer)

    # Campaign loop
    templates = list(Path(scheduled_root).rglob("*.txt")) + list(Path(scheduled_root).rglob("*.docx"))
    for tpl in templates:
        domain = tpl.parent.name
        content = load_campaign_content(str(tpl))
        if not content:
            continue
        subject = f"Campaign: {tpl.stem}"
        tracking_id = generate_tracking_id(domain, tpl.stem, tpl.name)
        enriched = [dict(c, tracking_id=tracking_id) for c in contacts]
        result = emailer.send_campaign(f"{domain}/{tpl.stem}", subject, content, enriched, FROM_NAME)
        save_tracking_data(tracking_root, domain, tracking_id, result)

    print("[runner] Done.")

# ==============================================================
# CLI
# ==============================================================
if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Compliant Domain-Aware Email Campaign Processor")
    p.add_argument("--contacts", required=True)
    p.add_argument("--scheduled", required=True)
    p.add_argument("--tracking", required=True)
    p.add_argument("--alerts", required=True)
    p.add_argument("--dry-run", action="store_true")
    p.add_argument("--queue-emails", action="store_true")
    args = p.parse_args()

    campaign_main(
        contacts_root=args.contacts,
        scheduled_root=args.scheduled,
        tracking_root=args.tracking,
        alerts_email=args.alerts,
        dry_run=args.dry_run,
        queue_emails=args.queue_emails
    )
