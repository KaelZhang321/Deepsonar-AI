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
def check_user_can_generate(user: Optional[User]) -> tuple[bool, int, int, bool]:
    """
    Check if user can generate a report based on membership and monthly limits.
    
    Returns:
        (can_generate, remaining_reports, monthly_limit, is_expired)
    """
    if user is None:
        return False, 0, 0, True
    
    is_active = user.is_membership_active()
    can_gen = user.can_generate_report()
    remaining = user.get_remaining_reports()
    limit = user.get_monthly_report_limit()
    is_expired = not is_active
    return can_gen, remaining, limit, is_expired


@sync_to_async
def increment_user_report_count(user: Optional[User]) -> None:
    """Increment the user's monthly report count after successful generation."""
    if user is not None:
        user.increment_report_count()


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

@cl.header_auth_callback
async def header_auth_callback(headers: dict) -> Optional[cl.User]:
    """
    SSO Authentication via JWT cookie.
    
    This callback is triggered first and allows automatic login
    when user has already authenticated via Django.
    """
    import jwt
    
    # Try to get the SSO cookie from headers
    cookie_header = headers.get("cookie", "")
    
    # Parse cookie to extract deepsonar_sso_token
    token = None
    for cookie in cookie_header.split(";"):
        cookie = cookie.strip()
        if cookie.startswith("deepsonar_sso_token="):
            token = cookie.split("=", 1)[1]
            break
    
    if not token:
        print("🔐 [SSO] No token cookie found, falling back to password auth")
        return None
    
    try:
        # Verify JWT token
        jwt_secret = os.getenv('JWT_SECRET', os.getenv('DJANGO_SECRET_KEY', 'fallback-secret'))
        payload = jwt.decode(token, jwt_secret, algorithms=['HS256'])
        
        username = payload.get('username')
        user_id = payload.get('user_id')
        email = payload.get('email', '')
        
        if username and user_id:
            print(f"🔐 [SSO] Auto-login successful for user: {username}")
            return cl.User(
                identifier=username,
                metadata={
                    "user_id": user_id,
                    "email": email,
                    "sso": True,
                }
            )
    except jwt.ExpiredSignatureError:
        print("🔐 [SSO] Token expired, falling back to password auth")
    except jwt.InvalidTokenError as e:
        print(f"🔐 [SSO] Invalid token: {e}, falling back to password auth")
    except Exception as e:
        print(f"🔐 [SSO] Error: {e}")
    
    return None


