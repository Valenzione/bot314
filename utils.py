import random
from itertools import groupby, dropwhile

import telebot
import database
from telebot import types

import config
from itertools import cycle

bot = telebot.TeleBot(config.token)


def generate_markup(data):
    global answer_list, callback_list
    if data == "init":
        answer_list = ["Я сделал", "Я хочу", "Расписание и История"]
        callback_list = ["done", "tobe", "tt"]
    if data == "done":
        answer_list = ["Я вынес мусор", "Я принес воду", "Назад"]
        callback_list = ["trash_done", "water_done", "back"]
    if data == "tobe":
        answer_list = ["Я хочу чтобы вынесли мусор", "Я хочу чтобы принесли воду", "Назад"]
        callback_list = ["trash", "water", "back"]

    keyboard = types.InlineKeyboardMarkup()
    for i in range(len(answer_list)):
        b = types.InlineKeyboardButton(text=answer_list[i], callback_data=callback_list[i])
        keyboard.add(b)

    return keyboard


def send_message(recevier_id, message):
    bot.send_message(chat_id=recevier_id, text=message)


# Return table of users in markdown
def get_oreder_table():
    users = database.get_active_users()
    basic_text = "**Порядок:**\n"
    for x in range(len(users)):
        basic_text += str(x + 1) + ". "
        basic_text += users[x]["name"]
        basic_text += "\n"
    water_next = "Следующий приносит воду *" + get_next_user(database.get_water_user())['name'] + "*"
    trash_next = "Следующий выкидывает мусор *" + get_next_user(database.get_trash_user())['name'] + "*"
    return "*" + basic_text + "*\n" + trash_next + "\n" + water_next


def get_water_history():
    water_logs = database.get_water_logs()
    users = database.get_users()
    out = "*История поставок воды:*\n"
    for log in water_logs:
        out += '*' + users[int(log['user_id'])] + '* ' + log['date'] + '\n'
    return out


def get_trash_history():
    trash_logs = database.get_trash_logs()
    users = database.get_users()
    out = "*История выноса мусора*:\n"
    for log in trash_logs:
        out += '*' + users[int(log['user_id'])] + '* ' + log['date'] + '\n'
    return out


# Get next user by iterating circular list
def get_next_user(last_user):
    users = cycle(database.get_active_users())
    skipped = dropwhile(lambda x: x['user_id'] != last_user['user_id'], users)
    next(skipped)  # Skip current user
    return next(skipped)
