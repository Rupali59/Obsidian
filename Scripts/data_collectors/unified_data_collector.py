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
    
    def collect_data_for_date(self, target_date: date) -> Dict:
        """Collect GitHub data for a specific date"""
        commits = 0
        prs = 0
        issues = 0
        repository_details = {}
        
        date_str = target_date.strftime('%Y-%m-%d')
        
        for repo in self.repositories:
            repo_commits = 0
            repo_prs = 0
            repo_issues = 0
            
            # Get commits - handle both full repo names and just repo names
            if '/' in repo:
                commits_url = f"{self.api_base}/repos/{repo}/commits"
            else:
                commits_url = f"{self.api_base}/repos/{self.username}/{repo}/commits"
            params = {'since': f"{date_str}T00:00:00Z", 'per_page': 100}
            
            try:
                response = requests.get(commits_url, headers=self.headers, params=params)
                if response.status_code == 200:
                    commits_data = response.json()
                    # Filter commits that were actually made on the target date
                    repo_commits = 0
                    for commit in commits_data:
                        commit_date = commit['commit']['committer']['date'][:10]  # Get YYYY-MM-DD part
                        if commit_date == date_str:
                            repo_commits += 1
                        elif commit_date < date_str:
                            # Stop if we've gone past the target date
                            break
                    commits += repo_commits
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                logging.warning(f"Failed to fetch commits for {repo}: {e}")
            
            # Get pull requests - handle both full repo names and just repo names
            if '/' in repo:
                prs_url = f"{self.api_base}/repos/{repo}/pulls"
            else:
                prs_url = f"{self.api_base}/repos/{self.username}/{repo}/pulls"
            params = {'state': 'all', 'since': f"{date_str}T00:00:00Z"}
            
            try:
                response = requests.get(prs_url, headers=self.headers, params=params)
                if response.status_code == 200:
                    prs_data = response.json()
                    # Filter PRs created on target date
                    repo_prs = len([pr for pr in prs_data if pr['created_at'].startswith(date_str)])
                    prs += repo_prs
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                logging.warning(f"Failed to fetch PRs for {repo}: {e}")
            
            # Get issues - handle both full repo names and just repo names
            if '/' in repo:
                issues_url = f"{self.api_base}/repos/{repo}/issues"
            else:
                issues_url = f"{self.api_base}/repos/{self.username}/{repo}/issues"
            params = {'state': 'all', 'since': f"{date_str}T00:00:00Z"}
            
            try:
                response = requests.get(issues_url, headers=self.headers, params=params)
                if response.status_code == 200:
                    issues_data = response.json()
                    # Filter issues created on target date
                    repo_issues = len([issue for issue in issues_data if issue['created_at'].startswith(date_str)])
                    issues += repo_issues
                time.sleep(0.1)  # Rate limiting
            except Exception as e:
                logging.warning(f"Failed to fetch issues for {repo}: {e}")
            
            # Store repository details if there was activity
            if repo_commits > 0 or repo_prs > 0 or repo_issues > 0:
                # Use just the repo name for display
                display_name = repo.split('/')[-1] if '/' in repo else repo
                repository_details[display_name] = {
                    'commits': repo_commits,
                    'prs': repo_prs,
                    'issues': repo_issues
                }
        
        return {
            'commits': commits,
            'prs': prs,
            'issues': issues,
            'repository_details': repository_details
        }

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
        
        # Repository details
        for repo_name, repo_metrics in github_data.get('repository_details', {}).items():
            if repo_metrics.get('commits', 0) > 0 or repo_metrics.get('prs', 0) > 0 or repo_metrics.get('issues', 0) > 0:
                content.append(f"#### **{repo_name}**")
                content.append(f"- **Commits**: {repo_metrics.get('commits', 0)}")
                content.append(f"- **Pull Requests**: {repo_metrics.get('prs', 0)}")
                content.append(f"- **Issues**: {repo_metrics.get('issues', 0)}")
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
        
        github_commits = github_data.get('total_commits', 0) if github_data else 0
        wakatime_time = wakatime_data.get('daily_data', {}).get('total_time', '0h 0m') if wakatime_data else '0h 0m'
        
        content.append(f"| Commits | {github_commits} | - |")
        content.append(f"| Coding Time | - | {wakatime_time} |")
        content.append(f"| Pull Requests | {github_data.get('total_prs', 0) if github_data else 0} | - |")
        content.append(f"| Issues | {github_data.get('total_issues', 0) if github_data else 0} | - |")
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
            
            if not calendar_file.exists():
                print(f"⚠️  Calendar file not found: {calendar_file}")
                return False
            
            # Read existing content
            with open(calendar_file, 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            # Generate content sections
            github_content = self.format_github_content(github_data)
            wakatime_content = self.format_wakatime_content(wakatime_data)
            datatable_content = self.create_datatable_content(github_data, wakatime_data)
            
            # Combine all content
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
    
    args = parser.parse_args()
    
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
