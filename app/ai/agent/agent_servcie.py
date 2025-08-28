import asyncio

from langchain_core.messages import AIMessage, AIMessageChunk

from app.ai.agent.simple_agent import MySimpleAgent
from typing import Dict


class AgentService:
    _agents: Dict[str, MySimpleAgent] = {}

    @classmethod
    def get_agent(cls, config: dict) -> MySimpleAgent:
        model_type = f"{config['model_name']}"

        if model_type not in cls._agents:
            print("创建新的agent")
            new_agent = MySimpleAgent(model_name=model_type)
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
            print(f"chunk{type(chunk)}-{chunk}")
            print(f"metadata{type(metadata)}-{metadata}")
            if isinstance(chunk, AIMessageChunk):
                print(f"chunk{chunk}")
                await asyncio.sleep(0.05)
                yield chunk.content


