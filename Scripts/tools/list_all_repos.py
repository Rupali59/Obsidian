#!/usr/bin/env python3
"""
List all repositories found during GitHub capture
"""

import sys
from pathlib import Path

# Add the sync directory to the path
sys.path.insert(0, str(Path(__file__).parent / "sync" / "github"))

from github_data_fetcher import GitHubDailyMetrics

def main():
    """List all repositories found"""
    print("🔍 Getting complete list of your GitHub repositories...")
    print("=" * 60)
    
    try:
        # Initialize the GitHub metrics capture
        github_capture = GitHubDailyMetrics(".")
        
        # Get all repositories
        print("📚 Fetching repositories from GitHub...")
        repos = github_capture.get_user_repositories()
        
        print(f"\n🎯 Total repositories found: {len(repos)}")
        print("=" * 60)
        
        # Group repositories by type
        owned_repos = []
        contributed_repos = []
        
        for repo in repos:
            if repo['owner']['login'] == github_capture.github_username:
                owned_repos.append(repo)
            else:
                contributed_repos.append(repo)
        
        print(f"\n👑 YOUR REPOSITORIES ({len(owned_repos)}):")
        print("-" * 40)
        for repo in sorted(owned_repos, key=lambda x: x['name'].lower()):
            print(f"  {repo['name']}")
        
        if contributed_repos:
            print(f"\n🤝 CONTRIBUTED REPOSITORIES ({len(contributed_repos)}):")
            print("-" * 40)
            for repo in sorted(contributed_repos, key=lambda x: x['name'].lower()):
                print(f"  {repo['name']} (owned by {repo['owner']['login']})")
        
        print("\n" + "=" * 60)
        print("💡 Copy the repository names above to update repos_to_track.env")
        
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()
