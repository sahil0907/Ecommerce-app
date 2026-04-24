from flask import Flask, jsonify, request, render_template, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
import os
from dotenv import load_dotenv  
load_dotenv() 

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'dev-key-only')
database_url = os.getenv('DATABASE_URL')
if not database_url:
    raise ValueError("CRITICAL: DATABASE_URL environment variable is not set!")

# --- DATABASE CONFIG ---
app.config['SQLALCHEMY_DATABASE_URI'] = database_url
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)
class Product(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    price = db.Column(db.Float, nullable=False)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False) # In Pro, we hash this!

class Order(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product_name = db.Column(db.String(100))
    username = db.Column(db.String(80))   
@app.route('/')
def login():
    return render_template('login.html')

@app.route('/login', methods=['POST'])
def do_login():
    username = request.form.get('username')
    password = request.form.get('password')
    
    # Simple check: In v3 we will check the DB, for now let's just allow anyone
    session['user'] = username
    return redirect(url_for('products_page'))

@app.route('/products')
def products_page():
    if 'user' not in session:
        return redirect(url_for('login'))
    products = Product.query.all()
    return render_template('products.html', products=products, user=session['user'])

@app.route('/buy/<int:product_id>')
def buy_product(product_id):
    if 'user' not in session:
        return redirect(url_for('login'))
    
    product = Product.query.get(product_id)
    new_order = Order(product_name=product.name, username=session['user'])
    db.session.add(new_order)
    db.session.commit()
    
    return render_template('success.html', product_name=product.name)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
        # SEED DATA: Add a sample product if the table is empty
        if not Product.query.first():
            db.session.add(Product(name="DevOps Laptop", price=1200.00))
            db.session.commit()
    app.run(host='0.0.0.0', port=5000, debug=True)