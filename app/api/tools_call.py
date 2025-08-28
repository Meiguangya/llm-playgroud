import asyncio

from fastapi import APIRouter, Request, Header, Query
from starlette.responses import StreamingResponse
from app.ai.agent.agent_servcie import AgentService

router = APIRouter(prefix="/api/v1", tags=["Agent"])


@router.get("/tool-call")
async def tool_call(
        prompt: str = Query(..., description="用户输入的查询内容"),
        chatId: str = Header(..., description="会话ID")
):
    """
    调用simple agent 完成工具调用
    :param prompt:
    :param chatId:
    :return:
    """

    return StreamingResponse(
        AgentService.stream_agent_response(prompt,chat_id=chatId),
        media_type="text/event-stream"
    )
