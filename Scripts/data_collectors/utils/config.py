"""
Configuration loading and environment setup utilities
"""

import os
import json
from pathlib import Path
from typing import Dict, Optional

# Try to load python-dotenv if available
try:
    from dotenv import load_dotenv
    DOTENV_AVAILABLE = True
except ImportError:
    DOTENV_AVAILABLE = False


def setup_env(config_path: Optional[Path] = None) -> None:
    """Load environment variables from .env file if available"""
    if not DOTENV_AVAILABLE:
        return
    
    if config_path:
        # Try loading from .env in the workspace root or script directory
        env_path = config_path.parent.parent.parent / '.env'
        if not env_path.exists():
            env_path = config_path.parent / '.env'
        if env_path.exists():
            load_dotenv(env_path)


def load_config(config_path: Path) -> Dict:
    """Load configuration from JSON file"""
    try:
        with open(config_path, 'r') as f:
            config = json.load(f)
        return config
    except Exception as e:
        print(f"❌ Failed to load config: {e}")
        return {}
