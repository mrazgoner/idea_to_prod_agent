"""MCP status panel widget"""

from PyQt6.QtWidgets import QWidget, QGridLayout, QFrame, QVBoxLayout, QLabel
from PyQt6.QtGui import QFont

from idea_to_prod.desktop_app.styles import (
    get_mcp_card_style, get_mcp_card_connected_style, get_mcp_card_disconnected_style,
    SUCCESS_TEXT, ERROR_TEXT
)


class MCPStatusPanel(QWidget):
    """Widget for displaying MCP connection status"""
    
    def __init__(self):
        super().__init__()
        self.mcp_cards = {}
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QGridLayout()
        layout.setSpacing(12)
        
        platforms = ["GitHub", "Jira", "Google Drive", "Playwright"]
        positions = [(0, 0), (0, 1), (1, 0), (1, 1)]
        
        for platform, pos in zip(platforms, positions):
            card = self.create_mcp_card(platform)
            self.mcp_cards[platform] = card
            layout.addWidget(card, pos[0], pos[1])
        
        self.setLayout(layout)
    
    def create_mcp_card(self, platform: str) -> QFrame:
        """Create an MCP status card"""
        frame = QFrame()
        frame.setStyleSheet(get_mcp_card_style())
        
        layout = QVBoxLayout()
        
        title = QLabel(platform)
        title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        status = QLabel("Checking...")
        status.setFont(QFont("Arial", 10))
        status.setObjectName(f"{platform}-status")
        
        layout.addWidget(title)
        layout.addWidget(status)
        
        frame.setLayout(layout)
        frame.setObjectName(f"{platform}-card")
        return frame
    
    def update_status(self, platform: str, connected: bool):
        """Update MCP connection status"""
        card = self.mcp_cards[platform]
        status_label = card.findChild(QLabel, f"{platform}-status")
        
        if connected:
            card.setStyleSheet(get_mcp_card_connected_style())
            status_label.setText("✓ Connected")
            status_label.setStyleSheet(f"color: {SUCCESS_TEXT};")
        else:
            card.setStyleSheet(get_mcp_card_disconnected_style())
            status_label.setText("✗ Disconnected")
            status_label.setStyleSheet(f"color: {ERROR_TEXT};")
