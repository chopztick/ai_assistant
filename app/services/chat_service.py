from typing import AsyncGenerator
from app.domain.chat.chat_service_interface import ChatServiceInterface 
from app.domain.chat.llm_messages_repo_interface import LlmInterface
from app.domain.chat.messages_repo_interface import MessagesInterface
from app.schemas.chat_models import ChatMessageCreate, ChatMessageResponse, ConversationHistoryResponse
from app.infrastructure.db.models.message import Message
from app.utils.message_utils import create_stream_chunk, form_chat_message
from pydantic_ai.messages import ModelMessage, ModelMessagesTypeAdapter
from datetime import datetime

class ChatService(ChatServiceInterface):

    def __init__(self, chat_repository: MessagesInterface, llm_agent: LlmInterface):
        """
        Initialize the ChatService with a chat repository.

        Args:
            chat_repository (ChatRepositoryInterface): The repository for chat operations.
        """
        self.chat_repository = chat_repository
        self.llm_agent = llm_agent  
    

    async def get_conversation_history(self, conversation_id: int) -> ConversationHistoryResponse:
        """
        Retrieve a conversation by its ID.

        Args:
            conversation_id (int): The ID of the conversation to retrieve.

        Returns:    
            ConversationHistoryResponse: The conversation history.
        """

        message_history = await self.chat_repository.get_conversation(conversation_id)

        agent_message_history: list[ModelMessage] = []
        for item in message_history:
            agent_message_history.extend(ModelMessagesTypeAdapter.validate_json(item.content))

        model_msg_list: list[ChatMessageResponse] = [form_chat_message(msg) for msg in agent_message_history]

        return ConversationHistoryResponse(
            conversation_id=conversation_id,
            messages=model_msg_list
        )
    

    async def process_message(self, message: ChatMessageCreate) -> AsyncGenerator[bytes, None]:
        """
        Send the given messages to the LLM, save it with the response into the database, and stream the response.

        Args:
            message (ChatMessage): The request message sent to the LLM agent.

        Returns:
            AsyncGenerator[bytes, None]: An async generator that yields the response from the LLM agent.
        """
        agent_message_history: list[ModelMessage] = []

        # Create the initial message object
        yield create_stream_chunk('meta', message.conversation_id)

        # If conversation_id is not None, get all messages with the conversation_id and merge them into a list[ModelMessage]
        if message.conversation_id is not None:
            message_history = await self.chat_repository.get_conversation(message.conversation_id)
            for item in message_history:
                # Extend the agent_message_history with the validated JSON content (list[ModelMessage])
                agent_message_history.extend(ModelMessagesTypeAdapter.validate_json(item.content))

        # Stream the response from the LLM agent
        async for chunk in self.llm_agent.send_message(message.user_request, agent_message_history):
            yield chunk
       
        # Get the complete generated response from the LLM agent
        completed_response = await self.llm_agent.get_final_message()

        # Create the Message object with the completed response
        orm_message = Message(
            user_id=message.user_id,
            conversation_id=message.conversation_id,
            timestamp=datetime.now(),
            content=completed_response,
        )

        # Save the message to the database
        saved_message = await self.chat_repository.add_message(orm_message)

        # Create the closing message object
        yield create_stream_chunk('done', saved_message.conversation_id)
