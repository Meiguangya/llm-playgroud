# crud.py
from datetime import date
from typing import Optional, Tuple, List

from sqlalchemy import and_, func
from sqlalchemy.orm import Session
from app.models.employee import Employee
from app.schemas.employee import EmployeeQuery


def update_employee(db: Session, emp_no: int, new_data: dict, current_version: int):
    employee = db.query(Employee).filter(Employee.emp_no == emp_no).first()
    if not employee:
        raise ValueError("Employee not found")
    if employee.version != current_version:
        raise ValueError("Version conflict: data has been modified by another user")

    for k, v in new_data.items():
        setattr(employee, k, v)
    employee.version += 1
    db.commit()
    db.refresh(employee)
    return employee

def get_employee_by_emp_no(db: Session, emp_no: int) -> Optional[Employee]:
    return db.query(Employee).filter(Employee.emp_no == emp_no).first()


def get_employees_paginated(db: Session, query: EmployeeQuery) -> Tuple[List[Employee], int]:
    """
    分页查询员工，返回 (数据列表, 总数)
    """
    # 构建查询条件
    filters = []
    if query.first_name:
        filters.append(Employee.first_name.like(f"%{query.first_name}%"))
    if query.last_name:
        filters.append(Employee.last_name.like(f"%{query.last_name}%"))
    if query.gender:
        filters.append(Employee.gender == query.gender)

    # 查询总数
    total = db.query(Employee).filter(and_(*filters)).count()

    # 查询分页数据
    data = (
        db.query(Employee)
        .filter(and_(*filters))
        .order_by(Employee.emp_no.asc())
        .offset(query.offset)
        .limit(query.limit)
        .all()
    )

    return data, total


def get_employee_count(
    db: Session,
    first_name: Optional[str] = None,
    last_name: Optional[str] = None,
    gender: Optional[str] = None,
    birth_date_min: Optional[date] = None,
    birth_date_max: Optional[date] = None
) -> int:
    """
    根据条件查询员工总数（只返回 count）
    """
    query = db.query(func.count(Employee.emp_no))  # 只 select count

    if first_name:
        query = query.filter(Employee.first_name.ilike(f"%{first_name}%"))
    if last_name:
        query = query.filter(Employee.last_name.ilike(f"%{last_name}%"))
    if gender:
        query = query.filter(Employee.gender == gender.upper())
    if birth_date_min:
        query = query.filter(Employee.birth_date >= birth_date_min)
    if birth_date_max:
        query = query.filter(Employee.birth_date <= birth_date_max)

    return query.scalar()  # 返回单个数值