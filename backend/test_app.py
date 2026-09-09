from backend.app import app

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