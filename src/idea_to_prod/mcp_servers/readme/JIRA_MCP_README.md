# Jira MCP (Model Context Protocol) Server

A configurable Model Context Protocol server for Jira operations. This server provides a unified interface for interacting with Jira, supporting both stub mode (for testing) and API mode (for real Jira instances).

## Features

- **Create, read, update, and manage Jira issues**
- **Search and filter issues** with simple JQL-like queries
- **Manage issue workflows** - transition between statuses
- **Add comments** to issues
- **Project management** - list and manage projects
- **Configurable storage** - local JSON-based storage in stub mode
- **Enterprise-ready** - prepared for direct Jira API integration

## Supported Tools

### Issue Management
- `create_issue` - Create new issues
- `get_issue` - Retrieve issue details
- `update_issue` - Update issue fields
- `list_issues` - List issues with optional filters
- `search_issues` - Search using JQL-like queries
- `add_comment` - Add comments to issues
- `transition_issue` - Change issue status/workflow

### Project Management
- `get_project` - Get project details
- `list_projects` - List all projects
- `get_issue_types` - Get available issue types

## Installation

The Jira MCP is included in the IdeaToProdAgent project. No additional installation is required.

### Dependencies

- Python 3.8+
- No external dependencies required for stub mode
- Optional: `requests` library for real API integration

## Configuration

### Environment Variables

Configure Jira MCP using environment variables:

```bash
# Jira API Settings
export JIRA_BASE_URL="https://company.atlassian.net"
export JIRA_USERNAME="your-email@company.com"
export JIRA_API_TOKEN="your-api-token"

# MCP Settings
export JIRA_MCP_MODE="stub"  # or "api" for real Jira
export JIRA_MCP_STORAGE_DIR="~/.idea_to_prod/jira"
export JIRA_MCP_LOGGING="true"
export JIRA_MCP_LOG_LEVEL="INFO"
```

### Programmatic Configuration

```python
from jira_mcp import create_jira_server

# Stub mode (for testing)
jira = create_jira_server(
    mode="stub",
    enable_logging=True,
    log_level="INFO"
)

# API mode (real Jira)
jira = create_jira_server(
    jira_base_url="https://company.atlassian.net",
    jira_username="your-email@company.com",
    jira_api_token="your-api-token",
    mode="api",
    enable_logging=True
)
```

## Usage Examples

### Create an Issue

```python
result = jira.create_issue(
    summary="Implement user authentication",
    issue_type="Story",
    description="Add OAuth2 support",
    priority="High",
    assignee="alice",
    labels=["backend", "auth"]
)
issue_key = result["issue"]["key"]  # e.g., "DEFAULT-1"
```

### Get Issue Details

```python
result = jira.get_issue(issue_key="DEFAULT-1")
issue = result["issue"]
print(f"Status: {issue['status']}")
print(f"Assignee: {issue['assignee']}")
```

### Update an Issue

```python
result = jira.update_issue(
    issue_key="DEFAULT-1",
    assignee="bob",
    priority="Highest",
    labels=["backend", "auth", "urgent"]
)
```

### Change Issue Status

```python
result = jira.transition_issue(
    issue_key="DEFAULT-1",
    new_status="In Progress"
)
# Valid statuses: "To Do", "In Progress", "In Review", "Done"
```

### Add a Comment

```python
result = jira.add_comment(
    issue_key="DEFAULT-1",
    comment_text="Started implementation",
    author="alice"
)
```

### List Issues

```python
# All issues
result = jira.list_issues()

# Filtered by status
result = jira.list_issues(status="In Progress")

# Filtered by assignee
result = jira.list_issues(assignee="alice")

# Filtered by project
result = jira.list_issues(project="DEFAULT", max_results=50)
```

### Search Issues

```python
# Search by status
result = jira.search_issues(jql="status=Done")

# Search by type
result = jira.search_issues(jql="type=Bug")

# Search by assignee
result = jira.search_issues(jql="assignee=alice")
```

### List Projects

```python
result = jira.list_projects()
for project in result["projects"]:
    print(f"{project['name']}: {project['issue_count']} issues")
```

### Get Available Issue Types

```python
result = jira.get_issue_types()
for issue_type in result["issue_types"]:
    print(f"- {issue_type['name']}: {issue_type['description']}")
```

## Data Storage

### Stub Mode

Issues are stored in JSON format at `~/.idea_to_prod/jira/issues.json`. The storage location can be customized via:

- Environment variable: `JIRA_MCP_STORAGE_DIR`
- Configuration parameter: `storage_dir`

### API Mode

When API mode is enabled, issues are retrieved from the actual Jira instance. Local storage is not used.

## Supported Issue Statuses

- `To Do` - Not started
- `In Progress` - Currently being worked on
- `In Review` - Under review
- `Done` - Completed

## Supported Priorities

- `Lowest`
- `Low`
- `Medium`
- `High`
- `Highest`

## Supported Issue Types

- `Task` - A task or piece of work
- `Bug` - A bug in the software
- `Story` - A user story
- `Epic` - An epic spanning multiple issues
- `Sub-task` - A subtask of another issue

## Error Handling

All methods return a consistent response format:

```python
# Success
{
    "status": "success",
    "message": "Operation completed successfully",
    "issue": {...}
}

# Error
{
    "status": "error",
    "message": "Failed to create issue: Invalid input",
    "error": "ValueError"
}
```

## Testing

Run the example usage script to test basic functionality:

```bash
cd src/idea_to_prod/mcp_servers/tests
python example_jira_usage.py
```

This will:
1. Create several test issues
2. Retrieve issue details
3. Update issues
4. Add comments
5. Transition issue statuses
6. List and search issues
7. List projects and issue types

## API Mode Integration

To integrate with a real Jira instance:

1. Create an API token in Jira: https://id.atlassian.com/manage-profile/security/api-tokens
2. Set environment variables:
   ```bash
   export JIRA_BASE_URL="https://your-domain.atlassian.net"
   export JIRA_USERNAME="your-email@company.com"
   export JIRA_API_TOKEN="your-api-token"
   export JIRA_MCP_MODE="api"
   ```
3. Use the server as normal - API calls will be used automatically

## Architecture

- **JiraConfig** - Configuration management with environment variable support
- **JiraIssue** - Data class representing a Jira issue
- **JiraMCPServer** - Main server implementation with all tools

## File Structure

```
mcp_servers/
├── jira_mcp.py              # Main Jira MCP server
├── config/
│   └── jira_config.py       # Configuration management
└── tests/
    └── example_jira_usage.py # Example usage and tests
```

## Performance Considerations

- **Stub Mode**: All operations are in-memory, extremely fast
- **API Mode**: Performance depends on Jira instance and network latency
- **Max Results**: Limited to 100 results per query by default (configurable)
- **Comment Length**: Limited to 32,767 characters (Jira's limit)

## Future Enhancements

- [ ] Full Jira REST API v3 integration
- [ ] Support for custom fields
- [ ] Issue linking and relationship management
- [ ] Advanced search with complex JQL
- [ ] Webhook support for real-time updates
- [ ] Bulk operations (create/update multiple issues)
- [ ] Sprint management
- [ ] Release/version management
- [ ] User and permission management

## License

Part of the IdeaToProdAgent project.

## Support

For issues or feature requests, please refer to the main project repository.
