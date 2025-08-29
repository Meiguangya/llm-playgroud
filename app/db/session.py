# app/db/session.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

load_dotenv()

# 从 .env 读取数据库 URL
DATABASE_URL = os.getenv("DATABASE_URL")

if not DATABASE_URL:
    raise ValueError("DATABASE_URL not set in environment variables")


# 创建数据库引擎
engine = create_engine(
    DATABASE_URL,
    # 可选参数
    pool_pre_ping=True,        # 验证连接有效性
    echo=True,                # 开启 SQL 日志（调试时设为 True）
    pool_size=10,              # 连接池大小
    max_overflow=20,           # 最大溢出连接数
)

# 创建会话工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 声明基类
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()