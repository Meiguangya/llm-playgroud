# api/v1/messages.py

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from app.common.response import ApiResponse
from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.chat_message import ChatMessage
from app.models.chat_conversation import ChatConversation
from app.schemas.chat_message import ChatMessageDTO
from app.schemas.user import CurrentUser

router = APIRouter(
    prefix="/api/v1/messages",
    tags=["messages"]
)

@router.get("/{conversation_id}", response_model=ApiResponse[List[ChatMessageDTO]])
def list_messages(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user: CurrentUser = Depends(get_current_user)
):
    """
    根据 conversation_id 查询该会话下的所有聊天消息
    - 权限校验：确保该会话属于当前用户
    - 排序：按创建时间升序（从旧到新）
    """
    # 1. 校验会话是否存在且属于当前用户
    conversation = db.query(ChatConversation).filter(
        ChatConversation.id == conversation_id,
        ChatConversation.user_id == current_user.user_id,
        ChatConversation.deleted_at.is_(None)
    ).first()

    if not conversation:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="会话不存在或无访问权限"
        )

    # 2. 查询该会话下的所有消息，按时间升序排列
    messages = (
        db.query(ChatMessage)
        .filter(ChatMessage.conversation_id == conversation_id)
        .order_by(ChatMessage.created_at.asc())
        .all()
    )

    # 3. 转换为 ChatMessageDTO
    message_dtos = []
    for msg in messages:
        message_dtos.append(ChatMessageDTO(
            id=msg.id,
            conversation_id=msg.conversation_id,
            role=msg.role,
            content=msg.content
            #model_name=msg.model_name,
            #metadata=msg.metadata_ or {},
            #created_at=msg.created_at
        ))

    return ApiResponse.success(data = message_dtos)