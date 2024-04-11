import os
from dotenv import load_dotenv, find_dotenv

if not find_dotenv():  # Функция поиска переменных окружения
    exit("Переменные окружения не загружены, так как отсутствует файл .env")
else:
    load_dotenv()  # Загрузка переменных окружения


BOT_TOKEN = os.getenv("BOT_TOKEN")
