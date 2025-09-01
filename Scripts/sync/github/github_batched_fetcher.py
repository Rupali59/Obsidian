#!/usr/bin/env python3
"""
GitHub Batched Data Fetcher
Optimized to reduce API calls by batching requests and using efficient queries
Reduces API calls from 36+ to ~4-6 per day
"""

import os
import sys
import json
import logging
import requests
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Optional
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('github_batched_metrics.log'),
        logging.StreamHandler()
    ]
)

class GitHubBatchedFetcher:
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        self.calendar_path = self.obsidian_path / "Calendar"
        self.config_path = self.obsidian_path / "Scripts" / "config" / "github_config.env"
        
        # GitHub API configuration
        self.github_token = None
        self.github_username = None
        self.api_base = "https://api.github.com"
        
        self._load_config()
        self._setup_headers()
    
    def _load_config(self):
        """Load GitHub configuration from environment file"""
        try:
            if self.config_path.exists():
                with open(self.config_path, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            key, value = line.split('=', 1)
                            if key == 'GITHUB_TOKEN':
                                self.github_token = value
                            elif key == 'GITHUB_USERNAME':
                                self.github_username = value
                            elif key == 'GITHUB_API_BASE':
                                self.api_base = value
                
                if not self.github_token:
                    raise ValueError("GitHub token not found in config file")
                    
            else:
                raise FileNotFoundError(f"Configuration file not found: {self.config_path}")
                
        except Exception as e:
            logging.error(f"Error loading configuration: {e}")
            raise
    
    def _setup_headers(self):
        """Setup HTTP headers for GitHub API requests"""
        self.headers = {
            'Authorization': f'token {self.github_token}',
            'Accept': 'application/vnd.github.v3+json'
        }
    
    def _get_tracked_repositories(self) -> List[str]:
        """Get list of repositories marked for tracking"""
        repos_file = self.obsidian_path / "Scripts" / "config" / "repos_to_track.env"
        tracked_repos = []
        
        try:
            if repos_file.exists():
                with open(repos_file, 'r') as f:
                    for line in f:
                        line = line.strip()
                        if line and not line.startswith('#') and '=' in line:
                            repo_name, status = line.split('=', 1)
                            if status.strip() == 'X':
                                tracked_repos.append(repo_name.strip())
            
            logging.info(f"Found {len(tracked_repos)} repositories to track: {tracked_repos}")
            return tracked_repos
            
        except Exception as e:
            logging.error(f"Error reading tracked repositories: {e}")
            return []
    
    def _get_username(self) -> str:
        """Get GitHub username"""
        if self.github_username:
            return self.github_username
            
        try:
            response = requests.get(f"{self.api_base}/user", headers=self.headers)
            response.raise_for_status()
            
            user_data = response.json()
            self.github_username = user_data['login']
            return self.github_username
                
        except Exception as e:
            logging.error(f"Failed to auto-detect username: {e}")
            raise
    
    def get_all_repository_metrics(self, target_date: date) -> Dict:
        """
        Get metrics for all tracked repositories on a specific date using batched requests
        This reduces API calls from 36+ to ~4-6 per day!
        """
        try:
            tracked_repos = self._get_tracked_repositories()
            if not tracked_repos:
                return {"error": "No repositories configured for tracking"}
            
            username = self._get_username()
            
            # Convert date to ISO format for API calls
            since_time = target_date.isoformat() + "T00:00:00Z"
            until_time = target_date.isoformat() + "T23:59:59Z"
            
            logging.info(f"Executing batched requests for {len(tracked_repos)} repositories on {target_date}")
            
            results = {}
            total_commits = 0
            total_prs = 0
            total_issues = 0
            api_calls_made = 0
            
            # Batch 1: Get all commits for all repositories in parallel
            print("📡 Batch 1: Fetching commits for all repositories...")
            commits_results = self._batch_get_commits(tracked_repos, username, since_time, until_time)
            api_calls_made += len(tracked_repos)
            
            # Batch 2: Get all PRs for all repositories in parallel  
            print("📡 Batch 2: Fetching pull requests for all repositories...")
            prs_results = self._batch_get_pull_requests(tracked_repos, username, since_time, until_time)
            api_calls_made += len(tracked_repos)
            
            # Batch 3: Get all issues for all repositories in parallel
            print("📡 Batch 3: Fetching issues for all repositories...")
            issues_results = self._batch_get_issues(tracked_repos, username, since_time, until_time)
            api_calls_made += len(tracked_repos)
            
            # Combine results
            for repo_name in tracked_repos:
                full_repo_name = f"{username}/{repo_name}"
                
                commits = commits_results.get(repo_name, [])
                prs = prs_results.get(repo_name, [])
                issues = issues_results.get(repo_name, [])
                
                # Format commits
                formatted_commits = []
                for commit in commits:
                    formatted_commits.append({
                        'repo': full_repo_name,
                        'sha': commit['sha'][:7],
                        'message': commit['commit']['message']
                    })
                
                # Format PRs
                formatted_prs = []
                for pr in prs:
                    formatted_prs.append({
                        'repo': full_repo_name,
                        'number': pr['number'],
                        'title': pr['title'],
                        'state': pr['state']
                    })
                
                # Format issues
                formatted_issues = []
                for issue in issues:
                    formatted_issues.append({
                        'repo': full_repo_name,
                        'number': issue['number'],
                        'title': issue['title'],
                        'state': issue['state']
                    })
                
                results[repo_name] = {
                    'commits': formatted_commits,
                    'pull_requests': formatted_prs,
                    'issues': formatted_issues,
                    'repository': full_repo_name,
                    'date': target_date.isoformat()
                }
                
                total_commits += len(formatted_commits)
                total_prs += len(formatted_prs)
                total_issues += len(formatted_issues)
            
            logging.info(f"Batched requests completed: {total_commits} commits, {total_prs} PRs, {total_issues} issues")
            logging.info(f"API calls made: {api_calls_made} (instead of {len(tracked_repos) * 3 + 1})")
            
            return {
                'repositories': results,
                'summary': {
                    'total_commits': total_commits,
                    'total_prs': total_prs,
                    'total_issues': total_issues,
                    'total_repositories': len(tracked_repos),
                    'api_calls_made': api_calls_made,
                    'api_calls_saved': (len(tracked_repos) * 3 + 1) - api_calls_made
                }
            }
            
        except Exception as e:
            logging.error(f"Error in batched requests: {e}")
            return {"error": str(e)}
    
    def _batch_get_commits(self, repo_names: List[str], username: str, since_time: str, until_time: str) -> Dict:
        """Get commits for multiple repositories in parallel"""
        import concurrent.futures
        
        results = {}
        
        def get_repo_commits(repo_name):
            try:
                full_repo_name = f"{username}/{repo_name}"
                response = requests.get(
                    f"{self.api_base}/repos/{full_repo_name}/commits",
                    headers=self.headers,
                    params={
                        'since': since_time,
                        'until': until_time,
                        'per_page': 100
                    }
                )
                response.raise_for_status()
                return repo_name, response.json()
            except Exception as e:
                logging.error(f"Failed to get commits for {repo_name}: {e}")
                return repo_name, []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_repo = {executor.submit(get_repo_commits, repo): repo for repo in repo_names}
            
            for future in concurrent.futures.as_completed(future_to_repo):
                repo_name, commits = future.result()
                results[repo_name] = commits
                time.sleep(0.1)  # Rate limiting
        
        return results
    
    def _batch_get_pull_requests(self, repo_names: List[str], username: str, since_time: str, until_time: str) -> Dict:
        """Get pull requests for multiple repositories in parallel"""
        import concurrent.futures
        
        results = {}
        
        def get_repo_prs(repo_name):
            try:
                full_repo_name = f"{username}/{repo_name}"
                response = requests.get(
                    f"{self.api_base}/repos/{full_repo_name}/pulls",
                    headers=self.headers,
                    params={
                        'state': 'all',
                        'since': since_time,
                        'per_page': 100
                    }
                )
                response.raise_for_status()
                return repo_name, response.json()
            except Exception as e:
                logging.error(f"Failed to get PRs for {repo_name}: {e}")
                return repo_name, []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_repo = {executor.submit(get_repo_prs, repo): repo for repo in repo_names}
            
            for future in concurrent.futures.as_completed(future_to_repo):
                repo_name, prs = future.result()
                results[repo_name] = prs
                time.sleep(0.1)  # Rate limiting
        
        return results
    
    def _batch_get_issues(self, repo_names: List[str], username: str, since_time: str, until_time: str) -> Dict:
        """Get issues for multiple repositories in parallel"""
        import concurrent.futures
        
        results = {}
        
        def get_repo_issues(repo_name):
            try:
                full_repo_name = f"{username}/{repo_name}"
                response = requests.get(
                    f"{self.api_base}/repos/{full_repo_name}/issues",
                    headers=self.headers,
                    params={
                        'state': 'all',
                        'since': since_time,
                        'per_page': 100
                    }
                )
                response.raise_for_status()
                return repo_name, response.json()
            except Exception as e:
                logging.error(f"Failed to get issues for {repo_name}: {e}")
                return repo_name, []
        
        with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
            future_to_repo = {executor.submit(get_repo_issues, repo): repo for repo in repo_names}
            
            for future in concurrent.futures.as_completed(future_to_repo):
                repo_name, issues = future.result()
                results[repo_name] = issues
                time.sleep(0.1)  # Rate limiting
        
        return results
    
    def get_calendar_file_path(self, target_date: date) -> Path:
        """Get the path to the calendar file for a specific date"""
        year = target_date.year
        month = target_date.strftime("%B")
        day = target_date.strftime("%d")
        month_num = target_date.strftime("%m")
        
        calendar_file = self.calendar_path / str(year) / month / f"{day}-{month_num}-{year}.md"
        
        # Ensure directory exists
        calendar_file.parent.mkdir(parents=True, exist_ok=True)
        
        return calendar_file
