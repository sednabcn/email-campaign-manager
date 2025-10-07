#!/usr/bin/env python3
"""
Analyze campaign execution logs and tracking files
"""
import json
import sys
from pathlib import Path
from datetime import datetime

def analyze_tracking_files(tracking_dir='tracking'):
    """Analyze tracking files to understand what happened"""
    tracking_path = Path(tracking_dir)
    
    if not tracking_path.exists():
        print(f"❌ Tracking directory not found: {tracking_dir}")
        return False
    
    print("=" * 70)
    print("  Campaign Tracking Analysis")
    print("=" * 70)
    print()
    
    # Find all campaign tracking files
    campaign_files = list(tracking_path.glob('**/campaigns/*.json'))
    
    if not campaign_files:
        print("⚠️  No campaign tracking files found")
        return False
    
    print(f"📊 Found {len(campaign_files)} campaign tracking file(s)\n")
    
    total_sent = 0
    total_failed = 0
    total_queued = 0
    campaigns_summary = []
    
    for i, campaign_file in enumerate(sorted(campaign_files), 1):
        try:
            with open(campaign_file, 'r') as f:
                data = json.load(f)
                
            campaign_id = data.get('campaign_id', 'Unknown')
            status = data.get('status', 'Unknown')
            sent = data.get('emails_sent', 0)
            failed = data.get('emails_failed', 0)
            queued = data.get('emails_queued', 0)
            timestamp = data.get('timestamp', 'Unknown')
            error = data.get('error')
            
            print(f"{i}. Campaign: {campaign_file.name}")
            print(f"   ID: {campaign_id}")
            print(f"   Status: {status}")
            print(f"   Sent: {sent}")
            print(f"   Failed: {failed}")
            print(f"   Queued: {queued}")
            print(f"   Timestamp: {timestamp}")
            
            if error:
                print(f"   ❌ Error: {error}")
                
            # Show recipients if available
            recipients = data.get('recipients', [])
            if recipients:
                print(f"   👥 Recipients: {len(recipients)}")
                for j, recipient in enumerate(recipients[:3], 1):
                    email = recipient.get('email', 'Unknown')
                    rec_status = recipient.get('status', 'Unknown')
                    print(f"      {j}. {email} - {rec_status}")
                if len(recipients) > 3:
                    print(f"      ... and {len(recipients) - 3} more")
                    
            print()
            
            total_sent += sent
            total_failed += failed
            total_queued += queued
            
            campaigns_summary.append({
                'file': campaign_file.name,
                'status': status,
                'sent': sent,
                'failed': failed,
                'queued': queued
            })
            
        except Exception as e:
            print(f"❌ Error reading {campaign_file.name}: {e}")
            print()
            
    # Summary
    print("=" * 70)
    print("  Summary")
    print("=" * 70)
    print(f"Total Campaigns: {len(campaign_files)}")
    print(f"Total Sent: {total_sent}")
    print(f"Total Failed: {total_failed}")
    print(f"Total Queued: {total_queued}")
    print()
    
    # Status breakdown
    status_counts = {}
    for campaign in campaigns_summary:
        status = campaign['status']
        status_counts[status] = status_counts.get(status, 0) + 1
        
    print("Status Breakdown:")
    for status, count in status_counts.items():
        print(f"  - {status}: {count}")
        print()
        
    return True

def analyze_execution_log(log_file='campaign_json_execution.log'):
    """Analyze the execution log file"""
    log_path = Path(log_file)
    
    if not log_path.exists():
        print(f"⚠️  Log file not found: {log_file}")
        return False
    
    print("=" * 70)
    print("  Execution Log Analysis")
    print("=" * 70)
    print()
    
    with open(log_path, 'r') as f:
        lines = f.readlines()
        
    print(f"📄 Log file: {log_file}")
    print(f"📏 Total lines: {len(lines)}")
    print()
    
    # Extract key information
    errors = [line for line in lines if 'ERROR' in line or 'Error:' in line or 'error:' in line]
    warnings = [line for line in lines if 'WARNING' in line or 'Warning:' in line]
    success_msgs = [line for line in lines if '✅' in line or 'Success' in line or 'completed successfully' in line]
    
    if errors:
        print(f"❌ Errors found: {len(errors)}")
        for error in errors[:5]:  # Show first 5 errors
            print(f"   {error.strip()}")
        if len(errors) > 5:
            print(f"   ... and {len(errors) - 5} more errors")
            print()
            
    if warnings:
        print(f"⚠️  Warnings found: {len(warnings)}")
        for warning in warnings[:3]:  # Show first 3 warnings
            print(f"   {warning.strip()}")
        if len(warnings) > 3:
            print(f"   ... and {len(warnings) - 3} more warnings")
            print()
            
    if success_msgs:
        print(f"✅ Success messages: {len(success_msgs)}")
        for msg in success_msgs[:3]:
            print(f"   {msg.strip()}")
            print()
            
    # Show last 10 lines (often contains the most important info)
    print("📋 Last 10 lines of log:")
    print("-" * 70)
    for line in lines[-10:]:
        print(line.rstrip())
        print("-" * 70)
        print()
        
    return True

def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Analyze campaign execution results')
    parser.add_argument('--tracking-dir', default='tracking', help='Tracking directory path')
    parser.add_argument('--log-file', default='campaign_json_execution.log', help='Execution log file')
    parser.add_argument('--full-log', action='store_true', help='Show full log instead of summary')
    
    args = parser.parse_args()
    
    print()
    print("🔍 Campaign Execution Analysis")
    print()
    
    # Analyze tracking files
    tracking_ok = analyze_tracking_files(args.tracking_dir)
    
    # Analyze execution log
    log_ok = analyze_execution_log(args.log_file)
    
    if args.full_log:
        log_path = Path(args.log_file)
        if log_path.exists():
            print("\n" + "=" * 70)
            print("  Full Execution Log")
            print("=" * 70)
            print()
            with open(log_path, 'r') as f:
                print(f.read())
                
    print("=" * 70)
    print("  Analysis Complete")
    print("=" * 70)
    
    if not tracking_ok and not log_ok:
        print("❌ No tracking files or logs found")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main())
