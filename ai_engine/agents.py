"""
CrewAI Agent definitions for the Business Data Analysis Platform.

This module defines three specialized agents:
1. Market Researcher - Gathers data from web searches
2. Business Analyst - Analyzes data and writes reports
3. Quality Supervisor - Reviews and ensures report quality

The Quality Supervisor implements a SUPERVISION/REVIEW pattern:
- Reviews the final report for quality and completeness
- Can request revisions if the report doesn't meet standards
- Ensures the output is professional and actionable

LLM Configuration:
- Uses 火山引擎 ARK API (Volcengine) as the LLM provider
- Custom OpenAI-compatible endpoint with ARK credentials
"""
import os
from dotenv import load_dotenv
from crewai import Agent, LLM
from .tools import search_tool, crawler_tool

# Load environment variables
load_dotenv()


def get_ark_llm() -> LLM:
    """
    Configure LLM to use 火山引擎 ARK API.

    Uses the OpenAI-compatible interface with custom base_url.
    
    Note: ARK API supports OpenAI's chat/completions format.
    The model name should be the endpoint ID directly.

    Returns:
        Configured LLM instance for Volcengine ARK
    """
    api_key = os.getenv("ARK_API_KEY")
    base_url = os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3")
    model_endpoint = os.getenv("ARK_MODEL_ENDPOINT", "ep-20251123151038-946rh")
    
    # Set environment variables for OpenAI SDK compatibility
    # This is needed because some libraries read directly from env vars
    os.environ["OPENAI_API_KEY"] = api_key
    os.environ["OPENAI_API_BASE"] = base_url
    
    return LLM(
        # Use openai/ prefix for LiteLLM to route correctly
        model=f"openai/{model_endpoint}",
        base_url=base_url,
        api_key=api_key,
        # Additional parameters to improve compatibility
        temperature=0.7,
        max_tokens=4096,
    )



def create_market_researcher() -> Agent:
    """
    Create the Market Researcher agent.

    This agent is responsible for analyzing topics using its extensive
    knowledge base (web search tools are currently disabled due to 
    network restrictions in China).

    Returns:
        Configured Market Researcher agent
    """
    return Agent(
        role="Market Researcher",
        goal=(
            "Conduct comprehensive research on the given topic to gather "
            "relevant market data, trends, competitor information, and insights "
            "using your extensive knowledge and expertise"
        ),
        backstory=(
            "You are a senior market researcher with 15 years of experience "
            "in business intelligence. You have extensive knowledge about "
            "global markets, technology trends, and business developments. "
            "You specialize in providing quantitative data and qualitative "
            "trends that inform business decisions. You can provide insights "
            "based on your comprehensive training data and industry expertise."
        ),
        llm=get_ark_llm(),
        tools=[],  # Tools disabled due to network restrictions
        verbose=True,
        memory=True,
        allow_delegation=False,
    )


def create_business_analyst() -> Agent:
    """
    Create the Business Analyst agent.

    This agent analyzes the research data and produces a comprehensive
    business analysis report in markdown format.

    Returns:
        Configured Business Analyst agent
    """
    return Agent(
        role="Business Analyst",
        goal=(
            "Analyze the research data and produce a comprehensive, "
            "well-structured business analysis report with actionable insights"
        ),
        backstory=(
            "You are a seasoned business analyst with expertise in transforming "
            "raw data into strategic insights. You have an MBA from a top "
            "business school and have consulted for Fortune 500 companies. "
            "Your reports are known for their clarity, depth, and practical "
            "recommendations that drive business value."
        ),
        llm=get_ark_llm(),
        tools=[],  # Analyst works with data provided by Researcher
        verbose=True,
        memory=True,
        allow_delegation=False,
    )


def create_quality_supervisor() -> Agent:
    """
    Create the Quality Supervisor agent.

    SUPERVISION/REVIEW LOGIC:
    -------------------------
    This agent implements a quality control pattern where it:
    1. Reviews the report produced by the Business Analyst
    2. Evaluates it against quality criteria (completeness, accuracy, clarity)
    3. Either approves the report OR provides specific feedback for revision

    The supervisor can delegate work back to other agents if the quality
    isn't satisfactory, ensuring the final output meets professional standards.

    Returns:
        Configured Quality Supervisor agent
    """
    return Agent(
        role="Quality Supervisor",
        goal=(
            "Review the business analysis report for quality, accuracy, and "
            "completeness. Ensure it meets professional standards and provides "
            "actionable value to the reader. Approve or request revisions."
        ),
        backstory=(
            "You are a meticulous quality assurance director with experience "
            "in editorial review and business consulting. You have reviewed "
            "thousands of reports and know exactly what makes a report excellent "
            "versus mediocre. You ensure every report that goes out is polished, "
            "accurate, and valuable. You are strict but fair - you approve good "
            "work and provide constructive feedback when improvements are needed."
        ),
        llm=get_ark_llm(),
        tools=[],
        verbose=True,
        memory=True,
        # IMPORTANT: Allow delegation so supervisor can send work back
        allow_delegation=True,
    )


# Factory function to create all agents
def create_all_agents() -> dict[str, Agent]:
    """
    Create all agents for the business analysis crew.

    Returns:
        Dictionary mapping agent names to Agent instances
    """
    return {
        "researcher": create_market_researcher(),
        "analyst": create_business_analyst(),
        "supervisor": create_quality_supervisor(),
    }
