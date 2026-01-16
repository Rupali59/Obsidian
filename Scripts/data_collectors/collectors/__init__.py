"""
Data collector modules
"""

from .github import GitHubCollector, fetch_commits_parallel_from_config

__all__ = ['GitHubCollector', 'fetch_commits_parallel_from_config']
