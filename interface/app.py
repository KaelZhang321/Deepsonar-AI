"""
Chainlit Chat Interface for AI Business Data Analysis Platform.

This module provides the chat interface where users can:
1. Input a topic/keyword for analysis
2. Watch the AI agent team work in real-time
3. Receive and view the final business analysis report
4. Have reports saved to the Django database

IMPORTANT: This file must initialize Django before importing Django models.
Uses sync_to_async for Django ORM operations in async context.
"""
import os
import sys
from pathlib import Path

# =============================================================================
# DJANGO SETUP - Must be done before any Django imports
# =============================================================================

# Add the backend directory to the Python path
BACKEND_DIR = Path(__file__).resolve().parent.parent / "backend"
sys.path.insert(0, str(BACKEND_DIR))

# Set the Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings")

# Initialize Django
import django
django.setup()

# =============================================================================
# Now we can import Django models and async utilities
# =============================================================================

from apps.reports.models import Report
from asgiref.sync import sync_to_async

# =============================================================================
# Chainlit and CrewAI imports
# =============================================================================

import chainlit as cl
from dotenv import load_dotenv

# Add the project root to path for ai_engine imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_engine.crew import BusinessAnalysisCrew

# Load environment variables
load_dotenv()


# =============================================================================
# Async wrappers for Django ORM operations
# =============================================================================

@sync_to_async
def create_report(query: str) -> Report:
    """Create a new report record in the database."""
    return Report.objects.create(
        query=query,
        status=Report.Status.IN_PROGRESS,
    )


@sync_to_async
def mark_report_completed(report: Report, output: str) -> None:
    """Mark a report as completed with the given output."""
    report.mark_completed(output)


@sync_to_async
def mark_report_failed(report: Report, error_message: str) -> None:
    """Mark a report as failed with an error message."""
    report.mark_failed(error_message)


@sync_to_async
def get_recent_reports(limit: int = 5) -> list[Report]:
    """Get recent completed reports from the database."""
    return list(
        Report.objects.filter(
            status=Report.Status.COMPLETED
        ).order_by("-created_at")[:limit]
    )


# =============================================================================
# Chainlit Event Handlers
# =============================================================================

@cl.on_chat_start
async def on_chat_start() -> None:
    """
    Handler for when a new chat session starts.

    Sets up the session and displays a welcome message.
    """
    # Store the crew instance in the session for reuse
    crew = BusinessAnalysisCrew(verbose=True)
    cl.user_session.set("crew", crew)

    # Send welcome message
    await cl.Message(
        content=(
            "# 🔍 AI Business Analysis Platform\n\n"
            "Welcome! I'm your AI-powered business analysis assistant.\n\n"
            "**How it works:**\n"
            "1. Enter a topic or keyword (e.g., 'electric vehicles market')\n"
            "2. Our AI team will research and analyze the topic:\n"
            "   - 🔎 **Market Researcher** - Gathers data from the web\n"
            "   - 📊 **Business Analyst** - Writes a comprehensive report\n"
            "   - ✅ **Quality Supervisor** - Reviews and ensures quality\n"
            "3. Receive a professional business analysis report\n\n"
            "**Enter a topic to get started!**"
        )
    ).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """
    Handler for incoming user messages.

    Triggers the CrewAI analysis process and streams results.

    Args:
        message: The user's message containing the topic to analyze
    """
    topic = message.content.strip()

    if not topic:
        await cl.Message(content="Please enter a valid topic to analyze.").send()
        return

    # Create a Report record in the database (using async wrapper)
    report = await create_report(topic)

    # Send initial status message
    status_msg = cl.Message(content=f"🚀 Starting analysis for: **{topic}**\n\nThis may take a few minutes...")
    await status_msg.send()

    try:
        # Get the crew from session
        crew: BusinessAnalysisCrew = cl.user_session.get("crew")

        # Send progress updates
        await cl.Message(
            content="🔎 **Market Researcher** is gathering data..."
        ).send()

        # Run the crew (this is the main AI processing)
        # Using run_async for better async compatibility with Chainlit
        result = await crew.run_async(topic)
        
        # Ensure result is a string
        if result is None:
            result = "No output generated. Please try again."
        elif hasattr(result, 'raw'):
            result = str(result.raw)
        elif hasattr(result, 'output'):
            result = str(result.output)
        else:
            result = str(result)

        # Update progress
        await cl.Message(
            content="✅ **Quality Supervisor** has approved the final report!"
        ).send()

        # Save the result to the database (using async wrapper)
        await mark_report_completed(report, result)

        # Send the final report as a separate message with clear formatting
        report_content = f"""# 📊 Business Analysis Report

**Topic:** {topic}

**Report ID:** {report.id}

---

{result}

---

✅ *Report saved to database successfully*
"""
        final_msg = cl.Message(content=report_content)
        await final_msg.send()

    except Exception as e:
        # Handle errors (using async wrapper)
        error_message = str(e)
        await mark_report_failed(report, error_message)

        await cl.Message(
            content=(
                f"❌ **Error during analysis:**\n\n"
                f"```\n{error_message}\n```\n\n"
                f"Please check your API keys and try again."
            )
        ).send()


@cl.on_stop
async def on_stop() -> None:
    """Handler for when the user stops the current task."""
    await cl.Message(content="⏹️ Analysis stopped.").send()


# =============================================================================
# Additional Chainlit Actions (Optional)
# =============================================================================

@cl.action_callback("view_history")
async def view_history(action: cl.Action) -> None:
    """
    Action to view previous reports.

    Displays the user's report history from the database.
    """
    # Get recent reports (using async wrapper)
    recent_reports = await get_recent_reports(5)

    if not recent_reports:
        await cl.Message(content="No previous reports found.").send()
        return

    history_text = "# 📚 Recent Reports\n\n"
    for report in recent_reports:
        history_text += (
            f"- **{report.query[:50]}...** "
            f"(ID: {report.id}, {report.created_at.strftime('%Y-%m-%d %H:%M')})\n"
        )

    await cl.Message(content=history_text).send()


# =============================================================================
# Run Configuration
# =============================================================================

if __name__ == "__main__":
    # This allows running with: python app.py
    # But the recommended way is: chainlit run app.py
    print("To run this app, use: chainlit run app.py")

