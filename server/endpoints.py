"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""

from flask import request, Flask
from flask_restx import Resource, Api
import data.users as usr
import data.add_product as prods
import data.get_product as get_prod

app = Flask(__name__)
api = Api(app)

USERS = 'users'
ADD_PRODUCT = 'add_product'
GET_PRODUCT = "get_product"
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
        data = request.get_json()
        new_user = usr.create_user(
            data['username'], 
            data['user_id'], 
            data['password'], 
            data['shopping_cart']
            )
        
        if new_user:
            return {'message': 'User added successfully'}, 201
        else:
            return {'message': 'Failed to add user'}, 409
    
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
        data = request.get_json()
        
		# validation of product before adding
        if 'user_id' not in data or 'name' not in data or 'price' not in data \
            or 'condition' not in data or 'brand' not in data \
                    or 'categories' not in data or 'date_posted' not in data \
                        or 'comments' not in data:
            return {'message': 'All fields required for adding product'}

        # add the product
        new_product = prods.add_product(
            data['user_id'],
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
            

    
    