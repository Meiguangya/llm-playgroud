from typing import Generic, TypeVar, Optional
from pydantic import BaseModel

T = TypeVar('T')


class ApiResponse(BaseModel, Generic[T]):
    """
    统一响应包装类
    """

    code: int
    message: str
    data: Optional[T] = None

    @classmethod
    def success(cls, data: T = None, message: str = "success"):
        return cls(code=200, message=message, data=data)

    @classmethod
    def fail(cls, code: int = 400, message: str = ""):
        return cls(code=code, message=message, data=None)
