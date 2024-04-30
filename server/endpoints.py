"""
This is the file containing all of the endpoints for our flask app.
The endpoint called `endpoints` will return all available endpoints.
"""
from http import HTTPStatus

import os
import sys

from flask import Flask
from flask_cors import CORS
from flask import request, Flask
from flask_restx import Resource, Api, fields
from werkzeug.security import generate_password_hash
import werkzeug.exceptions as wz
import data.db_connect as dbc
import data.product_form as prod_form
import data.users as usr
import data.add_product as prods
import data.get_product as get_prod
import data.delete_product as del_prod
import data.add_followers as add_follower
import data.get_followers as get_follower
import data.get_convo as get_convo
import data.add_convo as add_convo
import data.update_convo as update_convo
import data.delete_convo as delete_convo


current_dir = os.path.dirname(os.path.abspath(__file__))

parent_dir = os.path.join(current_dir, '..')
sys.path.append(parent_dir)

app = Flask(__name__)
api = Api(app)
CORS(app)

USERS = 'users'
DELETE = 'delete'
DEL_USER = f'{USERS}/{DELETE}'
PRODUCT = 'product'
ADD_PRODUCT = 'add_product'
DELETE_PRODUCT = 'delete_product'
UPDATE_PRODUCT = 'update_product'
SHOPPING_CART = 'shopping_cart'
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
    usr.FOLLOWING: fields.List(fields.String),
    usr.RES_HALL: fields.String, 
    usr.ADDRESS: fields.String,
    usr.PRONOUNS: fields.String,
})

user_login_fields = api.model('LoginUser', {
	usr.USERNAME: fields.String,
    usr.PASSWORD: fields.String,
})

@api.route(f'/{DEL_USER}/<username>')
class DelUser(Resource):
    """
    {DELETE USER} Deletes a user by username.
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
        

@api.route(f'/{USERS}/<username>')
class GetUser(Resource):
    """
    {GET USER} Return a user by username.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, username):
        """
        Deletes a user by username.
        """
        try:
            return  usr.get_user(username)
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')	
    @api.expect(user_fields)
    def put(self, username):
        """
        {UPDATE USER PROFILE} This method updates an existing user's profile.
        """
        data = request.get_json()
        existing_user = usr.get_user(username)
        if existing_user:
            updated_user = usr.update_user(username, data)
            if updated_user:
                return {'message' : 'User profile updated successfully'}, 200
            else:
                raise wz.InternalServerError('Failed to update user info')
        else:
             raise wz.NotFound('User not found')
    
			

                   
              
	
        

@api.route(f'/{USERS}')
class Users(Resource):
    """
    This class supports fetching all users.
    """
         
    def get(self):
        """
        {RETRIEVE ALL USERS} This method returns all users. (FOR DEVELOPER USE)
        """
        return usr.get_users(), 201
    
    @api.expect(user_fields)
    def post(self):
        """
        {CREATE NEW USER} This method creates a new user.
        """
        data = request.get_json()
        password_hash = generate_password_hash(data['password'], method='scrypt')
        try:
            new_user = usr.create_user(
				data['first_name'],
				data['last_name'],
				data['username'],
				data['email'],
				password_hash
			)
            if new_user:
                 return {'message': 'User added successfully'}, 201
            else:
                 raise wz.BadRequest(f"User not acceptable: {data['username']}")
        except ValueError as e:
            raise wz.BadRequest(f'{str(e)}')
            
	
    
        
@api.route(f'/{USERS}/login')
class UserLogin(Resource):
    """
    This class supports authentication for user login.
    """
    @api.expect(user_login_fields)
    def post(self):
        data = request.get_json()
        try:
            result = usr.login_auth(data['username'], data['password'])
            if result:
                return {'message' : 'User logged in successfully'}, 201
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
@api.route(f'/{PRODUCT}')
class Product(Resource):
    """
    This class supports creating, retrieving, and deleting products.
    """
    @api.expect(product_fields)
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
    def post(self):
        """
        {CREATE A NEW PRODUCT} This method creates a new product.
        """
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
        
    def get(self):
        """
        {RETRIEVE ALL PRODUCTS} This method returns all products.
        """
        return get_prod.get_products(), 201
        
