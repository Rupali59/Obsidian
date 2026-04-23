#!/usr/bin/env python3
"""
Main unified data collector - orchestrates all modules
"""

import os
import sys
import json
import logging
import time
from pathlib import Path
from datetime import datetime, date, timezone
from typing import Any, Dict

from .utils.config import load_config, setup_env
from .collectors.github import GitHubCollector
from .obsidian_calendar.updater import CalendarUpdater

# Configure logging — Scripts/python/data_collectors/main.py -> parents[2] == Scripts/
SCRIPTS_DIR = Path(__file__).resolve().parents[2]
LOGS_DIR = SCRIPTS_DIR / "logs"
LOGS_DIR.mkdir(exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(LOGS_DIR / 'unified_data_collector.log'),
        logging.StreamHandler()
    ]
)

METRICS_SCHEMA_VERSION = 1
LAST_RUN_METRICS_FILE = LOGS_DIR / "last_run_metrics.json"


def _default_run_metrics(target_date: date, started_at: str) -> Dict[str, Any]:
    return {
        "schema_version": METRICS_SCHEMA_VERSION,
        "started_at": started_at,
        "finished_at": None,
        "target_date": target_date.isoformat(),
        "success": False,
        "duration_ms": 0,
        "metrics": {
            "github_enabled": False,
            "github_initialized": False,
            "commits": None,
            "prs": None,
            "issues": None,
            "repositories_with_activity": None,
            "repositories_configured": None,
            "preflight_skipped_fanout": None,
        },
        "errors": {
            "fatal": None,
            "github_blocked": False,
            "initialization_failed": False,
            "calendar_update_failed": False,
            "github_collection_failed": False,
            "github_collection_error": None,
        },
    }


def _merge_github_metrics(payload: Dict[str, Any], github_data: Dict) -> None:
    if not github_data:
        return
    m = payload["metrics"]
    m["commits"] = github_data.get("commits")
    m["prs"] = github_data.get("prs")
    m["issues"] = github_data.get("issues")
    details = github_data.get("repository_details") or {}
    m["repositories_with_activity"] = len(details)
    if github_data.get("repositories_configured") is not None:
        m["repositories_configured"] = github_data.get("repositories_configured")
    if github_data.get("preflight_skipped_fanout") is not None:
        m["preflight_skipped_fanout"] = github_data.get("preflight_skipped_fanout")
    if github_data.get("collection_error"):
        payload["errors"]["github_collection_failed"] = True
        payload["errors"]["github_collection_error"] = str(github_data["collection_error"])[:500]


def write_last_run_metrics(payload: Dict[str, Any]) -> None:
    """Machine-readable snapshot for dashboards, alerts, and jq."""
    try:
        with open(LAST_RUN_METRICS_FILE, "w", encoding="utf-8") as f:
            json.dump(payload, f, indent=2)
    except OSError as e:
        logging.warning("Could not write %s: %s", LAST_RUN_METRICS_FILE, e)


