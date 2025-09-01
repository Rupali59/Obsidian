#!/usr/bin/env python3
"""
Parallel Repository Processing Runner
Processes multiple repositories in parallel for a specific date
"""

import os
import sys
import json
import logging
import re
from pathlib import Path
from datetime import datetime, date
from concurrent.futures import ThreadPoolExecutor, as_completed
import time

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from sync.github.github_data_fetcher import GitHubDailyMetrics

class ParallelRepoRunner:
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        # The obsidian_path should be the root of the vault, not the Scripts directory
        # Change to the obsidian directory so the data fetcher can find the config
        os.chdir(obsidian_path)
        self.data_fetcher = GitHubDailyMetrics(str(obsidian_path))
        self._setup_logging()
        
    def _setup_logging(self):
        """Setup logging for the runner"""
        # Import log manager
        sys.path.insert(0, str(Path(__file__).parent.parent / "tools"))
        from log_manager import LogManager
        
        # Setup logging with rotation
        log_manager = LogManager(str(Path(__file__).parent.parent))
        self.logger = log_manager.setup_logging("parallel_repo_runner", logging.INFO)
        
        self.logger.info("Parallel repository runner started")
    
    def _get_tracked_repositories(self):
        """Get list of repositories marked for tracking"""
        config_path = Path(self.obsidian_path) / "Scripts" / "config" / "repos_to_track.env"
        
        if not config_path.exists():
            self.logger.error(f"Repository config not found: {config_path}")
            return []
        
        tracked_repos = []
        with open(config_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith('#') and '=' in line:
                    repo_name, status = line.split('=', 1)
                    repo_name = repo_name.strip()
                    status = status.strip()
                    
                    if status == 'X':
                        tracked_repos.append(repo_name)
        
        self.logger.info(f"Found {len(tracked_repos)} repositories to track: {tracked_repos}")
        return tracked_repos
    
    def _process_repository(self, repo_name, target_date):
        """Process a single repository for a specific date (worker function)"""
        try:
            self.logger.info(f"Processing repository: {repo_name} for {target_date}")
            
            # Create a new data fetcher instance for this repository
            repo_fetcher = GitHubDailyMetrics(str(self.obsidian_path))
            
            # Get repository-specific metrics with full username/repo format
            full_repo_name = f"{repo_fetcher.github_username}/{repo_name}"
            repo_metrics = repo_fetcher._get_repository_metrics(full_repo_name, target_date)
            
            # Transform the data to match the expected format
            if "error" not in repo_metrics:
                # Transform commits to match expected format
                formatted_commits = []
                for commit in repo_metrics.get('commits', []):
                    formatted_commits.append({
                        'repo': full_repo_name,
                        'sha': commit['sha'][:7],
                        'message': commit['commit']['message']
                    })
                repo_metrics['commits'] = formatted_commits
                
                # Transform PRs to match expected format
                formatted_prs = []
                for pr in repo_metrics.get('pull_requests', []):
                    formatted_prs.append({
                        'repo': full_repo_name,
                        'number': pr['number'],
                        'title': pr['title'],
                        'state': pr['state']
                    })
                repo_metrics['pull_requests'] = formatted_prs
                
                # Transform issues to match expected format
                formatted_issues = []
                for issue in repo_metrics.get('issues', []):
                    formatted_issues.append({
                        'repo': full_repo_name,
                        'number': issue['number'],
                        'title': issue['title'],
                        'state': issue['state']
                    })
                repo_metrics['issues'] = formatted_issues
            
            return repo_name, repo_metrics
            
        except Exception as e:
            self.logger.error(f"Error processing {repo_name} for {target_date}: {e}")
            return repo_name, {"error": str(e)}
    
    def run_for_date(self, target_date, max_workers=5, rate_limit=0.2, update_calendar=True):
        """Run parallel processing for a specific date"""
        tracked_repos = self._get_tracked_repositories()
        
        if not tracked_repos:
            self.logger.error("No repositories configured for tracking")
            return []
        
        print(f"🚀 Starting parallel repository processing for {target_date}")
        print(f"📦 Processing {len(tracked_repos)} repositories with {max_workers} workers")
        print(f"⏱️  Rate limit: {rate_limit}s between API calls")
        print("=" * 60)
        
        # Initialize calendar file if update_calendar is True
        if update_calendar:
            self._initialize_calendar_file(target_date)
        
        results = []
        completed = 0
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            # Submit all repositories for processing
            future_to_repo = {
                executor.submit(self._process_repository, repo, target_date): repo 
                for repo in tracked_repos
            }
            
            # Process completed futures
            for future in as_completed(future_to_repo):
                repo_name, result = future.result()
                results.append((repo_name, result))
                completed += 1
                
                # Write repository data to calendar immediately if successful
                if update_calendar and "error" not in result:
                    self._write_repo_data_to_calendar(repo_name, result, target_date)
                
                # Show progress
                print(f"   ✅ Progress: {completed}/{len(tracked_repos)} repositories processed")
                
                # Rate limiting
                time.sleep(rate_limit)
        
        self._print_summary(results, target_date)
        return results
    
    def _initialize_calendar_file(self, target_date):
        """Initialize the calendar file with basic structure, preserving existing content"""
        try:
            # Create a temporary data fetcher to get the calendar file path
            temp_fetcher = GitHubDailyMetrics(str(self.obsidian_path))
            calendar_file = temp_fetcher.get_calendar_file_path(target_date)
            
            # Create directory if it doesn't exist
            calendar_file.parent.mkdir(parents=True, exist_ok=True)
            
            # Initialize file with basic structure if it doesn't exist
            if not calendar_file.exists():
                with open(calendar_file, 'w', encoding='utf-8') as f:
                    f.write(f"# {target_date.strftime('%B %d, %Y')}\n\n## Daily Notes\n\n## GitHub Activity\n\n**Activity Summary:** 0 commits\n\n### Commits\n\n")
                print(f"📝 Initialized new calendar file: {calendar_file}")
            else:
                # Check if GitHub Activity section exists and is properly structured
                with open(calendar_file, 'r', encoding='utf-8') as f:
                    content = f.read()
                
                if "## GitHub Activity" not in content:
                    # Add GitHub Activity section at the end, preserving all existing content
                    with open(calendar_file, 'a', encoding='utf-8') as f:
                        f.write("\n## GitHub Activity\n\n**Activity Summary:** 0 commits\n\n### Commits\n\n")
                    print(f"📝 Added GitHub Activity section to existing file: {calendar_file}")
                else:
                    print(f"📝 Using existing calendar file with GitHub Activity section: {calendar_file}")
                
        except Exception as e:
            self.logger.error(f"Error initializing calendar file: {e}")
            print(f"❌ Error initializing calendar file: {e}")
    
    def _write_repo_data_to_calendar(self, repo_name, result, target_date):
        """Write repository data to calendar file immediately, preserving existing content"""
        try:
            # Create a temporary data fetcher to get the calendar file path
            temp_fetcher = GitHubDailyMetrics(str(self.obsidian_path))
            calendar_file = temp_fetcher.get_calendar_file_path(target_date)
            
            if not calendar_file.exists():
                self.logger.error(f"Calendar file not found: {calendar_file}")
                return
            
            # Create backup before modifying
            self._create_backup(calendar_file)
            
            # Read current content
            with open(calendar_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Format repository data
            repo_data = self._format_repo_data_for_calendar(repo_name, result)
            
            if repo_data:
                # Check if this repository's data already exists
                repo_section_pattern = f"\\*\\*{repo_name}:\\*\\*"
                if re.search(repo_section_pattern, content):
                    # Replace existing repository section only
                    pattern = f"\\*\\*{repo_name}:\\*\\*.*?(?=\\n\\*\\*|\\n$)"
                    new_content = re.sub(pattern, repo_data, content, flags=re.DOTALL)
                    print(f"   🔄 Replaced existing {repo_name} data in calendar")
                else:
                    # Add new repository section in the commits area
                    if "### Commits" in content:
                        # Find the end of the commits section and insert there
                        commits_section_start = content.find("### Commits")
                        # Look for the end of the commits section (before next ## or end of file)
                        next_section = content.find("\n## ", commits_section_start)
                        if next_section == -1:
                            # No next section, add at the end
                            new_content = content + "\n" + repo_data
                        else:
                            # Insert before the next section
                            new_content = content[:next_section] + "\n" + repo_data + content[next_section:]
                    else:
                        # Add at the end of GitHub Activity section
                        github_section_start = content.find("## GitHub Activity")
                        if github_section_start != -1:
                            # Find end of GitHub Activity section
                            next_section = content.find("\n## ", github_section_start)
                            if next_section == -1:
                                new_content = content + "\n" + repo_data
                            else:
                                new_content = content[:next_section] + "\n" + repo_data + content[next_section:]
                        else:
                            # Fallback: add at the end
                            new_content = content + "\n" + repo_data
                    print(f"   ➕ Added new {repo_name} data to calendar")
                
                # Write updated content
                with open(calendar_file, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                
                # Update activity summary
                self._update_activity_summary(calendar_file, result)
                
                print(f"   ✅ Successfully updated {repo_name} data in calendar")
            
        except Exception as e:
            self.logger.error(f"Error writing {repo_name} data to calendar: {e}")
            print(f"❌ Error writing {repo_name} data to calendar: {e}")
            # Restore from backup if writing failed
            self._restore_from_backup(calendar_file)
    
    def _format_repo_data_for_calendar(self, repo_name, result):
        """Format repository data for calendar display"""
        if not result.get('commits'):
            return ""
        
        formatted_lines = [f"**{repo_name}:**"]
        for commit in result['commits']:
            message = commit['message'].split('\n')[0]  # First line only
            formatted_lines.append(f"- `{commit['sha']}` {message}")
        formatted_lines.append("")  # Empty line after repository
        
        return "\n".join(formatted_lines)
    
    def _update_activity_summary(self, calendar_file, result):
        """Update the activity summary in the calendar file"""
        try:
            with open(calendar_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Count total commits in the file
            commit_count = content.count("- `")
            
            # Update activity summary
            pattern = r"\*\*Activity Summary:\*\* \d+ commits"
            replacement = f"**Activity Summary:** {commit_count} commits"
            new_content = re.sub(pattern, replacement, content)
            
            with open(calendar_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
                
        except Exception as e:
            self.logger.error(f"Error updating activity summary: {e}")
    
    def _create_backup(self, calendar_file):
        """Create a backup of the calendar file before modification"""
        try:
            backup_file = calendar_file.with_suffix('.backup')
            with open(calendar_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            self.logger.info(f"Created backup: {backup_file}")
        except Exception as e:
            self.logger.error(f"Error creating backup: {e}")
    
    def _restore_from_backup(self, calendar_file):
        """Restore calendar file from backup if modification failed"""
        try:
            backup_file = calendar_file.with_suffix('.backup')
            if backup_file.exists():
                with open(backup_file, 'r', encoding='utf-8') as src:
                    with open(calendar_file, 'w', encoding='utf-8') as dst:
                        dst.write(src.read())
                self.logger.info(f"Restored from backup: {backup_file}")
                print(f"🔄 Restored calendar file from backup due to error")
            else:
                self.logger.error(f"Backup file not found: {backup_file}")
        except Exception as e:
            self.logger.error(f"Error restoring from backup: {e}")
    
    def _update_calendar_with_results(self, results, target_date):
        """Update calendar entry with the parallel processing results"""
        try:
            # Aggregate all the results
            all_commits = []
            all_prs = []
            all_issues = []
            successful_repos = []
            
            for repo_name, result in results:
                if "error" not in result:
                    all_commits.extend(result.get('commits', []))
                    all_prs.extend(result.get('pull_requests', []))
                    all_issues.extend(result.get('issues', []))
                    successful_repos.append(repo_name)
            
            # Create a temporary data fetcher to handle calendar updates
            temp_fetcher = GitHubDailyMetrics(str(self.obsidian_path))
            
            # Set the aggregated data
            temp_fetcher.daily_metrics = {
                'commits': all_commits,
                'pull_requests': all_prs,
                'issues': all_issues,
                'repositories': successful_repos,
                'contributions': len(all_commits)
            }
            
            # Get the calendar file path
            calendar_file = temp_fetcher.get_calendar_file_path(target_date)
            
            # Format the metrics for calendar
            github_content = temp_fetcher.format_metrics_for_calendar(target_date)
            
            if not github_content:
                print(f"No GitHub activity found for {target_date}")
                return
            
            # Read existing content if file exists
            existing_content = ""
            if calendar_file.exists():
                with open(calendar_file, 'r', encoding='utf-8') as f:
                    existing_content = f.read()
            
            # Check if GitHub section already exists
            if "## GitHub Activity" in existing_content:
                print(f"GitHub section already exists in {calendar_file.name}, updating...")
                # Replace existing GitHub section
                import re
                pattern = r"## GitHub Activity.*?(?=\n##|\n$)"
                new_content = re.sub(pattern, github_content, existing_content, flags=re.DOTALL)
            else:
                # Add GitHub section at the end
                if existing_content.strip():
                    new_content = existing_content.rstrip() + "\n\n" + github_content
                else:
                    # Create new file with basic structure
                    new_content = f"# {target_date.strftime('%B %d, %Y')}\n\n## Daily Notes\n\n{github_content}"
            
            # Write the updated content
            with open(calendar_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Calendar updated: {calendar_file}")
            
        except Exception as e:
            self.logger.error(f"Error updating calendar: {e}")
            print(f"❌ Error updating calendar: {e}")
    
    def _print_summary(self, results, target_date):
        """Print a summary of the results"""
        print("=" * 60)
        print("🎉 PARALLEL REPOSITORY PROCESSING COMPLETED!")
        print("=" * 60)
        print(f"📅 Date processed: {target_date}")
        print(f"📊 Total repositories processed: {len(results)}")
        
        # Count successful vs failed
        successful = sum(1 for _, result in results if "error" not in result)
        failed = len(results) - successful
        
        print(f"✅ Successful: {successful}")
        print(f"❌ Failed: {failed}")
        
        if failed > 0:
            print(f"\n⚠️  Failed repositories:")
            for repo_name, result in results:
                if "error" in result:
                    print(f"   {repo_name}: {result['error']}")
        
        # Show activity summary
        total_commits = 0
        total_prs = 0
        total_issues = 0
        
        for repo_name, result in results:
            if "error" not in result:
                total_commits += len(result.get('commits', []))
                total_prs += len(result.get('pull_requests', []))
                total_issues += len(result.get('issues', []))
        
        print(f"\n📈 Activity Summary:")
        print(f"   📝 Total commits: {total_commits}")
        print(f"   🔄 Total PRs: {total_prs}")
        print(f"   🐛 Total issues: {total_issues}")
        
        print("=" * 60)

def main():
    """Main function"""
    if len(sys.argv) < 2:
        print("Usage: python3 parallel_repo_runner.py <obsidian_path> [target_date]")
        print("Example: python3 parallel_repo_runner.py . 2025-09-01")
        print("If no date provided, uses today's date")
        sys.exit(1)
    
    obsidian_path = sys.argv[1]
    
    # Parse target date
    if len(sys.argv) > 2:
        try:
            target_date = datetime.strptime(sys.argv[2], '%Y-%m-%d').date()
        except ValueError:
            print("❌ Invalid date format. Use YYYY-MM-DD")
            sys.exit(1)
    else:
        target_date = date.today()
    
    try:
        runner = ParallelRepoRunner(obsidian_path)
        results = runner.run_for_date(target_date)
        print("✅ Parallel repository processing completed successfully!")
        
    except Exception as e:
        print(f"❌ Parallel repository processing failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
