import telebot

import config
import utils
import database

bot = telebot.TeleBot(config.token)


# Обычный режим
@bot.message_handler(commands=['start'])
def start(message):
    keyboard = utils.generate_markup("init")
    bot.send_message(message.chat.id, "Бот дающий указания", reply_markup=keyboard)


@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    if call.message:
        if call.data == "done":
            keyboard = utils.generate_markup(call.data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Что ты сделал?", reply_markup=keyboard)
        if call.data == "tobe":
            keyboard = utils.generate_markup(call.data)
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Что ты хочешь?",
                                  reply_markup=keyboard)
        if call.data == "water":
            water_user = utils.get_next_user(database.get_water_user())
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Воду выносит " + water_user['name'] + " aka " + water_user['alias'])
            utils.send_message(water_user['chat_id'], "Принеси воду")

        if call.data == "trash":
            trash_user = utils.get_next_user(database.get_trash_user())
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Воду выносит " + trash_user['name'] + " aka " + trash_user['alias'])
            utils.send_message(trash_user['chat_id'], "Вынеси мусор")

        if call.data == "water_done":
            water_user = utils.get_next_user(database.get_water_user())
            database.log_water(water_user['user_id'])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Молодец")

        if call.data == "trash_done":
            trash_user = utils.get_next_user(database.get_trash_user())
            database.log_trash(trash_user['user_id'])
            bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                                  text="Молодец")

        if call.data == "back" or call.data == "back1":
            keyboard = utils.generate_markup("init")
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, text="Бот устанавливающий порядок",
                                  reply_markup=keyboard)
        if call.data == "tt":
            bot.edit_message_text(chat_id=call.message.chat.id,
                                  message_id=call.message.message_id, text=utils.get_oreder_table(),
                                  parse_mode="Markdown")


if __name__ == '__main__':
    print("Bot polling started!")
    bot.polling(none_stop=True)
