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


class IdeaToProaTeam:
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
            "enabled_steps": self.steps_enabled,
            "step_results": {},
            "errors": [],
            "skipped_steps": []
        }

        if steps_enabled is None:
            self.steps_enabled = [True, True, True, True, True]
        else:
            if len(steps_enabled) != 5:
                raise ValueError(f"steps_enabled must have exactly 5 boolean values, got {len(steps_enabled)}")
            self.steps_enabled = steps_enabled
        
        try:
            # Log enabled steps
            enabled_step_names = [
                name for name, enabled in zip(self.STEP_NAMES, self.steps_enabled) if enabled
            ]
            skipped_step_names = [
                name for name, enabled in zip(self.STEP_NAMES, self.steps_enabled) if not enabled
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
    
    
    def reset(self):
        """Reset all agents to initial state, maintaining current step configuration."""
        try:
            # Re-instantiate agents while keeping the same steps_enabled configuration
            steps_config = self.steps_enabled.copy()
            self.__init__(steps_enabled=steps_config)
        except Exception as e:
            print(f"Error resetting team: {e}")


def create_team() -> IdeaToProaTeam:
    """
    Create and return an Idea-To-Prod Agent Team.
    
    Args:
        steps_enabled: Optional vector of 5 booleans determining which steps to perform.
                      If None, all steps are enabled by default.
                      Order: [HL Design, Detailed Design, Code Gen, Test Gen, Test Exec]
    
    Returns:
        IdeaToProaTeam: Configured team ready to process ideas
    """
    return IdeaToProaTeam()