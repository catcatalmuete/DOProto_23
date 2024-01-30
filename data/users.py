"""
This module interfaces to our user data.
"""
import data.db_connect as dbc
import data.add_product as add_prod

USERNAME = "username"
USER_ID = "user_id"
PASSWORD = "password"
SHOPPING_CART = "shopping_cart" # meant to be a list, but will be saved as a string with commas
SAVED = "saved" # meant to be a list, but will be saved as a string with commas
MIN_USER_NAME_LEN = 6
MIN_PASSWORD_LEN = 8
USERS_COLLECT = "users"


def get_users() -> dict:
    dbc.connect_db()
    return dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT)

def create_user(username : str, user_id : str, password : str, shopping_cart : str, saved : str):
    dbc.connect_db()
    found_user = dbc.fetch_one(USERS_COLLECT,{USERNAME: username})
    if found_user:
        raise ValueError(f'Duplicate username: {username=}')
    new_user = {}
    new_user[USERNAME] = username
    new_user[USER_ID] = user_id
    new_user[PASSWORD] = password
    new_user[SHOPPING_CART] = shopping_cart
    new_user[SAVED] = saved
    _id = dbc.insert_one(USERS_COLLECT, new_user)
    return _id is not None

def delete_user(username: str):
    dbc.connect_db()
    return dbc.del_one(USERS_COLLECT, {USERNAME: username})

def get_shopping_cart(username: str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        shopping_cart = user.get(SHOPPING_CART, "")
        return shopping_cart
 
def add_shopping_cart(username: str, prod_name : str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        shopping_cart = user.get(SHOPPING_CART, "")
        shopping_cart_list = shopping_cart.split(',') if shopping_cart else []
        shopping_cart_list.append(prod_name)
        updated_shopping_cart = ','.join(map(str, shopping_cart_list))
        return dbc.update_one(USERS_COLLECT, {USERNAME: username}, {"$set": {SHOPPING_CART: updated_shopping_cart}})
       

def delete_shopping_cart(username: str, del_prod : str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        shopping_cart = user.get(SHOPPING_CART, "")
        shopping_cart_list = shopping_cart.split(',') if shopping_cart else []
        try:
            shopping_cart_list.remove(del_prod)
        except ValueError:
            pass
        
        updated_shopping_cart = ','.join(map(str, shopping_cart_list))
        return dbc.update_one(USERS_COLLECT, {USERNAME: username}, {"$set": {SHOPPING_CART: updated_shopping_cart}})

def calc_checkout_price():
    dbc.connect_db()
    return dbc.fetch_all_as_dict(SHOPPING_CART, "users")
    total_price = 0
    for product in SHOPPING_CART:
        total_price += product.price
    return total_price  # calculate total price of all products in user shopping cart

def get_saved(username: str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        saved = user.get(SAVED, "")
        return saved
    
def add_saved(username: str, prod_name : str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        saved = user.get(SAVED, "")
        saved_list = saved.split(',') if saved else []
        saved_list.append(prod_name)
        updated_saved = ','.join(map(str, saved_list))
        return dbc.update_one(USERS_COLLECT, {USERNAME: username}, {"$set": {SAVED: updated_saved}})
       
def delete_saved(username : str, del_prod : str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        saved = user.get(SAVED, "")
        saved_list = saved.split(',') if saved else []
        try:
            saved_list.remove(del_prod)
        except ValueError:
            pass
        
        updated_saved = ','.join(map(str, saved_list))
        return dbc.update_one(USERS_COLLECT, {USERNAME: username}, {"$set": {SAVED: updated_saved}})


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
