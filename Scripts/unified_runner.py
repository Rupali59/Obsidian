#!/usr/bin/env python3
"""
Unified GitHub Metrics System Runner
Single entry point for all system operations with configuration-driven functionality
"""

import os
import sys
import json
import logging
import argparse
from pathlib import Path
from typing import Dict, Optional

# Add modules to path
sys.path.insert(0, str(Path(__file__).parent / "modules" / "setup"))
sys.path.insert(0, str(Path(__file__).parent / "modules" / "data"))
sys.path.insert(0, str(Path(__file__).parent / "modules" / "cleanup"))

from system_setup import SystemSetup
from data_acquisition import DataAcquisition
from system_cleanup import SystemCleanup

class UnifiedRunner:
    def __init__(self, obsidian_path: str):
        self.obsidian_path = Path(obsidian_path)
        self.config = self._load_system_config()
        self.operation_configs = self._load_operation_configs()
        
        # Setup logging
        self._setup_logging()
        self.logger = logging.getLogger('unified_runner')
        
        # Initialize modules
        self.setup_module = SystemSetup(str(obsidian_path), self.config)
        self.data_module = DataAcquisition(str(obsidian_path), self.config)
        self.cleanup_module = SystemCleanup(str(obsidian_path), self.config)
        
        self.logger.info("Unified Runner initialized successfully")
    
    def _load_system_config(self) -> Dict:
        """Load system configuration"""
        config_path = self.obsidian_path / "Scripts" / "config" / "system_config.json"
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading system config: {e}")
            return {}
    
    def _load_operation_configs(self) -> Dict:
        """Load operation configurations"""
        config_path = self.obsidian_path / "Scripts" / "config" / "operation_configs.json"
        
        try:
            with open(config_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading operation configs: {e}")
            return {}
    
    def _setup_logging(self):
        """Setup logging configuration"""
        log_dir = self.obsidian_path / "Scripts" / "logs"
        log_dir.mkdir(parents=True, exist_ok=True)
        
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_dir / 'unified_runner.log'),
                logging.StreamHandler()
            ]
        )
    
    def run_operation(self, operation_name: str, custom_config: Optional[Dict] = None) -> Dict:
        """Run a specific operation"""
        try:
            if operation_name not in self.operation_configs["operations"]:
                return {
                    "success": False,
                    "error": f"Unknown operation: {operation_name}"
                }
            
            operation = self.operation_configs["operations"][operation_name]
            module_name = operation["module"]
            operation_config = operation["config"].copy()
            
            # Override with custom config if provided
            if custom_config:
                operation_config.update(custom_config)
            
            self.logger.info(f"Running operation: {operation_name} using module: {module_name}")
            print(f"🚀 Running: {operation['name']}")
            print(f"📝 Description: {operation['description']}")
            print("=" * 60)
            
            # Route to appropriate module
            if module_name == "setup":
                if operation_name == "system_health":
                    result = self.setup_module.run_health_check(operation_config)
                else:
                    result = self.setup_module.run_setup(operation_config)
            
            elif module_name == "data":
                if operation_name == "capture_today":
                    result = self.data_module.run_capture_today(operation_config)
                elif operation_name == "capture_date_range":
                    result = self.data_module.run_capture_date_range(operation_config)
                elif operation_name == "capture_month":
                    result = self.data_module.run_capture_month(operation_config)
                else:
                    result = {"success": False, "error": f"Unknown data operation: {operation_name}"}
            
            elif module_name == "cleanup":
                if operation_name == "cleanup_logs":
                    result = self.cleanup_module.run_cleanup_logs(operation_config)
                elif operation_name == "cleanup_backups":
                    result = self.cleanup_module.run_cleanup_backups(operation_config)
                else:
                    result = {"success": False, "error": f"Unknown cleanup operation: {operation_name}"}
            
            else:
                result = {"success": False, "error": f"Unknown module: {module_name}"}
            
            # Print result summary
            self._print_operation_result(operation_name, result)
            
            return result
            
        except Exception as e:
            self.logger.error(f"Operation {operation_name} failed: {e}")
            return {"success": False, "error": str(e)}
    
    def list_operations(self) -> None:
        """List all available operations"""
        print("📋 Available Operations:")
        print("=" * 60)
        
        for op_name, op_config in self.operation_configs["operations"].items():
            print(f"🔧 {op_name}")
            print(f"   Name: {op_config['name']}")
            print(f"   Description: {op_config['description']}")
            print(f"   Module: {op_config['module']}")
            print()
    
    def _print_operation_result(self, operation_name: str, result: Dict):
        """Print operation result summary"""
        print("=" * 60)
        
        if result.get("success", False):
            print(f"✅ Operation '{operation_name}' completed successfully!")
            
            # Print specific result details
            if "summary" in result:
                summary = result["summary"]
                if "total_commits" in summary:
                    print(f"📊 Results: {summary.get('total_commits', 0)} commits, {summary.get('total_prs', 0)} PRs, {summary.get('total_issues', 0)} issues")
                if "api_calls_made" in summary:
                    print(f"⚡ API calls: {summary.get('api_calls_made', 0)} (saved {summary.get('api_calls_saved', 0)})")
            
            if "operations" in result:
                print(f"🔧 Operations completed: {len(result['operations'])}")
            
            if "checks" in result:
                print(f"🔍 Health checks passed: {len(result['checks'])}")
            
            if "files_removed" in result:
                print(f"🗑️  Files removed: {result['files_removed']}")
        
        else:
            print(f"❌ Operation '{operation_name}' failed!")
            if "error" in result:
                print(f"   Error: {result['error']}")
            if "errors" in result:
                print(f"   Errors: {result['errors']}")
        
        print("=" * 60)

def main():
    """Main function"""
    parser = argparse.ArgumentParser(description="Unified GitHub Metrics System Runner")
    parser.add_argument("obsidian_path", help="Path to Obsidian vault")
    parser.add_argument("operation", nargs='?', help="Operation to run")
    parser.add_argument("--config", help="Custom configuration JSON string")
    parser.add_argument("--list", action="store_true", help="List available operations")
    
    args = parser.parse_args()
    
    try:
        runner = UnifiedRunner(args.obsidian_path)
        
        if args.list:
            runner.list_operations()
            return
        
        if not args.operation:
            print("Error: Operation is required when --list is not specified")
            parser.print_help()
            sys.exit(1)
        
        # Parse custom config if provided
        custom_config = None
        if args.config:
            try:
                custom_config = json.loads(args.config)
            except json.JSONDecodeError as e:
                print(f"Error parsing custom config: {e}")
                sys.exit(1)
        
        # Run operation
        result = runner.run_operation(args.operation, custom_config)
        
        if not result.get("success", False):
            sys.exit(1)
            
    except Exception as e:
        print(f"❌ Runner failed: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
