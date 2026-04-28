"""
Main entry point for the Idea-To-Prod platform.

This is a console application that runs agents and saves results to files.
"""

import asyncio
import logging
import sys
from pathlib import Path
from datetime import datetime
from typing import Optional

from .agents.agent_1_hl_design import create_hl_design_agent
from .agents.agent_2_detailed_design import create_detailed_design_agent

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)


def create_results_folder() -> Path:
    """Create and return results folder with timestamp."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    results_dir = Path(__file__).parent.parent.parent / "results" / timestamp
    results_dir.mkdir(parents=True, exist_ok=True)
    return results_dir


def save_result(results_dir: Path, filename: str, content: str) -> None:
    """Save content to file in results directory."""
    filepath = results_dir / filename
    filepath.write_text(content, encoding="utf-8")
    logger.info(f"✓ Saved: {filepath}")


async def run_agent_1_console(idea: str, results_dir: Path) -> str:
    """Run Agent 1 and capture output."""
    logger.info("\n" + "="*70)
    logger.info("STEP 1: High-Level Design Generation")
    logger.info("="*70 + "\n")
    
    logger.info(f"Input idea:\n{idea}\n")
    
    try:
        agent = create_hl_design_agent()
        logger.info(f"✓ Agent created: {agent.name}")
        
        # Run the agent with the idea
        logger.info(f"\n→ Running agent...")
        response = agent.run(idea)
        
        # Convert response to string if needed
        result_text = str(response)
        
        # Save to file
        save_result(results_dir, "01_hl_design.md", result_text)
        
        logger.info("✓ High-level design generated successfully\n")
        return result_text
        
    except Exception as e:
        logger.error(f"✗ Error in Agent 1: {e}")
        error_msg = f"Agent 1 Error: {str(e)}"
        save_result(results_dir, "01_hl_design_ERROR.txt", error_msg)
        return ""


async def run_agent_2_console(hl_design: str, results_dir: Path) -> str:
    """Run Agent 2 and capture output."""
    logger.info("\n" + "="*70)
    logger.info("STEP 2: Detailed Design & Task Generation")
    logger.info("="*70 + "\n")
    
    logger.info(f"Input design (first 200 chars):\n{hl_design[:200]}...\n")
    
    try:
        agent = create_detailed_design_agent()
        logger.info(f"✓ Agent created: {agent.name}")
        
        # Run the agent with the HL design
        logger.info(f"\n→ Running agent...")
        response = agent.run(hl_design)
        
        # Convert response to string if needed
        result_text = str(response)
        
        # Save to file
        save_result(results_dir, "02_detailed_design.md", result_text)
        
        logger.info("✓ Detailed design generated successfully\n")
        return result_text
        
    except Exception as e:
        logger.error(f"✗ Error in Agent 2: {e}")
        error_msg = f"Agent 2 Error: {str(e)}"
        save_result(results_dir, "02_detailed_design_ERROR.txt", error_msg)
        return ""


async def main(idea: str, run_all: bool = False) -> Path:
    """
    Main console application for Idea-To-Prod platform.
    
    Runs agents and saves results to timestamped folder.
    
    Args:
        idea: The application idea to implement
        run_all: If True, run all agents. Otherwise just Agent 1.
        
    Returns:
        Path to results folder
    """
    results_dir = create_results_folder()
    
    logger.info(f"\n{'='*70}")
    logger.info("IdeaToProd - Console Application")
    logger.info(f"Results folder: {results_dir}")
    logger.info(f"{'='*70}\n")
    
    # Save input
    save_result(results_dir, "00_input_idea.txt", idea)
    
    # Run Agent 1
    hl_design_result = await run_agent_1_console(idea, results_dir)
    
    # Optionally run Agent 2 if we got results from Agent 1
    if run_all and hl_design_result:
        detailed_design_result = await run_agent_2_console(hl_design_result, results_dir)
    
    # Summary
    logger.info("\n" + "="*70)
    logger.info("WORKFLOW COMPLETE")
    logger.info("="*70)
    logger.info(f"\nResults saved to:\n{results_dir}\n")
    
    # List generated files
    generated_files = list(results_dir.glob("*.md")) + list(results_dir.glob("*.txt"))
    if generated_files:
        logger.info("Generated files:")
        for fpath in sorted(generated_files):
            logger.info(f"  • {fpath.name}")
    
    logger.info("")
    return results_dir


def get_user_input() -> str:
    """Get application idea from user console input."""
    print("\n" + "="*70)
    print("Enter your application idea")
    print("="*70)
    print("Describe what you want to build (press Enter twice to finish):\n")
    
    lines = []
    empty_count = 0
    
    while empty_count < 1:
        try:
            line = input()
            if line.strip():
                lines.append(line)
                empty_count = 0
            else:
                empty_count += 1
        except EOFError:
            break
    
    return "\n".join(lines)


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="IdeaToProd Console Application"
    )
    parser.add_argument(
        "--idea",
        type=str,
        help="Application idea (if not provided, interactive mode)"
    )
    parser.add_argument(
        "--all",
        action="store_true",
        help="Run all agents (default: Agent 1 only)"
    )
    parser.add_argument(
        "--example",
        action="store_true",
        help="Run with example idea"
    )
    
    args = parser.parse_args()
    
    # Determine input idea
    if args.example:
        idea = """
        Build a todo application with priority levels,
        due dates, and team collaboration features.
        Include authentication and notifications.
        """
    elif args.idea:
        idea = args.idea
    else:
        idea = get_user_input()
    
    if not idea.strip():
        logger.error("No idea provided. Exiting.")
        sys.exit(1)
    
    # Run workflow
    results_path = asyncio.run(main(idea, run_all=args.all))
    logger.info(f"✓ All results saved to: {results_path}")
