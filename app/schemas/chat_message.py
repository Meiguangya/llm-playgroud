# schemas/message.py

from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional, Dict


class ChatMessageDTO(BaseModel):
    id: str
    conversation_id: str
    role: str
    content: str
    #content_type: str = ""
    #token_count: int = 0
    #model_name: Optional[str] = None
    #metadata: Optional[dict] = None
    #created_at: datetime

    class Config:
        from_attributes = True  # 支持 ORM 模式


class CreateMessageDTO(BaseModel):
    """
    创建消息的请求 DTO
    """
    conversation_id: str
    role: str  # user, assistant, system
    content: str
    content_type: str = "text"
    token_count: int = 0
    model_name: Optional[str] = None
    metadata: Optional[Dict] = None