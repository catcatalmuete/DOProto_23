import data.db_connect as dbc
import data.users as users
import data.get_followers as gf
from datetime import datetime

MESSAGES_COLLECT = "Messages"
USER_ID_1 = "userid1"
USER_ID_2 = "userid2"
MESSAGES = "messages"
TIME_UPDATED = "updated"

# get 2 usernames as strings
def add_convo(user1 : str, user2 : str):
    dbc.connect_db()

    user1id = dbc.fetch_one(users, {'username': user1})['_id']
    user2id = dbc.fetch_one(users, {'username': user2})['_id']

    # confirm user1 follows user2 before allowing convo to be started
    if user1 not in gf.get_followers(user2):
        raise ValueError("User 1 does not follow user 2")

    # check if convo already exists
    convo_exists = dbc.fetch_one(MESSAGES_COLLECT, {USER_ID_1: user1id, USER_ID_2: user2id})
    
    if convo_exists:
        dbc.close_db()
        return False
    
    else:
        current_utc_time = datetime.utcnow()
        dbc.insert_one(MESSAGES_COLLECT, {USER_ID_1: user1, USER_ID_2: user2, MESSAGES: [], TIME_UPDATED: current_utc_time})
        dbc.close_db()
        return True