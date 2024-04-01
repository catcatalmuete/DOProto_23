"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

import os
import sys

from flask import Flask
from flask_cors import CORS

current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

from flask import request, Flask
from flask_restx import Resource, Api, fields
import werkzeug.exceptions as wz
import data.db_connect as dbc
import data.users as usr
import data.add_product as prods
import data.get_product as get_prod
import data.delete_product as del_prod
import data.add_followers as add_follower
import data.get_followers as get_follower

app = Flask(__name__)
api = Api(app)
CORS(app)

USERS = 'users'
DELETE = 'delete'
DEL_USER = f'{USERS}/{DELETE}'
ADD_PRODUCT = 'add_product'
DELETE_PRODUCT = 'delete_product'
UPDATE_PRODUCT = 'update_product'
SHOPPING_CART = 'shopping_cart'
ADD_SHOPPING_CART = 'add_shopping_cart'
DELETE_SHOPPING_CART = 'delete_shopping_cart'
SAVED = 'saved'
DELETE_SAVED = 'delete_saved'
GET_PRODUCT = "get_product"
FOLLOWERS = 'followers'
ADD_FOLLOWERS = 'add_followers'
GET_FOLLOWERS = 'get_followers'
MAIN_MENU = ""
USER_ID = "User ID"
PRODUCT_ID = "Product ID"
FOLLOW_ID = "Follower ID"

# @api.route('/endpoints')
# class Endpoints(Resource):
#     """
#     This class will serve as live, fetchable documentation of what endpoints
#     are available in the system.
#     """
#     def get(self):
#         """
#         The `get()` method will return a list of available endpoints.
#         """
#         endpoints = sorted(rule.rule for rule in api.app.url_map.iter_rules())
#         return {"Available endpoints": endpoints}

user_fields = api.model('NewUser', {
    usr.FIRST_NAME: fields.String,
	usr.LAST_NAME: fields.String,
	usr.USERNAME: fields.String,
    usr.EMAIL: fields.String,
    usr.PASSWORD: fields.String,
    usr.SHOPPING_CART: fields.List(fields.String),
    usr.SAVED: fields.List(fields.String),
    usr.FOLLOWERS: fields.List(fields.String),
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
        return usr.get_users(), 201
    
    @api.expect(user_fields)
    def post(self):
        """
        This method creates a new user.
        """
       
        data = request.get_json()
        try:
            new_user = usr.create_user(
				data['first_name'],
				data['last_name'],
				data['username'],
				data['email'],
				data['password']
			)
            if new_user:
                 return {'message': 'User added successfully'}, 201
            else:
                 raise wz.BadRequest(f"User not acceptable: {data['username']}")
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')
        
        
            


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
    This class supports users adding their own product on the app
    """
    @api.expect(product_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
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

shopping_fields = api.model('NewProductForShoppingCart', {
    get_prod.PRODUCT_ID: fields.String,
   
})
        
@api.route(f'/{ADD_SHOPPING_CART}/<username>')
class AddToShoppingCart(Resource):
    """
    This class supports adding to a user's shopping cart
    """
    @api.expect(shopping_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self, username):
        """
        This method adds a product to user shopping cart.
        """
        data = request.get_json()
       
        if '_id' not in data:
            raise wz.BadRequest(f"_id required for adding to shopping cart")
        
        try:
            result = usr.add_shopping_cart(username, data['_id'])
            if result:
                return {"message": "Product added to shopping cart successfully"}, 201
            else:
                return {"message": "Failed to add product to shopping cart"}, 409
        except ValueError as e:
            raise wz.NotFound(str(e))

@api.route(f'/{SHOPPING_CART}/<username>')
class ShoppingCart(Resource):
    
	def get(self, username):
		""" This method returns the products in a user's shopping cart"""
        
		return usr.get_shopping_cart(username);        

	@api.expect(shopping_fields)
	@api.response(HTTPStatus.OK, 'Success')
	@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
	def delete(self, username):
		"""
        This method deletes a product from user shopping cart.
        """
		data = request.get_json()
        
		if '_id' not in data:
			raise wz.BadRequest(f'_id required to remove from shopping cart')
          
		try:
			result = usr.delete_shopping_cart(username, data['_id'])
			if result:
				return {"message": "Product removed from shopping cart successfully."}, 201
			else:
				return {"message": "Failed to remove product from shopping cart."}, 409
		except ValueError as e:
			raise wz.NotFound(str(e))
          
        
        
#     def calc_checkout_price(self, username):
#         """
#         Deletes a product by from the shopping cart of a iser by product name.
#         """
#         new_prod_name = "new prod"
#         try:
#             usr.delete_shopping_cart(username, new_prod_name)
#             return { new_prod_name: 'Deleted'}
#         except ValueError as e:
#             raise wz.NotFound(f'{str(e)}')
        
follow_fields = api.model('NewFollower', {
    add_follower.USERNAME: fields.String,
    add_follower.FOLLOWERS: fields.String,
})

@api.route(f'/{FOLLOWERS}')
class GetFollowers(Resource):
    """
    This class supports fetching user's followers.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def get(self):
        """
        This method returns all followers.
        """
        return get_follower.get_followers(), 201
        
# for adding followers
@api.route(f'/{ADD_FOLLOWERS}')
class AddFollowers(Resource):
    """
    This class supports adding new followers for a user 
    """
    @api.expect(follow_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        This method adds new followers for a user 
        """
        username = request.json[add_follower.USERNAME]
        followers = request.json[add_follower.FOLLOWERS]
        
        try:
            new_following = add_follower.add_followers(username, followers)
            if new_following is None:
                raise wz.ServiceUnavailable('There is a technical issue.')
            return {FOLLOW_ID: new_following}
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')


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


@api.route(f'/{DELETE_SAVED}/<user_name>')
class DeleteSaved(Resource):
    
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def delete(self, user_name):
        """
        Deletes a product by from the saved list of a iser by product name.
        """
        new_prod_name = "new prod"
        try:
            usr.delete_saved(user_name, new_prod_name)
            return { new_prod_name: 'Deleted'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')
    

    @api.route('/messages/<user1>/<user2>') #change formatting, this is just inital template
    class Messages(Resource):
        def get(self, user1, user2):
            # fetch the messages between user1 and user2 from your database
            # messages = db.Messages.find({"$or": [{"user1": user1, "user2": user2}, {"user1": user2, "user2": user1}]})
            # return messages
            pass

        # @api.expect(message_fields)
        def post(self, user1, user2):
            # Here you would typically add a new message to your database
            # For example:
            # db.Messages.insert(api.payload)
            # return {"message": "Message added successfully"}, HTTPStatus.CREATED
            pass


