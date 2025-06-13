from flask import Flask
from shop_app.views import generate_full_page
from shared import database

app = Flask(__name__, static_folder='../assets', static_url_path='/static')

@app.route('/')
def home():
    return str(generate_full_page())