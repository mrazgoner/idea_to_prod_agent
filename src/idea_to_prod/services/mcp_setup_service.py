"""
MCP Setup Service

Handles MCP configuration validation, persistence, and testing.
Provides a unified interface for both Desktop and Web UIs to manage MCPs.
"""

import logging
from typing import Dict, Any, Tuple, Optional
from datetime import datetime

logger = logging.getLogger(__name__)


class MCPSetupService:
    """
    Manages MCP configuration for setup and testing.
    
    Responsibilities:
    - Validate MCP configurations
    - Save configurations to persistent storage
    - Test MCPs with provided configurations
    - Load saved configurations
    - Provide configuration UI data
    """
    
    PLATFORM_SCHEMAS = {
        "GitHub": {
            "required": ["mode"],
            "optional": ["token", "username", "base_url", "enable_logging"],
            "description": "GitHub repository management"
        },
        "Jira": {
            "required": ["mode"],
            "optional": ["instance_url", "email", "api_token", "enable_logging"],
            "description": "Jira task management"
        },
        "Google Drive": {
            "required": ["mode"],
            "optional": ["credentials_path", "folder_id", "enable_logging"],
            "description": "Google Drive document storage"
        },
        "Playwright": {
            "required": ["mode"],
            "optional": ["headless", "timeout", "enable_logging"],
            "description": "Browser automation and testing"
        }
    }
    
    def __init__(self, config_store=None, connection_service=None):
        """
        Initialize the MCPSetupService.
        
        Args:
            config_store: ConfigStore instance. If None, creates a new one.
            connection_service: MCPConnectionService instance. If None, creates a new one.
        """
        if config_store is None:
            from .config_storage import ConfigStore
            config_store = ConfigStore()
        
        if connection_service is None:
            from .mcp_connection_service import MCPConnectionService
            connection_service = MCPConnectionService(config_store)
        
        self.config_store = config_store
        self.connection_service = connection_service
    
    def validate_config(self, platform: str, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Validate a configuration for a specific platform.
        
        Args:
            platform: Platform name
            config: Configuration dict to validate
        
        Returns:
            Tuple of (is_valid, error_message)
        """
        if platform not in self.PLATFORM_SCHEMAS:
            return False, f"Unknown platform: {platform}"
        
        schema = self.PLATFORM_SCHEMAS[platform]
        
        # Check required fields
        for field in schema["required"]:
            if field not in config:
                return False, f"Missing required field: {field}"
        
        # Validate mode field
        if config.get("mode") not in ["stub", "real", "direct"]:
            return False, "Mode must be 'stub', 'real', or 'direct'"
        
        # Platform-specific validation
        if platform == "GitHub":
            if config.get("mode") == "real" and not config.get("token"):
                return False, "GitHub token required for real mode"
        
        elif platform == "Jira":
            if config.get("mode") == "real":
                if not config.get("instance_url"):
                    return False, "Jira instance URL required for real mode"
                if not config.get("api_token"):
                    return False, "Jira API token required for real mode"
        
        elif platform == "Google Drive":
            if config.get("mode") == "real":
                if not config.get("credentials_path"):
                    return False, "Google Drive credentials path required for real mode"
        
        elif platform == "Playwright":
            if "timeout" in config:
                try:
                    timeout = int(config["timeout"])
                    if timeout <= 0:
                        return False, "Timeout must be positive"
                except (ValueError, TypeError):
                    return False, "Timeout must be an integer"
        
        return True, ""
    
    def save_config(self, platform: str, config: Dict[str, Any]) -> Tuple[bool, str]:
        """
        Save a configuration for a platform after validation.
        
        Args:
            platform: Platform name
            config: Configuration dict
        
        Returns:
            Tuple of (success, message)
        """
        # Validate first
        is_valid, error_msg = self.validate_config(platform, config)
        if not is_valid:
            return False, f"Validation failed: {error_msg}"
        
        try:
            self.config_store.save_config(platform, config)
            logger.info(f"Saved configuration for {platform}")
            return True, f"Configuration saved for {platform}"
        except Exception as e:
            logger.error(f"Failed to save {platform} config: {e}")
            return False, f"Failed to save configuration: {str(e)}"
    
    def load_config(self, platform: str) -> Optional[Dict[str, Any]]:
        """
        Load a saved configuration for a platform.
        
        Args:
            platform: Platform name
        
        Returns:
            Configuration dict or None if not found
        """
        return self.config_store.load_config(platform)
    
    def test_mcp(self, platform: str, config: Dict[str, Any]) -> Dict[str, Any]:
        """
        Test an MCP with a given configuration.
        
        Args:
            platform: Platform name
            config: Configuration to test
        
        Returns:
            Test result dict with 'success' bool and details
        """
        # Validate config first
        is_valid, error_msg = self.validate_config(platform, config)
        if not is_valid:
            return {
                "success": False,
                "platform": platform,
                "error": f"Validation failed: {error_msg}",
                "timestamp": datetime.now().isoformat()
            }
        
        try:
            # Temporarily save config for testing
            self.config_store.save_config(platform, config)
            
            # Get status
            status = self.connection_service.get_mcp_status(platform)
            
            # Test specific operations based on mode
            if config.get("mode") == "stub":
                test_result = self._test_stub_operations(platform)
            else:
                test_result = self._test_real_operations(platform)
            
            return {
                "success": status.get("connected", False),
                "platform": platform,
                "mode": config.get("mode"),
                "status": status,
                "operations_tested": test_result,
                "timestamp": datetime.now().isoformat()
            }
        
        except Exception as e:
            logger.error(f"Error testing {platform}: {e}")
            return {
                "success": False,
                "platform": platform,
                "error": str(e),
                "timestamp": datetime.now().isoformat()
            }
    
    def _test_stub_operations(self, platform: str) -> list:
        """
        Test stub mode operations (always succeed).
        
        Args:
            platform: Platform name
        
        Returns:
            List of tested operations
        """
        stub_tests = {
            "GitHub": [
                "list_repositories",
                "create_repository",
                "create_issue",
                "add_comment"
            ],
            "Jira": [
                "list_issues",
                "create_issue",
                "update_issue"
            ],
            "Google Drive": [
                "list_files",
                "create_file",
                "upload_file"
            ],
            "Playwright": [
                "launch_browser",
                "navigate_page",
                "take_screenshot"
            ]
        }
        
        operations = stub_tests.get(platform, [])
        return [{"name": op, "success": True} for op in operations]
    
    def _test_real_operations(self, platform: str) -> list:
        """
        Test real mode operations against actual APIs.
        
        Args:
            platform: Platform name
        
        Returns:
            List of tested operations with results
        """
        # This would test actual operations against real APIs
        # For now, return empty list - would be implemented per MCP
        logger.info(f"Real mode testing not yet fully implemented for {platform}")
        return []
    
    def list_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all saved MCP configurations.
        
        Returns:
            Dict mapping platform names to their configs
        """
        return self.config_store.list_all_configs()
    
    def delete_config(self, platform: str) -> Tuple[bool, str]:
        """
        Delete configuration for a platform.
        
        Args:
            platform: Platform name
        
        Returns:
            Tuple of (success, message)
        """
        try:
            if self.config_store.delete_config(platform):
                return True, f"Configuration deleted for {platform}"
            return False, f"No configuration found for {platform}"
        except Exception as e:
            return False, f"Failed to delete configuration: {str(e)}"
    
    def get_platform_schema(self, platform: str) -> Dict[str, Any]:
        """
        Get the configuration schema for a platform.
        
        Useful for UI to know what fields to display.
        
        Args:
            platform: Platform name
        
        Returns:
            Schema dict with required and optional fields
        """
        return self.PLATFORM_SCHEMAS.get(platform, {})
    
    def test_all_mcps(self) -> Dict[str, Dict[str, Any]]:
        """
        Test all configured MCPs.
        
        Returns:
            Dict mapping platform names to their test results
        """
        results = {}
        for platform in self.config_store.VALID_PLATFORMS:
            config = self.config_store.load_config(platform)
            if config:
                results[platform] = self.test_mcp(platform, config)
            else:
                results[platform] = {
                    "success": False,
                    "platform": platform,
                    "error": "Not configured",
                    "timestamp": datetime.now().isoformat()
                }
        
        return results
