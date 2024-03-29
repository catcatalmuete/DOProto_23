import data.db_connect as dbc

FOLLOWERS_COLLECT = "followers"
USERNAME = "username"
FOLLOWERS = 'following'


def new_add_followers(user, followers):
	dbc.connect_db()

	# check if follower is duplicate
	found_user = dbc.fetch_one(FOLLOWERS_COLLECT,  {USERNAME: user})
	if found_user:
		raise ValueError(f'User not found: {user=}')
	
	# Insert new follower into database
	new_follower = {
		USERNAME: user,
		FOLLOWERS: followers
		}
	
	_id = dbc.insert_one(FOLLOWERS_COLLECT, new_follower)
	return _id is not None
	


def add_followers(user, followers):
	dbc.connect_db()

	# check if follower is duplicate
	found_user = dbc.fetch_one(FOLLOWERS_COLLECT,  {USERNAME: user})
	if found_user:
		raise ValueError(f'User not found: {user=}')
	
	# Insert new follower into database
	new_follower = {
		USERNAME: user,
		FOLLOWERS: followers
		}
	
	_id = dbc.insert_one(FOLLOWERS_COLLECT, new_follower)
	return _id is not None
	
