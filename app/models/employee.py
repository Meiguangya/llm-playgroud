from app.db.session import Base
from sqlalchemy import Column,Integer,String, Date, Enum, Table

# 定义 gender 枚举类型
GENDER_ENUM = Enum('M', 'F', name='gender_enum')

class Employee(Base):
    __tablename__ = "employees"

    # 字段定义
    emp_no = Column(Integer, primary_key=True, comment="员工编号")
    birth_date = Column(Date, nullable=False, comment="出生日期")
    first_name = Column(String(14), nullable=False, comment="名")
    last_name = Column(String(16), nullable=False, comment="姓")
    gender = Column(GENDER_ENUM, nullable=False, comment="性别: 'M' 男, 'F' 女")
    hire_date = Column(Date, nullable=False, comment="入职日期")
    version = Column(Integer, nullable=True, default=1, comment="版本号（乐观锁）")

    def __repr__(self):
        return f"<Employee(emp_no={self.emp_no}, name={self.first_name} {self.last_name}, gender={self.gender}, hire_date={self.hire_date})>"