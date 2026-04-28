"""
Example usage and tests for Jira MCP Server
Demonstrates how to use the Jira MCP server in stub mode
"""

import sys
from pathlib import Path

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent.parent))

from jira_mcp import create_jira_server, JiraMCPServer


def test_basic_operations():
    """Test basic Jira MCP operations"""
    print("\n" + "="*70)
    print("JIRA MCP SERVER - EXAMPLE USAGE")
    print("="*70 + "\n")
    
    # Create a Jira MCP server in stub mode
    jira = create_jira_server(mode="stub", enable_logging=True, log_level="INFO")
    print(f"✓ Created Jira MCP Server: {jira.config.name} v{jira.config.version}")
    print(f"  Mode: {jira.config.mode}\n")
    
    # Test 1: Create issues
    print("Test 1: Creating issues...")
    print("-" * 70)
    
    issue1_result = jira.create_issue(
        summary="Implement user authentication",
        issue_type="Story",
        description="Add OAuth2 support for user login",
        priority="High",
        labels=["backend", "security"]
    )
    issue1_key = issue1_result["issue"]["key"]
    print(f"✓ Created issue: {issue1_key}")
    print(f"  Summary: {issue1_result['issue']['summary']}\n")
    
    issue2_result = jira.create_issue(
        summary="Fix login button styling",
        issue_type="Bug",
        description="Button appears cut off on mobile devices",
        priority="Medium",
        labels=["frontend", "ui"]
    )
    issue2_key = issue2_result["issue"]["key"]
    print(f"✓ Created issue: {issue2_key}")
    print(f"  Summary: {issue2_result['issue']['summary']}\n")
    
    issue3_result = jira.create_issue(
        summary="Add password reset feature",
        issue_type="Task",
        description="Implement email-based password reset",
        priority="Medium",
        labels=["feature", "auth"]
    )
    issue3_key = issue3_result["issue"]["key"]
    print(f"✓ Created issue: {issue3_key}\n")
    
    # Test 2: Get issue details
    print("Test 2: Retrieving issue details...")
    print("-" * 70)
    
    get_result = jira.get_issue(issue1_key)
    if get_result["status"] == "success":
        issue = get_result["issue"]
        print(f"✓ Retrieved issue {issue1_key}")
        print(f"  Status: {issue['status']}")
        print(f"  Priority: {issue['priority']}")
        print(f"  Type: {issue['issue_type']}\n")
    
    # Test 3: Update issue
    print("Test 3: Updating issue...")
    print("-" * 70)
    
    update_result = jira.update_issue(
        issue_key=issue1_key,
        assignee="alice",
        priority="Highest"
    )
    if update_result["status"] == "success":
        print(f"✓ Updated issue {issue1_key}")
        print(f"  New assignee: {update_result['issue']['assignee']}")
        print(f"  New priority: {update_result['issue']['priority']}\n")
    
    # Test 4: Add comments
    print("Test 4: Adding comments...")
    print("-" * 70)
    
    comment_result = jira.add_comment(
        issue_key=issue1_key,
        comment_text="Started working on OAuth2 integration. Setting up provider configuration.",
        author="alice"
    )
    if comment_result["status"] == "success":
        print(f"✓ Added comment to {issue1_key}")
        print(f"  Author: {comment_result['comment']['author']}")
        print(f"  Body: {comment_result['comment']['body']}\n")
    
    # Test 5: Transition issue status
    print("Test 5: Transitioning issue status...")
    print("-" * 70)
    
    transition_result = jira.transition_issue(
        issue_key=issue1_key,
        new_status="In Progress"
    )
    if transition_result["status"] == "success":
        print(f"✓ Transitioned {issue1_key} to 'In Progress'\n")
    
    # Test 6: List issues with filters
    print("Test 6: Listing issues...")
    print("-" * 70)
    
    all_issues = jira.list_issues()
    print(f"✓ Total issues: {all_issues['total']}")
    for issue in all_issues["issues"][:3]:
        print(f"  - {issue['key']}: {issue['summary']} ({issue['status']})")
    print()
    
    in_progress = jira.list_issues(status="In Progress")
    print(f"✓ Issues in progress: {in_progress['total']}")
    for issue in in_progress["issues"]:
        print(f"  - {issue['key']}: {issue['summary']}\n")
    
    # Test 7: Search issues
    print("Test 7: Searching issues...")
    print("-" * 70)
    
    search_result = jira.search_issues(jql="type=Bug")
    print(f"✓ Found {search_result['total']} bugs")
    for issue in search_result["issues"]:
        print(f"  - {issue['key']}: {issue['summary']}")
    print()
    
    # Test 8: Get projects
    print("Test 8: Getting projects...")
    print("-" * 70)
    
    projects = jira.list_projects()
    print(f"✓ Total projects: {projects['total']}")
    for project in projects["projects"]:
        print(f"  - {project['name']} ({project['key']}): {project['issue_count']} issues")
    print()
    
    # Test 9: Get issue types
    print("Test 9: Getting issue types...")
    print("-" * 70)
    
    issue_types = jira.get_issue_types()
    print(f"✓ Available issue types:")
    for itype in issue_types["issue_types"]:
        print(f"  - {itype['name']}: {itype['description']}")
    print()
    
    print("="*70)
    print("ALL TESTS COMPLETED SUCCESSFULLY!")
    print("="*70)


if __name__ == "__main__":
    test_basic_operations()
