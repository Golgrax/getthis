from flask import Flask
from shop_app.views import generate_full_page
from shared import database

app = Flask(__name__, static_folder='../assets', static_url_path='/static')

@app.route('/')
def home():
    # 1. Get all products from the database
    products = database.get_all_products()
    
    # 2. Pass the products into our template generating function
    return generate_full_page(products)