@api.route(f'/{PRODUCT}/<product_id>')
class GetProduct(Resource):
    """
    {GET USER} Return a product by product ID.
    """
    @api.response(HTTPStatus.OK, 'Success')
    @api.response(HTTPStatus.NOT_FOUND, 'Not Found')
    def get(self, product_id):
        """
        Deletes a user by username.
        """
        try:
            return get_prod.get_product(product_id)
            #return {'message' : f'Found user with username: {username}.'}
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')	

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

@api.route(f'/get_product_form')
class ProductForm(Resource):
     def get(self):
          return prod_form.get_product_form()

@api.route(f'/{SHOPPING_CART}/<username>')
class ShoppingCart(Resource):
     
	"""
    This class supports a user's shopping cart
    """
    
	def get(self, username):
		""" 
        {RETRIEVE SHOPPING CART} This method returns the products in a user's shopping cart
        """
        
		return usr.get_shopping_cart(username);    

	@api.expect(shopping_fields)
	@api.response(HTTPStatus.OK, 'Success')
	@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
	def post(self, username):
		"""
        {ADD TO SHOPPING CART} This method adds a product to user shopping cart.
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
        
          
saved_fields = api.model('NewProductForSavedList', {
    get_prod.PRODUCT_ID: fields.String,
   
})
          
@api.route(f'/{SAVED}/<username>')
class SavedProducts(Resource):
     
	"""
    This class supports a user's saved/ favorited products
    """
    
	def get(self, username):
		""" 
        {RETRIEVE SAVED PRODUCTS} This method returns the products in a user's saved list
        """
        
		return usr.get_saved(username);    

	@api.expect(saved_fields)  
	@api.response(HTTPStatus.OK, 'Success')
	@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')	
	def post(self, username):
		"""
        {ADD TO SAVED LIST} This method adds a product to user saved list.
        """
		data = request.get_json()
       
		if '_id' not in data:
			raise wz.BadRequest(f"_id required for adding to saved list")
		try:
			result = usr.add_saved(username, data['_id'])
			if result:
				return {"message": "Product added to saved list successfully"}, 201
			else:
				return {"message": "Failed to add product to saved list"}, 409
		except ValueError as e:
			raise wz.NotFound(str(e))    

	@api.expect(saved_fields)  
	@api.response(HTTPStatus.OK, 'Success')
	@api.response(HTTPStatus.NOT_ACCEPTABLE, 'Not Acceptable')
	def delete(self, username):
		"""
        This method deletes a product from user saved list.
        """
		data = request.get_json()
        
		if '_id' not in data:
			raise wz.BadRequest(f'_id required to remove from saved list')
          
		try:
			result = usr.delete_saved(username, data['_id'])
			if result:
				return {"message": "Product removed from saved list successfully."}, 201
			else:
				return {"message": "Failed to remove product from saved list."}, 409
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
        Deletes a product by from the saved list of a user by product name.
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
        try:
            return get_convo.get_convo(user1, user2)
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')

    # @api.expect(message_fields)
    def post(self, user1, user2):
        try:
            success = add_convo.add_convo(user1, user2)
            if success:
                return {"message": "Message added successfully"}, HTTPStatus.CREATED
            else:
                return {"message": "Message not added"}, HTTPStatus.NOT_ACCEPTABLE
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')
        
    def update(self, user1, user2, message):
        try:
            update_convo.update_convo(user1, user2, message)
        except ValueError as e:
            raise wz.NotAcceptable(f'{str(e)}')

    def delete(self, user1, user2):
        try:
            success = delete_convo.delete_convo(user1, user2)
            if success:
                return {"message": "Message deleted successfully"}, HTTPStatus.OK
            else:
                return {"message": "Message not deleted"}, HTTPStatus.NOT_FOUND
        except ValueError as e:
            raise wz.NotFound(f'{str(e)}')


