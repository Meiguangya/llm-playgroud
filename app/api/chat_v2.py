import asyncio

from fastapi import APIRouter, Request, Header
from fastapi.responses import StreamingResponse

from app.ai.agent.agent_servcie import AgentService

router = APIRouter(prefix="/api/v2", tags=["Chat-V2"])


@router.post("/chat")
async def chat(
        request: Request,
        model: str = Header(None, alias="model"),
        chat_id: str = Header(None, alias="chatId")
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

    # 定义异步生成器，用于流式输出
    async def generate_stream():
        try:
            async for text in AgentService.stream_agent_response2(prompt, model, chat_id):
                yield text
                await asyncio.sleep(0)  # 协程让步，避免阻塞
        except Exception as e:
            yield f"Error: {str(e)}"

    # 返回流式响应
    return StreamingResponse(
        generate_stream(),
        media_type="text/event-stream"
    )
