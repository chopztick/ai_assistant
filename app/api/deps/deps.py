from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic_ai import Agent

# Import repositories
from app.infrastructure.db.repositories.messages_repo import MessagesRepository
from app.infrastructure.db.repositories.users_repo import UsersRepository
from app.infrastructure.llm.models.agent_models import Deps
from app.infrastructure.llm.repositories.llm_messages_repo import LlmRepository
# Import interfaces
from app.domain.chat.chat_service_interface import ChatServiceInterface
# Import services
from app.services.chat_service import ChatService
# Import dependencies
from app.infrastructure.db.session import get_session
from app.infrastructure.llm.llm_agents import get_chat_agent


def get_chat_service(session: AsyncSession = Depends(get_session), llm_agent: Agent[Deps] = Depends(get_chat_agent)) -> ChatServiceInterface:
    chat_repository = MessagesRepository(session=session)
    user_repository = UsersRepository(session=session)
    agent = LlmRepository(llm_agent=llm_agent, deps=Deps(user_repo=user_repository))

    return ChatService(chat_repository=chat_repository, llm_agent=agent)