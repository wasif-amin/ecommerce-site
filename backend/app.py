from flask import Flask, jsonify, request, session
from flask_login import login_user
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_cors import CORS
app = Flask(__name__)
CORS(app, supports_credentials=True)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:21070212w@localhost:5432/ecommercesite'
app.config['SESSION_PERMANENT'] = False
db = SQLAlchemy(app)
app.secret_key = "21070212w"

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  name = db.Column(db.String(100))
  price = db.Column(db.Float)
  image_url = db.Column(db.String(200))
class Cart(db.Model):
  id = db.Column(db.Integer, primary_key=True, autoincrement=True)
  session_id = db.Column(db.String(100), nullable=False)
  product_id = db.Column(db.Integer, db.ForeignKey('product.id'))
  quantity = db.Column(db.Integer, default=1)
  product = db.relationship('Product', backref='cart_items')
  with app.app_context():
    db.create_all()
    print("database tables were created")


@app.route('/test-db')
def test_db():
    product = Product.query.first()
    if product:
        return f"Database is working! Found: {product.name} at ${product.price}"
    return "Database connected, but no products found."
@app.route('/create-tables')
def create_tables():
    with app.app_context():
        db.create_all()
    return "Tables created successfully!"
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
    session_id = request.args.get("session_id")
    if not session_id:
       return jsonify([])
    cart_items = Cart.query.filter_by(session_id=session_id).all()
    cart_list = []
    for item in cart_items:
        if item.product:
            cart_list.append({
                "id": item.id,
                "name": item.product.name,
                "price": item.product.price,
                "image_url": item.product.image_url,
                "quantity": item.quantity
            })
            
    return jsonify(cart_list)
@app.route('/api/add-product', methods=['POST'])
def add_product():
    if not session.get("is_admin"):
       return jsonify({"error": "Unauthorized"}), 403
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
   session_id = data.get('session_id')
   existing_item = Cart.query.filter_by(session_id=session_id, product_id=product_id).first()
    
   if existing_item:
        existing_item.quantity += 1
        db.session.commit()
   else:
        new_cart_item = Cart(session_id=session_id, product_id=product_id)
        db.session.add(new_cart_item)
        db.session.commit()
        return jsonify({"message": "Product added to cart successfully!"}), 201

    
@app.route('/api/remove-from-cart/<int:item_id>', methods=['DELETE'])
def remove_from_cart(item_id):
    cart_item = db.session.get(Cart, item_id)
    if cart_item:
        try:
            db.session.delete(cart_item)
            db.session.commit()
            return jsonify({"success": "Item removed"}), 200
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Could not delete item", "details": str(e)}), 500
    return jsonify({"error": "Item not found"}), 404

@app.route('/api/remove-from-store/<int:item_id>', methods=['DELETE'])
def remove_from_store(item_id):
   if not session.get("is_admin"):
      return  jsonify({"error": "Unauthorized"}), 403
   product = db.session.get(Product, item_id)
   if product:
    try:
        db.session.delete(product)
        db.session.commit()
        return jsonify({"success": "Item removed"}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"error": "Could not delete item", "details": str(e)}), 500
   return jsonify({"error": "Item not found"}), 404

      

@app.route('/api/update-cart-item/<int:item_id>', methods=['PUT'])
def update_cart(item_id):
   data = request.get_json()
   change = data.get('change', 0)
    
   cart_item = db.session.get(Cart, item_id)
     
   if cart_item:
    cart_item.quantity += change
        
    if cart_item.quantity <= 0:
        db.session.delete(cart_item)
            
    db.session.commit()  
    return jsonify({"message": "Cart updated successfully"}), 200
        
    return jsonify({"error": "Item not found"}), 404

@app.route("/api/wasif-login", methods=["POST"])          
def wasif_login():
    data = request.get_json()
    password = data.get("password")
    if password == "21070212w":
      session["is_admin"] = True
      return jsonify({"message": "logged in!"}), 200
    else:
      return jsonify({"error": "Invalid password"}), 401
   

@app.route("/api/check-auth")
def check_auth():
   return jsonify({"isAdmin": session.get("is_admin", False)})

@app.route("/api/wasif-logout")
def wasif_logout():
   session["is_admin"] = False
   return jsonify({"message": "logged out"}), 200
   
if __name__ == "__main__":
    app.run(port=5001, debug=True)