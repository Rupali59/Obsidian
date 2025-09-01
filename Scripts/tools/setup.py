#!/usr/bin/env python3
"""
GitHub Metrics System Setup
One-time setup for the parallel GitHub metrics capture system
"""

import os
import sys
import json
from pathlib import Path

class GitHubSetup:
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        self.scripts_path = self.obsidian_path / "Scripts"
        self.config_path = self.scripts_path / "config"
        self.parallel_path = self.scripts_path / "parallel"
        
    def create_structure(self):
        """Create the directory structure"""
        print("📁 Creating directory structure...")
        
        directories = [
            self.config_path,
            self.parallel_path,
            self.parallel_path / "configs",
            self.scripts_path / "tools",
            self.scripts_path / "scripts"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            print(f"  ✅ {directory}")
    
    def create_configs(self):
        """Create configuration files"""
        print("\n⚙️  Creating configuration files...")
        
        # GitHub config
        github_config = self.config_path / "github_config.env"
        if not github_config.exists():
            with open(github_config, 'w') as f:
                f.write("""# GitHub Configuration
GITHUB_TOKEN=your_github_token_here
# GITHUB_USERNAME=your_username
# GITHUB_API_BASE=https://api.github.com
""")
            print(f"  ✅ {github_config}")
        
        # Repos config
        repos_config = self.config_path / "repos_to_track.env"
        if not repos_config.exists():
            with open(repos_config, 'w') as f:
                f.write("""# Repository Tracking Configuration
# Format: REPO_NAME=X (X means track, blank means ignore)

# Core Projects
SSJK-CRM=X
Obsidian=X

# Add more repositories below
""")
            print(f"  ✅ {repos_config}")
    
    def create_parallel_configs(self):
        """Create parallel execution configurations"""
        print("\n🔄 Creating parallel configurations...")
        
        configs_dir = self.parallel_path / "configs"
        
        # August config
        august_config = configs_dir / "august_2025.json"
        august_data = {
            "name": "August 2025",
            "start_date": "2025-08-01",
            "end_date": "2025-08-31",
            "workers": 3,
            "rate_limit": 0.3
        }
        
        with open(august_config, 'w') as f:
            json.dump(august_data, f, indent=2)
        print(f"  ✅ {august_config}")
        
        # Year config
        year_config = configs_dir / "year_2025.json"
        year_data = {
            "name": "Year 2025",
            "start_date": "2025-01-01",
            "end_date": "2025-12-31",
            "workers": 5,
            "rate_limit": 0.5
        }
        
        with open(year_config, 'w') as f:
            json.dump(year_data, f, indent=2)
        print(f"  ✅ {year_config}")
    
    def run_setup(self):
        """Run the complete setup"""
        print("🚀 GitHub Metrics System Setup")
        print("=" * 40)
        
        try:
            self.create_structure()
            self.create_configs()
            self.create_parallel_configs()
            
            print("\n🎉 Setup completed successfully!")
            print("\n📋 Next steps:")
            print("  1. Configure GitHub token in Scripts/config/github_config.env")
            print("  2. Mark repositories in Scripts/config/repos_to_track.env")
            print("  3. Run: cd Scripts/parallel && ./run_august.sh")
            
        except Exception as e:
            print(f"\n❌ Setup failed: {e}")
            raise

def main():
    """Main function"""
    obsidian_path = sys.argv[1] if len(sys.argv) > 1 else "."
    setup = GitHubSetup(obsidian_path)
    setup.run_setup()

if __name__ == "__main__":
    main()
