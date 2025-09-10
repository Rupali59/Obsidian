#!/usr/bin/env python3
"""
Unified Parallel Repository Runner
Single script that uses configuration files and optimized GraphQL batching
Supports both single date and date range processing
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from datetime import datetime, date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Add the sync/github directory to the path
scripts_dir = Path(__file__).parent.parent
github_dir = scripts_dir / "sync" / "github"
sys.path.insert(0, str(github_dir))

from github_batched_fetcher import GitHubBatchedFetcher

class UnifiedParallelRunner:
    def __init__(self, obsidian_path: str, config_name: str = "september_2025"):
        self.obsidian_path = Path(obsidian_path)
        self.calendar_path = self.obsidian_path / "Calendar"
        self.config_name = config_name
        
        # Setup logging
        self.logger = logging.getLogger(__name__)
        self.logger.setLevel(logging.INFO)
        
        # Initialize batched fetcher (most efficient)
        self.batched_fetcher = GitHubBatchedFetcher(str(obsidian_path))
        
        # Load configuration
        self.config = self._load_config()
        
        print(f"🚀 Unified Parallel Runner initialized")
        print(f"📁 Obsidian path: {self.obsidian_path}")
        print(f"📅 Calendar path: {self.calendar_path}")
        print(f"⚙️  Config: {config_name}")
    
    def _load_config(self):
        """Load configuration from parallel/configs directory"""
        config_path = self.obsidian_path / "Scripts" / "parallel" / "configs" / f"{self.config_name}.json"
        
        if not config_path.exists():
            print(f"⚠️  Config file not found: {config_path}")
            print("📝 Using default configuration")
            return {
                "name": "Default Capture",
                "description": "Default GitHub metrics capture",
                "parallel_workers": 3,
                "rate_limit_delay": 0.3,
                "progress_interval": 5
            }
        
        with open(config_path, 'r') as f:
            config = json.load(f)
        
        print(f"✅ Loaded config: {config.get('name', 'Unknown')}")
        return config
    
    def run_for_date(self, target_date: date, update_calendar=True):
        """
        Run optimized processing for a specific date using batched requests
        This reduces API calls from 36+ to ~4-6!
        """
        print(f"🚀 Starting UNIFIED parallel repository processing for {target_date}")
        print("=" * 60)
        
        try:
            # Get all repository metrics using batched requests
            print("📡 Executing batched requests for all repositories...")
            start_time = time.time()
            
            # Use the optimized batched fetcher
            result = self.batched_fetcher.get_all_repository_metrics(target_date)
            metrics = result.get('metrics', {})
            api_stats = result.get('api_stats', {})
            
            processing_time = time.time() - start_time
            
            # Display results
            total_commits = sum(repo.get('commits', 0) for repo in metrics.values())
            total_prs = sum(repo.get('prs', 0) for repo in metrics.values())
            total_issues = sum(repo.get('issues', 0) for repo in metrics.values())
            total_repos = len(metrics)
            api_calls_made = api_stats.get('api_calls_made', 0)
            api_calls_saved = api_stats.get('api_calls_saved', 0)
            
            print(f"⚡ Batched requests completed in {processing_time:.2f} seconds")
            print(f"📊 Results Summary:")
            print(f"   📝 Total commits: {total_commits}")
            print(f"   🔄 Total PRs: {total_prs}")
            print(f"   🐛 Total issues: {total_issues}")
            print(f"   📦 Total repositories: {total_repos}")
            print(f"   ⚡ API calls made: {api_calls_made}")
            print(f"   💾 API calls saved: {api_calls_saved}")
            
            # Update calendar if requested
            if update_calendar:
                print(f"\n📝 Updating calendar entry for {target_date}...")
                calendar_file = self._update_calendar_entry(target_date, metrics)
                print(f"✅ Calendar updated: {calendar_file}")
            
            return {
                "success": True,
                "date": str(target_date),
                "summary": {
                    "total_commits": total_commits,
                    "total_prs": total_prs,
                    "total_issues": total_issues,
                "total_repositories": total_repos,
                "api_calls_made": api_calls_made,
                "api_calls_saved": api_calls_saved
                },
                "processing_time": processing_time
            }
            
        except Exception as e:
            print(f"❌ Error during processing: {e}")
            self.logger.error(f"Processing failed for {target_date}: {e}")
            return {"success": False, "error": str(e)}
    
    def run_for_date_range(self, start_date: date, end_date: date, update_calendar=True):
        """
        Run processing for a date range
        """
        print(f"🚀 Starting UNIFIED parallel processing for date range: {start_date} to {end_date}")
        print("=" * 60)
        
        results = []
        current_date = start_date
        
        while current_date <= end_date:
            print(f"\n📅 Processing {current_date}...")
            result = self.run_for_date(current_date, update_calendar)
            results.append(result)
            
            if not result.get("success", False):
                print(f"⚠️  Failed to process {current_date}")
            
            current_date += timedelta(days=1)
        
        # Summary
        successful = sum(1 for r in results if r.get("success", False))
        total_commits = sum(r.get("summary", {}).get("total_commits", 0) for r in results)
        
        print(f"\n✅ Date range processing completed!")
        print(f"📊 Processed {successful}/{len(results)} dates successfully")
        print(f"📝 Total commits across all dates: {total_commits}")
        
        return results
    
    def _update_calendar_entry(self, target_date: date, metrics: dict):
        """Update calendar entry with metrics"""
        # Create calendar file path
        year = target_date.year
        month = target_date.strftime("%B")
        day = target_date.strftime("%d-%m-%Y")
        
        calendar_dir = self.calendar_path / str(year) / month
        calendar_dir.mkdir(parents=True, exist_ok=True)
        
        calendar_file = calendar_dir / f"{day}.md"
        
        # Create backup if file exists
        if calendar_file.exists():
            backup_file = calendar_file.with_suffix('.backup')
            calendar_file.rename(backup_file)
            print(f"📁 Created backup: {backup_file}")
        
        # Generate calendar content
        content = self._generate_calendar_content(target_date, metrics)
        
        # Write to file
        with open(calendar_file, 'w') as f:
            f.write(content)
        
        return calendar_file
    
    def _generate_calendar_content(self, target_date: date, metrics: dict):
        """Generate calendar content from metrics"""
        day_name = target_date.strftime("%A")
        month_name = target_date.strftime("%B")
        
        # Calculate totals
        total_commits = sum(repo.get('commits', 0) for repo in metrics.values())
        total_prs = sum(repo.get('prs', 0) for repo in metrics.values())
        total_issues = sum(repo.get('issues', 0) for repo in metrics.values())
        
        content = f"""# {day_name}, {month_name} {target_date.day}, {target_date.year}

