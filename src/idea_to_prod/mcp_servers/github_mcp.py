"""
GitHub MCP Server
A configurable Model Context Protocol server for GitHub operations.
Supports both 'stub' mode for testing and 'api' mode for real GitHub API integration.
"""

import json
import logging
from datetime import datetime
from typing import Any, Optional, Dict, List
from dataclasses import dataclass, asdict, field
import uuid

# Handle both relative and absolute imports
try:
    from .config.github_config import GitHubConfig, create_config
except ImportError:
    from config.github_config import GitHubConfig, create_config

# Import PyGithub for real API operations
try:
    from github import Github, GithubException
    PYGITHUB_AVAILABLE = True
except ImportError:
    PYGITHUB_AVAILABLE = False


@dataclass
class GitHubRepository:
    """Represents a GitHub repository"""
    id: str
    name: str
    owner: str
    description: Optional[str] = None
    url: str = ""
    is_private: bool = False
    stars: int = 0
    forks: int = 0
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    language: Optional[str] = None
    topics: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert repository to dictionary"""
        return {
            "id": self.id,
            "name": self.name,
            "owner": self.owner,
            "description": self.description,
            "url": self.url,
            "is_private": self.is_private,
            "stars": self.stars,
            "forks": self.forks,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "language": self.language,
            "topics": self.topics,
        }


@dataclass
class GitHubIssue:
    """Represents a GitHub issue"""
    id: str
    number: int
    title: str
    body: Optional[str] = None
    state: str = "open"
    repository: str = ""
    author: Optional[str] = None
    assignee: Optional[str] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    labels: List[str] = field(default_factory=list)
    comments: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert issue to dictionary"""
        return {
            "id": self.id,
            "number": self.number,
            "title": self.title,
            "body": self.body,
            "state": self.state,
            "repository": self.repository,
            "author": self.author,
            "assignee": self.assignee,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "labels": self.labels,
            "comments": self.comments,
        }


