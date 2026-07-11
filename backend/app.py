from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:21070212w@localhost:5432/ecommercesite'
db = SQLAlchemy(app)

class Product(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100))
  price = db.Column(db.Float)
  

with app.app_context():
  db.create_all()
  print("database tables were created")


@app.route('/test-db')
def test_db():
    product = Product.query.first()
    if product:
        return f"Database is working! Found: {product.name} at ${product.price}"
    return "Database connected, but no products found."

if __name__ == "__main__":
    app.run(debug=True)