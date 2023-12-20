import data.db_connect as dbc

PRODUCTS_COLLECT = "products"
USER_ID = "user_id"
PRODUCT_NAME = "name"
PRODUCT_PRICE = "price"
PRODUCT_CONDITION = "condition"
PRODUCT_BRAND = "brand"
PRODUCT_CATEGORIES = "categories"
PRODUCT_DATE_POSTED = "date posted"
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

def add_product(user_id : str, name : str, price : int, condition : str, 
				brand : str, categories : str, date_posted : str, comments: str):
	dbc.connect_db()

	# check if product already exists
	found_product = dbc.fetch_one(PRODUCTS_COLLECT, {PRODUCT_NAME: name})
	if found_product:
		raise ValueError(f'Duplicate product name: {name=}')
	new_prod = {}
	new_prod[USER_ID] = user_id
	new_prod[PRODUCT_NAME] = name
	new_prod[PRODUCT_PRICE] = price
	new_prod[PRODUCT_CONDITION] = condition
	new_prod[PRODUCT_BRAND] = brand
	new_prod[PRODUCT_CATEGORIES] = categories
	new_prod[PRODUCT_DATE_POSTED] = date_posted
	new_prod[PRODUCT_COMMENTS] = comments
	_id = dbc.insert_one(PRODUCTS_COLLECT, new_prod)
	return _id is not None