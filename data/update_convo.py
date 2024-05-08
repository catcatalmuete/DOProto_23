from datetime import datetime
from data import users
import data.db_connect as dbc

MESSAGES_COLLECT = "Messages"
USER_ID_1 = "userid1"
USER_ID_2 = "userid2"
MESSAGES = "messages"
TIME_UPDATED = "updated"


def update_convo(user1: str, user2: str, message: str):
    dbc.connect_db()
    user1id = dbc.fetch_one(users, {'username': user1})['_id']
    current_utc_time = datetime.utcnow()
    dbc.update_one((MESSAGES_COLLECT,
                    {"$push": {MESSAGES:
                               [user1id, message, current_utc_time]}}))
    dbc.close_db()
    return True
