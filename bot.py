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
WELCOME_MESSAGE = "Добро пожаловать"