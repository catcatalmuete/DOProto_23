import data.db_connect as dbc

PRODUCTS_COLLECT = "products"
USER_ID = "user_id"
PRODUCT_NAME = "name"
PRODUCT_PRICE = "price"
PRODUCT_CONDITION = "condition"
PRODUCT_BRAND = "brand"
PRODUCT_CATEGORIES = "categories"
PRODUCT_DATE_POSTED = "date_posted"
PRODUCT_COMMENTS = "comments"

"""
Params:
 - name (str) : name of product
 - price (float) : price of produt
 - condition (str) : condition of product (new, refurbished, used, damaged, for parts)
 - brand (str) : brand of product
 - categories (list) : list of categories for the product
 - date_posted (str) : date when product was posted
 - comments (str) : comments from the seller
"""

def add_products(user_id, name, price, condition, brand, categories, date_posted, comments):
	dbc.connect_db()

	# check if product already exists
	found_product = dbc.fetch_one({PRODUCT_NAME: name}, PRODUCTS_COLLECT)
	if found_product:
		return False
	
	# Insert new product into database
	new_product = {
		USER_ID: user_id,
		PRODUCT_NAME: name, 
		PRODUCT_PRICE: price,
		PRODUCT_CONDITION: condition,
		PRODUCT_BRAND: brand, 
		PRODUCT_CATEGORIES: categories,
		PRODUCT_DATE_POSTED: date_posted,
		PRODUCT_COMMENTS: comments
		}
	dbc.insert_one(new_product, PRODUCTS_COLLECT)
	return True