"""
Custom Chainlit Data Layer using Django ORM.

This module implements Chainlit's BaseDataLayer to persist chat history
to Django's database and display it in the sidebar.
"""
import uuid
from typing import Dict, List, Optional
from datetime import datetime

from chainlit.data import BaseDataLayer
from chainlit.types import Pagination, ThreadFilter, ThreadDict, Feedback, PaginatedResponse, PageInfo
from chainlit.user import User as ChainlitUser, PersistedUser
from chainlit.element import ElementDict
from chainlit.step import StepDict

from asgiref.sync import sync_to_async

# Django imports (assuming Django is already set up)
from apps.reports.models import ChatSession, ChatMessage
from apps.users.models import User as DjangoUser


class DjangoDataLayer(BaseDataLayer):
    """
    Custom data layer that uses Django ORM for persistence.
    
    This enables the sidebar chat history feature in Chainlit.
    """
    
    def build_debug_url(self) -> str:
        """Build a debug URL (not used with Django backend)."""
        return ""
    
    async def close(self) -> None:
        """Close any open connections (Django handles this automatically)."""
        pass
    
    async def get_user(self, identifier: str) -> Optional[PersistedUser]:
        """Get a user by identifier. Returns PersistedUser for threads API."""
        try:
            django_user = await sync_to_async(DjangoUser.objects.get)(username=identifier)
            return PersistedUser(
                id=str(django_user.id),
                createdAt=django_user.date_joined.isoformat() if django_user.date_joined else datetime.now().isoformat(),
                identifier=django_user.username,
                metadata={
                    "user_id": django_user.id,
                    "email": django_user.email or "",
                }
            )
        except DjangoUser.DoesNotExist:
            return None
    
    async def create_user(self, user: ChainlitUser) -> Optional[PersistedUser]:
        """Create a new user (handled by Django auth, return as PersistedUser)."""
        return PersistedUser(
            id=user.metadata.get("user_id", str(uuid.uuid4())),
            createdAt=datetime.now().isoformat(),
            identifier=user.identifier,
            metadata=user.metadata
        )
    
    async def upsert_feedback(self, feedback: Feedback) -> str:
        """Store feedback (not implemented for MVP)."""
        return str(uuid.uuid4())
    
    async def create_element(self, element: ElementDict) -> Optional[ElementDict]:
        """Create an element (not implemented for MVP)."""
        return element
    
    async def get_element(
        self, thread_id: str, element_id: str
    ) -> Optional[ElementDict]:
        """Get an element (not implemented for MVP)."""
        return None
    
    async def delete_element(self, element_id: str, thread_id: Optional[str] = None) -> bool:
        """Delete an element (not implemented for MVP)."""
        return True
    
    async def create_step(self, step_dict: StepDict) -> Optional[StepDict]:
        """Save a step (message) to the database."""
        thread_id = step_dict.get("threadId")
        if not thread_id:
            return step_dict
        
        try:
            session_id = int(thread_id)
            content = step_dict.get("output", "") or step_dict.get("input", "")
            step_type = step_dict.get("type", "")
            
            # Determine sender based on step type
            if step_type == "user_message":
                sender = "user"
            else:
                sender = "ai"
            
            if content:
                await sync_to_async(ChatMessage.objects.create)(
                    session_id=session_id,
                    sender=sender,
                    content=content[:10000]  # Limit content length
                )
        except (ValueError, Exception):
            pass
        
        return step_dict
    
    async def update_step(self, step_dict: StepDict) -> Optional[StepDict]:
        """Update a step (not fully implemented for MVP)."""
        return step_dict
    
    async def delete_step(self, step_id: str) -> bool:
        """Delete a step (not implemented for MVP)."""
        return True
    
    async def get_thread_author(self, thread_id: str) -> Optional[str]:
        """Get the author of a thread."""
        try:
            session = await sync_to_async(ChatSession.objects.select_related('user').get)(
                id=int(thread_id)
            )
            if session.user:
                return session.user.username
        except (ValueError, ChatSession.DoesNotExist):
            pass
        return None
    
    async def delete_thread(self, thread_id: str) -> bool:
        """Delete a thread."""
        try:
            await sync_to_async(ChatSession.objects.filter(id=int(thread_id)).delete)()
            return True
        except (ValueError, Exception):
            return False
    
    async def list_threads(
        self, pagination: Pagination, filters: ThreadFilter
    ) -> PaginatedResponse[ThreadDict]:
        """
        List threads for the sidebar.
        
        This is the key method for displaying chat history in the sidebar.
        Returns PaginatedResponse as required by Chainlit 2.9.3.
        
        Note: Chainlit sends PersistedUser.id as filters.userId, which in our case
        is the Django user ID (as string). We need to handle both ID and username lookup.
        """
        user_id = filters.userId if filters else None
        
        if not user_id:
            return PaginatedResponse(
                pageInfo=PageInfo(hasNextPage=False, startCursor=None, endCursor=None),
                data=[]
            )
        
        # Get sessions for this user
        @sync_to_async
        def get_sessions():
            try:
                # First try to find user by ID (Chainlit sends PersistedUser.id)
                try:
                    user = DjangoUser.objects.get(id=int(user_id))
                except (ValueError, DjangoUser.DoesNotExist):
                    # Fallback to username lookup
                    user = DjangoUser.objects.get(username=user_id)
                
                sessions = ChatSession.objects.filter(user=user).order_by('-created_at')[:20]
                return list(sessions)
            except DjangoUser.DoesNotExist:
                return []
        
        sessions = await get_sessions()
        
        threads = []
        for session in sessions:
            # Get first message as preview
            @sync_to_async
            def get_preview(s):
                first_msg = s.messages.filter(sender="user").first()
                return first_msg.content[:50] if first_msg else s.title
            
            preview = await get_preview(session)
            
            thread_dict: ThreadDict = {
                "id": str(session.id),
                "name": preview,
                "createdAt": session.created_at.isoformat(),
                "userId": user_id,
                "userIdentifier": user_id,
                "metadata": {},
                "steps": [],
            }
            threads.append(thread_dict)
        
        return PaginatedResponse(
            pageInfo=PageInfo(hasNextPage=False, startCursor=None, endCursor=None),
            data=threads
        )
    
    async def get_thread(self, thread_id: str) -> Optional[ThreadDict]:
        """Get a specific thread with all its messages."""
        try:
            @sync_to_async
            def fetch_thread_data():
                """Fetch all thread data in a synchronous context."""
                session = ChatSession.objects.select_related('user').get(id=int(thread_id))
                messages = list(session.messages.order_by('timestamp'))
                user_identifier = session.user.username if session.user else "Anonymous"
                
                # Build steps list
                steps = []
                for msg in messages:
                    step_type = "user_message" if msg.sender == "user" else "assistant_message"
                    steps.append({
                        "id": str(msg.id),
                        "name": msg.sender,
                        "type": step_type,
                        "threadId": thread_id,
                        "output": msg.content,
                        "createdAt": msg.timestamp.isoformat(),
                    })
                
                return {
                    "id": str(session.id),
                    "name": session.title,
                    "createdAt": session.created_at.isoformat(),
                    "userId": user_identifier,
                    "userIdentifier": user_identifier,
                    "metadata": {},
                    "steps": steps,
                }
            
            return await fetch_thread_data()
        except (ValueError, ChatSession.DoesNotExist):
            return None
    
    async def update_thread(
        self,
        thread_id: str,
        name: Optional[str] = None,
        user_id: Optional[str] = None,
        metadata: Optional[Dict] = None,
        tags: Optional[List[str]] = None,
    ) -> None:
        """Update thread metadata."""
        try:
            @sync_to_async
            def update():
                session = ChatSession.objects.get(id=int(thread_id))
                if name:
                    session.title = name[:200]
                    session.save()
            
            await update()
        except (ValueError, ChatSession.DoesNotExist):
            pass
    
    async def delete_feedback(self, feedback_id: str) -> bool:
        """Delete feedback (not implemented for MVP)."""
        return True
