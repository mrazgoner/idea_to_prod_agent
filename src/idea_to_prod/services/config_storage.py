"""
Configuration Storage Service

Handles persistent storage of MCP configurations using JSON files.
Provides a single source of truth for all MCP settings.
"""

import json
import logging
from pathlib import Path
from typing import Dict, Any, Optional

logger = logging.getLogger(__name__)


class ConfigStore:
    """
    Manages persistent storage of MCP configurations.
    
    Stores configurations in a JSON file in the workspace root.
    Supports multiple MCP platforms: GitHub, Jira, Google Drive, Playwright.
    """
    
    DEFAULT_CONFIG_FILE = Path.home() / ".idea_to_prod" / "mcp_config.json"
    
    VALID_PLATFORMS = ["GitHub", "Jira", "Google Drive", "Playwright"]
    
    def __init__(self, config_file: Optional[Path] = None):
        """
        Initialize the ConfigStore.
        
        Args:
            config_file: Path to config file. Defaults to ~/.idea_to_prod/mcp_config.json
        """
        self.config_file = config_file or self.DEFAULT_CONFIG_FILE
        self.config_file.parent.mkdir(parents=True, exist_ok=True)
        self._configs = self._load_configs()
    
    def _load_configs(self) -> Dict[str, Dict[str, Any]]:
        """Load all configurations from file."""
        if self.config_file.exists():
            try:
                with open(self.config_file, 'r') as f:
                    return json.load(f)
            except Exception as e:
                logger.warning(f"Failed to load config file: {e}. Starting fresh.")
                return {}
        return {}
    
    def _save_configs(self) -> None:
        """Save all configurations to file."""
        try:
            self.config_file.parent.mkdir(parents=True, exist_ok=True)
            with open(self.config_file, 'w') as f:
                json.dump(self._configs, f, indent=2)
        except Exception as e:
            logger.error(f"Failed to save config file: {e}")
            raise
    
    def load_config(self, platform: str) -> Optional[Dict[str, Any]]:
        """
        Load configuration for a specific platform.
        
        Args:
            platform: Platform name (GitHub, Jira, Google Drive, Playwright)
        
        Returns:
            Configuration dict or None if not found
        """
        if platform not in self.VALID_PLATFORMS:
            raise ValueError(f"Invalid platform: {platform}. Valid: {self.VALID_PLATFORMS}")
        
        return self._configs.get(platform)
    
    def save_config(self, platform: str, config: Dict[str, Any]) -> bool:
        """
        Save configuration for a specific platform.
        
        Args:
            platform: Platform name
            config: Configuration dict
        
        Returns:
            True if saved successfully
        """
        if platform not in self.VALID_PLATFORMS:
            raise ValueError(f"Invalid platform: {platform}. Valid: {self.VALID_PLATFORMS}")
        
        self._configs[platform] = config
        self._save_configs()
        logger.info(f"Saved config for {platform}")
        return True
    
    def delete_config(self, platform: str) -> bool:
        """
        Delete configuration for a specific platform.
        
        Args:
            platform: Platform name
        
        Returns:
            True if deleted, False if not found
        """
        if platform not in self.VALID_PLATFORMS:
            raise ValueError(f"Invalid platform: {platform}")
        
        if platform in self._configs:
            del self._configs[platform]
            self._save_configs()
            logger.info(f"Deleted config for {platform}")
            return True
        return False
    
    def list_all_configs(self) -> Dict[str, Dict[str, Any]]:
        """
        Get all saved configurations.
        
        Returns:
            Dict mapping platform names to their configs
        """
        return self._configs.copy()
    
    def has_config(self, platform: str) -> bool:
        """
        Check if configuration exists for a platform.
        
        Args:
            platform: Platform name
        
        Returns:
            True if config exists
        """
        return platform in self._configs
    
    def clear_all(self) -> None:
        """Clear all configurations. Use with caution."""
        self._configs = {}
        self._save_configs()
        logger.warning("Cleared all configurations")
