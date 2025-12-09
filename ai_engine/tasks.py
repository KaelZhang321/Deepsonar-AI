"""
CrewAI Task definitions for the Business Data Analysis Platform.

Pre-Search Mode: Search results are fetched BEFORE crew runs and injected
into task descriptions. This bypasses CrewAI tool calling issues with ARK API.
"""
from crewai import Task, Agent
from typing import Optional


def create_research_task(
    topic: str, 
    researcher: Agent,
    pre_search_data: Optional[str] = None
) -> Task:
    """
    Create the research task with pre-fetched search data.
    
    In Pre-Search Mode, search results are already available and just need
    to be organized and analyzed.

    Args:
        topic: The keyword or topic to research
        researcher: The Market Researcher agent
        pre_search_data: Pre-fetched search results (optional)

    Returns:
        Configured research Task
    """
    if pre_search_data:
        # Pre-Search Mode: Data already available
        description = (
            f"针对主题「{topic}」整理和分析以下搜索资料。\n\n"
            "【已搜索到的资料】\n"
            f"{pre_search_data}\n\n"
            "【任务要求】\n"
            "1. 整理上述资料，提取关键信息\n"
            "2. 保留所有 [Ref-N] 引用编号\n"
            "3. 按以下维度整理：市场规模、竞争格局、消费者洞察\n"
            "4. 使用中文输出\n\n"
            "直接基于上述资料进行分析，不需要再次搜索。"
        )
    else:
        # Normal Mode: Use search tools
        description = (
            f"针对主题「{topic}」进行多维度深度市场研究。\n\n"
            "【搜索策略】请使用搜索工具获取信息。\n"
            "【输出要求】\n"
            "- 保留所有 [Ref-N] 引用编号\n"
            "- 整理成结构化的研究发现\n"
            "- 使用中文输出"
        )
    
    return Task(
        description=description,
        expected_output=(
            "一份结构化的中文研究发现文档，包含：\n"
            "- 市场数据（规模、增长率、预测）\n"
            "- 主要竞争对手信息\n"
            "- 消费者洞察\n"
            "- 所有数据带有 [Ref-N] 引用编号"
        ),
        agent=researcher,
    )


def create_analysis_task(topic: str, analyst: Agent, context: list[Task]) -> Task:
    """
    Create the analysis task with structured deep report template.
    """
    return Task(
        description=(
            f"根据研究数据，撰写一份关于「{topic}」的深度商业分析报告。\n\n"
            "【关键要求】\n"
            "1. **深度优先**：不要写泛泛的摘要，要写深入的分析\n"
            "2. **字数要求**：全文不少于 2000 字\n"
            "3. **引用规范**：正文中使用 [Ref-N] 标注信息来源\n"
            "4. **语言要求**：全部使用中文撰写\n\n"
            "【强制报告结构】必须严格按照以下 Markdown 模板撰写：\n\n"
            f"# {topic} 深度商业分析报告\n\n"
            "## 执行摘要\n"
            "*简要概述本报告的核心发现和建议，100-150字*\n\n"
            "## 1. 市场宏观概况\n"
            "*分析市场规模、增长率、核心驱动力。至少 300 字。*\n\n"
            "## 2. 竞争格局分析\n"
            "*分析主要玩家、市场份额、护城河。至少 400 字。*\n\n"
            "## 3. 消费者洞察\n"
            "*分析用户画像、痛点、需求变化。至少 300 字。*\n\n"
            "## 4. SWOT 分析\n"
            "### 优势 (Strengths)\n"
            "### 劣势 (Weaknesses)\n"
            "### 机会 (Opportunities)\n"
            "### 威胁 (Threats)\n\n"
            "## 5. 风险与挑战\n\n"
            "## 6. 战略建议\n\n"
            "## 7. 结论\n\n"
            "## 参考文献\n"
            "- [Ref-1] 标题, 链接: URL\n"
            "- [Ref-2] 标题, 链接: URL\n\n"
            "【重要提示】每个章节必须有实质内容，使用研究数据中的 [Ref-N] 引用。"
        ),
        expected_output=(
            "一份完整的中文深度商业分析报告，包含：\n"
            "- 完整的7个主要章节\n"
            "- 每个章节有充实的分析内容\n"
            "- 正文中有 [Ref-N] 引用标注\n"
            "- 结尾有完整的参考文献列表\n"
            "- 总字数不少于 2000 字\n"
            "- 规范的 Markdown 格式"
        ),
        agent=analyst,
        context=context,
    )


def create_review_task(
    topic: str,
    supervisor: Agent,
    context: list[Task],
) -> Task:
    """
    Create a streamlined review task for quick quality check.
    """
    return Task(
        description=(
            f"快速审核关于「{topic}」的商业分析报告。\n\n"
            "【审核清单】检查以下项目：\n"
            "1. ✅ 报告是否包含所有必需章节？\n"
            "2. ✅ 正文是否有 [Ref-N] 引用？\n"
            "3. ✅ 是否有参考文献章节？\n"
            "4. ✅ 格式是否为规范的 Markdown？\n\n"
            "【审核原则】\n"
            "- 如果以上都满足：直接通过，输出最终报告\n"
            "- 不要反复修改，一次审核后立即输出\n"
            "- 不添加审核意见到报告正文中\n\n"
            "【输出】直接输出最终版本的报告（不包含审核意见）"
        ),
        expected_output=(
            "最终版本的中文商业分析报告（Markdown格式）。\n"
            "直接输出报告内容，不包含审核意见或批注。"
        ),
        agent=supervisor,
        context=context,
    )


def create_all_tasks(
    topic: str,
    researcher: Agent,
    analyst: Agent,
    supervisor: Agent,
    pre_search_data: Optional[str] = None,
) -> list[Task]:
    """
    Create all tasks for the business analysis pipeline.

    Args:
        topic: The topic to analyze
        researcher: Market Researcher agent
        analyst: Business Analyst agent
        supervisor: Quality Supervisor agent
        pre_search_data: Pre-fetched search results (optional)

    Returns:
        List of tasks in execution order
    """
    research_task = create_research_task(topic, researcher, pre_search_data)
    analysis_task = create_analysis_task(topic, analyst, context=[research_task])
    review_task = create_review_task(topic, supervisor, context=[analysis_task])

    return [research_task, analysis_task, review_task]
