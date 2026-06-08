"""Worker thread for testing MCP connections"""

from PyQt6.QtCore import QThread, pyqtSignal
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from idea_to_prod.services.mcp_setup_service import MCPSetupService


class TestMCPWorker(QThread):
    """Worker thread for testing MCP connections asynchronously"""
    
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, mcp_setup_service: "MCPSetupService"):
        super().__init__()
        self.mcp_setup_service = mcp_setup_service
    
    def run(self):
        """Execute the MCP tests"""
        try:
            result = self.mcp_setup_service.test_all_mcps()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))
