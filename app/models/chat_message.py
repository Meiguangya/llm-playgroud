# models/message.py

from sqlalchemy import Column, String, Enum, Text, Integer, DateTime, JSON, ForeignKey
from app.db.session import Base
from datetime import datetime

class ChatMessage(Base):
    __tablename__ = "chat_messages"

    id = Column(String(36), primary_key=True, index=True)
    conversation_id = Column(String(36), ForeignKey("chat_conversations.id"), nullable=False, index=True)
    role = Column(Enum("human", "ai", "system", name="role_enum"), nullable=False)
    content = Column(Text, nullable=False)
    content_type = Column(String(20), default="text", nullable=False)
    token_count = Column(Integer, default=0, nullable=False)
    model_name = Column(String(50), nullable=True)
    metadata_ = Column("metadata", JSON, nullable=True)  # 避免与关键字冲突
    created_at = Column(DateTime(6), default=datetime.utcnow, nullable=False)

    # 可选：添加 relationship
    # conversation = relationship("ChatConversation", back_populates="messages")