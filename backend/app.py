from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:21070212w@localhost:5432/ecommercesite'
db = SQLAlchemy(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100))
  price = db.Column(db.Float)
  image_url = db.Column(db.String(200))
class Cart(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  product_id = db.Column(db.Integer, db.ForeignKey(Product.id))
  quantity = db.Column(db.Integer, default=1)
  product = db.relationship('Product')
  with app.app_context():
    db.create_all()
    print("database tables were created")


@app.route('/test-db')
def test_db():
    product = Product.query.first()
    if product:
        return f"Database is working! Found: {product.name} at ${product.price}"
    return "Database connected, but no products found."

@app.route('/api/products')
def get_products():
   result = db.session.execute(db.select(Product))
   products = result.scalars().all()
   product_list = [{"id": p.id, "name": p.name, "price": p.price, "image_url": p.image_url} for p in products]
   if product_list:
        return jsonify(product_list)
   else:  
    return jsonify({"error": "No product found"}), 404
   
@app.route('/api/cart-products')
def get_cart_products():
    cart_items = Cart.query.all()
    cart_list = []

    for item in cart_items:
        print(f"cart item id: {item.id} has product: {item.product}")
        if item.product:
            cart_list.append({
                "id": item.id,
                "name": item.product.name,
                "price": item.product.price,
                "image_url": item.product.image_url,
                "quantity": item.quantity
            })

    if cart_list:
        return jsonify(cart_list)
    else:
        return jsonify({"error": "no items found in cart"}), 404
       
@app.route('/api/add-product', methods=['POST'])
def add_product():
     data = request.json
     new_product = Product(
        name=data['name'],
        price=data['price'],
        image_url=data['image_url']
    )
     db.session.add(new_product)
     db.session.commit()

     return jsonify({"message": "Product added successfully!"}), 201

@app.route('/api/add/cart', methods=['POST'])
def add_to_cart():
   data = request.json
   product_id = data.get('product_id')
   new_cart_item = Cart(product_id=product_id)
   db.session.add(new_cart_item)
   db.session.commit()
   return jsonify({"message": "Product added to cart successfully!"}), 201


if __name__ == "__main__":
    app.run(debug=True)