import requests
import json
from config import load_config
import logging
import re

# 设置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 加载配置
config = load_config()

def format_response(response_text):
    """优化AI回复的格式，使其在Telegram中更美观"""
    
    # 处理标题格式 (使用 Telegram Markdown)
    response_text = re.sub(r'^#\s+(.+)$', r'*\\1*', response_text, flags=re.MULTILINE)
    response_text = re.sub(r'^##\s+(.+)$', r'_\\1_', response_text, flags=re.MULTILINE)
    
    # 处理列表项，确保格式统一
    response_text = re.sub(r'^\*\s+(.+)$', r'• \\1', response_text, flags=re.MULTILINE)
    response_text = re.sub(r'^-\s+(.+)$', r'• \\1', response_text, flags=re.MULTILINE)
    
    # 优化重点内容显示
    response_text = re.sub(r'\*\*(.+?)\*\*', r'*\\1*', response_text)
    
    # 提升重要分隔符的视觉效果
    response_text = re.sub(r'^---+$', r'\n━━━━━━━━━━━━━━━\n', response_text, flags=re.MULTILINE)
    
    # 确保段落间有足够空行
    response_text = re.sub(r'\n{3,}', '\n\n', response_text)
    response_text = re.sub(r'([^\n])\n([^\n])', r'\\1\n\n\\2', response_text)
    
    return response_text

def get_openai_response(user_message):
    """通过API获取响应并格式化"""
    try:
        api_type = config["API_TYPE"]
        base_url = config["API_BASE_URL"]
        api_key = config["API_KEY"]
        model = config["MODEL"]
        
        # 添加系统提示来指导输出格式
        system_prompt = """你是一个友好的助手。请按照以下格式回复:
        1. 使用简洁清晰的语言
        2. 重要的概念或关键词用*加粗*
        3. 使用emoji增强表达（适量）
        4. 适当使用列表和分隔符提高可读性
        5. 保持回答结构化和有组织性"""
        
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
