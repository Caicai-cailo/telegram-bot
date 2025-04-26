import os
from dotenv import load_dotenv


def load_config():
    """加载配置变量"""
    load_dotenv()  # 从.env文件加载环境变量

    required_vars = ["TELEGRAM_TOKEN"]
    config = {}

    for var in required_vars:
        value = os.getenv(var)
        if not value:
            raise ValueError(f"环境变量 {var} 未设置。请检查您的.env文件")
        config[var] = value

    # API配置
    config["API_TYPE"] = os.getenv("API_TYPE", "openai")  # 可选: openai, one-api, new-api

    # API基础URL
    config["API_BASE_URL"] = os.getenv("API_BASE_URL", "https://api.openai.com/v1")

    # API密钥
    config["API_KEY"] = os.getenv("API_KEY", "")
    if not config["API_KEY"]:
        raise ValueError("环境变量 API_KEY 未设置。请检查您的.env文件")

    # 模型配置
    config["MODEL"] = os.getenv("MODEL", "gpt-3.5-turbo")

    return config