import asyncio

from langchain_core.messages import HumanMessage
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.tools import tool
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import MemorySaver
from app.chroma.chroma_client import ChromaSingleton
from langchain_community.chat_models import ChatTongyi


system_prompt = """你是一个专业的问答助手，负责根据提供的上下文回答用户问题。\n
请遵守以下规则：
1. 所有问题都必须先调用 retrieve 工具进行信息检索，不得直接回答。
2. 即使你认为自己知道答案，也必须通过 retrieve 获取最新资料。
3. 回答必须基于 retrieve 返回的内容，不能编造。
4. 如果资料中没有明确答案,判断这是不是一个常识问题，如果是一个常识问题，那么你做一个简短的回答，否则就回答：“抱歉，我还没有学习相关的知识”。
5. 回答应简洁、准确，使用中文。
6. 不要暴露「参考资料」的存在，像自然回答一样输出。
"""


@tool(response_format="content_and_artifact")
def retrieve(query: str):
    """Retrieve information related to a query."""
    retrieved_docs = ChromaSingleton.get_vectorstore().similarity_search(query, k=5)
    serialized = "\n\n".join(
        (f"Source: {doc.metadata}\nContent: {doc.page_content}")
        for doc in retrieved_docs
    )
    return serialized, retrieved_docs


class RagAgent:
    _rag_agent: CompiledStateGraph = None
    _memory:MemorySaver = None

    @classmethod
    def get_rag_agent(cls):
        if cls._rag_agent is None:
            cls._rag_agent = cls.init_rag_agent()

        return cls._rag_agent

    @classmethod
    def init_rag_agent(cls) -> CompiledStateGraph:
        print("初始化rag agent")

        # 初始化 Qwen 大模型
        qwen_llm = ChatTongyi(model_name="qwen-plus")

        if cls._memory is None:
            cls._memory = MemorySaver()

        agent_executor = create_react_agent(qwen_llm, [retrieve],
                                            prompt=system_prompt,
                                            checkpointer=cls._memory)

        return agent_executor


async def stream_rag_response(query: str, chat_id: str = None):
    """
    流式生成rag相应
    :param query:
    :param chat_id:
    :return:
    """

    config = {"configurable": {"thread_id": chat_id}}

    agent = RagAgent.get_rag_agent()

    full_content = ""

    async for event in agent.astream(
            {"messages": [("human", query)]},
            stream_mode="values",
            config=config,
    ):
        msg = event["messages"][-1]
        if msg.type == "ai" and not msg.tool_calls:
            full_content = msg.content

    # 逐字 yield，模拟流式
    for char in full_content:
        await asyncio.sleep(0.05)
        yield char
