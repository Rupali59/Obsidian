#!/usr/bin/env python3
"""
GitHub GraphQL Data Fetcher
Optimized to reduce API calls by using GraphQL to fetch all repository data in a single request
"""

import os
import sys
import json
import logging
import requests
from pathlib import Path
from datetime import datetime, date
from typing import List, Dict, Optional

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('github_graphql_metrics.log'),
        logging.StreamHandler()
    ]
)

class GitHubGraphQLFetcher:
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        self.calendar_path = self.obsidian_path / "Calendar"
        self.config_path = self.obsidian_path / "Scripts" / "config" / "github_config.env"
        
        # GitHub API configuration
        self.github_token = None
        self.github_username = None
        self.api_base = "https://api.github.com/graphql"
        
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
            'Content-Type': 'application/json',
            'Accept': 'application/vnd.github.v4+json'
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
            query = """
            query {
                viewer {
                    login
                }
            }
            """
            
            response = requests.post(
                self.api_base,
                headers=self.headers,
                json={'query': query}
            )
            response.raise_for_status()
            
            data = response.json()
            if 'data' in data and 'viewer' in data['data']:
                self.github_username = data['data']['viewer']['login']
                return self.github_username
            else:
                raise ValueError("Could not get username from GitHub API")
                
        except Exception as e:
            logging.error(f"Failed to auto-detect username: {e}")
            raise
    
    def get_all_repository_metrics(self, target_date: date) -> Dict:
        """
        Get metrics for all tracked repositories on a specific date using a single GraphQL query
        This dramatically reduces API calls from 36+ to just 1!
        """
        try:
            tracked_repos = self._get_tracked_repositories()
            if not tracked_repos:
                return {"error": "No repositories configured for tracking"}
            
            username = self._get_username()
            
            # Convert date to ISO format for API calls
            since_time = target_date.isoformat() + "T00:00:00Z"
            until_time = target_date.isoformat() + "T23:59:59Z"
            
            # Build GraphQL query for all repositories
            # We'll use the search API to get commits, PRs, and issues for all repos at once
            query_parts = []
            
            for repo_name in tracked_repos:
                full_repo_name = f"{username}/{repo_name}"
                
                # Add commits search - use COMMIT type for commits
                query_parts.append(f"""
                commits_{repo_name.replace('-', '_')}: search(query: "repo:{full_repo_name} committer-date:{target_date.isoformat()}", type: COMMIT, first: 100) {{
                    edges {{
                        node {{
                            ... on Commit {{
                                oid
                                messageHeadline
                                committedDate
                                author {{
                                    name
                                }}
                            }}
                        }}
                    }}
                }}
                """)
                
                # Add PRs search - use ISSUE type for PRs
                query_parts.append(f"""
                prs_{repo_name.replace('-', '_')}: search(query: "repo:{full_repo_name} is:pr created:{target_date.isoformat()}", type: ISSUE, first: 100) {{
                    edges {{
                        node {{
                            ... on PullRequest {{
                                number
                                title
                                state
                                createdAt
                            }}
                        }}
                    }}
                }}
                """)
                
                # Add issues search - use ISSUE type for issues
                query_parts.append(f"""
                issues_{repo_name.replace('-', '_')}: search(query: "repo:{full_repo_name} is:issue created:{target_date.isoformat()}", type: ISSUE, first: 100) {{
                    edges {{
                        node {{
                            ... on Issue {{
                                number
                                title
                                state
                                createdAt
                            }}
                        }}
                    }}
                }}
                """)
            
            # Combine all queries
            full_query = f"""
            query {{
                {' '.join(query_parts)}
            }}
            """
            
            logging.info(f"Executing GraphQL query for {len(tracked_repos)} repositories on {target_date}")
            
            response = requests.post(
                self.api_base,
                headers=self.headers,
                json={'query': full_query}
            )
            response.raise_for_status()
            
            data = response.json()
            
            if 'errors' in data:
                logging.error(f"GraphQL errors: {data['errors']}")
                return {"error": f"GraphQL errors: {data['errors']}"}
            
            # Process the results
            results = {}
            total_commits = 0
            total_prs = 0
            total_issues = 0
            
            for repo_name in tracked_repos:
                repo_key = repo_name.replace('-', '_')
                
                # Process commits
                commits_data = data.get('data', {}).get(f'commits_{repo_key}', {}).get('edges', [])
                commits = []
                for edge in commits_data:
                    commit = edge['node']
                    commits.append({
                        'repo': f"{username}/{repo_name}",
                        'sha': commit['oid'][:7],
                        'message': commit['messageHeadline']
                    })
                
                # Process PRs
                prs_data = data.get('data', {}).get(f'prs_{repo_key}', {}).get('edges', [])
                prs = []
                for edge in prs_data:
                    pr = edge['node']
                    prs.append({
                        'repo': f"{username}/{repo_name}",
                        'number': pr['number'],
                        'title': pr['title'],
                        'state': pr['state']
                    })
                
                # Process issues
                issues_data = data.get('data', {}).get(f'issues_{repo_key}', {}).get('edges', [])
                issues = []
                for edge in issues_data:
                    issue = edge['node']
                    issues.append({
                        'repo': f"{username}/{repo_name}",
                        'number': issue['number'],
                        'title': issue['title'],
                        'state': issue['state']
                    })
                
                results[repo_name] = {
                    'commits': commits,
                    'pull_requests': prs,
                    'issues': issues,
                    'repository': f"{username}/{repo_name}",
                    'date': target_date.isoformat()
                }
                
                total_commits += len(commits)
                total_prs += len(prs)
                total_issues += len(issues)
            
            logging.info(f"GraphQL query completed: {total_commits} commits, {total_prs} PRs, {total_issues} issues")
            
            return {
                'repositories': results,
                'summary': {
                    'total_commits': total_commits,
                    'total_prs': total_prs,
                    'total_issues': total_issues,
                    'total_repositories': len(tracked_repos)
                }
            }
            
        except Exception as e:
            logging.error(f"Error in GraphQL query: {e}")
            return {"error": str(e)}
    
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
