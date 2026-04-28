"""
Agent implementations for the Idea-To-Prod platform.

Agents:
- Agent 1: High-Level Design Generator
- Agent 2: Detailed Design & Task Generator
- Agent 3: Code Generation
- Agent 4: Unit Test Generation
- Agent 5: Test Execution & Validation

Team:
- IdeaToProaTeam: Orchestrates all five agents in sequence
"""

from .agent_1_hl_design import create_hl_design_agent
from .agent_2_detailed_design import create_detailed_design_agent
from .agent_3_code_generation import create_code_generation_agent
from .agent_4_test_generation import create_test_generation_agent
from .agent_5_test_execution import create_test_execution_agent
from .team import IdeaToProaTeam, create_team

__all__ = [
    "create_hl_design_agent",
    "create_detailed_design_agent",
    "create_code_generation_agent",
    "create_test_generation_agent",
    "create_test_execution_agent",
    "IdeaToProaTeam",
    "create_team",
]
