<<<<<<< HEAD
import os
import sys

current_dir = os.path.dirname(os.path.abspath(__file__))
parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

import data.db_connect as dbc

FOLLOWERS_COLLECT = "followers"
USER_ID = "username"
FOLLOWERS = 'following'


def add_followers(user, follower):
	data.dbc.connect_db()

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
=======
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
	
>>>>>>> 188c666b1016cb52492c7feb015f099203c70057
