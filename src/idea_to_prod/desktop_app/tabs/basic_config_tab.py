"""Basic configuration tab for models and API tokens"""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel, QLineEdit,
    QComboBox, QPushButton, QGroupBox, QFormLayout
)
from PyQt6.QtGui import QFont


class BasicConfigTab(QWidget):
    """Basic configuration tab for models and tokens"""
    
    def __init__(self, on_save_callback=None):
        super().__init__()
        self.on_save_callback = on_save_callback
        self.init_ui()
    
    def init_ui(self):
        """Initialize the UI"""
        layout = QVBoxLayout()
        
        # Model Selection Group
        model_group = QGroupBox("Model Selection")
        model_layout = QFormLayout()
        
        # Agent 1: High-Level Design
        model_layout.addRow(QLabel("Agent 1 (High-Level Design):"), self._create_model_combo("Agent 1"))
        
        # Agent 2: Detailed Design
        model_layout.addRow(QLabel("Agent 2 (Detailed Design):"), self._create_model_combo("Agent 2"))
        
        # Agent 3: Code Generation
        model_layout.addRow(QLabel("Agent 3 (Code Generation):"), self._create_model_combo("Agent 3"))
        
        # Agent 4: Test Generation
        model_layout.addRow(QLabel("Agent 4 (Test Generation):"), self._create_model_combo("Agent 4"))
        
        # Agent 5: Test Execution
        model_layout.addRow(QLabel("Agent 5 (Test Execution):"), self._create_model_combo("Agent 5"))
        
        model_group.setLayout(model_layout)
        layout.addWidget(model_group)
        
        # API Tokens Group
        tokens_group = QGroupBox("API Tokens")
        tokens_layout = QFormLayout()
        
        # OpenAI Token
        self.openai_token = QLineEdit()
        self.openai_token.setEchoMode(QLineEdit.EchoMode.Password)
        self.openai_token.setPlaceholderText("sk-...")
        tokens_layout.addRow(QLabel("OpenAI API Key:"), self.openai_token)
        
        # Anthropic Token
        self.anthropic_token = QLineEdit()
        self.anthropic_token.setEchoMode(QLineEdit.EchoMode.Password)
        self.anthropic_token.setPlaceholderText("sk-ant-...")
        tokens_layout.addRow(QLabel("Anthropic API Key:"), self.anthropic_token)
        
        tokens_group.setLayout(tokens_layout)
        layout.addWidget(tokens_group)
        
        # Save Button
        save_button = QPushButton("Save Configuration")
        save_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        save_button.clicked.connect(self._on_save)
        layout.addWidget(save_button)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def _create_model_combo(self, agent_name: str) -> QComboBox:
        """Create a model selection combo box"""
        combo = QComboBox()
        combo.addItems([
            "gpt-4",
            "gpt-4-turbo",
            "gpt-3.5-turbo",
            "claude-3-5-sonnet-20241022",
            "claude-3-opus-20240229"
        ])
        combo.setObjectName(f"model_{agent_name.replace(' ', '_')}")
        return combo
    
    def _on_save(self):
        """Handle save button click"""
        config = {
            "openai_token": self.openai_token.text(),
            "anthropic_token": self.anthropic_token.text()
        }
        
        if self.on_save_callback:
            self.on_save_callback(config)
