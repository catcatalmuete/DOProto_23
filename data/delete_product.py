import data.db_connect as dbc


PRODUCTS_COLLECT = "products"
PRODUCT_ID = "_id"


def delete_product(prod_id: str):
    dbc.connect_db()
    return dbc.del_one(PRODUCTS_COLLECT, {PRODUCT_ID: prod_id})
