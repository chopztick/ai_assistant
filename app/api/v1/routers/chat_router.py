from logging import getLogger
from typing import Any, AsyncGenerator
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import StreamingResponse
from app.domain.chat.chat_service_interface import ChatServiceInterface
from app.schemas.chat_models import ChatMessageCreate, ConversationHistoryResponse
from app.api.deps.deps import get_chat_service

# Get logger
logger = getLogger("chat_app")

# Set up FastAPI router
router = APIRouter(prefix="/chat", tags=["chat"])


@router.get("/conversations/{conversation_id}", response_model=ConversationHistoryResponse, status_code=status.HTTP_200_OK)
async def get_conversation(
    conversation_id: int,
    chat_service: ChatServiceInterface = Depends(get_chat_service)) -> Any:
    """
    Retrieve the conversation history by ID.

    Returns all messages associated with the given conversation.
    Raises a 404 error if not found.
    """
    try:
        logger.info(f"Fetching conversation history for ID: {conversation_id}")
        history = await chat_service.get_conversation_history(conversation_id)
        if not history:
            raise HTTPException(status_code=404, detail="Conversation not found.")
        return history
    except Exception as e:
        logger.exception("Error fetching conversation")
        raise HTTPException(status_code=500, detail="Internal server error")


@router.post("/chat_stream", response_class=StreamingResponse, status_code=status.HTTP_200_OK)
async def add_messages(
    messages: ChatMessageCreate,
    chat_service: ChatServiceInterface = Depends(get_chat_service)) -> StreamingResponse:
    """
    Stream the AI response to a new user message.

    Accepts a message and returns a streaming NDJSON response as the AI replies.
    """
    try:
        # logger.info(f"Streaming response for new messages from {request.client.host}")
        generator: AsyncGenerator[bytes, None] = chat_service.process_message(messages)
        return StreamingResponse(generator, media_type="application/x-ndjson")
    except Exception as e:
        logger.exception("Error streaming chat response")
        raise HTTPException(status_code=500, detail="Streaming failed")