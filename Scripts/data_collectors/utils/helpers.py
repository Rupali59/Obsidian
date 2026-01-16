"""
Helper utility functions
"""

from typing import Dict


def normalize_repo_identifier(raw_repo: str, default_username: str) -> str:
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


def calculate_project_switches(github_data: Dict) -> int:
    """Calculate number of project switches from commits sorted by timestamp"""
    all_commits = []
    repository_details = github_data.get('repository_details', {})
    
    # Collect all commits with their repo names and timestamps
    for repo_name, repo_metrics in repository_details.items():
        commit_details = repo_metrics.get('commit_details', [])
        for commit in commit_details:
            timestamp = commit.get('timestamp', '')
            if timestamp:  # Only include commits with valid timestamps
                all_commits.append({
                    'repo': repo_name,
                    'timestamp': timestamp
                })
    
    # If we have less than 2 commits, no switches possible
    if len(all_commits) < 2:
        return 0
    
    # Sort commits by timestamp
    try:
        all_commits.sort(key=lambda x: x['timestamp'])
    except (ValueError, TypeError):
        # If timestamp parsing fails, return 0
        return 0
    
    # Count switches (when consecutive commits are from different repos)
    switches = 0
    for i in range(1, len(all_commits)):
        if all_commits[i]['repo'] != all_commits[i-1]['repo']:
            switches += 1
    
    return switches
