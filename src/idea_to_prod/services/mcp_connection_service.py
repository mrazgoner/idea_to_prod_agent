"""
MCP Connection Service

Manages the lifecycle of MCP server instances.
Initializes MCPs with saved configurations and provides access to them.
"""

import logging
from typing import Dict, Any, Optional
from pathlib import Path
import sys

logger = logging.getLogger(__name__)


class MCPConnectionService:
    """
    Manages MCP server instances and their lifecycle.
    
    Responsibilities:
    - Initialize MCP servers with saved configurations
    - Cache MCP instances for reuse
    - Provide access to initialized MCPs
    - Test MCP connections
    - Handle MCP lifecycle (init, close)
    """
    
    def __init__(self, config_store=None):
        """
        Initialize the MCPConnectionService.
        
        Args:
            config_store: ConfigStore instance. If None, creates a new one.
        """
        if config_store is None:
            from .config_storage import ConfigStore
            config_store = ConfigStore()
        
        self.config_store = config_store
        self._mcp_instances: Dict[str, Any] = {}
        self._initialized = set()
    
    def initialize_mcp(self, platform: str) -> Optional[Any]:
        """
        Initialize an MCP instance with saved configuration.
        
        Args:
            platform: Platform name (GitHub, Jira, Google Drive, Playwright)
        
        Returns:
            Initialized MCP instance or None if initialization fails
        """
        # Return cached instance if already initialized
        if platform in self._initialized:
            return self._mcp_instances.get(platform)
        
        # Load config for this platform
        config = self.config_store.load_config(platform)
        if config is None:
            logger.warning(f"No configuration found for {platform}. Using stub mode.")
            config = {"mode": "stub", "enable_logging": False}
        
        try:
            mcp_instance = self._create_mcp_instance(platform, config)
            if mcp_instance:
                self._mcp_instances[platform] = mcp_instance
                self._initialized.add(platform)
                logger.info(f"Initialized {platform} MCP")
                return mcp_instance
        except Exception as e:
            logger.error(f"Failed to initialize {platform} MCP: {e}")
        
        return None
    
    def _create_mcp_instance(self, platform: str, config: Dict[str, Any]) -> Optional[Any]:
        """
        Create an MCP instance based on platform and config.
        
        Args:
            platform: Platform name
            config: Configuration dict
        
        Returns:
            MCP instance or None
        """
        try:
            workspace = Path(__file__).parent.parent.parent.parent
            src_path = workspace / "src"
            
            if platform == "GitHub":
                from idea_to_prod.mcp_servers.config.github_config import GitHubConfig
                from idea_to_prod.mcp_servers.github_mcp import GitHubMCPServer
                
                github_config = GitHubConfig(**config)
                return GitHubMCPServer(github_config)
            
            elif platform == "Jira":
                from idea_to_prod.mcp_servers.config.jira_config import JiraConfig
                from idea_to_prod.mcp_servers.jira_mcp import JiraMCPServer
                
                jira_config = JiraConfig(**config)
                return JiraMCPServer(jira_config)
            
            elif platform == "Google Drive":
                from idea_to_prod.mcp_servers.config.google_drive_config import GoogleDriveConfig
                from idea_to_prod.mcp_servers.google_drive_mcp import GoogleDriveMCPServer
                
                gdrive_config = GoogleDriveConfig(**config)
                return GoogleDriveMCPServer(gdrive_config)
            
            elif platform == "Playwright":
                from idea_to_prod.mcp_servers.config.playwright_config import PlaywrightConfig
                from idea_to_prod.mcp_servers.playwright_mcp import PlaywrightMCPServer
                
                pw_config = PlaywrightConfig(**config)
                return PlaywrightMCPServer(pw_config)
            
            else:
                logger.error(f"Unknown platform: {platform}")
                return None
        
        except Exception as e:
            logger.error(f"Error creating {platform} MCP instance: {e}")
            return None
    
    def get_mcp(self, platform: str) -> Optional[Any]:
        """
        Get an initialized MCP instance.
        
        Args:
            platform: Platform name
        
        Returns:
            MCP instance or None if not initialized
        """
        if platform not in self._initialized:
            self.initialize_mcp(platform)
        
        return self._mcp_instances.get(platform)
    
    def get_mcp_status(self, platform: str) -> Dict[str, Any]:
        """
        Get connection status for an MCP.
        
        Args:
            platform: Platform name
        
        Returns:
            Status dict with 'connected' bool and other details
        """
        mcp = self.get_mcp(platform)
        
        if mcp is None:
            return {
                "platform": platform,
                "connected": False,
                "reason": "Not initialized"
            }
        
        try:
            # Try to get a basic status from the MCP
            if hasattr(mcp, 'test_connection'):
                result = mcp.test_connection()
                return {
                    "platform": platform,
                    "connected": result.get("success", False),
                    "details": result
                }
            else:
                # Assume connected if instance exists
                return {
                    "platform": platform,
                    "connected": True,
                    "reason": "Instance initialized"
                }
        except Exception as e:
            return {
                "platform": platform,
                "connected": False,
                "reason": str(e)
            }
    
    def test_all_mcps(self) -> Dict[str, Dict[str, Any]]:
        """
        Test all configured MCPs.
        
        Returns:
            Dict mapping platform names to their status
        """
        results = {}
        for platform in self.config_store.VALID_PLATFORMS:
            results[platform] = self.get_mcp_status(platform)
        
        return results
    
    def get_available_mcps(self) -> list:
        """
        Get list of available (configured) MCPs.
        
        Returns:
            List of platform names that have configurations
        """
        return list(self.config_store.list_all_configs().keys())
    
    def close_all(self) -> None:
        """Close all MCP connections."""
        for platform, mcp in self._mcp_instances.items():
            try:
                if hasattr(mcp, 'close'):
                    mcp.close()
                logger.info(f"Closed {platform} MCP")
            except Exception as e:
                logger.error(f"Error closing {platform} MCP: {e}")
        
        self._mcp_instances.clear()
        self._initialized.clear()
    
    def __del__(self):
        """Cleanup on deletion."""
        self.close_all()
