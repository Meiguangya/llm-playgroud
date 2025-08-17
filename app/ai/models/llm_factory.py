# app/ai/models/llm_factory.py
from langchain_community.chat_models import ChatTongyi
from langchain_core.language_models.chat_models import BaseChatModel

# 可选：未来支持 DeepSeek（假设通过 OpenAI 兼容接口调用）
from langchain_openai import ChatOpenAI

import os


def get_llm(model_name: str) -> BaseChatModel:
    """
    LLM 工厂函数：根据模型名称返回对应的 LLM 实例
    :param model_name: 模型名称，如 qwen-max, deepseek-v3
    :return: LangChain 兼容的 LLM 实例
    """

    print(f"调用get_llm")
    model_name = model_name.strip().lower()

    # === 通义千问系列 ===
    if model_name.startswith("qwen-") or model_name in ["qwen", "qwen-max", "qwen-plus", "qwen-turbo"]:
        api_key = os.getenv("DASHSCOPE_API_KEY")
        if not api_key:
            raise ValueError("DASHSCOPE_API_KEY is required for Qwen models")
        return ChatTongyi(
            model_name=model_name,
            dashscope_api_key=api_key,
            streaming=True
        )

    # === DeepSeek 系列 ===
    elif model_name.startswith("deepseek-") or model_name in ["deepseek-v3", "deepseek-chat"]:
        api_key = os.getenv("DEEPSEEK_API_KEY")
        base_url = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")
        if not api_key:
            raise ValueError("DEEPSEEK_API_KEY is required for DeepSeek models")

        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url=base_url,  # 支持自定义 endpoint
            streaming=True
        )

    # === 其他模型（未来扩展）===
    elif model_name.startswith("gpt-"):
        api_key = os.getenv("OPENAI_API_KEY")
        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            base_url="https://api.openai.com/v1",
            streaming=True
        )

    # === 默认或未知模型 ===
    else:
        raise ValueError(f"Unsupported model: {model_name}")