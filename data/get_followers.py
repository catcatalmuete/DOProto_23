import data.db_connect as dbc

FOLLOWERS_COLLECT = "followers"
USERNAME = "username"

def get_followers():
	dbc.connect_db()
	return dbc.fetch_all_as_dict(USERNAME, FOLLOWERS_COLLECT)


