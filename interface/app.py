"""
Chainlit Chat Interface for AI Business Data Analysis Platform.

This module provides the chat interface where users can:
1. Authenticate using Django's user system
2. Input a topic/keyword for analysis
3. Watch the AI agent team work in real-time
4. Receive and view the final business analysis report
5. Have all chat history saved to the Django database

IMPORTANT: This file must initialize Django before importing Django models.
"""
import os
import sys
from pathlib import Path
from typing import Optional

# =============================================================================
# DJANGO SETUP - Must be done FIRST before any Django imports
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

from django.contrib.auth import authenticate
from apps.reports.models import Report, ChatSession, ChatMessage
from apps.users.models import User
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
def django_authenticate(username: str, password: str) -> Optional[User]:
    """Authenticate user against Django database."""
    return authenticate(username=username, password=password)


@sync_to_async
def get_user_by_username(username: str) -> Optional[User]:
    """Get user by username."""
    try:
        return User.objects.get(username=username)
    except User.DoesNotExist:
        return None


@sync_to_async
def create_chat_session(user: Optional[User], title: str) -> ChatSession:
    """Create a new chat session."""
    return ChatSession.objects.create(
        user=user,
        title=title
    )


@sync_to_async
def save_chat_message(session: ChatSession, sender: str, content: str) -> ChatMessage:
    """Save a chat message to the database."""
    return ChatMessage.objects.create(
        session=session,
        sender=sender,
        content=content
    )


@sync_to_async
def create_report(query: str, user: Optional[User] = None) -> Report:
    """Create a new report record in the database."""
    return Report.objects.create(
        user=user,
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
def get_session_messages(session_id: int) -> list[dict]:
    """Get all messages for a session."""
    messages = ChatMessage.objects.filter(session_id=session_id).order_by('timestamp')
    return [{"sender": m.sender, "content": m.content} for m in messages]


# =============================================================================
# Chainlit Authentication
# =============================================================================

@cl.password_auth_callback
async def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """
    Authenticate users against Django database.
    
    This callback is triggered when a user attempts to log in via Chainlit.
    """
    user = await django_authenticate(username, password)
    
    if user is not None:
        return cl.User(
            identifier=username,
            metadata={
                "user_id": user.id,
                "email": user.email or "",
                "company": getattr(user, 'company', '') or "",
            }
        )
    return None


# =============================================================================
# Chainlit Event Handlers
# =============================================================================

@cl.on_chat_start
async def on_chat_start() -> None:
    """
    Handler for when a new chat session starts.

    Sets up the session, creates a database chat session, and displays welcome message.
    """
    # Get authenticated user info
    user_info = cl.user_session.get("user")
    username = user_info.identifier if user_info else "Anonymous"
    user_id = user_info.metadata.get("user_id") if user_info else None
    
    # Get Django user object if logged in
    django_user = None
    if user_id:
        django_user = await get_user_by_username(username)
    
    # Store the crew instance in the session for reuse
    crew = BusinessAnalysisCrew(verbose=True)
    cl.user_session.set("crew", crew)
    cl.user_session.set("django_user", django_user)
    
    # Create a new chat session in the database
    chat_session = await create_chat_session(
        user=django_user,
        title=f"Chat Session - {username}"
    )
    cl.user_session.set("chat_session", chat_session)

    # Send welcome message
    welcome_msg = f"""# 🔍 AI Business Analysis Platform

Welcome, **{username}**! I'm your AI-powered business analysis assistant.

**How it works:**
1. Enter a topic or keyword (e.g., 'electric vehicles market')
2. Our AI team will research and analyze the topic:
   - 🔎 **Market Researcher** - Gathers market data
   - 📊 **Business Analyst** - Writes comprehensive report
   - ✅ **Quality Supervisor** - Reviews and ensures quality
3. Receive a professional business analysis report

**Enter a topic to get started!**
"""
    await cl.Message(content=welcome_msg).send()


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """
    Handler for incoming user messages.

    Saves the message to database, triggers the CrewAI analysis, and streams results.
    """
    topic = message.content.strip()

    if not topic:
        await cl.Message(content="Please enter a valid topic to analyze.").send()
        return

    # Get session info
    chat_session: ChatSession = cl.user_session.get("chat_session")
    django_user = cl.user_session.get("django_user")
    
    # Save user message to database
    await save_chat_message(
        session=chat_session,
        sender=ChatMessage.Sender.USER,
        content=topic
    )

    # Create a Report record in the database
    report = await create_report(topic, django_user)

    # Send initial status message
    await cl.Message(
        content=f"🚀 **Starting analysis for:** {topic}\n\nThis may take a few minutes..."
    ).send()

    try:
        # Get the crew from session
        crew: BusinessAnalysisCrew = cl.user_session.get("crew")

        # Send progress updates
        await cl.Message(
            content="🔎 **Market Researcher** is gathering data..."
        ).send()

        # Run the crew (this is the main AI processing)
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

        # Save the result to the database
        await mark_report_completed(report, result)
        
        # Save AI response to chat history
        await save_chat_message(
            session=chat_session,
            sender=ChatMessage.Sender.AI,
            content=result
        )

        # Send the final report
        report_content = f"""# 📊 Business Analysis Report

**Topic:** {topic}

**Report ID:** {report.id}

---

{result}

---

✅ *Report saved to database successfully*
"""
        await cl.Message(content=report_content).send()

    except Exception as e:
        # Handle errors
        error_message = str(e)
        await mark_report_failed(report, error_message)
        
        # Save error to chat history
        await save_chat_message(
            session=chat_session,
            sender=ChatMessage.Sender.AI,
            content=f"Error: {error_message}"
        )

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


# Note: on_chat_resume is disabled due to Chainlit version compatibility
# @cl.on_chat_resume
# async def on_chat_resume(thread) -> None:
#     """Handler for resuming a previous chat session."""
#     crew = BusinessAnalysisCrew(verbose=True)
#     cl.user_session.set("crew", crew)


# =============================================================================
# Run Configuration
# =============================================================================

if __name__ == "__main__":
    print("To run this app, use: chainlit run app.py")

