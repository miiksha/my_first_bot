from time import time, sleep
import telebot
import datetime
import random
from random import choice
import config
import sqlite3
import requests
import json
from threading import *
from PIL import Image, ImageFilter
from translate import Translator
from loguru import logger

bot = telebot.TeleBot(config.token)
logger.add("info.log", format="{time} {level} {message}", level="INFO")
logger.add("error.log", format="{time} {level} {message}", level="ERROR")

def main():
    fun_command.today("start")
    DataBase.create_table()



class command:
    @bot.message_handler(commands=['start', 'help'])
    def send_welcome(message):
        bot.reply_to(message, "Вы используете телеграм Бота, от создателя 'Михаил' \n https://vk.com/vk_com1999.")
        bot.send_message(message.from_user.id, "Команды:\nпривет\nСамая глупая порода собаки?\nlaba\nсекрет"
                                               "\nид\nшар1\nшар2\nсегодня\nпереводчик\nпереводчик2(3 или "
                                               "4)\nкот\nфото\nкартинка\nспам")
        bot.send_message(message.from_user.id, "держите миленького котика")
        fun_command.send_cat(message)
        bot.send_message(config.root,
                         f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
        bot.send_message(config.root, "зарегался/проверил команды")
        DataBase.insert_start(message)


    @bot.message_handler(func=lambda m: True)
    def echo_all(message):
        if 'привет' in message.text.lower():
            bot.reply_to(message, "Привет, я на море")
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал привет")


        elif message.text.lower() == "спам" and message.from_user.id == config.root:
            bot.send_message(config.root, "кому спамить будем?")
            user_data = DataBase.read("SELECT * FROM users")
            people = 0
            for row in user_data:
                bot.send_message(config.root, f"{row[0]} {row[1]}")
                people += 1
            bot.register_next_step_handler(message, fun_command.spam_threading)
            # bot.register_next_step_handler(message, DataBase.read("SELECT user_id FROM users WHERE user_id = '{message.text}'"))


        elif message.text.lower() == "фото":
            fun_command.photo(message)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал фото")


        elif message.text.lower() == "кот":
            fun_command.send_cat(message)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал 'кот'")


        elif message.text.lower() == "картинка":
            fun_command.image_random(message)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал картинка")


        elif message.text.lower() == "сегодня":
            fun_command.today(message)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал сегодня")


        elif message.text.lower() == "переводчик":
            bot.send_message(message.from_user.id, "введи текст для перевода на русский язык")
            bot.register_next_step_handler(message, fun_command.trans)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал переводчик")


        elif message.text.lower() == "переводчик2":
            bot.send_message(message.from_user.id, "введи текст для перевода на английский язык")
            bot.register_next_step_handler(message, fun_command.trans2)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал переводчик2")


        elif message.text.lower() == "переводчик3":
            bot.send_message(message.from_user.id, "введи текст для перевода на английский язык")
            bot.register_next_step_handler(message, fun_command.trans3)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал переводчик3")


        elif message.text.lower() == "переводчик4":
            bot.send_message(message.from_user.id, "введи текст для перевода на русский язык")
            bot.register_next_step_handler(message, fun_command.trans4)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал переводчик4")

        elif message.text.lower() == "спам":
            bot.send_message(message.from_user.id, "вам это недоступно")

        elif message.text.lower() == "шар1":
            fun_command.fun_yes_no(message)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал шар1")

        elif message.text.lower() == "шар2":
            fun_command.fun2_yes_no(message)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал шар2")

        elif message.text.lower() == "крах":
            bot.send_message(message.from_user.id, "крах")
            test_num = 1 / 0

        elif message.text == "Самая глупая порода собаки?":
            bot.send_message(message.from_user.id, "Анастасия Курилло")
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал 'Самая глупая порода собаки'")

        elif "laba" in message.text:
            bot.send_message(message.from_user.id, "Лабораторная работа(калькулятор). Введи первое число")
            bot.register_next_step_handler(message, fun_command.data)
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал 'laba'")

        elif message.text.lower() == "секрет" and (message.from_user.id == config.root
                                                   or message.from_user.id == 1261758771):
            fun_command.time_together(message)
            fun_command.send_cat(message)
            bot.send_message(config.root, "root использовал(а) 'секрет'")


        elif message.text.lower() == "секрет" and message.from_user.id == 93966951:
            bot.send_message(message.from_user.id, "Привет БОСС")
            bot.send_message(config.root, "Денис использовала 'секрет'")

        elif message.text.lower() == "секрет":
            bot.send_message(message.from_user.id, "у вас недостаточно полномочий")
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал 'секрет'")

        elif message.text.lower() == "ид":
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал 'ид'")
            bot.send_message(message.from_user.id, f"{message.from_user.first_name} - это твоё имя при регистрации")
            bot.send_message(message.from_user.id, f"{message.from_user.id} - это твой айди в телеграме")


        else:
            bot.reply_to(message, "такой команды еще нет\n Разрабочик:\n https://vk.com/vk_com1999")
            bot.send_message(message.from_user.id,
                             "Команды:\nпривет\nСамая глупая порода собаки?\nlaba\nсекрет"
                             "\nид\nшар1\nшар2\nсегодня\nпереводчик\nпереводчик2(3 или 4)\nкот\nфото\nкартинка\nспам")
            bot.send_message(config.root,
                             f"{message.from_user.id}  {message.from_user.first_name} @{message.from_user.username}")
            bot.send_message(config.root, "использовал 'неизвестную команду'")


class fun_command:


    def send_cat(message):
        response = requests.get(url="https://thiscatdoesnotexist.com/")
        bot.send_photo(message.from_user.id, response.content)


    def spam_threading(message):
            thread1 = Thread(target=fun_command.spam_threading1, args=(message.text,))
            thread1.start()


    def spam_threading1(id_prey):
        for i in range(11):
            bot.send_message(id_prey, "это спам от Миши")
            sleep(5)


    def photo(message):

        try:
            bot.send_message(message.from_user.id, f"держи фото")
            original = Image.open("test.jpg")
            bot.send_message(message.from_user.id, f"{original.format}, {original.size}, {original.mode}")
            bot.send_photo(message.from_user.id, open('test.jpg', 'rb'))
            # original.show()
        except FileNotFoundError:
            bot.send_message(message.from_user.id, f"фото не найдено")
        except:
            bot.send_message(message.from_user.id, f"неудача")
            bot.send_message(config.root, f"неудача")
        fun_command.image_random(message)

    def image_random(message):
        response = requests.get(url="https://picsum.photos/1920/1080")
        # with open("img.jpg", "wb") as somefile:
        #     somefile.write(response.content)
        # bot.send_photo(message.from_user.id, open('img.jpg', 'rb'))
        bot.send_message(message.from_user.id, "вот ещё рандомная картинка с интернета")
        bot.send_photo(message.from_user.id, response.content)

    def trans(message):
        text = message.text
        url_trans = requests.get(
            url=f'https://fasttranslator.herokuapp.com/api/v1/text/to/text?source={text}&lang=en-ru')
        bot.send_message(config.root, url_trans)
        try:
            json_dict_raw = json.loads(url_trans.text)
            json_dict = json_dict_raw["data"]
            bot.send_message(message.from_user.id, f"перевод:  {json_dict} ")
        except:
            bot.send_message(message.from_user.id, f"временно не работает(ищу api который будет работать в сша) ")

    def trans2(message):
        text = message.text
        url_trans = requests.get(
            url=f'https://fasttranslator.herokuapp.com/api/v1/text/to/text?source={text}&lang=ru-en')
        bot.send_message(config.root, url_trans)
        try:
            json_dict_raw = json.loads(url_trans.text)
            json_dict = json_dict_raw["data"]
            bot.send_message(message.from_user.id, f"перевод:  {json_dict} ")
        except:
            bot.send_message(message.from_user.id, f"временно не работает(ищу api который будет работать в сша) ")

    def trans3(message):
        text = message.text
        try:
            trans = Translator(from_lang="ru", to_lang="en")
            end_text = trans.translate(text)
            bot.send_message(message.from_user.id, f"перевод:  {end_text} ")
            bot.send_message(config.root, f"перевод:  {end_text} ")
        except:
            bot.send_message(message.from_user.id, f"временно не работает ")

    def trans4(message):
        text = message.text
        try:
            trans = Translator(from_lang="en", to_lang="ru")
            end_text = trans.translate(text)
            bot.send_message(message.from_user.id, f"перевод:  {end_text} ")
            bot.send_message(config.root, f"перевод:  {end_text} ")
        except:
            bot.send_message(message.from_user.id, f"временно не работает ")

    def today(message):
        today = datetime.datetime.today()
        if message == "start":
            bot.send_message(config.root, f"Бот стартовал сегодня {today} ")
            logger.info(f"Бот стартовал сегодня {today} ")
        else:
            bot.send_message(message.from_user.id, f"на данный момент {today} ")

    def time_together(message):
        todayy = datetime.datetime.today()
        # todayy = datetime.datetime(2021,12,15) #10 дней с 15 по 25
        # 6.01.2022 последний раз расставлись ❤❤❤
        # todayy = datetime.datetime(2022,1,5)
        then = datetime.datetime(2018, 7, 5)
        delta = todayy - then
        bot.send_message(message.from_user.id, f" {delta.days} дней уже вместе ❤❤❤")
        response = requests.get('https://complimentr.com/api')
        json_dict = json.loads(response.text)
        bot.send_message(message.from_user.id, json_dict["compliment"])
        trans = Translator(from_lang="en", to_lang="ru")
        end_text = trans.translate(json_dict["compliment"])
        bot.send_message(message.from_user.id, end_text)

    def fun_yes_no(message):
        yes_no = ["да", "нет"]
        rand = random.randint(0, 1)
        bot.send_message(message.from_user.id, yes_no[rand])

    def fun2_yes_no(message):
        answer = choice(
            ['да', 'нет', 'не знаю', 'больше да чем нет', 'вероятно да', 'скорее всего да', 'вряд ли', 'не стоит',
             'забудь',
             'полная хрень', 'может быть нет', 'может быть да', 'стоит подождать', 'не спеши', 'подбрось монетку',
             'используй шар1'])
        bot.send_message(message.from_user.id, answer)

    def data(message):
        global num1
        global bash
        bash = 0
        try:
            num1 = int(message.text)
        except:
            bot.send_message(message.from_user.id, "ERROR: ТЫ ввёл не число")
            bash = 1
        if bash == 0:
            bot.send_message(message.from_user.id, "Введите второе число")
            bot.register_next_step_handler(message, fun_command.data2)
        else:
            bot.send_message(config.root, "ошибка первого числа")
            bot.send_message(config.root, f"у пользователя {message.from_user.first_name}")

    def data2(message):
        global num2
        global bash
        bash = 0
        try:
            num2 = int(message.text)
        except:
            bot.send_message(message.from_user.id, "ERROR: ТЫ ввёл не число")
            bash = 1
        if bash == 0:
            bot.send_message(message.from_user.id, "Введи любое действие из списка: \n  +  \n  -  \n  *  \n  /  ")
            bot.register_next_step_handler(message, fun_command.data3)
        else:
            bot.send_message(config.root, "ошибка второго числа")
            bot.send_message(config.root, f"у пользователя {message.from_user.first_name}")

    def data3(message):
        global action
        action = message.text
        if action == "+":
            result = num1 + num2
            bot.send_message(message.from_user.id, "Вычисления завершены. Ответ: " + str(result))
        elif action == "-":
            result = num1 - num2
            bot.send_message(message.from_user.id, "Вычисления завершены. Ответ: " + str(result))
        elif action == "*":
            result = num1 * num2
            bot.send_message(message.from_user.id, "Вычисления завершены. Ответ: " + str(result))
        elif action == "/":
            if num2 == 0:
                bot.send_message(message.from_user.id, "не надо делить на 0")
            else:
                result = num1 / num2
                bot.send_message(message.from_user.id, f"Вычисления завершены. Ответ: {str(result)}")
        else:
            bot.send_message(message.from_user.id, "Ошибка, такой команды нет!!!")
            bot.send_message(config.root, "ошибка действия калькулятора")
            bot.send_message(config.root, f"у пользователя {message.from_user.first_name}")


class DataBase:
    @staticmethod
    def create_table():
        connect = sqlite3.connect(config.database_name)
        sql = connect.cursor()
        sql.execute("""CREATE TABLE IF NOT EXISTS users (
            user_id INT,
            first_name TEXT,
            login TEXT,
            password TEXT
        )""")
        connect.commit()
        connect.close()

    @staticmethod
    def read(select):
        conn = sqlite3.connect(config.database_name)
        sql = conn.cursor()
        sql.execute(select)
        result = sql.fetchall()
        sql.close()
        conn.close()
        return result

    @staticmethod
    def insert_start(message):
        conn = sqlite3.connect(config.database_name)
        sql = conn.cursor()
        user_data = DataBase.read(f"SELECT user_id FROM users WHERE user_id = '{message.from_user.id}'")
        if not user_data:
            sql.execute("INSERT INTO users VALUES (?, ?, ?, ?)",
                        (message.from_user.id, message.from_user.first_name, None, None))
        conn.commit()
        sql.close()
        conn.close()


if __name__ == '__main__':
    try:
        main()
        bot.polling()
    except Exception as err:
        unknown_bug = f'Неизвестная ошибка - {err}'
        logger.opt(exception=True).error(unknown_bug)

