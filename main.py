import os
import asyncio
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import telebot
from telebot.types import ReplyKeyboardMarkup, KeyboardButton, WebAppInfo
import uvicorn

# --- НАСТРОЙКИ ---
# Токен бота (лучше передавать через переменные окружения Docker, либо вставь временно строкой)
BOT_TOKEN = os.getenv("BOT_TOKEN", "ТВОЙ_ТОКЕН_БОТА")
# URL, где будет крутиться твой сервер (нужен для WebApp кнопки)
WEBAPP_URL = os.getenv("WEBAPP_URL", "https://твой-домен.ru")

bot = telebot.TeleBot(BOT_TOKEN)
app = FastAPI()

# Монтируем папку static, чтобы были доступны картинки и манифест TON Connect
app.mount("/static", StaticFiles(directory="static"), name="static")

# --- ЛОГИКА ФРОНТЕНДА (FastAPI) ---
@app.get("/")
async def read_root():
    # Отдаем твой index.html из папки static
    return FileResponse("static/index.html")

# --- ЛОГИКА БОТА (pyTelegramBotAPI) ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True)
    
    # Кнопка, которая откроет твой WebApp (index.html) прямо внутри Телеграма
    webapp_info = WebAppInfo(url=WEBAPP_URL)
    web_app_button = KeyboardButton(text="🚀 Открыть Квантовое Приложение", web_app=webapp_info)
    
    markup.add(web_app_button)
    
    welcome_text = (
        f"Привет, {message.from_user.first_name}! ⚡\n\n"
        f"Добро пожаловать в проект QUANCORE.\n"
        f"Здесь ты можешь подключить кошелек, выполнять задания и получать токены QC.\n\n"
        f"Нажми на кнопку ниже, чтобы запустить приложение!"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# --- ЗАПУСК ---
async def run_bot():
    print("Бот успешно запущен...")
    # Чтобы бот не блокировал веб-сервер, запускаем его в бесконечном неблокирующем цикле
    while True:
        try:
            bot.polling(none_stop=True, interval=0, timeout=20)
        except Exception as e:
            print(f"Ошибка бота: {e}")
            await asyncio.sleep(5)

@app.on_event("startup")
async def startup_event():
    # Запускаем бота в бэкграунде при старте FastAPI
    asyncio.create_task(run_bot())

if __name__ == "__main__":
    # Запуск сервера на порту 8000
    uvicorn.run(app, host="0.0.0.0", port=8000)
