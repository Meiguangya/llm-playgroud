import os

from langchain_core.messages import HumanMessage

from app.ai.graph.chat_graph import ConversationState
from app.ai.graph.chat_graph_service import ChatGraphService

# 从环境变量获取 API Key
DASHSCOPE_API_KEY = os.getenv("DASHSCOPE_API_KEY")
if not DASHSCOPE_API_KEY:
    raise ValueError("DASHSCOPE_API_KEY is not set")

print(f"获取DASHSCOPE_API_KEY成功{DASHSCOPE_API_KEY}")


async def stream_chat_response(
        prompt: str,
        model: str = "qwen-plus",
        chat_id: str = None
):
    """
    流式生成聊天响应
    :param prompt: 用户输入
    :param model: 模型名称
    :param chat_id: 会话ID（可选，可用于后续上下文管理）
    """
    chat_graph = None
    try:
        chat_graph = ChatGraphService.get_chat_graph({"model_name": model})
    except Exception as e:
        yield f"Error: {str(e)}"

    if not chat_graph:
        yield f"Error: 系统错误"

    chat_app = chat_graph.workflow

    config = {"configurable": {"thread_id": chat_id}}
    input_messages = [HumanMessage(content=prompt)]

    state = ConversationState(messages=input_messages)

    # 调用异步流式接口
    async for chunk in chat_app.astream(state, config=config):
        # 将每个 chunk 转换为 SSE 格式（可选，也可以直接返回 JSON 流）
        # print(f"chunk:{type(chunk)} \n {chunk}")
        # yield f"dataxxxxx: {chunk}\n\n"
        yield chunk["call_model"]["messages"][-1].content
        # print(f"{type(chunk)} \n {chunk}")
        # yield chunk


