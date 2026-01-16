"""
GitHub data collector module
Fetches commits, PRs, and issues from GitHub repositories
"""

import os
import json
import logging
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import date
from typing import Dict, List

from ..utils.config import setup_env, DOTENV_AVAILABLE
from ..utils.helpers import normalize_repo_identifier

if DOTENV_AVAILABLE:
    from dotenv import load_dotenv


class GitHubCollector:
    """GitHub data collector for commits, PRs, and issues"""
    
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
            if response.status_code == 403:
                error_msg = f"GitHub API returned 403 Forbidden for {repo}. Access denied - token may be invalid or expired."
                logging.error(error_msg)
                raise PermissionError(error_msg)
            if response.status_code == 200:
                branches_data = response.json()
                branches = [b['name'] for b in branches_data]
        except PermissionError:
            raise  # Re-raise permission errors
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
                if response.status_code == 403:
                    error_msg = f"GitHub API returned 403 Forbidden for {repo} commits. Access denied - token may be invalid or expired."
                    logging.error(error_msg)
                    raise PermissionError(error_msg)
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
                            commit_timestamp = commit.get('commit', {}).get('committer', {}).get('date', '')
                            
                            commit_details.append({
                                'sha': commit_sha[:7],  # Short SHA
                                'message': commit_msg.split('\n')[0],  # First line only
                                'author': commit_author,
                                'url': commit_url,
                                'timestamp': commit_timestamp
                            })
                        elif commit_date < date_str:
                            break
            except PermissionError:
                raise  # Re-raise permission errors
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
            if response.status_code == 403:
                error_msg = f"GitHub API returned 403 Forbidden for {repo} PRs. Access denied - token may be invalid or expired."
                logging.error(error_msg)
                raise PermissionError(error_msg)
            if response.status_code == 200:
                prs_data = response.json()
                repo_prs = len([pr for pr in prs_data if pr['created_at'].startswith(date_str)])
        except PermissionError:
            raise  # Re-raise permission errors
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
            if response.status_code == 403:
                error_msg = f"GitHub API returned 403 Forbidden for {repo} issues. Access denied - token may be invalid or expired."
                logging.error(error_msg)
                raise PermissionError(error_msg)
            if response.status_code == 200:
                issues_data = response.json()
                repo_issues = len([issue for issue in issues_data if issue['created_at'].startswith(date_str)])
        except PermissionError:
            raise  # Re-raise permission errors
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
        has_403_error = False
        error_repos = []
        
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
                except PermissionError as e:
                    repo = futures[future]
                    has_403_error = True
                    error_repos.append(repo)
                    logging.error(f"403 Forbidden error for {repo}: {e}")
                except Exception as e:
                    repo = futures[future]
                    logging.error(f"Error processing {repo}: {e}")
        
        # If we encountered any 403 errors, raise an exception to stop processing
        if has_403_error:
            error_message = (
                f"\n❌ GITHUB API ACCESS DENIED (403 Forbidden)\n"
                f"   GitHub is not accessible. Please check:\n"
                f"   1. Your GitHub API token is valid and not expired\n"
                f"   2. The token has the necessary permissions\n"
                f"   3. Your network connection is working\n"
                f"   Affected repositories: {', '.join(error_repos[:5])}{'...' if len(error_repos) > 5 else ''}\n"
                f"   Process stopped. No calendar files will be written.\n"
            )
            raise PermissionError(error_message)
        
        return {
            'commits': commits,
            'prs': prs,
            'issues': issues,
            'repository_details': repository_details
        }


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
        if resp.status_code == 403:
            error_msg = f"GitHub API returned 403 Forbidden for {owner_repo}. Access denied - token may be invalid or expired."
            logging.error(error_msg)
            return { 'repository': owner_repo, 'error': 'HTTP 403 Forbidden', 'commits': [], 'is_403': True }
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
    # Load environment variables if available
    setup_env(Path(config_path))
    if DOTENV_AVAILABLE:
        env_path = Path(config_path).parent.parent.parent / '.env'
        if not env_path.exists():
            env_path = Path(config_path).parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)
    
    with open(config_path, 'r') as f:
        cfg = json.load(f)
    gh_cfg = cfg.get('github', {})
    # Prefer environment variables, fallback to config
    token = os.getenv('GITHUB_API_TOKEN') or os.getenv('GITHUB_TOKEN') or gh_cfg.get('api_token', '')
    username = os.getenv('GITHUB_USERNAME') or gh_cfg.get('username', '')
    raw_repos = gh_cfg.get('repositories', [])
    repos = [normalize_repo_identifier(r, username) for r in raw_repos]

    since_iso = f"{since_date.isoformat()}T00:00:00Z"
    # Use end of day for until
    until_iso = f"{until_date.isoformat()}T23:59:59Z"

    results: Dict[str, List[Dict]] = {}
    errors: Dict[str, str] = {}
    has_403_error = False
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
                if res.get('is_403', False) or '403' in res['error']:
                    has_403_error = True
            results[repo] = res.get('commits', [])

    # If we encountered 403 errors, raise an exception
    if has_403_error:
        error_repos = [repo for repo, error in errors.items() if '403' in error]
        error_message = (
            f"\n❌ GITHUB API ACCESS DENIED (403 Forbidden)\n"
            f"   GitHub is not accessible. Please check:\n"
            f"   1. Your GitHub API token is valid and not expired\n"
            f"   2. The token has the necessary permissions\n"
            f"   3. Your network connection is working\n"
            f"   Affected repositories: {', '.join(error_repos[:5])}{'...' if len(error_repos) > 5 else ''}\n"
            f"   Process stopped.\n"
        )
        raise PermissionError(error_message)

    summary = {
        'since': since_date.isoformat(),
        'until': until_date.isoformat(),
        'total_repositories': len(repos),
        'total_commits': sum(len(c) for c in results.values()),
        'repositories': results,
        'errors': errors
    }
    return summary
