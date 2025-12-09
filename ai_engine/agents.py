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
from .tools import search_tool, crawler_tool, bocha_search_tool

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
        max_tokens=8192,  # Increased for longer context with search results
    )



def create_market_researcher(step_callback=None) -> Agent:
    """
    Create the Market Researcher agent.

    In Pre-Search Mode (default), this agent does NOT use tools.
    Search results are pre-fetched and injected into task descriptions.
    This bypasses CrewAI tool calling issues with ARK API.

    Args:
        step_callback: Optional callback for step-by-step logging

    Returns:
        Configured Market Researcher agent
    """
    return Agent(
        role="市场研究专家",
        goal=(
            "整理和分析提供的搜索资料，提取关键市场信息。"
            "保留所有 [Ref-N] 引用编号。使用中文输出。"
            "直接基于提供的资料进行分析，不需要其他操作。"
        ),
        backstory=(
            "您是资深市场研究专家。根据提供的搜索资料整理成结构化研究发现，保留 [Ref-N] 来源编号。"
        ),
        llm=get_ark_llm(),
        tools=[],
        verbose=True,
        memory=False,
        allow_delegation=False,
        max_iter=3,
        handle_parsing_errors=True,
        step_callback=step_callback,
    )


def create_business_analyst(step_callback=None) -> Agent:
    """
    Create the Business Analyst agent.

    Args:
        step_callback: Optional callback for step-by-step logging

    Returns:
        Configured Business Analyst agent
    """
    return Agent(
        role="商业分析师",
        goal=(
            "分析研究数据，撰写结构清晰的商业分析报告（Markdown格式）。"
            "使用 [Ref-N] 格式引用来源，结尾添加'参考文献'章节。"
            "信息足够时立即输出，不要反复验证。"
        ),
        backstory=(
            "您是资深商业分析师，注重数据来源的严谨性。"
            "报告格式：正文使用[Ref-N]引用，结尾添加'参考文献'列表。"
        ),
        llm=get_ark_llm(),
        tools=[],
        verbose=True,
        memory=False,
        allow_delegation=False,
        max_iter=3,
        handle_parsing_errors=True,
        step_callback=step_callback,
    )


def create_quality_supervisor(step_callback=None) -> Agent:
    """
    Create the Quality Supervisor agent.

    Args:
        step_callback: Optional callback for step-by-step logging

    Returns:
        Configured Quality Supervisor agent
    """
    return Agent(
        role="质量审核总监",
        goal=(
            "快速审核商业分析报告的质量。确认报告包含引用和参考文献后立即通过。"
            "不要反复审核，一次审核后立即输出结果。"
        ),
        backstory=(
            "您是质量保证总监。快速检查报告是否包含[Ref-N]引用和参考文献章节，然后立即通过。"
        ),
        llm=get_ark_llm(),
        tools=[],
        verbose=True,
        memory=False,
        allow_delegation=False,
        max_iter=3,
        handle_parsing_errors=True,
        step_callback=step_callback,
    )


# Factory function to create all agents
def create_all_agents(step_callback=None) -> dict[str, Agent]:
    """
    Create all agents for the business analysis crew.

    Args:
        step_callback: Optional callback function to receive step-by-step logs.
                       This enables real-time UI updates.

    Returns:
        Dictionary mapping agent names to Agent instances
    """
    return {
        "researcher": create_market_researcher(step_callback),
        "analyst": create_business_analyst(step_callback),
        "supervisor": create_quality_supervisor(step_callback),
    }

