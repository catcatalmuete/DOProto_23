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

def get_product():
	dbc.connect_db()
	return dbc.fetch_all_as_dict(PRODUCT_NAME, PRODUCTS_COLLECT)

