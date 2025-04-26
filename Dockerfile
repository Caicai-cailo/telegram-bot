FROM python:3.9-slim

WORKDIR /app

# 复制项目文件
COPY requirements.txt .
COPY *.py .
COPY .env .

# 安装依赖
RUN pip install --no-cache-dir -r requirements.txt

# 运行机器人
CMD ["python", "bot.py"]