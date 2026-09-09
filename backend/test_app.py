from backend.app import app
from unittest.mock import patch

def test_app_loads():
    assert app is not None

def test_get_products():
    with app.test_client() as client:
        response = client.get('/api/products')
        assert response.status_code in [200, 404]

def test_get_cart_products_no_session():
    with app.test_client() as client:
        response = client.get('/api/cart-products')
        assert response.status_code == 200
        assert response.get_json() == []

def test_create_tables():
    with app.test_client() as client:
        response = client.get('/create-tables')
        assert response.status_code == 200

def test_serve_upload_missing():
    with app.test_client() as client:
        response = client.get('/uploads/does-not-exist.jpg')
        assert response.status_code in [404, 500]

def test_add_product_no_admin():
    with app.test_client() as client:
        response = client.post('/api/add-product', json={"name": "test"})
        assert response.status_code in [401, 403, 400]

def test_get_cart_products_with_session():
    with app.test_client() as client:
        response = client.get('/api/cart-products?session_id=test123')
        assert response.status_code == 200

def test_add_product_as_admin():
    with app.test_client() as client:
        with patch('backend.app.session', {'is_admin': True}):
            response = client.post('/api/add-product', 
                                   data={'name': 'test', 'price': '10'},
                                   content_type='multipart/form-data')
            assert response.status_code != 403