class UnifiedDataCollector:
    """Main orchestrator for unified data collection"""
    
    def __init__(self, config_path: str):
        # Setup environment
        setup_env(Path(config_path))
        
        self.config_path = Path(config_path)
        self.config = load_config(self.config_path)
        self.obsidian_path = Path(self.config['obsidian']['vault_path'])
        self.calendar_path = self.obsidian_path / "Calendar"
        self.logger = logging.getLogger(__name__)
        
        # Initialize collectors
        self.github_collector = None
        
        # GitHub configuration - prefer environment variables, fallback to config
        self.github_config = self.config.get('github', {})
        self.github_token = os.getenv('GITHUB_API_TOKEN') or os.getenv('GITHUB_TOKEN') or self.github_config.get('api_token', '')
        self.github_username = os.getenv('GITHUB_USERNAME') or self.github_config.get('username', '')
        
        # Obsidian vault path can also come from env
        obsidian_vault_path = os.getenv('OBSIDIAN_VAULT_PATH')
        if obsidian_vault_path:
            self.obsidian_path = Path(obsidian_vault_path)
            self.calendar_path = self.obsidian_path / "Calendar"
            self.config['obsidian']['vault_path'] = obsidian_vault_path
        
        print(f"🚀 Unified Data Collector initialized")
        print(f"📁 Obsidian path: {self.obsidian_path}")
        print(f"📅 Calendar path: {self.calendar_path}")
        print(f"⚙️  Config: {self.config_path}")
        
        # Show enabled services
        github_enabled = self.config.get('github', {}).get('enabled', False)
        print(f"🔧 Services: GitHub={'✅' if github_enabled else '❌'}")
        
        # Initialize calendar updater
        self.calendar_updater = CalendarUpdater(self.calendar_path)
    
    def initialize_collectors(self):
        """Initialize GitHub collector based on config"""
        try:
            # Initialize GitHub collector
            if self.config.get('github', {}).get('enabled', False):
                print("🔧 Initializing GitHub collector...")
                repositories = self.github_config.get('repositories', [])
                repo_names = repositories
                
                self.github_collector = GitHubCollector(
                    self.github_token, 
                    self.github_username, 
                    repo_names
                )
                print("✅ GitHub collector initialized")
            
            return True
            
        except Exception as e:
            print(f"❌ Failed to initialize collectors: {e}")
            return False
    
    def collect_github_data(self, target_date: date) -> Dict:
        """Collect GitHub data for the target date"""
        if not self.github_collector:
            print("⚠️  GitHub collector not initialized")
            return {
                "commits": 0,
                "prs": 0,
                "issues": 0,
                "repository_details": {},
                "collection_error": "collector_not_initialized",
            }

        try:
            print(f"📊 Collecting GitHub data for {target_date}...")
            result = self.github_collector.collect_data_for_date(target_date)

            # Format for calendar entry (+ fields for last_run_metrics.json)
            github_data = {
                "commits": result.get("commits", 0),
                "prs": result.get("prs", 0),
                "issues": result.get("issues", 0),
                "repository_details": result.get("repository_details", {}),
                "preflight_skipped_fanout": result.get("preflight_skipped_fanout"),
                "repositories_configured": result.get("repositories_configured")
                if result.get("repositories_configured") is not None
                else len(self.github_collector.repositories),
            }

            print(
                f"✅ GitHub data collected: {github_data['commits']} commits, "
                f"{github_data['prs']} PRs, {github_data['issues']} issues"
            )
            return github_data

        except PermissionError as e:
            # Re-raise permission errors to stop the process
            print(str(e))
            raise
        except Exception as e:
            print(f"❌ GitHub data collection failed: {e}")
            return {
                "commits": 0,
                "prs": 0,
                "issues": 0,
                "repository_details": {},
                "collection_error": str(e),
            }
    
    def update_calendar_entry(self, target_date: date, github_data: Dict):
        """Update calendar entry with all collected data"""
        return self.calendar_updater.update_calendar_entry(
            target_date,
            github_data
        )
    
    def run_data_collection(self, target_date: date):
        """Run complete data collection for target date. Always writes last_run_metrics.json."""
        t0 = time.perf_counter()
        started_at = datetime.now(timezone.utc).isoformat()
        payload = _default_run_metrics(target_date, started_at)
        success = False
        try:
            payload["metrics"]["github_enabled"] = self.config.get("github", {}).get("enabled", False)
            print(f"🚀 Starting unified data collection for {target_date}")
            print("=" * 60)

            if not self.initialize_collectors():
                print("❌ Failed to initialize collectors")
                payload["errors"]["initialization_failed"] = True
                return False

            payload["metrics"]["github_initialized"] = bool(self.github_collector)

            github_data: Dict = {}
            try:
                if payload["metrics"]["github_enabled"]:
                    github_data = self.collect_github_data(target_date)
            except PermissionError as e:
                print(str(e))
                print("\n🛑 Process stopped due to GitHub API access issues.")
                print("   No calendar files will be written.")
                payload["errors"]["github_blocked"] = True
                payload["errors"]["fatal"] = str(e)[:2000]
                return False

            _merge_github_metrics(payload, github_data)

            ok = self.update_calendar_entry(target_date, github_data)
            if not ok:
                print("❌ Calendar update failed")
                payload["errors"]["calendar_update_failed"] = True
                return False

            success = True
            if github_data:
                print("✅ Data collection and calendar update completed successfully!")
            else:
                print("✅ Calendar update completed (no GitHub data)")
            return True

        except PermissionError as e:
            print(str(e))
            print("\n🛑 Process stopped due to GitHub API access issues.")
            print("   No calendar files will be written.")
            payload["errors"]["github_blocked"] = True
            payload["errors"]["fatal"] = str(e)[:2000]
            return False
        except Exception as e:
            print(f"❌ Data collection failed: {e}")
            payload["errors"]["fatal"] = str(e)[:2000]
            return False
        finally:
            payload["success"] = success
            payload["finished_at"] = datetime.now(timezone.utc).isoformat()
            payload["duration_ms"] = int((time.perf_counter() - t0) * 1000)
            write_last_run_metrics(payload)


