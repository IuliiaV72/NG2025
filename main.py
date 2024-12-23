import telebot

# Ваш токен от BotFather
TOKEN = "7565067409:AAE4oSFTqwBDud3l4JG0XtcjbibFlopEaRw"
bot = telebot.TeleBot(TOKEN)

# Вопросы и ответы
questions = [
    {
        "question": "Шуршат в кармане, в кошельке, считать их любят все в уме, я пожелаю вам, ребята, их много-много в двадцать пятом.",
        "options": ["Вороны", "Семечки", "Деньги"],
        "answer": "Деньги"
    },
    {
        "question": "Пусть кто-то говорит, что любит оно лишь только тишину, я громко много пожелаю его вам в будущем году.",
        "options": ["Библиотека", "Счастье", "Новый пароль от WiFi"],
        "answer": "Счастье"
    },
    {
        "question": "В аптеке ты его не купишь, и в банке ты не одолжишь, на лыжах, в парке и у моря его, конечно, сохранишь!",
        "options": ["Спокойствие", "Нервы", "Здоровье"],
        "answer": "Здоровье"
    }
]

# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Привет! Давай поиграем в новогодние загадки! Готов?")
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
        bot.send_message(chat_id, "Поздравляю, вы отгадали все загадки! С Новым годом!")

# Проверяем ответ
def check_answer(message, question_index):
    question = questions[question_index]
    if message.text == question["answer"]:
        bot.send_message(message.chat.id, "Правильно! 🎉")
    else:
        bot.send_message(message.chat.id, f"Увы, неверно. Правильный ответ: {question['answer']}.")
    ask_question(message.chat.id, question_index + 1)

# Запуск бота
bot.polling()