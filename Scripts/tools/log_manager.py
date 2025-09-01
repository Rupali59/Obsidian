#!/usr/bin/env python3
"""
Log Management Utility
Handles log rotation and organization within the Scripts folder
"""

import os
import glob
import shutil
from pathlib import Path
from datetime import datetime, timedelta
import logging
from logging.handlers import RotatingFileHandler

class LogManager:
    def __init__(self, scripts_path: str):
        self.scripts_path = Path(scripts_path)
        self.logs_path = self.scripts_path / "logs"
        self.max_log_size = 10 * 1024 * 1024  # 10MB
        self.backup_count = 5  # Keep 5 backup files
        
    def setup_logging(self, log_name: str, log_level=logging.INFO):
        """Setup logging with rotation"""
        self.logs_path.mkdir(exist_ok=True)
        
        # Create log file path
        log_file = self.logs_path / f"{log_name}.log"
        
        # Setup rotating file handler
        handler = RotatingFileHandler(
            log_file,
            maxBytes=self.max_log_size,
            backupCount=self.backup_count
        )
        
        # Setup formatter
        formatter = logging.Formatter(
            '%(asctime)s - %(levelname)s - %(message)s',
            datefmt='%Y-%m-%d %H:%M:%S'
        )
        handler.setFormatter(formatter)
        
        # Setup logger
        logger = logging.getLogger(log_name)
        logger.setLevel(log_level)
        logger.addHandler(handler)
        
        # Also add console handler for immediate feedback
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)
        
        return logger
    
    def cleanup_old_logs(self, days_to_keep=30):
        """Clean up log files older than specified days"""
        cutoff_date = datetime.now() - timedelta(days=days_to_keep)
        
        # Find all log files
        log_files = glob.glob(str(self.logs_path / "*.log*"))
        
        cleaned_count = 0
        for log_file in log_files:
            file_path = Path(log_file)
            if file_path.exists():
                # Check file modification time
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                if mtime < cutoff_date:
                    try:
                        file_path.unlink()
                        cleaned_count += 1
                        print(f"🧹 Cleaned up old log: {file_path.name}")
                    except Exception as e:
                        print(f"⚠️  Could not delete {file_path.name}: {e}")
        
        return cleaned_count
    
    def get_log_stats(self):
        """Get statistics about log files"""
        log_files = glob.glob(str(self.logs_path / "*.log*"))
        
        stats = {
            'total_files': len(log_files),
            'total_size': 0,
            'files': []
        }
        
        for log_file in log_files:
            file_path = Path(log_file)
            if file_path.exists():
                size = file_path.stat().st_size
                mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                stats['total_size'] += size
                stats['files'].append({
                    'name': file_path.name,
                    'size': size,
                    'modified': mtime
                })
        
        return stats
    
    def print_log_stats(self):
        """Print log statistics"""
        stats = self.get_log_stats()
        
        print("📊 Log Statistics")
        print("=" * 40)
        print(f"Total log files: {stats['total_files']}")
        print(f"Total size: {stats['total_size'] / (1024*1024):.2f} MB")
        print()
        
        if stats['files']:
            print("Log files:")
            for file_info in sorted(stats['files'], key=lambda x: x['modified'], reverse=True):
                size_mb = file_info['size'] / (1024*1024)
                print(f"  {file_info['name']:<30} {size_mb:>8.2f} MB  {file_info['modified'].strftime('%Y-%m-%d %H:%M')}")
        
        print("=" * 40)

def main():
    """Main function for log management"""
    import sys
    
    if len(sys.argv) > 1:
        scripts_path = sys.argv[1]
    else:
        scripts_path = "."
    
    log_manager = LogManager(scripts_path)
    
    if len(sys.argv) > 2 and sys.argv[2] == "cleanup":
        print("🧹 Cleaning up old logs...")
        cleaned = log_manager.cleanup_old_logs()
        print(f"✅ Cleaned up {cleaned} old log files")
    elif len(sys.argv) > 2 and sys.argv[2] == "stats":
        log_manager.print_log_stats()
    else:
        print("Log Manager - Available commands:")
        print("  python3 log_manager.py . stats     # Show log statistics")
        print("  python3 log_manager.py . cleanup   # Clean up old logs")
        print("  python3 log_manager.py .           # Show this help")

if __name__ == "__main__":
    main()
