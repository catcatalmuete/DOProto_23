"""
This module interfaces to our user data.
"""
import data.db_connect as dbc
USERNAME = "username"
PASSWORD = "password"
MIN_USER_NAME_LEN = 6
MIN_PASSWORD_LEN = 8
USERS_COLLECT = "users"
SHOPPING_CART = "shopping_cart"


def get_users():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT)

def create_user():
    dbc.connect_db()
    return dbc.insert_one(USERS_COLLECT)

def delete_user():
    dbc.connect_db()
    return dbc.del_one(USERS_COLLECT)

# Add shopping cart field to allow users to add items to their shopping cart
def get_shopping_cart():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SHOPPING_CART, USERS_COLLECT)

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
