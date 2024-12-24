import logging
import os
import telebot
from flask import Flask, request
from telebot.apihelper import ApiTelegramException

# Настройка логирования
logging.basicConfig(
    level=logging.DEBUG,  # Установите DEBUG для подробных логов
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),  # Логи будут выводиться в консоль
    ]
)

logger = logging.getLogger(__name__)

# Токен бота
TOKEN = '7565067409:AAF-mHyv0CWgQ_UUQnhNZZ8NtfpMk5eo-x8'
if not TOKEN:
    logger.error("Переменная окружения TELEGRAM_TOKEN не установлена")
    raise ValueError("Переменная окружения TELEGRAM_TOKEN не установлена")

bot = telebot.TeleBot(TOKEN)
app = Flask(__name__)

# Пример вопросов
questions = [
    {
        "question": "Шуршат в кармане, в кошельке, считать все любят их в уме, а я желаю вам, ребята, их много-много в двадцать пятом!",
        "options": ["Вороны", "Семечки", "Деньги"],
        "answer": "Деньги"
    },
    # Добавьте другие вопросы...
]

# Логирование получения команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    try:
        logger.info(f"Получена команда /start от пользователя {message.chat.id}")
        bot.send_message(
            message.chat.id,
            "Пожелания-загадки приготовил дед Мороз! Отгадайте и узнайте, что в мешке он вам принес! Готовы?"
        )
        ask_question(message.chat.id, 0)  # Начало игры
    except Exception as e:
        logger.error(f"Ошибка в send_welcome: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте снова позже.")

# Логирование вопросов и ответов
def ask_question(chat_id, question_index):
    try:
        if question_index < len(questions):
            question = questions[question_index]
            logger.debug(f"Задаём вопрос {question_index} пользователю {chat_id}: {question['question']}")
            markup = telebot.types.ReplyKeyboardMarkup(one_time_keyboard=True, resize_keyboard=True)
            for option in question["options"]:
                markup.add(option)
            bot.send_message(chat_id, question["question"], reply_markup=markup)
            bot.register_next_step_handler_by_chat_id(chat_id, lambda msg: check_answer(msg, question_index))
        else:
            logger.info(f"Пользователь {chat_id} ответил на все вопросы")
            bot.send_message(chat_id, "Поздравляю, вы отгадали все загадки! С Новым годом!!!")
    except Exception as e:
        logger.error(f"Ошибка в ask_question: {e}")
        bot.send_message(chat_id, "Произошла ошибка. Попробуйте снова позже.")

def check_answer(message, question_index):
    try:
        question = questions[question_index]
        logger.debug(f"Ответ от пользователя {message.chat.id}: {message.text}")
        if message.text == question["answer"]:
            bot.send_message(message.chat.id, "Правильно! 🎉")
        else:
            bot.send_message(message.chat.id, f"Увы, неверно. Правильный ответ: {question['answer']}.")
        ask_question(message.chat.id, question_index + 1)
    except IndexError:
        logger.error(f"Вопрос с индексом {question_index} не найден.")
        bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте снова.")
    except Exception as e:
        logger.error(f"Ошибка в check_answer: {e}")
        bot.send_message(message.chat.id, "Произошла ошибка. Попробуйте снова позже.")

# Команда /help
@bot.message_handler(commands=['help'])
def send_help(message):
    bot.send_message(
        message.chat.id,
        "Команды:\n"
        "/start - Начать игру\n"
        "/help - Получить справку"
    )

# Обработка Webhook
@app.route(f"/{TOKEN}", methods=['POST'])
def webhook():
    json_data = request.get_data(as_text=True)
    logger.debug(f"Получен запрос Webhook: {json_data}")
    update = telebot.types.Update.de_json(json_data)
    bot.process_new_updates([update])
    return "OK", 200

if __name__ == "__main__":
    try:
        logger.info("Удаляем старый Webhook...")
        bot.remove_webhook()
        logger.info("Устанавливаем новый Webhook...")
        webhook_url = f"https://ng2025-92xj.onrender.com/{TOKEN}"
        if not webhook_url.startswith("https://"):
            logger.error("Webhook URL должен использовать HTTPS.")
            raise ValueError("Webhook URL должен использовать HTTPS.")
        success = bot.set_webhook(url=webhook_url)
        if success:
            logger.info("Webhook успешно установлен.")
        else:
            logger.warning("Не удалось установить Webhook.")
        logger.info("Запуск Flask-приложения...")
        app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 10000)))
    except ApiTelegramException as e:
        logger.error(f"Ошибка установки Webhook: {e}")
