# 使用支持 Python 3.12 的官方镜像
FROM python:3.12-slim

# 设置工作目录
WORKDIR /app

# 复制依赖文件并安装
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 复制项目代码
COPY . .

# 复制 .env 文件（仅用于开发环境）
COPY .env .env

# 声明端口
EXPOSE 8000

# 启动 FastAPI 应用
# 假设你的 app 实例在 app/main.py 中：app = FastAPI()
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]