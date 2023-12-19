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


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT)

def create_user(username : str, user_id : str, password : str):
    dbc.connect_db()
    found_user = dbc.fetch_one(USERS_COLLECT,{USERNAME: username},)
    if found_user:
        raise ValueError(f'Duplicate username: {username=}')
    new_user = {}
    new_user[USERNAME] = username
    new_user[USER_ID] = user_id
    new_user[PASSWORD] = password
    _id = dbc.insert_one(USERS_COLLECT, new_user)
    return _id is not None

    
	# def create_user(username : str, user_id : str, password : str, shopping_cart : list, saved : list):
    
	# # Insert new user into the database
    # new_user = {
	# 	USERNAME: username,
    #     USER_ID: user_id,
    #     PASSWORD: password,
    #     SHOPPING_CART: shopping_cart,
    #     SAVED: saved
	# }
    # return dbc.insert_one(new_user, "users")

def delete_user(username: str):
    dbc.connect_db()
    return dbc.del_one(USERS_COLLECT, {USERNAME: username})

def get_shopping_cart():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SHOPPING_CART, "users") # return all products in user shopping cart

def add_shopping_cart():
    dbc.connect_db()
    return dbc.insert_one(SHOPPING_CART, "users") # add a product to user shopping cart 

def delete_shopping_cart():
    dbc.connect_db()
    return dbc.del_one(SHOPPING_CART, "users") # delete a product from user shopping cart

def calc_checkout_price():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SHOPPING_CART, "users")
    total_price = 0
    for product in SHOPPING_CART:
        total_price += product.price
    return total_price  # calculate total price of all products in user shopping cart

def get_saved():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SAVED, "users") # return all products in user saved list

def add_saved():
    dbc.connect_db()
    return dbc.insert_one(SAVED, "users") # Saved a product to user saved list

def delete_saved():
    dbc.connect_db()
    return dbc.del_one(SAVED, "users") # delete a product from user saved list


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
