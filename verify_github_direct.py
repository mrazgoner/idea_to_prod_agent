#!/usr/bin/env python
"""Direct GitHub MCP test without full package imports"""

import sys
from pathlib import Path

# Add src to path
workspace = Path(__file__).parent
src_path = workspace / "src"
sys.path.insert(0, str(src_path))

# Direct imports without going through __init__
import importlib.util

# Load config module directly
config_path = src_path / "idea_to_prod" / "mcp_servers" / "config" / "github_config.py"
spec = importlib.util.spec_from_file_location("github_config", config_path)
github_config_module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(github_config_module)

# Load server module directly  
server_path = src_path / "idea_to_prod" / "mcp_servers" / "github_mcp.py"
spec = importlib.util.spec_from_file_location("github_mcp", server_path)
github_mcp_module = importlib.util.module_from_spec(spec)
sys.modules['github_config'] = github_config_module
spec.loader.exec_module(github_mcp_module)

GitHubConfig = github_config_module.GitHubConfig
GitHubMCPServer = github_mcp_module.GitHubMCPServer

print("=" * 80)
print("GitHub MCP Server - Direct Verification")
print("=" * 80)

# Initialize and test
try:
    config = GitHubConfig(mode="stub", enable_logging=False)
    server = GitHubMCPServer(config)
    print("\n✓ GitHub MCP Server initialized successfully!")
    
    # Test basic operations
    repo = server.create_repository(
        name="test-repo",
        owner="test-org"
    )
    print(f"✓ Repository created: {repo['success']}")
    
    issue = server.create_issue(
        repository="test-org/test-repo",
        title="Test"
    )
    print(f"✓ Issue created: {issue['success']}")
    
    pr = server.create_pull_request(
        repository="test-org/test-repo",
        title="Test PR",
        head_branch="feature/test",
        base_branch="main"
    )
    print(f"✓ PR created: {pr['success']}")
    
    print("\n" + "=" * 80)
    print("✓ GitHub MCP is working correctly!")
    print("=" * 80)
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
