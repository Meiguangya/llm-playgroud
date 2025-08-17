# app/api/users.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app import schemas, models, crud
from app.db.session import SessionLocal
from app.core.security import get_password_hash

router = APIRouter(prefix="/users", tags=["users"])


# 依赖：获取数据库会话
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.post("/register", response_model=schemas.UserOut, status_code=status.HTTP_201_CREATED)
def register_user(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    """
    用户注册接口
    - **username**: 用户名（必填）
    - **password**: 密码（明文，后端自动加密）
    - **email**: 邮箱（可选）
    """
    # 检查用户名是否已存在
    existing_user_by_username = db.query(models.User).filter(models.User.username == user_in.username).first()
    if existing_user_by_username:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该用户名已被使用"
        )

    # 检查邮箱是否已存在（如果提供了邮箱）
    if user_in.email:
        existing_user_by_email = db.query(models.User).filter(models.User.email == user_in.email).first()
        if existing_user_by_email:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="该邮箱已被注册"
            )

    # 创建新用户（密码加密）
    db_user = models.User(
        username=user_in.username,
        hashed_password=get_password_hash(user_in.password),
        email=user_in.email,
        is_active=True
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)

    return db_user