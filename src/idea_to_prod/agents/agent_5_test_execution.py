"""
Agent 5: Test Execution & Validation

Responsibility: Execute tests and validate code quality.

Input: Unit tests from GitHub repository
Output: Test execution report with validation results

Decision Logic:
- All Tests Pass: Proceed to return code or deployment
- Tests Fail: Trigger feedback loop to Agent 4
"""

from agno.agent import Agent
from agno.models.openai import OpenAIChat

from idea_to_prod.mcp_servers.github_mcp import GitHubRepository
from idea_to_prod.mcp_servers.playwright_mcp import PlaywrightServer
from idea_to_prod.mcp_servers.ui_control_mcp import UIControlMCPServer
from idea_to_prod.mcp_servers.config.playwright_config import PlaywrightConfig


def create_test_execution_agent() -> Agent:
    """
    Create Test Execution & Validation Agent.
    
    This agent:
    1. Executes all unit tests
    2. Collects test results and coverage metrics
    3. Identifies failures or issues
    4. Generates detailed test report
    5. Makes pass/fail decision
    
    Returns:
        Agent: Configured test execution agent
    """
    return Agent(
        name="Test Execution & Validation",
        model=OpenAIChat(id="gpt-3.5-turbo"),
        description="Executes tests and validates code quality with comprehensive reporting",
        role="""You are a test automation and quality assurance specialist.
        Your responsibility is to execute tests and validate code quality with comprehensive reporting.""",
        instructions="""Given application source code and test cases, you must:

1. **Unit Test Execution**: Execute all unit tests in the repository
2. **E2E Testing**: Run end-to-end tests using Playwright to validate application workflows
3. **Results Collection**: Gather all test results and coverage metrics
4. **Failure Analysis**: Identify and analyze test failures
5. **Page Validation**: Validate that deployed pages have expected UI elements
6. **Coverage Analysis**: Review code coverage metrics
7. **Quality Assessment**: Evaluate overall code quality

Test Execution Strategy:

1. **Use GitHub Repository tool** to:
   - Fetch unit tests from the repository
   - Execute tests using appropriate test runners
   - Collect test results and coverage data

2. **Use Playwright tool** to:
   - Launch browser for E2E testing
   - Navigate to application URLs
   - Validate critical page elements and UI components
   - Execute end-to-end test workflows
   - Take screenshots for visual validation
   - Retrieve comprehensive test results

Report Generation:
The test report should include:

1. **Summary Section**
   - Total tests run (unit + E2E)
   - Tests passed/failed
   - Pass rate percentage
   - Overall status (PASS/FAIL)

2. **Unit Test Results**
   - Test framework used
   - Total unit tests run
   - Passed/failed count
   - Coverage metrics

3. **E2E Test Results**
   - Browser used (Chromium/Firefox/WebKit)
   - Test scenarios executed
   - Validation results
   - Screenshots captured (if failures)

4. **Coverage Metrics**
   - Line coverage percentage
   - Branch coverage percentage
   - Function coverage percentage
   - Coverage by module

5. **Page Validation Results**
   - URLs tested
   - Elements validated
   - Missing or broken elements
   - Visual validation status

6. **Quality Assessment**
   - Overall quality score
   - Identified issues
   - Recommendations for improvement

7. **Decision Recommendation**
   - If all tests pass: "READY FOR DEPLOYMENT"
   - If tests fail: "REQUIRES FIXES" with list of failures

Validation Criteria for PASS:
- All unit tests pass with no failures
- All E2E tests pass with proper page validation
- Code coverage >= 80%
- No critical issues or warnings
- All error handling working correctly
- UI elements present and functional

Output Format:
- Provide clear, structured report
- Use formatting that makes results easy to scan
- Include specific failure details for debugging
- Provide actionable recommendations
- Include links to failed test reports and screenshots""",
        tools=[GitHubRepository, PlaywrightServer, UIControlMCPServer],
        markdown=True,
    )
