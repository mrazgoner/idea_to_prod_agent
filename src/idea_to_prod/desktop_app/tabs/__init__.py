"""Tabs package for desktop application"""

from .github_tab import GitHubTab
from .jira_tab import JiraTab
from .google_drive_tab import GoogleDriveTab
from .playwright_tab import PlaywrightTab
from .basic_config_tab import BasicConfigTab

__all__ = ['GitHubTab', 'JiraTab', 'GoogleDriveTab', 'PlaywrightTab', 'BasicConfigTab']
