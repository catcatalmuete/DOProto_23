"""
This module interfaces to our user data.
"""
import data.db_connect as dbc
import data.add_product as add_prod
from bson import ObjectId
from werkzeug.security import check_password_hash

USERNAME = "username"
EMAIL = "email"
PASSWORD = "password"
FIRST_NAME = "first_name"
LAST_NAME = "last_name"
SHOPPING_CART = "shopping_cart" 
SAVED = "saved"
FOLLOWERS = "followers"
FOLLOWING = "following"
RES_HALL = "res_hall"
ADDRESS = "address"
PRONOUNS = "pronouns"
MIN_USER_NAME_LEN = 6
MIN_PASSWORD_LEN = 8
USERS_COLLECT = "users"


def get_users() -> dict:
    dbc.connect_db()
    users = dbc.fetch_all_as_dict(USERNAME, USERS_COLLECT)
    for user in users.values():
        user[SHOPPING_CART] = [str(item) for item in user.get(SHOPPING_CART, []) if isinstance(item, ObjectId)]
        user[SAVED] = [str(item) for item in user.get(SAVED, []) if isinstance(item, ObjectId)]
        user[FOLLOWERS] = [str(item) for item in user.get(FOLLOWERS, []) if isinstance(item, ObjectId)]
    return users
    

def create_user(first_name: str, 
                last_name: str, 
                username : str, 
                email : str, 
                password : str, 
                res_hall : str, 
                address : str, 
                pronouns : str):
    dbc.connect_db()
    found_user = dbc.fetch_one(USERS_COLLECT,{USERNAME: username})
    if found_user:
        raise ValueError(f'Duplicate username: {username=}')
    new_user = {}
    new_user[FIRST_NAME] = first_name
    new_user[LAST_NAME] = last_name
    new_user[USERNAME] = username
    new_user[EMAIL] = email
    new_user[PASSWORD] = password
    new_user[SHOPPING_CART] = []
    new_user[SAVED] = []
    new_user[FOLLOWERS] = []
    new_user[FOLLOWING] = []
    new_user[RES_HALL] = res_hall
    new_user[ADDRESS] = address
    new_user[PRONOUNS] = pronouns
    
    _id = dbc.insert_one(USERS_COLLECT, new_user)
    return _id is not None

def delete_user(username: str):
    dbc.connect_db()
    return dbc.del_one(USERS_COLLECT, {USERNAME: username})

def get_user(username: str):
    dbc.connect_db()
    return dbc.fetch_one(USERS_COLLECT, {USERNAME: username})

def login_auth(username: str, password: str):
    dbc.connect_db()
    found_user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if found_user and check_password_hash(found_user['password'], password):
            return {'message': 'User login successful'}, 201
    else:
        raise ValueError(f"User {username} not found")

def update_user(username: str, data: dict):
    dbc.connect_db()
    found_user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if found_user:
        update_data = {}
        for key, val in data.items():
            if key in [FIRST_NAME , LAST_NAME, EMAIL, RES_HALL, ADDRESS, PRONOUNS]:
                update_data[key] = val
        result = dbc.update_one(USERS_COLLECT, {USERNAME: username}, {"$set" : update_data})
        return result.modified_count > 0
    else:
        raise ValueError(f"User {username} not found")


def get_shopping_cart(username: str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        shopping_cart_ids = user.get(SHOPPING_CART, [])
        shopping_cart_products = []
        for product_id in shopping_cart_ids:
            product = dbc.fetch_one("products", {"_id": product_id})
            if product:
                 shopping_cart_products.append(product)
            else:
                 return None
        return shopping_cart_products
    else:
        raise ValueError(f"User {username} not found")

 
def add_shopping_cart(username: str, prod_id : str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        shopping_cart = user.get(SHOPPING_CART, [])
        if isinstance(prod_id, str):
            prod_id = ObjectId(prod_id)
        shopping_cart.append(prod_id)
        result = dbc.update_one(USERS_COLLECT, {USERNAME: username}, {"$set": {SHOPPING_CART: shopping_cart}})
        if result:
            return {"message": "Product added to shopping cart successfully"}, 201
        else:
            return {"message" : "Failed to add product to shopping cart."}, 409
        
    else:
        raise ValueError(f"User '{username}' not found")
       

def delete_shopping_cart(username: str, prod_id : str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        shopping_cart = user.get(SHOPPING_CART, [])
        if isinstance(prod_id, str):
            prod_id = ObjectId(prod_id)
        shopping_cart.remove(prod_id)
        result = dbc.update_one(USERS_COLLECT, {USERNAME: username}, {"$set": {SHOPPING_CART: shopping_cart}})
        if result:
            return {"message": "Product removed from shopping cart successfully"}, 201
        else:
            return {"message" : "Failed to remove product from shopping cart."}, 409
        
        

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
        saved_ids = user.get(SHOPPING_CART, [])
        saved_products = []
        for product_id in saved_ids:
            product = dbc.fetch_one("products", {"_id": product_id})
            if product:
                 saved_products.append(product)
            else:
                 return {"message": f"Product with ID {product_id} not found."}
        return saved_products
    else:
        raise ValueError(f"User {username} not found")
    
def add_saved(username: str, prod_id : str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        saved = user.get(SAVED, [])
        if isinstance(prod_id, str):
            prod_id = ObjectId(prod_id)
        saved.append(prod_id)
        result = dbc.update_one(USERS_COLLECT, {USERNAME: username}, {"$set": {SAVED: saved}})
        if result:
            return {"message": "Product added to saved successfully"}, 201
        else:
            return {"message" : "Failed to add product to saved."}, 409
        
    else:
        raise ValueError(f"User '{username}' not found")
       
def delete_saved(username : str, prod_id : str):
    dbc.connect_db()
    user = dbc.fetch_one(USERS_COLLECT, {USERNAME: username})
    if user:
        saved = user.get(SAVED, [])
        if isinstance(prod_id, str):
            prod_id = ObjectId(prod_id)
        saved.remove(prod_id)
        result = dbc.update_one(USERS_COLLECT, {USERNAME: username}, {"$set": {SAVED : saved}})
        if result:
            return {"message": "Product removed from saved successfully"}, 201
        else:
            return {"message" : "Failed to remove product from saved."}, 409
        