"""
Services Layer

Provides configuration management and MCP lifecycle services shared by
both Desktop and Web UIs.
"""

from .config_storage import ConfigStore
from .mcp_connection_service import MCPConnectionService
from .mcp_setup_service import MCPSetupService

__all__ = [
    "ConfigStore",
    "MCPConnectionService",
    "MCPSetupService",
]
