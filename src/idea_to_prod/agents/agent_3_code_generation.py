"""
Agent 3: Code Generation

Responsibility: Generate complete application code from detailed specifications.

Input: Development tasks/work items from Jira
Output: Complete codebase (GitHub repository)
"""

from agno.agent import Agent

from idea_to_prod.mcp_servers.github_mcp import GitHubRepository
from idea_to_prod.mcp_servers.jira_mcp import JiraMCPServer
from idea_to_prod.mcp_servers.ui_control_mcp import UIControlMCPServer

from .config import AGENT_3_MODEL


def create_code_generation_agent() -> Agent:
    """
    Create Code Generation Agent.
    
    This agent:
    1. Fetches action items from Jira
    2. Analyzes technical requirements
    3. Generates code for each component
    4. Creates project structure
    5. Includes config files and dependencies
    
    Returns:
        Agent: Configured code generation agent
    """
    return Agent(
        name="Code Generator",
        model=AGENT_3_MODEL,
        description="Generates complete application code from specifications and development tasks",
        role="""You are an expert software developer responsible for code generation.
        Your responsibility is to take detailed specifications and development tasks and generate complete, production-ready code.""",
        instructions="""Given development tasks and specifications, you must:

1. **Task Analysis**: Understand all development tasks and requirements
2. **Code Architecture**: Design the code structure and organization
3. **Component Implementation**: Generate code for each component
4. **Project Structure**: Create proper directory and file organization
5. **Dependencies**: Include all necessary dependency declarations (requirements.txt, package.json, etc.)
6. **Configuration**: Create configuration files with sensible defaults
7. **Scripts**: Generate build, setup, and run scripts
8. **Documentation**: Include inline code documentation and comments
9. **Best Practices**: Follow language-specific best practices and conventions
10. **Error Handling**: Implement comprehensive error handling and validation

Output Format:
- Generate complete, production-ready code
- Include directory structure with all files
- Each file should be complete and compilable
- Include setup/installation instructions
- Provide a main entry point
- Include configuration files and dependencies

Key Requirements:
- Code must be syntactically correct and runnable
- Follow SOLID principles and clean code practices  
- Include type hints where applicable
- Use meaningful variable and function names
- Make the code modular and maintainable""",
        tools=[JiraMCPServer, GitHubRepository, UIControlMCPServer], 
        markdown=True,
    )
