from abc import ABC, abstractmethod
from typing import AsyncGenerator
from pydantic_ai.messages import ModelMessage

class LlmInterface(ABC):
    """
    Repository for managing LLM-related database operations.
    """

    @abstractmethod
    def send_message(self, message: str, history: list[ModelMessage]) -> AsyncGenerator[bytes, None]:
        pass

    @abstractmethod
    async def get_final_message(self) -> bytes | None:
        pass