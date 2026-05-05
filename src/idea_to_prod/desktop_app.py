"""
Idea-To-Prod Desktop Application

A native PyQt6-based desktop application for the Idea-To-Prod Agent Team.
Provides all features of the web UI but as a standalone desktop app.
"""

import sys
import logging
from pathlib import Path
from typing import Optional, Dict, Any

from PyQt6.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QLabel, QTextEdit, QPushButton, QTabWidget, QFormLayout,
    QLineEdit, QComboBox, QCheckBox, QFrame, QScrollArea,
    QMessageBox, QGridLayout, QProgressBar, QStatusBar
)
from PyQt6.QtCore import Qt, QThread, pyqtSignal, QTimer
from PyQt6.QtGui import QFont, QIcon, QColor, QPixmap

from idea_to_prod.agents.team import IdeaToProdTeam
from idea_to_prod.services.mcp_setup_service import MCPSetupService
from idea_to_prod.services.mcp_connection_service import MCPConnectionService

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# ============================================================================
# Worker Threads
# ============================================================================

class ProcessIdeaWorker(QThread):
    """Worker thread for processing ideas"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    progress = pyqtSignal(str, int)  # message, step number
    
    def __init__(self, team: IdeaToProdTeam, idea: str):
        super().__init__()
        self.team = team
        self.idea = idea
    
    def run(self):
        try:
            self.progress.emit("Starting High-Level Design...", 1)
            result = self.team.process_idea(self.idea)
            
            for i in range(2, 6):
                self.progress.emit(f"Completed Stage {i-1}", i)
            
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


class TestMCPWorker(QThread):
    """Worker thread for testing MCP connections"""
    finished = pyqtSignal(dict)
    error = pyqtSignal(str)
    
    def __init__(self, mcp_setup_service: MCPSetupService):
        super().__init__()
        self.mcp_setup_service = mcp_setup_service
    
    def run(self):
        try:
            result = self.mcp_setup_service.test_all_mcps()
            self.finished.emit(result)
        except Exception as e:
            self.error.emit(str(e))


# ============================================================================
# UI Widgets
# ============================================================================

class WorkflowDiagram(QWidget):
    """Custom widget for displaying the workflow diagram"""
    
    def __init__(self):
        super().__init__()
        self.steps = [
            ("High-Level Design", "pending"),
            ("Detailed Design", "pending"),
            ("Code Generation", "pending"),
            ("Test Generation", "pending"),
            ("Test Execution", "pending")
        ]
        self.init_ui()
    
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(15)
        
        for i, (step_name, _) in enumerate(self.steps, 1):
            step_frame = self.create_step_frame(i, step_name)
            layout.addWidget(step_frame)
            
            if i < len(self.steps):
                arrow = QLabel("↓")
                arrow.setAlignment(Qt.AlignmentFlag.AlignCenter)
                arrow.setFont(QFont("Arial", 16, QFont.Weight.Bold))
                arrow.setStyleSheet("color: #667eea;")
                layout.addWidget(arrow)
        
        layout.addStretch()
        self.setLayout(layout)
    
    def create_step_frame(self, step_num: int, step_name: str) -> QFrame:
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: white;
                border-left: 4px solid #667eea;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        
        layout = QHBoxLayout()
        
        # Step number circle
        num_label = QLabel(str(step_num))
        num_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        num_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        num_label.setStyleSheet("""
            background-color: #667eea;
            color: white;
            border-radius: 20px;
            width: 40px;
            height: 40px;
            padding: 0px;
        """)
        
        # Step name
        name_label = QLabel(step_name)
        name_label.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        layout.addWidget(num_label)
        layout.addWidget(name_label)
        layout.addStretch()
        
        frame.setLayout(layout)
        frame.setObjectName(f"step-{step_num}")
        return frame
    
    def set_step_status(self, step_num: int, status: str):
        """Update step status: pending, active, completed, failed"""
        self.steps[step_num - 1] = (self.steps[step_num - 1][0], status)
        
        step_frame = self.findChild(QFrame, f"step-{step_num}")
        if step_frame:
            if status == "completed":
                style = "border-left: 4px solid #4CAF50; background-color: #e8f5e9;"
            elif status == "active":
                style = "border-left: 4px solid #2196F3; background-color: #e3f2fd;"
            elif status == "failed":
                style = "border-left: 4px solid #f44336; background-color: #ffebee;"
            else:
                style = "border-left: 4px solid #ccc; background-color: white;"
            
            step_frame.setStyleSheet(f"""
                QFrame {{
                    {style}
                    border-radius: 6px;
                    padding: 12px;
                }}
            """)
    
    def reset(self):
        """Reset all steps to pending"""
        for i in range(1, 6):
            self.set_step_status(i, "pending")


class MCPStatusPanel(QWidget):
    """Widget for displaying MCP connection status"""
    
    def __init__(self):
        super().__init__()
        self.mcp_cards = {}
        self.init_ui()
    
    def init_ui(self):
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
        frame = QFrame()
        frame.setStyleSheet("""
            QFrame {
                background-color: #f5f5f5;
                border-left: 4px solid #ccc;
                border-radius: 6px;
                padding: 12px;
            }
        """)
        
        layout = QVBoxLayout()
        
        title = QLabel(platform)
        title.setFont(QFont("Arial", 11, QFont.Weight.Bold))
        
        status = QLabel("Checking...")
        status.setFont(QFont("Arial", 10))
        status.setAlignment(Qt.AlignmentFlag.AlignCenter)
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
            card.setStyleSheet("""
                QFrame {
                    background-color: #e8f5e9;
                    border-left: 4px solid #4CAF50;
                    border-radius: 6px;
                    padding: 12px;
                }
            """)
            status_label.setText("✓ Connected")
            status_label.setStyleSheet("color: #2e7d32;")
        else:
            card.setStyleSheet("""
                QFrame {
                    background-color: #ffebee;
                    border-left: 4px solid #f44336;
                    border-radius: 6px;
                    padding: 12px;
                }
            """)
            status_label.setText("✗ Disconnected")
            status_label.setStyleSheet("color: #c62828;")


# ============================================================================
# Main Application Window
# ============================================================================

class IdeaToProdApp(QMainWindow):
    """Main application window"""
    
    def __init__(self):
        super().__init__()
        self.team = IdeaToProdTeam()
        self.mcp_setup_service = MCPSetupService()
        self.process_worker = None
        self.mcp_worker = None
        self.init_ui()
        self.setWindowTitle("Idea-To-Prod Agent Team")
        self.setGeometry(100, 100, 1200, 800)
    
    def init_ui(self):
        """Initialize the user interface"""
        # Create main widget
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        
        # Main layout
        main_layout = QHBoxLayout()
        main_layout.setContentsMargins(20, 20, 20, 20)
        main_layout.setSpacing(20)
        
        # Left side - Input and diagram
        left_layout = QVBoxLayout()
        
        # Idea input section
        idea_label = QLabel("Application Idea")
        idea_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.idea_input = QTextEdit()
        self.idea_input.setPlaceholderText(
            "Describe your application idea here...\n\n"
            "Example: A real-time collaboration tool for remote teams with chat, "
            "file sharing, and video conferencing"
        )
        self.idea_input.setMinimumHeight(120)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        self.process_button = QPushButton("Process Idea")
        self.process_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.process_button.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 10px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #5568d3;
            }
            QPushButton:pressed {
                background-color: #4557c2;
            }
        """)
        self.process_button.clicked.connect(self.process_idea)
        
        self.test_button = QPushButton("Test MCPs")
        self.test_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.test_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 10px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3d8b40;
            }
        """)
        self.test_button.clicked.connect(self.test_mcp_connections)
        
        self.reset_button = QPushButton("Reset")
        self.reset_button.setFont(QFont("Arial", 10, QFont.Weight.Bold))
        self.reset_button.setStyleSheet("""
            QPushButton {
                background-color: #f44336;
                color: white;
                padding: 10px;
                border-radius: 6px;
                border: none;
            }
            QPushButton:hover {
                background-color: #da190b;
            }
            QPushButton:pressed {
                background-color: #c2160a;
            }
        """)
        self.reset_button.clicked.connect(self.reset_form)
        
        button_layout.addWidget(self.process_button)
        button_layout.addWidget(self.test_button)
        button_layout.addWidget(self.reset_button)
        
        # Status message
        self.status_label = QLabel()
        self.status_label.setWordWrap(True)
        self.status_label.setMinimumHeight(30)
        self.status_label.setStyleSheet("""
            background-color: #e3f2fd;
            color: #1565c0;
            padding: 10px;
            border-radius: 6px;
            border-left: 4px solid #2196F3;
        """)
        self.status_label.hide()
        
        left_layout.addWidget(idea_label)
        left_layout.addWidget(self.idea_input)
        left_layout.addLayout(button_layout)
        left_layout.addWidget(self.status_label)
        
        # Workflow diagram
        diagram_label = QLabel("Processing Pipeline")
        diagram_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        self.workflow_diagram = WorkflowDiagram()
        
        left_layout.addWidget(diagram_label)
        left_layout.addWidget(self.workflow_diagram)
        
        # Right side - Configuration tabs
        right_layout = QVBoxLayout()
        
        config_label = QLabel("MCP Platform Configuration")
        config_label.setFont(QFont("Arial", 12, QFont.Weight.Bold))
        
        # MCP Status panel
        self.mcp_status = MCPStatusPanel()
        
        # Tabs
        self.tabs = QTabWidget()
        self.tabs.addTab(self.create_github_tab(), "GitHub")
        self.tabs.addTab(self.create_jira_tab(), "Jira")
        self.tabs.addTab(self.create_google_drive_tab(), "Google Drive")
        self.tabs.addTab(self.create_playwright_tab(), "Playwright")
        
        right_layout.addWidget(config_label)
        right_layout.addWidget(self.mcp_status)
        right_layout.addWidget(self.tabs)
        right_layout.addStretch()
        
        # Add left and right to main
        main_layout.addLayout(left_layout, 1)
        main_layout.addLayout(right_layout, 1)
        
        main_widget.setLayout(main_layout)
        
        # Status bar
        self.statusBar().showMessage("Ready")
        
        # Test MCPs on startup
        QTimer.singleShot(500, self.test_mcp_connections)
    
    def create_github_tab(self) -> QWidget:
        """Create GitHub configuration tab"""
        widget = QWidget()
        layout = QFormLayout()
        
        mode = QComboBox()
        mode.addItems(["stub", "real"])
        layout.addRow("Mode:", mode)
        
        token = QLineEdit()
        token.setEchoMode(QLineEdit.EchoMode.Password)
        token.setPlaceholderText("ghp_xxxxxxxxxxxxxxxxxxxx")
        layout.addRow("Personal Access Token:", token)
        
        username = QLineEdit()
        username.setPlaceholderText("Your GitHub username")
        layout.addRow("Username:", username)
        
        url = QLineEdit()
        url.setText("https://api.github.com")
        layout.addRow("Base URL:", url)
        
        logging_checkbox = QCheckBox("Enable Logging")
        layout.addRow("", logging_checkbox)
        
        save_button = QPushButton("Save & Test GitHub Config")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
        """)
        
        def save_github_config():
            config = {
                "mode": mode.currentText(),
                "token": token.text() if token.text() else None,
                "username": username.text() if username.text() else None,
                "base_url": url.text(),
                "enable_logging": logging_checkbox.isChecked()
            }
            
            is_valid, error_msg = self.mcp_setup_service.validate_config("GitHub", config)
            if not is_valid:
                self.show_status(f"GitHub config invalid: {error_msg}", "error")
                return
            
            success, msg = self.mcp_setup_service.save_config("GitHub", config)
            if success:
                self.show_status(f"Testing GitHub MCP...", "info")
                result = self.mcp_setup_service.test_mcp("GitHub", config)
                if result.get("success"):
                    self.show_status("✓ GitHub config saved and tested successfully!", "success")
                    self.mcp_status.update_status("GitHub", True)
                else:
                    self.show_status(f"GitHub config saved but test failed: {result.get('error')}", "warning")
                    self.mcp_status.update_status("GitHub", False)
            else:
                self.show_status(f"Failed to save GitHub config: {msg}", "error")
        
        save_button.clicked.connect(save_github_config)
        layout.addRow("", save_button)
        
        widget.setLayout(layout)
        return widget
    
    def create_jira_tab(self) -> QWidget:
        """Create Jira configuration tab"""
        widget = QWidget()
        layout = QFormLayout()
        
        mode = QComboBox()
        mode.addItems(["stub", "real"])
        layout.addRow("Mode:", mode)
        
        url = QLineEdit()
        url.setPlaceholderText("https://your-domain.atlassian.net")
        layout.addRow("Instance URL:", url)
        
        email = QLineEdit()
        email.setPlaceholderText("your-email@example.com")
        layout.addRow("Email:", email)
        
        token = QLineEdit()
        token.setEchoMode(QLineEdit.EchoMode.Password)
        token.setPlaceholderText("Your API token")
        layout.addRow("API Token:", token)
        
        logging_checkbox = QCheckBox("Enable Logging")
        layout.addRow("", logging_checkbox)
        
        save_button = QPushButton("Save & Test Jira Config")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
        """)
        
        def save_jira_config():
            config = {
                "mode": mode.currentText(),
                "instance_url": url.text() if url.text() else None,
                "email": email.text() if email.text() else None,
                "api_token": token.text() if token.text() else None,
                "enable_logging": logging_checkbox.isChecked()
            }
            
            is_valid, error_msg = self.mcp_setup_service.validate_config("Jira", config)
            if not is_valid:
                self.show_status(f"Jira config invalid: {error_msg}", "error")
                return
            
            success, msg = self.mcp_setup_service.save_config("Jira", config)
            if success:
                self.show_status(f"Testing Jira MCP...", "info")
                result = self.mcp_setup_service.test_mcp("Jira", config)
                if result.get("success"):
                    self.show_status("✓ Jira config saved and tested successfully!", "success")
                    self.mcp_status.update_status("Jira", True)
                else:
                    self.show_status(f"Jira config saved but test failed: {result.get('error')}", "warning")
                    self.mcp_status.update_status("Jira", False)
            else:
                self.show_status(f"Failed to save Jira config: {msg}", "error")
        
        save_button.clicked.connect(save_jira_config)
        layout.addRow("", save_button)
        
        widget.setLayout(layout)
        return widget
    
    def create_google_drive_tab(self) -> QWidget:
        """Create Google Drive configuration tab"""
        widget = QWidget()
        layout = QFormLayout()
        
        mode = QComboBox()
        mode.addItems(["stub", "real"])
        layout.addRow("Mode:", mode)
        
        creds = QLineEdit()
        creds.setPlaceholderText("/path/to/credentials.json")
        layout.addRow("Credentials Path:", creds)
        
        folder = QLineEdit()
        folder.setPlaceholderText("Google Drive folder ID")
        layout.addRow("Folder ID:", folder)
        
        logging_checkbox = QCheckBox("Enable Logging")
        layout.addRow("", logging_checkbox)
        
        save_button = QPushButton("Save & Test Google Drive Config")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
        """)
        
        def save_gdrive_config():
            config = {
                "mode": mode.currentText(),
                "credentials_path": creds.text() if creds.text() else None,
                "folder_id": folder.text() if folder.text() else None,
                "enable_logging": logging_checkbox.isChecked()
            }
            
            is_valid, error_msg = self.mcp_setup_service.validate_config("Google Drive", config)
            if not is_valid:
                self.show_status(f"Google Drive config invalid: {error_msg}", "error")
                return
            
            success, msg = self.mcp_setup_service.save_config("Google Drive", config)
            if success:
                self.show_status(f"Testing Google Drive MCP...", "info")
                result = self.mcp_setup_service.test_mcp("Google Drive", config)
                if result.get("success"):
                    self.show_status("✓ Google Drive config saved and tested successfully!", "success")
                    self.mcp_status.update_status("Google Drive", True)
                else:
                    self.show_status(f"Google Drive config saved but test failed: {result.get('error')}", "warning")
                    self.mcp_status.update_status("Google Drive", False)
            else:
                self.show_status(f"Failed to save Google Drive config: {msg}", "error")
        
        save_button.clicked.connect(save_gdrive_config)
        layout.addRow("", save_button)
        
        widget.setLayout(layout)
        return widget
    
    def create_playwright_tab(self) -> QWidget:
        """Create Playwright configuration tab"""
        widget = QWidget()
        layout = QFormLayout()
        
        mode = QComboBox()
        mode.addItems(["stub", "real"])
        layout.addRow("Mode:", mode)
        
        headless = QCheckBox("Headless Mode")
        headless.setChecked(True)
        layout.addRow("", headless)
        
        timeout = QLineEdit()
        timeout.setText("30000")
        timeout.setPlaceholderText("30000")
        layout.addRow("Timeout (ms):", timeout)
        
        logging_checkbox = QCheckBox("Enable Logging")
        layout.addRow("", logging_checkbox)
        
        save_button = QPushButton("Save & Test Playwright Config")
        save_button.setStyleSheet("""
            QPushButton {
                background-color: #667eea;
                color: white;
                padding: 8px;
                border-radius: 4px;
            }
        """)
        
        def save_pw_config():
            try:
                timeout_val = int(timeout.text())
            except ValueError:
                self.show_status("Playwright timeout must be a number", "error")
                return
            
            config = {
                "mode": mode.currentText(),
                "headless": headless.isChecked(),
                "timeout": timeout_val,
                "enable_logging": logging_checkbox.isChecked()
            }
            
            is_valid, error_msg = self.mcp_setup_service.validate_config("Playwright", config)
            if not is_valid:
                self.show_status(f"Playwright config invalid: {error_msg}", "error")
                return
            
            success, msg = self.mcp_setup_service.save_config("Playwright", config)
            if success:
                self.show_status(f"Testing Playwright MCP...", "info")
                result = self.mcp_setup_service.test_mcp("Playwright", config)
                if result.get("success"):
                    self.show_status("✓ Playwright config saved and tested successfully!", "success")
                    self.mcp_status.update_status("Playwright", True)
                else:
                    self.show_status(f"Playwright config saved but test failed: {result.get('error')}", "warning")
                    self.mcp_status.update_status("Playwright", False)
            else:
                self.show_status(f"Failed to save Playwright config: {msg}", "error")
        
        save_button.clicked.connect(save_pw_config)
        layout.addRow("", save_button)
        
        widget.setLayout(layout)
        return widget
    
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
        self.workflow_diagram.reset()
        
        self.process_worker = ProcessIdeaWorker(self.team, idea)
        self.process_worker.finished.connect(self.on_process_finished)
        self.process_worker.error.connect(self.on_process_error)
        self.process_worker.progress.connect(self.on_process_progress)
        self.process_worker.start()
    
    def on_process_progress(self, message: str, step: int):
        """Update progress during processing"""
        self.statusBar().showMessage(message)
        self.workflow_diagram.set_step_status(step, "active")
        if step > 1:
            self.workflow_diagram.set_step_status(step - 1, "completed")
    
    def on_process_finished(self, result: dict):
        """Handle process completion"""
        self.workflow_diagram.set_step_status(5, "completed")
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
        
        # Update status cards
        for platform, platform_result in result.items():
            if isinstance(platform_result, dict):
                connected = platform_result.get("success", False)
                self.mcp_status.update_status(platform, connected)
    
    def on_mcp_test_error(self, error: str):
        """Handle MCP test error"""
        self.show_status(f"MCP test error: {error}", "error")
        self.test_button.setEnabled(True)
    
    def reset_form(self):
        """Reset the form"""
        self.idea_input.clear()
        self.workflow_diagram.reset()
        self.status_label.hide()
        self.statusBar().showMessage("Ready")
    
    def show_status(self, message: str, status_type: str = "info"):
        """Show status message"""
        self.status_label.setText(message)
        self.status_label.show()
        
        if status_type == "success":
            self.status_label.setStyleSheet("""
                background-color: #e8f5e9;
                color: #2e7d32;
                padding: 10px;
                border-radius: 6px;
                border-left: 4px solid #4CAF50;
            """)
        elif status_type == "error":
            self.status_label.setStyleSheet("""
                background-color: #ffebee;
                color: #c62828;
                padding: 10px;
                border-radius: 6px;
                border-left: 4px solid #f44336;
            """)
        elif status_type == "warning":
            self.status_label.setStyleSheet("""
                background-color: #fff3e0;
                color: #e65100;
                padding: 10px;
                border-radius: 6px;
                border-left: 4px solid #ff9800;
            """)
        else:  # info
            self.status_label.setStyleSheet("""
                background-color: #e3f2fd;
                color: #1565c0;
                padding: 10px;
                border-radius: 6px;
                border-left: 4px solid #2196F3;
            """)


def main():
    """Main entry point"""
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    window = IdeaToProdApp()
    window.show()
    
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
