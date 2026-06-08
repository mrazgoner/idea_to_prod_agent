"""Playwright configuration tab"""

from PyQt6.QtWidgets import QLineEdit, QCheckBox, QComboBox
from idea_to_prod.desktop_app.templates import TabTemplate


class PlaywrightTab(TabTemplate):
    """Playwright MCP configuration tab"""
    
    def __init__(self, on_save_callback=None):
        self.on_save_callback = on_save_callback
        super().__init__("Playwright")
    
    def setup_layout(self):
        """Setup Playwright-specific configuration fields"""
        super().setup_layout()
        
        self.mode = self.add_mode_selector()
        
        self.headless = QCheckBox("Headless Mode")
        self.headless.setChecked(True)
        self.layout.addRow("", self.headless)
        
        self.timeout = self.add_text_input("Timeout (ms):", "30000")
        self.timeout.setText("30000")
        
        self.logging = self.add_logging_checkbox()
        
        self.save_button = self.add_save_button(on_click=self._on_save)
    
    def _on_save(self):
        """Handle save button click"""
        config = self.get_config()
        if self.on_save_callback:
            self.on_save_callback(config)
    
    def get_config(self) -> dict:
        """Get current configuration as dictionary"""
        try:
            timeout_val = int(self.timeout.text())
        except ValueError:
            timeout_val = 30000
        
        return {
            "mode": self.mode.currentText(),
            "headless": self.headless.isChecked(),
            "timeout": timeout_val,
            "enable_logging": self.logging.isChecked()
        }
    
    def set_config(self, config: dict):
        """Set configuration from dictionary"""
        if "mode" in config:
            self.mode.setCurrentText(config["mode"])
        if "headless" in config:
            self.headless.setChecked(config["headless"])
        if "timeout" in config:
            self.timeout.setText(str(config["timeout"]))
        if "enable_logging" in config:
            self.logging.setChecked(config["enable_logging"])