def main():
    """Main function"""
    import argparse
    from .collectors.github import fetch_commits_parallel_from_config
    
    # Construct default config path relative to script location
    default_config = SCRIPTS_DIR / 'config' / 'unified_data_config.json'
    
    parser = argparse.ArgumentParser(description='Unified Data Collector')
    parser.add_argument('--config', default=str(default_config), help='Config file path')
    parser.add_argument('--date', type=str, help='Specific date (YYYY-MM-DD)')
    parser.add_argument('--today', action='store_true', help='Process today (default)')
    parser.add_argument('--commits-range', nargs=2, metavar=('SINCE','UNTIL'), help='Fetch commit titles/descriptions for all repos between dates (YYYY-MM-DD YYYY-MM-DD)')
    
    args = parser.parse_args()
    
    # If commits-range provided, run parallel fetch and print JSON to stdout
    if args.commits_range:
        since_str, until_str = args.commits_range
        since_dt = datetime.strptime(since_str, '%Y-%m-%d').date()
        until_dt = datetime.strptime(until_str, '%Y-%m-%d').date()
        try:
            summary = fetch_commits_parallel_from_config(str(args.config), since_dt, until_dt)
            print(json.dumps(summary, indent=2))
        except PermissionError as e:
            print(str(e), file=sys.stderr)
            sys.exit(1)
        return
    
    # Determine target date
    if args.date:
        target_date = datetime.strptime(args.date, '%Y-%m-%d').date()
    else:
        target_date = date.today()  # Default to today
    
    # Initialize collector (metrics file written inside run_data_collection on success path)
    try:
        collector = UnifiedDataCollector(args.config)
    except Exception as e:
        p = _default_run_metrics(target_date, datetime.now(timezone.utc).isoformat())
        p["errors"]["fatal"] = f"init_failed: {e}"[:2000]
        p["finished_at"] = datetime.now(timezone.utc).isoformat()
        p["duration_ms"] = 0
        p["success"] = False
        write_last_run_metrics(p)
        print(f"❌ Failed to initialize collector: {e}", file=sys.stderr)
        sys.exit(1)

    success = collector.run_data_collection(target_date)

    if success:
        print(f"\n✅ Unified data collection completed for {target_date}")
        print(f"📄 Run metrics: {LAST_RUN_METRICS_FILE}")
    else:
        print(f"\n❌ Unified data collection failed for {target_date}")
        print(f"📄 Run metrics: {LAST_RUN_METRICS_FILE}")
        sys.exit(1)


if __name__ == "__main__":
    main()
