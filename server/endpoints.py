"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import request, Flask, jsonify
from flask_restx import Resource, Api
import data.users as usr
import data.add_product as prods
import data.get_product as get_prod
import data.add_followers as add_follower
import data.get_followers as get_follower

# import requests
# import json

url = "http://127.0.0.1:8000//add_product"  # Replace with your actual API endpoint

headers = {"Content-Type": "application/json"}


app = Flask(__name__)
api = Api(app)

USERS = 'users'
ADD_PRODUCT = 'add_product'
UPDATE_PRODUCT = 'update_product'
SHOPPING_CART = 'shopping_cart'
SAVED = 'saved'
GET_PRODUCT = "get_product"
FOLLOWERS = 'followers'
ADD_FOLLOWERS = 'add_followers'
GET_FOLLOWERS = 'get_followers'
MAIN_MENU = ""

@api.route('/hello')
class HelloWorld(Resource):
    """
    The purpose of the HelloWorld class is to have a simple test to see if the
    app is working at all.
    """
    def get(self):
        """
        A trivial endpoint to see if the server is running.
        It just answers with "hello world."
        """
        return {'hello': 'world'}


@api.route('/endpoints')
class Endpoints(Resource):
    """
    This class will serve as live, fetchable documentation of what endpoints
    are available in the system.
    """
    def get(self):
        """
        The `get()` method will return a list of available endpoints.
        """
        endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
        return {"Available endpoints": endpoints}


@api.route(f'/{MAIN_MENU}')
@api.route('/')
class MainMenu(Resource):
    """
    This will deliver our main menu.
    """
    def get(self):
        """
        Gets the main game menu.
        """
        return {'Title': MAIN_MENU,
                'Default': 2,
                'Choices': {
                    '1': {'url': '/', 'method': 'get',
                          'text': 'List Available Characters'},
                    '2': {'url': '/',
                          'method': 'get', 'text': 'List Active Games'},
                    '3': {'url': f'/{USERS}',
                          'method': 'get', 'text': 'List Users'},
                    'X': {'text': 'Exit'},
                }}


@api.route(f'/{USERS}')
class Users(Resource):
    """
    This class supports fetching all users.
    """
    def get(self):
        """
        This method returns all users.
        """
        return usr.get_users(), 201
    
    def post(self):
        """
        This method creates a new user.
        """
        data = request.get_json()
        username = data.get('username')
        user_id = data.get('user_id')
        password = data.get('password')
        shopping_cart = data.get('shopping_cart', [])
        saved = data.get('saved', [])

        new_user = usr.create_user(
            username, user_id, password, shopping_cart, saved
            )
        
        if new_user:
            return jsonify({'message': 'User added successfully'}), 201
        else:
            return jsonify({'message': 'Failed to add user'}), 409
    
    def delete(self):
        """
        This method deletes a user.
        """
        data = request.get_json()
        if 'username' not in data or 'user_id' not in data:
            return {'message': 'Username and user_id required for deleting a user'}, 400
        filter = {'username': data['username'], 'user_id': data['user_id']}
        deleted_user = usr.delete_user(filter, usr.USERS_COLLECT)
        
        if deleted_user:
            return {'message': 'User deleted successfully'}, 200
        else:
            return {'message': 'Failed to delete user'}, 404


@api.route(f'/{GET_PRODUCT}')
class GetProduct(Resource):
    """
    This class supports fetching all products.
    """
    def get(self):
        """
        This method returns all products.
        """
        return get_prod.get_product(), 201

        
    
    
# for product listing
@api.route(f'/{ADD_PRODUCT}')
class AddProduct(Resource):
    """
    This class supports users adding their own product on app
    """
    def post(self):
         """
        This method adds a product
        """
         print("Working")
         data = request.get_json()
		# validation of product before adding
         if 'user_id' not in data or 'name' not in data or 'price' not in data \
            or 'condition' not in data or 'brand' not in data \
                    or 'categories' not in data or 'date_posted' not in data \
                        or 'comments' not in data:
            return {'message': 'All fields required for adding product'}
        # print("Received data:", data) 
        # new_product = prods.add_products(
        #     data['user_id'],
        #     data['name'], 
        #     data['price'],
        #     data['condition'],
        #     data['brand'],
        #     data['categories'],
        #     data['date_posted'],
        #     data['comments'],
		# )
        # print("New product:", new_product)
         return prods.add_products(
            data['user_id'],
            data['name'], 
            data['price'],
            data['condition'],
            data['brand'],
            data['categories'],
            data['date_posted'],
            data['comments'],
		)
        
        # if new_product:
        #     return {'message': 'Product added successfully'}, 201
        # else:
        #     return {'message': 'Failed to add product'}, 409
        

# Updating product information
@api.route(f'/{UPDATE_PRODUCT}')
class UpdateProduct(Resource):
    """
    This class supports users updating their product information
    """
    def put(self):
         """
        This method updates a product.
        """
         data = request.get_json()
        
        # validation of product before updating
         if 'name' not in data or 'price' not in data \
            or 'condition' not in data or 'brand' not in data \
                    or 'categories' not in data or 'date_posted' not in data \
                        or 'comments' not in data:
            return {'message': 'All fields required for updating product'}

        # update the product
         updated_product = prods.update_product(
            data['name'], 
            data['price'],
            data['condition'],
            data['brand'],
            data['categories'],
            data['date_posted'],
            data['comments'],
            )  
         return updated_product
        
# Use get_shopping_cart() from users.py to show all products in user shopping cart
@api.route(f'/{SHOPPING_CART}')
class ShoppingCart(Resource):
    """
    This class supports fetching user's shopping cart.
    """
    def get(self):
        """
        This method returns all products shopping cart.
        """
        return usr.get_shopping_cart(), 201

    def post(self):
        """
        This method adds a product to user shopping cart.
        """
        return usr.add_shopping_cart()
    
    def delete(self):
        """
        This method deletes a product from user shopping cart.
        """
        return usr.delete_shopping_cart()
    
    def calc_checkout_price(self):
        """
        This method calculates total price of all products in user shopping cart.
        """
        return usr.calc_checkout_price()

@api.route(f'/{FOLLOWERS}')
class Followers(Resource):
    """
    This class supports fetching user's followers.
    """
    def get(self):
        """
        This method returns all followers.
        """
        return get_follower.get_followers(), 201

# Use get_shopping_cart() from users.py to show all products in user shopping cart
@api.route(f'/{SAVED}')
class Saved(Resource):
    """
    This class supports fetching user's shopping cart.
    """
    def get(self):
        """
        This method returns all products shopping cart.
        """
        return usr.get_saved(), 201

    def add(self):
        """
        This method adds a product to user shopping cart.
        """
        return usr.add_saved()
    
    def delete(self):
        """
        This method deletes a product from user shopping cart.
        """
        return usr.delete_saved()
    