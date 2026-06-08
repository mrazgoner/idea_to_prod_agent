"""Base template for configuration tabs"""

from PyQt6.QtWidgets import QWidget, QFormLayout, QPushButton, QLineEdit, QComboBox, QCheckBox
from PyQt6.QtGui import QFont

from idea_to_prod.desktop_app.styles import get_primary_button_style


class TabTemplate(QWidget):
    """Base template for MCP configuration tabs"""
    
    def __init__(self, tab_name: str):
        super().__init__()
        self.tab_name = tab_name
        self.layout = QFormLayout()
        self.setup_layout()
    
    def setup_layout(self):
        """Setup the tab layout"""
        self.setLayout(self.layout)
    
    def add_mode_selector(self) -> QComboBox:
        """Add mode selector (stub/real)"""
        mode = QComboBox()
        mode.addItems(["stub", "real"])
        self.layout.addRow("Mode:", mode)
        return mode
    
    def add_text_input(self, label: str, placeholder: str = "", is_password: bool = False) -> QLineEdit:
        """Add text input field"""
        input_field = QLineEdit()
        input_field.setPlaceholderText(placeholder)
        if is_password:
            input_field.setEchoMode(QLineEdit.EchoMode.Password)
        self.layout.addRow(label, input_field)
        return input_field
    
    def add_logging_checkbox(self) -> QCheckBox:
        """Add logging enable checkbox"""
        logging_checkbox = QCheckBox("Enable Logging")
        self.layout.addRow("", logging_checkbox)
        return logging_checkbox
    
    def add_save_button(self, label: str = "", on_click=None) -> QPushButton:
        """Add save button"""
        button_text = label or f"Save & Test {self.tab_name} Config"
        save_button = QPushButton(button_text)
        save_button.setStyleSheet(get_primary_button_style())
        
        if on_click:
            save_button.clicked.connect(on_click)
        
        self.layout.addRow("", save_button)
        return save_button
    
    def get_layout(self) -> QFormLayout:
        """Get the form layout"""
        return self.layout
