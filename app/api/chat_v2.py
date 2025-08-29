import asyncio

from fastapi import APIRouter, Request, Header, Depends
from fastapi.responses import StreamingResponse
from sqlalchemy.orm import Session

from app.ai.agent.agent_servcie import AgentService
from app.db.session import get_db
from app.schemas.chat_message import CreateMessageDTO
from app.service.chat_message_service import save_message_to_db,recall_save_message_to_db
from fastapi import BackgroundTasks

router = APIRouter(prefix="/api/v2", tags=["Chat-V2"])


@router.post("/chat")
async def chat(
        request: Request,
        model: str = Header(None, alias="model"),
        chat_id: str = Header(None, alias="chatId"),
        db: Session = Depends(get_db)
):
    """
    流式聊天接口
    - 接收纯文本 prompt
    - 返回 text/event-stream 流式响应
    """
    # 读取请求体（纯文本）
    prompt = (await request.body()).decode('utf-8').strip()
    if not prompt:
        return {"error": "Prompt is required"}

    # 默认模型
    model = model or "qwen-plus"

    # 先保存用户消息到数据库
    try:
        user_dto = CreateMessageDTO(
            conversation_id=chat_id,
            role="human",
            content=prompt,
            model_name=model,
            metadata={"from": "user"}
        )
        save_message_to_db(db, user_dto)
    except Exception as e:
        print(f"保存用户消息失败: {e}")

    # 返回流式响应
    return StreamingResponse(
        AgentService.stream_agent_response3(prompt, model, chat_id, recall_save_message_to_db),
        media_type="text/event-stream"
    )
