"""
Idea-To-Prod Agent Team Orchestrator

Coordinates the five core agents to transform application ideas into
tested, deployable code.

Workflow:
    Idea → Agent 1 → Agent 2 → Agent 3 → Agent 4 → Agent 5 → Output
                                                      ↓ (if fails)
                                                    Agent 4 (retry)
"""

from typing import Optional, List
from agno.team import Team
from agno.agent import Agent

from .agent_1_hl_design import create_hl_design_agent
from .agent_2_detailed_design import create_detailed_design_agent
from .agent_3_code_generation import create_code_generation_agent
from .agent_4_test_generation import create_test_generation_agent
from .agent_5_test_execution import create_test_execution_agent


class IdeaToProdTeam:
    """
    Idea-To-Prod Agent Team Orchestrator
    
    Manages the workflow of five specialized agents working together to
    transform high-level ideas into production-ready, tested code.
    """
    
    STEP_NAMES = [
        "High-Level Design",
        "Detailed Design",
        "Code Generation",
        "Test Generation",
        "Test Execution"
    ]
    
    def __init__(self):
        """
        Initialize the Idea-To-Prod agent team.
        """
        
        self.agent_1_hl_design = create_hl_design_agent()
        self.agent_2_detailed_design = create_detailed_design_agent()
        self.agent_3_code_generation = create_code_generation_agent()
        self.agent_4_test_generation = create_test_generation_agent()
        self.agent_5_test_execution = create_test_execution_agent()
        
        self.team = Team(
            name="IdeaToProdTeam",
            description="""The Team Takes a high-level application idea and processes it through a complete development pipeline""",
            members=[
                self.agent_1_hl_design,
                self.agent_2_detailed_design,
                self.agent_3_code_generation,
                self.agent_4_test_generation,
                self.agent_5_test_execution
            ],
            markdown=True,
            show_members_responses=True,
            role="""You are a team of agents working together to take a high-level application idea and turn it into production-ready code. Each agent has a specific role in the development process. 
            Follow the workflow carefully and ensure that the final output is tested and validated before declaring success.""",
            instructions="""The team must take an idea from the user and process it through the following steps:
1. High-Level Design: Create a high-level design and architecture for the application based on the provided idea.
2. Detailed Design: Break down the high-level design into detailed components, modules, and tasks.
3. Code Generation: Generate code for the application based on the detailed design and tasks.   
4. Test Generation: Create unit tests for the generated code to ensure functionality and quality.
5. Test Execution: Run the generated tests against the code and validate the results. If tests
fail, identify issues and iterate on the code and tests until all tests pass successfully.
Make sure to communicate clearly between agents and provide detailed outputs at each step. The final output should be production-ready code that has been thoroughly tested and validated.""",
        )
    
    def process_idea(self, application_idea: str, steps_enabled: Optional[List[bool]] = None, start_of_step: int = 0) -> dict:
        """
        Process an application idea through the Idea-To-Prod pipeline.
        
        Workflow:
        1. Agent 1 (if enabled): Creates high-level design from idea
        2. Agent 2 (if enabled): Generates detailed design and tasks from HL design
        3. Agent 3 (if enabled): Generates code from detailed design and tasks
        4. Agent 4 (if enabled): Generates unit tests from code
        5. Agent 5 (if enabled): Executes tests and validates quality
        
        Args:
            application_idea (str): High-level description of the application to build
            
        Returns:
            dict: Results from each enabled step containing:
                - 'success': bool indicating overall success
                - 'enabled_steps': List[bool] of which steps were executed
                - 'step_results': dict mapping step names to their outputs
                - 'errors': List of any errors encountered
        """
        results = {
            "success": False,
            "enabled_steps": steps_enabled if steps_enabled else [True, True, True, True, True],
            "step_results": {},
            "errors": [],
            "skipped_steps": []
        }

        if steps_enabled is None:
            steps_enabled = [True, True, True, True, True]
        else:
            if len(steps_enabled) != 5:
                raise ValueError(f"steps_enabled must have exactly 5 boolean values, got {len(steps_enabled)}")
        
        try:
            # Log enabled steps
            enabled_step_names = [
                name for name, enabled in zip(self.STEP_NAMES, steps_enabled) if enabled
            ]
            skipped_step_names = [
                name for name, enabled in zip(self.STEP_NAMES, steps_enabled) if not enabled
            ]
            
            if skipped_step_names:
                results["skipped_steps"] = skipped_step_names
            
            # Run the Agno team with the idea
            response = self.team.run("The User had enabled the following steps: " + ", ".join(enabled_step_names) 
                                     + f". Application idea: {application_idea} starting from step {start_of_step + 1}.")
            
            # Capture team response
            results["step_results"]["team_output"] = str(response)
            results["success"] = True
            
        except Exception as e:
            error_msg = f"Error processing idea: {str(e)}"
            results["errors"].append(error_msg)
            results["success"] = False
        
        return results
    
    def test_mcp_connections(self) -> dict:
        """
        Test connectivity and functionality of all MCP servers across all platforms.
        
        Checks connections to:
        - GitHub MCP
        - Google Drive MCP
        - Jira MCP
        - Playwright MCP
        
        Returns:
            dict: Results of MCP connectivity tests containing:
                - 'success': bool indicating if all MCPs are connected
                - 'platform_results': dict mapping platform names to their test results
                - 'connected_platforms': list of successfully connected platforms
                - 'failed_platforms': list of platforms that failed connection
                - 'errors': dict mapping platform names to error messages (if any)
        """
        results = {
            "success": False,
            "platform_results": {},
            "connected_platforms": [],
            "failed_platforms": [],
            "errors": {}
        }
        
        # Define MCPs to test
        mcps_to_test = {
            "GitHub": self._test_github_mcp,
            "Google Drive": self._test_google_drive_mcp,
            "Jira": self._test_jira_mcp,
            "Playwright": self._test_playwright_mcp
        }
        
        # Test each MCP
        for platform_name, test_func in mcps_to_test.items():
            try:
                test_result = test_func()
                results["platform_results"][platform_name] = test_result
                
                if test_result["connected"]:
                    results["connected_platforms"].append(platform_name)
                else:
                    results["failed_platforms"].append(platform_name)
                    if "error" in test_result:
                        results["errors"][platform_name] = test_result["error"]
                        
            except Exception as e:
                results["failed_platforms"].append(platform_name)
                results["errors"][platform_name] = str(e)
                results["platform_results"][platform_name] = {
                    "connected": False,
                    "error": str(e)
                }
        
        # Overall success if all platforms are connected
        results["success"] = len(results["failed_platforms"]) == 0
        
        return results
    
    def _test_github_mcp(self) -> dict:
        """Test GitHub MCP connectivity."""
        try:
            from ..mcp_servers.github_mcp import GitHubMCPServer
            from ..mcp_servers.config.github_config import create_config
            
            config = create_config()
            server = GitHubMCPServer(config)
            
            # Attempt a basic operation to verify connectivity
            result = server.get_user_info()
            
            return {
                "connected": result.get("success", False),
                "message": "GitHub MCP is connected and functional",
                "details": result
            }
        except Exception as e:
            return {
                "connected": False,
                "error": f"GitHub MCP connection failed: {str(e)}"
            }
    
    def _test_google_drive_mcp(self) -> dict:
        """Test Google Drive MCP connectivity."""
        try:
            from ..mcp_servers.google_drive_mcp import GoogleDriveMCPServer
            from ..mcp_servers.config.google_drive_config import create_config
            
            config = create_config()
            server = GoogleDriveMCPServer(config)
            
            # Attempt a basic operation to verify connectivity
            result = server.list_files()
            
            return {
                "connected": result.get("success", False),
                "message": "Google Drive MCP is connected and functional",
                "details": result
            }
        except Exception as e:
            return {
                "connected": False,
                "error": f"Google Drive MCP connection failed: {str(e)}"
            }
    
    def _test_jira_mcp(self) -> dict:
        """Test Jira MCP connectivity."""
        try:
            from ..mcp_servers.jira_mcp import JiraMCPServer
            from ..mcp_servers.config.jira_config import create_config
            
            config = create_config()
            server = JiraMCPServer(config)
            
            # Attempt a basic operation to verify connectivity
            result = server.get_jira_info()
            
            return {
                "connected": result.get("success", False),
                "message": "Jira MCP is connected and functional",
                "details": result
            }
        except Exception as e:
            return {
                "connected": False,
                "error": f"Jira MCP connection failed: {str(e)}"
            }
    
    def _test_playwright_mcp(self) -> dict:
        """Test Playwright MCP connectivity."""
        try:
            from ..mcp_servers.playwright_mcp import PlaywrightMCPServer
            from ..mcp_servers.config.playwright_config import create_config
            
            config = create_config()
            server = PlaywrightMCPServer(config)
            
            # Attempt a basic operation to verify connectivity
            result = server.get_browser_info()
            
            return {
                "connected": result.get("success", False),
                "message": "Playwright MCP is connected and functional",
                "details": result
            }
        except Exception as e:
            return {
                "connected": False,
                "error": f"Playwright MCP connection failed: {str(e)}"
            }
    
    def reset(self):
        """Reset all agents to initial state."""
        try:
            # Re-instantiate agents
            self.__init__()
        except Exception as e:
            print(f"Error resetting team: {e}")


def create_team() -> IdeaToProdTeam:
    """
    Create and return an Idea-To-Prod Agent Team.
    
    Returns:
        IdeaToProdTeam: Configured team ready to process ideas.
                       All pipeline steps enabled by default.
    """
    return IdeaToProdTeam()