@cl.password_auth_callback
async def auth_callback(username: str, password: str) -> Optional[cl.User]:
    """
    Authenticate users against Django database.
    
    This callback is triggered when a user attempts to log in via Chainlit.
    This is a fallback when SSO header auth fails or is not available.
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


@cl.on_logout
def on_logout(request, response):
    """
    Handle user logout from Chainlit.
    
    Clear SSO cookie and redirect to Django login page.
    """
    # Clear the SSO cookies
    cookie_domain = os.getenv('SSO_COOKIE_DOMAIN', '.deepsonar.com.cn')
    response.delete_cookie('deepsonar_sso_token', domain=cookie_domain)
    response.delete_cookie('deepsonar_sso_active', domain=cookie_domain)
    
    # Get Django login URL
    django_url = os.getenv('DJANGO_URL', 'http://www.deepsonar.com.cn')
    login_url = f"{django_url}/login/"
    
    # Set redirect headers
    response.status_code = 302
    response.headers["Location"] = login_url
    
    print(f"🔐 [SSO] Logout: cleared cookies, redirecting to {login_url}")


# =============================================================================
# Chainlit Event Handlers
# =============================================================================

@cl.on_chat_resume
async def on_chat_resume(thread: dict):
    """
    Handler for when a chat session is resumed from sidebar history.
    
    This restores the chat history and allows users to continue the conversation.
    The `thread` dict contains 'steps' which are the historical messages.
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
    
    # Restore chat session from thread_id
    thread_id = thread.get("id")
    if thread_id:
        chat_session = await get_chat_session_by_id(int(thread_id))
        cl.user_session.set("chat_session", chat_session)
        cl.user_session.set("thread_id", thread_id)
    
    # Restore historical messages from thread steps
    # Chainlit 2.9.3+ automatically displays steps, but we need to ensure they're formatted correctly
    steps = thread.get("steps", [])
    if steps:
        # Log for debugging
        print(f"📜 [Chat Resume] Restoring {len(steps)} messages for thread {thread_id}")
        
        # Note: Chainlit automatically restores messages from steps if data layer is configured correctly
        # The steps are displayed in the "Previous conversation" section
        # If you need to manually restore them to the main chat, uncomment below:
        # for step in steps:
        #     if step.get("type") == "user_message":
        #         await cl.Message(content=step.get("output", ""), author="user").send()
        #     else:
        #         await cl.Message(content=step.get("output", "")).send()
    
    # Send a brief resume message
    thread_name = thread.get("name", "对话")
    await cl.Message(
        content=f"💡 **会话已恢复** - 欢迎回来，{username}！\n\n📜 上次话题：**{thread_name}**\n\n您可以继续输入主题进行分析。"
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

📊 **[查看历史报告]({os.getenv('DJANGO_URL', 'http://www.deepsonar.com.cn')}/reports/)** - 支持导出为 Markdown、Word、PDF

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


# Note: view_reports button removed - reports are now available at http://www.deepsonar.com.cn/reports/


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

    # Check if user can generate a report (membership + monthly limit check)
    if django_user:
        can_generate, remaining, monthly_limit, is_expired = await check_user_can_generate(django_user)
        if not can_generate:
            if is_expired:
                # Membership expired
                expires_str = django_user.membership_expires_at.strftime('%Y年%m月%d日') if django_user.membership_expires_at else "未知日期"
                expired_msg = f"""⚠️ **会员已过期**

您的 **{django_user.get_membership_level_display()}** 会员已于 **{expires_str}** 到期。

🔒 会员过期后无法生成新报告，但您仍可以：
- 查看历史报告
- 导出已生成的报告

🚀 **续费或升级会员** 即可继续使用：
- 入门版 (Starter)：每月 30 份报告
- 专业版 (Pro)：每月 100 份报告
- 企业版 (Enterprise)：每月 600 份报告
"""
                await cl.Message(content=expired_msg).send()
            else:
                # Quota exceeded
                limit_msg = f"""⚠️ **本月报告生成次数已达上限**

您的会员等级为 **{django_user.get_membership_level_display()}**，每月最多生成 **{monthly_limit}** 份报告。

📅 本月剩余次数：**{remaining}** 份
⏰ 次数将于下月 1 日重置

🚀 **升级会员** 可获得更多每月报告次数：
- 入门版 (Starter)：每月 30 份
- 专业版 (Pro)：每月 100 份
- 企业版 (Enterprise)：每月 600 份
"""
                await cl.Message(content=limit_msg).send()
            return

    # Create a Report record in the database
    # Debug: Log user association for troubleshooting
    if django_user:
        print(f"📝 [Report Creation] User: {django_user.username} (ID: {django_user.id}), Topic: {topic[:30]}...")
    else:
        print(f"⚠️ [Report Creation] No user associated! Topic: {topic[:30]}...")
    
    report = await create_report(topic, django_user)

    # Send initial status message
    init_msg = await cl.Message(
        content=f"🚀 **Starting analysis for:** {topic}\n\n⏳ *正在生成详细日志，请稍候...*",
    ).send()

    # Create a streaming message for live logs
    log_msg = cl.Message(content="")
    await log_msg.send()
    
    # Define simple log stream manager using message streaming
    class LogStream:
        def __init__(self, message):
            self.message = message
            self.content = ""
        
        async def log(self, text: str):
            """Stream a new log line."""
            line = f"{text}\n"
            self.content += line
            await self.message.stream_token(line)
        
        async def log_separator(self):
            """Add a visual separator."""
            await self.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        
        # Aliases for compatibility
        def append_sync(self, text):
            """Sync append - adds to buffer."""
            self.content += f"{text}\n"
        
        async def update(self):
            """Stream any buffered content."""
            if self.content:
                # Find content that hasn't been streamed yet
                current_output = self.message.content or ""
                if len(self.content) > len(current_output):
                    new_content = self.content[len(current_output):]
                    if new_content:
                        await self.message.stream_token(new_content)

    log_stream = LogStream(log_msg)

    # ==========================
    # 🧠 Google Deep Research Mode - Intent Decomposition (Planning Phase)
    # ==========================
    await log_stream.log_separator()
    await log_stream.log(f"📌 分析主题: {topic}")
    await log_stream.log_separator()
    await log_stream.log("")
    await log_stream.log("🧠 [阶段 1/4] 意图拆解与研究路径规划...")
    await log_stream.log("   → 正在分析主题的核心研究方向")
    
    # Use the same LLM config as agents
    import os
    from litellm import completion
    
    plan_prompt = f"""
用户想研究: "{topic}"。
请作为一名资深商业分析师，将这个主题拆解为 3 个具体的、互不重叠的子研究方向。
每个方向应该是一个可以独立搜索的具体问题或数据需求。

只返回 3 行文本，每行一个方向，不要其他任何内容。
示例格式:
1. [具体方向1]
2. [具体方向2]
3. [具体方向3]
"""
    
    try:
        await log_stream.log("   → 调用 AI 分析研究方向...")
        
        plan_response = await cl.make_async(lambda: completion(
            model="openai/" + os.getenv("ARK_MODEL_ENDPOINT", "ep-20250603140551-tp9lt"),
            messages=[{"role": "user", "content": plan_prompt}],
            api_key=os.getenv("ARK_API_KEY"),
            base_url=os.getenv("ARK_BASE_URL", "https://ark.cn-beijing.volces.com/api/v3"),
            max_tokens=500
        ))()
        
        plan_text = plan_response.choices[0].message.content.strip()
        
        await log_stream.log("   ✅ 研究方向规划完成:")
        for line in plan_text.split('\n'):
            if line.strip():
                await log_stream.log(f"      {line.strip()}")
        await log_stream.log("")
        
        # Construct enhanced input with the research plan
        enhanced_topic = f"""
研究主题: {topic}

请重点围绕以下三个维度进行深度研究和数据搜集:
{plan_text}

请确保针对每个维度都进行独立的搜索和分析，最终整合成一份完整的报告。
"""
    except Exception as e:
        # Fallback to original topic if planning fails
        await log_stream.log(f"⚠️ 规划阶段出现问题，使用原始主题: {str(e)}")
        enhanced_topic = topic

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
        await stream.log(text)

    try:
        # === USE LONG REPORT GENERATION AS DEFAULT ===
        # This uses the "Divide and Conquer" chapter-by-chapter approach
        # for higher quality, longer reports with deduplicated references
        
        await log_stream.log("")
        await log_stream.log("📝 [阶段 2/4] 生成报告大纲...")
        await log_stream.log("   → 正在规划报告结构和章节")
        
        # Generate long-form report with chapter-by-chapter approach
        result = await generate_long_report(
            topic=topic,  # Use original topic, outline generation handles decomposition
            log_stream=log_stream,
            log_msg=log_msg,
            init_msg=init_msg
        )
        
        # === FINAL REPORT DISPLAY ===
        
        # Ensure result is a string for display
        if result is None:
            display_result = "No output generated."
        elif hasattr(result, 'raw'):
            display_result = str(result.raw)
        elif hasattr(result, 'output'):
            display_result = str(result.output)
        else:
            display_result = str(result)
        
        await cl.Message(
            content=f"🎉 **{topic}** 分析完成！\n\n📄 *完整报告已在下方展示*",
        ).send()

        # Save the result to the database (filter out review/audit opinions)
        filtered_result = filter_review_content(result)
        await mark_report_completed(report, filtered_result)
        
        # Increment user's daily report count
        await increment_user_report_count(django_user)
        
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
        # Log error to stream
        try:
            await log_stream.log(f"\n❌ 错误: {error_message}")
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


async def generate_long_report(topic: str, log_stream, log_msg, init_msg) -> str:
    """
    Generate an ultra-long report using chapter-by-chapter approach.
    
    This implements the "Divide and Conquer" pattern:
    1. Generate outline with LLM
    2. Generate each chapter independently with focused search
    3. Deduplicate and merge references globally
    4. Assemble final document
    
    Args:
        topic: The report topic
        log_stream: LogStream instance for UI updates
        log_msg: cl.Message for log streaming
        init_msg: Initial message for UI binding
        
    Returns:
        Complete report as markdown string
    """
    from ai_engine.utils import GlobalReferenceManager
    from ai_engine.generator import (
        generate_report_outline, 
        generate_single_chapter,
        summarize_chapter
    )
    
    # Initialize reference manager
    ref_manager = GlobalReferenceManager()
    
    # --- Step 1: Generate Outline ---
    await log_stream.log("   → 正在调用 AI 生成大纲...")
    
    outline = await generate_report_outline(topic)
    
    await log_stream.log(f"   ✅ 大纲生成完成，共 {len(outline)} 章:")
    for ch in outline:
        await log_stream.log(f"      • {ch['title']}")
    await log_stream.log("")
    
    # Initialize report body
    full_report = f"# {topic} 深度行业分析报告\n\n"
    full_report += f"*生成时间: {__import__('datetime').datetime.now().strftime('%Y-%m-%d %H:%M')}*\n\n"
    full_report += "---\n\n"
    
    # Track previous chapter summaries for context continuity
    previous_summaries = []
    
    # --- Step 2: Generate Chapters ---
    await log_stream.log("📊 [阶段 3/4] 分章撰写报告...")
    await log_stream.log(f"   → 预计需要 {len(outline) * 1} - {len(outline) * 2} 分钟")
    await log_stream.log("")
    
    for index, chapter_info in enumerate(outline):
        chapter_title = chapter_info.get('title', f'章节 {index + 1}')
        chapter_focus = chapter_info.get('focus', '')
        
        # Update UI
        progress_bar = "█" * (index + 1) + "░" * (len(outline) - index - 1)
        await log_stream.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        await log_stream.log(f"📖 第 {index + 1}/{len(outline)} 章: {chapter_title}")
        await log_stream.log(f"   进度: [{progress_bar}] {(index + 1) * 100 // len(outline)}%")
        
        # Build context from previous chapters
        previous_context = ""
        if previous_summaries:
            previous_context = "前文摘要: " + " | ".join(previous_summaries[-2:])  # Last 2 chapters
        
        # Generate this chapter
        try:
            # Define log callback for this chapter
            async def chapter_log_callback(msg: str):
                await log_stream.log(msg)
            
            chapter_content, chapter_refs = await generate_single_chapter(
                topic=topic,
                chapter_info=chapter_info,
                previous_summary=previous_context,
                search_count=8,
                log_callback=chapter_log_callback
            )
            
            # Process references (deduplicate and rewrite IDs)
            processed_content = ref_manager.process_chapter_content(chapter_content, chapter_refs)
            
            # Add to report
            full_report += f"## {chapter_title}\n\n"
            full_report += processed_content
            full_report += "\n\n"
            
            # Update summary for next chapter's context
            chapter_summary = summarize_chapter(chapter_content, max_length=150)
            previous_summaries.append(f"{chapter_title}: {chapter_summary}")
            
            await log_stream.log(f"✅ 第 {index + 1} 章完成 ({len(chapter_content)} 字)")
                
        except Exception as e:
            await log_stream.log(f"⚠️ 第 {index + 1} 章生成失败: {str(e)}")
            full_report += f"## {chapter_title}\n\n*[章节生成失败]*\n\n"
    
    # --- Step 3: Add Final Bibliography ---
    await log_stream.log("")
    await log_stream.log("📚 [阶段 4/4] 整理参考文献...")
    
    bibliography = ref_manager.get_final_bibliography()
    full_report += bibliography
    
    ref_count = ref_manager.get_ref_count()
    await log_stream.log(f"   ✅ 参考文献整理完成，共 {ref_count} 条唯一引用")
    await log_stream.log("")
    await log_stream.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    await log_stream.log("🎉 报告生成完成！")
    await log_stream.log("━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
    
    return full_report


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

