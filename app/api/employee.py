from datetime import date
from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Path, Query
from sqlalchemy.orm import Session

from app.common.pagination import PageResponse
from app.db.session import get_db
from app.schemas.employee import EmployeeBase, EmployeeQuery
from app.crud.employee import *
from app.common.response import ApiResponse

router = APIRouter(
    prefix="/employees",
    tags=["employees"],
    responses={404: {"description": "Not found"}}
)


@router.get("/list", response_model=ApiResponse[PageResponse[EmployeeBase]])
def list_employees(
    first_name: Optional[str] = Query(None, description="名模糊查询"),
    last_name: Optional[str] = Query(None, description="姓模糊查询"),
    gender: Optional[str] = Query(None, description="性别 M/F"),
    page: int = Query(1, ge=1, description="页码"),
    size: int = Query(10, ge=1, le=100, description="每页数量，最大100"),
    db: Session = Depends(get_db)
):
    """
    分页查询员工信息
    """
    # 构造查询对象
    query = EmployeeQuery(
        first_name=first_name,
        last_name=last_name,
        gender=gender,
        page=page,
        size=size
    )

    data, total = get_employees_paginated(db, query)

    page_result = PageResponse[EmployeeBase].create(
        data=data,
        total=total,
        page=page,
        size=size
    )

    return ApiResponse.success(data=page_result)


@router.get("/count", response_model=ApiResponse[int])
def count_employees(
    first_name: Optional[str] = Query(None, description="名模糊查询"),
    last_name: Optional[str] = Query(None, description="姓模糊查询"),
    gender: Optional[str] = Query(None, description="性别 M/F"),
    birth_date_min: Optional[date] = Query(None, description="最小出生日期，格式 YYYY-MM-DD"),
    birth_date_max: Optional[date] = Query(None, description="最大出生日期，格式 YYYY-MM-DD"),
    db: Session = Depends(get_db)
):
    """
    根据条件查询员工数量
    """
    count = get_employee_count(db,
                               first_name=first_name,
                               last_name=last_name,
                               gender=gender,
                               birth_date_min=birth_date_min,
                               birth_date_max=birth_date_max
                               )
    return ApiResponse.success(data=count)


@router.get("/{emp_no}", response_model=ApiResponse[EmployeeBase])
def read_employee(
        emp_no: int = Path(..., description="要查询的员工编号", ge=1),
        db: Session = Depends(get_db)
):
    """
    根据 emp_no 查询员工信息
    """
    employee = get_employee_by_emp_no(db, emp_no=emp_no)

    if not employee:
        return ApiResponse.fail(40001, f"找不到编号为{emp_no}的员工")



    return ApiResponse.success(employee)





