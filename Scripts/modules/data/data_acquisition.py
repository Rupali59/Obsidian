#!/usr/bin/env python3
"""
Data Acquisition Module
Handles GitHub metrics capture with parallel processing and optimized API usage
"""

import os
import sys
import json
import logging
import re
from pathlib import Path
from datetime import datetime, date, timedelta
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Dict, List, Optional

# Add the sync/github directory to the path
scripts_dir = Path(__file__).parent.parent.parent
github_dir = scripts_dir / "sync" / "github"
sys.path.insert(0, str(github_dir))

from github_batched_fetcher import GitHubBatchedFetcher

class DataAcquisition:
    def __init__(self, obsidian_path: str, config: Dict):
        self.obsidian_path = Path(obsidian_path)
        self.config = config
        self.data_logger = logging.getLogger('data')
        
        # Initialize the optimized fetcher
        self.fetcher = GitHubBatchedFetcher(str(obsidian_path))
        
    def run_capture_today(self, operation_config: Dict) -> Dict:
        """Capture GitHub metrics for today"""
        try:
            target_date = date.today()
            self.data_logger.info(f"Capturing data for today: {target_date}")
            
            return self._capture_single_date(target_date, operation_config)
            
        except Exception as e:
            self.data_logger.error(f"Today capture failed: {e}")
            return {"success": False, "error": str(e)}
    
    def run_capture_date_range(self, operation_config: Dict) -> Dict:
        """Capture GitHub metrics for a date range"""
        try:
            start_date = datetime.strptime(operation_config["start_date"], "%Y-%m-%d").date()
            end_date = datetime.strptime(operation_config["end_date"], "%Y-%m-%d").date()
            
            self.data_logger.info(f"Capturing data for date range: {start_date} to {end_date}")
            
            return self._capture_date_range(start_date, end_date, operation_config)
            
        except Exception as e:
            self.data_logger.error(f"Date range capture failed: {e}")
            return {"success": False, "error": str(e)}
    
    def run_capture_month(self, operation_config: Dict) -> Dict:
        """Capture GitHub metrics for an entire month"""
        try:
            year = operation_config["year"]
            month = operation_config["month"]
            
            # Calculate start and end dates for the month
            start_date = date(year, month, 1)
            if month == 12:
                end_date = date(year + 1, 1, 1) - timedelta(days=1)
            else:
                end_date = date(year, month + 1, 1) - timedelta(days=1)
            
            self.data_logger.info(f"Capturing data for month: {year}-{month:02d}")
            
            return self._capture_date_range(start_date, end_date, operation_config)
            
        except Exception as e:
            self.data_logger.error(f"Month capture failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _capture_single_date(self, target_date: date, operation_config: Dict) -> Dict:
        """Capture data for a single date"""
        try:
            print(f"🚀 Capturing GitHub metrics for {target_date}")
            print("=" * 60)
            
            # Get repository metrics using optimized fetcher
            start_time = datetime.now()
            all_metrics = self.fetcher.get_all_repository_metrics(target_date)
            end_time = datetime.now()
            
            if "error" in all_metrics:
                return {"success": False, "error": all_metrics["error"]}
            
            # Process results
            repositories_data = all_metrics.get('repositories', {})
            summary = all_metrics.get('summary', {})
            
            print(f"📊 Results Summary:")
            print(f"   📝 Total commits: {summary.get('total_commits', 0)}")
            print(f"   🔄 Total PRs: {summary.get('total_prs', 0)}")
            print(f"   🐛 Total issues: {summary.get('total_issues', 0)}")
            print(f"   📦 Total repositories: {summary.get('total_repositories', 0)}")
            print(f"   ⚡ API calls made: {summary.get('api_calls_made', 0)}")
            print(f"   💾 API calls saved: {summary.get('api_calls_saved', 0)}")
            print(f"   ⏱️  Processing time: {(end_time - start_time).total_seconds():.2f} seconds")
            
            # Update calendar if requested
            if operation_config.get("update_calendar", True):
                self._update_calendar_with_results(repositories_data, target_date, operation_config)
            
            return {
                "success": True,
                "date": target_date.isoformat(),
                "summary": summary,
                "processing_time": (end_time - start_time).total_seconds()
            }
            
        except Exception as e:
            self.data_logger.error(f"Single date capture failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _capture_date_range(self, start_date: date, end_date: date, operation_config: Dict) -> Dict:
        """Capture data for a date range with parallel processing"""
        try:
            # Generate list of dates
            dates = []
            current_date = start_date
            while current_date <= end_date:
                dates.append(current_date)
                current_date = current_date + timedelta(days=1)
            
            max_workers = operation_config.get("max_workers", 3)
            
            print(f"🚀 Capturing GitHub metrics for {len(dates)} dates")
            print(f"📅 Date range: {start_date} to {end_date}")
            print(f"👥 Max workers: {max_workers}")
            print(f"⚡ Expected API calls: {len(dates) * 13} (instead of {len(dates) * 37})")
            print("=" * 60)
            
            results = []
            completed = 0
            start_time = datetime.now()
            
            with ThreadPoolExecutor(max_workers=max_workers) as executor:
                # Submit all dates for processing
                future_to_date = {
                    executor.submit(self._capture_single_date, target_date, operation_config): target_date
                    for target_date in dates
                }
                
                # Process completed dates
                for future in as_completed(future_to_date):
                    target_date = future_to_date[future]
                    try:
                        result = future.result()
                        results.append((target_date, result))
                        completed += 1
                        
                        if completed % 5 == 0 or completed == len(dates):
                            print(f"   ✅ Progress: {completed}/{len(dates)} dates processed")
                            
                    except Exception as e:
                        self.data_logger.error(f"Error processing {target_date}: {e}")
                        results.append((target_date, {"success": False, "error": str(e)}))
                        completed += 1
            
            end_time = datetime.now()
            
            # Print summary
            self._print_range_summary(results, start_date, end_date, start_time, end_time)
            
            return {
                "success": True,
                "date_range": f"{start_date} to {end_date}",
                "total_dates": len(dates),
                "results": results,
                "processing_time": (end_time - start_time).total_seconds()
            }
            
        except Exception as e:
            self.data_logger.error(f"Date range capture failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _update_calendar_with_results(self, repositories_data: dict, target_date: date, operation_config: Dict):
        """Update calendar file with repository data"""
        try:
            calendar_file = self.fetcher.get_calendar_file_path(target_date)
            
            # Create backup if requested
            if operation_config.get("backup_before_write", True):
                self._create_backup(calendar_file)
            
            # Create directory if it doesn't exist
            calendar_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Initialize file with basic structure if it doesn't exist
            if not calendar_file.exists():
                with open(calendar_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {target_date.strftime('%B %d, %Y')}\\n\\n## Daily Notes\\n\\n## GitHub Activity\\n\\n**Activity Summary:** 0 commits\\n\\n### Commits\\n\\n")
                print(f"📝 Initialized calendar file: {calendar_file}")
            
            # Read current content
            with open(calendar_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Calculate total activity
            total_commits = sum(len(repo_data.get('commits', [])) for repo_data in repositories_data.values())
            total_prs = sum(len(repo_data.get('pull_requests', [])) for repo_data in repositories_data.values())
            total_issues = sum(len(repo_data.get('issues', [])) for repo_data in repositories_data.values())
            
            # Update activity summary
            summary_pattern = r'\\*\\*Activity Summary:\\*\\* \\d+ commits'
            new_summary = f"**Activity Summary:** {total_commits} commits"
            if total_prs > 0:
                new_summary += f", {total_prs} PRs"
            if total_issues > 0:
                new_summary += f", {total_issues} issues"
            
            content = re.sub(summary_pattern, new_summary, content)
            
            # Build GitHub activity section
            github_section = "\\n## GitHub Activity\\n\\n" + new_summary + "\\n\\n"
            
            if total_commits > 0:
                github_section += "### Commits\\n\\n"
                
                for repo_name, repo_data in repositories_data.items():
                    commits = repo_data.get('commits', [])
                    if commits:
                        github_section += f"**{repo_name}:**\\n"
                        for commit in commits:
                            github_section += f"- `{commit['sha']}` {commit['message']}\\n"
                        github_section += "\\n"
            
            if total_prs > 0:
                github_section += "### Pull Requests\\n\\n"
                
                for repo_name, repo_data in repositories_data.items():
                    prs = repo_data.get('pull_requests', [])
                    if prs:
                        github_section += f"**{repo_name}:**\\n"
                        for pr in prs:
                            github_section += f"- #{pr['number']} {pr['title']} ({pr['state']})\\n"
                        github_section += "\\n"
            
            if total_issues > 0:
                github_section += "### Issues\\n\\n"
                
                for repo_name, repo_data in repositories_data.items():
                    issues = repo_data.get('issues', [])
                    if issues:
                        github_section += f"**{repo_name}:**\\n"
                        for issue in issues:
                            github_section += f"- #{issue['number']} {issue['title']} ({issue['state']})\\n"
                        github_section += "\\n"
            
            # Replace or add GitHub section
            github_pattern = r'## GitHub Activity.*?(?=##|$)'
            if re.search(github_pattern, content, re.DOTALL):
                content = re.sub(github_pattern, github_section.strip(), content, flags=re.DOTALL)
            else:
                content += github_section
            
            # Write updated content
            with open(calendar_file, 'w', encoding='utf-8') as f:
                f.write(content)
            
            print(f"📝 Updated calendar file: {calendar_file}")
            print(f"   📝 Added {total_commits} commits, {total_prs} PRs, {total_issues} issues")
            
        except Exception as e:
            self.data_logger.error(f"Error updating calendar: {e}")
    
    def _create_backup(self, calendar_file: Path):
        """Create backup of calendar file"""
        try:
            if calendar_file.exists():
                backup_file = calendar_file.with_suffix('.backup')
                with open(calendar_file, 'r', encoding='utf-8') as src:
                    with open(backup_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                self.data_logger.info(f"Created backup: {backup_file}")
        except Exception as e:
            self.data_logger.error(f"Error creating backup: {e}")
    
    def _print_range_summary(self, results: List, start_date: date, end_date: date, start_time: datetime, end_time: datetime):
        """Print summary for date range processing"""
        successful = len([r for _, r in results if r.get("success", False)])
        failed = len(results) - successful
        
        print("=" * 60)
        print("🎉 PARALLEL PROCESSING COMPLETED!")
        print("=" * 60)
        print(f"📅 Date range: {start_date} to {end_date}")
        print(f"📊 Total dates processed: {len(results)}")
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        print(f"⏱️  Total processing time: {(end_time - start_time).total_seconds():.2f} seconds")
        
        if failed > 0:
            print(f"\\n⚠️  Failed dates:")
            for target_date, result in results:
                if not result.get("success", False):
                    print(f"   {target_date}: {result.get('error', 'Unknown error')}")
        
        # Show activity summary for successful dates
        successful_results = [r for _, r in results if r.get("success", False)]
        if successful_results:
            total_commits = sum(r.get("summary", {}).get("total_commits", 0) for r in successful_results)
            total_prs = sum(r.get("summary", {}).get("total_prs", 0) for r in successful_results)
            total_issues = sum(r.get("summary", {}).get("total_issues", 0) for r in successful_results)
            total_api_calls = sum(r.get("summary", {}).get("api_calls_made", 0) for r in successful_results)
            
            print(f"\\n📈 Activity Summary:")
            print(f"   📝 Total commits: {total_commits}")
            print(f"   🔄 Total PRs: {total_prs}")
            print(f"   🐛 Total issues: {total_issues}")
            print(f"   ⚡ Total API calls: {total_api_calls}")
            print(f"   💾 API calls saved: {len(results) * 24}")  # 24 calls saved per date
        
        print("=" * 60)
