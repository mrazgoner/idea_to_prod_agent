# GitHub MCP (Model Context Protocol) Server

A comprehensive Model Context Protocol server implementation for GitHub operations. The server provides stub-based operations for testing and can be extended to support real GitHub API interactions.

## Overview

The GitHub MCP Server provides a unified interface for:
- **Repository Management**: Create, list, and retrieve repositories
- **Issue Management**: Create, read, update, and search issues
- **Pull Request Management**: Create, review, and merge pull requests
- **Branch Management**: Create and list branches
- **Collaboration**: Add comments and manage collaborators

## Architecture

### Components

1. **GitHubMCPServer** (`github_mcp.py`)
   - Main server class implementing all GitHub operations
   - Handles both stub and API modes
   - Manages in-memory data storage with persistent JSON backend

2. **GitHubConfig** (`config/github_config.py`)
   - Configuration management for the MCP server
   - Environment variable support
   - Tool allowlisting and constraints

3. **Data Models**
   - `GitHubRepository`: Represents GitHub repositories
   - `GitHubIssue`: Represents GitHub issues
   - `GitHubPullRequest`: Represents pull requests

## Features

### Repository Tools
- `create_repository()` - Create a new repository
- `get_repository()` - Retrieve repository information
- `list_repositories()` - List repositories with optional filtering

### Issue Management
- `create_issue()` - Create a new issue
- `get_issue()` - Retrieve issue details
- `list_issues()` - List issues by state (open/closed/all)
- `update_issue()` - Update issue properties
- `add_comment()` - Add comments to issues

### Pull Request Management
- `create_pull_request()` - Create a new pull request
- `get_pull_request()` - Retrieve PR details
- `list_pull_requests()` - List PRs by state

### Branch Management
- `list_branches()` - List repository branches
- `create_branch()` - Create new branches

## Configuration

### Environment Variables

Configure the GitHub MCP server using environment variables:

```bash
# GitHub API credentials
GITHUB_TOKEN=your_github_token
GITHUB_USERNAME=your_username
GITHUB_OWNER=your_organization

# API URL (optional, defaults to https://api.github.com)
GITHUB_API_URL=https://api.github.com

# Server mode
GITHUB_MCP_MODE=stub  # 'stub' for testing, 'api' for real API

# Storage directory
GITHUB_MCP_STORAGE_DIR=~/.idea_to_prod/github

# Logging
GITHUB_MCP_LOGGING=true
GITHUB_MCP_LOG_LEVEL=INFO
```

### Python Configuration

```python
from idea_to_prod.mcp_servers import GitHubConfig, GitHubMCPServer

# Create configuration
config = GitHubConfig(
    mode="stub",
    github_token="your_token",
    github_username="your_username",
    enable_logging=True,
    log_level="INFO"
)

# Initialize server
server = GitHubMCPServer(config)
```

## Usage Examples

### Create a Repository

```python
result = server.create_repository(
    name="my-project",
    owner="my-org",
    description="My awesome project",
    language="Python",
    topics=["ai", "python"]
)

print(result["repository"])
```

### Create an Issue

```python
result = server.create_issue(
    repository="my-org/my-project",
    title="Bug: Crash on startup",
    body="The application crashes when started with...",
    author="john-doe",
    labels=["bug", "critical"]
)

print(f"Issue #{result['issue']['number']} created")
```

### Create a Pull Request

```python
result = server.create_pull_request(
    repository="my-org/my-project",
    title="Feature: Add dark mode",
    head_branch="feature/dark-mode",
    base_branch="main",
    body="This PR adds support for dark mode...",
    author="jane-smith"
)

print(f"PR #{result['pull_request']['number']} created")
```

### Add a Comment

```python
result = server.add_comment(
    repository="my-org/my-project",
    issue_number=42,
    body="Great catch! I'll fix this right away.",
    author="john-doe"
)

print(f"Comment added: {result['comment']['id']}")
```

## Data Persistence

### Stub Mode

In stub mode, data is persisted to local JSON files:

```
~/.idea_to_prod/github/
├── repositories.json      # All repositories
├── issues.json           # All issues
├── pull_requests.json    # All pull requests
└── branches.json         # Branch information
```

### API Mode

In API mode (when implemented), the server communicates directly with the GitHub API:
- Uses OAuth tokens for authentication
- No local persistence required
- Real-time data synchronization

## Constraints & Limits

- **Max file size**: 100MB (configurable)
- **Max results per query**: 100 (configurable)
- **Max comment length**: 65,536 characters
- **Timeout**: 30 seconds (configurable)

These limits help prevent resource exhaustion and ensure reasonable response times.

## Error Handling

All methods return a consistent response format:

```python
{
    "success": True/False,
    "data": {...},  # Method-specific data
    "error": "Error message if success=False"
}
```

## Logging

The server includes comprehensive logging:

- **DEBUG**: Detailed operation tracking
- **INFO**: Operation summaries
- **WARNING**: Recoverable issues
- **ERROR**: Operation failures

Enable logging with:

```python
config = GitHubConfig(enable_logging=True, log_level="DEBUG")
```

## Future Enhancements

### API Mode Implementation
- Real GitHub API integration
- OAuth token management
- Rate limit handling
- Webhook support

### Additional Features
- Activity timeline
- Milestone management
- Release management
- Webhook event handling
- Advanced search capabilities
- Team management
- Repository settings

## Testing

Example test file available at:
`src/idea_to_prod/mcp_servers/tests/example_github_usage.py`

Run tests:

```bash
python -m pytest src/idea_to_prod/mcp_servers/tests/test_github_mcp.py -v
```

## Integration with IdeaToProdAgent

The GitHub MCP Server is integrated into the IdeaToProdAgent workflow:

1. **Agent 1 (Design)**: Can create repositories and design documents
2. **Agent 3 (Code Generation)**: Can reference pull requests and commit messages
3. **Agent 4 (Testing)**: Can create test issues and track results
4. **Agent 5 (Execution)**: Can manage deployment and release PRs

## Performance Notes

- **Stub mode** is optimized for development and testing
- **API mode** will depend on GitHub API rate limits
- Caching layer can be added for frequently accessed repositories
- Batch operations recommended for bulk tasks

## Security Considerations

1. **Token Security**: Never commit tokens to version control
2. **Rate Limiting**: Implement exponential backoff for API calls
3. **Input Validation**: All inputs are validated before processing
4. **Error Messages**: Sensitive details are excluded from logs

## License

Part of the IdeaToProdAgent project.
