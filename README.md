# OpenAI Telegram 聊天机器人

这是一个Telegram机器人，可让用户通过Telegram与AI模型进行对话。机器人接收用户消息，将其发送到API，然后将回复返回给用户。

## 功能特点

- 使用Telegram Bot API与用户交互
- 支持多种API接口(OpenAI, one-api, new-api)
- 支持配置不同的AI模型
- 简单易用的命令界面
- Docker支持，方便部署

## 安装步骤

### 方法1: 直接安装

1. 克隆此仓库:
git clone https://github.com/Caicai-cailo/openai-telegram-bot.git

cd openai-telegram-bot
3. 安装依赖项:
pip install -r requirements.txt
4. 创建一个`.env`文件，参考`.env.example`添加你的API密钥:
cp .env.example .env
然后编辑`.env`文件，添加你的Telegram Bot Token和API密钥。
5. 启动机器人:
python bot.py

### 方法2: 使用Docker部署

1. 克隆此仓库:
git clone https://github.com/Caicai-cailo/openai-telegram-bot.git

cd openai-telegram-bot
3. 创建一个`.env`文件，参考`.env.example`添加你的API密钥:
cp .env.example .env
然后编辑`.env`文件，添加你的Telegram Bot Token和API密钥。
4. 使用Docker Compose构建并启动容器:
docker-compose up -d
5. 查看日志:
docker-compose logs -f
6. 停止容器:
docker-compose down


## 配置

在`.env`文件中设置以下环境变量:

- `TELEGRAM_TOKEN`: 你的Telegram Bot Token (从BotFather获取)
- `API_TYPE`: API类型 (可选: openai, one-api, new-api)
- `API_BASE_URL`: API基础URL
  - 使用OpenAI: https://api.openai.com/v1
  - 使用one-api: https://your-one-api-url/v1
  - 使用new-api: https://your-new-api-url/v1
- `API_KEY`: API密钥
- `MODEL`: 要使用的模型 (默认: "gpt-3.5-turbo")

### One-API/New-API配置说明

如果您使用one-api或new-api中转服务：

1. 获取您的中转服务URL和API密钥
2. 在`.env`文件中设置:
API_TYPE=one-api # 或 new-api
API_BASE_URL=https://your-one-api-url/v1
API_KEY=your_api_key_from_middleware
3. 中转服务通常会保持与OpenAI API相同的接口格式，所以无需额外配置

注意：某些中转服务可能需要特定的模型标识符，请参考中转服务的文档。

## 使用方法

1. 在Telegram中查找并开始与你的机器人聊天。

2. 使用以下命令:
- `/start` - 开始与机器人交互
- `/help` - 获取帮助信息

## 部署到生产环境

对于生产环境部署，建议:

1. 使用Docker部署方式
2. 设置适当的日志记录和监控
3. 考虑使用Docker Swarm或Kubernetes进行编排
4. 使用反向代理如Nginx处理SSL终止

## 注意事项

- 确保你有足够的API额度
- 此机器人仅处理文本消息，不支持图片、音频或其他类型的媒体
- 请遵守API服务提供商和Telegram的使用条款

## 许可证

MIT
