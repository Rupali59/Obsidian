#!/usr/bin/env python3
"""
Parallel GitHub Metrics Runner
Executes GitHub metrics capture using parallel processing
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime, date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from parallel_repo_runner import ParallelRepoRunner

class ParallelRunner:
    def __init__(self, obsidian_path: str, config_file: str):
        self.obsidian_path = Path(obsidian_path)
        self.config_file = Path(config_file)
        self.config = self._load_config()
        self.parallel_runner = ParallelRepoRunner(obsidian_path)
        self._setup_logging()
        
    def _load_config(self):
        """Load configuration from JSON file"""
        if not self.config_file.exists():
            raise FileNotFoundError(f"Config file not found: {self.config_file}")
        
        with open(self.config_file, 'r') as f:
            return json.load(f)
    
    def _setup_logging(self):
        """Setup logging for the runner"""
        # Import log manager
        sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
        from log_manager import LogManager
        
        # Setup logging with rotation
        log_manager = LogManager(str(Path(__file__).parent.parent))
        self.logger = log_manager.setup_logging("parallel_runner", logging.INFO)
        
        self.logger.info(f"Parallel runner started: {self.config_file}")
    
    def _get_date_range(self):
        """Get the date range from configuration"""
        start_date = datetime.strptime(self.config['start_date'], '%Y-%m-%d').date()
        end_date = datetime.strptime(self.config['end_date'], '%Y-%m-%d').date()
        
        dates = []
        current_date = start_date
        while current_date <= end_date:
            dates.append(current_date)
            # Use timedelta to properly increment date
            current_date = current_date + timedelta(days=1)
        
        return dates
    
    def _process_date(self, target_date):
        """Process a single date (worker function)"""
        try:
            self.logger.info(f"Processing {target_date}")
            # Use the parallel repo runner for this specific date
            results = self.parallel_runner.run_for_date(target_date, max_workers=3, rate_limit=0.2, update_calendar=True)
            
            # Aggregate results for summary
            total_commits = sum(len(result.get('commits', [])) for _, result in results)
            total_prs = sum(len(result.get('pull_requests', [])) for _, result in results)
            total_issues = sum(len(result.get('issues', [])) for _, result in results)
            
            result = {
                "commits": total_commits,
                "pull_requests": total_prs,
                "issues": total_issues,
                "repositories_processed": len(results)
            }
            
            self.logger.info(f"Captured metrics: {total_commits} commits, {total_prs} PRs, {total_issues} issues")
            return target_date, result
        except Exception as e:
            self.logger.error(f"Error processing {target_date}: {e}")
            return target_date, {"error": str(e)}
    
    def run(self):
        """Run the parallel capture process"""
        dates = self._get_date_range()
        workers = self.config.get('parallel_workers', 3)
        rate_limit = self.config.get('rate_limit_delay', 0.3)
        
        print(f"🚀 Starting parallel capture: {self.config['name']}")
        print(f"📅 Processing {len(dates)} dates with {workers} workers")
        print(f"⏱️  Rate limit: {rate_limit}s between API calls")
        print("=" * 60)
        
        results = []
        completed = 0
        
        with ThreadPoolExecutor(max_workers=workers) as executor:
            # Submit all dates for processing
            future_to_date = {executor.submit(self._process_date, date): date for date in dates}
            
            # Process completed futures
            for future in as_completed(future_to_date):
                target_date, result = future.result()
                results.append((target_date, result))
                completed += 1
                
                # Show progress
                if completed % 5 == 0 or completed == len(dates):
                    print(f"   ✅ Progress: {completed}/{len(dates)} dates processed")
                
                # Rate limiting
                time.sleep(rate_limit)
        
        self._print_summary(results)
        return results
    
    def _print_summary(self, results):
        """Print a summary of the results"""
        print("=" * 60)
        print("🎉 PARALLEL CAPTURE COMPLETED!")
        print("=" * 60)
        print(f"📅 Configuration: {self.config['name']}")
        print(f"📊 Total dates processed: {len(results)}")
        
        # Count successful vs failed
        successful = sum(1 for _, result in results if "error" not in result)
        failed = len(results) - successful
        
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        
        if failed > 0:
            print(f"\n⚠️  Failed dates:")
            for target_date, result in results:
                if "error" in result:
                    print(f"   {target_date}: {result['error']}")
        
        # Show activity summary for successful dates
        successful_results = [r for _, r in results if "error" not in r]
        if successful_results:
            total_commits = sum(r.get('commits', 0) for r in successful_results)
            total_prs = sum(r.get('pull_requests', 0) for r in successful_results)
            total_issues = sum(r.get('issues', 0) for r in successful_results)
            total_repos = sum(r.get('repositories_processed', 0) for r in successful_results)
            
            print(f"\n📈 Activity Summary:")
            print(f"   📝 Total commits: {total_commits}")
            print(f"   🔄 Total PRs: {total_prs}")
            print(f"   🐛 Total issues: {total_issues}")
            print(f"   📦 Total repository processing sessions: {total_repos}")
        
        print("=" * 60)

def main():
    """Main function"""
    if len(sys.argv) != 3:
        print("Usage: python3 runner.py <obsidian_path> <config_file>")
        print("Example: python3 runner.py . configs/august_2025.json")
        sys.exit(1)
    
    obsidian_path = sys.argv[1]
    config_file = sys.argv[2]
    
    try:
        runner = ParallelRunner(obsidian_path, config_file)
        runner.run()
        print("✅ Parallel capture completed successfully!")
    
    except Exception as e:
        print(f"❌ Parallel capture failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
