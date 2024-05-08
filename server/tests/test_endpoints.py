from server import endpoints
import json

def test_hello():
    app = endpoints.app.test_client()
    response = app.get('/hello')
    assert response.status_code == 200
    assert response.get_json() == {'hello' : 'world'}
    
def test_endpoints():
    app = endpoints.app.test_client()
    response = app.get('/endpoints')
    assert response.status_code == 200
  
    
def test_add_product():
    app = endpoints.app.test_client()
    data = {
        'user_id': 'test_user',
        'product_name': 'Test Product',
        'price' : 10.0,
        'condition' : 'New',
        'brand': 'Test Brand',
        'categories': ['Electronics', 'Apparel'],
        'date_posted': '2023-11-30',
        'comments' : 'A great product!'
	}
    response = app.post('/add_product', json=data)
    assert response.status_code == 201

# followers endpoint tests 
def test_followers_get():
    app = endpoints.app.test_client()
    response = app.get('/followers')
    assert response.status_code == 200
    assert response.get_json() == {'followers': []}

def test_followers_post():
    app = endpoints.app.test_client()
    data = {
        'user_id': 123,
        'follower_id': 456
    }
    response = app.post('/followers', json=data)
    assert response.status_code == 201
    assert response.get_json() == {'message': 'Follower added successfully'}

def test_followers_delete():
    app = endpoints.app.test_client()
    response = app.delete('/followers')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Followers deleted successfully'}


# shoppinbg cart endpoints test
def test_shopping_cart_get():
    app = endpoints.app.test_client()
    response = app.get('/shopping_cart')
    assert response.status_code == 200
    assert response.get_json() == {'shopping_cart': []}

def test_shopping_cart_post():
    app = endpoints.app.test_client()
    data = {
        'user_id': 123,
        'product_id': 456
    }
    response = app.post('/shopping_cart', json=data)
    assert response.status_code == 201
    assert response.get_json() == {'message': 'Product added to shopping cart successfully'}

def test_shopping_cart_delete():
    app = endpoints.app.test_client()
    response = app.delete('/shopping_cart')
    assert response.status_code == 200
    assert response.get_json() == {'message': 'Shopping cart cleared successfully'}

def test_shopping_cart_calc_checkout_price():
    app = endpoints.app.test_client()
    response = app.get('/shopping_cart/calc_checkout_price')
    assert response.status_code == 200
    assert response.get_json() == {'checkout_price': 0.0}
