from app.infrastructure.db.base import Base
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import LargeBinary
from datetime import datetime

class Message(Base):
    __tablename__ = "messages"

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int]
    conversation_id: Mapped[int] = mapped_column(nullable=True)
    timestamp: Mapped[datetime]
    content: Mapped[bytes] = mapped_column(LargeBinary)