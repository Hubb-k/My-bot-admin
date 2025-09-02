import logging
import os
from telegram import Update
from telegram.ext import Application, CommandHandler, ChatMemberHandler, ContextTypes

# Настройка логирования
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
logger = logging.getLogger(__name__)

# Загрузка конфигурации
try:
    from config import TOKEN, CHANNEL_ID
except ImportError:
    TOKEN = os.getenv("TOKEN")
    CHANNEL_ID = int(os.getenv("CHANNEL_ID")) if os.getenv("CHANNEL_ID") else None

# Приветственное сообщение
WELCOME_MESSAGE = "Добро пожаловать! Следуйте инструкции и ожидайте ответа."

async def welcome_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Отправляет приветственное сообщение новым участникам и логирует chat_id."""
    # Логируем chat_id для любого события в канале
    logger.info(f"Chat ID: {update.effective_chat.id}")
    
    # Проверяем ограничение по каналу, если CHANNEL_ID задан
    if CHANNEL_ID and update.effective_chat.id != CHANNEL_ID:
        return
    
    new_members = update.chat_member.new_chat_member
    for member in new_members:
        if member.is_bot:
            continue
        username = member.username or member.first_name
        try:
            await context.bot.send_message(
                chat_id=update.effective_chat.id,
                text=f"@{username} {WELCOME_MESSAGE}"
            )
            logger.info(f"Приветствие отправлено для {username}")
        except Exception as e:
            logger.error(f"Ошибка при отправке приветствия: {e}")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Команда /start для тестирования бота."""
    await update.message.reply_text("Бот запущен и готов к работе!")

async def error_handler(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    """Обработка ошибок."""
    logger.error(f"Ошибка: {context.error}")

def main() -> None:
    """Запуск бота."""
    application = Application.builder().token(TOKEN).build()
    application.add_handler(ChatMemberHandler(welcome_new_member, ChatMemberHandler.CHAT_MEMBER))
    application.add_handler(CommandHandler("start", start))
    application.add_error_handler(error_handler)
    
    logger.info("Бот запущен...")
    application.run_polling(allowed_updates=Update.ALL_TYPES)

if __name__ == "__main__":
    main()