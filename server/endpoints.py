"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import request, Flask
from flask_restx import Resource, Api
import data.users as usr
import data.add_product as prods

app = Flask(__name__)
api = Api(app)

USERS = 'users'
ADD_PRODUCT = 'add_product'
UPDATE_PRODUCT = 'update_product'
SHOPPING_CART = 'shopping_cart'


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
        return {'Title': MAIN_MENU_NM,
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
        return usr.create_user()
    
    def delete(self):
        """
        This method deletes a user.
        """
        return usr.delete_user()
    
    
# for product listing
@api.route(f'/{ADD_PRODUCT}')
class AddProduct(Resource):
    """
    This class supports users adding their own product on app
    """
    def post(self):
        data = request.get_json()
        
		# validation of product before adding
        if 'name' not in data or 'price' not in data \
            or 'condition' not in data or 'brand' not in data \
                    or 'categories' not in data or 'date_posted' not in data \
                        or 'comments' not in data:
            return {'message': 'All fields required for adding product'}

        # add the product
        new_product = prods.add_product(
            data['name'], 
            data['price'],
            data['condition'],
            data['brand'],
            data['categories'],
            data['date_posted'],
            data['comments'],
            )
        
        if new_product:
            return {'message': 'Product added successfully'}, 201
        else:
            return {'message': 'Failed to add product'}, 409
        

# Updating product information
@api.route(f'/{UPDATE_PRODUCT}')
class UpdateProduct(Resource):
    """
    This class supports users updating their product information
    """
    def put(self):
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
        
        if updated_product:
            return {'message': 'Product updated successfully'}, 201
        else:
            return {'message': 'Failed to update product'}, 409
        
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

