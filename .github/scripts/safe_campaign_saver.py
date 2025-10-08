#!/usr/bin/env python3
"""
Safe campaign result saver with automatic directory creation.
Prevents "No such file or directory" errors.
"""

import json
import os
import sys
from pathlib import Path
from datetime import datetime
from typing import Dict, Any, Optional


class SafeCampaignSaver:
    """Handle safe saving of campaign results with directory creation."""
    
    def __init__(self, base_tracking_dir: str = "tracking"):
        """
        Initialize saver.
        
        Args:
            base_tracking_dir: Base directory for tracking files
        """
        self.base_dir = Path(base_tracking_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
    
    def ensure_directory(self, file_path: str) -> Path:
        """
        Ensure directory exists for a file path.
        
        Args:
            file_path: Path to file
            
        Returns:
            Path object for the file
        """
        path = Path(file_path)
        path.parent.mkdir(parents=True, exist_ok=True)
        return path
    
    def save_campaign_result(
        self,
        campaign_id: str,
        domain: str,
        subdomain: str,
        result_data: Dict[str, Any],
        timestamp: Optional[str] = None
    ) -> str:
        """
        Save campaign result with proper directory creation.
        
        Args:
            campaign_id: Campaign identifier
            domain: Campaign domain (education, finance, etc.)
            subdomain: Campaign subdomain (adult_education, etc.)
            result_data: Result data to save
            timestamp: Optional timestamp string
            
        Returns:
            Path to saved file
        """
        if timestamp is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        # Build safe file path
        filename = f"{campaign_id}_{timestamp}.json"
        file_path = self.base_dir / domain / subdomain / filename
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata
        result_data.update({
            "saved_at": datetime.now().isoformat(),
            "campaign_id": campaign_id,
            "domain": domain,
            "subdomain": subdomain,
            "file_path": str(file_path)
        })
        
        # Save with error handling
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(result_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved campaign result: {file_path}")
            return str(file_path)
        
        except Exception as e:
            print(f"❌ Error saving {file_path}: {e}", file=sys.stderr)
            
            # Try fallback location
            fallback_dir = self.base_dir / "execution_logs"
            fallback_dir.mkdir(parents=True, exist_ok=True)
            fallback_path = fallback_dir / filename
            
            try:
                with open(fallback_path, 'w', encoding='utf-8') as f:
                    json.dump(result_data, f, indent=2, ensure_ascii=False)
                print(f"⚠️ Saved to fallback location: {fallback_path}")
                return str(fallback_path)
            except Exception as e2:
                print(f"❌ Fallback save also failed: {e2}", file=sys.stderr)
                raise
    
    def save_batch_summary(
        self,
        batch_data: Dict[str, Any],
        batch_id: Optional[str] = None
    ) -> str:
        """
        Save batch processing summary.
        
        Args:
            batch_data: Batch summary data
            batch_id: Optional batch identifier
            
        Returns:
            Path to saved file
        """
        if batch_id is None:
            batch_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        
        filename = f"batch_summary_{batch_id}.json"
        file_path = self.base_dir / "batch_reports" / filename
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata
        batch_data.update({
            "saved_at": datetime.now().isoformat(),
            "batch_id": batch_id
        })
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(batch_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved batch summary: {file_path}")
            return str(file_path)
        
        except Exception as e:
            print(f"❌ Error saving batch summary: {e}", file=sys.stderr)
            raise
    
    def save_execution_log(
        self,
        log_data: Dict[str, Any],
        log_type: str = "execution"
    ) -> str:
        """
        Save execution log data.
        
        Args:
            log_data: Log data to save
            log_type: Type of log
            
        Returns:
            Path to saved file
        """
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{log_type}_{timestamp}.json"
        file_path = self.base_dir / "execution_logs" / filename
        
        # Ensure directory exists
        file_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata
        log_data.update({
            "saved_at": datetime.now().isoformat(),
            "log_type": log_type
        })
        
        try:
            with open(file_path, 'w', encoding='utf-8') as f:
                json.dump(log_data, f, indent=2, ensure_ascii=False)
            
            print(f"✅ Saved execution log: {file_path}")
            return str(file_path)
        
        except Exception as e:
            print(f"❌ Error saving execution log: {e}", file=sys.stderr)
            raise


def main():
    """Demo and test functionality."""
    print("Testing SafeCampaignSaver...")
    print()
    
    saver = SafeCampaignSaver()
    
    # Test campaign result save
    test_result = {
        "status": "success",
        "emails_sent": 10,
        "emails_failed": 0,
        "template": "adult_education_letter.txt"
    }
    
    try:
        saved_path = saver.save_campaign_result(
            campaign_id="adult_education_letter",
            domain="education",
            subdomain="adult_education",
            result_data=test_result
        )
        print(f"✅ Test successful: {saved_path}")
    except Exception as e:
        print(f"❌ Test failed: {e}")
        return 1
    
    # Test batch summary save
    test_batch = {
        "total_campaigns": 5,
        "total_emails": 50,
        "success_rate": 100.0
    }
    
    try:
        saved_path = saver.save_batch_summary(test_batch)
        print(f"✅ Batch test successful: {saved_path}")
    except Exception as e:
        print(f"❌ Batch test failed: {e}")
        return 1
    
    print()
    print("✅ All tests passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
