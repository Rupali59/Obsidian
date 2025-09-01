#!/usr/bin/env python3
"""
Simple launcher for the Unified GitHub Metrics System
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch the unified runner"""
    # Get the Obsidian vault path (parent directory of Scripts)
    obsidian_path = Path(__file__).parent.parent
    
    print("🚀 GitHub Metrics System - Unified Runner")
    print("=" * 50)
    
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python3 Scripts/run.py <operation>")
        print("  python3 Scripts/run.py --list")
        print()
        print("Examples:")
        print("  python3 Scripts/run.py setup")
        print("  python3 Scripts/run.py capture_today")
        print("  python3 Scripts/run.py capture_month")
        print("  python3 Scripts/run.py cleanup_logs")
        print("  python3 Scripts/run.py system_health")
        print()
        print("Run 'python3 Scripts/run.py --list' to see all available operations")
        sys.exit(1)
    
    # Build command
    cmd = [sys.executable, str(Path(__file__).parent / "unified_runner.py"), str(obsidian_path)] + sys.argv[1:]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()