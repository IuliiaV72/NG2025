import telebot
import telebot
from telebot.apihelper import ApiTelegramException

# Ваш токен от BotFather
TOKEN = '7565067409:AAEQiThMAmfN1MeWXdfuN2hERMLQdRr-JaU'
bot = telebot.TeleBot(TOKEN)

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
bot.get_updates(offset=-1)
# Обработчик команды /start
@bot.message_handler(commands=['start'])
def send_welcome(message):
    bot.send_message(message.chat.id, "Пожелания-загадки приготовил дед Мороз! Отгадайте и узнайте, что в мешке он вам принес! Готовы?")
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
        bot.send_message(chat_id, "Поздравляю, вы отгадали все загадки! С Новым годом!!!☃️🍾🎄")

# Проверяем ответ
def check_answer(message, question_index):
    question = questions[question_index]
    if message.text == question["answer"]:
        bot.send_message(message.chat.id, "Правильно! 🎉")
    else:
        bot.send_message(message.chat.id, f"Увы, неверно. Но дедушка Мороз очень добрый, поэтому в Новом году Вас обязательно ждёт: {question['answer']}!!!")
    ask_question(message.chat.id, question_index + 1)

# Запуск бота
bot.polling()
