from datetime import datetime, timezone
from typing import AsyncGenerator
from pydantic_ai import Agent
from pydantic_ai.messages import ModelMessage, ModelResponse, TextPart
from app.domain.chat.llm_messages_repo_interface import LlmInterface
from app.infrastructure.llm.models.agent_models import Deps
from app.schemas.chat_models import ChatMessageResponse
from app.utils.message_utils import form_chat_message

class LlmRepository(LlmInterface):
    """
    Repository for managing LLM messages.
    """

    def __init__(self, llm_agent: Agent[Deps], deps: Deps):
        """
        Initialize the LLMMessagesRepo with an LLM agent.

        Args:
            agent (Agent): The LLM agent to use for operations.
        """
        self.agent = llm_agent
        self.message_to_save = None
        self.deps = deps


    async def send_message(self, message: str, history: list[ModelMessage]) -> AsyncGenerator[bytes, None]:
        """
        Send a message to the LLM agent and receive a response.

        Args:
            message (str): The message to send to the LLM agent.
            history (list[ModelMessage]): The conversation history to include in the request.

        Returns:
            AsyncGenerator[bytes, None]: An async generator that yields the response from the LLM agent.
        """
        # Yield the user message first
        yield (
            ChatMessageResponse(
                type="content",
                role="user",
                timestamp=datetime.now(tz=timezone.utc),
                content=message,
            ).model_dump_json().encode("utf-8") + b"\n"
        )


        # Streams the response from the LLM agent
        async with self.agent.run_stream(user_prompt=message, message_history=history, deps=self.deps) as response:
            # Run the async generator to get the response
            async for text in response.stream(debounce_by=0.5):
                # Construct the ModelResponse object
                msg = ModelResponse(parts=[TextPart(content=text)], timestamp=response.timestamp())
                # Yield the response message
                chat_msg = form_chat_message(msg)
                if chat_msg is not None:
                    yield chat_msg.model_dump_json().encode('utf-8') + b'\n'

            # Save the complete generated response to be saved into the database
            self.message_to_save = response.new_messages_json()


    async def get_final_message(self) -> bytes | None:
        """
        Get the complete generated message from the LLM agent.

        Returns:
            list[ModelMessage]: The complete message from the LLM agent.
        """
        return self.message_to_save
