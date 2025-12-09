"""
Chainlit Chat Interface for AI Business Data Analysis Platform.

This module provides the chat interface where users can:
1. Authenticate using Django's user system
2. Input a topic/keyword for analysis
3. Watch the AI agent team work in real-time
4. Receive and view the final business analysis report
5. Have all chat history saved to the Django database
6. View chat history in the sidebar

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
import chainlit.data
from dotenv import load_dotenv
import re


def filter_review_content(content: str) -> str:
    """
    Filter out review/audit opinion sections from the report content.
    Removes sections that contain quality review feedback.
    """
    if not content:
        return content
    
    # Patterns to remove (review-related sections)
    patterns_to_remove = [
        # Chinese review section headers (any heading level)
        r'#{1,6}\s*审核意见.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*质量审核.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*审核反馈.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*修改建议.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*审核结果.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*审核总结.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*审核评价.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*报告审核.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*质量评估.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*审核通过.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*Supervisor.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*Review.*?(?=\n#{1,6}\s|\Z)',
        # English review section headers
        r'#{1,6}\s*Quality\s*Review.*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*Audit\s*(Opinion|Feedback|Summary).*?(?=\n#{1,6}\s|\Z)',
        r'#{1,6}\s*Final\s*Review.*?(?=\n#{1,6}\s|\Z)',
        # Inline review markers (bold)
        r'\*\*审核意见[：:]\*\*.*?(?=\n\n|\n#|\Z)',
        r'\*\*质量审核[：:]\*\*.*?(?=\n\n|\n#|\Z)',
        r'\*\*审核结果[：:]\*\*.*?(?=\n\n|\n#|\Z)',
        r'\*\*审核通过[：:]\*\*.*?(?=\n\n|\n#|\Z)',
        r'\*\*Supervisor[：:]\*\*.*?(?=\n\n|\n#|\Z)',
        # Lines starting with review keywords
        r'^审核意见[：:].*$',
        r'^质量审核[：:].*$',
        r'^审核结果[：:].*$',
        r'^本报告审核.*$',
        r'^经审核.*$',
        # Paragraphs containing review statements
        r'作为质量审核.*?(?=\n\n|\Z)',
        r'经过审核.*?(?=\n\n|\Z)',
        r'审核认为.*?(?=\n\n|\Z)',
        r'审核建议.*?(?=\n\n|\Z)',
    ]
    
    filtered = content
    for pattern in patterns_to_remove:
        filtered = re.sub(pattern, '', filtered, flags=re.DOTALL | re.IGNORECASE | re.MULTILINE)
    
    # Clean up multiple consecutive blank lines
    filtered = re.sub(r'\n{3,}', '\n\n', filtered)
    # Clean up lines with only dashes/separators after removed content
    filtered = re.sub(r'\n---\s*\n---', '\n---', filtered)
    
    return filtered.strip()


# Add the project root to path for ai_engine imports
PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from ai_engine.crew import BusinessAnalysisCrew
from data_layer import DjangoDataLayer

# Load environment variables
load_dotenv()

# =============================================================================
# Initialize the data layer for sidebar chat history
# =============================================================================
# Set the data layer directly for Chainlit 2.9.3
chainlit.data._data_layer = DjangoDataLayer()


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


@sync_to_async
def get_user_chat_sessions(user) -> list[dict]:
    """Get all chat sessions for a user."""
    if user is None:
        return []
    sessions = ChatSession.objects.filter(user=user).order_by('-created_at')[:10]
    return [
        {
            "id": s.id,
            "title": s.title,
            "created_at": s.created_at.strftime("%Y-%m-%d %H:%M"),
            "message_count": s.messages.count()
        }
        for s in sessions
    ]


@sync_to_async
def get_session_history(session_id: int) -> list[dict]:
    """Get full message history for a session."""
    try:
        session = ChatSession.objects.get(id=session_id)
        messages = session.messages.order_by('timestamp')
        return [
            {
                "sender": m.sender,
                "content": m.content[:500] + "..." if len(m.content) > 500 else m.content,
                "timestamp": m.timestamp.strftime("%H:%M")
            }
            for m in messages
        ]
    except ChatSession.DoesNotExist:
        return []


@sync_to_async
def get_user_reports(user) -> list[dict]:
    """Get completed reports for a user."""
    if user is None:
        return []
    reports = Report.objects.filter(user=user, status=Report.Status.COMPLETED).order_by('-created_at')[:10]
    return [
        {
            "id": r.id,
            "query": r.query[:50],
            "created_at": r.created_at.strftime("%Y-%m-%d %H:%M"),
        }
        for r in reports
    ]


@sync_to_async
def update_session_title(session: ChatSession, title: str) -> None:
    """Update the title of a chat session."""
    session.title = title[:100]
    session.save()


@sync_to_async
def get_chat_session_by_id(session_id: int) -> Optional[ChatSession]:
    """Get a chat session by ID."""
    try:
        return ChatSession.objects.get(id=session_id)
    except ChatSession.DoesNotExist:
        return None


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

@cl.on_chat_resume
async def on_chat_resume(thread: dict):
    """
    Handler for when a chat session is resumed (page reload/tab switch).
    
    This prevents the welcome message from being shown again when users
    switch tabs and come back to the page.
    """
    # Restore user info
    user_info = cl.user_session.get("user")
    username = user_info.identifier if user_info else "Anonymous"
    user_id = user_info.metadata.get("user_id") if user_info else None
    
    # Get Django user object if logged in
    django_user = None
    if user_id:
        django_user = await get_user_by_username(username)
    
    # Recreate crew instance (it's stateless)
    crew = BusinessAnalysisCrew(verbose=True)
    cl.user_session.set("crew", crew)
    cl.user_session.set("django_user", django_user)
    cl.user_session.set("session_initialized", True)  # Mark as resumed
    
    # Send a brief resume message instead of full welcome
    await cl.Message(
        content=f"💡 **会话已恢复** - 欢迎回来，{username}！您可以继续输入主题进行分析。"
    ).send()


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
    
    # Note: ChatSession is created lazily on first message to avoid empty entries
    cl.user_session.set("chat_session", None)  # Will be created on first message
    cl.user_session.set("session_initialized", False)

    # Create action button for history
    actions = [
        cl.Action(
            name="view_history",
            payload={"action": "history"},
            label="📜 查看对话历史",
        )
    ]

    # Send welcome message with action buttons
    welcome_msg = f"""# 🔍 DeepSonar AI 商业分析平台

