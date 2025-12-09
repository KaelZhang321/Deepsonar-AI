"""
CrewAI Task definitions for the Business Data Analysis Platform.

This module defines the tasks that agents will perform:
1. Research Task - Gather market data
2. Analysis Task - Write the business report
3. Review Task - Quality review with delegation capability

The tasks form a pipeline where each builds on the previous output.
"""
from crewai import Task, Agent


def create_research_task(topic: str, researcher: Agent) -> Task:
    """
    Create the research task for gathering market data.

    Args:
        topic: The keyword or topic to research
        researcher: The Market Researcher agent

    Returns:
        Configured research Task
    """
    return Task(
        description=(
            f"Conduct comprehensive research on the topic: '{topic}'\n\n"
            "Your research should cover:\n"
            "1. Market overview and size\n"
            "2. Key players and competitors\n"
            "3. Recent trends and developments\n"
            "4. Challenges and opportunities\n"
            "5. Future outlook and predictions\n\n"
            "Use web search tools to gather current and relevant information. "
            "Focus on authoritative sources and recent data (within the last 2 years). "
            "Compile your findings in a structured format that the analyst can use."
        ),
        expected_output=(
            "A comprehensive research document containing:\n"
            "- Executive summary of findings\n"
            "- Detailed data points with sources\n"
            "- Key statistics and metrics\n"
            "- Notable trends and patterns\n"
            "- List of major players/competitors"
        ),
        agent=researcher,
    )


def create_analysis_task(topic: str, analyst: Agent, context: list[Task]) -> Task:
    """
    Create the analysis task for writing the business report.

    Args:
        topic: The original topic being analyzed
        analyst: The Business Analyst agent
        context: List of tasks whose output this task depends on

    Returns:
        Configured analysis Task
    """
    return Task(
        description=(
            f"Analyze the research data about '{topic}' and create a comprehensive "
            "business analysis report.\n\n"
            "Your report should include:\n"
            "1. Executive Summary\n"
            "2. Market Analysis\n"
            "3. Competitive Landscape\n"
            "4. SWOT Analysis (Strengths, Weaknesses, Opportunities, Threats)\n"
            "5. Key Insights and Findings\n"
            "6. Strategic Recommendations\n"
            "7. Conclusion\n\n"
            "Format the report in clean Markdown with proper headings, "
            "bullet points, and data tables where appropriate. "
            "Make the report professional and actionable."
        ),
        expected_output=(
            "A well-structured Markdown business analysis report with:\n"
            "- Clear section headings\n"
            "- Data-backed insights\n"
            "- Professional formatting\n"
            "- Actionable recommendations\n"
            "- Length: 1000-2000 words"
        ),
        agent=analyst,
        context=context,  # Depends on research task output
    )


def create_review_task(
    topic: str,
    supervisor: Agent,
    context: list[Task],
) -> Task:
    """
    Create the review task for quality supervision.

    SUPERVISION/REVIEW LOGIC:
    -------------------------
    This task implements quality control where the supervisor:

    1. EVALUATES the report against criteria:
       - Completeness: All required sections present
       - Accuracy: Claims are supported by research data
       - Clarity: Writing is clear and professional
       - Value: Recommendations are actionable

    2. DECIDES on action:
       - If quality is HIGH: Approve and output the final report
       - If quality needs improvement: Provide specific feedback

    3. The supervisor can DELEGATE back to the analyst if major
       revisions are needed, thanks to allow_delegation=True

    Args:
        topic: The original topic being analyzed
        supervisor: The Quality Supervisor agent
        context: List of tasks whose output this task depends on

    Returns:
        Configured review Task
    """
    return Task(
        description=(
            f"Review the business analysis report about '{topic}' for quality, "
            "accuracy, and completeness.\n\n"
            "EVALUATION CRITERIA:\n"
            "1. Completeness: Are all required sections present and thorough?\n"
            "2. Accuracy: Are claims supported by the research data?\n"
            "3. Clarity: Is the writing clear, professional, and well-organized?\n"
            "4. Value: Are the recommendations actionable and strategic?\n"
            "5. Format: Is the Markdown formatting correct and consistent?\n\n"
            "REVIEW PROCESS:\n"
            "- If the report meets all criteria: Approve and output the final version\n"
            "- If improvements are needed: Provide specific, constructive feedback\n"
            "- For minor issues: Make direct edits to improve the report\n"
            "- For major issues: Delegate back to the analyst with clear instructions\n\n"
            "Your final output should be the polished, approved version of the report."
        ),
        expected_output=(
            "The final, approved business analysis report in Markdown format.\n"
            "This should be a polished, professional document ready for "
            "delivery to stakeholders. Include a brief approval note at the end "
            "indicating any revisions made during review."
        ),
        agent=supervisor,
        context=context,  # Depends on analysis task output
    )


def create_all_tasks(
    topic: str,
    researcher: Agent,
    analyst: Agent,
    supervisor: Agent,
) -> list[Task]:
    """
    Create all tasks for the business analysis pipeline.

    Args:
        topic: The topic to analyze
        researcher: Market Researcher agent
        analyst: Business Analyst agent
        supervisor: Quality Supervisor agent

    Returns:
        List of tasks in execution order
    """
    research_task = create_research_task(topic, researcher)
    analysis_task = create_analysis_task(topic, analyst, context=[research_task])
    review_task = create_review_task(topic, supervisor, context=[analysis_task])

    return [research_task, analysis_task, review_task]
