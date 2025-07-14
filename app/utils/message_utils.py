from datetime import datetime
import json
from typing import Literal
from pydantic_ai import UnexpectedModelBehavior
from pydantic_ai.messages import ModelMessage, ModelRequest, UserPromptPart, ModelResponse, TextPart, ToolCallPart, ToolReturnPart, RetryPromptPart, SystemPromptPart
from app.schemas.chat_models import ChatMessageResponse


def form_chat_message(message: ModelMessage) -> ChatMessageResponse | None:
    """
    Convert a ModelMessage to a ChatMessageResponse.
    """
    def convert_part(part, timestamp) -> ChatMessageResponse | None:
        if isinstance(part, SystemPromptPart):
            return None

        if isinstance(part, UserPromptPart):
            assert isinstance(part.content, str)
            return ChatMessageResponse(
                type='content',
                role='user',
                timestamp=timestamp,
                content=part.content,
            )
        elif isinstance(part, TextPart):
            return ChatMessageResponse(
                type='content',
                role='ai_assistant',
                timestamp=timestamp,
                content=part.content,
            )
        elif isinstance(part, ToolCallPart):
            return ChatMessageResponse(
                type='tool_call',
                role='ai_assistant',
                timestamp=timestamp,
                content=f"Tool call: {part.tool_name}({part.args})"
            )
        elif isinstance(part, ToolReturnPart):
            return ChatMessageResponse(
                type='tool_return',
                role='ai_assistant',
                timestamp=timestamp,
                content=f"Tool return: {part.tool_name}"
            )
        elif isinstance(part, RetryPromptPart):
            return ChatMessageResponse(
                type='extra_forbidden',
                role='ai_assistant',
                timestamp=timestamp,
                content="Retrying the prompt due to an error."
            )
        
        else:
            raise UnexpectedModelBehavior(f"Unknown part type: {part}")

    if isinstance(message, ModelRequest):
        for part in message.parts:
            return convert_part(part, part.timestamp)
    elif isinstance(message, ModelResponse):
        for part in message.parts:
            return convert_part(part, message.timestamp)
    
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
