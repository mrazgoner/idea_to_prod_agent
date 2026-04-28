"""
Jira MCP Server Configuration
Manages configurable settings for the Jira MCP server.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class JiraConfig:
    """Configuration for Jira MCP Server"""
    
    # Server identifiers
    name: str = "jira-mcp"
    version: str = "1.0.0"
    
    # Jira connection settings
    jira_base_url: Optional[str] = None
    jira_username: Optional[str] = None
    jira_api_token: Optional[str] = None
    
    # Mode configuration (stub or api)
    mode: str = "stub"  # 'stub' for testing, 'api' for real Jira
    
    # Local storage for stub mode
    storage_dir: Path = field(default_factory=lambda: Path.home() / ".idea_to_prod" / "jira")
    
    # MCP Protocol settings
    enable_logging: bool = True
    log_level: str = "INFO"
    
    # Tool configuration
    allowed_tools: list[str] = field(default_factory=lambda: [
        "create_issue",
        "get_issue",
        "update_issue",
        "list_issues",
        "search_issues",
        "add_comment",
        "get_project",
        "list_projects",
        "transition_issue",
        "get_issue_types",
    ])
    
    # Rate limiting and constraints
    max_results_per_query: int = 100
    max_comment_length: int = 32767  # Jira's limit
    
    def __post_init__(self):
        """Validate and prepare configuration after initialization"""
        # Validate mode
        if self.mode not in ("stub", "api"):
            raise ValueError(f"Mode must be 'stub' or 'api'. Got: {self.mode}")
        
        # Create storage directory if it doesn't exist
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Load from environment variables if available
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Jira connection settings
        env_url = os.getenv("JIRA_BASE_URL")
        if env_url:
            self.jira_base_url = env_url
        
        env_username = os.getenv("JIRA_USERNAME")
        if env_username:
            self.jira_username = env_username
        
        env_token = os.getenv("JIRA_API_TOKEN")
        if env_token:
            self.jira_api_token = env_token
        
        # Mode
        env_mode = os.getenv("JIRA_MCP_MODE")
        if env_mode in ("stub", "api"):
            self.mode = env_mode
        
        # Storage directory
        env_storage = os.getenv("JIRA_MCP_STORAGE_DIR")
        if env_storage:
            self.storage_dir = Path(env_storage)
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Logging
        env_logging = os.getenv("JIRA_MCP_LOGGING", "").lower()
        if env_logging in ("true", "false"):
            self.enable_logging = env_logging == "true"
        
        env_log_level = os.getenv("JIRA_MCP_LOG_LEVEL")
        if env_log_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            self.log_level = env_log_level
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "mode": self.mode,
            "jira_base_url": self.jira_base_url,
            "jira_username": self.jira_username,
            "storage_dir": str(self.storage_dir),
            "enable_logging": self.enable_logging,
            "log_level": self.log_level,
            "allowed_tools": self.allowed_tools,
            "max_results_per_query": self.max_results_per_query,
            "max_comment_length": self.max_comment_length,
        }
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "JiraConfig":
        """Create configuration from dictionary"""
        return cls(**config_dict)


def create_config(
    jira_base_url: Optional[str] = None,
    jira_username: Optional[str] = None,
    jira_api_token: Optional[str] = None,
    mode: str = "stub",
    storage_dir: Optional[str] = None,
    enable_logging: bool = True,
    log_level: str = "INFO",
) -> JiraConfig:
    """
    Factory function to create JiraConfig with custom settings
    
    Args:
        jira_base_url: Base URL of Jira instance (e.g., https://company.atlassian.net)
        jira_username: Jira username for authentication
        jira_api_token: Jira API token for authentication
        mode: Operation mode ('stub' for testing, 'api' for real Jira)
        storage_dir: Directory to store local cache/data
        enable_logging: Whether to enable logging
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        JiraConfig instance
    """
    config_kwargs = {
        "mode": mode,
        "enable_logging": enable_logging,
        "log_level": log_level,
    }
    
    if jira_base_url:
        config_kwargs["jira_base_url"] = jira_base_url
    
    if jira_username:
        config_kwargs["jira_username"] = jira_username
    
    if jira_api_token:
        config_kwargs["jira_api_token"] = jira_api_token
    
    if storage_dir:
        config_kwargs["storage_dir"] = Path(storage_dir)
    
    return JiraConfig(**config_kwargs)
