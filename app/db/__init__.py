# app/db/__init__.py
"""
数据库初始化模块，提供统一的导入入口
"""
from .session import SessionLocal, engine, Base


# 可选：可以在这里创建所有表（不推荐在生产中直接使用，建议用 Alembic）
def init_db():
    """
    初始化数据库：创建所有未创建的表
    注意：生产环境建议使用迁移工具（如 Alembic）
    """
    import app.models  # 确保所有模型都被导入，以便 Base 能识别
    Base.metadata.create_all(bind=engine)


__all__ = [
    "session",
    "SessionLocal",
    "engine",
    "Base",
    "init_db"
]