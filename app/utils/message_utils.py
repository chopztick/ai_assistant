from datetime import datetime
import json
from typing import Literal
from pydantic_ai import UnexpectedModelBehavior
from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart, ModelResponse, TextPart
from app.schemas.chat_models import ChatMessageResponse


def form_chat_message(message: ModelMessage) -> ChatMessageResponse:
    """
    Convert a ModelMessage to a ChatMessageResponse.

    Args:
        message (ModelMessage): The message to convert.
        
    Returns:
        ChatMessageResponse: The converted message.
    """
    if isinstance(message, ModelRequest):
        for part in message.parts:
            if isinstance(part, UserPromptPart):
                assert isinstance(part.content, str)
                return ChatMessageResponse(
                    type='content',
                    role='user',
                    timestamp=part.timestamp,
                    content=part.content,
                )
    elif isinstance(message, ModelResponse):
        for part in message.parts:
            if isinstance(part, TextPart):
                return ChatMessageResponse(
                    type='content',
                    role='ai_assistant',
                    timestamp=message.timestamp,
                    content=part.content,
                )
    raise UnexpectedModelBehavior(f'Unexpected message type for chat app: {message}')


def create_stream_chunk(chunk_type: Literal['meta', 'done'], conversation_id: int | None) -> bytes:
    """
    Create a stream initial or ending chunk for the response.
    
    Args:
        chunk_type (Literal['meta', 'done']): The type of chunk to create.
        conversation_id (int): The ID of the conversation.

    Returns:
        bytes: The created chunk as bytes.
    """
    return json.dumps({
            "type": chunk_type,
            "conversation_id": conversation_id,
            "timestamp": datetime.now().isoformat()
        }).encode("utf-8") + b"\n"
