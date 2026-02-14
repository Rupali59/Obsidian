"""
GitHub data collector module
Fetches commits, PRs, and issues from GitHub repositories
"""

import os
import json
import logging
import time
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path
from datetime import date, datetime
from typing import Dict, List, Optional, Tuple

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
    
    def _is_rate_limit_error(self, response: requests.Response) -> bool:
        """Check if a 403 error is due to rate limiting"""
        if response.status_code != 403:
            return False
        
        # Check rate limit headers
        remaining = response.headers.get('x-ratelimit-remaining', '')
        if remaining == '0':
            return True
        
        # Check for rate limit message in response body
        try:
            error_data = response.json()
            if isinstance(error_data, dict):
                message = error_data.get('message', '').lower()
                if 'rate limit' in message or 'api rate limit' in message:
                    return True
        except:
            pass
        
        return False
    
    def _get_rate_limit_wait_time(self, response: requests.Response) -> Optional[int]:
        """Get the wait time in seconds from rate limit headers"""
        # Check retry-after header first (takes priority)
        retry_after = response.headers.get('retry-after')
        if retry_after:
            try:
                return int(retry_after)
            except ValueError:
                pass
        
        # Check x-ratelimit-reset header
        reset_time = response.headers.get('x-ratelimit-reset')
        if reset_time:
            try:
                reset_epoch = int(reset_time)
                wait_seconds = reset_epoch - int(time.time())
                return max(0, wait_seconds)  # Don't return negative
            except (ValueError, TypeError):
                pass
        
        return None
    
    def _make_request_with_retry(self, url: str, params: Optional[Dict] = None, 
                                  max_retries: int = 3, timeout: int = 10) -> requests.Response:
        """Make an API request with retry logic for rate limits and transient errors"""
        retry_count = 0
        last_exception = None
        
        while retry_count <= max_retries:
            try:
                response = requests.get(url, headers=self.headers, params=params, timeout=timeout)
                
                # Handle rate limiting
                if response.status_code == 403 and self._is_rate_limit_error(response):
                    wait_time = self._get_rate_limit_wait_time(response)
                    if wait_time is not None and wait_time > 0:
                        reset_time = datetime.fromtimestamp(int(time.time()) + wait_time).strftime('%H:%M:%S')
                        logging.warning(
                            f"Rate limit exceeded. Waiting {wait_time} seconds until reset at {reset_time}..."
                        )
                        time.sleep(wait_time + 1)  # Add 1 second buffer
                        retry_count += 1
                        continue
                    else:
                        # Rate limited but no wait time available, wait 60 seconds
                        logging.warning("Rate limit exceeded but no reset time available. Waiting 60 seconds...")
                        time.sleep(60)
                        retry_count += 1
                        continue
                
                # Handle 429 (Too Many Requests) - standard rate limit status
                if response.status_code == 429:
                    wait_time = self._get_rate_limit_wait_time(response) or 60
                    reset_time = datetime.fromtimestamp(int(time.time()) + wait_time).strftime('%H:%M:%S')
                    logging.warning(
                        f"Rate limit exceeded (429). Waiting {wait_time} seconds until reset at {reset_time}..."
                    )
                    time.sleep(wait_time + 1)  # Add 1 second buffer
                    retry_count += 1
                    continue
                
                # Handle transient server errors (500, 502, 503, 504)
                if response.status_code in [500, 502, 503, 504]:
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count  # Exponential backoff: 1s, 2s, 4s
                        logging.warning(
                            f"Server error {response.status_code}. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{max_retries + 1})"
                        )
                        time.sleep(wait_time)
                        retry_count += 1
                        continue
                    else:
                        response.raise_for_status()
                
                # Handle network/connection errors
                if response.status_code == 200:
                    return response
                
                # For other status codes, check if we should retry
                if response.status_code in [408, 429]:  # Request timeout or rate limit
                    if retry_count < max_retries:
                        wait_time = 2 ** retry_count
                        logging.warning(f"Status {response.status_code}. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        retry_count += 1
                        continue
                
                # Non-retryable errors or success
                return response
                
            except requests.exceptions.Timeout:
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count
                    logging.warning(f"Request timeout. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{max_retries + 1})")
                    time.sleep(wait_time)
                    retry_count += 1
                    continue
                else:
                    raise
            
            except requests.exceptions.ConnectionError as e:
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count
                    logging.warning(f"Connection error. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{max_retries + 1})")
                    time.sleep(wait_time)
                    retry_count += 1
                    last_exception = e
                    continue
                else:
                    raise
            
            except Exception as e:
                # For other exceptions, don't retry
                raise
        
        # If we've exhausted retries, raise the last exception
        if last_exception:
            raise last_exception
        raise Exception(f"Failed after {max_retries + 1} attempts")
    
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
            response = self._make_request_with_retry(branches_url)
            if response.status_code == 403:
                # Check if it's a rate limit or auth error
                if self._is_rate_limit_error(response):
                    # Should have been handled by retry logic, but if we still get here, raise
                    wait_time = self._get_rate_limit_wait_time(response) or 3600
                    error_msg = (
                        f"GitHub API rate limit exceeded for {repo}. "
                        f"Please wait {wait_time} seconds before retrying."
                    )
                    logging.error(error_msg)
                    raise PermissionError(error_msg)
                else:
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
                response = self._make_request_with_retry(commits_url, params=params)
                if response.status_code == 403:
                    # Check if it's a rate limit or auth error
                    if self._is_rate_limit_error(response):
                        wait_time = self._get_rate_limit_wait_time(response) or 3600
                        error_msg = (
                            f"GitHub API rate limit exceeded for {repo} commits. "
                            f"Please wait {wait_time} seconds before retrying."
                        )
                        logging.error(error_msg)
                        raise PermissionError(error_msg)
                    else:
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
            response = self._make_request_with_retry(prs_url, params=params)
            if response.status_code == 403:
                # Check if it's a rate limit or auth error
                if self._is_rate_limit_error(response):
                    wait_time = self._get_rate_limit_wait_time(response) or 3600
                    error_msg = (
                        f"GitHub API rate limit exceeded for {repo} PRs. "
                        f"Please wait {wait_time} seconds before retrying."
                    )
                    logging.error(error_msg)
                    raise PermissionError(error_msg)
                else:
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
            response = self._make_request_with_retry(issues_url, params=params)
            if response.status_code == 403:
                # Check if it's a rate limit or auth error
                if self._is_rate_limit_error(response):
                    wait_time = self._get_rate_limit_wait_time(response) or 3600
                    error_msg = (
                        f"GitHub API rate limit exceeded for {repo} issues. "
                        f"Please wait {wait_time} seconds before retrying."
                    )
                    logging.error(error_msg)
                    raise PermissionError(error_msg)
                else:
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
        
        # Fetch data from all repos in parallel (optimized for concurrent API calls)
        max_workers = min(15, max(1, len(self.repositories)))  # Scale with repo count, max 15
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
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


def _is_rate_limit_error_response(response: requests.Response) -> bool:
    """Check if a 403 error is due to rate limiting (standalone function)"""
    if response.status_code not in [403, 429]:
        return False
    
    # Check rate limit headers
    remaining = response.headers.get('x-ratelimit-remaining', '')
    if remaining == '0':
        return True
    
    # Check for rate limit message in response body
    try:
        error_data = response.json()
        if isinstance(error_data, dict):
            message = error_data.get('message', '').lower()
            if 'rate limit' in message or 'api rate limit' in message:
                return True
    except:
        pass
    
    return False


def _get_rate_limit_wait_time_response(response: requests.Response) -> Optional[int]:
    """Get the wait time in seconds from rate limit headers (standalone function)"""
    # Check retry-after header first (takes priority)
    retry_after = response.headers.get('retry-after')
    if retry_after:
        try:
            return int(retry_after)
        except ValueError:
            pass
    
    # Check x-ratelimit-reset header
    reset_time = response.headers.get('x-ratelimit-reset')
    if reset_time:
        try:
            reset_epoch = int(reset_time)
            wait_seconds = reset_epoch - int(time.time())
            return max(0, wait_seconds)  # Don't return negative
        except (ValueError, TypeError):
            pass
    
    return None


def _make_request_with_retry_standalone(url: str, headers: Dict, params: Optional[Dict] = None,
                                        max_retries: int = 3, timeout: int = 30) -> requests.Response:
    """Make an API request with retry logic (standalone function)"""
    retry_count = 0
    last_exception = None
    
    while retry_count <= max_retries:
        try:
            response = requests.get(url, headers=headers, params=params, timeout=timeout)
            
            # Handle rate limiting
            if response.status_code in [403, 429] and _is_rate_limit_error_response(response):
                wait_time = _get_rate_limit_wait_time_response(response)
                if wait_time is not None and wait_time > 0:
                    reset_time = datetime.fromtimestamp(int(time.time()) + wait_time).strftime('%H:%M:%S')
                    logging.warning(
                        f"Rate limit exceeded. Waiting {wait_time} seconds until reset at {reset_time}..."
                    )
                    time.sleep(wait_time + 1)  # Add 1 second buffer
                    retry_count += 1
                    continue
                else:
                    # Rate limited but no wait time available, wait 60 seconds
                    logging.warning("Rate limit exceeded but no reset time available. Waiting 60 seconds...")
                    time.sleep(60)
                    retry_count += 1
                    continue
            
            # Handle transient server errors (500, 502, 503, 504)
            if response.status_code in [500, 502, 503, 504]:
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count  # Exponential backoff: 1s, 2s, 4s
                    logging.warning(
                        f"Server error {response.status_code}. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{max_retries + 1})"
                    )
                    time.sleep(wait_time)
                    retry_count += 1
                    continue
                else:
                    response.raise_for_status()
            
            # Handle network/connection errors
            if response.status_code == 200:
                return response
            
            # For other status codes, check if we should retry
            if response.status_code in [408, 429]:  # Request timeout or rate limit
                if retry_count < max_retries:
                    wait_time = 2 ** retry_count
                    logging.warning(f"Status {response.status_code}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    retry_count += 1
                    continue
            
            # Non-retryable errors or success
            return response
            
        except requests.exceptions.Timeout:
            if retry_count < max_retries:
                wait_time = 2 ** retry_count
                logging.warning(f"Request timeout. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{max_retries + 1})")
                time.sleep(wait_time)
                retry_count += 1
                continue
            else:
                raise
        
        except requests.exceptions.ConnectionError as e:
            if retry_count < max_retries:
                wait_time = 2 ** retry_count
                logging.warning(f"Connection error. Retrying in {wait_time} seconds... (attempt {retry_count + 1}/{max_retries + 1})")
                time.sleep(wait_time)
                retry_count += 1
                last_exception = e
                continue
            else:
                raise
        
        except Exception as e:
            # For other exceptions, don't retry
            raise
    
    # If we've exhausted retries, raise the last exception
    if last_exception:
        raise last_exception
    raise Exception(f"Failed after {max_retries + 1} attempts")


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
        resp = _make_request_with_retry_standalone(url, headers, params=params, timeout=30)
        if resp.status_code == 403:
            # Check if it's a rate limit or auth error
            if _is_rate_limit_error_response(resp):
                wait_time = _get_rate_limit_wait_time_response(resp) or 3600
                error_msg = f"GitHub API rate limit exceeded for {owner_repo}. Please wait {wait_time} seconds before retrying."
                logging.error(error_msg)
                return { 'repository': owner_repo, 'error': 'HTTP 403 Rate Limit', 'commits': [], 'is_403': True, 'is_rate_limit': True }
            else:
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
    # Optimize parallelism: use more workers for better throughput
    max_workers = min(15, max(1, len(repos)))  # Scale with repo count, max 15
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        future_map = {
            executor.submit(_fetch_repo_commits, repo, token, since_iso, until_iso): repo
            for repo in repos
        }
        for fut in as_completed(future_map):
            repo = future_map[fut]
            res = fut.result()
            if 'error' in res and res['error']:
                errors[repo] = res['error']
                # Only treat as auth error if it's not a rate limit
                if res.get('is_403', False) and not res.get('is_rate_limit', False):
                    has_403_error = True
                elif '403' in res['error'] and 'Rate Limit' not in res['error']:
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
