from telebot import types

import db

def init_queues():
    keyboard = types.InlineKeyboardMarkup()
    for x in db.get_queues():
        keyboard.add(types.InlineKeyboardButton(text=x['descr'], callback_data="queue_" + x['name']))
    return keyboard

def status_change():
    keyboard = types.InlineKeyboardMarkup()
    keyboard.add(types.InlineKeyboardButton(text="On", callback_data="status_active"))
    keyboard.add(types.InlineKeyboardButton(text="Off", callback_data="status_inactive"))
    return keyboard

def init_queue(chat_id, queue):
    keyboard = types.InlineKeyboardMarkup()
    if chat_id==queue["next"]:
        keyboard.add(types.InlineKeyboardButton(text="Сделано", callback_data="done_" + queue['name']))
    keyboard.add(types.InlineKeyboardButton(text="Напомнить", callback_data="notify_" + queue['name']))
    return keyboard