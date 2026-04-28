"""
Agent models configuration.

Centralized model settings for all agents - the most common configuration to manage.
"""

from agno.models.openai import OpenAIChat
from agno.models.anthropic import Claude


# Agent 1: High-Level Design Generator
AGENT_1_MODEL = OpenAIChat(id="gpt-4")

# Agent 2: Detailed Design & Task Generator
AGENT_2_MODEL = Claude(id="claude-3-5-sonnet-20241022")

# Agent 3: Code Generation
AGENT_3_MODEL = OpenAIChat(id="gpt-4")

# Agent 4: Unit Test Generation
AGENT_4_MODEL = OpenAIChat(id="gpt-4-turbo")

# Agent 5: Test Execution & Validation
AGENT_5_MODEL = OpenAIChat(id="gpt-3.5-turbo")
