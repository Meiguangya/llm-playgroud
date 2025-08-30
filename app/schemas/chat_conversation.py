from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

# ----------------------------
# 响应 DTO：返回给前端的会话信息
# ----------------------------
class ConversationDTO(BaseModel):
    id: str
    title: str
    status: int
    model_name: Optional[str] = None
    total_tokens: int
    message_count: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # 支持 ORM 模式（旧版：orm_mode = True）

# ----------------------------
# 请求 DTO：创建会话时的输入（可选）
# ----------------------------
class CreateConversationRequest(BaseModel):
    title: Optional[str] = "新对话"
    model_name: Optional[str] = "gpt-4o"

# ----------------------------
# 响应 DTO：批量返回会话列表
# ----------------------------
class ListConversationsResponse(BaseModel):
    conversations: List[ConversationDTO]


class UpdateConversationTitleRequest(BaseModel):
    title: str