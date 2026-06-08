"""Google Drive configuration tab"""

from PyQt6.QtWidgets import QLineEdit, QCheckBox, QComboBox
from idea_to_prod.desktop_app.templates import TabTemplate


class GoogleDriveTab(TabTemplate):
    """Google Drive MCP configuration tab"""
    
    def __init__(self, on_save_callback=None):
        self.on_save_callback = on_save_callback
        super().__init__("Google Drive")
    
    def setup_layout(self):
        """Setup Google Drive-specific configuration fields"""
        super().setup_layout()
        
        self.mode = self.add_mode_selector()
        self.creds = self.add_text_input("Credentials Path:", "/path/to/credentials.json")
        self.folder = self.add_text_input("Folder ID:", "Google Drive folder ID")
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
            "credentials_path": self.creds.text() if self.creds.text() else None,
            "folder_id": self.folder.text() if self.folder.text() else None,
            "enable_logging": self.logging.isChecked()
        }
    
    def set_config(self, config: dict):
        """Set configuration from dictionary"""
        if "mode" in config:
            self.mode.setCurrentText(config["mode"])
        if "credentials_path" in config:
            self.creds.setText(config["credentials_path"] or "")
        if "folder_id" in config:
            self.folder.setText(config["folder_id"] or "")
        if "enable_logging" in config:
            self.logging.setChecked(config["enable_logging"])
