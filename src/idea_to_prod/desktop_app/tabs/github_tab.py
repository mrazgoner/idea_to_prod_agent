"""GitHub configuration tab"""

from PyQt6.QtWidgets import QComboBox, QLineEdit, QCheckBox
from idea_to_prod.desktop_app.templates import TabTemplate


class GitHubTab(TabTemplate):
    """GitHub MCP configuration tab"""
    
    def __init__(self, on_save_callback=None):
        self.on_save_callback = on_save_callback
        super().__init__("GitHub")
    
    def setup_layout(self):
        """Setup GitHub-specific configuration fields"""
        super().setup_layout()
        
        self.mode = self.add_mode_selector()
        self.token = self.add_text_input("Personal Access Token:", "ghp_xxxxxxxxxxxxxxxxxxxx", is_password=True)
        self.username = self.add_text_input("Username:", "Your GitHub username")
        self.url = self.add_text_input("Base URL:", "https://api.github.com")
        self.url.setText("https://api.github.com")
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
            "token": self.token.text() if self.token.text() else None,
            "username": self.username.text() if self.username.text() else None,
            "base_url": self.url.text(),
            "enable_logging": self.logging.isChecked()
        }
    
    def set_config(self, config: dict):
        """Set configuration from dictionary"""
        if "mode" in config:
            self.mode.setCurrentText(config["mode"])
        if "token" in config:
            self.token.setText(config["token"] or "")
        if "username" in config:
            self.username.setText(config["username"] or "")
        if "base_url" in config:
            self.url.setText(config["base_url"])
        if "enable_logging" in config:
            self.logging.setChecked(config["enable_logging"])
