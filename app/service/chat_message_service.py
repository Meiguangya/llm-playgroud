# services/message_service.py
from typing import Optional, Dict

from sqlalchemy.orm import Session
from app.models.chat_message import ChatMessage
from app.schemas.chat_message import CreateMessageDTO
import uuid
from datetime import datetime
from app.db.session import get_db


class MessageService:
    def __init__(self, db: Session):
        self.db = db

    def create_message(self, dto: CreateMessageDTO) -> ChatMessage:
        """
        插入一条新的聊天消息
        :param dto: CreateMessageRequest DTO
        :return: 创建的消息对象
        """
        print(dto)
        message = ChatMessage(
            id=str(uuid.uuid4()),
            conversation_id=dto.conversation_id,
            role=dto.role,
            content=dto.content,
            content_type=dto.content_type,
            token_count=dto.token_count,
            model_name=dto.model_name,
            metadata_=dto.metadata,
            created_at=datetime.utcnow()
        )
        self.db.add(message)
        self.db.commit()
        self.db.refresh(message)
        return message


def save_message_to_db(db: Session, dto: CreateMessageDTO):
    print("将消息插入数据库")
    ms = MessageService(db)

    ms.create_message(dto)


# 回调方法
async def recall_save_message_to_db(full_content: str, conversation_id: str, model_name: str, status="success"):
    # 创建新的 db 实例（不要用上层传进来的 db）
    local_db = next(get_db())
    try:
        dto = CreateMessageDTO(
            conversation_id=conversation_id,
            role="ai",
            content=full_content,
            model_name=model_name,
            metadata={"status": status, "from": "AgentService.on_complete"}
        )
        # 调用你的保存逻辑（同步或异步）
        save_message_to_db(local_db, dto)
    except Exception as e:
        print(f"保存失败: {e}")
    finally:
        local_db.close()
