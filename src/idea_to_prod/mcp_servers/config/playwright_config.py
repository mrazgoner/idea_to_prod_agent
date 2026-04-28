"""
Playwright MCP Server Configuration
Manages configurable settings for the Playwright MCP server.
"""

import os
from dataclasses import dataclass, field
from typing import Optional
from pathlib import Path


@dataclass
class PlaywrightConfig:
    """Configuration for Playwright MCP Server"""
    
    # Server identifiers
    name: str = "playwright-mcp"
    version: str = "1.0.0"
    
    # Playwright connection settings
    browser_type: str = "chromium"  # chromium, firefox, webkit
    headless: bool = True
    
    # Mode configuration (stub or api)
    mode: str = "stub"  # 'stub' for testing, 'api' for real browser automation
    
    # Local storage for test results and screenshots
    storage_dir: Path = field(default_factory=lambda: Path.home() / ".idea_to_prod" / "playwright")
    screenshots_dir: Path = field(default_factory=lambda: Path.home() / ".idea_to_prod" / "playwright" / "screenshots")
    results_dir: Path = field(default_factory=lambda: Path.home() / ".idea_to_prod" / "playwright" / "results")
    
    # MCP Protocol settings
    enable_logging: bool = True
    log_level: str = "INFO"
    
    # Browser settings
    timeout: int = 30000  # milliseconds
    viewport_width: int = 1280
    viewport_height: int = 720
    
    # Tool configuration
    allowed_tools: list[str] = field(default_factory=lambda: [
        "launch_browser",
        "close_browser",
        "navigate_to_url",
        "fill_input",
        "click_element",
        "take_screenshot",
        "get_page_content",
        "execute_javascript",
        "wait_for_element",
        "run_e2e_tests",
        "validate_page_element",
        "get_test_results",
    ])
    
    # Test configuration
    max_test_duration: int = 300  # seconds
    retry_attempts: int = 3
    retry_delay: int = 1000  # milliseconds
    
    # Trace and recording settings
    enable_trace: bool = True
    enable_video: bool = False
    
    def __post_init__(self):
        """Validate and prepare configuration after initialization"""
        # Validate browser type
        valid_browsers = ("chromium", "firefox", "webkit")
        if self.browser_type not in valid_browsers:
            raise ValueError(f"Browser type must be one of {valid_browsers}. Got: {self.browser_type}")
        
        # Validate mode
        if self.mode not in ("stub", "api"):
            raise ValueError(f"Mode must be 'stub' or 'api'. Got: {self.mode}")
        
        # Create storage directories if they don't exist
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self.screenshots_dir.mkdir(parents=True, exist_ok=True)
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
        # Load from environment variables if available
        self._load_from_env()
    
    def _load_from_env(self):
        """Load configuration from environment variables"""
        # Browser settings
        env_browser = os.getenv("PLAYWRIGHT_BROWSER")
        if env_browser:
            self.browser_type = env_browser
        
        env_headless = os.getenv("PLAYWRIGHT_HEADLESS", "").lower()
        if env_headless in ("true", "false"):
            self.headless = env_headless == "true"
        
        # Mode
        env_mode = os.getenv("PLAYWRIGHT_MODE")
        if env_mode in ("stub", "api"):
            self.mode = env_mode
        
        # Timeout
        env_timeout = os.getenv("PLAYWRIGHT_TIMEOUT")
        if env_timeout:
            try:
                self.timeout = int(env_timeout)
            except ValueError:
                pass
        
        # Video recording
        env_video = os.getenv("PLAYWRIGHT_VIDEO", "").lower()
        if env_video in ("true", "false"):
            self.enable_video = env_video == "true"


def create_config(mode: str = "stub", **kwargs) -> PlaywrightConfig:
    """
    Factory function to create Playwright configuration
    
    Args:
        mode: 'stub' for testing, 'api' for real browser automation
        **kwargs: Additional configuration overrides
    
    Returns:
        PlaywrightConfig instance
    """
    config = PlaywrightConfig(mode=mode, **kwargs)
    return config