## Daily Notes


## GitHub Activity

**Activity Summary:** {total_commits} commits, {total_prs} PRs, {total_issues} issues

### Development Summary

**🔧 Components Worked On:**

"""
        
        # Add repository-specific content
        for repo_name, repo_metrics in metrics.items():
            if repo_metrics.get('commits', 0) > 0 or repo_metrics.get('prs', 0) > 0 or repo_metrics.get('issues', 0) > 0:
                content += f"#### **{repo_name}**\n"
                content += f"- **Commits**: {repo_metrics.get('commits', 0)}\n"
                content += f"- **Pull Requests**: {repo_metrics.get('prs', 0)}\n"
                content += f"- **Issues**: {repo_metrics.get('issues', 0)}\n\n"
        
        content += f"""
**🎯 Key Achievements:**
- **API Efficiency**: Used optimized GraphQL batching to reduce API calls
- **Parallel Processing**: Processed multiple repositories simultaneously
- **Data Accuracy**: Captured comprehensive GitHub activity metrics
- **System Integration**: Updated calendar with detailed development summaries

---
*Generated by Unified Parallel Runner - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
        
        return content

def main():
    """Main entry point with command line arguments"""
    parser = argparse.ArgumentParser(description='Unified Parallel Repository Runner')
    parser.add_argument('obsidian_path', help='Path to Obsidian vault')
    parser.add_argument('--date', type=str, help='Specific date (YYYY-MM-DD)')
    parser.add_argument('--yesterday', action='store_true', help='Process yesterday')
    parser.add_argument('--today', action='store_true', help='Process today (default)')
    parser.add_argument('--config', type=str, default='september_2025', help='Configuration name')
    parser.add_argument('--no-calendar', action='store_true', help='Skip calendar update')
    
    args = parser.parse_args()
    
    # Determine target date
    if args.date:
        target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
    elif args.yesterday:
        target_date = date.today() - timedelta(days=1)
    else:
        target_date = date.today()  # Default to today
    
    # Initialize runner
    runner = UnifiedParallelRunner(args.obsidian_path, args.config)
    
    # Run processing
    result = runner.run_for_date(target_date, not args.no_calendar)
    
    if result.get("success", False):
        print(f"\n✅ Processing completed successfully!")
        print(f"📊 Summary: {result['summary']}")
    else:
        print(f"\n❌ Processing failed: {result.get('error', 'Unknown error')}")
        sys.exit(1)

if __name__ == "__main__":
    main()
