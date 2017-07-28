import telebot
import cherrypy
import config
import db
import keyboard
import logging

bot = telebot.TeleBot(config.token)
logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)  # Outputs debug messages to console.


class WebhookServer(object):
    @cherrypy.expose
    def index(self):
        if 'content-length' in cherrypy.request.headers and \
                        'content-type' in cherrypy.request.headers and \
                        cherrypy.request.headers['content-type'] == 'application/json':
            length = int(cherrypy.request.headers['content-length'])
            json_string = cherrypy.request.body.read(length).decode("utf-8")
            update = telebot.types.Update.de_json(json_string)
            # Эта функция обеспечивает проверку входящего сообщения
            bot.process_new_updates([update])
            return ''
        else:
            raise cherrypy.HTTPError(403)


@bot.message_handler(commands=['register'])
def echo_register(message):
    user_data = {"chat_id": message.chat.id, "name": message.chat.last_name + " " + message.chat.first_name,
                 "username": message.chat.username,
                 "active": True}
    db.store_user(user_data)
    bot.send_message(message.chat.id, str(user_data))

@bot.message_handler(commands=['logs'])
def echo_logs(message):
    text = "Recent logs: \n"
    for event in db.get_recent_logs():
        user_chat_id = event["user"]
        type = event['event']
        date = event["date"]
        text+="*"+str(user_chat_id)+" "+str(type)+" "+str(date)+"\n"

    bot.send_message(message.chat.id,text)


@bot.message_handler(commands=['change_status'])
def echo_register(message):
    bot.send_message(message.chat.id, "Вы сменили статус", reply_markup=keyboard.status_change())


@bot.message_handler(func=lambda message: True, content_types=['text'])
def echo_message(message):
    bot.send_message(message.chat.id, text="Выбери очередь", reply_markup=keyboard.init_queues())


@bot.callback_query_handler(func=lambda call: parse_call(call)[0] == "status")
def status_callback(call):
    status = True if parse_call(call)[-1] == "active" else False
    db.change_status(call.message.chat.id, status)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="Status changed")


def generate_queue_text(queue):
    text = queue["descr"] + "\n\n"
    participants = ""
    for user in queue["participants"]:
        if user["active"]:
            prefix = "*" if user["chat_id"] == queue["next"]else ""
            participants += prefix + user["name"] + prefix + "\n"
    return text + participants


@bot.callback_query_handler(func=lambda call: parse_call(call)[0] == "queue")
def queue_callback(call):
    queue_name = parse_call(call)[-1]
    queue = db.get_queue(name=queue_name)
    text = generate_queue_text(queue)

    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text=text, reply_markup=keyboard.init_queue(call.message.chat.id, queue),
                          parse_mode="Markdown")


@bot.callback_query_handler(func=lambda call: parse_call(call)[0] == "done")
def done_callback(call):
    queue = db.get_queue(parse_call(call)[-1])
    db.complete_task(queue)
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Спасибо!")


@bot.callback_query_handler(func=lambda call: parse_call(call)[0] == "notify")
def notify_callback(call):
    queue = db.get_queue(parse_call(call)[-1])
    bot.send_message(chat_id=queue['next'], text=queue['notify_text'])
    bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id,
                          text="Напоминание отправлено")


def parse_call(call):
    """
    Parse arguments divided by underscore
    :param call:
    :return: Return list with arguments of callback
    """
    return str(call.data).split("_")


if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=config.WEBHOOK_URL_BASE + config.WEBHOOK_URL_PATH,
                    certificate=open(config.WEBHOOK_SSL_CERT, 'r'))

    cherrypy.config.update({
        'server.socket_host': config.WEBHOOK_LISTEN,
        'server.socket_port': config.WEBHOOK_PORT,
        'server.ssl_module': 'builtin',
        'server.ssl_certificate': config.WEBHOOK_SSL_CERT,
        'server.ssl_private_key': config.WEBHOOK_SSL_PRIV
    })

    cherrypy.quickstart(WebhookServer(), config.WEBHOOK_URL_PATH, {'/': {}})
