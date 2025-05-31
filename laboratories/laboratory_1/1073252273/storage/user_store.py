
from models.user import User

user_db = {}

def add_user(name, preferred_channel, available_channels):
    user = User(name, preferred_channel, available_channels)
    user_db[name] = user
    return user

def get_user(name):
    return user_db.get(name)

def list_users():
    return list(user_db.values())
