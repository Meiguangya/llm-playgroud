import asyncio

from fastapi import APIRouter, Request, Header, Query
from starlette.responses import StreamingResponse
from app.ai.rag.rag_agent import stream_rag_response

router = APIRouter(prefix="/api/v1/rag", tags=["RAG"])


@router.get("/files")
def files():
    return ["1.txt", "2.pdf"]


@router.get("/")
async def rag_query(
        prompt: str = Query(..., description="用户输入的查询内容"),
        chatId: str = Header(..., description="会话ID")
):
    """
    流式RAG接口，返回SSE格式的响应
    """

    print(f"prompt:{prompt}")
    print(f"chatId:{chatId}")

    async def event_stream():
        try:
            async for text in stream_rag_response(query=prompt, chat_id=chatId):
                yield text
                await asyncio.sleep(0)
        except Exception as e:
            yield f"Error: {str(e)}"

    # async def event_stream():
    #     # --- 模拟从 RAG Agent 获取流式输出 ---
    #     # 这里我们模拟 LLM 逐步生成回答的过程
    #     # 实际中这里应接入你的 agent.stream(...) 并监听 tokens
    #
    #     # 示例：假设这是你的 RAG 系统生成的回答
    #     full_response = (
    #         "瓜子通常指向日葵的种子，是一种常见的休闲食品。"
    #         "它富含脂肪、蛋白质和多种维生素，适量食用有助于补充能量。"
    #         "但不宜过量，以免摄入过多热量。"
    #     )
    #
    #     # 模拟逐字或逐句输出（更真实的是按 token 流出）
    #     for char in full_response:
    #         # 模拟网络延迟或生成耗时
    #         await asyncio.sleep(0.3)  # 控制流速，可调
    #
    #         yield char

    return StreamingResponse(
        event_stream(),
        media_type="text/event-stream"  # 可根据需要改为 "text/plain" 或 "application/octet-stream"
    )
