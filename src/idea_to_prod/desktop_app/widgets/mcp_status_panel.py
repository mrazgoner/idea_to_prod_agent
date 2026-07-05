"""MCP status panel widget"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont

from idea_to_prod.desktop_app.styles import SUCCESS_TEXT, ERROR_TEXT


class MCPStatusPanel(QWidget):
    """Widget for displaying MCP connection status"""
    
    def __init__(self):
        super().__init__()
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        layout.setSpacing(10)
        
        title = QLabel("MCP Status")
        title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        layout.addWidget(title)
        
        platforms = ["GitHub", "Jira", "Google Drive", "Playwright"]
        for platform in platforms:
            status_label = QLabel(f"{platform}: Checking...")
            status_label.setFont(QFont("Arial", 10))
            status_label.setObjectName(f"{platform}-status")
            layout.addWidget(status_label)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def update_status(self, platform: str, connected: bool):
        """Update MCP connection status"""
        status_label = self.findChild(QLabel, f"{platform}-status")
        if status_label:
            if connected:
                status_label.setText(f"{platform}: ✓ Connected")
                status_label.setStyleSheet(f"color: {SUCCESS_TEXT};")
            else:
                status_label.setText(f"{platform}: ✗ Disconnected")
                status_label.setStyleSheet(f"color: {ERROR_TEXT};")
