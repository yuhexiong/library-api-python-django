# 使用官方 Python 镜像作为基础镜像
FROM python:3.11-slim

# 安装 MySQL 客户端和构建所需的工具
RUN apt-get update && apt-get install -y \
    pkg-config \
    libmariadb-dev \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# 设置工作目录
WORKDIR /app

# 安装依赖
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# 复制当前目录内容到容器内
COPY . /app/

# 设置容器启动时运行的命令
CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
