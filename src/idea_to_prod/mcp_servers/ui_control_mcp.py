"""
UIControl MCP Tool - Enables agents to interact with the UI for Human-In-The-Loop

Provides methods for:
1. Validating MCP configurations before use
2. Requesting user input when configurations are missing (blocking)
3. Updating UI with progress/status information (non-blocking)

These become LLM-callable tools that agents invoke during execution.
"""

from typing import Dict, Any, Optional
from idea_to_prod.mcp_servers.ui_signal_bridge import UISignalBridge
from idea_to_prod.services.mcp_setup_service import MCPSetupService
from idea_to_prod.services.config_storage import ConfigStore


class UIControlMCPServer:
    """
    MCP Server for UI control and Human-In-The-Loop interaction.
    
    Public methods become LLM-callable tools that agents can invoke.
    """
    
    def __init__(self):
        """Initialize UIControl tool with access to bridge and services"""
        self.bridge = UISignalBridge()
        self.setup_service = MCPSetupService()
        self.config_store = ConfigStore()
    
    # =====================================================================
    # Tool 1: Validate MCP Configuration
    # =====================================================================
    
    def validate_mcp_config(self, mcp_name: str) -> Dict[str, Any]:
        """
        Validate if an MCP configuration exists and is properly configured.
        
        Non-blocking. Agents call this before attempting to use an MCP.
        Returns immediately with validation status.
        
        Args:
            mcp_name: Name of MCP to validate (github, jira, google_drive, playwright)
        
        Returns:
            Dict with validation result:
            {
                "configured": bool,  # Whether MCP is configured
                "status": str,       # "ready", "missing_token", "invalid", etc.
                "error": str         # Error message if any
            }
        """
        try:
            # Map MCP name to platform name
            platform_map = {
                "github": "GitHub",
                "jira": "Jira",
                "google_drive": "Google Drive",
                "playwright": "Playwright"
            }
            
            platform = platform_map.get(mcp_name.lower())
            if not platform:
                return {
                    "configured": False,
                    "status": "unknown_mcp",
                    "error": f"Unknown MCP: {mcp_name}"
                }
            
            # Check if config exists
            config = self.config_store.load_config(platform)
            if config is None:
                return {
                    "configured": False,
                    "status": "missing_config",
                    "error": f"{platform} not configured"
                }
            
            # Validate the config
            is_valid, error_msg = self.setup_service.validate_config(platform, config)
            if not is_valid:
                return {
                    "configured": False,
                    "status": "invalid_config",
                    "error": error_msg or f"{platform} configuration is invalid"
                }
            
            # Test the connection to be sure
            result = self.setup_service.test_mcp(platform, config)
            if result.get("success"):
                return {
                    "configured": True,
                    "status": "ready",
                    "error": None
                }
            else:
                return {
                    "configured": False,
                    "status": "connection_failed",
                    "error": result.get("error", "Connection test failed")
                }
        
        except Exception as e:
            return {
                "configured": False,
                "status": "error",
                "error": str(e)
            }
    
    # =====================================================================
    # Tool 2: Request User Input (BLOCKING PAUSE FOR HITL)
    # =====================================================================
    
    def request_user_input(
        self,
        step_name: str,
        required_config: str,
        message: str
    ) -> Dict[str, Any]:
        """
        **BLOCKING CALL** - Pause execution and request user configuration.
        
        Used for Human-In-The-Loop. Agents call this when they detect a missing
        MCP configuration. This method BLOCKS until the user configures the MCP
        in the UI and clicks "Continue".
        
        Args:
            step_name: Name of current step (e.g., "Code Generation")
            required_config: Name of MCP config needed (e.g., "GitHub")
            message: Message to show user (e.g., "GitHub token required to create repository")
        
        Returns:
            Dict with status and user-provided data:
            {
                "status": "provided"|"timeout"|"cancelled",
                "data": {...config data from user...},
                "resume": True|False
            }
        """
        try:
            # Extract step number from step_name for signal
            step_num = self._get_step_number(step_name)
            mcp_short = required_config.lower().replace(" ", "_")
            
            # Signal UI to pause and show config dialog
            # This emits pause_signal which main.py will handle
            self.bridge.emit_pause_signal(step_num, mcp_short)
            
            # BLOCKING WAIT for user approval
            # UI will call bridge.resume_from_pause() when user clicks Continue
            result = self.bridge.wait_for_user_approval(timeout=3600)  # 1 hour timeout
            
            return result
        
        except Exception as e:
            return {
                "status": "error",
                "data": None,
                "resume": False,
                "error": str(e)
            }
    
    # =====================================================================
    # Tool 3: Update UI Status/Progress (NON-BLOCKING)
    # =====================================================================
    
    def update_ui_status(
        self,
        step_num: int,
        message: str,
        mcp_accessed: Optional[str] = None
    ) -> Dict[str, Any]:
        """
        Non-blocking signal to update UI logger and diagram.
        
        Agents call this after significant steps to provide real-time progress
        feedback to the user and mark MCP access in the diagram.
        
        Args:
            step_num: Current step number (1-5)
            message: Status message to log
            mcp_accessed: (Optional) MCP name that was just accessed (github, jira, etc.)
        
        Returns:
            {"status": "logged"}
        """
        try:
            # Emit progress to logger
            self.bridge.emit_progress_signal(step_num, message)
            
            # If an MCP was accessed, mark it on diagram
            if mcp_accessed:
                mcp_list = [mcp_accessed.lower()]
                self.bridge.emit_mcp_access_signal(step_num, mcp_list)
            
            return {"status": "logged"}
        
        except Exception as e:
            return {
                "status": "error",
                "error": str(e)
            }
    
    # =====================================================================
    # Helper Methods
    # =====================================================================
    
    def _get_step_number(self, step_name: str) -> int:
        """Map step name to step number (1-5)"""
        steps = {
            "high-level design": 1,
            "detailed design": 2,
            "code generation": 3,
            "test generation": 4,
            "test execution": 5
        }
        return steps.get(step_name.lower(), 1)
