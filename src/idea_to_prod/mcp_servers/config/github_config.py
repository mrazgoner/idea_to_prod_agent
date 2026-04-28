"""
GitHub MCP Server Configuration
Manages configurable settings for the GitHub MCP server.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class GitHubConfig:
    """Configuration for GitHub MCP Server"""
    
    # Server identifiers
    name: str = "github-mcp"
    version: str = "1.0.0"
    
    # GitHub connection settings
    github_api_url: str = "https://api.github.com"
    github_token: Optional[str] = None
    github_username: Optional[str] = None
    github_owner: Optional[str] = None  # Default owner for operations
    
    # Mode configuration (stub or api)
    mode: str = "stub"  # 'stub' for testing, 'api' for real GitHub API
    
    # Local storage for stub mode
    storage_dir: Path = field(default_factory=lambda: Path.home() / ".idea_to_prod" / "github")
    
    # MCP Protocol settings
    enable_logging: bool = True
    log_level: str = "INFO"
    
    # Tool configuration
    allowed_tools: list[str] = field(default_factory=lambda: [
        "create_repository",
        "get_repository",
        "list_repositories",
        "create_issue",
        "get_issue",
        "list_issues",
        "update_issue",
        "create_pull_request",
        "get_pull_request",
        "list_pull_requests",
        "add_comment",
        "list_branches",
        "create_branch",
        "get_user",
        "search_repositories",
        "add_collaborator",
    ])
    
    # Rate limiting and constraints
    max_results_per_query: int = 100
    max_comment_length: int = 65536  # GitHub's limit
    max_repositories_per_query: int = 100
    timeout_seconds: int = 30
    
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
        # GitHub connection settings
        env_token = os.getenv("GITHUB_TOKEN")
        if env_token:
            self.github_token = env_token
        
        env_username = os.getenv("GITHUB_USERNAME")
        if env_username:
            self.github_username = env_username
        
        env_owner = os.getenv("GITHUB_OWNER")
        if env_owner:
            self.github_owner = env_owner
        
        env_api_url = os.getenv("GITHUB_API_URL")
        if env_api_url:
            self.github_api_url = env_api_url
        
        # Mode
        env_mode = os.getenv("GITHUB_MCP_MODE")
        if env_mode in ("stub", "api"):
            self.mode = env_mode
        
        # Storage directory
        env_storage = os.getenv("GITHUB_MCP_STORAGE_DIR")
        if env_storage:
            self.storage_dir = Path(env_storage)
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Logging
        env_logging = os.getenv("GITHUB_MCP_LOGGING", "").lower()
        if env_logging in ("true", "false"):
            self.enable_logging = env_logging == "true"
        
        env_log_level = os.getenv("GITHUB_MCP_LOG_LEVEL")
        if env_log_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            self.log_level = env_log_level
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "mode": self.mode,
            "github_api_url": self.github_api_url,
            "github_username": self.github_username,
            "github_owner": self.github_owner,
            "storage_dir": str(self.storage_dir),
            "enable_logging": self.enable_logging,
            "log_level": self.log_level,
            "allowed_tools": self.allowed_tools,
            "max_results_per_query": self.max_results_per_query,
            "max_comment_length": self.max_comment_length,
            "timeout_seconds": self.timeout_seconds,
        }


def create_config(
    mode: str = "stub",
    github_token: Optional[str] = None,
    github_username: Optional[str] = None,
    github_owner: Optional[str] = None,
    storage_dir: Optional[Path] = None,
    enable_logging: bool = True,
    log_level: str = "INFO",
) -> GitHubConfig:
    """
    Create a GitHub MCP Server configuration
    
    Args:
        mode: 'stub' for testing, 'api' for real GitHub API
        github_token: GitHub API token for authentication
        github_username: GitHub username (for API mode)
        github_owner: Default GitHub owner/organization
        storage_dir: Directory for storing files in stub mode
        enable_logging: Enable logging output
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        GitHubConfig instance
    """
    config = GitHubConfig(
        mode=mode,
        github_token=github_token,
        github_username=github_username,
        github_owner=github_owner,
        enable_logging=enable_logging,
        log_level=log_level,
    )
    
    if storage_dir:
        config.storage_dir = storage_dir
        config.storage_dir.mkdir(parents=True, exist_ok=True)
    
    return config
