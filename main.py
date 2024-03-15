import telebot
from telebot import types

import requests
import datetime

token = ""
appid = ""

bot = telebot.TeleBot(token)
s_city = "Moscow, RU"


def weather():
    res = requests.get("http://api.openweathermap.org/data/2.5/weather",
                       params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = res.json()
    return data


def weatherweek():
    fres = requests.get("http://api.openweathermap.org/data/2.5/forecast",
                        params={'q': s_city, 'units': 'metric', 'lang': 'ru', 'APPID': appid})
    data = fres.json()
    return data


# команды
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = types.ReplyKeyboardMarkup()
    keyboard.row("Расписание на текущую неделю", "Расписание на следующую неделю", "Неделя", "Погода",
                 "Погода на неделю", "Сайт МТУСИ", "/help")
    bot.send_message(message.chat.id,
                     "Здравсвтвуйте, " + message.from_user.first_name + "! \n \nЯ бот, который сделает обучение в МТУСИ комфортнее. \n \nНапишите команду /help или нажмите на соответствующую кнопку для ознакомления с функционалом",
                     reply_markup=keyboard)


@bot.message_handler(commands=['help'])
def start_message(message):
    bot.send_message(message.chat.id,
                     "Напишите:\nТекущая неделя или команду /текущая чтобы узнать расписание на текущую неделю; \nСледующая неделя или команду /следующая чтобы узнать расписание на следующую неделю; \nНеделя или команду /week для того чтобы узнать какая сейчас неделя; \n МТУСИ или команду /mtuci чтобы получить ссылку на главную страницу сайта МТУСИ \n \n Вы также можете использовать кнопки")


@bot.message_handler(commands=['mtuci'])
def start_message(message):
    bot.send_message(message.chat.id, "Сайт МТУСИ - https://mtuci.ru/")


@bot.message_handler(commands=['week'])
def start_message(message):
    bot.send_message(message.chat.id, "Сейчас " + "- " + "неделя.")


@bot.message_handler(commands=['текущая'])
def start_message(message):
    bot.send_message(message.chat.id, "Текущая неделя - . \n \n Расписание на текущую неделю:")


@bot.message_handler(commands=['следующая'])
def start_message(message):
    bot.send_message(message.chat.id, "Следующая неделя - " + "\n \n Расписание на следующую неделю:")


@bot.message_handler(commands=['погода'])
def prognoz(message):
    pogoda = weather()
    bot.send_message(message.chat.id, f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                                      f"Погодные условия: {pogoda['weather'][0]['description']}\nТемпература:{pogoda['main']['temp']}C°"
                                      f"Максимальная температура:{pogoda['main']['temp_max']}C°\nМинимальная температура:{pogoda['main']['temp_min']}C°\nСкорость ветра:{pogoda['wind']['speed']}м/с\nВлажность:{pogoda['main']['humidity']}%\n"
                                      f"Видимость:{str(pogoda['visisbility'])}м")


@bot.message_handler(commands=['погодананеделю'])
def prognozweek(message):
    pogodaweek = weatherweek()
    perv_day = None
    for pogoda in pogodaweek["list"]:
        day = pogoda['dt_txt'].split()[0]
        if perv_day != None and day == perv_day:
            continue
        bot.send_message(message.chat.id, f"Дата:{pogoda['dt_txt']}\n"
                                          f"Погодные условия: {pogoda['weather'][0]['description']}\nТемпература:{pogoda['main']['temp']}C°\nМаксимальная температура:{pogoda['main']['temp_max']}C°\n"
                                          f"Минимальная температура:{pogoda['main']['temp_min']}C°\nСкорость ветра:{pogoda['wind']['speed']}м/с\nВлажность:{pogoda['main']['humidity']}%")
        perv_day = day


# текстовые команды
@bot.message_handler(content_types=['text'])
def answer(message):
    if message.text.lower() == "понедельник" or message.text.lower() == "расписание на понедельник":
        bot.send_message(message.chat.id, "Расписание на Понедельник: \n \n<Предмет><Кабинет><Время><Преподаватель>")
    elif message.text.lower() == "вторник" or message.text.lower() == "расписание на вторник":
        bot.send_message(message.chat.id, "Расписание на Вторник: \n \n<Предмет><Кабинет><Время><Преподаватель>")
    elif message.text.lower() == "среда" or message.text.lower() == "расписание на среду":
        bot.send_message(message.chat.id, "Расписание на Среду: \n \n<Предмет><Кабинет><Время><Преподаватель>")
    elif message.text.lower() == "четверг" or message.text.lower() == "расписание на четверг":
        bot.send_message(message.chat.id, "Расписание на Четверг: \n \n<Предмет><Кабинет><Время><Преподаватель>")
    elif message.text.lower() == "пятница" or message.text.lower() == "расписание на Пятницу":
        bot.send_message(message.chat.id, "Расписание на Пятницу: \n \n<Предмет><Кабинет><Время><Преподаватель>")
    elif message.text.lower() == "суббота" or message.text.lower() == "расписание на субботу":
        bot.send_message(message.chat.id, "Расписание на Субботу: \n \n<Предмет><Кабинет><Время><Преподаватель>")
    elif message.text.lower() == "неделя" or message.text.lower() == "какая неделя" or message.text.lower() == "какая сейчас неделя":
        bot.send_message(message.chat.id, "Сейчас " + "- " + "неделя.")
    elif message.text.lower() == "расписание на текущую неделю" or message.text.lower() == "текущая неделя" or message.text.lower() == "текущая":
        bot.send_message(message.chat.id, "Текущая неделя - . \n \n Расписание на текущую неделю:")
    elif message.text.lower() == "расписание на следующую неделю" or message.text.lower() == "следующая неделя" or message.text.lower() == "следующая":
        bot.send_message(message.chat.id, "Следующая неделя - . \n \n Расписание на следующую неделю:")
    elif message.text.lower() == "сайт мтуси" or message.text.lower() == "какой сайт мтуси" or message.text.lower() == "сайт":
        bot.send_message(message.chat.id, "Сайт МТУСИ - https://mtuci.ru/")
    else:
        bot.send_message(message.chat.id, "Извините, я Вас не понял")


bot.polling(none_stop=True, interval=0)
