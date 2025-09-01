#!/usr/bin/env python3
"""
Capture GitHub data for today (September 1st, 2025)
Simple single-date capture script
"""

import sys
from pathlib import Path

# Add the sync/github directory to the path
scripts_dir = Path(__file__).parent.parent
github_dir = scripts_dir / "sync" / "github"
sys.path.insert(0, str(github_dir))

from github_data_fetcher import GitHubDailyMetrics
from datetime import date

def main():
    """Capture GitHub data for today"""
    print("🚀 Capturing GitHub data for today")
    print("=" * 50)
    
    # Initialize the GitHub metrics capture
    github_capture = GitHubDailyMetrics(".")
    
    # Set target date to today
    target_date = date.today()
    
    print(f"📅 Target date: {target_date}")
    print()
    
    try:
        # Capture metrics for the specific date
        print("🔍 Capturing GitHub metrics...")
        result = github_capture.capture_github_metrics(target_date)
        
        print("✅ Capture completed successfully!")
        print(f"📊 Results: {result}")
        
        # Update the calendar entry
        print("\n📝 Updating calendar entry...")
        calendar_result = github_capture.update_calendar_entry(target_date)
        
        print("✅ Calendar updated successfully!")
        print(f"📁 File: {calendar_result}")
        
    except Exception as e:
        print(f"❌ Error during capture: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
