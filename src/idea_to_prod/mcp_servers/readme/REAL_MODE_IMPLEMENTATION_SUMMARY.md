# Real API Mode Implementation Summary

This document describes the real API mode implementations for the MCP servers. Each MCP server now supports both **stub mode** (for testing with local storage) and **api mode** (for real integration with actual services).

## Overview

- **Stub Mode** (`mode="stub"`): Uses local JSON files or directory storage for testing
- **API Mode** (`mode="api"`): Uses real service APIs for production use

## GitHub MCP Server

### Configuration

```python
from src.idea_to_prod.mcp_servers.github_mcp import GitHubMCPServer
from src.idea_to_prod.mcp_servers.config.github_config import GitHubConfig

# Real API mode
config = GitHubConfig(
    mode="api",
    github_token="your_github_token_here",
    github_username="your_github_username"
)
server = GitHubMCPServer(config)
```

### Environment Variables

```bash
export GITHUB_MCP_MODE=api
export GITHUB_TOKEN=your_github_token
export GITHUB_USERNAME=your_username
export GITHUB_OWNER=your_organization
```

### Implemented Methods (API Mode)

- `create_repository()` - Creates a real GitHub repository
- `get_repository()` - Fetches repository info from GitHub
- `list_repositories()` - Lists your GitHub repositories
- `create_issue()` - Creates issues in real repositories
- `get_issue()` - Retrieves issue details
- `list_issues()` - Lists issues by state

### Dependencies

- `PyGithub>=2.1.0` (already in pyproject.toml)

### Authentication

1. Generate a personal access token on GitHub: https://github.com/settings/tokens
2. Ensure token has `repo` scope for repository access
3. Set `GITHUB_TOKEN` environment variable or pass to config

---

## Jira MCP Server

### Configuration

```python
from src.idea_to_prod.mcp_servers.jira_mcp import JiraMCPServer
from src.idea_to_prod.mcp_servers.config.jira_config import JiraConfig

# Real API mode
config = JiraConfig(
    mode="api",
    jira_base_url="https://your-jira-instance.atlassian.net",
    jira_username="your_email@example.com",
    jira_api_token="your_jira_api_token"
)
server = JiraMCPServer(config)
```

### Environment Variables

```bash
export JIRA_MCP_MODE=api
export JIRA_BASE_URL=https://your-jira-instance.atlassian.net
export JIRA_USERNAME=your_email@example.com
export JIRA_API_TOKEN=your_api_token
```

### Implemented Methods (API Mode)

- `create_issue()` - Creates real Jira issues
- `get_issue()` - Retrieves issue details
- `update_issue()` - Updates issue fields and status
- `list_issues()` - Lists issues based on JQL queries

### Dependencies

- `jira>=3.10.0` (already in pyproject.toml)

### Authentication

1. For Atlassian Cloud:
   - Generate API token: https://id.atlassian.com/manage-profile/security/api-tokens
   - Use your email as username
2. For Jira Server/Data Center:
   - Use your Jira username and password or API token
3. Set environment variables or pass to config

---

## Google Drive MCP Server

### Configuration

```python
from src.idea_to_prod.mcp_servers.google_drive_mcp import GoogleDriveMCPServer
from src.idea_to_prod.mcp_servers.config.google_drive_config import GoogleDriveConfig

# Real API mode
config = GoogleDriveConfig(
    mode="api",
    google_credentials_path="path/to/credentials.json"
)
server = GoogleDriveMCPServer(config)
```

### Environment Variables

```bash
export GDRIVE_MCP_MODE=api
export GOOGLE_APPLICATION_CREDENTIALS=path/to/credentials.json
# OR for OAuth2:
# Place credentials.json in the working directory
```

### Implemented Methods (API Mode)

- `save_document()` - Saves documents to Google Drive
- `read_document()` - Reads documents from Google Drive
- `list_files()` - Lists files in Google Drive
- `delete_file()` - Deletes files from Google Drive
- `create_folder()` - Creates folders in Google Drive
- `get_file_metadata()` - Retrieves file metadata

### Dependencies

- `google-auth-oauthlib>=1.0.0`
- `google-auth-httplib2>=0.2.0`
- `google-api-python-client>=2.100.0`
(all already in pyproject.toml)

### Authentication

**Option 1: Service Account (Recommended for server-side)**
1. Create a service account in Google Cloud Console
2. Download the JSON credentials file
3. Set `GOOGLE_APPLICATION_CREDENTIALS` environment variable

**Option 2: OAuth2 (For user-facing applications)**
1. Create OAuth2 credentials in Google Cloud Console
2. Download credentials.json to your working directory
3. The first run will open a browser for authentication

---

## Switching Between Modes

### Stub Mode (Default - Testing)

```python
config = GitHubConfig(mode="stub")  # No credentials needed
```

### API Mode (Production)

```python
config = GitHubConfig(mode="api", github_token="...")
```

## Error Handling

All methods return consistent response objects:

```python
# Success response
{
    "success": True,
    "message": "Operation successful",
    "data": {...}
}

# Error response
{
    "status": "error",
    "message": "Error description",
    "error": "ErrorType"
}
```

## Rate Limiting

Each MCP respects the API rate limits:
- **GitHub**: Standard rate limits (60 unauthenticated, 5000 authenticated per hour)
- **Jira**: Instance-specific rate limits
- **Google Drive**: Depends on quota

## Migration Guide

If you're switching from stub to real mode:

1. Update configuration to set `mode="api"`
2. Provide required authentication credentials
3. API methods maintain the same interface as stub methods
4. Error handling is consistent across both modes

## Troubleshooting

### GitHub API Issues
- Verify token has correct scopes
- Check rate limits: `gh api rate_limit`
- Ensure user/org exists

### Jira API Issues
- Verify Jira instance URL is correct
- Confirm API token is active
- Check project key exists

### Google Drive API Issues
- Enable Google Drive API in Cloud Console
- Verify credentials have proper permissions
- Check quota limits

## Testing

Each MCP includes test files:
- `tests/test_github_mcp.py`
- `tests/test_jira_mcp.py`
- `tests/test_google_drive_mcp.py`

Test both modes:
```bash
# Stub mode tests (no credentials needed)
pytest tests/test_github_mcp.py -k "stub"

# API mode tests (requires credentials)
pytest tests/test_github_mcp.py -k "api"
```

---

## Future Enhancements

Potential improvements for API modes:
- Retry logic with exponential backoff
- Caching layer for frequently accessed items
- Batch operations support
- Webhook event handling
- More advanced query capabilities
