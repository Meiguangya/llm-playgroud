import asyncio

from fastapi import APIRouter, Request, Header
from fastapi.responses import StreamingResponse

from app.ai.services.chat_service import stream_chat_response

router = APIRouter(prefix="/api/v1", tags=["Chat"])


@router.post("/chat")
async def chat(
        request: Request,
        model: str = Header(None, alias="model"),
        chatId: str = Header(None, alias="chatId")
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
            async for text in stream_chat_response(prompt, model, chatId):
                # 可以在这里插入 <think> 标签逻辑（如按句分割）
                # 示例：每段前后加 <think>（可选）
                # yield f"<think>{text}</think>"
                yield text
                await asyncio.sleep(0)  # 协程让步，避免阻塞
        except Exception as e:
            yield f"Error: {str(e)}"

    # 返回流式响应
    return StreamingResponse(
        generate_stream(),
        #media_type="text/plain"  # 或 "text/event-stream" 如果是 SSE
        media_type="text/event-stream"
    )
