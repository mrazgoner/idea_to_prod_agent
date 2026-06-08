"""Base template for widgets"""

from PyQt6.QtWidgets import QWidget, QVBoxLayout
from PyQt6.QtGui import QFont


class WidgetTemplate(QWidget):
    """Base template for custom widgets"""
    
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setup_ui()
    
    def setup_ui(self):
        """Override to setup widget UI"""
        self.setLayout(self.layout)
    
    def set_font(self, font_size: int, bold: bool = False, font_family: str = "Arial"):
        """Set widget font"""
        font = QFont(font_family, font_size)
        if bold:
            font.setBold(True)
        self.setFont(font)
    
    def add_to_layout(self, widget):
        """Add widget to main layout"""
        self.layout.addWidget(widget)
    
    def add_stretch(self):
        """Add stretch to layout"""
        self.layout.addStretch()
