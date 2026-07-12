from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
app = Flask(__name__)
CORS(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:21070212w@localhost:5432/ecommercesite'
db = SQLAlchemy(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  price = db.Column(db.Float)
  image_url = db.Column(db.String(200))
  

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
   product_list = [{"name": p.name, "price": p.price, "image_url": p.image_url} for p in products]
   if product_list:
        return jsonify(product_list)
   else:  
    return jsonify({"error": "No product found"}), 404  
if __name__ == "__main__":
    app.run(debug=True)