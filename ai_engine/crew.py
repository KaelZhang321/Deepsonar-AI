"""
Main CrewAI orchestration module for the Business Data Analysis Platform.

This module provides the entry point for running the AI agent team.
It assembles the crew (Researcher + Analyst + Supervisor) and
orchestrates their collaboration to produce business analysis reports.
"""
import os
from typing import Optional, Callable
from dotenv import load_dotenv
from crewai import Crew, Process

from .agents import create_all_agents
from .tasks import create_all_tasks


# Load environment variables
load_dotenv()


class BusinessAnalysisCrew:
    """
    Orchestrates the business analysis agent team.

    This class manages the CrewAI crew that consists of:
    - Market Researcher: Gathers data using search tools
    - Business Analyst: Writes the analysis report
    - Quality Supervisor: Reviews and approves the final output

    Usage:
        crew = BusinessAnalysisCrew()
        result = crew.run("electric vehicles market")
    """

    def __init__(
        self,
        verbose: bool = True,
        process: Process = Process.sequential,
    ) -> None:
        """
        Initialize the business analysis crew.

        Args:
            verbose: Whether to enable verbose output from agents
            process: CrewAI process type (sequential or hierarchical)

        Note on Process Types:
        - SEQUENTIAL: Tasks are executed in order, each building on the previous
        - HIERARCHICAL: A manager agent coordinates and delegates work

        For the supervision/review pattern, SEQUENTIAL works well because
        it ensures the research → analysis → review flow is maintained.
        """
        self.verbose = verbose
        self.process = process
        self._agents: Optional[dict] = None
        self._crew: Optional[Crew] = None

    def _setup_agents(self) -> dict:
        """Create and cache agents."""
        if self._agents is None:
            self._agents = create_all_agents()
        return self._agents

    def _build_crew(self, topic: str) -> Crew:
        """
        Build the crew for a specific topic.

        Args:
            topic: The topic to analyze

        Returns:
            Configured Crew instance
        """
        agents = self._setup_agents()

        # Create tasks for this topic
        tasks = create_all_tasks(
            topic=topic,
            researcher=agents["researcher"],
            analyst=agents["analyst"],
            supervisor=agents["supervisor"],
        )

        # Build the crew
        # Using SEQUENTIAL process to ensure proper flow:
        # Research → Analysis → Review/Supervision
        crew = Crew(
            agents=[
                agents["researcher"],
                agents["analyst"],
                agents["supervisor"],
            ],
            tasks=tasks,
            process=self.process,
            verbose=self.verbose,
        )

        return crew

    def run(
        self,
        topic: str,
        callback: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Run the business analysis crew on a topic.

        Args:
            topic: The keyword or topic to analyze
            callback: Optional callback function for streaming output

        Returns:
            The final business analysis report as a string

        Raises:
            Exception: If the crew execution fails
        """
        crew = self._build_crew(topic)

        # Execute the crew
        # The result will be the output from the final task (review)
        result = crew.kickoff()

        # Handle different result types (CrewAI version compatibility)
        if hasattr(result, "raw"):
            output = result.raw
        elif hasattr(result, "output"):
            output = result.output
        else:
            output = str(result)

        return output

    async def run_async(
        self,
        topic: str,
        callback: Optional[Callable[[str], None]] = None,
    ) -> str:
        """
        Async version of run for integration with async frameworks.

        Args:
            topic: The keyword or topic to analyze
            callback: Optional callback function for streaming output

        Returns:
            The final business analysis report as a string
        """
        crew = self._build_crew(topic)

        # Execute the crew asynchronously
        result = await crew.kickoff_async()

        # Handle different result types
        if hasattr(result, "raw"):
            output = result.raw
        elif hasattr(result, "output"):
            output = result.output
        else:
            output = str(result)

        return output


def run_analysis(topic: str, verbose: bool = True) -> str:
    """
    Convenience function to run a business analysis.

    Args:
        topic: The topic to analyze
        verbose: Whether to enable verbose output

    Returns:
        The final business analysis report
    """
    crew = BusinessAnalysisCrew(verbose=verbose)
    return crew.run(topic)


# Allow running directly for testing
if __name__ == "__main__":
    import sys

    if len(sys.argv) < 2:
        print("Usage: python -m ai_engine.crew <topic>")
        print("Example: python -m ai_engine.crew 'electric vehicles market'")
        sys.exit(1)

    topic = " ".join(sys.argv[1:])
    print(f"\n🚀 Starting business analysis for: {topic}\n")

    result = run_analysis(topic)

    print("\n" + "=" * 60)
    print("📊 FINAL REPORT")
    print("=" * 60)
    print(result)
