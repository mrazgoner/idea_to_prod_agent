"""
Agent 1: High-Level Design Generator

Responsibility: Create comprehensive high-level architecture and design document
from an application idea.

Input: Application idea/concept (natural language)
Output: High-level design document (saved to Google Drive)
"""

from agno.agent import Agent

from idea_to_prod.mcp_servers.google_drive_mcp import GoogleDriveMCPServer

from .config import AGENT_1_MODEL


def create_hl_design_agent() -> Agent:
    """
    Create High-Level Design Generator Agent.
    
    This agent:
    1. Parses the application idea
    2. Defines system components and modules
    3. Identifies key architectural patterns
    4. Documents requirements and constraints
    5. Creates design overview
    
    Returns:
        Agent: Configured high-level design generation agent
    """
    return Agent(
        name="HL Design Generator",
        model=AGENT_1_MODEL,
        description="Generates high-level architecture and design documents from application ideas",
        role="""You are an expert architect responsible for creating high-level design documents.""",
        instructions=""" Given an application idea, you must:
        
1. **Parse the Idea**: Understand the core requirements and goals
2. **Define Components**: Identify major system components and modules
3. **Architecture Patterns**: Suggest appropriate architectural patterns (monolith, microservices, etc.)
4. **Requirements**: Document functional and non-functional requirements
5. **Constraints**: Identify technical, business, and operational constraints
6. **Technology Stack**: Recommend initial technology choices
7. **Design Rationale**: Explain architectural decisions

Output Format:
- Create a comprehensive design document
- Use clear sections and subsections
- Include diagrams/descriptions for system architecture
- List all identified components
- Document key design decisions and rationale""",
        tools=[GoogleDriveMCPServer],
        markdown=True,
    )
