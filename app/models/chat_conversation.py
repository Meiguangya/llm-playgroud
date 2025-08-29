from sqlalchemy import Column, String, BigInteger, Integer, DateTime, Text, Enum, Index
from app.db.session import Base
from datetime import datetime

class ChatConversation(Base):
    __tablename__ = "chat_conversations"

    # 主键：UUID 字符串（36位）
    id = Column(String(36), primary_key=True, index=True)

    # 用户ID
    user_id = Column(BigInteger, nullable=False, index=True)

    # 会话标题
    title = Column(String(255), default="新对话", nullable=True)

    # 状态：1=活跃，2=归档，3=删除
    status = Column(Integer, default=1, nullable=False)

    # 使用的AI模型
    model_name = Column(String(50), nullable=True)

    # 统计字段
    total_tokens = Column(Integer, default=0, nullable=False)
    message_count = Column(Integer, default=0, nullable=False)

    # 时间字段
    created_at = Column(DateTime(6), default=datetime.utcnow, nullable=False)
    updated_at = Column(DateTime(6), default=datetime.utcnow, onupdate=datetime.utcnow, nullable=False)
    deleted_at = Column(DateTime(6), nullable=True)

    # 索引
    __table_args__ = (
        Index("idx_user_status", user_id, status, updated_at.desc()),
        Index("idx_user_updated", user_id, updated_at.desc()),
    )