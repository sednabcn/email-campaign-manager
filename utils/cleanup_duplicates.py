#!/usr/bin/env python3
"""
One-time cleanup: Remove all duplicate CSVs from contacts/ directory
Keeps only the oldest version of each unique contact set
"""
import os
import csv
import hashlib
from pathlib import Path
from datetime import datetime

def get_file_creation_time(filepath):
    """Get file creation/modification time"""
    try:
        return os.path.getctime(filepath)
    except:
        return os.path.getmtime(filepath)

def calculate_csv_hash(csv_path):
    """Calculate hash of CSV content"""
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rows = sorted([dict(row) for row in reader], key=lambda x: x.get('email', ''))
            
            content_parts = []
            for row in rows:
                sorted_items = sorted(row.items())
                row_str = '|'.join(f"{k}:{v.strip()}" for k, v in sorted_items if v)
                content_parts.append(row_str)
            
            content = '\n'.join(content_parts)
            return hashlib.sha256(content.encode('utf-8')).hexdigest()
    except Exception as e:
        print(f"Error hashing {csv_path}: {e}")
        return None

def cleanup_duplicates(contacts_dir):
    """Remove duplicate CSVs, keeping only the oldest"""
    contacts_path = Path(contacts_dir)
    
    if not contacts_path.exists():
        print(f"Directory not found: {contacts_dir}")
        return
    
    csv_files = list(contacts_path.glob('*.csv'))
    
    if not csv_files:
        print(f"No CSV files found in {contacts_dir}")
        return
    
    print(f"Found {len(csv_files)} CSV files")
    print("Analyzing for duplicates...\n")
    
    # Group files by content hash
    hash_groups = {}
    
    for csv_file in csv_files:
        file_hash = calculate_csv_hash(csv_file)
        if not file_hash:
            print(f"Skipping {csv_file.name} (could not hash)")
            continue
        
        if file_hash not in hash_groups:
            hash_groups[file_hash] = []
        
        hash_groups[file_hash].append({
            'path': csv_file,
            'name': csv_file.name,
            'created': get_file_creation_time(csv_file),
            'hash': file_hash
        })
    
    # Find and remove duplicates
    total_removed = 0
    total_kept = 0
    
    for file_hash, files in hash_groups.items():
        if len(files) == 1:
            total_kept += 1
            print(f"UNIQUE: {files[0]['name']}")
        else:
            # Sort by creation time (oldest first)
            files.sort(key=lambda x: x['created'])
            
            # Keep the oldest
            keep_file = files[0]
            duplicate_files = files[1:]
            
            print(f"\nDUPLICATE SET (hash: {file_hash[:12]}...):")
            print(f"  KEEPING: {keep_file['name']} (created: {datetime.fromtimestamp(keep_file['created']).isoformat()})")
            
            for dup in duplicate_files:
                print(f"  REMOVING: {dup['name']} (created: {datetime.fromtimestamp(dup['created']).isoformat()})")
                try:
                    os.remove(dup['path'])
                    total_removed += 1
                except Exception as e:
                    print(f"    ERROR: Could not remove - {e}")
            
            total_kept += 1
    
    print("\n" + "="*60)
    print("CLEANUP SUMMARY")
    print("="*60)
    print(f"Original files: {len(csv_files)}")
    print(f"Unique sets: {len(hash_groups)}")
    print(f"Files kept: {total_kept}")
    print(f"Files removed: {total_removed}")
    print(f"Final count: {total_kept}")
    
    # Show remaining files
    remaining = list(contacts_path.glob('*.csv'))
    if remaining:
        print("\nRemaining files:")
        for f in sorted(remaining):
            print(f"  - {f.name}")

if __name__ == '__main__':
    import sys
    
    contacts_dir = sys.argv[1] if len(sys.argv) > 1 else 'contacts'
    
    print("="*60)
    print("ONE-TIME DUPLICATE CLEANUP")
    print("="*60)
    print(f"Directory: {contacts_dir}")
    print()
    
    cleanup_duplicates(contacts_dir)
