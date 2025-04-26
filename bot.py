import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import load_config
from openai_handler import get_openai_response

# 设置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)


# 命令处理函数
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """发送机器人启动时的消息"""
    user = update.effective_user
    await update.message.reply_text(
        f"你好 {user.first_name}! 我是一个AI聊天机器人。发送任何消息与我交流吧!"
    )


async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """发送帮助信息"""
    await update.message.reply_text("我是一个AI聊天机器人。你可以直接向我发送消息，我会通过AI给你回复!")


# 处理消息
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """处理用户消息并调用API"""
    user_message = update.message.text
    chat_id = update.effective_chat.id
    
    # 发送"正在输入"状态
    await context.bot.send_chat_action(chat_id=chat_id, action="typing")
    
    try:
        # 调用API
        response = get_openai_response(user_message)
        
        # 使用Telegram的parse_mode以支持Markdown格式
        await update.message.reply_text(
            response, 
            parse_mode="Markdown",
            disable_web_page_preview=True  # 防止链接预览干扰格式
        )
    except Exception as e:
        logger.error(f"Error in handling message: {e}")
        await update.message.reply_text("抱歉，处理您的请求时出现错误，请稍后再试。")


def main() -> None:
    """启动机器人"""
    # 加载配置
    config = load_config()

    # 创建应用并设置token
    application = Application.builder().token(config["TELEGRAM_TOKEN"]).build()

    # 添加命令处理器
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("help", help_command))

    # 添加消息处理器
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    # 启动机器人
    logger.info("Starting bot...")
    application.run_polling()


if __name__ == "__main__":
    main()
