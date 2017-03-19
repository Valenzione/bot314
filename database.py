from datetime import datetime

from pymongo import MongoClient

import config

client = MongoClient(config.db_uri)
db = client.heroku_76pgrdhp


# Store record of bringing the water by this user_id
def log_water(user_id):
    db.water.insert_one({
        "user_id": user_id,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


# Return last user who brought the water
def get_water_user():
    document = db.water.find_one(sort=[("date", -1)])
    return document


# Store record of taking the trash out by this user_id
def log_trash(user_id):
    db.trash.insert_one({
        "user_id": user_id,
        "date": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    })


# Return last user who threw trash out
def get_trash_user():
    document = db.trash.find_one(sort=[("date", -1)])
    return document


# Return list of active users
def get_active_users():
    cursor = db.users.find({"active": True})
    return list(cursor)
