"""
Main CrewAI orchestration module for the Business Data Analysis Platform.

Pre-Search Mode: Search results are fetched BEFORE the crew runs,
bypassing CrewAI tool calling issues with ARK API.
"""
import os
from typing import Optional, Callable
from dotenv import load_dotenv
from crewai import Crew, Process

from .agents import create_all_agents
from .tasks import create_all_tasks
from .pre_search import pre_search, format_research_data, save_search_to_db


# Load environment variables
load_dotenv()

# Global flag to enable/disable pre-search mode
PRE_SEARCH_MODE = True  # Set to False to use normal tool-based mode


class BusinessAnalysisCrew:
    """
    Orchestrates the business analysis agent team.

    Pre-Search Mode:
    - Search results are fetched BEFORE crew runs
    - Results are injected into task descriptions
    - Agents work with provided data, no tool calls needed
    - This bypasses ARK API compatibility issues with CrewAI tools
    
    Usage:
        crew = BusinessAnalysisCrew()
        result = crew.run("electric vehicles market")
    """

    def __init__(
        self,
        verbose: bool = True,
        process: Process = Process.sequential,
        use_pre_search: bool = PRE_SEARCH_MODE,
    ) -> None:
        """
        Initialize the business analysis crew.

        Args:
            verbose: Whether to enable verbose output from agents
            process: CrewAI process type (sequential or hierarchical)
            use_pre_search: Whether to use pre-search mode (recommended for ARK API)
        """
        self.verbose = verbose
        self.process = process
        self.use_pre_search = use_pre_search
        self._agents: Optional[dict] = None
        self._crew: Optional[Crew] = None

    def _setup_agents(self) -> dict:
        """Create and cache agents."""
        if self._agents is None:
            self._agents = create_all_agents()
        return self._agents

    def _build_crew(self, topic: str, search_data: Optional[str] = None) -> Crew:
        """
        Build the crew for a specific topic.

        Args:
            topic: The topic to analyze
            search_data: Pre-fetched search data (for pre-search mode)

        Returns:
            Configured Crew instance
        """
        agents = self._setup_agents()

        # Create tasks with pre-search data if available
        tasks = create_all_tasks(
            topic=topic,
            researcher=agents["researcher"],
            analyst=agents["analyst"],
            supervisor=agents["supervisor"],
            pre_search_data=search_data,
        )

        # Build the crew
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

        In Pre-Search Mode:
        1. First fetches search results via direct API call
        2. Saves results to database
        3. Injects results into crew task descriptions
        4. Runs crew with pre-loaded data (no tool calls)

        Args:
            topic: The keyword or topic to analyze
            callback: Optional callback function for streaming output

        Returns:
            The final business analysis report as a string
        """
        search_data_str = None
        
        if self.use_pre_search:
            # === PRE-SEARCH PHASE ===
            print(f"🔍 Pre-Search Mode: Fetching data for '{topic}'...")
            
            search_result = pre_search(topic, count=5)
            
            if search_result["raw_data"]:
                # Save to database
                try:
                    save_search_to_db(topic, search_result)
                    print(f"💾 Saved {len(search_result['raw_data'])} search results to database")
                except Exception as e:
                    print(f"⚠️ Database save failed: {e}")
                
                # Format for injection
                search_data_str = format_research_data(topic, search_result)
                print(f"✅ Pre-search complete: {len(search_result['raw_data'])} results ready")
            else:
                print("⚠️ No search results found, crew will use general knowledge")
        
        # === CREW EXECUTION PHASE ===
        crew = self._build_crew(topic, search_data_str)
        result = crew.kickoff()

        # Handle different result types
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
        search_data_str = None
        
        if self.use_pre_search:
            # Pre-search (sync, but fast)
            print(f"🔍 Pre-Search Mode: Fetching data for '{topic}'...")
            
            search_result = pre_search(topic, count=5)
            
            if search_result["raw_data"]:
                try:
                    save_search_to_db(topic, search_result)
                except Exception as e:
                    print(f"⚠️ Database save failed: {e}")
                
                search_data_str = format_research_data(topic, search_result)
                print(f"✅ Pre-search complete: {len(search_result['raw_data'])} results ready")
        
        crew = self._build_crew(topic, search_data_str)
        result = await crew.kickoff_async()

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
