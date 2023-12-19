import data.db_connect as dbc

FOLLOWERS_COLLECT = "followers"
USER_ID = "username"

def get_followers():
	dbc.connect_db()
	
	try:
		if USER_ID not in dbc.get_collection_names():
			raise ValueError("Username not found in followers collection")
		
		return dbc.fetch_all_as_dict(USER_ID, FOLLOWERS_COLLECT)
	except Exception as e:
		print(f"Error: {e}")


