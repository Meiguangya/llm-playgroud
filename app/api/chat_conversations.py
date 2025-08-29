# api/v1/conversations.py

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app.common.response import ApiResponse
from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.schemas.user import CurrentUser
from app.schemas.chat_conversation import ConversationDTO, CreateConversationRequest
from app.models.chat_conversation import ChatConversation
import uuid

router = APIRouter(
    prefix="/api/v1/conversations",
    tags=["conversations"],
    responses={404: {"description": "Not found"}}
)


@router.get("/", response_model=ApiResponse[List[ConversationDTO]])
def list_conversations(
        db: Session = Depends(get_db),
        current_user=Depends(get_current_user)
):
    """
    获取当前用户的聊天会话列表
    - **认证**：通过 JWT Token 获取当前用户
    - **过滤**：只返回该用户的会话（未软删除）
    - **排序**：按最后更新时间倒序（最新在前）
    """
    # 查询用户的所有会话（排除已删除的）
    conversations = (
        db.query(ChatConversation)
        .filter(
            ChatConversation.user_id == current_user.user_id,
            ChatConversation.deleted_at.is_(None)  # 软删除过滤
        )
        .order_by(ChatConversation.updated_at.desc())
        .limit(50)
        .all()
    )

    if not conversations:
        # 用户没有会话，返回空列表（不是错误）
        return ApiResponse.success(data=[])

    return ApiResponse.success(conversations)


@router.post("/", response_model=ApiResponse[ConversationDTO])
def create_conversation(
        request: CreateConversationRequest,
        db: Session = Depends(get_db),
        current_user:CurrentUser=Depends(get_current_user)
):
    """
    创建一个新的聊天会话
    - 使用用户提供的标题，若为空则使用默认值
    - 自动生成 UUID 作为主键
    - 初始化统计字段（token 数、消息数等）
    """
    conversation = ChatConversation(
        id=str(uuid.uuid4()),  # 需要导入 uuid
        user_id=current_user.user_id,
        title=request.title,
        model_name=request.model_name,
        status=1,  # 活跃状态
        total_tokens=0,
        message_count=0,
        # created_at 和 updated_at 使用数据库默认值
    )
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return ApiResponse.success(data=conversation)
