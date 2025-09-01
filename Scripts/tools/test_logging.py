#!/usr/bin/env python3
"""
Test script for the logging system
"""

import sys
from pathlib import Path

# Add tools directory to path
sys.path.insert(0, str(Path(__file__).parent / "tools"))

from log_manager import LogManager

def main():
    """Test the logging system"""
    print("🧪 Testing Logging System")
    print("=" * 30)
    
    # Initialize log manager
    log_manager = LogManager(".")
    
    # Setup logging
    logger = log_manager.setup_logging("test_logging", logging.INFO)
    
    # Test logging
    logger.info("This is a test info message")
    logger.warning("This is a test warning message")
    logger.error("This is a test error message")
    
    print("✅ Logging test completed!")
    print("📁 Check Scripts/logs/test_logging.log for the log file")
    
    # Show log stats
    print("\n📊 Current Log Statistics:")
    log_manager.print_log_stats()

if __name__ == "__main__":
    import logging
    main()
