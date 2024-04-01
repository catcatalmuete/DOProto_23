import data.db_connect as dbc
import users as users

MESSAGES_COLLECT = "Messages"
USER_ID_1 = "userid1"
USER_ID_2 = "userid2"
MESSAGES = "messages"
TIME_UPDATED = "updated"

def get_convo(user1 : str, user2 : str):
    dbc.connect_db()
    user1id = dbc.fetch_one(users, {'username': user1})['_id']
    user2id = dbc.fetch_one(users, {'username': user2})['_id']
    convo = dbc.fetch_one(MESSAGES_COLLECT, {"$or": [{USER_ID_1: user1id, USER_ID_2: user2id}, {USER_ID_1: user2id, USER_ID_2: user1id}]})
    dbc.close_db()
    return convo