@dataclass
class GitHubPullRequest:
    """Represents a GitHub pull request"""
    id: str
    number: int
    title: str
    body: Optional[str] = None
    state: str = "open"
    repository: str = ""
    author: Optional[str] = None
    head_branch: str = ""
    base_branch: str = ""
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    merged_at: Optional[str] = None
    comments: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert pull request to dictionary"""
        return {
            "id": self.id,
            "number": self.number,
            "title": self.title,
            "body": self.body,
            "state": self.state,
            "repository": self.repository,
            "author": self.author,
            "head_branch": self.head_branch,
            "base_branch": self.base_branch,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "merged_at": self.merged_at,
            "comments": self.comments,
        }


class GitHubMCPServer:
    """
    MCP Server for GitHub operations.
    Stub implementation that stores data locally in JSON format.
    Can be extended to support real GitHub API.
    """
    
    def __init__(self, config: Optional[GitHubConfig] = None):
        """
        Initialize GitHub MCP Server
        
        Args:
            config: GitHubConfig instance. If None, uses default config.
        """
        self.config = config or GitHubConfig()
        self._setup_logging()
        self.logger.info(f"Initializing {self.config.name} v{self.config.version}")
        self.logger.info(f"Mode: {self.config.mode}, Storage: {self.config.storage_dir}")
        
        # Initialize API client if in 'api' mode
        self.gh = None
        if self.config.mode == "api":
            if not PYGITHUB_AVAILABLE:
                raise ImportError("PyGithub is required for 'api' mode. Install with: pip install PyGithub")
            
            if not self.config.github_token:
                raise ValueError("github_token is required for API mode")
            
            try:
                self.gh = Github(self.config.github_token)
                # Verify token is valid
                self.gh.get_user().login
                self.logger.info("GitHub API client initialized successfully")
            except GithubException as e:
                self.logger.error(f"Failed to authenticate with GitHub: {e}")
                raise
        
        # In-memory store for stub mode
        self.repositories: Dict[str, GitHubRepository] = {}
        self.issues: Dict[str, GitHubIssue] = {}
        self.pull_requests: Dict[str, GitHubPullRequest] = {}
        self.branches: Dict[str, List[str]] = {}
        
        # Load data from storage if available (stub mode only)
        if self.config.mode == "stub":
            self._load_from_storage()
    
    def _setup_logging(self):
        """Configure logging based on config settings"""
        self.logger = logging.getLogger(self.config.name)
        
        if self.config.enable_logging:
            handler = logging.StreamHandler()
            formatter = logging.Formatter(
                "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
            )
            handler.setFormatter(formatter)
            self.logger.addHandler(handler)
            self.logger.setLevel(self.config.log_level)
        else:
            self.logger.addHandler(logging.NullHandler())
    
    def _load_from_storage(self):
        """Load repositories, issues, and PRs from local storage"""
        try:
            repos_file = self.config.storage_dir / "repositories.json"
            if repos_file.exists():
                with open(repos_file, 'r') as f:
                    repos_data = json.load(f)
                    for repo_id, repo_data in repos_data.items():
                        self.repositories[repo_id] = GitHubRepository(**repo_data)
                self.logger.info(f"Loaded {len(self.repositories)} repositories")
            
            issues_file = self.config.storage_dir / "issues.json"
            if issues_file.exists():
                with open(issues_file, 'r') as f:
                    issues_data = json.load(f)
                    for issue_id, issue_data in issues_data.items():
                        self.issues[issue_id] = GitHubIssue(**issue_data)
                self.logger.info(f"Loaded {len(self.issues)} issues")
            
            prs_file = self.config.storage_dir / "pull_requests.json"
            if prs_file.exists():
                with open(prs_file, 'r') as f:
                    prs_data = json.load(f)
                    for pr_id, pr_data in prs_data.items():
                        self.pull_requests[pr_id] = GitHubPullRequest(**pr_data)
                self.logger.info(f"Loaded {len(self.pull_requests)} pull requests")
            
            branches_file = self.config.storage_dir / "branches.json"
            if branches_file.exists():
                with open(branches_file, 'r') as f:
                    self.branches = json.load(f)
                self.logger.info(f"Loaded branches for {len(self.branches)} repositories")
        
        except Exception as e:
            self.logger.warning(f"Failed to load data from storage: {e}")
    
    def _save_to_storage(self):
        """Save repositories, issues, and PRs to local storage"""
        try:
            # Save repositories
            repos_file = self.config.storage_dir / "repositories.json"
            repos_data = {
                repo_id: repo.to_dict()
                for repo_id, repo in self.repositories.items()
            }
            with open(repos_file, 'w') as f:
                json.dump(repos_data, f, indent=2)
            
            # Save issues
            issues_file = self.config.storage_dir / "issues.json"
            issues_data = {
                issue_id: issue.to_dict()
                for issue_id, issue in self.issues.items()
            }
            with open(issues_file, 'w') as f:
                json.dump(issues_data, f, indent=2)
            
            # Save pull requests
            prs_file = self.config.storage_dir / "pull_requests.json"
            prs_data = {
                pr_id: pr.to_dict()
                for pr_id, pr in self.pull_requests.items()
            }
            with open(prs_file, 'w') as f:
                json.dump(prs_data, f, indent=2)
            
            # Save branches
            branches_file = self.config.storage_dir / "branches.json"
            with open(branches_file, 'w') as f:
                json.dump(self.branches, f, indent=2)
        
        except Exception as e:
            self.logger.error(f"Failed to save data to storage: {e}")
    
    # =========================================================================
    # Repository Tools
    # =========================================================================
    
    def create_repository(
        self,
        name: str,
        owner: str,
        description: Optional[str] = None,
        is_private: bool = False,
        language: Optional[str] = None,
        topics: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new GitHub repository
        
        Args:
            name: Repository name
            owner: Repository owner (username or organization)
            description: Repository description
            is_private: Whether the repository is private
            language: Primary programming language
            topics: List of topics/tags
        
        Returns:
            Dict with repository info or error
        """
        self.logger.info(f"create_repository: {owner}/{name}")
        
        if self.config.mode == "api":
            return self._api_create_repository(name, owner, description, is_private, language, topics)
        else:
            return self._stub_create_repository(name, owner, description, is_private, language, topics)
    
    def _api_create_repository(
        self,
        name: str,
        owner: str,
        description: Optional[str] = None,
        is_private: bool = False,
        language: Optional[str] = None,
        topics: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Real GitHub API implementation for create_repository"""
        try:
            user = self.gh.get_user(owner)
            
            # Create repository using the API
            repo = user.create_repo(
                name=name,
                description=description,
                private=is_private,
                auto_init=True,
            )
            
            # Set topics if provided
            if topics:
                repo.edit(topics=topics)
            
            self.logger.info(f"Repository created via API: {owner}/{name}")
            
            return {
                "success": True,
                "repository": {
                    "id": str(repo.id),
                    "name": repo.name,
                    "owner": repo.owner.login,
                    "description": repo.description,
                    "url": repo.html_url,
                    "is_private": repo.private,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "created_at": repo.created_at.isoformat(),
                    "updated_at": repo.updated_at.isoformat(),
                    "language": repo.language,
                    "topics": repo.get_topics(),
                },
            }
        except GithubException as e:
            self.logger.error(f"GitHub API error creating repository: {e}")
            return {
                "success": False,
                "error": f"GitHub API error: {str(e)}",
            }
        except Exception as e:
            self.logger.error(f"Error creating repository via API: {e}")
            return {"success": False, "error": str(e)}
    
    def _stub_create_repository(
        self,
        name: str,
        owner: str,
        description: Optional[str] = None,
        is_private: bool = False,
        language: Optional[str] = None,
        topics: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Stub implementation for create_repository"""
        try:
            # Check if repository already exists
            repo_key = f"{owner}/{name}".lower()
            if any(
                f"{repo.owner}/{repo.name}".lower() == repo_key
                for repo in self.repositories.values()
            ):
                return {
                    "success": False,
                    "error": f"Repository {repo_key} already exists",
                }
            
            # Create repository
            repo_id = str(uuid.uuid4())
            now = datetime.utcnow().isoformat() + "Z"
            repo = GitHubRepository(
                id=repo_id,
                name=name,
                owner=owner,
                description=description,
                url=f"https://github.com/{owner}/{name}",
                is_private=is_private,
                created_at=now,
                updated_at=now,
                language=language,
                topics=topics or [],
            )
            
            self.repositories[repo_id] = repo
            self.branches[repo_key] = ["main"]  # Default branch
            self._save_to_storage()
            
            return {
                "success": True,
                "repository": repo.to_dict(),
            }
        
        except Exception as e:
            self.logger.error(f"Error creating repository: {e}")
            return {"success": False, "error": str(e)}
    
    def get_repository(self, owner: str, name: str) -> Dict[str, Any]:
        """
        Get repository information
        
        Args:
            owner: Repository owner
            name: Repository name
        
        Returns:
            Dict with repository info or error
        """
        self.logger.info(f"get_repository: {owner}/{name}")
        
        if self.config.mode == "api":
            return self._api_get_repository(owner, name)
        else:
            return self._stub_get_repository(owner, name)
    
    def _api_get_repository(self, owner: str, name: str) -> Dict[str, Any]:
        """Real GitHub API implementation for get_repository"""
        try:
            repo = self.gh.get_user(owner).get_repo(name)
            
            return {
                "success": True,
                "repository": {
                    "id": str(repo.id),
                    "name": repo.name,
                    "owner": repo.owner.login,
                    "description": repo.description,
                    "url": repo.html_url,
                    "is_private": repo.private,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "created_at": repo.created_at.isoformat(),
                    "updated_at": repo.updated_at.isoformat(),
                    "language": repo.language,
                    "topics": repo.get_topics(),
                },
            }
        except GithubException as e:
            self.logger.error(f"GitHub API error getting repository: {e}")
            return {
                "success": False,
                "error": f"GitHub API error: {str(e)}",
            }
        except Exception as e:
            self.logger.error(f"Error getting repository via API: {e}")
            return {"success": False, "error": str(e)}
    
    def _stub_get_repository(self, owner: str, name: str) -> Dict[str, Any]:
        """Stub implementation for get_repository"""
        try:
            repo_key = f"{owner}/{name}".lower()
            for repo in self.repositories.values():
                if f"{repo.owner}/{repo.name}".lower() == repo_key:
                    return {
                        "success": True,
                        "repository": repo.to_dict(),
                    }
            
            return {
                "success": False,
                "error": f"Repository {repo_key} not found",
            }
        
        except Exception as e:
            self.logger.error(f"Error getting repository: {e}")
            return {"success": False, "error": str(e)}
    
    def list_repositories(
        self,
        owner: Optional[str] = None,
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        List repositories
        
        Args:
            owner: Optional owner filter
            limit: Maximum number of repositories to return
        
        Returns:
            Dict with list of repositories
        """
        self.logger.info(f"list_repositories: owner={owner}, limit={limit}")
        
        if self.config.mode == "api":
            return self._api_list_repositories(owner, limit)
        else:
            return self._stub_list_repositories(owner, limit)
    
    def _api_list_repositories(self, owner: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """Real GitHub API implementation for list_repositories"""
        try:
            if owner:
                repos = self.gh.get_user(owner).get_repos()
            else:
                repos = self.gh.get_user().get_repos()
            
            repo_list = []
            for repo in repos:
                repo_list.append({
                    "id": str(repo.id),
                    "name": repo.name,
                    "owner": repo.owner.login,
                    "description": repo.description,
                    "url": repo.html_url,
                    "is_private": repo.private,
                    "stars": repo.stargazers_count,
                    "forks": repo.forks_count,
                    "created_at": repo.created_at.isoformat(),
                    "updated_at": repo.updated_at.isoformat(),
                    "language": repo.language,
                    "topics": repo.get_topics(),
                })
                if len(repo_list) >= limit:
                    break
            
            return {
                "success": True,
                "repositories": repo_list,
                "total": len(repo_list),
            }
        except GithubException as e:
            self.logger.error(f"GitHub API error listing repositories: {e}")
            return {
                "success": False,
                "error": f"GitHub API error: {str(e)}",
            }
        except Exception as e:
            self.logger.error(f"Error listing repositories via API: {e}")
            return {"success": False, "error": str(e)}
    
    def _stub_list_repositories(self, owner: Optional[str] = None, limit: int = 100) -> Dict[str, Any]:
        """Stub implementation for list_repositories"""
        try:
            repos = list(self.repositories.values())
            
            if owner:
                repos = [r for r in repos if r.owner.lower() == owner.lower()]
            
            repos = repos[:limit]
            
            return {
                "success": True,
                "repositories": [r.to_dict() for r in repos],
                "total": len(repos),
            }
        
        except Exception as e:
            self.logger.error(f"Error listing repositories: {e}")
            return {"success": False, "error": str(e)}
    
    # =========================================================================
    # Issue Tools
    # =========================================================================
    
    def create_issue(
        self,
        repository: str,
        title: str,
        body: Optional[str] = None,
        author: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new GitHub issue
        
        Args:
            repository: Repository identifier (owner/name)
            title: Issue title
            body: Issue body/description
            author: Issue author username
            labels: List of labels
        
        Returns:
            Dict with issue info or error
        """
        self.logger.info(f"create_issue: {repository}")
        
        if self.config.mode == "api":
            return self._api_create_issue(repository, title, body, author, labels)
        else:
            return self._stub_create_issue(repository, title, body, author, labels)
    
    def _api_create_issue(
        self,
        repository: str,
        title: str,
        body: Optional[str] = None,
        author: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Real GitHub API implementation for create_issue"""
        try:
            owner, repo_name = repository.split('/')
            repo = self.gh.get_user(owner).get_repo(repo_name)
            
            # Create issue
            issue = repo.create_issue(
                title=title,
                body=body or "",
                labels=labels or [],
            )
            
            self.logger.info(f"Issue created via API: {repository}#{issue.number}")
            
            return {
                "success": True,
                "issue": {
                    "id": str(issue.id),
                    "number": issue.number,
                    "title": issue.title,
                    "body": issue.body,
                    "state": issue.state,
                    "repository": repository,
                    "author": issue.user.login,
                    "assignee": issue.assignee.login if issue.assignee else None,
                    "created_at": issue.created_at.isoformat(),
                    "updated_at": issue.updated_at.isoformat(),
                    "labels": [label.name for label in issue.labels],
                    "comments": [],
                },
            }
        except GithubException as e:
            self.logger.error(f"GitHub API error creating issue: {e}")
            return {
                "success": False,
                "error": f"GitHub API error: {str(e)}",
            }
        except Exception as e:
            self.logger.error(f"Error creating issue via API: {e}")
            return {"success": False, "error": str(e)}
    
    def _stub_create_issue(
        self,
        repository: str,
        title: str,
        body: Optional[str] = None,
        author: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Stub implementation for create_issue"""
        try:
            issue_id = str(uuid.uuid4())
            issue_number = len([i for i in self.issues.values() if i.repository == repository]) + 1
            now = datetime.utcnow().isoformat() + "Z"
            
            issue = GitHubIssue(
                id=issue_id,
                number=issue_number,
                title=title,
                body=body,
                repository=repository,
                author=author,
                created_at=now,
                updated_at=now,
                labels=labels or [],
            )
            
            self.issues[issue_id] = issue
            self._save_to_storage()
            
            return {
                "success": True,
                "issue": issue.to_dict(),
            }
        
        except Exception as e:
            self.logger.error(f"Error creating issue: {e}")
            return {"success": False, "error": str(e)}
    
    def get_issue(self, repository: str, issue_number: int) -> Dict[str, Any]:
        """
        Get issue information
        
        Args:
            repository: Repository identifier (owner/name)
            issue_number: Issue number
        
        Returns:
            Dict with issue info or error
        """
        self.logger.info(f"get_issue: {repository}#{issue_number}")
        
        if self.config.mode == "api":
            return self._api_get_issue(repository, issue_number)
        else:
            return self._stub_get_issue(repository, issue_number)
    
    def _api_get_issue(self, repository: str, issue_number: int) -> Dict[str, Any]:
        """Real GitHub API implementation for get_issue"""
        try:
            owner, repo_name = repository.split('/')
            repo = self.gh.get_user(owner).get_repo(repo_name)
            issue = repo.get_issue(issue_number)
            
            return {
                "success": True,
                "issue": {
                    "id": str(issue.id),
                    "number": issue.number,
                    "title": issue.title,
                    "body": issue.body,
                    "state": issue.state,
                    "repository": repository,
                    "author": issue.user.login,
                    "assignee": issue.assignee.login if issue.assignee else None,
                    "created_at": issue.created_at.isoformat(),
                    "updated_at": issue.updated_at.isoformat(),
                    "labels": [label.name for label in issue.labels],
                    "comments": [],
                },
            }
        except GithubException as e:
            self.logger.error(f"GitHub API error getting issue: {e}")
            return {
                "success": False,
                "error": f"GitHub API error: {str(e)}",
            }
        except Exception as e:
            self.logger.error(f"Error getting issue via API: {e}")
            return {"success": False, "error": str(e)}
    
    def _stub_get_issue(self, repository: str, issue_number: int) -> Dict[str, Any]:
        """Stub implementation for get_issue"""
        try:
            for issue in self.issues.values():
                if issue.repository == repository and issue.number == issue_number:
                    return {
                        "success": True,
                        "issue": issue.to_dict(),
                    }
            
            return {
                "success": False,
                "error": f"Issue #{issue_number} not found in {repository}",
            }
        
        except Exception as e:
            self.logger.error(f"Error getting issue: {e}")
            return {"success": False, "error": str(e)}
    
    def list_issues(
        self,
        repository: str,
        state: str = "open",
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        List issues in a repository
        
        Args:
            repository: Repository identifier (owner/name)
            state: Issue state ('open', 'closed', or 'all')
            limit: Maximum number of issues to return
        
        Returns:
            Dict with list of issues
        """
        self.logger.info(f"list_issues: {repository}, state={state}")
        
        if self.config.mode == "api":
            return self._api_list_issues(repository, state, limit)
        else:
            return self._stub_list_issues(repository, state, limit)
    
    def _api_list_issues(self, repository: str, state: str = "open", limit: int = 100) -> Dict[str, Any]:
        """Real GitHub API implementation for list_issues"""
        try:
            owner, repo_name = repository.split('/')
            repo = self.gh.get_user(owner).get_repo(repo_name)
            
            # Convert state to GitHub API format
            api_state = state if state == "all" else state
            issues = repo.get_issues(state=api_state)
            
            issue_list = []
            for issue in issues:
                issue_list.append({
                    "id": str(issue.id),
                    "number": issue.number,
                    "title": issue.title,
                    "body": issue.body,
                    "state": issue.state,
                    "repository": repository,
                    "author": issue.user.login,
                    "assignee": issue.assignee.login if issue.assignee else None,
                    "created_at": issue.created_at.isoformat(),
                    "updated_at": issue.updated_at.isoformat(),
                    "labels": [label.name for label in issue.labels],
                    "comments": [],
                })
                if len(issue_list) >= limit:
                    break
            
            return {
                "success": True,
                "repository": repository,
                "state": state,
                "issues": issue_list,
                "total": len(issue_list),
            }
        except GithubException as e:
            self.logger.error(f"GitHub API error listing issues: {e}")
            return {
                "success": False,
                "error": f"GitHub API error: {str(e)}",
            }
        except Exception as e:
            self.logger.error(f"Error listing issues via API: {e}")
            return {"success": False, "error": str(e)}
    
    def _stub_list_issues(self, repository: str, state: str = "open", limit: int = 100) -> Dict[str, Any]:
        """Stub implementation for list_issues"""
        try:
            issues = [i for i in self.issues.values() if i.repository == repository]
            
            if state != "all":
                issues = [i for i in issues if i.state == state]
            
            issues = issues[:limit]
            
            return {
                "success": True,
                "repository": repository,
                "state": state,
                "issues": [i.to_dict() for i in issues],
                "total": len(issues),
            }
        
        except Exception as e:
            self.logger.error(f"Error listing issues: {e}")
            return {"success": False, "error": str(e)}
    
    def update_issue(
        self,
        repository: str,
        issue_number: int,
        title: Optional[str] = None,
        body: Optional[str] = None,
        state: Optional[str] = None,
        assignee: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Update an issue
        
        Args:
            repository: Repository identifier (owner/name)
            issue_number: Issue number
            title: New title (optional)
            body: New body (optional)
            state: New state (optional)
            assignee: New assignee (optional)
            labels: New labels (optional)
        
        Returns:
            Dict with updated issue or error
        """
        self.logger.info(f"update_issue: {repository}#{issue_number}")
        
        try:
            for issue in self.issues.values():
                if issue.repository == repository and issue.number == issue_number:
                    if title is not None:
                        issue.title = title
                    if body is not None:
                        issue.body = body
                    if state is not None:
                        issue.state = state
                    if assignee is not None:
                        issue.assignee = assignee
                    if labels is not None:
                        issue.labels = labels
                    
                    issue.updated_at = datetime.utcnow().isoformat() + "Z"
                    self._save_to_storage()
                    
                    return {
                        "success": True,
                        "issue": issue.to_dict(),
                    }
            
            return {
                "success": False,
                "error": f"Issue #{issue_number} not found",
            }
        
        except Exception as e:
            self.logger.error(f"Error updating issue: {e}")
            return {"success": False, "error": str(e)}
    
    def add_comment(
        self,
        repository: str,
        issue_number: int,
        body: str,
        author: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Add a comment to an issue
        
        Args:
            repository: Repository identifier (owner/name)
            issue_number: Issue number
            body: Comment text
            author: Comment author username
        
        Returns:
            Dict with comment info or error
        """
        self.logger.info(f"add_comment: {repository}#{issue_number}")
        
        try:
            if len(body) > self.config.max_comment_length:
                return {
                    "success": False,
                    "error": f"Comment exceeds maximum length of {self.config.max_comment_length}",
                }
            
            for issue in self.issues.values():
                if issue.repository == repository and issue.number == issue_number:
                    comment = {
                        "id": str(uuid.uuid4()),
                        "body": body,
                        "author": author,
                        "created_at": datetime.utcnow().isoformat() + "Z",
                    }
                    issue.comments.append(comment)
                    issue.updated_at = datetime.utcnow().isoformat() + "Z"
                    self._save_to_storage()
                    
                    return {
                        "success": True,
                        "comment": comment,
                    }
            
            return {
                "success": False,
                "error": f"Issue #{issue_number} not found",
            }
        
        except Exception as e:
            self.logger.error(f"Error adding comment: {e}")
            return {"success": False, "error": str(e)}
    
    # =========================================================================
    # Pull Request Tools
    # =========================================================================
    
    def create_pull_request(
        self,
        repository: str,
        title: str,
        head_branch: str,
        base_branch: str = "main",
        body: Optional[str] = None,
        author: Optional[str] = None,
    ) -> Dict[str, Any]:
        """
        Create a new pull request
        
        Args:
            repository: Repository identifier (owner/name)
            title: PR title
            head_branch: Feature branch name
            base_branch: Target branch name (default: main)
            body: PR description
            author: PR author username
        
        Returns:
            Dict with PR info or error
        """
        self.logger.info(f"create_pull_request: {repository}")
        
        try:
            pr_id = str(uuid.uuid4())
            pr_number = len([p for p in self.pull_requests.values() if p.repository == repository]) + 1
            now = datetime.utcnow().isoformat() + "Z"
            
            pr = GitHubPullRequest(
                id=pr_id,
                number=pr_number,
                title=title,
                body=body,
                repository=repository,
                author=author,
                head_branch=head_branch,
                base_branch=base_branch,
                created_at=now,
                updated_at=now,
            )
            
            self.pull_requests[pr_id] = pr
            self._save_to_storage()
            
            return {
                "success": True,
                "pull_request": pr.to_dict(),
            }
        
        except Exception as e:
            self.logger.error(f"Error creating pull request: {e}")
            return {"success": False, "error": str(e)}
    
    def get_pull_request(self, repository: str, pr_number: int) -> Dict[str, Any]:
        """
        Get pull request information
        
        Args:
            repository: Repository identifier (owner/name)
            pr_number: Pull request number
        
        Returns:
            Dict with PR info or error
        """
        self.logger.info(f"get_pull_request: {repository}#{pr_number}")
        
        try:
            for pr in self.pull_requests.values():
                if pr.repository == repository and pr.number == pr_number:
                    return {
                        "success": True,
                        "pull_request": pr.to_dict(),
                    }
            
            return {
                "success": False,
                "error": f"Pull request #{pr_number} not found",
            }
        
        except Exception as e:
            self.logger.error(f"Error getting pull request: {e}")
            return {"success": False, "error": str(e)}
    
    def list_pull_requests(
        self,
        repository: str,
        state: str = "open",
        limit: int = 100,
    ) -> Dict[str, Any]:
        """
        List pull requests in a repository
        
        Args:
            repository: Repository identifier (owner/name)
            state: PR state ('open', 'closed', or 'merged')
            limit: Maximum number of PRs to return
        
        Returns:
            Dict with list of PRs
        """
        self.logger.info(f"list_pull_requests: {repository}, state={state}")
        
        try:
            prs = [p for p in self.pull_requests.values() if p.repository == repository]
            
            if state == "merged":
                prs = [p for p in prs if p.merged_at is not None]
            elif state != "all":
                prs = [p for p in prs if p.state == state]
            
            prs = prs[:limit]
            
            return {
                "success": True,
                "repository": repository,
                "state": state,
                "pull_requests": [p.to_dict() for p in prs],
                "total": len(prs),
            }
        
        except Exception as e:
            self.logger.error(f"Error listing pull requests: {e}")
            return {"success": False, "error": str(e)}
    
    # =========================================================================
    # Branch Tools
    # =========================================================================
    
    def list_branches(self, repository: str) -> Dict[str, Any]:
        """
        List branches in a repository
        
        Args:
            repository: Repository identifier (owner/name)
        
        Returns:
            Dict with list of branches
        """
        self.logger.info(f"list_branches: {repository}")
        
        try:
            branches = self.branches.get(repository.lower(), ["main"])
            
            return {
                "success": True,
                "repository": repository,
                "branches": branches,
                "total": len(branches),
            }
        
        except Exception as e:
            self.logger.error(f"Error listing branches: {e}")
            return {"success": False, "error": str(e)}
    
    def create_branch(
        self,
        repository: str,
        branch_name: str,
        base_branch: str = "main",
    ) -> Dict[str, Any]:
        """
        Create a new branch in a repository
        
        Args:
            repository: Repository identifier (owner/name)
            branch_name: Name of the new branch
            base_branch: Base branch to create from
        
        Returns:
            Dict with success status or error
        """
        self.logger.info(f"create_branch: {repository} from {base_branch}")
        
        try:
            repo_key = repository.lower()
            if repo_key not in self.branches:
                self.branches[repo_key] = ["main"]
            
            if branch_name in self.branches[repo_key]:
                return {
                    "success": False,
                    "error": f"Branch {branch_name} already exists",
                }
            
            self.branches[repo_key].append(branch_name)
            self._save_to_storage()
            
            return {
                "success": True,
                "repository": repository,
                "branch": branch_name,
                "base_branch": base_branch,
            }
        
        except Exception as e:
            self.logger.error(f"Error creating branch: {e}")
            return {"success": False, "error": str(e)}
