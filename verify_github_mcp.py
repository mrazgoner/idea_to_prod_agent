#!/usr/bin/env python
"""
Quick verification script for GitHub MCP Server
Runs in the workspace and tests basic functionality
"""

import sys
from pathlib import Path

# Add src to path for imports
workspace = Path(__file__).parent
src_path = workspace / "src"
sys.path.insert(0, str(src_path))

from idea_to_prod.mcp_servers.config.github_config import GitHubConfig
from idea_to_prod.mcp_servers.github_mcp import GitHubMCPServer

print("=" * 80)
print("GitHub MCP Server - Verification")
print("=" * 80)

# Initialize server with stub mode
config = GitHubConfig(mode="stub", enable_logging=False)
server = GitHubMCPServer(config)

print("\n✓ GitHub MCP Server initialized successfully!")

# Test creating a repository
repo = server.create_repository(
    name="test-repo",
    owner="test-org",
    description="Test repository"
)
assert repo["success"], "Failed to create repository"
print(f"✓ Repository created: {repo['repository']['name']}")

# Test creating an issue
issue = server.create_issue(
    repository="test-org/test-repo",
    title="Test Issue",
    body="Test issue body"
)
assert issue["success"], "Failed to create issue"
print(f"✓ Issue created: #{issue['issue']['number']}")

# Test adding a comment
comment = server.add_comment(
    repository="test-org/test-repo",
    issue_number=1,
    body="Test comment",
    author="test-user"
)
assert comment["success"], "Failed to add comment"
print(f"✓ Comment added to issue")

# Test creating a pull request
pr = server.create_pull_request(
    repository="test-org/test-repo",
    title="Test PR",
    head_branch="feature/test",
    base_branch="main"
)
assert pr["success"], "Failed to create pull request"
print(f"✓ Pull Request created: #{pr['pull_request']['number']}")

# Test branch management
branch = server.create_branch(
    repository="test-org/test-repo",
    branch_name="feature/another",
    base_branch="main"
)
assert branch["success"], "Failed to create branch"
branches = server.list_branches("test-org/test-repo")
assert branches["success"], "Failed to list branches"
print(f"✓ Branch management working ({branches['total']} branches)")

# Test listing operations
repos = server.list_repositories()
assert repos["success"], "Failed to list repositories"
print(f"✓ Repository listing working ({repos['total']} repos)")

issues = server.list_issues("test-org/test-repo", state="all")
assert issues["success"], "Failed to list issues"
print(f"✓ Issue listing working ({issues['total']} issues)")

prs = server.list_pull_requests("test-org/test-repo", state="all")
assert prs["success"], "Failed to list PRs"
print(f"✓ PR listing working ({prs['total']} PRs)")

print("\n" + "=" * 80)
print("✓ All GitHub MCP Server operations verified successfully!")
print("=" * 80)
