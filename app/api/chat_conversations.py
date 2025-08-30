# api/v1/conversations.py
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException,status
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session
from typing import List

from app.common.response import ApiResponse
from app.db.session import get_db
from app.dependencies.get_current_user import get_current_user
from app.models.chat_message import ChatMessage
from app.schemas.user import CurrentUser
from app.schemas.chat_conversation import ConversationDTO, CreateConversationRequest,UpdateConversationTitleRequest
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




@router.delete("/{conversation_id}")
def delete_conversation(
    conversation_id: str,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    硬删除一个会话及其所有消息（物理删除）
    - 权限校验：确保该会话属于当前用户
    - 级联删除：自动删除 chat_messages 中的相关消息
    - 返回标准 ApiResponse 格式
    """
    try:
        # 1. 查询会话：必须存在、属于当前用户
        conversation = db.query(ChatConversation).filter(
            ChatConversation.id == conversation_id,
            ChatConversation.user_id == current_user.user_id
        ).first()

        if not conversation:
            return ApiResponse.fail(
                message="会话不存在或无权限删除",
                code=status.HTTP_404_NOT_FOUND
            )

        # 2. 删除该会话下的所有消息
        db.query(ChatMessage).filter(ChatMessage.conversation_id == conversation_id).delete(
            synchronize_session=False
        )

        # 3. 删除会话本身
        db.delete(conversation)
        db.commit()

        return ApiResponse.success(
            data=None,
            message="会话已成功删除",
        )

    except SQLAlchemyError as e:
        db.rollback()
        return ApiResponse.fail(
            message="数据库操作失败",
            code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )
    except Exception as e:
        db.rollback()
        return ApiResponse.fail(
            message="删除会话时发生未知错误"+str(e),
            code=status.HTTP_500_INTERNAL_SERVER_ERROR
        )




@router.patch("/{conversation_id}/title")
def update_conversation_title(
    conversation_id: str,
    request: UpdateConversationTitleRequest,
    db: Session = Depends(get_db),
    current_user = Depends(get_current_user)
):
    """
    修改会话标题
    """
    title = request.title.strip()
    if not title:
        return ApiResponse.fail(
            message="会话标题不能为空",
            code=400
        )

    if len(title) > 100:
        return ApiResponse.fail(
            message="会话标题不能超过100个字符",
            code=400
        )

    conversation = db.query(ChatConversation).filter(
        ChatConversation.id == conversation_id,
        ChatConversation.user_id == current_user.user_id,
        ChatConversation.deleted_at.is_(None)
    ).first()

    if not conversation:
        return ApiResponse.failure(
            message="会话不存在或已被删除",
            code=404
        )

    conversation.title = title
    conversation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(conversation)

    return ApiResponse.success(
        data={
            "id": conversation.id,
            "title": conversation.title,
            "updated_at": conversation.updated_at
        },
        message="标题更新成功"
    )