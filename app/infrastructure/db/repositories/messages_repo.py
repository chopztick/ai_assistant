from app.domain.chat.messages_repo_interface import MessagesInterface
from app.infrastructure.db.models.message import Message
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select

class MessagesRepository(MessagesInterface):
    """
    Repository for managing chat-related database operations.
    """

    def __init__(self, session: AsyncSession):
        """
        Initialize the ChatRepository with a database session.

        Args:
            session (AsyncSession): The database session to use for operations.
        """
        self.session = session


    async def get_conversation(self, conversation_id: int, limit: int | None = None) -> list[Message]:
        """
        Retrieve a conversation by its ID. If limit is provided, it will return the last N messages in the conversation.

        Args:
            conversation_id (int): The ID of the conversation to retrieve.
            limit (int | None): The maximum number of messages to retrieve.

        Returns:
            list[Message]: A list of Message objects in the conversation.
        """
        stmt = select(Message).where(Message.conversation_id == conversation_id)

        if limit is not None:
            stmt = stmt.order_by(Message.id.desc()).limit(limit)
            result = await self.session.execute(stmt)
            return list(reversed(result.scalars().all()))
        else:
            stmt = stmt.order_by(Message.id.asc())
            result = await self.session.execute(stmt)
            return list(result.scalars().all())


    async def add_message(self, message: Message) -> Message:
        """
        Save given messages to the database.
        Insert a message and update conversation_id if not provided.

        Args:
            message (Message): The message to save.
            
        Returns:
            Message: The saved message.
        """
        self.session.add(message)
        await self.session.flush()

        if message.conversation_id is None:
            message.conversation_id = message.id

        await self.session.commit()
        return message
    

    async def get_all_conversations(self, user_id: int) -> list[Message]:
        """
        Retrieve every first message each conversations for a given user.

        Args:
            user_id (int): The ID of the user to retrieve conversations for.

        Returns:
            list[Message]: A list of Message objects from each conversation.
        """
        # Build query, as the conversation_id is the same as the first message id,
        # it could be used to filter the first message of each conversation
        stmt = select(Message).where(Message.user_id == user_id, Message.id == Message.conversation_id).order_by(Message.id.asc())

        result = await self.session.execute(stmt)
        return list(result.scalars().all())
