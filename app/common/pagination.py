# schemas/pagination.py
from typing import Generic, TypeVar, List, Optional
from pydantic import BaseModel, Field

T = TypeVar('T')

class PageResponse(BaseModel, Generic[T]):
    """
    分页响应包装类
    """
    list: List[T] = Field(default_factory=list)
    total: int = 0
    page: int = 1
    size: int = 10
    has_next: bool = False

    @classmethod
    def create(cls, data: List[T], total: int, page: int, size: int):
        return cls(
            list=data,
            total=total,
            page=page,
            size=size,
            has_next=page * size < total
        )