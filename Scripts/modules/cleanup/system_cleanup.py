#!/usr/bin/env python3
"""
System Cleanup Module
Handles cleanup of logs, backups, and temporary files
"""

import os
import sys
import json
import logging
from pathlib import Path
from datetime import datetime, timedelta
from typing import Dict, List, Optional

class SystemCleanup:
    def __init__(self, obsidian_path: str, config: Dict):
        self.obsidian_path = Path(obsidian_path)
        self.config = config
        self.cleanup_logger = logging.getLogger('cleanup')
        
    def run_cleanup_logs(self, operation_config: Dict) -> Dict:
        """Clean up old log files"""
        try:
            retention_days = operation_config.get("retention_days", 7)
            dry_run = operation_config.get("dry_run", False)
            
            self.cleanup_logger.info(f"Cleaning up logs older than {retention_days} days (dry_run={dry_run})")
            
            return self._cleanup_files_by_age(
                self.obsidian_path / "Scripts" / "logs",
                retention_days,
                dry_run,
                "log files"
            )
            
        except Exception as e:
            self.cleanup_logger.error(f"Log cleanup failed: {e}")
            return {"success": False, "error": str(e)}
    
    def run_cleanup_backups(self, operation_config: Dict) -> Dict:
        """Clean up old backup files"""
        try:
            retention_days = operation_config.get("retention_days", 3)
            dry_run = operation_config.get("dry_run", False)
            
            self.cleanup_logger.info(f"Cleaning up backups older than {retention_days} days (dry_run={dry_run})")
            
            return self._cleanup_files_by_age(
                self.obsidian_path / "Calendar",
                retention_days,
                dry_run,
                "backup files",
                pattern="*.backup"
            )
            
        except Exception as e:
            self.cleanup_logger.error(f"Backup cleanup failed: {e}")
            return {"success": False, "error": str(e)}
    
    def run_cleanup_temp_files(self, operation_config: Dict) -> Dict:
        """Clean up temporary files"""
        try:
            dry_run = operation_config.get("dry_run", False)
            
            self.cleanup_logger.info(f"Cleaning up temporary files (dry_run={dry_run})")
            
            temp_dirs = [
                self.obsidian_path / "Scripts" / "modules" / "data" / "temp",
                self.obsidian_path / "Scripts" / "cache"
            ]
            
            results = {
                "success": True,
                "files_removed": 0,
                "directories_cleaned": 0,
                "errors": []
            }
            
            for temp_dir in temp_dirs:
                if temp_dir.exists():
                    try:
                        result = self._cleanup_directory(temp_dir, dry_run)
                        results["files_removed"] += result["files_removed"]
                        results["directories_cleaned"] += 1
                    except Exception as e:
                        results["errors"].append(f"Error cleaning {temp_dir}: {e}")
            
            if results["errors"]:
                results["success"] = False
            
            return results
            
        except Exception as e:
            self.cleanup_logger.error(f"Temp file cleanup failed: {e}")
            return {"success": False, "error": str(e)}
    
    def run_full_cleanup(self, operation_config: Dict) -> Dict:
        """Run full system cleanup"""
        try:
            self.cleanup_logger.info("Starting full system cleanup...")
            
            results = {
                "success": True,
                "operations": [],
                "errors": []
            }
            
            # Clean up logs
            log_result = self.run_cleanup_logs(operation_config)
            results["operations"].append(("cleanup_logs", log_result))
            if not log_result["success"]:
                results["errors"].append(f"Log cleanup failed: {log_result.get('error', 'Unknown error')}")
            
            # Clean up backups
            backup_result = self.run_cleanup_backups(operation_config)
            results["operations"].append(("cleanup_backups", backup_result))
            if not backup_result["success"]:
                results["errors"].append(f"Backup cleanup failed: {backup_result.get('error', 'Unknown error')}")
            
            # Clean up temp files
            temp_result = self.run_cleanup_temp_files(operation_config)
            results["operations"].append(("cleanup_temp_files", temp_result))
            if not temp_result["success"]:
                results["errors"].append(f"Temp file cleanup failed: {temp_result.get('error', 'Unknown error')}")
            
            # Check for errors
            if results["errors"]:
                results["success"] = False
                self.cleanup_logger.error(f"Full cleanup completed with errors: {results['errors']}")
            else:
                self.cleanup_logger.info("Full system cleanup completed successfully!")
            
            return results
            
        except Exception as e:
            self.cleanup_logger.error(f"Full cleanup failed: {e}")
            return {"success": False, "error": str(e)}
    
    def _cleanup_files_by_age(self, directory: Path, retention_days: int, dry_run: bool, file_type: str, pattern: str = "*") -> Dict:
        """Clean up files older than specified days"""
        try:
            if not directory.exists():
                return {
                    "success": True,
                    "message": f"Directory {directory} does not exist",
                    "files_removed": 0
                }
            
            cutoff_date = datetime.now() - timedelta(days=retention_days)
            files_removed = 0
            files_checked = 0
            
            for file_path in directory.rglob(pattern):
                if file_path.is_file():
                    files_checked += 1
                    file_mtime = datetime.fromtimestamp(file_path.stat().st_mtime)
                    
                    if file_mtime < cutoff_date:
                        if not dry_run:
                            file_path.unlink()
                            self.cleanup_logger.info(f"Removed {file_type}: {file_path}")
                        else:
                            self.cleanup_logger.info(f"Would remove {file_type}: {file_path}")
                        files_removed += 1
            
            action = "Would remove" if dry_run else "Removed"
            message = f"{action} {files_removed} {file_type} (checked {files_checked} files)"
            
            return {
                "success": True,
                "message": message,
                "files_removed": files_removed,
                "files_checked": files_checked,
                "dry_run": dry_run
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _cleanup_directory(self, directory: Path, dry_run: bool) -> Dict:
        """Clean up all files in a directory"""
        try:
            if not directory.exists():
                return {
                    "success": True,
                    "message": f"Directory {directory} does not exist",
                    "files_removed": 0
                }
            
            files_removed = 0
            
            for file_path in directory.iterdir():
                if file_path.is_file():
                    if not dry_run:
                        file_path.unlink()
                        self.cleanup_logger.info(f"Removed temp file: {file_path}")
                    else:
                        self.cleanup_logger.info(f"Would remove temp file: {file_path}")
                    files_removed += 1
            
            action = "Would remove" if dry_run else "Removed"
            message = f"{action} {files_removed} temporary files from {directory}"
            
            return {
                "success": True,
                "message": message,
                "files_removed": files_removed,
                "dry_run": dry_run
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def get_cleanup_stats(self) -> Dict:
        """Get statistics about files that can be cleaned up"""
        try:
            stats = {
                "log_files": self._get_file_stats(self.obsidian_path / "Scripts" / "logs", "*.log"),
                "backup_files": self._get_file_stats(self.obsidian_path / "Calendar", "*.backup"),
                "temp_files": self._get_file_stats(self.obsidian_path / "Scripts" / "modules" / "data" / "temp", "*")
            }
            
            return {
                "success": True,
                "stats": stats
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _get_file_stats(self, directory: Path, pattern: str) -> Dict:
        """Get statistics about files in a directory"""
        try:
            if not directory.exists():
                return {"count": 0, "total_size": 0, "oldest_file": None, "newest_file": None}
            
            files = list(directory.rglob(pattern))
            if not files:
                return {"count": 0, "total_size": 0, "oldest_file": None, "newest_file": None}
            
            total_size = sum(f.stat().st_size for f in files if f.is_file())
            file_times = [(f, f.stat().st_mtime) for f in files if f.is_file()]
            
            if file_times:
                oldest_file = min(file_times, key=lambda x: x[1])[0]
                newest_file = max(file_times, key=lambda x: x[1])[0]
            else:
                oldest_file = newest_file = None
            
            return {
                "count": len(files),
                "total_size": total_size,
                "total_size_mb": round(total_size / (1024 * 1024), 2),
                "oldest_file": str(oldest_file) if oldest_file else None,
                "newest_file": str(newest_file) if newest_file else None
            }
            
        except Exception as e:
            return {"error": str(e)}
