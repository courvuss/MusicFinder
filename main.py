import telebot
import requests
#<=== Импорты библиотек ===>
from telebot.types import Message, ReplyKeyboardRemove
import dotenv
import telebot
import os
from reply import menu_buttons
dotenv.load_dotenv()
bot = telebot.TeleBot(os.getenv("TOKEN"))

#<=== Функция для стартовой команды ===>
@bot.message_handler(commands=['start'])
def start(message: Message):
    chat_id = message.chat.id
    bot.send_message(chat_id, 'Вас приветствует бот для нахождения музыки в телеграмме', reply_markup=menu_buttons())
#<=== Функция для поиска в википедии через библиотеку - wikipedia ===>
@bot.message_handler(regexp='Найти музыку')
def reaction_for_artist(message: Message):
    chat_id = message.chat.id
    bot.delete_message(chat_id, message.message_id)
    bot.send_message(chat_id, 'Введите имя исполнителя или трека: ')
    bot.register_next_step_handler(message, get_text_for_wikipedia)#<=== Запуск следуйшей функции ===>
#<=== Получение ответа от википедии и в случае провала отправка сообщения об ошибке ===>
def get_text_for_wikipedia(message: Message):
    chat_id = message.chat.id
    artist_songname = message.text
    url = f"https://api.deezer.com/search?q={artist_songname}"
    response = requests.get(url)

    if response.status_code == 200 and response.text.strip():
        data = response.json()

        # Проходим по списку треков в ключе "data"
        for track in data.get("data", []):
            title = track["title"]
            artist = track["artist"]["name"]
            duration = track["duration"]
            request_get = (f"🎵 {artist} — {title} ({duration} сек.)")
            bot.send_message(chat_id, request_get)
    else:
        print("Ошибка при получении данных")

    #<=== Функция чтобы бот даже после ошибок продолжал работать ===>
bot.infinity_polling()