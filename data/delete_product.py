import data.db_connect as dbc


PRODUCTS_COLLECT = "products"
PRODUCT_NAME = "name"

def delete_product(prod_name: str):
    dbc.connect_db()
    return dbc.del_one(PRODUCTS_COLLECT, {PRODUCT_NAME: prod_name})