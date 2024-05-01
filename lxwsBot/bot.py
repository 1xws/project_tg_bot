import telebot
import wikipedia
import re

bot = telebot.TeleBot('6588089680:AAF2tnqu1nzsx7QGX3T2wo2jyMsuCAb9bnY')
wikipedia.set_lang("ru")

user_states = {}  # Словарь для отслеживания состояний каждого пользователя


# Функция для очистки текста статьи в Wikipedia и ограничения его до тысячи символов
def getwiki(s):
    try:
        ny = wikipedia.page(s)
        wikitext = ny.content[:1000]
        wikitext = re.sub(r'\([^()]*\)', '', wikitext)
        wikitext = re.sub(r'\([^()]*\)', '', wikitext)
        wikitext = re.sub(r'\{[^{}]*\}', '', wikitext)
        return wikitext
    except Exception as e:
        return 'В энциклопедии нет информации об этом'


# Обработка команды /start
@bot.message_handler(commands=["start"])
def start(message):
    user_states[message.chat.id] = 'start'
    bot.send_message(message.chat.id, 'Отправьте мне любое слово, и я найду его значение на Wikipedia')


# Обработка текстовых сообщений
@bot.message_handler(func=lambda message: user_states.get(message.chat.id) == 'start')
def handle_text(message):
    user_states.pop(message.chat.id)
    bot.send_message(message.chat.id, getwiki(message.text))


# Получение сообщений от пользователей
@bot.message_handler(content_types=["text"])
def handle_all_text(message):
    bot.send_message(message.chat.id, "Отправьте команду /start, чтобы начать")


# Запуск бота
bot.polling(none_stop=True, interval=0)