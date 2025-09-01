#!/usr/bin/env python3
"""
Quick launcher for the GitHub Metrics System
Redirects to the main launcher in the tools directory
"""

import sys
import subprocess
from pathlib import Path

def main():
    """Launch the main launcher"""
    tools_dir = Path(__file__).parent / "tools"
    launcher_path = tools_dir / "launcher.py"
    
    if not launcher_path.exists():
        print("❌ Main launcher not found!")
        print(f"Expected location: {launcher_path}")
        sys.exit(1)
    
    print("🚀 Launching GitHub Metrics System...")
    print("=" * 40)
    
    # Change to tools directory and run launcher
    try:
        subprocess.run([sys.executable, str(launcher_path)], cwd=tools_dir)
    except KeyboardInterrupt:
        print("\n👋 Goodbye!")
    except Exception as e:
        print(f"❌ Error launching system: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
