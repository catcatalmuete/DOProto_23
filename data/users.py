"""
This module interfaces to our user data.
"""
import data.db_connect as dbc
USERNAME = "username"
USER_ID = "user_id"
PASSWORD = "password"
SHOPPING_CART = []
MIN_USER_NAME_LEN = 6
MIN_PASSWORD_LEN = 8
USERS_COLLECT = "users"


def get_users():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT)

def create_user(username, user_id, password, shopping_cart):
    dbc.connect_db()
    found_user = dbc.fetch_one({USERNAME: username}, USERS_COLLECT)
    if found_user:
        return False
    
	# Insert new user into the database
    new_user = {
		USERNAME: username,
        USER_ID: user_id,
        PASSWORD: password,
        SHOPPING_CART: shopping_cart
	}
    return dbc.insert_one(new_user, USERS_COLLECT)

def delete_user(user_filter, user_collection):
    dbc.connect_db()
    return dbc.del_one(user_filter, user_collection)

# def old_get_users():
#     users = {
        
# 		"user_one": {
#             USERNAME: "test_username_1", 
#             PASSWORD: "12345"   
# 		},
        
#         "user_two": {
#             USERNAME: "test_username_2", 
#             PASSWORD: "12345"      
# 		},
#         "user_three": {
#             USERNAME: "test_username_3", 
#             PASSWORD: "12345"   
# 		},
        
# 	}
    
	
#     return users
