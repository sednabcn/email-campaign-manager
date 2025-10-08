#!/usr/bin/env python3
"""
Ensure all tracking directories exist before campaign execution.
This prevents "No such file or directory" errors when saving results.
"""

import os
import sys
from pathlib import Path


def create_tracking_structure(base_dir="tracking"):
    """
    Create comprehensive tracking directory structure.
    
    Args:
        base_dir: Base tracking directory path
    """
    base_path = Path(base_dir)
    
    # Main tracking subdirectories
    main_dirs = [
        "feedback_responses",
        "domain_stats",
        "execution_logs",
        "batch_reports",
        "reply_tracking"
    ]
    
    # Domain-specific tracking directories
    domains = {
        "education": ["adult_education", "higher_education", "k12_education", "vocational"],
        "finance": ["banking", "insurance", "investment", "accounting"],
        "healthcare": ["hospitals", "clinics", "research", "pharma"],
        "industry": ["manufacturing", "retail", "services", "construction"],
        "technology": ["software", "hardware", "telecom", "it_services"],
        "government": ["federal", "state", "local", "agencies"]
    }
    
    print(f"Creating tracking directory structure in: {base_path.absolute()}")
    
    # Create main directories
    for dir_name in main_dirs:
        dir_path = base_path / dir_name
        dir_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ {dir_path}")
    
    # Create domain-specific directories
    for domain, subdomains in domains.items():
        domain_path = base_path / domain
        domain_path.mkdir(parents=True, exist_ok=True)
        print(f"✅ {domain_path}")
        
        for subdomain in subdomains:
            subdomain_path = domain_path / subdomain
            subdomain_path.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ {subdomain_path}")
    
    print(f"\n✅ Tracking directory structure created successfully")
    return True


def ensure_result_path(result_path):
    """
    Ensure the directory for a result file exists.
    
    Args:
        result_path: Path to the result file
    
    Returns:
        True if directory exists or was created successfully
    """
    result_file = Path(result_path)
    result_dir = result_file.parent
    
    if not result_dir.exists():
        print(f"Creating directory: {result_dir}")
        result_dir.mkdir(parents=True, exist_ok=True)
        return True
    
    return True


def main():
    """Main execution."""
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Ensure tracking directory structure exists"
    )
    parser.add_argument(
        "--base-dir",
        default="tracking",
        help="Base tracking directory (default: tracking)"
    )
    parser.add_argument(
        "--verify-path",
        help="Verify a specific result path can be written"
    )
    
    args = parser.parse_args()
    
    try:
        # Create base structure
        create_tracking_structure(args.base_dir)
        
        # Verify specific path if requested
        if args.verify_path:
            print(f"\nVerifying path: {args.verify_path}")
            if ensure_result_path(args.verify_path):
                print(f"✅ Path verified: {args.verify_path}")
            else:
                print(f"❌ Failed to verify path: {args.verify_path}")
                sys.exit(1)
        
        return 0
    
    except Exception as e:
        print(f"❌ Error: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return 1


if __name__ == "__main__":
    sys.exit(main())
