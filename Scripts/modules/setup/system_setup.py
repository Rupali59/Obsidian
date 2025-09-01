#!/usr/bin/env python3
"""
System Setup Module
Handles initialization, configuration validation, and system health checks
"""

import os
import sys
import json
import logging
import requests
from pathlib import Path
from typing import Dict, List, Optional

class SystemSetup:
    def __init__(self, obsidian_path: str, config: Dict):
        self.obsidian_path = Path(obsidian_path)
        self.config = config
        self.setup_logger = logging.getLogger('setup')
        
    def run_setup(self, operation_config: Dict) -> Dict:
        """Run setup operation based on configuration"""
        try:
            self.setup_logger.info("Starting system setup...")
            
            results = {
                "success": True,
                "operations": [],
                "errors": []
            }
            
            # Validate GitHub token
            if operation_config.get("validate_github_token", True):
                result = self._validate_github_token()
                results["operations"].append(("validate_github_token", result))
                if not result["success"]:
                    results["errors"].append(f"GitHub token validation failed: {result['error']}")
            
            # Create directories
            if operation_config.get("create_directories", True):
                result = self._create_directories()
                results["operations"].append(("create_directories", result))
                if not result["success"]:
                    results["errors"].append(f"Directory creation failed: {result['error']}")
            
            # Setup logging
            if operation_config.get("setup_logging", True):
                result = self._setup_logging()
                results["operations"].append(("setup_logging", result))
                if not result["success"]:
                    results["errors"].append(f"Logging setup failed: {result['error']}")
            
            # Test API connection
            if operation_config.get("test_api_connection", True):
                result = self._test_api_connection()
                results["operations"].append(("test_api_connection", result))
                if not result["success"]:
                    results["errors"].append(f"API connection test failed: {result['error']}")
            
            # Check for errors
            if results["errors"]:
                results["success"] = False
                self.setup_logger.error(f"Setup completed with errors: {results['errors']}")
            else:
                self.setup_logger.info("System setup completed successfully!")
            
            return results
            
        except Exception as e:
            self.setup_logger.error(f"Setup failed: {e}")
            return {
                "success": False,
                "operations": [],
                "errors": [str(e)]
            }
    
    def run_health_check(self, operation_config: Dict) -> Dict:
        """Run system health check"""
        try:
            self.setup_logger.info("Starting system health check...")
            
            results = {
                "success": True,
                "checks": [],
                "errors": []
            }
            
            # Check GitHub API
            if operation_config.get("check_github_api", True):
                result = self._check_github_api()
                results["checks"].append(("github_api", result))
                if not result["success"]:
                    results["errors"].append(f"GitHub API check failed: {result['error']}")
            
            # Check directories
            if operation_config.get("check_directories", True):
                result = self._check_directories()
                results["checks"].append(("directories", result))
                if not result["success"]:
                    results["errors"].append(f"Directory check failed: {result['error']}")
            
            # Check permissions
            if operation_config.get("check_permissions", True):
                result = self._check_permissions()
                results["checks"].append(("permissions", result))
                if not result["success"]:
                    results["errors"].append(f"Permission check failed: {result['error']}")
            
            # Validate configuration
            if operation_config.get("validate_config", True):
                result = self._validate_configuration()
                results["checks"].append(("configuration", result))
                if not result["success"]:
                    results["errors"].append(f"Configuration validation failed: {result['error']}")
            
            # Check for errors
            if results["errors"]:
                results["success"] = False
                self.setup_logger.error(f"Health check completed with errors: {results['errors']}")
            else:
                self.setup_logger.info("System health check passed!")
            
            return results
            
        except Exception as e:
            self.setup_logger.error(f"Health check failed: {e}")
            return {
                "success": False,
                "checks": [],
                "errors": [str(e)]
            }
    
    def _validate_github_token(self) -> Dict:
        """Validate GitHub token"""
        try:
            config_path = self.obsidian_path / "Scripts" / "config" / "github_config.env"
            
            if not config_path.exists():
                return {"success": False, "error": "GitHub config file not found"}
            
            # Read token
            github_token = None
            with open(config_path, 'r') as f:
                for line in f:
                    line = line.strip()
                    if line.startswith('GITHUB_TOKEN='):
                        github_token = line.split('=', 1)[1]
                        break
            
            if not github_token:
                return {"success": False, "error": "GitHub token not found in config"}
            
            # Test token
            headers = {'Authorization': f'token {github_token}'}
            response = requests.get("https://api.github.com/user", headers=headers, timeout=10)
            
            if response.status_code == 200:
                user_data = response.json()
                return {
                    "success": True,
                    "message": f"Token valid for user: {user_data.get('login', 'Unknown')}",
                    "rate_limit": response.headers.get('X-RateLimit-Remaining', 'Unknown')
                }
            else:
                return {"success": False, "error": f"Token validation failed: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _create_directories(self) -> Dict:
        """Create necessary directories"""
        try:
            directories = [
                self.obsidian_path / "Scripts" / "logs",
                self.obsidian_path / "Scripts" / "cache",
                self.obsidian_path / "Calendar" / "2025",
                self.obsidian_path / "Scripts" / "modules" / "data" / "temp"
            ]
            
            created = []
            for directory in directories:
                directory.mkdir(parents=True, exist_ok=True)
                created.append(str(directory))
            
            return {
                "success": True,
                "message": f"Created {len(created)} directories",
                "directories": created
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _setup_logging(self) -> Dict:
        """Setup logging configuration"""
        try:
            log_dir = self.obsidian_path / "Scripts" / "logs"
            log_dir.mkdir(parents=True, exist_ok=True)
            
            # Configure logging
            logging.basicConfig(
                level=logging.INFO,
                format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                handlers=[
                    logging.FileHandler(log_dir / 'system.log'),
                    logging.StreamHandler()
                ]
            )
            
            return {
                "success": True,
                "message": "Logging configured successfully",
                "log_file": str(log_dir / 'system.log')
            }
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _test_api_connection(self) -> Dict:
        """Test GitHub API connection"""
        try:
            response = requests.get("https://api.github.com/rate_limit", timeout=10)
            
            if response.status_code == 200:
                rate_data = response.json()
                return {
                    "success": True,
                    "message": "API connection successful",
                    "rate_limit": rate_data.get('rate', {})
                }
            else:
                return {"success": False, "error": f"API connection failed: {response.status_code}"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _check_github_api(self) -> Dict:
        """Check GitHub API status"""
        return self._test_api_connection()
    
    def _check_directories(self) -> Dict:
        """Check if required directories exist"""
        try:
            required_dirs = [
                self.obsidian_path / "Scripts" / "config",
                self.obsidian_path / "Scripts" / "modules",
                self.obsidian_path / "Calendar"
            ]
            
            missing = []
            for directory in required_dirs:
                if not directory.exists():
                    missing.append(str(directory))
            
            if missing:
                return {"success": False, "error": f"Missing directories: {missing}"}
            else:
                return {"success": True, "message": "All required directories exist"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _check_permissions(self) -> Dict:
        """Check file system permissions"""
        try:
            test_file = self.obsidian_path / "Scripts" / "logs" / "permission_test.tmp"
            
            # Test write permission
            test_file.parent.mkdir(parents=True, exist_ok=True)
            test_file.write_text("test")
            test_file.unlink()
            
            return {"success": True, "message": "File system permissions OK"}
            
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    def _validate_configuration(self) -> Dict:
        """Validate system configuration"""
        try:
            config_files = [
                self.obsidian_path / "Scripts" / "config" / "system_config.json",
                self.obsidian_path / "Scripts" / "config" / "operation_configs.json",
                self.obsidian_path / "Scripts" / "config" / "github_config.env",
                self.obsidian_path / "Scripts" / "config" / "repos_to_track.env"
            ]
            
            missing = []
            for config_file in config_files:
                if not config_file.exists():
                    missing.append(str(config_file))
            
            if missing:
                return {"success": False, "error": f"Missing config files: {missing}"}
            else:
                return {"success": True, "message": "All configuration files present"}
                
        except Exception as e:
            return {"success": False, "error": str(e)}
