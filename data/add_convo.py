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
dbc.connect_db()
user1 = dbc.fetch_one(users, {'_id': USER_ID_1})['username']
user2 = dbc.fetch_one(users, {'_id': USER_ID_2})['username']

# confirm user1 follows user2 before allowing conv oto be started
if user1 not in gf.get_followers(user2):
    raise ValueError("User 1 does not follow user 2")
else:
    current_utc_time = datetime.utcnow()
    dbc.insert_one(MESSAGES_COLLECT, {USER_ID_1: user1, USER_ID_2: user2, MESSAGES: [], TIME_UPDATED: current_utc_time})
    
