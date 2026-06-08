"""
Agent 4: Unit Test Generator

Responsibility: Create comprehensive unit tests for generated code with high coverage.

Input: Source code from GitHub repository
Output: Unit test files (GitHub repository)
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from idea_to_prod.mcp_servers.github_mcp import GitHubRepository
from idea_to_prod.mcp_servers.ui_control_mcp import UIControlMCPServer


def create_test_generation_agent() -> Agent:
    """
    Create Unit Test Generator Agent.
    
    This agent:
    1. Fetches code from repository
    2. Analyzes code structure and logic
    3. Identifies test scenarios
    4. Generates unit tests with high coverage
    5. Includes edge cases and error handling
    
    Returns:
        Agent: Configured test generation agent
    """
    return Agent(
        name="Test Generator",
        model=OpenAIChat(id="gpt-4-turbo"),
        description="Generates comprehensive unit tests for application code with high coverage",
        role="""You are an expert QA engineer and test strategist.
        Your responsibility is to take application source code and generate comprehensive unit tests with high coverage.""",
        instructions="""Given application source code, you must:

1. **Code Analysis**: Understand the code structure, functions, and classes
2. **Test Strategy**: Develop a comprehensive test strategy
3. **Test Scenarios**: Identify all important test scenarios:
   - Happy path (normal operation)
   - Edge cases (boundary conditions)
   - Error cases (exceptions and validation)
   - Integration scenarios
4. **Test Generation**: Generate unit tests for all components
5. **Coverage**: Aim for high code coverage (>80%)
6. **Assertions**: Use meaningful assertions that validate behavior
7. **Mocking**: Use appropriate mocking for external dependencies
8. **Fixtures**: Create reusable test fixtures
9. **Documentation**: Document test purpose and approach

Output Format:
- Generate test files for each source module
- Use the testing framework appropriate for the language:
  * Python: pytest, unittest
  * JavaScript/Node: Jest
  * Java: JUnit
  * Go: testing package
- Include setup and teardown where needed
- Each test should have a clear name describing what it tests
- Include parametrized tests for multiple scenarios

Test Quality Requirements:
- Tests should be independent and runnable in any order
- Tests should run quickly
- Avoid flaky tests
- Test behavior, not implementation
- Include both unit and integration tests where appropriate
- Generate a test summary showing coverage metrics""",
        tools=[GitHubRepository, UIControlMCPServer],
        markdown=True,
    )
