import requests
import json
from config import load_config
import logging

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载配置
config = load_config()


def get_openai_response(user_message):
    """通过API获取响应"""
    try:
        api_type = config["API_TYPE"]
        base_url = config["API_BASE_URL"]
        api_key = config["API_KEY"]
        model = config["MODEL"]

        # 构建请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }

        # 构建请求体
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": "你是一个友好的助手。"},
                {"role": "user", "content": user_message}
            ],
            "max_tokens": 1000,
            "temperature": 0.7
        }

        # 构建完整的API URL
        url = f"{base_url}/chat/completions"

        # 发送请求
        response = requests.post(url, headers=headers, json=data)

        # 检查响应状态
        response.raise_for_status()

        # 解析响应
        response_data = response.json()

        # 根据不同API类型解析结果
        if api_type == "openai" or api_type == "one-api" or api_type == "new-api":
            return response_data["choices"][0]["message"]["content"]
        else:
            logger.error(f"不支持的API类型: {api_type}")
            return "抱歉，发生了配置错误。请联系管理员。"

    except requests.exceptions.RequestException as e:
        logger.error(f"请求错误: {e}")
        raise Exception(f"调用API时出错: {e}")
    except (KeyError, IndexError, json.JSONDecodeError) as e:
        logger.error(f"解析响应错误: {e}")
        raise Exception(f"解析API响应时出错: {e}")
    except Exception as e:
        logger.error(f"未预期的错误: {e}")
        raise Exception(f"发生未预期的错误: {e}")