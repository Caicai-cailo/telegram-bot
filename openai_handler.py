import requests
import json
from config import load_config
import logging
import re
import html

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载配置
config = load_config()

# 在openai_handler.py中添加一个格式化函数

import re

def format_response(text):
    """格式化API返回的文本，使其在Telegram中显示更美观 (Markdown)"""
    # 1.只保留一级标题
    text = re.sub(r'^#{2,} (.+)$', r'**\1**', text, flags=re.MULTILINE)   # 将 ##... 或更高级标题转为加粗
    
    # 2. 列表项，行首"- "
    # Telegram Markdown对 "• " 同样只当普通文本，所以可以直接保留 "- "
    # 但如果想统一为 "• "，如下所示：
    text = re.sub(r'^- (.+)$', r'• \1', text, flags=re.MULTILINE)
    
    # 3. 粗体
    # 保持 Markdown 格式
    # 可以让 AI 输出就用 **加粗**，无需替换
    # 但如果有些是 <b>...</b>，也建议转回成 **...**
    text = re.sub(r'<b>(.+?)</b>', r'**\1**', text)
    
    # 4. 斜体
    text = re.sub(r'<i>(.+?)</i>', r'_\1_', text)
    
    # 5. 多余空行
    text = re.sub(r'\n{3,}', r'\n\n', text)
    
    return text.strip()

def get_openai_response(user_message):
    """通过API获取响应并格式化"""
    try:
        api_type = config["API_TYPE"]
        base_url = config["API_BASE_URL"]
        api_key = config["API_KEY"]
        model = config["MODEL"]
        
        # 添加系统提示来指导输出格式
        system_prompt = """你是一个友好的助手。请以清晰的结构回复用户：
        1. 给重要概念添加标题，使用'## '开头
        2. 使用列表和项目符号组织信息 (用'- '开始列表项)
        3. 使用**粗体**标记重要内容
        4. 使用_斜体_标记次要强调
        5. 在主题转换处添加分隔符 (---)
        6. 对于关键概念，使用◆标记
        7. 保持简洁，每个段落不超过3行"""
        
        # 构建请求头
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {api_key}"
        }
        
        # 构建请求体
        data = {
            "model": model,
            "messages": [
                {"role": "system", "content": system_prompt},
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
            raw_response = response_data["choices"][0]["message"]["content"]
            
            # 应用格式优化
            formatted_response = format_response(raw_response)
            return formatted_response
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
