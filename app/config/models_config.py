# app/config/models_config.py
# 可配置的模型列表（可从数据库、文件、环境变量等加载，此处为示例）

SUPPORTED_MODELS = [
    {
        "model": "deepseek-chat",
        "desc": "deepseek-chat"
    },
    {
        "model": "qwen-max",
        "desc": "适合复杂任务，推理能力最强"
    },
    {
        "model": "qwen-plus",
        "desc": "效果与速度均衡，适合中等复杂任务"
    },
    {
        "model": "qwen-turbo",
        "desc": "速度快，成本低，适合简单任务"
    }
    # 后续可扩展更多模型
]