欢迎您，**{username}**！我是您的 AI 商业分析助手。

**使用说明：**
1. 输入一个主题或关键词（例如：'新能源汽车市场'、'人工智能行业'）
2. 我们的 AI 团队将自动研究和分析该主题：
   - 🔎 **市场研究专家** - 收集市场数据和行业情报
   - 📊 **商业分析师** - 撰写深度分析报告
   - ✅ **质量审核总监** - 审核确保报告质量
3. 获取一份专业的商业分析报告

📊 **[查看历史报告](http://localhost:8000/reports/)** - 支持导出为 Markdown、Word、PDF

**请输入一个主题开始分析！**
"""
    await cl.Message(content=welcome_msg, actions=actions).send()


@cl.action_callback("view_history")
async def on_action_view_history(action: cl.Action):
    """Handle the view history action button."""
    django_user = cl.user_session.get("django_user")
    
    if django_user is None:
        await cl.Message(content="⚠️ 请先登录以查看对话历史。").send()
        return
    
    sessions = await get_user_chat_sessions(django_user)
    
    if not sessions:
        await cl.Message(content="📭 暂无对话历史。开始一次对话来创建历史记录！").send()
        return
    
    # Format history as a nice list
    history_text = "# 📜 您的对话历史\n\n"
    history_text += "| # | 会话标题 | 日期 | 消息数 |\n"
    history_text += "|---|---------|------|--------|\n"
    
    for i, session in enumerate(sessions, 1):
        history_text += f"| {i} | {session['title'][:30]} | {session['created_at']} | {session['message_count']} |\n"
    
    history_text += "\n*显示最近10条会话*"
    
    await cl.Message(content=history_text).send()


# Note: view_reports button removed - reports are now available at http://localhost:8000/reports/


@cl.on_message
async def on_message(message: cl.Message) -> None:
    """
    Handler for incoming user messages.

    Saves the message to database, triggers the CrewAI analysis, and streams results
    with real-time progress updates using Chainlit Steps.
    """
    topic = message.content.strip()

    if not topic:
        await cl.Message(content="Please enter a valid topic to analyze.").send()
        return

    # Get session info
    chat_session: ChatSession = cl.user_session.get("chat_session")
    django_user = cl.user_session.get("django_user")
    session_initialized = cl.user_session.get("session_initialized", False)
    
    # Create chat session on first message (lazy initialization)
    if not session_initialized:
        chat_session = await create_chat_session(
            user=django_user,
            title=topic[:50]  # Use first message as title
        )
        cl.user_session.set("chat_session", chat_session)
        cl.user_session.set("session_initialized", True)
        # Set thread_id for Chainlit data layer
        cl.user_session.set("thread_id", str(chat_session.id))
    elif chat_session and chat_session.title == "New Chat":
        # Update session title with the topic (for sidebar display)
        await update_session_title(chat_session, topic[:50])
    
    # Save user message to database
    await save_chat_message(
        session=chat_session,
        sender=ChatMessage.Sender.USER,
        content=topic
    )

    # Create a Report record in the database
    report = await create_report(topic, django_user)

    # Create live log side panel
    # We use a simple alphanumeric name to ensure binding works correctly
    side_view_name = "live_logs" 
    side_view = cl.Text(
        name=side_view_name,
        content="🚀 系统启动，初始化智能体团队...\n",
        display="side",
        language="bash"
    )
    
    # Send initial status message
    # Attaching side_view here makes it available immediately
    init_msg = cl.Message(
        content=f"🚀 **Starting analysis for:** {topic}\n\n👇 *详细日志已生成，请查看侧边栏或点击下方 {side_view_name}*",
        elements=[side_view]
    )
    await init_msg.send()

    # Define simple log stream manager
    class LogStream:
        def __init__(self, element, msg_id):
            self.element = element
            self.content = element.content
            self.msg_id = msg_id

        async def update(self):
            """Async update method using robust strategies."""
            self.element.content = self.content
            
            # Strategy 1: Try update()
            if hasattr(self.element, "update"):
                try:
                    await self.element.update()
                    return
                except Exception:
                    pass
            
            # Strategy 2: Re-send (Overwrite) to same message
            try:
                # Note: Sending the element again updates it if name matches?
                # Or we can update the message elements?
                await self.element.send(for_id=self.msg_id)
            except Exception:
                pass

        def append_sync(self, text):
            # Add line buffering to prevent too frequent updates? 
            # For now append directly
            self.content += f"{text}\n"

    log_stream = LogStream(side_view, init_msg.id)

    # Define step callback for CrewAI
    def handle_agent_step(step_output):
        """Callback for every agent step to update the UI."""
        # Extract thought/log content
        thought = str(step_output)
        if hasattr(step_output, 'thought'):
             thought = step_output.thought
        elif isinstance(step_output, dict) and 'thought' in step_output:
            thought = step_output['thought']
        elif isinstance(step_output, tuple) and len(step_output) > 0:
            thought = str(step_output[0])
            
        log_entry = (
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n" 
            f"🤖 Agent 动作检测:\n" 
            f"{thought}\n" 
            f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n"
        )
        
        # Update UI asynchronously from sync callback
        cl.run_sync(
            async_append_log(log_stream, log_entry)
        )

    async def async_append_log(stream, text):
        """Async helper to append logs."""
        stream.append_sync(text)
        await stream.update()

    try:
        # Get the crew from session
        crew: BusinessAnalysisCrew = cl.user_session.get("crew")

        # Run the actual crew with live logging
        log_stream.append_sync("✅ 团队组建完成，开始执行任务...")
        await log_stream.update()
        
        # We need to run run_async but pass the sync handle_agent_step callback
        # The handle_agent_step callback itself handles the sync->async bridge
        
        # Note: We pass handle_agent_step as the callback for live logging
        result = await crew.run_async(topic, step_callback=handle_agent_step)
        
        # === FINAL REPORT DISPLAY ===
        # Switch side panel to report mode
        
        # Ensure result is a string for display
        if result is None:
            display_result = "No output generated."
        elif hasattr(result, 'raw'):
            display_result = str(result.raw)
        elif hasattr(result, 'output'):
            display_result = str(result.output)
        else:
            display_result = str(result)
            
        side_view.content = display_result
        side_view.language = "markdown"
        side_view.name = "✅ 最终深度分析报告"
        
        if hasattr(side_view, "update"):
            await side_view.update()
        else:
            await side_view.send(for_id=init_msg.id)
        
        await cl.Message(
            content=f"🎉 **{topic}** 分析完成！\n\n👉 请查看右侧面板阅读完整报告。",
        ).send()

        # Save the result to the database (filter out review/audit opinions)
        filtered_result = filter_review_content(result)
        await mark_report_completed(report, filtered_result)
        
        # Save AI response to chat history
        await save_chat_message(
            session=chat_session,
            sender=ChatMessage.Sender.AI,
            content=result
        )

        # Send the final report (also in main chat)
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
        # Log to side panel if possible
        log_stream.append_sync(f"\n❌ 错误: {error_message}")
        try:
            await log_stream.update()
        except:
            pass
            
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


@cl.on_chat_resume
async def on_chat_resume(thread: dict) -> None:
    """
    Handler for resuming a previous chat session from the sidebar.
    
    Loads the session and displays previous messages.
    """
    thread_id = thread.get("id")
    if not thread_id:
        return
    
    try:
        # Get the chat session from database
        session_id = int(thread_id)
        chat_session = await get_chat_session_by_id(session_id)
        
        if not chat_session:
            await cl.Message(content="⚠️ Session not found.").send()
            return
        
        # Set up the session
        cl.user_session.set("chat_session", chat_session)
        cl.user_session.set("thread_id", thread_id)
        
        # Initialize the crew
        crew = BusinessAnalysisCrew(verbose=True)
        cl.user_session.set("crew", crew)
        
        # Get user info
        user_info = cl.user_session.get("user")
        if user_info:
            django_user = await get_user_by_username(user_info.identifier)
            cl.user_session.set("django_user", django_user)
        
        # Load and display previous messages
        messages = await get_session_history(session_id)
        
        if messages:
            history_text = f"**📜 Previous conversation: {chat_session.title}**\n\n"
            for msg in messages[-5:]:  # Show last 5 messages
                sender_icon = "👤" if msg["sender"] == "user" else "🤖"
                content_preview = msg["content"][:200] + "..." if len(msg["content"]) > 200 else msg["content"]
                history_text += f"{sender_icon} **{msg['sender'].upper()}** ({msg['timestamp']}):\n{content_preview}\n\n"
            
            history_text += "---\n*Continue the conversation below...*"
            await cl.Message(content=history_text).send()
        else:
            await cl.Message(content=f"📄 Resumed session: **{chat_session.title}**\n\nEnter a new topic to analyze.").send()
    
    except (ValueError, Exception) as e:
        await cl.Message(content=f"⚠️ Error loading session: {str(e)}").send()


# =============================================================================
# Run Configuration
# =============================================================================

if __name__ == "__main__":
    print("To run this app, use: chainlit run app.py")

