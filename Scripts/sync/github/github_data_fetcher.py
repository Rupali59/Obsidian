#!/usr/bin/env python3
"""
GitHub Daily Metrics Capture
Automatically captures GitHub activity metrics for the previous day
and integrates them into Obsidian calendar entries while preserving existing content.
"""

import os
import re
import requests
import json
from pathlib import Path
from datetime import datetime, timedelta, date
import argparse
import logging
from typing import List, Dict, Optional, Union
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('github_daily_metrics.log'),
        logging.StreamHandler()
    ]
)

class GitHubDailyMetrics:
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        self.calendar_path = self.obsidian_path / "Calendar"
        # Use absolute path for config
        self.config_path = self.obsidian_path / "Scripts" / "config" / "github_config.env"
        
        # GitHub API configuration
        self.github_token = None
        self.github_username = None
        self.api_base = "https://api.github.com"
        
        # Load configuration
        self.load_config()
        
        # Setup API headers
        self.headers = {
            "Authorization": f"token {self.github_token}",
            "Accept": "application/vnd.github.v3+json",
            "User-Agent": "GitHub-Daily-Metrics/1.0"
        }
        
        # Auto-detect username if not set (after headers are created)
        if not self.github_username:
            self.detect_username()
        
        # Metrics storage
        self.daily_metrics = {
            'commits': [],
            'pull_requests': [],
            'issues': [],
            'repositories': [],
            'contributions': 0
        }
    
    def load_config(self):
        """Load configuration from the config file"""
        try:
            if not os.path.exists(self.config_path):
                logging.error(f"Configuration file not found: {self.config_path}")
                raise FileNotFoundError(f"Please run Phase 1 configuration first: {self.config_path}")
            
            with open(self.config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line and not line.startswith('#'):
                        if '=' in line:
                            key, value = line.split('=', 1)
                            key = key.strip()
                            value = value.strip()
                            
                            if key == 'GITHUB_TOKEN':
                                self.github_token = value
                            elif key == 'GITHUB_USERNAME':
                                self.github_username = value
            
            if not self.github_token or self.github_token == 'your_github_token_here':
                logging.error("GitHub token not configured. Please update github_config.env")
                raise ValueError("GitHub token not configured")
                
        except Exception as e:
            logging.error(f"Failed to load configuration: {e}")
            raise
    
    def detect_username(self):
        """Auto-detect GitHub username from API"""
        try:
            response = requests.get(f"{self.api_base}/user", headers=self.headers)
            response.raise_for_status()
            user_data = response.json()
            self.github_username = user_data['login']
            logging.info(f"Auto-detected GitHub username: {self.github_username}")
        except Exception as e:
            logging.error(f"Failed to auto-detect username: {e}")
            raise
    
    def get_yesterday_date(self) -> date:
        """Get yesterday's date"""
        return date.today() - timedelta(days=1)
    
    def get_calendar_file_path(self, target_date: date) -> Path:
        """Get the calendar file path for a specific date"""
        year = target_date.year
        month = target_date.strftime("%B")
        day = target_date.strftime("%d")
        month_num = target_date.strftime("%m")
        
        calendar_file = self.calendar_path / str(year) / month / f"{day}-{month_num}-{year}.md"
        
        # Ensure directory exists
        calendar_file.parent.mkdir(parents=True, exist_ok=True)
        
        return calendar_file
    
    def capture_github_metrics(self, target_date: date):
        """Capture GitHub metrics for a specific date"""
        logging.info(f"Capturing GitHub metrics for {target_date}")
        
        # Convert date to ISO format for GitHub API
        since_time = datetime.combine(target_date, datetime.min.time()).isoformat() + 'Z'
        until_time = datetime.combine(target_date + timedelta(days=1), datetime.min.time()).isoformat() + 'Z'
        
        try:
            # Get user's repositories
            repos = self.get_user_repositories()
            
            # Capture metrics for each repository
            for repo in repos:
                repo_name = repo['full_name']
                logging.info(f"Processing repository: {repo_name}")
                
                # Get commits for the day
                commits = self.get_repository_commits(repo_name, since_time, until_time)
                if commits:
                    self.daily_metrics['commits'].extend([
                        {
                            'repo': repo_name,
                            'sha': commit['sha'][:7],
                            'message': commit['commit']['message'],
                            'author': commit['commit']['author']['name'],
                            'date': commit['commit']['author']['date']
                        }
                        for commit in commits
                    ])
                
                # Get pull requests
                prs = self.get_repository_pull_requests(repo_name, since_time, until_time)
                if prs:
                    self.daily_metrics['pull_requests'].extend([
                        {
                            'repo': repo_name,
                            'number': pr['number'],
                            'title': pr['title'],
                            'state': pr['state'],
                            'author': pr['user']['login'],
                            'created_at': pr['created_at']
                        }
                        for pr in prs
                    ])
                
                # Get issues
                issues = self.get_repository_issues(repo_name, since_time, until_time)
                if issues:
                    self.daily_metrics['issues'].extend([
                        {
                            'repo': repo_name,
                            'number': issue['number'],
                            'title': issue['title'],
                            'state': issue['state'],
                            'author': issue['user']['login'],
                            'created_at': issue['created_at']
                        }
                        for issue in issues
                    ])
                
                # Rate limiting
                time.sleep(0.1)
            
            # Get user contributions
            self.daily_metrics['contributions'] = self.get_user_contributions(target_date)
            
            logging.info(f"Captured metrics: {len(self.daily_metrics['commits'])} commits, "
                        f"{len(self.daily_metrics['pull_requests'])} PRs, "
                        f"{len(self.daily_metrics['issues'])} issues")
            
        except Exception as e:
            logging.error(f"Failed to capture GitHub metrics: {e}")
            raise
    
    def get_user_repositories(self) -> List[Dict]:
        """Get all repositories for the authenticated user"""
        repos = []
        page = 1
        
        while True:
            try:
                response = requests.get(
                    f"{self.api_base}/user/repos",
                    headers=self.headers,
                    params={'page': page, 'per_page': 100, 'sort': 'updated'}
                )
                response.raise_for_status()
                
                page_repos = response.json()
                if not page_repos:
                    break
                
                repos.extend(page_repos)
                page += 1
                
                # Rate limiting
                time.sleep(0.1)
                
            except Exception as e:
                logging.error(f"Failed to get repositories: {e}")
                break
        
        return repos
    
    def get_repository_commits(self, repo_name: str, since_time: str, until_time: str) -> List[Dict]:
        """Get commits for a repository within a time range"""
        try:
            response = requests.get(
                f"{self.api_base}/repos/{repo_name}/commits",
                headers=self.headers,
                params={
                    'since': since_time,
                    'until': until_time,
                    'per_page': 100
                }
            )
            response.raise_for_status()
            return response.json()
        except Exception as e:
            logging.error(f"Failed to get commits for {repo_name}: {e}")
            return []
    
    def get_repository_pull_requests(self, repo_name: str, since_time: str, until_time: str) -> List[Dict]:
        """Get pull requests for a repository within a time range"""
        try:
            response = requests.get(
                f"{self.api_base}/repos/{repo_name}/pulls",
                headers=self.headers,
                params={
                    'state': 'all',
                    'per_page': 100
                }
            )
            response.raise_for_status()
            
            # Filter by date range
            prs = response.json()
            filtered_prs = []
            since_dt = datetime.fromisoformat(since_time.replace('Z', '+00:00'))
            until_dt = datetime.fromisoformat(until_time.replace('Z', '+00:00'))
            
            for pr in prs:
                pr_date = datetime.fromisoformat(pr['created_at'].replace('Z', '+00:00'))
                if since_dt <= pr_date < until_dt:
                    filtered_prs.append(pr)
            
            return filtered_prs
        except Exception as e:
            logging.error(f"Failed to get pull requests for {repo_name}: {e}")
            return []
    
    def get_repository_issues(self, repo_name: str, since_time: str, until_time: str) -> List[Dict]:
        """Get issues for a repository within a time range"""
        try:
            response = requests.get(
                f"{self.api_base}/repos/{repo_name}/issues",
                headers=self.headers,
                params={
                    'state': 'all',
                    'per_page': 100
                }
            )
            response.raise_for_status()
            
            # Filter by date range and exclude pull requests
            issues = response.json()
            filtered_issues = []
            since_dt = datetime.fromisoformat(since_time.replace('Z', '+00:00'))
            until_dt = datetime.fromisoformat(until_time.replace('Z', '+00:00'))
            
            for issue in issues:
                # Skip pull requests (they have pull_request field)
                if 'pull_request' in issue:
                    continue
                
                issue_date = datetime.fromisoformat(issue['created_at'].replace('Z', '+00:00'))
                if since_dt <= issue_date < until_dt:
                    filtered_issues.append(issue)
            
            return filtered_issues
        except Exception as e:
            logging.error(f"Failed to get issues for {repo_name}: {e}")
            return []
    
    def get_user_contributions(self, target_date: date) -> int:
        """Get user's contribution count for a specific date"""
        try:
            # Note: GitHub's GraphQL API would be better for this, but REST API is simpler
            # For now, we'll estimate based on commits
            return len(self.daily_metrics['commits'])
        except Exception as e:
            logging.error(f"Failed to get user contributions: {e}")
            return 0
    
    def _get_repository_metrics(self, repo_name: str, target_date: date) -> Dict:
        """Get metrics for a specific repository on a specific date"""
        try:
            # Convert date to ISO format for API calls
            since_time = target_date.isoformat() + "T00:00:00Z"
            until_time = target_date.isoformat() + "T23:59:59Z"
            
            # Get all metrics for this repository
            commits = self.get_repository_commits(repo_name, since_time, until_time)
            pull_requests = self.get_repository_pull_requests(repo_name, since_time, until_time)
            issues = self.get_repository_issues(repo_name, since_time, until_time)
            
            return {
                'commits': commits,
                'pull_requests': pull_requests,
                'issues': issues,
                'repository': repo_name,
                'date': target_date.isoformat()
            }
            
        except Exception as e:
            logging.error(f"Error getting metrics for {repo_name}: {e}")
            return {"error": str(e)}
    
    def format_metrics_for_calendar(self, target_date: date) -> str:
        """Format the captured metrics for calendar entry"""
        if not any([self.daily_metrics['commits'], self.daily_metrics['pull_requests'], 
                   self.daily_metrics['issues']]):
            return ""
        
        formatted_content = []
        
        # Summary section
        total_commits = len(self.daily_metrics['commits'])
        total_prs = len(self.daily_metrics['pull_requests'])
        total_issues = len(self.daily_metrics['issues'])
        
        if total_commits > 0 or total_prs > 0 or total_issues > 0:
            formatted_content.append("## GitHub Activity")
            formatted_content.append("")
            
            # Activity summary
            activity_summary = []
            if total_commits > 0:
                activity_summary.append(f"{total_commits} commit{'s' if total_commits != 1 else ''}")
            if total_prs > 0:
                activity_summary.append(f"{total_prs} pull request{'s' if total_prs != 1 else ''}")
            if total_issues > 0:
                activity_summary.append(f"{total_issues} issue{'s' if total_issues != 1 else ''}")
            
            formatted_content.append(f"**Activity Summary:** {', '.join(activity_summary)}")
            formatted_content.append("")
        
        # Commits section
        if self.daily_metrics['commits']:
            formatted_content.append("### Commits")
            formatted_content.append("")
            
            # Group commits by repository
            commits_by_repo = {}
            for commit in self.daily_metrics['commits']:
                repo = commit['repo']
                if repo not in commits_by_repo:
                    commits_by_repo[repo] = []
                commits_by_repo[repo].append(commit)
            
            for repo, commits in commits_by_repo.items():
                repo_name = repo.split('/')[-1]  # Extract just the repo name
                formatted_content.append(f"**{repo_name}:**")
                for commit in commits:
                    message = commit['message'].split('\n')[0]  # First line only
                    if len(message) > 80:
                        message = message[:77] + "..."
                    formatted_content.append(f"- `{commit['sha']}` {message}")
                formatted_content.append("")
        
        # Pull Requests section
        if self.daily_metrics['pull_requests']:
            formatted_content.append("### Pull Requests")
            formatted_content.append("")
            
            for pr in self.daily_metrics['pull_requests']:
                repo_name = pr['repo'].split('/')[-1]
                state_emoji = "🟢" if pr['state'] == 'open' else "🟡" if pr['state'] == 'closed' else "🔴"
                formatted_content.append(f"- {state_emoji} **{repo_name}#{pr['number']}** {pr['title']}")
            formatted_content.append("")
        
        # Issues section
        if self.daily_metrics['issues']:
            formatted_content.append("### Issues")
            formatted_content.append("")
            
            for issue in self.daily_metrics['issues']:
                repo_name = issue['repo'].split('/')[-1]
                state_emoji = "🟢" if issue['state'] == 'open' else "🟡"
                formatted_content.append(f"- {state_emoji} **{repo_name}#{issue['number']}** {issue['title']}")
            formatted_content.append("")
        
        return "\n".join(formatted_content)
    
    def update_calendar_entry(self, target_date: date):
        """Update the calendar entry with GitHub metrics while preserving existing content"""
        calendar_file = self.get_calendar_file_path(target_date)
        
        # Capture metrics first
        self.capture_github_metrics(target_date)
        
        # Format the new content
        github_content = self.format_metrics_for_calendar(target_date)
        
        if not github_content:
            logging.info(f"No GitHub activity found for {target_date}")
            return
        
        # Read existing content if file exists
        existing_content = ""
        if calendar_file.exists():
            with open(calendar_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
        
        # Check if GitHub section already exists
        if "## GitHub Activity" in existing_content:
            logging.info(f"GitHub section already exists in {calendar_file.name}, updating...")
            # Replace existing GitHub section
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
        
        logging.info(f"Updated calendar entry: {calendar_file}")
    
    def run_daily_capture(self):
        """Run the daily capture for yesterday's date"""
        try:
            yesterday = self.get_yesterday_date()
            logging.info(f"Running daily GitHub metrics capture for {yesterday}")
            
            self.update_calendar_entry(yesterday)
            
            logging.info("Daily GitHub metrics capture completed successfully")
            
        except Exception as e:
            logging.error(f"Daily GitHub metrics capture failed: {e}")
            raise

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="GitHub Daily Metrics Capture")
    parser.add_argument("--obsidian-path", default=".", help="Path to Obsidian vault")
    parser.add_argument("--date", help="Specific date to capture (YYYY-MM-DD), defaults to yesterday")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be captured without writing")
    
    args = parser.parse_args()
    
    try:
        # Initialize the metrics capture
        metrics_capture = GitHubDailyMetrics(args.obsidian_path)
        
        if args.date:
            # Capture for specific date
            target_date = datetime.strptime(args.date, "%Y-%m-%d").date()
            metrics_capture.update_calendar_entry(target_date)
        else:
            # Default: capture for yesterday
            metrics_capture.run_daily_capture()
        
        print("✅ GitHub daily metrics capture completed successfully!")
        
    except Exception as e:
        logging.error(f"Script failed: {e}")
        print(f"❌ Script failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
