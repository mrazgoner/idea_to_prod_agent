"""Workflow diagram widget"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QFrame, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont

from idea_to_prod.desktop_app.styles import (
    get_step_frame_style, get_step_frame_status_style,
    PRIMARY
)

# MCP emoji/icon mappings
MCP_ICONS = {
    "github": "🐙",
    "jira": "📋",
    "google_drive": "📁",
    "playwright": "🎭"
}


class WorkflowDiagram(QWidget):
    """Custom widget for displaying the processing workflow diagram"""
    
    def __init__(self):
        super().__init__()
        self.steps = [
            ("High-Level Design", "pending", []),
            ("Detailed Design", "pending", []),
            ("Code Generation", "pending", []),
            ("Test Generation", "pending", []),
            ("Test Execution", "pending", [])
        ]
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        layout.setSpacing(15)
        layout.setContentsMargins(5, 5, 5, 5)
        
        for i, (step_name, _, _) in enumerate(self.steps, 1):
            step_frame = self.create_step_frame(i, step_name)
            layout.addWidget(step_frame)
            
            if i < len(self.steps):
                arrow = QLabel("↓")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                arrow.setFont(QFont("Arial", 14, QFont.Weight.Bold))
                arrow.setStyleSheet(f"color: {PRIMARY}; margin: 5px;")
                layout.addWidget(arrow)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_step_frame(self, step_num: int, step_name: str) -> QFrame:
        """Create a single step frame"""
        frame = QFrame()
        frame.setStyleSheet(get_step_frame_style())
        
        layout = QHBoxLayout()
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(10)
        
        # Step number circle
        num_label = QLabel(str(step_num))
        num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        num_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        num_label.setStyleSheet(f"""
            background-color: {PRIMARY};
            color: white;
            border-radius: 20px;
            width: 40px;
            height: 40px;
            min-width: 40px;
            min-height: 40px;
            padding: 0px;
        """)
        
        # Step name
        name_label = QLabel(step_name)
        name_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        # Container for MCP icons
        self.mcp_icon_label = QLabel()
        self.mcp_icon_label.setFont(QFont("Arial", 16))
        self.mcp_icon_label.setObjectName(f"step-{step_num}-mcps")
        
        layout.addWidget(num_label)
        layout.addWidget(name_label)
        layout.addWidget(self.mcp_icon_label)
        layout.addStretch()
        
        frame.setLayout(layout)
        frame.setObjectName(f"step-{step_num}")
        return frame
    
    def set_step_status(self, step_num: int, status: str):
        """Update step status: pending, active, completed, failed"""
        step_name, _, mcps = self.steps[step_num - 1]
        self.steps[step_num - 1] = (step_name, status, mcps)
        
        step_frame = self.findChild(QFrame, f"step-{step_num}")
        if step_frame:
            step_frame.setStyleSheet(get_step_frame_status_style(status))
    
    def mark_mcp_access(self, step_num: int, mcp_names: list):
        """Mark MCPs accessed at this step and show their icons"""
        if step_num < 1 or step_num > len(self.steps):
            return
        
        step_name, status, _ = self.steps[step_num - 1]
        self.steps[step_num - 1] = (step_name, status, mcp_names)
        
        # Update MCP icon label
        mcp_icon_label = self.findChild(QLabel, f"step-{step_num}-mcps")
        if mcp_icon_label:
            icons = " ".join([MCP_ICONS.get(mcp.lower(), "◆") for mcp in mcp_names])
            mcp_icon_label.setText(icons if icons else "")
            mcp_icon_label.setToolTip(f"MCPs accessed: {', '.join(mcp_names)}")
    
    def reset(self):
        """Reset all steps to pending"""
        for i in range(1, 6):
            self.set_step_status(i, "pending")
            self.mark_mcp_access(i, [])
