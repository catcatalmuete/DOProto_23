import data.db_connect as dbc

FOLLOWERS_COLLECT = "followers"
USER_ID = "username"
FOLLOWERS = 'following'


def del_follower(user, follower):
    dbc.connect_db()

    # Check if follower exists
    existing_follower = dbc.fetch_one(({USER_ID: user, FOLLOWERS: follower},
                                       FOLLOWERS_COLLECT))
    if existing_follower:
        # Delete follower from database
        dbc.delete_one({USER_ID: user, FOLLOWERS: follower}, FOLLOWERS_COLLECT)
        return True
    else:
        raise Exception("Follower does not exist.")
