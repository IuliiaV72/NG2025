import os
import telebot
from flask import Flask, request
from telebot.apihelper import ApiTelegramException

# Токен бота
TOKEN = "7565067409:AAF-mHyv0CWgQ_UUQnhNZZ8NtfpMk5eo-x8"

if not TOKEN:
    raise ValueError("Токен Telegram не установлен")

bot = telebot.TeleBot(TOKEN)

# Flask-приложение для обработки Webhook
app = Flask(__name__)

# Вопросы и ответы
questions = [
    {
        "question": "Шуршат в кармане, в кошельке, считать все любят их в уме, а я желаю вам, ребята, их много-много в двадцать пятом!",
        "options": ["Вороны", "Семечки", "Деньги"],
        "answer": "Деньги"
    },
    {
        "question": "Пусть говорят, что ЭТО любит одну лишь только тишину, я ГРОМКО МНОГО пожелаю его вам в будущем году.",
        "options": ["Библиотека", "Счастье", "Новый пароль от WiFi"],
        "answer": "Счастье"
    },
    {
        "question": "В аптеке ты его не купишь, и в банке ты не одолжишь... На лыжах, в парке и у моря его, конечно, сохранишь!",
        "options": ["Спокойствие", "Нервы", "Здоровье"],
        "answer": "Здоровье"
    }
]

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(
        message.chat.id,
        "Пожелания-загадки приготовил дед Мороз! Отгадайте и узнайте, что в мешке он вам принес! Готовы?"
    )
    ask_question(message.chat.id, 0)

# Задаём вопрос
def ask_question(chat_id, question_index):
    if question_index < len(questions):
        question = questions[question_index]
        markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
        for option in question["options"]:
            markup.add(option)
        bot.send_message(chat_id, question["question"], reply_markup=markup)
        bot.register_next_step_handler_by_chat_id(chat_id, lambda msg: check_answer(msg, question_index))
    else:
        bot.send_message(chat_id, "Поздравляю, вы отгадали все загадки! С Новым годом!!!")

# Проверяем ответ
def check_answer(message, question_index):
    question = questions[question_index]
    if message.text == question["answer"]:
        bot.send_message(message.chat.id, "Правильно! 🎉")
    else:
        bot.send_message(message.chat.id, f"Увы, неверно. Правильный ответ: {question['answer']}.")
    ask_question(message.chat.id, question_index + 1)

# Webhook для обработки запросов Telegram
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_data = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

# Установка Webhook при запуске
if __name__ == "__main__":
    try:
        bot.remove_webhook()
        bot.set_webhook(url=f"https://ng2025-92xj.onrender.com/{TOKEN}")  # Ваш домен Render
    except ApiTelegramException as e:
        print(f"Ошибка установки Webhook: {e}")

    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
