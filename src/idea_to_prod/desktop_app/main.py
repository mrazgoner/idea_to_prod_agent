"""Main application window"""

import logging
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QTabWidget, QGroupBox,
    QMessageBox, QSplitter, QFrame
)
from PyQt6.QtCore import Qt, QTimer, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap, QColor, QPainter

from idea_to_prod.agents.team import IdeaToProdTeam
from idea_to_prod.services.mcp_setup_service import MCPSetupService
from idea_to_prod.services.mcp_connection_service import MCPConnectionService
from idea_to_prod.mcp_servers.ui_signal_bridge import UISignalBridge

from idea_to_prod.desktop_app.workers import ProcessIdeaWorker, TestMCPWorker
from idea_to_prod.desktop_app.tabs import GitHubTab, JiraTab, GoogleDriveTab, PlaywrightTab
from idea_to_prod.desktop_app.styles import (
    get_primary_button_style, get_success_button_style, get_error_button_style,
    get_success_status_style, get_error_status_style,
    get_warning_status_style, get_info_status_style
)

logger = logging.getLogger(__name__)


class IdeaToProdApp(QMainWindow):
    """Main application window for Idea-To-Prod Agent Team"""
    
    def __init__(self):
        super().__init__()
        self.team = IdeaToProdTeam()
        self.mcp_setup_service = MCPSetupService()
        self.ui_bridge = UISignalBridge()  # Initialize UI signal bridge
        
        self.process_worker = None
        self.mcp_worker = None
        
        # Pause/resume state
        self.paused_step = None
        self.paused_mcp = None
        
        self.init_ui()
        
        # Connect UI bridge signals to handler slots
        self.ui_bridge.pause_signal.connect(self.on_ui_pause_requested)
        self.ui_bridge.progress_signal.connect(self.on_ui_progress)
        self.ui_bridge.mcp_access_signal.connect(self.on_mcp_accessed)
        
        self.setWindowTitle("Idea-To-Prod Agent Team")
        self.setGeometry(100, 100, 1200, 800)
    
    def init_ui(self):
        """Initialize the user interface with vertical layout"""
        # Create main widget            
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout - VERTICAL instead of horizontal
        main_layout = QVBoxLayout()
        main_layout.setContentsMargins(10, 10, 10, 10)
        main_layout.setSpacing(10)
        
        # 1. TOP: Collapsible configuration section
        config_section = self.create_collapsible_config()
        main_layout.addWidget(config_section)
        
        # 2. MAIN: Input area (takes ~70% of remaining space)
        input_section = self.create_input_section()
        main_layout.addWidget(input_section, 3)  # Stretch factor 3
        
        # 3. BOTTOM: Expandable logger (takes ~30% of remaining space)
        logger_section = self.create_logger_section()
        main_layout.addWidget(logger_section, 1)  # Stretch factor 1
        
        main_widget.setLayout(main_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Test MCPs on startup
        QTimer.singleShot(500, self.test_mcp_connections)
    
    def create_collapsible_config(self) -> QGroupBox:
        """Create collapsible configuration section (MCP Status + Config Tabs)"""
        config_group = QGroupBox("MCP Configuration")
        config_group.setCheckable(True)
        config_group.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        
        config_layout = QVBoxLayout()
        
        # Configuration tabs
        self.tabs = QTabWidget()
        self.github_tab = GitHubTab(on_save_callback=self._on_github_config_save)
        self.jira_tab = JiraTab(on_save_callback=self._on_jira_config_save)
        self.gdrive_tab = GoogleDriveTab(on_save_callback=self._on_gdrive_config_save)
        self.playwright_tab = PlaywrightTab(on_save_callback=self._on_playwright_config_save)
        
        self.tabs.addTab(self.github_tab, "GitHub")
        self.tabs.addTab(self.jira_tab, "Jira")
        self.tabs.addTab(self.gdrive_tab, "Google Drive")
        self.tabs.addTab(self.playwright_tab, "Playwright")
        
        # Set compact height when collapsed
        self.tabs.setMaximumHeight(35)  # Just tab bar
        
        config_layout.addWidget(self.tabs)
        config_group.setLayout(config_layout)
        
        # Now set checked to False and ensure tabs stay enabled
        config_group.setChecked(False)  # Starts collapsed
        self.tabs.setEnabled(True)  # Force enabled after groupbox is set
        
        # When tab is clicked, auto-expand the config group
        self.tabs.tabBarClicked.connect(lambda idx: config_group.setChecked(True))
        
        # Store reference for later access
        self.config_group = config_group
        
        # Connect checkbox toggle to expand/collapse
        config_group.toggled.connect(lambda checked: self.on_config_toggle(checked))
        
        # Ensure tabs stay enabled even after all connections
        QTimer.singleShot(0, lambda: self.tabs.setEnabled(True))
        
        return config_group
    
    def on_config_toggle(self, checked: bool):
        """Handle config group toggle to expand/collapse"""
        # Always keep tabs enabled (never disabled)
        self.tabs.setEnabled(True)
        
        if checked:
            self.tabs.setMaximumHeight(16777215)  # QWIDGETSIZE_MAX - no limit
        else:
            self.tabs.setMaximumHeight(35)  # Compact - just tab bar
    
    def create_input_section(self) -> QWidget:
        """Create input section (idea input + buttons)"""
        input_widget = QFrame()
        input_layout = QVBoxLayout()
        
        # Idea input label
        idea_label = QLabel("Application Idea")
        idea_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        # Idea input text area (takes most space)
        self.idea_input = QTextEdit()
        self.idea_input.setPlaceholderText(
            "Describe your application idea here...\n\n"
            "Example: A real-time collaboration tool for remote teams with chat, "
            "file sharing, and video conferencing"
        )
        self.idea_input.setMinimumHeight(200)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.process_button = QPushButton("Process Idea")
        self.process_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.process_button.setStyleSheet(get_primary_button_style())
        self.process_button.clicked.connect(self.process_idea)
        
        self.test_button = QPushButton("Test MCPs")
        self.test_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.test_button.setStyleSheet(get_success_button_style())
        self.test_button.clicked.connect(self.test_mcp_connections)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.reset_button.setStyleSheet(get_error_button_style())
        self.reset_button.clicked.connect(self.reset_form)
        
        self.continue_button = QPushButton("Configure & Continue")
        self.continue_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.continue_button.setStyleSheet(get_success_button_style())
        self.continue_button.clicked.connect(self.on_continue_clicked)
        self.continue_button.hide()  # Only visible when paused
        
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.test_button)
        button_layout.addWidget(self.reset_button)
        button_layout.addWidget(self.continue_button)
        button_layout.addStretch()
        
        input_layout.addWidget(idea_label)
        input_layout.addWidget(self.idea_input)
        input_layout.addLayout(button_layout)
        input_layout.setContentsMargins(0, 0, 0, 0)
        input_layout.setSpacing(5)
        
        input_widget.setLayout(input_layout)
        return input_widget
    
    def create_logger_section(self) -> QWidget:
        """Create logger section (expandable, collapsible)"""
        logger_widget = QFrame()
        logger_layout = QVBoxLayout()
        
        # Logger header with label and expand button
        logger_header_layout = QHBoxLayout()
        
        logger_label = QLabel("Execution Log")
        logger_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        self.expand_logger_button = QPushButton("Expand")
        self.expand_logger_button.setMaximumWidth(100)
        self.expand_logger_button.setFont(QFont("Arial", 9))
        self.expand_logger_button.setCheckable(True)
        self.expand_logger_button.toggled.connect(self.on_logger_expand_toggle)
        
        self.clear_logger_button = QPushButton("Clear")
        self.clear_logger_button.setMaximumWidth(100)
        self.clear_logger_button.setFont(QFont("Arial", 9))
        self.clear_logger_button.clicked.connect(self.clear_logger)
        
        logger_header_layout.addWidget(logger_label)
        logger_header_layout.addStretch()
        logger_header_layout.addWidget(self.expand_logger_button)
        logger_header_layout.addWidget(self.clear_logger_button)
        
        # Logger text area (read-only)
        self.logger_output = QTextEdit()
        self.logger_output.setReadOnly(True)
        self.logger_output.setMaximumHeight(100)
        self.logger_output.setFont(QFont("Courier", 9))
        
        logger_layout.addLayout(logger_header_layout)
        logger_layout.addWidget(self.logger_output)
        logger_layout.setContentsMargins(0, 0, 0, 0)
        logger_layout.setSpacing(5)
        
        logger_widget.setLayout(logger_layout)
        return logger_widget
    
    def on_logger_expand_toggle(self, checked: bool):
        """Handle logger expand/collapse toggle"""
        if checked:
            self.logger_output.setMaximumHeight(300)  # Expanded
            self.expand_logger_button.setText("Collapse")
        else:
            self.logger_output.setMaximumHeight(100)  # Compact
            self.expand_logger_button.setText("Expand")
    
    def clear_logger(self):
        """Clear logger output"""
        self.logger_output.clear()
    
    def append_log(self, message: str):
        """Append message to logger"""
        self.logger_output.append(message)
    
    def _on_github_config_save(self, config: dict):
        """Handle GitHub configuration save"""
        self._save_and_test_mcp_config("GitHub", config)
    
    def _on_jira_config_save(self, config: dict):
        """Handle Jira configuration save"""
        self._save_and_test_mcp_config("Jira", config)
    
    def _on_gdrive_config_save(self, config: dict):
        """Handle Google Drive configuration save"""
        self._save_and_test_mcp_config("Google Drive", config)
    
    def _on_playwright_config_save(self, config: dict):
        """Handle Playwright configuration save"""
        self._save_and_test_mcp_config("Playwright", config)
    
    def _save_and_test_mcp_config(self, platform: str, config: dict):
        """Save and test MCP configuration"""
        is_valid, error_msg = self.mcp_setup_service.validate_config(platform, config)
        if not is_valid:
            self.show_status(f"{platform} config invalid: {error_msg}", "error")
            return
        
        success, msg = self.mcp_setup_service.save_config(platform, config)
        if success:
            self.show_status(f"Testing {platform} MCP...", "info")
            result = self.mcp_setup_service.test_mcp(platform, config)
            if result.get("success"):
                self.show_status(f"✓ {platform} config saved and tested successfully!", "success")
                self.update_tab_status(platform, True)
            else:
                self.show_status(f"{platform} config saved but test failed: {result.get('error')}", "warning")
                self.update_tab_status(platform, False)
        else:
            self.show_status(f"Failed to save {platform} config: {msg}", "error")
    
    def process_idea(self):
        """Process the application idea"""
        idea = self.idea_input.toPlainText().strip()
        
        if not idea:
            self.show_status("Please enter an application idea", "error")
            return
        
        self.show_status("Processing idea... Please wait", "info")
        self.process_button.setEnabled(False)
        self.test_button.setEnabled(False)
        self.reset_button.setEnabled(False)
        
        self.process_worker = ProcessIdeaWorker(self.team, idea)
        self.process_worker.finished.connect(self.on_process_finished)
        self.process_worker.error.connect(self.on_process_error)
        self.process_worker.progress.connect(self.on_process_progress)
        self.process_worker.start()
    
    def on_process_progress(self, message: str, step: int):
        """Update progress during processing"""
        self.statusBar().showMessage(f"[Step {step}] {message}")
    
    def on_process_finished(self, result: dict):
        """Handle process completion"""
        self.show_status("Idea processed successfully!", "success")
        self.statusBar().showMessage("Ready")
        self.process_button.setEnabled(True)
        self.test_button.setEnabled(True)
        self.reset_button.setEnabled(True)
    
    def on_process_error(self, error: str):
        """Handle process error"""
        self.show_status(f"Error: {error}", "error")
        self.statusBar().showMessage("Error")
        self.process_button.setEnabled(True)
        self.test_button.setEnabled(True)
        self.reset_button.setEnabled(True)
    
    def test_mcp_connections(self):
        """Test all MCP connections"""
        self.show_status("Testing MCP connections...", "info")
        self.test_button.setEnabled(False)
        
        self.mcp_worker = TestMCPWorker(self.mcp_setup_service)
        self.mcp_worker.finished.connect(self.on_mcp_test_finished)
        self.mcp_worker.error.connect(self.on_mcp_test_error)
        self.mcp_worker.start()
    
    def on_mcp_test_finished(self, result: dict):
        """Handle MCP test completion"""
        self.test_button.setEnabled(True)
        
        # Check if any tests passed
        passed = sum(1 for r in result.values() if isinstance(r, dict) and r.get("success"))
        total = len(result)
        
        if passed == total:
            self.show_status(f"✓ All {total} MCPs tested successfully!", "success")
        elif passed > 0:
            self.show_status(f"Partial success: {passed}/{total} MCPs connected", "warning")
        else:
            self.show_status("No MCPs configured yet. Configure them in the tabs above.", "warning")
        
        # Update tab statuses
        for platform, platform_result in result.items():
            if isinstance(platform_result, dict):
                connected = platform_result.get("success", False)
                self.update_tab_status(platform, connected)
    
    def on_mcp_test_error(self, error: str):
        """Handle MCP test error"""
        self.show_status(f"MCP test error: {error}", "error")
        self.test_button.setEnabled(True)
    
    def reset_form(self):
        """Reset the form"""
        self.idea_input.clear()
        self.statusBar().showMessage("Ready")
    
    def show_status(self, message: str, status_type: str = "info"):
        """Show status message in logger and status bar"""
        # Append to logger with status type indicator
        status_prefix = {
            "success": "✓",
            "error": "✗",
            "warning": "⚠",
            "info": "ℹ"
        }.get(status_type, "•")
        
        self.append_log(f"{status_prefix} {message}")
        
        # Also update status bar
        self.statusBar().showMessage(message)
    
    def update_tab_status(self, platform: str, connected: bool):
        """Update tab button with colored status icon"""
        tab_index_map = {
            "GitHub": 0,
            "Jira": 1,
            "Google Drive": 2,
            "Playwright": 3
        }
        
        if platform in tab_index_map:
            idx = tab_index_map[platform]
            
            # Create colored icon pixmap
            pixmap = QPixmap(16, 16)
            pixmap.fill(QColor(0, 0, 0, 0))  # Transparent
            
            painter = QPainter(pixmap)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)
            
            # Draw colored icon
            if connected:
                painter.setPen(QColor("#4CAF50"))  # Green
                painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            else:
                painter.setPen(QColor("#f44336"))  # Red
                painter.setFont(QFont("Arial", 10, QFont.Weight.Bold))
            
            painter.drawText(pixmap.rect(), Qt.AlignmentFlag.AlignCenter, "●")
            painter.end()
            
            # Set icon and text
            icon = QIcon(pixmap)
            self.tabs.setTabIcon(idx, icon)
            self.tabs.setTabText(idx, platform)
    
    # =====================================================================
    # UI Bridge Signal Handlers (Human-In-The-Loop)
    # =====================================================================
    
    def on_ui_pause_requested(self, step_num: int, mcp_name: str):
        """
        Handle pause signal from UIControl tool.
        Called when process encounters missing MCP configuration.
        """
        self.paused_step = step_num
        self.paused_mcp = mcp_name
        
        # Show status message
        self.show_status(f"⏸️ Process paused at Step {step_num} - {mcp_name.upper()} configuration required", "warning")
        
        # Map MCP name to tab index
        mcp_to_tab = {
            "github": 0,
            "jira": 1,
            "google_drive": 2,
            "playwright": 3
        }
        
        tab_index = mcp_to_tab.get(mcp_name.lower(), 0)
        
        # Expand the config group if it exists
        # (find first QGroupBox in the layout)
        
        # Switch to the appropriate tab
        if self.tabs:
            self.tabs.setCurrentIndex(tab_index)
        
        # Show the Continue button
        self.continue_button.show()
        
        # Show a message to user
        QMessageBox.warning(
            self,
            f"⏸️ Configuration Required",
            f"The process is paused at Step {step_num}.\n\n"
            f"Please configure {mcp_name.upper()} in the tab above and then click 'Configure & Continue'."
        )
    
    def on_ui_progress(self, step_num: int, message: str):
        """
        Handle progress signal from UIControl tool.
        Appends message to logger without blocking.
        """
        timestamp = __import__('datetime').datetime.now().strftime("%H:%M:%S")
        self.append_log(f"[{step_num}] [{timestamp}] {message}")
    
    def on_mcp_accessed(self, step_num: int, mcp_list: list):
        """
        Handle MCP access signal from UIControl tool.
        Updates the logger with MCP access info.
        """
        pass
    
    def on_continue_clicked(self):
        """
        Handle "Configure & Continue" button click.
        Validates MCP config and resumes process execution.
        """
        if not self.paused_mcp:
            return
        
        # Map MCP name to platform
        mcp_to_platform = {
            "github": "GitHub",
            "jira": "Jira",
            "google_drive": "Google Drive",
            "playwright": "Playwright"
        }
        platform = mcp_to_platform.get(self.paused_mcp.lower(), self.paused_mcp)
        
        # Test the MCP to ensure it's configured properly
        self.show_status(f"Testing {platform} configuration...", "info")
        
        try:
            result = self.mcp_setup_service.test_all_mcps()
            if result.get(platform, {}).get("success"):
                self.show_status(f"✓ {platform} configured successfully! Resuming process...", "success")
                
                # Resume the paused execution
                self.ui_bridge.resume_from_pause({"configured": True})
                
                # Hide the Continue button
                self.continue_button.hide()
                self.paused_step = None
                self.paused_mcp = None
            else:
                error = result.get(platform, {}).get("error", "Unknown error")
                self.show_status(f"✗ {platform} test failed: {error}. Please check configuration.", "error")
        
        except Exception as e:
            self.show_status(f"✗ Error testing {platform}: {str(e)}", "error")
