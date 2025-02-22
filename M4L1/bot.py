from telebot import TeleBot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from logic import DatabaseManager
import schedule
import threading
import time
from config import API_TOKEN, DATABASE

bot = TeleBot(API_TOKEN)
manager = DatabaseManager(DATABASE)
manager.create_tables()

def gen_markup(prize_id):
    markup = InlineKeyboardMarkup()
    markup.row_width = 1
    markup.add(InlineKeyboardButton("Получить!", callback_data=prize_id))
    return markup

@bot.message_handler(commands=['rating'])
def handle_rating(message):
    res = manager.get_rating() 
    res = [f'| @{x[0]:<11} | {x[1]:<11}|\n{"_"*26}' for x in res]
    res = '\n'.join(res)
    res = f'| USER_NAME    | COUNT_PRIZE |\n{"_"*26}\n' + res
    bot.send_message(message.chat.id, res)

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    prize_id = call.data
    user_id = call.message.chat.id

    # Проверяем, сколько пользователей уже получили приз
    if manager.get_winners_count(prize_id) < 3:
        res = manager.add_winner(user_id, prize_id)
        if res:
            img = manager.get_prize_img(prize_id)
            with open(f'img/{img}', 'rb') as photo:
                bot.send_photo(user_id, photo, caption="Поздравляем! Ты получил картинку!")
            bot.answer_callback_query(call.id, "Поздравляем! Вы получили приз!")
        else:
            bot.answer_callback_query(call.id, "Вы уже получили этот приз!")
    else:
        bot.answer_callback_query(call.id, "К сожалению, приз уже был получен тремя пользователями!")

def send_message():
    prize = manager.get_random_prize()
    if prize:
        prize_id, img = prize[:2]
        manager.mark_prize_used(prize_id)
        hide_img(img)
        for user in manager.get_users():
            with open(f'hidden_img/{img}', 'rb') as photo:
                bot.send_photo(user, photo, reply_markup=gen_markup(prize_id))
    else:
        print("Нет доступных призов для отправки.")

def schedule_thread():
    schedule.every().hour.do(send_message)  # Измените периодичность на каждый час
    while True:
        schedule.run_pending()
        time.sleep(5)

@bot.message_handler(commands=['start'])
def handle_start(message):
    user_id = message.chat.id
    if user_id in manager.get_users():
        bot.reply_to(message, "Ты уже зарегистрирован!")
    else:
        manager.add_user(user_id, message.from_user.username)
        bot.reply_to(message, """Привет! Добро пожаловать! 
Тебя успешно зарегистрировали!
Каждый час тебе будут приходить новые картинки и у тебя будет шанс их получить!
Для этого нужно быстрее всех нажать на кнопку 'Получить!'

Только три первых пользователя получат картинку!)""")

def polling_thread():
    bot.polling(none_stop=True)

if __name__ == '__main__':
    # Создаем потоки для опроса и планировщика
    polling_thread = threading.Thread(target=polling_thread)
    scheduling_thread = threading.Thread(target=schedule_thread)

    polling_thread.start()
    scheduling_thread.start()