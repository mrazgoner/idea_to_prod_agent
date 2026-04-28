"""
Example usage of the GitHub MCP Server

This script demonstrates how to use the GitHubMCPServer for various operations.
"""

from pathlib import Path
from idea_to_prod.mcp_servers import GitHubConfig, GitHubMCPServer


def main():
    """Run example GitHub MCP operations"""
    
    # Initialize server with stub mode
    config = GitHubConfig(
        mode="stub",
        github_username="demo-user",
        github_owner="demo-org",
        enable_logging=True,
        log_level="INFO",
    )
    
    server = GitHubMCPServer(config)
    
    print("=" * 80)
    print("GitHub MCP Server - Example Usage")
    print("=" * 80)
    
    # =========================================================================
    # Repository Operations
    # =========================================================================
    print("\n[1] Creating Repositories...")
    print("-" * 80)
    
    repo1 = server.create_repository(
        name="ai-project",
        owner="demo-org",
        description="An AI project for production",
        language="Python",
        topics=["ai", "machine-learning", "python"]
    )
    print(f"✓ Created: {repo1['repository']['name']}")
    print(f"  URL: {repo1['repository']['url']}")
    
    repo2 = server.create_repository(
        name="web-app",
        owner="demo-org",
        description="A web application",
        language="JavaScript",
        topics=["web", "react"]
    )
    print(f"✓ Created: {repo2['repository']['name']}")
    
    # =========================================================================
    # List Repositories
    # =========================================================================
    print("\n[2] Listing Repositories...")
    print("-" * 80)
    
    repos = server.list_repositories(owner="demo-org")
    print(f"✓ Found {repos['total']} repositories:")
    for repo in repos['repositories']:
        print(f"  - {repo['name']}: {repo['description']}")
    
    # =========================================================================
    # Issue Management
    # =========================================================================
    print("\n[3] Creating Issues...")
    print("-" * 80)
    
    issue1 = server.create_issue(
        repository="demo-org/ai-project",
        title="Add data preprocessing module",
        body="Need to add a data preprocessing module to handle input data normalization.",
        author="alice-dev",
        labels=["feature", "enhancement"]
    )
    print(f"✓ Created issue #{issue1['issue']['number']}: {issue1['issue']['title']}")
    
    issue2 = server.create_issue(
        repository="demo-org/ai-project",
        title="Bug: Model training crashes on large datasets",
        body="The model training process crashes when processing datasets larger than 100GB.",
        author="bob-dev",
        labels=["bug", "critical"]
    )
    print(f"✓ Created issue #{issue2['issue']['number']}: {issue2['issue']['title']}")
    
    # =========================================================================
    # Get Single Issue
    # =========================================================================
    print("\n[4] Retrieving Issue Details...")
    print("-" * 80)
    
    issue_detail = server.get_issue(repository="demo-org/ai-project", issue_number=1)
    issue = issue_detail['issue']
    print(f"✓ Issue #{issue['number']}: {issue['title']}")
    print(f"  State: {issue['state']}")
    print(f"  Author: {issue['author']}")
    print(f"  Labels: {', '.join(issue['labels'])}")
    
    # =========================================================================
    # Add Comments to Issue
    # =========================================================================
    print("\n[5] Adding Comments to Issue...")
    print("-" * 80)
    
    comment1 = server.add_comment(
        repository="demo-org/ai-project",
        issue_number=1,
        body="Great idea! I can help with this. Let me start working on it.",
        author="alice-dev"
    )
    print(f"✓ Added comment by {comment1['comment']['author']}")
    
    comment2 = server.add_comment(
        repository="demo-org/ai-project",
        issue_number=1,
        body="Thanks! Please check the design document at /docs/preprocessing.md",
        author="bob-dev"
    )
    print(f"✓ Added reply comment by {comment2['comment']['author']}")
    
    # =========================================================================
    # Update Issue
    # =========================================================================
    print("\n[6] Updating Issue...")
    print("-" * 80)
    
    updated = server.update_issue(
        repository="demo-org/ai-project",
        issue_number=2,
        state="in_progress",
        assignee="alice-dev"
    )
    print(f"✓ Updated issue #{updated['issue']['number']}")
    print(f"  New state: {updated['issue']['state']}")
    print(f"  Assigned to: {updated['issue']['assignee']}")
    
    # =========================================================================
    # List Issues
    # =========================================================================
    print("\n[7] Listing Issues...")
    print("-" * 80)
    
    all_issues = server.list_issues(
        repository="demo-org/ai-project",
        state="all"
    )
    print(f"✓ Found {all_issues['total']} total issues:")
    for issue in all_issues['issues']:
        print(f"  - #{issue['number']}: {issue['title']} ({issue['state']})")
    
    # =========================================================================
    # Branch Management
    # =========================================================================
    print("\n[8] Managing Branches...")
    print("-" * 80)
    
    # Create a branch
    branch_create = server.create_branch(
        repository="demo-org/ai-project",
        branch_name="feature/preprocessing",
        base_branch="main"
    )
    print(f"✓ Created branch: {branch_create['branch']}")
    
    branch_create = server.create_branch(
        repository="demo-org/ai-project",
        branch_name="bugfix/large-dataset",
        base_branch="main"
    )
    print(f"✓ Created branch: {branch_create['branch']}")
    
    # List branches
    branches = server.list_branches("demo-org/ai-project")
    print(f"✓ Repository branches ({branches['total']}):")
    for branch in branches['branches']:
        print(f"  - {branch}")
    
    # =========================================================================
    # Pull Request Operations
    # =========================================================================
    print("\n[9] Creating Pull Requests...")
    print("-" * 80)
    
    pr1 = server.create_pull_request(
        repository="demo-org/ai-project",
        title="Feature: Add data preprocessing module",
        head_branch="feature/preprocessing",
        base_branch="main",
        body="This PR adds the new data preprocessing module as requested in issue #1.\n\nChanges:\n- Add preprocessing.py\n- Add unit tests\n- Update documentation",
        author="alice-dev"
    )
    print(f"✓ Created PR #{pr1['pull_request']['number']}: {pr1['pull_request']['title']}")
    print(f"  From: {pr1['pull_request']['head_branch']} → {pr1['pull_request']['base_branch']}")
    
    # =========================================================================
    # Get Pull Request
    # =========================================================================
    print("\n[10] Retrieving Pull Request...")
    print("-" * 80)
    
    pr_detail = server.get_pull_request(repository="demo-org/ai-project", pr_number=1)
    pr = pr_detail['pull_request']
    print(f"✓ PR #{pr['number']}: {pr['title']}")
    print(f"  State: {pr['state']}")
    print(f"  Author: {pr['author']}")
    
    # =========================================================================
    # List Pull Requests
    # =========================================================================
    print("\n[11] Listing Pull Requests...")
    print("-" * 80)
    
    prs = server.list_pull_requests(
        repository="demo-org/ai-project",
        state="all"
    )
    print(f"✓ Found {prs['total']} total pull requests:")
    for pr in prs['pull_requests']:
        print(f"  - #{pr['number']}: {pr['title']} ({pr['state']})")
    
    # =========================================================================
    # Add Comment to PR
    # =========================================================================
    print("\n[12] Adding Comment to PR...")
    print("-" * 80)
    
    # Note: This is a method extension that could be added
    # For now, using the issue comment method on PR issue
    print("✓ PR review comments can be added via code review system")
    
    print("\n" + "=" * 80)
    print("GitHub MCP Server Examples Completed Successfully!")
    print("=" * 80)
    
    # Show summary
    print("\n[Summary]")
    print(f"- Created {len(repos['repositories'])} repositories")
    print(f"- Created {len(all_issues['issues'])} issues")
    print(f"- Created {len(prs['pull_requests'])} pull requests")
    print(f"- Created {branches['total'] - 1} branches (+ main)")


if __name__ == "__main__":
    main()
