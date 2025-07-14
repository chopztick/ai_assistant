from abc import ABC, abstractmethod
from app.infrastructure.db.models.message import Message

class MessagesInterface(ABC):
    """
    Repository for managing chat-related database operations.
    """
    @abstractmethod
    async def get_conversation(self, conversation_id: int, limit: int | None = None) -> list[Message]:
        """
        Retrieve a conversation by its ID. If limit is provided, it will return the last N messages in the conversation.
        """
        pass

    @abstractmethod
    async def add_message(self, message: Message) -> Message:
        """
        Save given messages to the database.
        """
        # Placeholder for actual database operation
        pass

    @abstractmethod
    async def get_all_conversations(self, user_id: int) -> list[Message]:
        """
        Retrieve every first message each conversations for a given user.
        """
        pass