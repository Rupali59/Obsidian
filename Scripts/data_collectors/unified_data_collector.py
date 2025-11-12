#!/usr/bin/env python3
"""
Unified Data Collector
Combines GitHub and Wakatime data collection with Obsidian integration
Uses configuration file for all settings and supports both API and dashboard scraping
"""

import os
import sys
import json
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
import time
from pathlib import Path
from datetime import datetime, date, timedelta
from typing import Dict, List, Optional, Union

# GitHub API functionality is now integrated directly into this script

class SimpleGitHubCollector:
    """Simple GitHub data collector integrated into unified collector"""
    
    def __init__(self, token: str, username: str, repositories: List[str]):
        self.token = token
        self.username = username
        self.repositories = repositories
        self.api_base = "https://api.github.com"
        self.headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def _fetch_repo_data(self, repo: str, date_str: str) -> Dict:
        """Fetch data for a single repository (called in parallel)"""
        repo_commits = 0
        repo_prs = 0
        repo_issues = 0
        seen_commits = set()  # Track unique commit SHAs to avoid duplicates
        commit_details = []  # Store actual commit details
        
        # Normalize repository to owner/repo if a URL was provided
        owner_repo = repo
        if 'github.com' in owner_repo:
            owner_repo = owner_repo.split('github.com/')[-1].strip('/')
            owner_repo = '/'.join(owner_repo.split('/')[:2])

        # Get all branches first
        if '/' in owner_repo:
            branches_url = f"{self.api_base}/repos/{owner_repo}/branches"
        else:
            branches_url = f"{self.api_base}/repos/{self.username}/{repo}/branches"
        
        branches = []
        try:
            response = requests.get(branches_url, headers=self.headers, timeout=10)
            if response.status_code == 200:
                branches_data = response.json()
                branches = [b['name'] for b in branches_data]
        except Exception as e:
            logging.warning(f"Failed to fetch branches for {repo}, will try default branch: {e}")
            branches = []  # Will fall back to default branch
        
        # If no branches found, fetch from default branch (no branch param)
        if not branches:
            branches = [None]  # None means use default branch
        
        # Get commits from all branches
        for branch in branches:
            if '/' in owner_repo:
                commits_url = f"{self.api_base}/repos/{owner_repo}/commits"
            else:
                commits_url = f"{self.api_base}/repos/{self.username}/{repo}/commits"
            
            params = {'since': f"{date_str}T00:00:00Z", 'per_page': 100}
            if branch:  # Add branch parameter if specified
                params['sha'] = branch
            
            try:
                response = requests.get(commits_url, headers=self.headers, params=params, timeout=10)
                if response.status_code == 200:
                    commits_data = response.json()
                    for commit in commits_data:
                        commit_sha = commit['sha']
                        commit_date = commit['commit']['committer']['date'][:10]
                        
                        # Only count unique commits on the target date
                        if commit_date == date_str and commit_sha not in seen_commits:
                            seen_commits.add(commit_sha)
                            repo_commits += 1
                            
                            # Store commit details
                            commit_msg = commit.get('commit', {}).get('message', '')
                            commit_author = commit.get('commit', {}).get('author', {}).get('name', 'Unknown')
                            commit_url = commit.get('html_url', '')
                            
                            commit_details.append({
                                'sha': commit_sha[:7],  # Short SHA
                                'message': commit_msg.split('\n')[0],  # First line only
                                'author': commit_author,
                                'url': commit_url
                            })
                        elif commit_date < date_str:
                            break
            except Exception as e:
                logging.warning(f"Failed to fetch commits for {repo} (branch: {branch}): {e}")
        
        # Get pull requests
        if '/' in owner_repo:
            prs_url = f"{self.api_base}/repos/{owner_repo}/pulls"
        else:
            prs_url = f"{self.api_base}/repos/{self.username}/{repo}/pulls"
        params = {'state': 'all', 'since': f"{date_str}T00:00:00Z"}
        
        try:
            response = requests.get(prs_url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                prs_data = response.json()
                repo_prs = len([pr for pr in prs_data if pr['created_at'].startswith(date_str)])
        except Exception as e:
            logging.warning(f"Failed to fetch PRs for {repo}: {e}")
        
        # Get issues
        if '/' in owner_repo:
            issues_url = f"{self.api_base}/repos/{owner_repo}/issues"
        else:
            issues_url = f"{self.api_base}/repos/{self.username}/{repo}/issues"
        params = {'state': 'all', 'since': f"{date_str}T00:00:00Z"}
        
        try:
            response = requests.get(issues_url, headers=self.headers, params=params, timeout=10)
            if response.status_code == 200:
                issues_data = response.json()
                repo_issues = len([issue for issue in issues_data if issue['created_at'].startswith(date_str)])
        except Exception as e:
            logging.warning(f"Failed to fetch issues for {repo}: {e}")
        
        display_name = owner_repo.split('/')[-1] if '/' in owner_repo else repo
        return {
            'repo': display_name,
            'commits': repo_commits,
            'prs': repo_prs,
            'issues': repo_issues,
            'commit_details': commit_details
        }
    
    def collect_data_for_date(self, target_date: date) -> Dict:
        """Collect GitHub data for a specific date (parallelized per repo)"""
        commits = 0
        prs = 0
        issues = 0
        repository_details = {}
        
        date_str = target_date.strftime('%Y-%m-%d')
        
        # Fetch data from all repos in parallel
        with ThreadPoolExecutor(max_workers=10) as executor:
            futures = {
                executor.submit(self._fetch_repo_data, repo, date_str): repo 
                for repo in self.repositories
            }
            
            for future in as_completed(futures):
                try:
                    result = future.result()
                    repo_commits = result['commits']
                    repo_prs = result['prs']
                    repo_issues = result['issues']
                    repo_commit_details = result.get('commit_details', [])
                    
                    commits += repo_commits
                    prs += repo_prs
                    issues += repo_issues
                    
                    # Store per-repository details if there's activity
                    if repo_commits > 0 or repo_prs > 0 or repo_issues > 0:
                        repository_details[result['repo']] = {
                            'commits': repo_commits,
                            'prs': repo_prs,
                            'issues': repo_issues,
                            'commit_details': repo_commit_details
                        }
                except Exception as e:
                    repo = futures[future]
                    logging.error(f"Error processing {repo}: {e}")
        
        return {
            'commits': commits,
            'prs': prs,
            'issues': issues,
            'repository_details': repository_details
        }

# -------- Parallel commit fetching utilities (no Obsidian dependency) --------

def _normalize_repo_identifier(raw_repo: str, default_username: str) -> str:
    """Convert various repo formats to owner/repo"""
    if not raw_repo:
        return ""
    if 'github.com' in raw_repo:
        # Expecting formats like https://github.com/owner/repo or owner/repo
        parts = raw_repo.split('github.com/')[-1].strip('/')
        # parts could contain extra path segments; keep first two
        owner_repo = '/'.join(parts.split('/')[:2])
        return owner_repo
    if '/' in raw_repo:
        return raw_repo
    # Just repo name; prefix username
    return f"{default_username}/{raw_repo}"

def _fetch_repo_commits(owner_repo: str, token: str, since_iso: str, until_iso: str) -> Dict:
    """Fetch commits for a single repo within date range."""
    api_base = "https://api.github.com"
    headers = {
        'Authorization': f'token {token}',
        'Accept': 'application/vnd.github.v3+json'
    }
    url = f"{api_base}/repos/{owner_repo}/commits"
    params = {
        'since': since_iso,
        'until': until_iso,
        'per_page': 100
    }
    try:
        resp = requests.get(url, headers=headers, params=params, timeout=30)
        if resp.status_code != 200:
            return { 'repository': owner_repo, 'error': f"HTTP {resp.status_code}", 'commits': [] }
        data = resp.json()
        commits = []
        for c in data:
            commit_obj = c.get('commit', {})
            message = commit_obj.get('message', '') or ''
            title, _, body = message.partition('\n\n')
            commits.append({
                'sha': c.get('sha'),
                'html_url': c.get('html_url'),
                'title': title.strip(),
                'description': body.strip(),
                'author': (commit_obj.get('author') or {}).get('name'),
                'date': (commit_obj.get('author') or {}).get('date')
            })
        return { 'repository': owner_repo, 'commits': commits }
    except Exception as e:
        return { 'repository': owner_repo, 'error': str(e), 'commits': [] }

def fetch_commits_parallel_from_config(config_path: str, since_date: date, until_date: date) -> Dict:
    """Fetch commits in parallel for all repos in config between dates (inclusive)."""
    with open(config_path, 'r') as f:
        cfg = json.load(f)
    gh_cfg = cfg.get('github', {})
    token = gh_cfg.get('api_token', '')
    username = gh_cfg.get('username', '')
    raw_repos = gh_cfg.get('repositories', [])
    repos = [_normalize_repo_identifier(r, username) for r in raw_repos]

    since_iso = f"{since_date.isoformat()}T00:00:00Z"
    # Use end of day for until
    until_iso = f"{until_date.isoformat()}T23:59:59Z"

    results: Dict[str, List[Dict]] = {}
    errors: Dict[str, str] = {}
    with ThreadPoolExecutor(max_workers=min(8, max(1, len(repos)))) as executor:
        future_map = {
            executor.submit(_fetch_repo_commits, repo, token, since_iso, until_iso): repo
            for repo in repos
        }
        for fut in as_completed(future_map):
            repo = future_map[fut]
            res = fut.result()
            if 'error' in res and res['error']:
                errors[repo] = res['error']
            results[repo] = res.get('commits', [])

    summary = {
        'since': since_date.isoformat(),
        'until': until_date.isoformat(),
        'total_repositories': len(repos),
        'total_commits': sum(len(c) for c in results.values()),
        'repositories': results,
        'errors': errors
    }
    return summary

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('unified_data_collector.log'),
        logging.StreamHandler()
    ]
)

