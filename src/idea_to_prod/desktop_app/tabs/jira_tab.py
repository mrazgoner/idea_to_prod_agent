"""Jira configuration tab"""

from PyQt6.QtWidgets import QLineEdit, QCheckBox, QComboBox
from idea_to_prod.desktop_app.templates import TabTemplate


class JiraTab(TabTemplate):
    """Jira MCP configuration tab"""
    
    def __init__(self, on_save_callback=None):
        self.on_save_callback = on_save_callback
        super().__init__("Jira")
    
    def setup_layout(self):
        """Setup Jira-specific configuration fields"""
        super().setup_layout()
        
        self.mode = self.add_mode_selector()
        self.url = self.add_text_input("Instance URL:", "https://your-domain.atlassian.net")
        self.email = self.add_text_input("Email:", "your-email@example.com")
        self.token = self.add_text_input("API Token:", "Your API token", is_password=True)
        self.logging = self.add_logging_checkbox()
        
        self.save_button = self.add_save_button(on_click=self._on_save)
    
    def _on_save(self):
        """Handle save button click"""
        config = self.get_config()
        if self.on_save_callback:
            self.on_save_callback(config)
    
    def get_config(self) -> dict:
        """Get current configuration as dictionary"""
        return {
            "mode": self.mode.currentText(),
            "instance_url": self.url.text() if self.url.text() else None,
            "email": self.email.text() if self.email.text() else None,
            "api_token": self.token.text() if self.token.text() else None,
            "enable_logging": self.logging.isChecked()
        }
    
    def set_config(self, config: dict):
        """Set configuration from dictionary"""
        if "mode" in config:
            self.mode.setCurrentText(config["mode"])
        if "instance_url" in config:
            self.url.setText(config["instance_url"] or "")
        if "email" in config:
            self.email.setText(config["email"] or "")
        if "api_token" in config:
            self.token.setText(config["api_token"] or "")
        if "enable_logging" in config:
            self.logging.setChecked(config["enable_logging"])
