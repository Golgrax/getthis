from flask import Flask, jsonify
from shop_app.views import generate_main_page
from shared import database

# Configure static folder to be the top-level 'assets'
app = Flask(__name__, static_folder='../assets', static_url_path='/static')

@app.route('/')
def home():
    products = database.get_all_products()
    return str(generate_main_page(products))