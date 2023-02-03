import telebot
from telebot import types
import time
import random

user_sweets=0
sweets=30
max_sweet=28
turn=0
flag="Игрок 1"
ttime=1
bot = telebot.TeleBot("6137723587:AAHRi6cuFIlu_NPGY_YpokrE0s64ySXL50E")
@bot.message_handler(commands=['start'])

def start(message):
    global sweets
    global name1
    global name2
    global flag
    name1 = message.from_user.first_name
    name2 = "Игрок 2"
    first_turn = random.choice([name1, name2])
    flag = name1 if first_turn==name1 else name2
    bot.send_message(message.chat.id, f"{message.from_user.first_name}, привет!\n Ты в игре.\n "
                                      f"Правила: На столе лежит 221 конфета. Играют два игрока делая ход друг после друга. "
                                      f"Первый ход определяется жеребьёвкой. "
                                      f"За один ход можно забрать не более чем 28 конфет. \n "
                                      f"Победит тот, кто заберет последнюю конфету")
    button(message)


def game(message):
    global turn
    global sweets
    global flag
    time.sleep(ttime)
    bot.send_message(message.chat.id, f"Ваш ход {flag}")
    if flag== name1:
        bot.send_message(message.chat.id, f"{flag}, введите количество конфет")
        bot.register_next_step_handler(message,get_input)
    else:
        get_count_bot(message)

def get_count_bot(message):
    time.sleep(ttime)
    global sweets
    global flag
    global turn
    if sweets <= max_sweet:
        turn = max_sweet
    elif sweets % max_sweet == 0:
        turn = max_sweet - 1
    else:
        turn = sweets % max_sweet - 1
    if turn>0:
        sweets=sweets-turn
    else:
        turn=random.randint(1,max_sweet)
        sweets = sweets - turn
    bot.send_message(message.chat.id, f"{flag} взял {turn} конфет")
    if sweets > 0:
        bot.send_message(message.chat.id, f"Осталось {sweets} конфет")
        flag = name1
        game(message)
    else:
        bot.send_message(message.chat.id, f"Осталось 0 конфет")
        time.sleep(ttime)
        bot.send_message(message.chat.id, f"Конец игры. Победил {flag}")
        time.sleep(ttime)
        button(message)

def get_count(message):
    time.sleep(ttime)
    global sweets
    global flag
    sweets=sweets-turn
    if sweets > 0:
        bot.send_message(message.chat.id, f"Осталось {sweets} конфет")
        flag = name2
        game(message)
    else:
        bot.send_message(message.chat.id, f"Осталось 0 конфет")
        time.sleep(ttime)
        bot.send_message(message.chat.id, f"Конец игры. Победил {flag}")
        time.sleep(ttime)
        button(message)

def get_input(message):
    global turn
    turn = int(message.text)
    if 0<turn<=max_sweet:
        get_count(message)
    else:
        bot.send_message(message.chat.id, f"Введите не более {max_sweet}")
        game(message)

@bot.message_handler(commands=["button"])
def button(message):
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    button1=types.KeyboardButton("Да")
    button2=types.KeyboardButton("Нет")
    markup.add(button1)
    markup.add(button2)
    bot.send_message(message.chat.id,f"Новая игра. Вы готовы?",reply_markup=markup)


@bot.message_handler(content_types=["text"])
def controller(message):
    if message.text=="Да":
        game(message)
    else:
        bot.send_message(message.chat.id, f"В следующий раз обязательно сыграем")
        pass

bot.infinity_polling()
