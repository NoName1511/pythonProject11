
import telebot
bot = telebot.TeleBot('5463495183:AAH4PD3UQmmbTRVj_us5kgc3jdSuTQWf0wc')

import gspread
gc = gspread.service_account(filename='ключ.json')
sh = gc.open('1')

user_dict = {}

class User:
    def __init__(self, cell):
        self.cell = cell
        self.valuecell = None

@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, 'Привет!')
    bot.send_message(message.chat.id, 'Введите номер ячейки (в формате A1)')
    bot.register_next_step_handler(message, get_valuecell);

@bot.message_handler(content_types=['text'])
def get_cell(message):
    bot.send_message(message.from_user.id, 'Введите номер ячейки (в формате A1)')
    bot.register_next_step_handler(message, get_valuecell);

def get_valuecell(message):
    chat_id = message.chat.id
    cell = message.text
    user = User(cell)
    user_dict[chat_id] = user
    user.cell = cell
    bot.send_message(message.from_user.id, 'Введите новое значение ячейки')
    bot.register_next_step_handler(message, get_change);

def get_change(message):
    chat_id = message.chat.id
    valuecell = message.text
    user = user_dict[chat_id]
    user.valuecell = valuecell
    worksheet = sh.sheet1
    worksheet.update(user.cell, user.valuecell)
    bot.send_message(message.from_user.id, 'Значение ячейки ' + user.cell + ' изменено на ' + user.valuecell + '')
    bot.send_message(message.from_user.id, 'Изменить другую ячейку?')
    if message.text == "да" or message.text == "Да":
        bot.register_next_step_handler(message, get_cell)


bot.polling(none_stop=True)
