import os
from dotenv import load_dotenv

def load_config():
    load_dotenv()
    config = {
        "TELEGRAM_TOKEN": os.getenv("TELEGRAM_TOKEN"),
        "OPENAI_API_KEY": os.getenv("OPENAI_API_KEY"),
        "OPENAI_MODEL": os.getenv("OPENAI_MODEL", "gpt-3.5-turbo"),
        "OPENAI_TIMEOUT": int(os.getenv("OPENAI_TIMEOUT", "20")),
        "OPENAI_TEMPERATURE": float(os.getenv("OPENAI_TEMPERATURE", "0.7")),
    }
    missing = [k for k, v in config.items() if v is None and not k.startswith("OPENAI_")]
    if missing:
        raise EnvironmentError(f"缺少必要环境变量: {', '.join(missing)}")
    return config
