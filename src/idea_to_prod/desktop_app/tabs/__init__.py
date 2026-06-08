"""Tabs package for desktop application"""

from .github_tab import GitHubTab
from .jira_tab import JiraTab
from .google_drive_tab import GoogleDriveTab
from .playwright_tab import PlaywrightTab

__all__ = ['GitHubTab', 'JiraTab', 'GoogleDriveTab', 'PlaywrightTab']
