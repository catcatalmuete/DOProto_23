from datetime import datetime

import data.db_connect as dbc
import data.users as users
import data.get_followers as gf

MESSAGES_COLLECT = "Messages"
USER_ID_1 = "userid1"
USER_ID_2 = "userid2"
MESSAGES = "messages"
TIME_UPDATED = "updated"

# get 2 usernames as strings
def delete_convo(user1 : str, user2 : str):
    dbc.connect_db()

    user1id = dbc.fetch_one(users, {'username': user1})['_id']
    user2id = dbc.fetch_one(users, {'username': user2})['_id']

    # check if convo exists
    convo_exists = dbc.fetch_one(MESSAGES_COLLECT, {USER_ID_1: user1id, USER_ID_2: user2id})
    
    if convo_exists:
        dbc.delete_one(MESSAGES_COLLECT, {USER_ID_1: user1id, USER_ID_2: user2id})
        dbc.close_db()
        return True
    else:
        dbc.close_db()
        return False
