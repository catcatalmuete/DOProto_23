import data.db_connect as dbc

FOLLOWERS_COLLECT = "followers"
USER_ID = "username"
FOLLOWERS = 'following'


def add_followers(user, follower):
	dbc.connect_db()

	# check if follower is duplicate
	check = dbc.fetch_one({USER_ID: follower}, FOLLOWERS_COLLECT)
	if check:
		return False
	
	# Insert new follower into database
	new_follower = {
		USER_ID: user,
		FOLLOWERS: follower
		}
	dbc.insert_one(new_follower, FOLLOWERS_COLLECT)
	return True