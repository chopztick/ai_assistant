from typing import List, Literal, Optional
from pydantic import BaseModel
from datetime import datetime


class ChatMessageResponse(BaseModel):
    """
    Represents a chat message in the conversation.
    """
    type: Literal['meta', 'done', 'content']
    role: Literal['user', 'ai_assistant']
    timestamp: datetime
    content: str


class ConversationHistoryResponse(BaseModel):
    """
    Represents the conversation history.
    """
    conversation_id: int
    messages: List[ChatMessageResponse]


class ChatMessageCreate(BaseModel):
    """
    Represents a new chat message to be sent.
    """
    user_id: int
    conversation_id: Optional[int] = None
    user_request: str
