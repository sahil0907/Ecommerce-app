from flask import Flask, jsonify, request, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, jsonify, request, render_template # Add render_template
import os

app = Flask(__name__)

# --- DATABASE CONFIG ---
# --- DATABASE CONFIG (Version 2: PostgreSQL) ---
# Format: postgresql://user:password@host:port/database
# Since we are on Level 0, host is 'localhost'
DB_USER = "ecom_user"
DB_PASS = "ecom_password"
DB_HOST = "localhost"
DB_NAME = "ecom_db"

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

# --- ROUTES ---

# Home Route to serve the Frontend
@app.route('/')
def index():
    return render_template('index.html')

# 1. Health Check
@app.route('/health', methods=['GET'])
def health():
    return jsonify({"status": "healthy", "tier": "tier-2"}), 200

# 2. Product Catalog
@app.route('/products', methods=['GET'])
def get_products():
    products = Product.query.all()
    return jsonify([{"id": p.id, "name": p.name, "price": p.price} for p in products])

# 3. Add Product
@app.route('/products', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data or 'name' not in data or 'price' not in data:
        return jsonify({"error": "Invalid data"}), 400
    
    new_product = Product(name=data['name'], price=data['price'])
    db.session.add(new_product)
    db.session.commit()
    return jsonify({"message": "Product added!"}), 201

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(host='0.0.0.0', port=5000, debug=True)