#!/usr/bin/env python3
"""
Unified Data Collector
GitHub data collection with Obsidian integration
Uses configuration file for all settings

NOTE: This file now imports from the modular structure.
For backwards compatibility, this file serves as the entry point.
The actual implementation is in main.py and related modules.
"""

import sys
from pathlib import Path

# Add Scripts directory to path so we can import as a package
_script_dir = Path(__file__).parent
_scripts_dir = _script_dir.parent
if str(_scripts_dir) not in sys.path:
    sys.path.insert(0, str(_scripts_dir))

# Import from package structure
from data_collectors.main import UnifiedDataCollector, main

# Re-export for backwards compatibility
__all__ = ['UnifiedDataCollector', 'main']

# Execute main if run as script
if __name__ == "__main__":
    main()
