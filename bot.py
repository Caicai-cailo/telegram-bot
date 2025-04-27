import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from config import load_config
from openai_handler import get_openai_response, format_response

# 设置日志
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# 全局变量存储 bot 信息
bot_info = None

# 命令处理函数
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    user = update.effective_user
    await update.message.reply_text(
        f"你好 {user.first_name}! 我是一个AI聊天机器人。发送任何消息与我交流吧!"
    )

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("我是一个AI聊天机器人。你可以直接向我发送消息,我会通过AI给你回复!")

# 处理消息
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    global bot_info
    if not bot_info:
        bot_info = await context.bot.get_me()

    user_message = update.message.text
    chat = update.effective_chat
    chat_id = chat.id

    # 私聊无条件响应
    if chat.type == "private":
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        try:
            response = get_openai_response(user_message)
            formatted_response = format_response(response)
            await update.message.reply_text(
                formatted_response,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error in handling private message: {e}")
            await update.message.reply_text("抱歉,处理您的请求时出现错误,请稍后再试。")
        return

    # 群组/超级群组，仅@或被回复时响应
    # 检查@机器人
    mentioned = False
    if update.message.entities:
        for entity in update.message.entities:
            if entity.type == "mention":
                mention_text = user_message[entity.offset: entity.offset + entity.length]
                if bot_info and bot_info.username:
                    if mention_text.lower() == f'@{bot_info.username.lower()}':
                        mentioned = True
                        break

    # 检查是否回复了机器人
    is_reply = (
        update.message.reply_to_message and
        update.message.reply_to_message.from_user and
        bot_info and
        update.message.reply_to_message.from_user.id == bot_info.id
    )

    if mentioned or is_reply:
        await context.bot.send_chat_action(chat_id=chat_id, action="typing")
        try:
            response = get_openai_response(user_message)
            formatted_response = format_response(response)
            await update.message.reply_text(
                formatted_response,
                parse_mode='Markdown'
            )
        except Exception as e:
            logger.error(f"Error in handling group message: {e}")
            await update.message.reply_text("抱歉,处理您的请求时出现错误,请稍后再试。")
    # 否则忽略
    return

def main() -> None:
    global bot_info
    # 加载配置
    config = load_config()

    # 创建应用并设置token
    application = Application.builder().token(config["TELEGRAM_TOKEN"]).build()

    # 获取bot信息并赋值
    async def setup_bot_info(app):
        global bot_info
        bot_info = await app.bot.get_me()
    application.post_init = setup_bot_info

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
