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



def create_market_researcher() -> Agent:
    """
    Create the Market Researcher agent.

    This agent is responsible for analyzing topics using the Bocha AI
    web search API to gather real-time information from the web.

    Returns:
        Configured Market Researcher agent
    """
    return Agent(
        role="市场研究专家",
        goal=(
            "针对给定主题进行全面深入的市场研究。使用博查网页搜索工具获取最新的"
            "市场数据、行业趋势、竞争对手信息和洞察分析。"
            "搜索结果中包含引用编号 [1]、[2] 等，请在分析中使用这些编号标注信息来源。"
            "所有输出必须使用中文。"
        ),
        backstory=(
            "您是一位拥有15年商业情报分析经验的资深市场研究专家。"
            "您擅长使用网络搜索工具获取第一手市场情报，并对信息进行严谨的分析和整理。"
            "您的研究报告以数据详实、来源可靠著称。"
            "重要提示：您必须使用 Bocha Web Search 工具搜索相关信息，"
            "并在输出中保留所有引用编号（如 [1]、[2]），以便后续报告中正确引用来源。"
        ),
        llm=get_ark_llm(),
        tools=[],  # Temporarily disabled - testing CrewAI + ARK compatibility
        verbose=True,
        memory=True,
        allow_delegation=False,
    )


def create_business_analyst() -> Agent:
    """
    Create the Business Analyst agent.

    This agent analyzes the research data and produces a comprehensive
    business analysis report in markdown format with proper citations.

    Returns:
        Configured Business Analyst agent
    """
    return Agent(
        role="商业分析师",
        goal=(
            "分析研究数据，撰写一份结构清晰、内容全面的商业分析报告。"
            "报告必须使用中文撰写，格式采用 Markdown。"
            "重要：在报告正文中使用论文引用格式 [1]、[2] 等标注信息来源，"
            "并在报告末尾添加【参考文献】章节，列出所有引用来源的完整信息。"
        ),
        backstory=(
            "您是一位经验丰富的商业分析师，擅长将原始数据转化为战略洞察。"
            "您毕业于顶尖商学院，曾为多家世界500强企业提供咨询服务。"
            "您的报告以清晰的逻辑、深入的分析和切实可行的建议著称。"
            "您严格遵循学术规范，在报告中使用 [数字] 格式引用信息来源，"
            "并在报告最后提供完整的参考文献列表。请始终使用中文撰写报告。"
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
        role="质量审核总监",
        goal=(
            "审核商业分析报告的质量、准确性和完整性。确保报告达到专业标准，"
            "为读者提供有价值的可操作信息。审批通过或提出修改意见。"
            "确保最终报告使用规范的中文表达，逻辑清晰，内容准确。"
        ),
        backstory=(
            "您是一位严谨细致的质量保证总监，在编辑审核和商业咨询领域拥有丰富经验。"
            "您审阅过数千份商业报告，深谙高质量报告与平庸报告的区别。"
            "您确保每一份发布的报告都经过精心打磨、准确无误且具有商业价值。"
            "您要求严格但评判公正——认可优秀作品，对需要改进之处提供建设性反馈。"
            "请使用中文进行所有审核和反馈。"
        ),
        llm=get_ark_llm(),
        tools=[],
        verbose=True,
        memory=True,
        # Disabled delegation due to ARK API compatibility issues with CrewAI internal tools
        allow_delegation=False,
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

