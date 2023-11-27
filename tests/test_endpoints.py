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
        'name': 'Test Product',
        'price' : 10.0,
        'condition' : 'New',
        'brand': 'Test Brand',
        'categories': ['Electronics', 'Apparel'],
        'comments' : 'A great product!'
	}
    response = app.post('/add_product', json=data)
    assert response.status_code == 201
    