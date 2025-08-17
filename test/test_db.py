# test_db.py
from app.db.session import engine
from sqlalchemy import create_engine, text

try:
    with engine.connect() as conn:
        result = conn.execute(text("SELECT 1"))
        print("✅ 数据库连接成功！")
        print("查询结果:", result.fetchone())
except Exception as e:
    print("❌ 数据库连接失败:", str(e))