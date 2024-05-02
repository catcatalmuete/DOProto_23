import data.db_connect as dbc
from bson import ObjectId

PRODUCTS_COLLECT = "products"
USER_ID = "user_id"
PRODUCT_NAME = "name"
PRODUCT_PRICE = "price"
PRODUCT_CONDITION = "condition"
PRODUCT_BRAND = "brand"
PRODUCT_CATEGORIES = "categories"
PRODUCT_DATE_POSTED = "date_posted"
PRODUCT_COMMENTS = "comments"
PRODUCT_ID = "_id"


def get_products():
	dbc.connect_db()
	return dbc.fetch_all_as_dict(PRODUCT_ID, PRODUCTS_COLLECT)

def get_product(prod_id: str):
    prod_id = ObjectId(prod_id)
    dbc.connect_db()
    return dbc.fetch_one(PRODUCTS_COLLECT, {PRODUCT_ID: prod_id})
