# app/api/dashscope.py
from fastapi import APIRouter,Request, Header
from app.config.models_config import SUPPORTED_MODELS
from app.ai.services.chat_service import stream_chat_response
from fastapi.responses import StreamingResponse

import asyncio

router = APIRouter(prefix="/api/v1/dashscope", tags=["DashScope"])

@router.get("/getModels")
def get_supported_models():
    """
    获取后端支持的模型列表
    """
    return {
        "code": 10000,
        "message": "success",
        "data": SUPPORTED_MODELS
    }

