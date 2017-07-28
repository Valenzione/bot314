from itertools import cycle

import pytz, datetime

from pymongo import MongoClient

db = MongoClient().bot314


def get_queues():
    return db.queues.find()


def get_queue(name):
    return db.queues.find_one({"name": name})


def change_status(chat_id, status):
    print(db.users.find_one_and_update({"chat_id": chat_id}, {"$set": {"active": status}}))
    update_queues()


def update_queues():
    users = list(db.users.find())
    db.queues.update_many({}, {"$set": {"participants": users}})


def store_user(user_data):
    update_queues()
    db.users.insert(user_data)


def generate_log(queue):
    local = pytz.timezone("Europe/Moscow")
    time = datetime.datetime.utcnow()
    tzoffset = local.utcoffset(time)
    local.localize(time)
    time = time + tzoffset
    log_dict = {"event": queue["name"], "user": queue["next"], "date": time}
    print(log_dict)
    return log_dict


def complete_task(queue):
    db.log.insert(generate_log(queue))
    participants = cycle(queue["participants"])
    user_found = False
    for user in participants:
        if user_found and user["active"] == True:
            db.queues.find_one_and_update({"name": queue["name"]}, {"$set": {"next": user["chat_id"]}})
            break
        if user['chat_id'] == queue['next']:
            user_found = True


def get_recent_logs():
    return list(db.log.find({},limit=5))