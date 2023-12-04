import data.db_connect as dbc

FOLLOWERS_COLLECT = "followers"
USER_ID = "username"

def get_product():
	dbc.connect_db()
	return dbc.fetch_all_as_dict(USER_ID, FOLLOWERS_COLLECT)

