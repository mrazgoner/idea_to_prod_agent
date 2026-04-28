"""
Unit tests for GitHub MCP Server

Tests cover all major operations including repositories, issues, PRs, and branches.
"""

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from idea_to_prod.mcp_servers import GitHubConfig, GitHubMCPServer


class TestGitHubMCPServer(unittest.TestCase):
    """Test cases for GitHub MCP Server"""
    
    def setUp(self):
        """Set up test fixtures"""
        self.temp_dir = TemporaryDirectory()
        self.config = GitHubConfig(
            mode="stub",
            storage_dir=Path(self.temp_dir.name),
            enable_logging=False,
        )
        self.server = GitHubMCPServer(self.config)
    
    def tearDown(self):
        """Clean up test fixtures"""
        self.temp_dir.cleanup()
    
    # =========================================================================
    # Repository Tests
    # =========================================================================
    
    def test_create_repository(self):
        """Test repository creation"""
        result = self.server.create_repository(
            name="test-repo",
            owner="test-org",
            description="Test repository",
            language="Python"
        )
        
        self.assertTrue(result["success"])
        self.assertIn("repository", result)
        self.assertEqual(result["repository"]["name"], "test-repo")
        self.assertEqual(result["repository"]["owner"], "test-org")
    
    def test_create_duplicate_repository(self):
        """Test that creating duplicate repository fails"""
        self.server.create_repository(
            name="test-repo",
            owner="test-org",
            description="Test repository"
        )
        
        result = self.server.create_repository(
            name="test-repo",
            owner="test-org",
            description="Duplicate repository"
        )
        
        self.assertFalse(result["success"])
        self.assertIn("error", result)
    
    def test_get_repository(self):
        """Test getting repository information"""
        created = self.server.create_repository(
            name="my-repo",
            owner="my-org"
        )
        
        result = self.server.get_repository(
            owner="my-org",
            name="my-repo"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["repository"]["id"], created["repository"]["id"])
    
    def test_get_nonexistent_repository(self):
        """Test getting non-existent repository returns error"""
        result = self.server.get_repository(
            owner="nonexistent",
            name="repo"
        )
        
        self.assertFalse(result["success"])
    
    def test_list_repositories(self):
        """Test listing repositories"""
        self.server.create_repository(name="repo1", owner="org1")
        self.server.create_repository(name="repo2", owner="org1")
        self.server.create_repository(name="repo3", owner="org2")
        
        result = self.server.list_repositories(owner="org1")
        
        self.assertTrue(result["success"])
        self.assertEqual(result["total"], 2)
    
    def test_list_all_repositories(self):
        """Test listing all repositories"""
        self.server.create_repository(name="repo1", owner="org1")
        self.server.create_repository(name="repo2", owner="org2")
        
        result = self.server.list_repositories()
        
        self.assertTrue(result["success"])
        self.assertEqual(result["total"], 2)
    
    # =========================================================================
    # Issue Tests
    # =========================================================================
    
    def test_create_issue(self):
        """Test issue creation"""
        result = self.server.create_issue(
            repository="test-org/test-repo",
            title="Test issue",
            body="Test description",
            author="test-author",
            labels=["test", "bug"]
        )
        
        self.assertTrue(result["success"])
        self.assertIn("issue", result)
        self.assertEqual(result["issue"]["number"], 1)
        self.assertEqual(result["issue"]["title"], "Test issue")
    
    def test_issue_auto_numbering(self):
        """Test that issues are auto-numbered"""
        self.server.create_issue(
            repository="test-org/test-repo",
            title="Issue 1"
        )
        issue2 = self.server.create_issue(
            repository="test-org/test-repo",
            title="Issue 2"
        )
        
        self.assertEqual(issue2["issue"]["number"], 2)
    
    def test_get_issue(self):
        """Test getting issue"""
        created = self.server.create_issue(
            repository="test-org/test-repo",
            title="Test issue"
        )
        
        result = self.server.get_issue(
            repository="test-org/test-repo",
            issue_number=created["issue"]["number"]
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["issue"]["title"], "Test issue")
    
    def test_get_nonexistent_issue(self):
        """Test getting non-existent issue returns error"""
        result = self.server.get_issue(
            repository="test-org/test-repo",
            issue_number=999
        )
        
        self.assertFalse(result["success"])
    
    def test_list_issues(self):
        """Test listing issues"""
        self.server.create_issue(
            repository="test-org/test-repo",
            title="Open issue 1",
            state="open"
        )
        self.server.create_issue(
            repository="test-org/test-repo",
            title="Open issue 2",
            state="open"
        )
        
        result = self.server.list_issues(
            repository="test-org/test-repo",
            state="open"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["total"], 2)
    
    def test_update_issue(self):
        """Test updating issue"""
        self.server.create_issue(
            repository="test-org/test-repo",
            title="Original title"
        )
        
        result = self.server.update_issue(
            repository="test-org/test-repo",
            issue_number=1,
            title="Updated title",
            state="closed"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["issue"]["title"], "Updated title")
        self.assertEqual(result["issue"]["state"], "closed")
    
    def test_add_comment(self):
        """Test adding comment to issue"""
        self.server.create_issue(
            repository="test-org/test-repo",
            title="Test issue"
        )
        
        result = self.server.add_comment(
            repository="test-org/test-repo",
            issue_number=1,
            body="Test comment",
            author="commenter"
        )
        
        self.assertTrue(result["success"])
        self.assertIn("comment", result)
        self.assertEqual(result["comment"]["body"], "Test comment")
    
    def test_comment_appears_in_issue(self):
        """Test that comment appears when retrieving issue"""
        self.server.create_issue(
            repository="test-org/test-repo",
            title="Test issue"
        )
        self.server.add_comment(
            repository="test-org/test-repo",
            issue_number=1,
            body="Comment 1"
        )
        self.server.add_comment(
            repository="test-org/test-repo",
            issue_number=1,
            body="Comment 2"
        )
        
        result = self.server.get_issue(
            repository="test-org/test-repo",
            issue_number=1
        )
        
        self.assertEqual(len(result["issue"]["comments"]), 2)
    
    def test_add_comment_too_long(self):
        """Test that oversized comments are rejected"""
        self.server.create_issue(
            repository="test-org/test-repo",
            title="Test issue"
        )
        
        long_comment = "x" * (self.config.max_comment_length + 1)
        result = self.server.add_comment(
            repository="test-org/test-repo",
            issue_number=1,
            body=long_comment
        )
        
        self.assertFalse(result["success"])
    
    # =========================================================================
    # Pull Request Tests
    # =========================================================================
    
    def test_create_pull_request(self):
        """Test PR creation"""
        result = self.server.create_pull_request(
            repository="test-org/test-repo",
            title="Test PR",
            head_branch="feature/test",
            base_branch="main",
            body="Test PR description",
            author="test-author"
        )
        
        self.assertTrue(result["success"])
        self.assertIn("pull_request", result)
        self.assertEqual(result["pull_request"]["number"], 1)
        self.assertEqual(result["pull_request"]["title"], "Test PR")
    
    def test_pr_auto_numbering(self):
        """Test that PRs are auto-numbered"""
        self.server.create_pull_request(
            repository="test-org/test-repo",
            title="PR 1",
            head_branch="feature/1",
            base_branch="main"
        )
        pr2 = self.server.create_pull_request(
            repository="test-org/test-repo",
            title="PR 2",
            head_branch="feature/2",
            base_branch="main"
        )
        
        self.assertEqual(pr2["pull_request"]["number"], 2)
    
    def test_get_pull_request(self):
        """Test getting PR"""
        created = self.server.create_pull_request(
            repository="test-org/test-repo",
            title="Test PR",
            head_branch="feature/test",
            base_branch="main"
        )
        
        result = self.server.get_pull_request(
            repository="test-org/test-repo",
            pr_number=created["pull_request"]["number"]
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["pull_request"]["title"], "Test PR")
    
    def test_list_pull_requests(self):
        """Test listing PRs"""
        self.server.create_pull_request(
            repository="test-org/test-repo",
            title="PR 1",
            head_branch="feature/1",
            base_branch="main"
        )
        self.server.create_pull_request(
            repository="test-org/test-repo",
            title="PR 2",
            head_branch="feature/2",
            base_branch="main"
        )
        
        result = self.server.list_pull_requests(
            repository="test-org/test-repo",
            state="all"
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["total"], 2)
    
    # =========================================================================
    # Branch Tests
    # =========================================================================
    
    def test_list_branches_default(self):
        """Test that new repositories have main branch"""
        self.server.create_repository(
            name="test-repo",
            owner="test-org"
        )
        
        result = self.server.list_branches("test-org/test-repo")
        
        self.assertTrue(result["success"])
        self.assertIn("main", result["branches"])
    
    def test_create_branch(self):
        """Test branch creation"""
        self.server.create_repository(
            name="test-repo",
            owner="test-org"
        )
        
        result = self.server.create_branch(
            repository="test-org/test-repo",
            branch_name="feature/test",
            base_branch="main"
        )
        
        self.assertTrue(result["success"])
    
    def test_branch_appears_in_list(self):
        """Test that created branch appears in list"""
        self.server.create_repository(
            name="test-repo",
            owner="test-org"
        )
        self.server.create_branch(
            repository="test-org/test-repo",
            branch_name="feature/test"
        )
        
        result = self.server.list_branches("test-org/test-repo")
        
        self.assertIn("feature/test", result["branches"])
    
    def test_create_duplicate_branch(self):
        """Test that duplicate branch creation fails"""
        self.server.create_repository(
            name="test-repo",
            owner="test-org"
        )
        self.server.create_branch(
            repository="test-org/test-repo",
            branch_name="feature/test"
        )
        
        result = self.server.create_branch(
            repository="test-org/test-repo",
            branch_name="feature/test"
        )
        
        self.assertFalse(result["success"])
    
    # =========================================================================
    # Storage Tests
    # =========================================================================
    
    def test_data_persistence(self):
        """Test that data is persisted to storage"""
        self.server.create_repository(
            name="test-repo",
            owner="test-org"
        )
        self.server.create_issue(
            repository="test-org/test-repo",
            title="Test issue"
        )
        
        # Create new server instance with same storage
        server2 = GitHubMCPServer(self.config)
        
        result = server2.get_issue(
            repository="test-org/test-repo",
            issue_number=1
        )
        
        self.assertTrue(result["success"])
        self.assertEqual(result["issue"]["title"], "Test issue")


class TestGitHubConfig(unittest.TestCase):
    """Test cases for GitHub configuration"""
    
    def test_default_config(self):
        """Test default configuration"""
        config = GitHubConfig()
        
        self.assertEqual(config.name, "github-mcp")
        self.assertEqual(config.mode, "stub")
        self.assertTrue(config.enable_logging)
    
    def test_config_to_dict(self):
        """Test configuration serialization"""
        config = GitHubConfig(mode="stub")
        config_dict = config.to_dict()
        
        self.assertIsInstance(config_dict, dict)
        self.assertEqual(config_dict["name"], "github-mcp")
        self.assertEqual(config_dict["mode"], "stub")
    
    def test_invalid_mode(self):
        """Test that invalid mode raises error"""
        with self.assertRaises(ValueError):
            GitHubConfig(mode="invalid")


if __name__ == "__main__":
    unittest.main()
