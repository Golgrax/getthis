from flask import Flask
from admin_app.admin_views import generate_admin_page

app = Flask(__name__)

@app.route('/')
def admin_home():
    return str(generate_admin_page())