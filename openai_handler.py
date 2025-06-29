import openai
import logging
from config import load_config

config = load_config()
openai.api_key = config["OPENAI_API_KEY"]

MODEL = config["OPENAI_MODEL"]
TIMEOUT = config["OPENAI_TIMEOUT"]
TEMPERATURE = config["OPENAI_TEMPERATURE"]

logger = logging.getLogger(__name__)

async def get_openai_response(message: str) -> str:
    try:
        response = await openai.ChatCompletion.acreate(
            model=MODEL,
            messages=[
                {"role": "system", "content": "你是一个有帮助的 AI 机器人"},
                {"role": "user", "content": message}
            ],
            temperature=TEMPERATURE,
            timeout=TIMEOUT
        )
        return response
    except Exception as e:
        logger.error(f"OpenAI 请求失败: {e}")
        raise RuntimeError("获取 AI 响应失败，请稍后再试。")

def format_response(response) -> str:
    try:
        return response["choices"][0]["message"]["content"].strip()
    except Exception as e:
        logger.error(f"格式化 OpenAI 响应失败: {e}")
        return "⚠️ AI 回复解析失败。"
