"""
Agent 2: Detailed Design & Task Generator

Responsibility: Transform high-level design into implementation-ready specifications
and generate development tasks.

Input: High-level design document from Agent 1
Output: 
    - Detailed design document (Google Drive)
    - Development tasks (Jira)
"""

from agno.agent import Agent

from idea_to_prod.mcp_servers.google_drive_mcp import GoogleDriveMCPServer
from idea_to_prod.mcp_servers.jira_mcp import JiraMCPServer

from .config import AGENT_2_MODEL


def create_detailed_design_agent() -> Agent:
    """
    Create Detailed Design & Task Generator Agent.
    
    This agent:
    1. Expands each component from HL design
    2. Creates detailed specifications for each phase
    3. Defines technical stack and dependencies
    4. Generates development tasks/work items
    5. Creates acceptance criteria for each task
    
    Returns:
        Agent: Configured detailed design generation agent
    """
    return Agent(
        name="Detailed Design & Task Generator",
        model=AGENT_2_MODEL,
        description="Expands high-level design into detailed specifications and generates development tasks",
        role="""You are an expert technical architect and project manager. 
        Your responsibility is to take a high-level design document and create detailed technical specifications and actionable development tasks.""",
        instructions="""Given a high-level design document, you must:

1. **Component Expansion**: Break down each component into detailed specifications
2. **Technical Specifications**: Define APIs, data models, interfaces
3. **Technology Stack**: Detail specific libraries, frameworks, and versions
4. **Dependencies**: Identify all internal and external dependencies
5. **Development Phases**: Organize work into logical phases
6. **Task Generation**: Create specific, actionable development tasks
7. **Acceptance Criteria**: Define clear acceptance criteria for each task
8. **Effort Estimation**: Estimate effort for each task
9. **Risk Assessment**: Identify potential risks and mitigation strategies

Output Format:
- Detailed design document with all specifications
- List of development tasks as Jira-formatted items:
  * Each task should have: Title, Description, Acceptance Criteria, Effort (story points)
  * Tasks should be ordered by dependency and priority
  * Include all subtasks and dependencies between tasks

Output two separate sections:
1. "DETAILED DESIGN DOCUMENT" - Full specifications
2. "DEVELOPMENT TASKS" - Jira-formatted work items""",
        tools=[GoogleDriveMCPServer, JiraMCPServer],
        markdown=True,
    )
