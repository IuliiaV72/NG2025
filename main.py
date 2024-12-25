import os
import telebot
from flask import Flask, request

# Получаем токен бота из переменной окружения
TOKEN = os.getenv('TELEGRAM_TOKEN')  # Убедитесь, что TELEGRAM_TOKEN установлен
if not TOKEN:
    raise ValueError("Переменная окружения TELEGRAM_TOKEN не установлена")

bot = telebot.TeleBot(TOKEN)

# Flask-приложение для обработки Webhook
app = Flask(name)

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

user_answers = {}  # Храним ответы пользователей

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    chat_id = message.chat.id
    user_answers[chat_id] = []  # Инициализируем список для ответов пользователя
    bot.send_message(
        chat_id,
        "Пожелания-загадки приготовил дед Мороз! Отгадайте и узнайте, что в мешке он вам принес! Готовы?"
    )
    ask_question(chat_id, 0)

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
        # Финальное сообщение с собранными ответами
        final_message = (
            f"В 2025 году тебя ждут огромные {user_answers[chat_id][0]}, "
            f"{user_answers[chat_id][1]} без конца и, конечно, {user_answers[chat_id][2]}! С Новым годом!"
        )
        bot.send_message(chat_id, final_message)
        user_answers.pop(chat_id, None)  # Удаляем данные пользователя после завершения

# Проверяем ответ
def check_answer(message, question_index):
    chat_id = message.chat.id
    question = questions[question_index]
    user_answers[chat_id].append(message.text)  # Сохраняем ответ пользователя

    if message.text == question["answer"]:
        bot.send_message(chat_id, "Правильно! 🎉")
    else:
        bot.send_message(chat_id, f"Увы, неверно. Правильный ответ: {question['answer']}.")

    ask_question(chat_id, question_index + 1)

# Webhook для обработки запросов Telegram
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_data = request.get_data(as_text=True)
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

# Установка Webhook при запуске
if name == "main":
    WEBHOOK_URL = f"https://ng2025-92xj.onrender.com/{TOKEN}"  # Укажите ваш домен на Render
    bot.remove_webhook()
    bot.set_webhook(url=WEBHOOK_URL)
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
