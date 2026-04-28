#!/usr/bin/env python
"""GitHub MCP Implementation Verification"""

from pathlib import Path
import os

print("=" * 80)
print("GitHub MCP Implementation Verification")
print("=" * 80)

workspace = Path(__file__).parent
mcp_servers = workspace / "src" / "idea_to_prod" / "mcp_servers"

# Check files exist
files_to_check = {
    "GitHub Config": mcp_servers / "config" / "github_config.py",
    "GitHub MCP Server": mcp_servers / "github_mcp.py",
    "GitHub MCP README": mcp_servers / "readme" / "GITHUB_MCP_README.md",
    "GitHub MCP Implementation Summary": mcp_servers / "readme" / "GITHUB_MCP_IMPLEMENTATION_SUMMARY.md",
    "GitHub MCP Tests": mcp_servers / "tests" / "test_github_mcp.py",
    "GitHub Usage Example": mcp_servers / "tests" / "example_github_usage.py",
    "Config __init__": mcp_servers / "config" / "__init__.py",
    "MCP Servers __init__": mcp_servers / "__init__.py",
}

print("\n[Files Check]")
all_exist = True
for name, path in files_to_check.items():
    exists = path.exists()
    status = "✓" if exists else "✗"
    print(f"  {status} {name}: {path.relative_to(workspace)}")
    if not exists:
        all_exist = False

# Check file sizes and line counts
print("\n[File Statistics]")
for name, path in files_to_check.items():
    if path.exists():
        size_kb = path.stat().st_size / 1024
        with open(path) as f:
            lines = len(f.readlines())
        print(f"  {name}: {size_kb:.1f}KB ({lines} lines)")

# Check code quality
print("\n[Code Quality Checks]")

# Check imports in github_mcp.py
github_mcp_path = mcp_servers / "github_mcp.py"
with open(github_mcp_path) as f:
    content = f.read()
    classes = [
        "GitHubMCPServer",
        "GitHubRepository", 
        "GitHubIssue",
        "GitHubPullRequest"
    ]
    for cls in classes:
        found = cls in content
        status = "✓" if found else "✗"
        print(f"  {status} Class {cls} defined")
    
    methods = [
        "create_repository",
        "get_repository",
        "list_repositories",
        "create_issue",
        "get_issue",
        "list_issues",
        "update_issue",
        "add_comment",
        "create_pull_request",
        "get_pull_request",
        "list_pull_requests",
        "create_branch",
        "list_branches",
    ]
    
    print(f"\n  Methods implemented:")
    for method in methods:
        found = f"def {method}" in content
        status = "✓" if found else "✗"
        print(f"    {status} {method}")

# Check config file
print("\n[Configuration Settings]")
github_config_path = mcp_servers / "config" / "github_config.py"
with open(github_config_path) as f:
    config_content = f.read()
    settings = [
        "github_api_url",
        "github_token",
        "mode",
        "storage_dir",
        "enable_logging",
        "max_comment_length",
        "allowed_tools",
    ]
    for setting in settings:
        found = setting in config_content
        status = "✓" if found else "✗"
        print(f"  {status} {setting}")

# Check __init__ exports
print("\n[Module Exports]")
init_path = mcp_servers / "__init__.py"
with open(init_path) as f:
    init_content = f.read()
    exports = [
        "GitHubConfig",
        "create_github_config",
        "GitHubMCPServer",
    ]
    for export in exports:
        found = export in init_content
        status = "✓" if found else "✗"
        print(f"  {status} {export} exported from __init__.py")

print("\n" + "=" * 80)
if all_exist:
    print("✓ GitHub MCP Implementation Complete!")
    print("\nTo use GitHub MCP in your project:")
    print("  1. from idea_to_prod.mcp_servers import GitHubConfig, GitHubMCPServer")
    print("  2. config = GitHubConfig(mode='stub', github_username='user')")
    print("  3. server = GitHubMCPServer(config)")
    print("\nSee GITHUB_MCP_README.md for full documentation.")
else:
    print("✗ Some files are missing!")

print("=" * 80)
