from copy import copy
from converter import Convertor, ApiError
from telebot import *
from config import *


bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands= ['start'])
def start(message: telebot.types.Message):
    if message.chat.username:
        mess = f'Привет, {message.from_user.username}'
        bot.reply_to(message, mess)
    else:
        mess = f'Привет, {message.from_user.first_name} {message.from_user.last_name if message.from_user.last_name else ""}'
        bot.reply_to(message, mess)
    mess = 'Я бот Гоша. Создан чтобы помочь узнать актуальные курсы валют (любых валют из существующих). Чтобы узнать курс интересующей нас валюты необходимо написать мне запрос в следующем виде ' \
           '\n\n<Имя валюты, цену которой хотим узнать> <Имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>' \
           '\n\nКоличество валюты необходимо записать либо целым числом либо десятичную дробью, а названия необходимо писать с БОЛЬШОЙ буквы. ' \
           '\nДля того чтобы правильно записать название валют рекомендую воспользоваться командой /values (команда также находится в разделе встроенных кнопок). Чтобы вызвать встроенные кнопки необходимо прописать команду /buttons. Также в помимо /values там будут находиться курсы самых популярных валют, и кнопка \help если вы вдруг забыли, что и как работает.' \
           '\nУДАЧИ!'
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands= ['help'])
def help(message: telebot.types.Message):
    mess = "Так и знал, что что-то забудешь. Вкратце напомню, что да как. Чтобы узнать курс интересующей нас валюты необходимо написать мне запрос в следующем виде " \
           "\n\n<Имя валюты, цену которой хотим узнать> <Имя валюты, в которой надо узнать цену первой валюты> <количество первой валюты>" \
           "\n\nКоличество валюты необходимо записать либо целым числом либо десятичную дробью, а названия необходимо писать с БОЛЬШОЙ буквы. " \
           "\nДля того чтобы правильно записать название валют рекомендую воспользоваться командой /values (команда также находится в разделе встроенных кнопок). Чтобы вызвать встроенные кнопки необходимо прописать команду /buttons. Также в помимо /values там будут находиться курсы самых популярных валют, и кнопка /help если вы вдруг снова забыли, что и как работает."
    bot.send_message(message.chat.id, mess)


@bot.message_handler(commands=['buttons'])
def button(message: telebot.types.Message):
    murkup = types.ReplyKeyboardMarkup()
    dol = types.KeyboardButton('/$')
    euro = types.KeyboardButton('/€')
    uan = types.KeyboardButton('/¥')
    funt = types.KeyboardButton('/£')
    val = types.KeyboardButton('/values')
    help = types.KeyboardButton('/help')
    murkup.add(dol, euro, uan, funt, val, help)
    bot.send_message(message.chat.id, f"Необходимый функционал и курсы популярных валют на данный момент:", reply_markup=murkup)


@bot.message_handler(commands=['$', '€', '¥', '£'])
def geting_pop_val(message: telebot.types.Message):
    print(pop_values[message.text[-1]])
    bot.send_message(message.chat.id, Convertor.get_price(copy(pop_values[message.text[-1]]))[3])


@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for i in value .keys():
        text = '\n'.join((text, i))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def converter(message: telebot.types.Message):
    mes = message.text.split()
    try:
        res = Convertor.get_price(mes)
        bot.reply_to(message, f"Цена {res[2]} {res[0]} в {res[1]} : {res[3]}")
    except ApiError as er:
        bot.reply_to(message, er)


bot.polling(none_stop=True)