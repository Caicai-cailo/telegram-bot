# 使用官方 Python 镜像
FROM python:3.11-slim

# 设置工作目录
WORKDIR /app

# 拷贝文件
COPY . /app

# 安装依赖
RUN pip install --upgrade pip \
    && pip install -r requirements.txt

# 启动程序
CMD ["python", "bot.py"]
