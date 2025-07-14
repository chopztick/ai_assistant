from abc import ABC, abstractmethod
from typing import AsyncGenerator
from app.schemas.chat_models import ChatMessageCreate, ConversationHistoryResponse

class ChatServiceInterface(ABC):

    @abstractmethod
    async def get_conversation_history(self, conversation_id: int) -> ConversationHistoryResponse:
        pass

    @abstractmethod
    def process_message(self, message: ChatMessageCreate) -> AsyncGenerator[bytes, None]:
        pass