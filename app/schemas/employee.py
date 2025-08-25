from typing import Optional

from pydantic import BaseModel
from datetime import date

class EmployeeBase(BaseModel):
    emp_no: int
    birth_date: date
    first_name: str
    last_name: str
    gender: str
    hire_date: date
    version: int = 1

    model_config = {
        "from_attributes": True
    }


class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    first_name: str = None
    last_name: str = None
    gender: str = None
    hire_date: date = None
    version: int = None


class EmployeeQuery(BaseModel):
    """
    员工查询条件（可扩展）
    """
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    gender: Optional[str] = None  # 'M' or 'F'
    page: int = 1
    size: int = 10

    # 防止非法分页
    @property
    def offset(self) -> int:
        return (self.page - 1) * self.size

    @property
    def limit(self) -> int:
        return self.size

