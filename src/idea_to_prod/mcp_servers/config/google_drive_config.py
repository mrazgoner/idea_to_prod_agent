"""
Google Drive MCP Server Configuration
Manages configurable settings for the Google Drive MCP server.
Supports both 'file' mode for local storage and 'api' mode for real Google Drive integration.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class GoogleDriveConfig:
    """Configuration for Google Drive MCP Server"""
    
    # Server identifiers
    name: str = "google-drive-mcp"
    version: str = "1.0.0"
    
    # Mode configuration (file or api)
    mode: str = "file"  # 'file' for local storage, 'api' for real Google Drive
    
    # File storage settings
    storage_dir: Path = field(default_factory=lambda: Path.home() / ".idea_to_prod" / "google_drive")
    
    # Google Drive connection settings
    google_credentials_path: Optional[str] = None
    google_project_id: Optional[str] = None
    
    # MCP Protocol settings
    enable_logging: bool = True
    log_level: str = "INFO"
    
    # Tool configuration
    allowed_tools: list[str] = field(default_factory=lambda: [
        "save_document",
        "read_document",
        "list_files",
        "delete_file",
        "create_folder",
        "get_file_metadata",
    ])
    
    # Rate limiting and constraints
    max_file_size_mb: int = 100
    max_files_per_operation: int = 50
    
    def __post_init__(self):
        """Validate and prepare configuration after initialization"""
        # Validate mode
        if self.mode not in ("file", "api"):
            raise ValueError(f"Mode must be 'file' or 'api'. Got: {self.mode}")
        
        # Create storage directory if it doesn't exist (for file mode)
        if self.mode == "file":
            self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        # Load from environment variables if available
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        env_storage = os.getenv("GDRIVE_MCP_STORAGE_DIR")
        if env_storage:
            self.storage_dir = Path(env_storage)
            if self.mode == "file":
                self.storage_dir.mkdir(parents=True, exist_ok=True)
        
        env_mode = os.getenv("GDRIVE_MCP_MODE")
        if env_mode in ("file", "api"):
            self.mode = env_mode
        
        env_creds = os.getenv("GOOGLE_CREDENTIALS_PATH")
        if env_creds:
            self.google_credentials_path = env_creds
        
        env_project = os.getenv("GOOGLE_PROJECT_ID")
        if env_project:
            self.google_project_id = env_project
        
        env_logging = os.getenv("GDRIVE_MCP_LOGGING", "").lower()
        if env_logging in ("true", "false"):
            self.enable_logging = env_logging == "true"
        
        env_log_level = os.getenv("GDRIVE_MCP_LOG_LEVEL")
        if env_log_level in ("DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"):
            self.log_level = env_log_level
    
    def to_dict(self) -> dict:
        """Convert configuration to dictionary"""
        return {
            "name": self.name,
            "version": self.version,
            "mode": self.mode,
            "storage_dir": str(self.storage_dir),
            "google_credentials_path": self.google_credentials_path,
            "google_project_id": self.google_project_id,
            "enable_logging": self.enable_logging,
            "log_level": self.log_level,
            "allowed_tools": self.allowed_tools,
            "max_file_size_mb": self.max_file_size_mb,
            "max_files_per_operation": self.max_files_per_operation,
        }
    
    @classmethod
    def from_dict(cls, config_dict: dict) -> "GoogleDriveConfig":
        """Create configuration from dictionary"""
        return cls(**config_dict)


def create_config(
    storage_dir: Optional[str] = None,
    mode: str = "file",
    enable_logging: bool = True,
    log_level: str = "INFO",
) -> GoogleDriveConfig:
    """
    Factory function to create GoogleDriveConfig with custom settings
    
    Args:
        storage_dir: Directory to store files locally
        mode: Operation mode (only 'file' supported)
        enable_logging: Whether to enable logging
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
    
    Returns:
        GoogleDriveConfig instance
    """
    config_kwargs = {
        "mode": mode,
        "enable_logging": enable_logging,
        "log_level": log_level,
    }
    
    if storage_dir:
        config_kwargs["storage_dir"] = Path(storage_dir)
    
    return GoogleDriveConfig(**config_kwargs)
