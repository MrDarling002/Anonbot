import config
import telebot
from telebot import types
from database import Database

db = Database('D:/DB/Новый текстовый документ.txt')

bot = telebot.TeleBot(config.TOKEN)

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 =types.KeyboardButton('👾 Поиск собеседника')
    markup.add(item1)

    bot.send_message(message.chat.id, 'Привет Странник! Ищешь с кем можешь анонимно пообщаться? Ты попал по адресу!'.format(message.from_user),reply_markup=markup)
    stik = open('static/sticker.webp', 'rb')
    bot.send_sticker(message.chat.id, stik)


@bot.message_handler(commands=['stop'])
def stop(message):
    chat_info = db.get_active(message.chat.id)
    if chat_info != False:
        db.delete_chat(chat_info[0])
        markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
        item1 =types.KeyboardButton('👾 Поиск собеседника')
        markup.add(item1)
        bot.send_message(chat_info[1], "Собеседник покинул чат",reply_markup=markup)
        bot.send_message(message.chat.id, "Вы вышли из чата", reply_markup=markup)

@bot.message_handler(content_types=['text'])
def bot_message(message):
    if message.chat.type == 'private':
        if message.text == '👾 Поиск собеседника':
            markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
            item1 = types.KeyboardButton('Остановить поиск')
            markup.add(item1)

            chat_two = db.get_chat()

            if db.create_chat(message.chat.id, chat_two) == False:
                db.add_wait(message.chat.id)
                bot.send_message(message.chat.id, '🫂 Поиск собеседника', reply_markup=markup)
            else:
                mess = "Собеседник найден! Чтобы остановить диалог напиши /stop"
                markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
                item1 = types.KeyboardButton('/stop')
                markup.add(item1)
                
                bot.send_message(message.chat.id, mess, reply_markup=markup)
                bot.send_message(chat_two, mess, reply_markup=markup)


        elif message.text == 'Остановить поиск':
            db.delete_queue(message.chat.id)
            bot.send_message(message.chat.id, "❌ Поиск собеседника, напишите /menu ")

        else:
            chat_info = db.get_active(message.chat.id)
            bot.send_message(chat_info[1],message.text)           
bot.polling() 