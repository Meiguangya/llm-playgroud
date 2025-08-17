import operator
from typing import Annotated, List, Union

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from langgraph.checkpoint.memory import MemorySaver
from langgraph.graph import StateGraph, END, START
from pydantic import BaseModel

from app.ai.models.llm_factory import get_llm


class ConversationState(BaseModel):
    # 完整的对话历史
    messages: Annotated[List[Union[HumanMessage, AIMessage, SystemMessage]], operator.add]

system_prompt = "你是一个有用的助手,你的名字叫小智"

class ChatGraph:

    def __init__(self,
                 model_name: str = "",
                 memory: bool = True):
        """
        初始化对话图
        :param model_name: 模型名称（支持 qwen/gpt/claude 等）
        :param memory: 是否启用记忆
        """

        self.system_prompt = system_prompt
        self.llm_model = get_llm(model_name)
        self.memory = memory
        self.workflow = self._build_graph()

    def _build_graph(self):
        """构建对话图结构"""
        workflow = StateGraph(ConversationState)

        def call_mode(state: ConversationState):


            for msg in state.messages:
                print(f"{msg}")

            print(f"{'*'*50}")

            print(f"调用call_mode,state:{type(state)}\n {len(state.messages)}")

            messages = [SystemMessage(content=self.system_prompt)] + state.messages

            response = self.llm_model.invoke(messages)
            return {"messages": [response]}


        # 添加节点和边
        workflow.add_node("call_model", call_mode)

        workflow.add_edge(START, "call_model")
        workflow.add_edge("call_model", END)

        return workflow.compile(
            checkpointer=MemorySaver() if self.memory else None
        )
