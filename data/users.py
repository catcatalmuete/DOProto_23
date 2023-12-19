"""
This module interfaces to our user data.
"""
import data.db_connect as dbc
USERNAME = "username"
USER_ID = "user_id"
PASSWORD = "password"
SHOPPING_CART = []
SAVED = []
MIN_USER_NAME_LEN = 6
MIN_PASSWORD_LEN = 8
USERS_COLLECT = "users"
SHOPPING_CART = ["shopping_cart"] # list of products in user shopping cart
SAVED = ["saved"] # list of products saved by user


def get_users():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT)

def create_user(username, user_id, password, shopping_cart, saved):
    dbc.connect_db()
    found_user = dbc.fetch_one({USERNAME: username}, USERS_COLLECT)
    if found_user:
        return False
    
	# Insert new user into the database
    new_user = {
		USERNAME: username,
        USER_ID: user_id,
        PASSWORD: password,
        SHOPPING_CART: shopping_cart,
        SAVED: saved
	}
    return dbc.insert_one(new_user, USERS_COLLECT)

def delete_user(user_filter, user_collection):
    dbc.connect_db()
    return dbc.del_one(user_filter, user_collection)

def get_shopping_cart():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SHOPPING_CART, USERS_COLLECT) # return all products in user shopping cart

def add_shopping_cart():
    dbc.connect_db()
    return dbc.insert_one(SHOPPING_CART, USERS_COLLECT) # add a product to user shopping cart 

def delete_shopping_cart():
    dbc.connect_db()
    return dbc.del_one(SHOPPING_CART, USERS_COLLECT) # delete a product from user shopping cart

def calc_checkout_price():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SHOPPING_CART, USERS_COLLECT)
    total_price = 0
    for product in SHOPPING_CART:
        total_price += product.price
    return total_price  # calculate total price of all products in user shopping cart

def get_saved():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SAVED, USERS_COLLECT) # return all products in user saved list

def add_saved():
    dbc.connect_db()
    return dbc.insert_one(SAVED, USERS_COLLECT) # Saved a product to user saved list

def delete_saved():
    dbc.connect_db()
    return dbc.del_one(SAVED, USERS_COLLECT) # delete a product from user saved list


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
