from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph.state import CompiledStateGraph
from langgraph.prebuilt import create_react_agent
from app.ai.agent.tools.employee_tools import *
from app.ai.agent.tools.retrieve_tools import retriever_tool

from app.ai.models.llm_factory import get_llm


tools = [fetch_employee_count,retriever_tool]

# system_prompt = "你是一个有用的助手,你的名字叫小光"

system_prompt = """你是一个专业的问答助手，你的名字叫小光,负责根据提供的上下文回答用户问题。\n
请遵守以下规则：
1. 自行判断回答用户的问题是否需要调用工具，自行进行调用工具
2. 如果用到了 retrieve_document 工具进行信息检索，回答必须基于 retrieve_document 返回的内容，不能编造。
4. 如果资料中没有明确答案,判断这是不是一个常识问题，如果是一个常识问题，那么你做一个简短的回答，否则就回答：“抱歉，我还没有学习相关的知识”。
5. 回答应简洁、准确，使用中文。
6. 不要暴露「参考资料」的存在，像自然回答一样输出。
"""


class MySimpleAgent:

    def __init__(self,
                 model_name: str = ""
                 ):
        self.llm_model = get_llm(model_name)
        #self.llm_model = None
        self.memory = MemorySaver()
        self.system_prompt = system_prompt
        self.tools = tools
        self.agent_executor = self._create_simple_agent()

    def _create_simple_agent(self) -> CompiledStateGraph:
        """
        创建ReAct-Agent
        :return: Graph
        """
        agent_executor = create_react_agent(self.llm_model,
                                            self.tools,
                                            checkpointer=self.memory,
                                            prompt=system_prompt)

        return agent_executor


if __name__ == "__main__":
    new_agent = MySimpleAgent(model_name="qwen-plus")
    print(new_agent)