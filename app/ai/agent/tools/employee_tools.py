# tools/employee_tools.py
from datetime import date

import requests
from typing import Optional
from langchain_core.tools import tool
from pydantic import BaseModel, Field


class EmployeeCountInput(BaseModel):
    first_name: Optional[str] = Field(
        default=None,
        description="员工的名字，用于模糊匹配，例如 'Anna' 或 'Georgi'"
    )
    last_name: Optional[str] = Field(
        default=None,
        description="员工的姓氏，用于模糊匹配，例如 'Wang' 或 'Smith'"
    )
    gender: Optional[str] = Field(
        default=None,
        description=(
            "员工性别，必须是单个字母："
            " 'M' 表示男性，'F' 表示女性。"
            " 不接受 '男'、'女'、'male'、'female' 等其他格式。"
        )
    )

    birth_date_min: Optional[date] = Field(
        default=None,
        description="出生日期下限，格式：YYYY-MM-DD，例如 1954-01-01"
    )

    birth_date_max: Optional[date] = Field(
        default=None,
        description="出生日期上限，格式：YYYY-MM-DD，例如 1960-12-31"
    )


@tool(args_schema=EmployeeCountInput)
def fetch_employee_count(
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    gender: Optional[str] = None,
    birth_date_min: Optional[date] = None,
    birth_date_max: Optional[date] = None
) -> str:
    """
    查询符合指定条件的员工总人数。
    注意：gender 参数必须是 'M' 或 'F'，不要传中文。
    """
    base_url = "http://localhost:9001"
    endpoint = "/employees/count"
    params = {}
    if first_name:
        params["first_name"] = first_name
    if last_name:
        params["last_name"] = last_name
    if gender:
        params["gender"] = gender.upper()  # 确保大写
    if birth_date_min:
        params["birth_date_min"] = birth_date_min.isoformat()  # 转为 "YYYY-MM-DD"
    if birth_date_max:
        params["birth_date_max"] = birth_date_max.isoformat()

    print(f"params{params}")

    try:
        response = requests.get(f"{base_url}{endpoint}", params=params, timeout=10)
        response.raise_for_status()
        data = response.json()

        if data.get("code") == 200:
            count = data["data"]
            return f"查询到符合条件的员工数量为: {count}"
        else:
            return f"查询失败: {data.get('message', '未知错误')}"

    except requests.exceptions.RequestException as e:
        return f"请求失败: {str(e)}"
    except Exception as e:
        return f"解析响应失败: {str(e)}"