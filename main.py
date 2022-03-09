import json
from aiogram import Bot, Dispatcher, utils
from aiohttp import request
from celery import Celery
import httpx

TELEGRAM_TOKEN = "5154320303:AAH3bcWtV498MMPOIQ8BVM7bkN5NHf9XIWQ"
CHAT_ID = 78114722
# Initialize bot and dispatcher
bot = Bot(token=TELEGRAM_TOKEN)
dp = Dispatcher(bot)

app = Celery()

def get_atm_list():
    request = httpx.post(
        'https://api.tinkoff.ru/geo/withdraw/clusters', 
        data={
            "bounds":{
                "bottomLeft":{"lat":53.49386236040929,"lng":49.24326325489341},
                "topRight":{"lat":53.5716913681692,"lng":49.54212571216879}},
                "filters":{
                    "banks":["tcs"],
                    "showUnavailable":True,
                    "currencies":["USD"]
                    },
                "zoom":13
            }
        )
        
    response = request.json()

    if len(response.payload.cluster) > 0:
        send_message(json.dumps(response.payload.cluster))

def send_message(message):
    try:
        bot.send_message(text = message, chat_id = CHAT_ID)
    except utils.exceptions.ChatNotFound:
        print("Chat is not found")

def on_startup():
    app.add_periodic_task(30, get_atm_list)

if __name__ == "__main__": 
    dp.polling(on_startup=on_startup)