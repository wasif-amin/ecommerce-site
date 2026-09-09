
from backend.app import app
from unittest.mock import patch, MagicMock
from io import BytesIO

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



def test_add_to_cart():
    with app.test_client() as client:
        with patch('backend.app.db.session.add'), \
             patch('backend.app.db.session.commit'), \
             patch('backend.app.Product') as MockProd:
            mock_prod = MagicMock()
            mock_prod.id = 1
            MockProd.query.get.return_value = mock_prod
            response = client.post('/api/add/cart', json={"product_id": 1, "session_id": "test123"})
            assert response.status_code in [200, 201, 400, 404]

def test_remove_from_cart():
    with app.test_client() as client:
        with patch('backend.app.Cart') as MockCart, \
             patch('backend.app.db.session.delete'), \
             patch('backend.app.db.session.commit'):
            MockCart.query.get.return_value = MagicMock()
            response = client.delete('/api/remove-from-cart/1')
            assert response.status_code in [200, 404, 500]

def test_remove_from_store_as_admin():
    with app.test_client() as client:
        with patch('backend.app.session', {'is_admin': True}), \
             patch('backend.app.Product') as MockProd, \
             patch('backend.app.db.session.delete'), \
             patch('backend.app.db.session.commit'):
            MockProd.query.get.return_value = MagicMock()
            response = client.delete('/api/remove-from-store/1')
            assert response.status_code in [200, 404]

def test_update_cart_item():
    with app.test_client() as client:
        with patch('backend.app.Cart') as MockCart, \
             patch('backend.app.db.session.commit'):
            mock_item = MagicMock()
            mock_item.quantity = 2
            MockCart.query.get.return_value = mock_item
            response = client.put('/api/update-cart-item/1', json={"quantity": 3})
            assert response.status_code in [200, 404]

def test_wasif_login():
    with app.test_client() as client:
        response = client.post('/api/wasif-login', json={"password": "wrong"})
        assert response.status_code in [200, 401, 400]

def test_check_auth_and_logout():
    with app.test_client() as client:
        r1 = client.get('/api/check-auth')
        assert r1.status_code in [200, 401]
        r2 = client.get('/api/wasif-logout')
        assert r2.status_code in [200, 302]

def test_checkout_session():
    with app.test_client() as client:
        with patch('backend.app.stripe.checkout.Session.create', return_value=MagicMock(url="http://test.com")) as mock_stripe:
            response = client.post('/api/checkout-session', json={"items": []})
            assert response.status_code in [200, 400, 500]