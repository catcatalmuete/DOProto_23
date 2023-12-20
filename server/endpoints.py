"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

from flask import request, Flask
from flask_restx import Resource, Api, fields
import werkzeug.exceptions as wz
import data.users as usr
import data.add_product as prods
import data.get_product as get_prod
import data.add_followers as add_follower
import data.get_followers as get_follower


app = Flask(__name__)
api = Api(app)

USERS = 'users'
DELETE = 'delete'
DEL_USER = f'{USERS}/{DELETE}'
ADD_PRODUCT = 'add_product'
UPDATE_PRODUCT = 'update_product'
SHOPPING_CART = 'shopping_cart'
SAVED = 'saved'
GET_PRODUCT = "get_product"
FOLLOWERS = 'followers'
ADD_FOLLOWERS = 'add_followers'
GET_FOLLOWERS = 'get_followers'
MAIN_MENU = ""
USER_ID = "User ID"
PRODUCT_ID = "Product ID"

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

user_fields = api.model('NewUser', {
    usr.USERNAME: fields.String,
    usr.USER_ID: fields.String,
    usr.PASSWORD: fields.String,
    usr.SHOPPING_CART: fields.String,
    usr.SAVED: fields.String
})

@api.route(f'/{DEL_USER}/<username>')
class DelUser(Resource):
    """
    Deletes a user by username.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, username):
        """
        Deletes a user by username.
        """
        try:
            usr.delete_user(username)
            return {username: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        

@api.route(f'/{USERS}')
class Users(Resource):
    """
    This class supports fetching all users.
    """
    def get(self):
        """
        This method returns all users.
        """
        print("this is user data: ", usr.get_users())
        return usr.get_users()
    
    @api.expect(user_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        Add a new user.
        """
        # if request.headers['Content-Type'] != 'application/json':
        #     return jsonify({'error': 'needs to be application/json'}), 415
        
        username = request.json[usr.USERNAME]
        user_id = request.json[usr.USER_ID]
        password = request.json[usr.PASSWORD]
        shopping_cart = request.json[usr.SHOPPING_CART]
        saved = request.json[usr.SAVED]
        try:
            new_user = usr.create_user(username, user_id, password, shopping_cart, saved)
            if new_user is None:
                raise wz.ServiceUnavailable('There is a technical issue.')
            return {USER_ID: new_user}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


product_fields = api.model('NewProduct', {
    prods.USER_ID: fields.String,
    prods.PRODUCT_NAME: fields.String,
    prods.PRODUCT_PRICE: fields.Float,
    prods.PRODUCT_CONDITION: fields.String,
    prods.PRODUCT_BRAND: fields.String,
    prods.PRODUCT_CATEGORIES: fields.String,
    prods.PRODUCT_DATE_POSTED: fields.String,
    prods.PRODUCT_COMMENTS: fields.String,
})
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
    @api.expect(product_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        This method adds a product
        """
        user_id = request.json[prods.USER_ID]
        name = request.json[prods.PRODUCT_NAME]
        price = request.json[prods.PRODUCT_PRICE]
        condition = request.json[prods.PRODUCT_CONDITION]
        brand = request.json[prods.PRODUCT_BRAND]
        categories = request.json[prods.PRODUCT_CATEGORIES]
        date_posted = request.json[prods.PRODUCT_DATE_POSTED]
        comments = request.json[prods.PRODUCT_COMMENTS]
        
        try:
            new_product = prods.add_product(user_id, name, price, condition, brand, categories, date_posted, comments)
            if new_product is None:
                raise wz.ServiceUnavailable('There is a technical issue.')
            return {PRODUCT_ID: new_product}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')
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
@api.route(f'/{SHOPPING_CART}/<username>')
class ShoppingCart(Resource):
    """
    This class supports fetching user's shopping cart.
    """
    def get(self, username):
        """
        This method returns all products shopping cart.
        """
        try:
            return usr.get_shopping_cart(username)
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    def post(self, username):
        """
        This method adds a product to user shopping cart.
        """
        new_prod_name = "new prod"
        return usr.add_shopping_cart(username, new_prod_name)
    
    def delete(self, username):
        """
        This method deletes a product from user shopping cart.
        """
        return usr.delete_shopping_cart()
    
    # def calc_checkout_price(self):
    #     """
    #     This method calculates total price of all products in user shopping cart.
    #     """
    #     return usr.calc_checkout_price()

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
@api.route(f'/{SAVED}/<username>')
class Saved(Resource):
    """
    This class supports fetching user's shopping cart.
    """
    def get(self, username):
        """
        This method returns all products shopping cart.
        """
        try:
            return usr.get_saved(username)
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
        
    def post(self, username):
        """
        This method adds a product to user saved list.
        """
        new_prod_name = "new prod"
        return usr.add_saved(username, new_prod_name)

    
    def delete(self, username):
        """
        This method deletes a product from user shopping cart.
        """
        return usr.delete_saved()
    