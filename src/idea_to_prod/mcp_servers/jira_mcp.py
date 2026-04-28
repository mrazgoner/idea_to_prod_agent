"""
Jira MCP Server
A configurable Model Context Protocol server for Jira operations.
Supports both 'stub' mode for testing and 'api' mode for real Jira API integration.
"""

import json
import logging
import sys
from datetime import datetime
from pathlib import Path
from typing import Any, Optional, Dict, List
from dataclasses import dataclass, asdict, field
import uuid

# Handle both relative and absolute imports
try:
    from .config.jira_config import JiraConfig, create_config
except ImportError:
    from config.jira_config import JiraConfig, create_config

# Import Jira library for real API operations
try:
    from jira import JIRA, JIRAError
    JIRA_AVAILABLE = True
except ImportError:
    JIRA_AVAILABLE = False


@dataclass
class JiraIssue:
    """Represents a Jira issue"""
    key: str
    summary: str
    description: Optional[str] = None
    issue_type: str = "Task"
    status: str = "To Do"
    assignee: Optional[str] = None
    reporter: Optional[str] = None
    project: str = "DEFAULT"
    priority: str = "Medium"
    created: Optional[str] = None
    updated: Optional[str] = None
    labels: List[str] = field(default_factory=list)
    comments: List[Dict[str, Any]] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convert issue to dictionary"""
        return {
            "key": self.key,
            "summary": self.summary,
            "description": self.description,
            "issue_type": self.issue_type,
            "status": self.status,
            "assignee": self.assignee,
            "reporter": self.reporter,
            "project": self.project,
            "priority": self.priority,
            "created": self.created,
            "updated": self.updated,
            "labels": self.labels,
            "comments": self.comments,
        }


class JiraMCPServer:
    """
    MCP Server for Jira operations.
    Stub implementation that stores issues locally in JSON format.
    Can be extended to support real Jira API.
    """
    
    # Issue counter for generating keys
    _issue_counter = 0
    
    def __init__(self, config: Optional[JiraConfig] = None):
        """
        Initialize Jira MCP Server
        
        Args:
            config: JiraConfig instance. If None, uses default config.
        """
        self.config = config or JiraConfig()
        self._setup_logging()
        self.logger.info(f"Initializing {self.config.name} v{self.config.version}")
        self.logger.info(f"Mode: {self.config.mode}, Storage: {self.config.storage_dir}")
        
        # Initialize API client if in 'api' mode
        self.jira = None
        if self.config.mode == "api":
            if not JIRA_AVAILABLE:
                raise ImportError("Jira library is required for 'api' mode. Install with: pip install jira")
            
            if not self.config.jira_base_url or not self.config.jira_username or not self.config.jira_api_token:
                raise ValueError("jira_base_url, jira_username, and jira_api_token are required for API mode")
            
            try:
                self.jira = JIRA(
                    server=self.config.jira_base_url,
                    basic_auth=(self.config.jira_username, self.config.jira_api_token),
                    options={'agile_rest_path': 'agile', 'async': True, 'retries': 3}
                )
                # Verify connection is valid
                self.jira.current_user()
                self.logger.info("Jira API client initialized successfully")
            except JIRAError as e:
                self.logger.error(f"Failed to authenticate with Jira: {e}")
                raise
        
        # In-memory store for stub mode
        self.issues: Dict[str, JiraIssue] = {}
        self.projects: Dict[str, Dict[str, Any]] = {
            "DEFAULT": {
                "key": "DEFAULT",
                "name": "Default Project",
                "description": "Default test project"
            }
        }
        
        # Load issues from storage if available (stub mode only)
        if self.config.mode == "stub":
            self._load_issues_from_storage()
    
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
    
    def _load_issues_from_storage(self):
        """Load issues from local storage"""
        try:
            issues_file = self.config.storage_dir / "issues.json"
            if issues_file.exists():
                with open(issues_file, 'r') as f:
                    issues_data = json.load(f)
                    for issue_key, issue_data in issues_data.items():
                        self.issues[issue_key] = JiraIssue(**issue_data)
                self.logger.info(f"Loaded {len(self.issues)} issues from storage")
        except Exception as e:
            self.logger.error(f"Error loading issues from storage: {str(e)}")
    
    def _save_issues_to_storage(self):
        """Save issues to local storage"""
        try:
            issues_file = self.config.storage_dir / "issues.json"
            issues_data = {key: issue.to_dict() for key, issue in self.issues.items()}
            with open(issues_file, 'w') as f:
                json.dump(issues_data, f, indent=2)
        except Exception as e:
            self.logger.error(f"Error saving issues to storage: {str(e)}")
    
    def _generate_issue_key(self, project: str = "DEFAULT") -> str:
        """Generate a unique issue key"""
        JiraMCPServer._issue_counter += 1
        return f"{project}-{JiraMCPServer._issue_counter}"
    
    # =========================================================================
    # Tool: create_issue
    # =========================================================================
    
    def create_issue(
        self,
        summary: str,
        issue_type: str = "Task",
        project: str = "DEFAULT",
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        priority: str = "Medium",
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Create a new Jira issue
        
        Args:
            summary: Issue summary/title
            issue_type: Type of issue (Task, Bug, Story, etc.)
            project: Project key (default: DEFAULT)
            description: Optional detailed description
            assignee: Optional assignee username
            priority: Priority level (Low, Medium, High, Highest)
            labels: Optional list of labels
        
        Returns:
            Dict with issue details or error
        """
        self.logger.info(f"create_issue called: summary={summary}, type={issue_type}")
        
        if self.config.mode == "api":
            return self._api_create_issue(summary, issue_type, project, description, assignee, priority, labels)
        else:
            return self._stub_create_issue(summary, issue_type, project, description, assignee, priority, labels)
    
    def _api_create_issue(
        self,
        summary: str,
        issue_type: str = "Task",
        project: str = "DEFAULT",
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        priority: str = "Medium",
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Real Jira API implementation for create_issue"""
        try:
            # Validate inputs
            if not summary or not isinstance(summary, str):
                raise ValueError("Summary must be a non-empty string")
            
            # Prepare issue fields
            fields = {
                "project": {"key": project},
                "summary": summary,
                "issuetype": {"name": issue_type},
                "priority": {"name": priority},
            }
            
            if description:
                fields["description"] = description
            
            if assignee:
                fields["assignee"] = {"name": assignee}
            
            if labels:
                fields["labels"] = labels
            
            # Create issue via API
            issue = self.jira.create_issue(fields=fields)
            
            self.logger.info(f"Issue created via API: {issue.key}")
            
            return {
                "status": "success",
                "message": f"Issue '{issue.key}' created successfully",
                "issue": {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "description": issue.fields.description,
                    "issue_type": issue.fields.issuetype.name,
                    "status": issue.fields.status.name,
                    "assignee": issue.fields.assignee.name if issue.fields.assignee else None,
                    "priority": issue.fields.priority.name if issue.fields.priority else None,
                    "project": issue.fields.project.key,
                    "labels": issue.fields.labels,
                    "created": issue.fields.created,
                    "updated": issue.fields.updated,
                    "comments": [],
                },
            }
        except JIRAError as e:
            self.logger.error(f"Jira API error creating issue: {e}")
            return {
                "status": "error",
                "message": f"Jira API error: {str(e)}",
                "error": type(e).__name__,
            }
        except Exception as e:
            self.logger.error(f"Error creating issue via API: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create issue: {str(e)}",
                "error": type(e).__name__,
            }
    
    def _stub_create_issue(
        self,
        summary: str,
        issue_type: str = "Task",
        project: str = "DEFAULT",
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        priority: str = "Medium",
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Stub implementation for create_issue"""
        try:
            # Validate inputs
            if not summary or not isinstance(summary, str):
                raise ValueError("Summary must be a non-empty string")
            
            if project not in self.projects and project != "DEFAULT":
                self.projects[project] = {
                    "key": project,
                    "name": project,
                    "description": f"Project {project}"
                }
            
            # Generate issue key
            issue_key = self._generate_issue_key(project)
            
            # Create issue
            now = datetime.now().isoformat()
            issue = JiraIssue(
                key=issue_key,
                summary=summary,
                description=description,
                issue_type=issue_type,
                project=project,
                assignee=assignee,
                priority=priority,
                labels=labels or [],
                reporter="mcp-bot",
                created=now,
                updated=now,
                status="To Do"
            )
            
            # Store issue
            self.issues[issue_key] = issue
            self._save_issues_to_storage()
            
            self.logger.info(f"Issue created: {issue_key}")
            
            return {
                "status": "success",
                "message": f"Issue '{issue_key}' created successfully",
                "issue": issue.to_dict(),
            }
        
        except Exception as e:
            self.logger.error(f"Error creating issue: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to create issue: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: get_issue
    # =========================================================================
    
    def get_issue(self, issue_key: str) -> Dict[str, Any]:
        """
        Get details of a specific issue
        
        Args:
            issue_key: Issue key (e.g., DEFAULT-1)
        
        Returns:
            Dict with issue details or error
        """
        self.logger.info(f"get_issue called: key={issue_key}")
        
        if self.config.mode == "api":
            return self._api_get_issue(issue_key)
        else:
            return self._stub_get_issue(issue_key)
    
    def _api_get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Real Jira API implementation for get_issue"""
        try:
            issue = self.jira.issue(issue_key)
            
            return {
                "status": "success",
                "issue": {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "description": issue.fields.description,
                    "issue_type": issue.fields.issuetype.name,
                    "status": issue.fields.status.name,
                    "assignee": issue.fields.assignee.name if issue.fields.assignee else None,
                    "reporter": issue.fields.reporter.name if issue.fields.reporter else None,
                    "priority": issue.fields.priority.name if issue.fields.priority else None,
                    "project": issue.fields.project.key,
                    "labels": issue.fields.labels,
                    "created": issue.fields.created,
                    "updated": issue.fields.updated,
                    "comments": [],
                },
            }
        except JIRAError as e:
            self.logger.error(f"Jira API error getting issue: {e}")
            return {
                "status": "error",
                "message": f"Jira API error: {str(e)}",
                "error": type(e).__name__,
            }
        except Exception as e:
            self.logger.error(f"Error getting issue via API: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get issue: {str(e)}",
                "error": type(e).__name__,
            }
    
    def _stub_get_issue(self, issue_key: str) -> Dict[str, Any]:
        """Stub implementation for get_issue"""
        try:
            if issue_key not in self.issues:
                raise ValueError(f"Issue not found: {issue_key}")
            
            issue = self.issues[issue_key]
            return {
                "status": "success",
                "issue": issue.to_dict(),
            }
        
        except Exception as e:
            self.logger.error(f"Error getting issue: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get issue: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: update_issue
    # =========================================================================
    
    def update_issue(
        self,
        issue_key: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        priority: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """
        Update an existing issue
        
        Args:
            issue_key: Issue key to update
            summary: New summary (optional)
            description: New description (optional)
            assignee: New assignee (optional)
            priority: New priority (optional)
            labels: New labels (optional)
        
        Returns:
            Dict with updated issue or error
        """
        self.logger.info(f"update_issue called: key={issue_key}")
        
        if self.config.mode == "api":
            return self._api_update_issue(issue_key, summary, description, assignee, priority, labels)
        else:
            return self._stub_update_issue(issue_key, summary, description, assignee, priority, labels)
    
    def _api_update_issue(
        self,
        issue_key: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        priority: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Real Jira API implementation for update_issue"""
        try:
            issue = self.jira.issue(issue_key)
            
            # Prepare update fields
            fields = {}
            if summary is not None:
                fields["summary"] = summary
            if description is not None:
                fields["description"] = description
            if assignee is not None:
                fields["assignee"] = {"name": assignee}
            if priority is not None:
                fields["priority"] = {"name": priority}
            if labels is not None:
                fields["labels"] = labels
            
            # Update the issue
            if fields:
                issue.update(fields=fields)
            
            self.logger.info(f"Issue updated via API: {issue_key}")
            
            return {
                "status": "success",
                "message": f"Issue '{issue_key}' updated successfully",
                "issue": {
                    "key": issue.key,
                    "summary": issue.fields.summary,
                    "description": issue.fields.description,
                    "issue_type": issue.fields.issuetype.name,
                    "status": issue.fields.status.name,
                    "assignee": issue.fields.assignee.name if issue.fields.assignee else None,
                    "priority": issue.fields.priority.name if issue.fields.priority else None,
                    "project": issue.fields.project.key,
                    "labels": issue.fields.labels,
                    "created": issue.fields.created,
                    "updated": issue.fields.updated,
                    "comments": [],
                },
            }
        except JIRAError as e:
            self.logger.error(f"Jira API error updating issue: {e}")
            return {
                "status": "error",
                "message": f"Jira API error: {str(e)}",
                "error": type(e).__name__,
            }
        except Exception as e:
            self.logger.error(f"Error updating issue via API: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to update issue: {str(e)}",
                "error": type(e).__name__,
            }
    
    def _stub_update_issue(
        self,
        issue_key: str,
        summary: Optional[str] = None,
        description: Optional[str] = None,
        assignee: Optional[str] = None,
        priority: Optional[str] = None,
        labels: Optional[List[str]] = None,
    ) -> Dict[str, Any]:
        """Stub implementation for update_issue"""
        try:
            if issue_key not in self.issues:
                raise ValueError(f"Issue not found: {issue_key}")
            
            issue = self.issues[issue_key]
            
            # Update fields
            if summary is not None:
                issue.summary = summary
            if description is not None:
                issue.description = description
            if assignee is not None:
                issue.assignee = assignee
            if priority is not None:
                issue.priority = priority
            if labels is not None:
                issue.labels = labels
            
            # Update timestamp
            issue.updated = datetime.now().isoformat()
            
            # Save changes
            self._save_issues_to_storage()
            
            self.logger.info(f"Issue updated: {issue_key}")
            
            return {
                "status": "success",
                "message": f"Issue '{issue_key}' updated successfully",
                "issue": issue.to_dict(),
            }
        
        except Exception as e:
            self.logger.error(f"Error updating issue: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to update issue: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: transition_issue (change status)
    # =========================================================================
    
    def transition_issue(
        self,
        issue_key: str,
        new_status: str,
    ) -> Dict[str, Any]:
        """
        Transition issue to a new status
        
        Args:
            issue_key: Issue key to transition
            new_status: New status (To Do, In Progress, In Review, Done)
        
        Returns:
            Dict with updated issue or error
        """
        self.logger.info(f"transition_issue called: key={issue_key}, status={new_status}")
        
        valid_statuses = ["To Do", "In Progress", "In Review", "Done"]
        
        try:
            if issue_key not in self.issues:
                raise ValueError(f"Issue not found: {issue_key}")
            
            if new_status not in valid_statuses:
                raise ValueError(f"Invalid status. Valid statuses: {valid_statuses}")
            
            issue = self.issues[issue_key]
            old_status = issue.status
            issue.status = new_status
            issue.updated = datetime.now().isoformat()
            
            # Save changes
            self._save_issues_to_storage()
            
            self.logger.info(f"Issue {issue_key} transitioned from {old_status} to {new_status}")
            
            return {
                "status": "success",
                "message": f"Issue transitioned from '{old_status}' to '{new_status}'",
                "issue": issue.to_dict(),
            }
        
        except Exception as e:
            self.logger.error(f"Error transitioning issue: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to transition issue: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: add_comment
    # =========================================================================
    
    def add_comment(
        self,
        issue_key: str,
        comment_text: str,
        author: str = "mcp-bot",
    ) -> Dict[str, Any]:
        """
        Add a comment to an issue
        
        Args:
            issue_key: Issue key to comment on
            comment_text: Comment text
            author: Author of the comment (default: mcp-bot)
        
        Returns:
            Dict with updated issue or error
        """
        self.logger.info(f"add_comment called: key={issue_key}")
        
        try:
            if issue_key not in self.issues:
                raise ValueError(f"Issue not found: {issue_key}")
            
            if len(comment_text) > self.config.max_comment_length:
                raise ValueError(
                    f"Comment exceeds maximum length of {self.config.max_comment_length}"
                )
            
            issue = self.issues[issue_key]
            
            # Create comment
            comment = {
                "id": str(uuid.uuid4()),
                "author": author,
                "body": comment_text,
                "created": datetime.now().isoformat(),
                "updated": datetime.now().isoformat(),
            }
            
            issue.comments.append(comment)
            issue.updated = datetime.now().isoformat()
            
            # Save changes
            self._save_issues_to_storage()
            
            self.logger.info(f"Comment added to issue {issue_key}")
            
            return {
                "status": "success",
                "message": f"Comment added to issue '{issue_key}'",
                "comment": comment,
                "issue": issue.to_dict(),
            }
        
        except Exception as e:
            self.logger.error(f"Error adding comment: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to add comment: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: list_issues
    # =========================================================================
    
    def list_issues(
        self,
        project: Optional[str] = None,
        status: Optional[str] = None,
        assignee: Optional[str] = None,
        max_results: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        List issues with optional filtering
        
        Args:
            project: Filter by project key (optional)
            status: Filter by status (optional)
            assignee: Filter by assignee (optional)
            max_results: Maximum number of results
        
        Returns:
            Dict with list of issues
        """
        self.logger.info(f"list_issues called: project={project}, status={status}")
        
        try:
            max_results = max_results or self.config.max_results_per_query
            
            # Filter issues
            filtered_issues = list(self.issues.values())
            
            if project:
                filtered_issues = [i for i in filtered_issues if i.project == project]
            if status:
                filtered_issues = [i for i in filtered_issues if i.status == status]
            if assignee:
                filtered_issues = [i for i in filtered_issues if i.assignee == assignee]
            
            # Limit results
            truncated = len(filtered_issues) > max_results
            filtered_issues = filtered_issues[:max_results]
            
            issues_data = [issue.to_dict() for issue in filtered_issues]
            
            return {
                "status": "success",
                "total": len(filtered_issues),
                "truncated": truncated,
                "issues": issues_data,
            }
        
        except Exception as e:
            self.logger.error(f"Error listing issues: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to list issues: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: search_issues (JQL support)
    # =========================================================================
    
    def search_issues(
        self,
        jql: str,
        max_results: Optional[int] = None,
    ) -> Dict[str, Any]:
        """
        Search issues using simple JQL-like queries
        
        Args:
            jql: Simple search query (e.g., "status=Done", "assignee=user1", "type=Bug")
            max_results: Maximum number of results
        
        Returns:
            Dict with matching issues
        """
        self.logger.info(f"search_issues called: jql={jql}")
        
        try:
            max_results = max_results or self.config.max_results_per_query
            
            # Simple JQL parser for common queries
            issues = list(self.issues.values())
            
            # Parse simple conditions (status=value, assignee=value, etc.)
            if "=" in jql:
                field, value = jql.split("=", 1)
                field = field.strip().lower()
                value = value.strip()
                
                if field == "status":
                    issues = [i for i in issues if i.status == value]
                elif field == "assignee":
                    issues = [i for i in issues if i.assignee == value]
                elif field == "type":
                    issues = [i for i in issues if i.issue_type == value]
                elif field == "project":
                    issues = [i for i in issues if i.project == value]
                elif field == "priority":
                    issues = [i for i in issues if i.priority == value]
            
            # Limit results
            truncated = len(issues) > max_results
            issues = issues[:max_results]
            
            issues_data = [issue.to_dict() for issue in issues]
            
            return {
                "status": "success",
                "total": len(issues_data),
                "truncated": truncated,
                "issues": issues_data,
            }
        
        except Exception as e:
            self.logger.error(f"Error searching issues: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to search issues: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: get_project
    # =========================================================================
    
    def get_project(self, project_key: str) -> Dict[str, Any]:
        """
        Get project details
        
        Args:
            project_key: Project key
        
        Returns:
            Dict with project details or error
        """
        self.logger.info(f"get_project called: key={project_key}")
        
        try:
            if project_key not in self.projects:
                raise ValueError(f"Project not found: {project_key}")
            
            project = self.projects[project_key]
            issue_count = sum(1 for i in self.issues.values() if i.project == project_key)
            
            return {
                "status": "success",
                "project": project,
                "issue_count": issue_count,
            }
        
        except Exception as e:
            self.logger.error(f"Error getting project: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get project: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: list_projects
    # =========================================================================
    
    def list_projects(self) -> Dict[str, Any]:
        """
        List all projects
        
        Returns:
            Dict with list of projects
        """
        self.logger.info("list_projects called")
        
        try:
            projects_list = []
            for key, project in self.projects.items():
                issue_count = sum(1 for i in self.issues.values() if i.project == key)
                projects_list.append({
                    **project,
                    "issue_count": issue_count,
                })
            
            return {
                "status": "success",
                "total": len(projects_list),
                "projects": projects_list,
            }
        
        except Exception as e:
            self.logger.error(f"Error listing projects: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to list projects: {str(e)}",
                "error": type(e).__name__,
            }
    
    # =========================================================================
    # Tool: get_issue_types
    # =========================================================================
    
    def get_issue_types(self) -> Dict[str, Any]:
        """
        Get available issue types
        
        Returns:
            Dict with list of issue types
        """
        self.logger.info("get_issue_types called")
        
        try:
            issue_types = [
                {"name": "Task", "description": "A task or piece of work"},
                {"name": "Bug", "description": "A bug in the software"},
                {"name": "Story", "description": "A user story"},
                {"name": "Epic", "description": "An epic spanning multiple issues"},
                {"name": "Sub-task", "description": "A subtask of another issue"},
            ]
            
            return {
                "status": "success",
                "issue_types": issue_types,
            }
        
        except Exception as e:
            self.logger.error(f"Error getting issue types: {str(e)}")
            return {
                "status": "error",
                "message": f"Failed to get issue types: {str(e)}",
                "error": type(e).__name__,
            }


def create_jira_server(
    jira_base_url: Optional[str] = None,
    jira_username: Optional[str] = None,
    jira_api_token: Optional[str] = None,
    mode: str = "stub",
    storage_dir: Optional[str] = None,
    enable_logging: bool = True,
    log_level: str = "INFO",
) -> JiraMCPServer:
    """
    Factory function to create a JiraMCPServer instance
    
    Args:
        jira_base_url: Base URL of Jira instance
        jira_username: Jira username
        jira_api_token: Jira API token
        mode: Operation mode ('stub' or 'api')
        storage_dir: Directory for local storage
        enable_logging: Whether to enable logging
        log_level: Logging level
    
    Returns:
        JiraMCPServer instance
    """
    config = create_config(
        jira_base_url=jira_base_url,
        jira_username=jira_username,
        jira_api_token=jira_api_token,
        mode=mode,
        storage_dir=storage_dir,
        enable_logging=enable_logging,
        log_level=log_level,
    )
    return JiraMCPServer(config)