class UnifiedDataCollector:
    def __init__(self, config_path: str):
        self.config_path = Path(config_path)
        self.config = self._load_config()
        self.obsidian_path = Path(self.config['obsidian']['vault_path'])
        self.calendar_path = self.obsidian_path / "Calendar"
        self.logger = logging.getLogger(__name__)
        
        # Initialize collectors
        self.github_collector = None
        self.wakatime_collector = None
        
        # GitHub configuration from unified config
        self.github_config = self.config.get('github', {})
        self.github_token = self.github_config.get('api_token', '')
        self.github_username = self.github_config.get('username', '')
        
        print(f"🚀 Unified Data Collector initialized")
        print(f"📁 Obsidian path: {self.obsidian_path}")
        print(f"📅 Calendar path: {self.calendar_path}")
        print(f"⚙️  Config: {self.config_path}")
        
        # Show enabled services
        github_enabled = self.config.get('github', {}).get('enabled', False)
        wakatime_enabled = self.config.get('wakatime', {}).get('enabled', False)
        print(f"🔧 Services: GitHub={'✅' if github_enabled else '❌'}, Wakatime={'✅' if wakatime_enabled else '❌'}")
    
    def _load_config(self) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(self.config_path, 'r') as f:
                config = json.load(f)
            return config
        except Exception as e:
            print(f"❌ Failed to load config: {e}")
            return {}
    
    def initialize_collectors(self):
        """Initialize GitHub and Wakatime collectors based on config"""
        try:
            # Initialize GitHub collector
            if self.config.get('github', {}).get('enabled', False):
                print("🔧 Initializing GitHub collector...")
                repositories = self.github_config.get('repositories', [])
                # Keep full repo names as they are in the config
                repo_names = repositories
                
                self.github_collector = SimpleGitHubCollector(
                    self.github_token, 
                    self.github_username, 
                    repo_names
                )
                print("✅ GitHub collector initialized")
            
            # Initialize Wakatime collector
            if self.config.get('wakatime', {}).get('enabled', False):
                print("🔧 Initializing Wakatime collector...")
                self.wakatime_collector = WakatimeAPIClient(str(self.config_path))
                
                # Test API connection
                if self.wakatime_collector.test_api_connection():
                    print("✅ Wakatime API collector initialized")
                else:
                    print("⚠️  Wakatime API connection failed, will use mock data")
                    # Fallback to mock data when API fails
                    self.wakatime_collector = None
                    print("✅ Wakatime fallback to mock data initialized")
            else:
                print("⏭️  Wakatime collector disabled in config")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize collectors: {e}")
            return False
    
    def collect_github_data(self, target_date: date) -> Dict:
        """Collect GitHub data for the target date"""
        if not self.github_collector:
            print("⚠️  GitHub collector not initialized")
            return {}
        
        try:
            print(f"📊 Collecting GitHub data for {target_date}...")
            result = self.github_collector.collect_data_for_date(target_date)
            
            # Format for calendar entry
            github_data = {
                'commits': result.get('commits', 0),
                'prs': result.get('prs', 0),
                'issues': result.get('issues', 0),
                'repository_details': result.get('repository_details', {})
            }
            
            print(f"✅ GitHub data collected: {github_data['commits']} commits, {github_data['prs']} PRs, {github_data['issues']} issues")
            return github_data
                
        except Exception as e:
            print(f"❌ GitHub data collection failed: {e}")
            return {}
    
    def collect_wakatime_data(self, target_date: date) -> Dict:
        """Collect Wakatime data for the target date"""
        if not self.wakatime_collector:
            print("⚠️  Wakatime collector not initialized, using mock data")
            return self._get_mock_wakatime_data(target_date)
        
        try:
            print(f"📊 Collecting Wakatime data for {target_date}...")
            
            # Try API first
            if hasattr(self.wakatime_collector, 'get_daily_summary'):
                daily_data = self.wakatime_collector.get_daily_summary(target_date)
                stats_data = self.wakatime_collector.get_stats_summary("last_7_days")
                
                wakatime_data = {
                    'date': target_date.strftime('%Y-%m-%d'),
                    'daily_data': daily_data,
                    'stats_data': stats_data,
                    'source': 'api'
                }
                
                print(f"✅ Wakatime data collected via API")
                return wakatime_data
            
            else:
                print("❌ No valid Wakatime collector method available, using mock data")
                return self._get_mock_wakatime_data(target_date)
                
        except Exception as e:
            print(f"❌ Error collecting Wakatime data: {e}, using mock data")
            return self._get_mock_wakatime_data(target_date)
    
    def _get_mock_wakatime_data(self, target_date: date) -> Dict:
        """Generate mock Wakatime data for testing"""
        return {
            'date': target_date.strftime('%Y-%m-%d'),
            'daily_data': {
                'total_time': '4h 32m',
                'total_seconds': 16320,
                'languages': [
                    {'name': 'Python', 'time': '2h 15m', 'seconds': 8100, 'percentage': '49.8%'},
                    {'name': 'JavaScript', 'time': '1h 30m', 'seconds': 5400, 'percentage': '33.2%'},
                    {'name': 'TypeScript', 'time': '47m', 'seconds': 2820, 'percentage': '17.0%'}
                ],
                'projects': [
                    {'name': 'obsidian-vault', 'time': '2h 10m', 'seconds': 7800, 'percentage': '47.8%'},
                    {'name': 'ssjk-crm', 'time': '1h 45m', 'seconds': 6300, 'percentage': '38.6%'},
                    {'name': 'quartz-site', 'time': '37m', 'seconds': 2220, 'percentage': '13.6%'}
                ],
                'editors': [
                    {'name': 'VS Code', 'time': '3h 20m', 'seconds': 12000, 'percentage': '73.5%'},
                    {'name': 'Cursor', 'time': '1h 12m', 'seconds': 4320, 'percentage': '26.5%'}
                ],
                'operating_systems': [
                    {'name': 'macOS', 'time': '4h 32m', 'seconds': 16320, 'percentage': '100.0%'}
                ]
            },
            'stats_data': {
                'total_time': '28h 45m',
                'daily_average': 4.1,
                'best_day': {
                    'date': '2025-09-08',
                    'time': '6h 15m',
                    'seconds': 22500
                }
            },
            'source': 'mock'
        }
    
    def format_github_content(self, github_data: Dict) -> str:
        """Format GitHub data for calendar entry"""
        if not github_data:
            return ""
        
        content = []
        content.append("## GitHub Activity")
        content.append("")
        content.append(f"**Activity Summary:** {github_data['commits']} commits, {github_data['prs']} PRs, {github_data['issues']} issues")
        content.append("")
        
        # Development Summary
        content.append("### Development Summary")
        content.append("")
        content.append("**🔧 Components Worked On:**")
        content.append("")
        
        # Repository details with commit details
        for repo_name, repo_metrics in github_data.get('repository_details', {}).items():
            if repo_metrics.get('commits', 0) > 0 or repo_metrics.get('prs', 0) > 0 or repo_metrics.get('issues', 0) > 0:
                content.append(f"#### **{repo_name}**")
                content.append(f"- **Commits**: {repo_metrics.get('commits', 0)}")
                content.append(f"- **Pull Requests**: {repo_metrics.get('prs', 0)}")
                content.append(f"- **Issues**: {repo_metrics.get('issues', 0)}")
                
                # Add commit details if available
                commit_details = repo_metrics.get('commit_details', [])
                if commit_details:
                    content.append("")
                    content.append("**📝 Commits:**")
                    for commit in commit_details:
                        sha = commit.get('sha', 'unknown')
                        message = commit.get('message', 'No message')
                        url = commit.get('url', '')
                        if url:
                            content.append(f"- [`{sha}`]({url}) {message}")
                        else:
                            content.append(f"- `{sha}` {message}")
                
                content.append("")
        
        
        return "\n".join(content)
    
    def format_wakatime_content(self, wakatime_data: Dict) -> str:
        """Format Wakatime data for calendar entry"""
        if not wakatime_data:
            return ""
        
        daily_data = wakatime_data.get('daily_data', {})
        stats_data = wakatime_data.get('stats_data', {})
        
        if hasattr(self.wakatime_collector, 'format_for_calendar'):
            return self.wakatime_collector.format_for_calendar(daily_data, stats_data)
        else:
            # Fallback formatting
            return self._format_wakatime_fallback(daily_data, stats_data)
    
    def _format_wakatime_fallback(self, daily_data: Dict, stats_data: Dict) -> str:
        """Fallback Wakatime formatting"""
        content = []
        content.append("## Wakatime Activity")
        content.append("")
        
        if daily_data.get('total_time') != '0h 0m':
            content.append(f"**⏱️ Daily Coding Time:** {daily_data['total_time']}")
            content.append("")
        
        # Languages
        if daily_data.get('languages'):
            content.append("### Programming Languages")
            content.append("")
            for lang in daily_data['languages'][:5]:
                content.append(f"- **{lang['name']}**: {lang['time']} ({lang['percentage']})")
            content.append("")
        
        # Projects
        if daily_data.get('projects'):
            content.append("### Active Projects")
            content.append("")
            for project in daily_data['projects'][:5]:
                content.append(f"- **{project['name']}**: {project['time']} ({project['percentage']})")
            content.append("")
        
        # Editors
        if daily_data.get('editors'):
            content.append("### Development Tools")
            content.append("")
            for editor in daily_data['editors'][:3]:
                content.append(f"- **{editor['name']}**: {editor['time']} ({editor['percentage']})")
            content.append("")
        
        # Operating Systems
        if daily_data.get('operating_systems'):
            content.append("### Development Environment")
            content.append("")
            for os in daily_data['operating_systems']:
                content.append(f"- **{os['name']}**: {os['time']} ({os['percentage']})")
            content.append("")
        
        # Weekly stats
        if stats_data and stats_data.get('daily_average'):
            content.append("### Weekly Summary")
            content.append("")
            content.append(f"- **Daily Average**: {stats_data['daily_average']} hours")
            if stats_data.get('best_day'):
                best_day = stats_data['best_day']
                content.append(f"- **Best Day**: {best_day['date']} ({best_day['time']})")
            content.append("")
        
        content.append(f"*Wakatime data captured on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(content)
    
    def create_datatable_content(self, github_data: Dict, wakatime_data: Dict) -> str:
        """Create comprehensive datatable content"""
        content = []
        content.append("## Development Analytics")
        content.append("")
        
        # Summary table
        content.append("### Daily Summary")
        content.append("")
        content.append("| Metric | GitHub | Wakatime |")
        content.append("|--------|--------|----------|")
        
        github_commits = github_data.get('commits', 0) if github_data else 0
        wakatime_time = wakatime_data.get('daily_data', {}).get('total_time', '0h 0m') if wakatime_data else '0h 0m'
        
        content.append(f"| Commits | {github_commits} | - |")
        content.append(f"| Coding Time | - | {wakatime_time} |")
        content.append(f"| Pull Requests | {github_data.get('prs', 0) if github_data else 0} | - |")
        content.append(f"| Issues | {github_data.get('issues', 0) if github_data else 0} | - |")
        content.append("")
        
        # Wakatime detailed tables
        if wakatime_data and wakatime_data.get('daily_data'):
            daily_data = wakatime_data['daily_data']
            
            # Languages table
            if daily_data.get('languages'):
                content.append("### Programming Languages")
                content.append("")
                content.append("| Language | Time | Percentage | Seconds |")
                content.append("|----------|------|------------|---------|")
                for lang in daily_data['languages']:
                    content.append(f"| {lang['name']} | {lang['time']} | {lang['percentage']} | {lang['seconds']} |")
                content.append("")
            
            # Projects table
            if daily_data.get('projects'):
                content.append("### Active Projects")
                content.append("")
                content.append("| Project | Time | Percentage | Seconds |")
                content.append("|---------|------|------------|---------|")
                for project in daily_data['projects']:
                    content.append(f"| {project['name']} | {project['time']} | {project['percentage']} | {project['seconds']} |")
                content.append("")
        
        content.append(f"*Generated on {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*")
        
        return "\n".join(content)
    
    def update_calendar_entry(self, target_date: date, github_data: Dict, wakatime_data: Dict):
        """Update calendar entry with all collected data"""
        try:
            # Create calendar file path
            year = target_date.year
            month = target_date.strftime("%B")
            day = target_date.strftime("%d-%m-%Y")
            
            calendar_dir = self.calendar_path / str(year) / month
            calendar_file = calendar_dir / f"{day}.md"
            
            # Ensure directory exists and create file with a basic header if missing
            if not calendar_file.exists():
                calendar_dir.mkdir(parents=True, exist_ok=True)
                header = f"# {month} {target_date.strftime('%d')}, {year}\n\n"
                with open(calendar_file, 'w', encoding='utf-8') as f:
                    f.write(header)
                print(f"🆕 Created calendar file: {calendar_file}")
            
            # Read existing content
            with open(calendar_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            # Generate content sections
            github_content = self.format_github_content(github_data)
            wakatime_content = self.format_wakatime_content(wakatime_data)
            datatable_content = self.create_datatable_content(github_data, wakatime_data)
            
            # Remove any existing GitHub Activity, Wakatime, and Development Analytics sections
            import re
            # Remove from first occurrence of "## GitHub Activity" to the end
            existing_content = re.sub(
                r'\n## GitHub Activity.*$',
                '',
                existing_content,
                flags=re.DOTALL
            )
            
            # Combine all content (replace old sections with new)
            new_content = existing_content.rstrip() + "\n\n" + github_content + "\n\n" + wakatime_content + "\n\n" + datatable_content
            
            # Write updated content
            with open(calendar_file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            
            print(f"✅ Updated calendar entry: {calendar_file}")
            return True
            
        except Exception as e:
            print(f"❌ Failed to update calendar entry: {e}")
            return False
    
    def run_data_collection(self, target_date: date):
        """Run complete data collection for target date"""
        try:
            print(f"🚀 Starting unified data collection for {target_date}")
            print("=" * 60)
            
            # Initialize collectors
            if not self.initialize_collectors():
                print("❌ Failed to initialize collectors")
                return False
            
            # Collect GitHub data
            github_data = self.collect_github_data(target_date)
            
            # Collect Wakatime data (only if enabled)
            wakatime_data = {}
            if self.config.get('wakatime', {}).get('enabled', False):
                wakatime_data = self.collect_wakatime_data(target_date)
            
            # Update calendar entry
            if github_data or wakatime_data:
                success = self.update_calendar_entry(target_date, github_data, wakatime_data)
                if success:
                    print("✅ Data collection and calendar update completed successfully!")
                    return True
                else:
                    print("❌ Calendar update failed")
                    return False
            else:
                print("⚠️  No data collected")
                return False
                
        except Exception as e:
            print(f"❌ Data collection failed: {e}")
            return False

def main():
    """Main function"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Unified Data Collector')
    parser.add_argument('--config', default='/Users/rupali.b/Documents/GitHub/Obsidian/Scripts/config/unified_data_config.json', help='Config file path')
    parser.add_argument('--date', type=str, help='Specific date (YYYY-MM-DD)')
    parser.add_argument('--today', action='store_true', help='Process today (default)')
    # New parallel commit fetching mode
    parser.add_argument('--commits-range', nargs=2, metavar=('SINCE','UNTIL'), help='Fetch commit titles/descriptions for all repos between dates (YYYY-MM-DD YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # If commits-range provided, run parallel fetch and print JSON to stdout
    if args.commits_range:
        since_str, until_str = args.commits_range
        since_dt = datetime.strptime(since_str, '%Y-%m-%d').date()
        until_dt = datetime.strptime(until_str, '%Y-%m-%d').date()
        summary = fetch_commits_parallel_from_config(args.config, since_dt, until_dt)
        print(json.dumps(summary, indent=2))
        return
    
    # Determine target date
    if args.date:
        target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
    else:
        target_date = date.today()  # Default to today
    
    # Initialize collector
    collector = UnifiedDataCollector(args.config)
    
    # Run data collection
    success = collector.run_data_collection(target_date)
    
    if success:
        print(f"\n✅ Unified data collection completed for {target_date}")
    else:
        print(f"\n❌ Unified data collection failed for {target_date}")
        sys.exit(1)

if __name__ == "__main__":
    main()
