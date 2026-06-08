"""
UI Signal Bridge - Bidirectional communication between MCP tools and the PyQt6 UI

This module provides a singleton bridge that enables MCP tools to:
1. Emit signals to the UI (pause, progress, diagram updates)
2. Wait for user input/approval (blocking call with threading events)
3. Resume after user interaction
"""

import threading
from typing import Dict, Any, Optional
from PyQt6.QtCore import QObject, pyqtSignal


class UISignalBridge(QObject):
    """
    Singleton bridge for MCP tool ↔ UI communication.
    
    Enables:
    - MCP tools to emit signals to UI
    - MCP tools to pause and wait for user approval
    - UI to signal completion of user actions back to waiting MCP tools
    """
    
    # Signals emitted to UI
    pause_signal = pyqtSignal(int, str)  # (step_num, mcp_name)
    progress_signal = pyqtSignal(int, str)  # (step_num, message)
    mcp_access_signal = pyqtSignal(int, list)  # (step_num, mcp_list)
    
    # Class variable to hold singleton instance
    _instance = None
    _lock = threading.Lock()
    
    def __new__(cls):
        """Ensure singleton pattern"""
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
                    cls._instance._initialized = False
        return cls._instance
    
    def __init__(self):
        """Initialize the bridge (only on first call)"""
        if self._initialized:
            return
        
        super().__init__()
        
        # Thread synchronization for pause/resume
        self._pause_event = threading.Event()  # Signals user approved
        self._pause_event.set()  # Start as "set" (not paused)
        
        self._user_approval_data = None  # Data from user input
        self._approval_lock = threading.Lock()
        
        self._initialized = True
    
    def emit_pause_signal(self, step_num: int, mcp_name: str) -> None:
        """
        Emit signal to UI that process is paused at a step due to missing MCP config.
        
        Args:
            step_num: Current step number (1-5)
            mcp_name: Name of the MCP that needs configuration (github, jira, etc.)
        """
        self.pause_signal.emit(step_num, mcp_name)
    
    def emit_progress_signal(self, step_num: int, message: str) -> None:
        """
        Emit signal to UI with progress update (non-blocking).
        
        Args:
            step_num: Current step number
            message: Progress message to log
        """
        self.progress_signal.emit(step_num, message)
    
    def emit_mcp_access_signal(self, step_num: int, mcp_list: list) -> None:
        """
        Emit signal to UI to mark MCPs accessed at this step in diagram.
        
        Args:
            step_num: Step number where MCPs are accessed
            mcp_list: List of MCP names (e.g., ["github", "jira"])
        """
        self.mcp_access_signal.emit(step_num, mcp_list)
    
    def wait_for_user_approval(self, timeout: int = 3600) -> Dict[str, Any]:
        """
        **BLOCKING CALL** - Pause execution and wait for user approval.
        
        Used by `request_user_input()` tool to pause agent execution until user
        configures the missing MCP and clicks "Continue" in the UI.
        
        Args:
            timeout: Maximum seconds to wait for approval (default: 1 hour)
        
        Returns:
            Dict with approval data or timeout/cancel status
        """
        # Clear event (set to "wait" state)
        self._pause_event.clear()
        
        try:
            # Block until UI signals approval (or timeout)
            is_approved = self._pause_event.wait(timeout=timeout)
            
            with self._approval_lock:
                if is_approved:
                    # User approved - return their input data
                    return {
                        "status": "provided",
                        "data": self._user_approval_data or {},
                        "resume": True
                    }
                else:
                    # Timeout
                    return {
                        "status": "timeout",
                        "data": None,
                        "resume": False
                    }
        finally:
            # Always set event back (resume state)
            self._pause_event.set()
    
    def resume_from_pause(self, approval_data: Optional[Dict[str, Any]] = None) -> None:
        """
        Called by UI when user clicks "Continue" to resume paused execution.
        
        Signals the waiting `request_user_input()` tool that user has finished
        configuring the MCP and execution should resume.
        
        Args:
            approval_data: Data from user input (e.g., {"github_token": "..."})
        """
        with self._approval_lock:
            self._user_approval_data = approval_data or {}
        
        # Signal the waiting thread
        self._pause_event.set()
