from typing import Dict

from app.ai.graph.chat_graph import ChatGraph


class ChatGraphService:
    _instances: Dict[str, ChatGraph] = {}

    @classmethod
    def get_chat_graph(cls, config: dict) -> ChatGraph:
        """获取或创建DialogGraph实例（单例模式）"""
        # 使用配置作为唯一标识
        config_key = f"{config['model_name']}"

        if config_key not in cls._instances:
            cls._instances[config_key] = ChatGraph(
                model_name=config["model_name"],
                memory=True
            )

        print(f"_instances:{cls._instances}")

        return cls._instances[config_key]
