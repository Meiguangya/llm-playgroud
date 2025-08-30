import asyncio

from langchain_core.messages import AIMessage, AIMessageChunk

from app.ai.agent.simple_agent import MySimpleAgent
from typing import Dict


class AgentService:
    _agents: Dict[str, MySimpleAgent] = {}

    @classmethod
    async def get_agent(cls, config: dict) -> MySimpleAgent:
        model_type = f"{config['model_name']}"

        if model_type not in cls._agents:
            print("创建新的agent")
            new_agent = MySimpleAgent(model_name=model_type)
            await new_agent.initialize()
            cls._agents[model_type] = new_agent

        return cls._agents[model_type]

    @classmethod
    async def stream_agent_response(cls,
                                    prompt: str,
                                    model_name: str = "qwen-plus",
                                    chat_id: str = None):

        """
        使用agent响应用户
        :param prompt:
        :param model_name:
        :param chat_id:
        :return:
        """

        my_simple_agent = cls.get_agent({"model_name": model_name})

        agent_executor = my_simple_agent.agent_executor

        config = {"configurable": {"thread_id": chat_id}}

        input = {"messages": [("human", prompt)]}

        final_result = ""

        async for step in agent_executor.astream(input,
                                                 stream_mode="values",
                                                 config=config):
            msg = step["messages"][-1]
            if msg.type == "ai" and not msg.tool_calls:
                final_result = msg.content

        # 模拟流式
        for char in final_result:
            await asyncio.sleep(0.05)
            yield char


    @classmethod
    async def stream_agent_response2(cls,
                                    prompt: str,
                                    model_name: str = "qwen-plus",
                                    chat_id: str = None):

        """
        使用agent响应用户
        :param prompt:
        :param model_name:
        :param chat_id:
        :return:
        """

        my_simple_agent = cls.get_agent({"model_name": model_name})

        agent_executor = my_simple_agent.agent_executor

        config = {"configurable": {"thread_id": chat_id}}

        input = {"messages": [("human", prompt)]}

        async for chunk,metadata in agent_executor.astream(input,
                                                 stream_mode="messages",
                                                 config=config):
            """
            使用token by token的返回方式
            """
            if isinstance(chunk, AIMessageChunk):
                await asyncio.sleep(0.05)
                yield chunk.content





    ############
    @classmethod
    async def stream_agent_response3(cls,
                                     prompt: str,
                                     model_name: str = "qwen-plus",
                                     chat_id: str = None,
                                     on_complete: callable = None):

        """
        使用agent响应用户
        :param prompt:
        :param model_name:
        :param chat_id:
        :param on_complete
        :return:
        """

        try:
            # 获取 agent
            my_simple_agent = await cls.get_agent({"model_name": model_name})
            agent_executor = my_simple_agent.agent_executor
            # 重写

            config = {"configurable": {"thread_id": chat_id}}
            input_data = {"messages": [("human", prompt)]}

            full_content = ""

            # 流式生成
            async for chunk, metadata in agent_executor.astream(
                    input_data,
                    stream_mode="messages",
                    config=config
            ):
                if isinstance(chunk, AIMessageChunk):
                    content = chunk.content
                    if content:  # 防止 yield 空字符串
                        await asyncio.sleep(0.05)  # 模拟流速，可调
                        yield content
                        full_content += content

            # 流式输出结束后，调用回调（此时 full_content 已完整）
            if on_complete and callable(on_complete):
                # 使用 create_task 避免阻塞
                # full_content: str, conversation_id: str, model_name: str, status="success"
                asyncio.create_task(
                    on_complete(
                        full_content=full_content,
                        conversation_id=chat_id,
                        model_name=model_name
                    )
                )

        except Exception as e:
            # 可选：也支持错误回调
            error_msg = f"Error in stream_agent_response: {str(e)}"
            # 仍然可以调用 on_complete，或单独处理
            if on_complete:
                asyncio.create_task(
                    on_complete(
                        full_content=f"系统错误：{str(e)}",
                        conversation_id=chat_id,
                        model_name=model_name,
                        status="error"
                    )
                )
            # 不 yield 错误，由上层处理
            # raise  # 或 yield error_msg，看你的需求
            yield error_msg


