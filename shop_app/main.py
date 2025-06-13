import webview
import threading
from shop_app.app import app
from shop_app.api import Api
from shared.database import init_db

def run_flask():
    app.run(host='127.0.0.1', port=5000, debug=False)

if __name__ == '__main__':
    init_db()

    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    api = Api()
    webview.create_window(
        'PUP E-Commerce Shop',
        'http://127.0.0.1:5000',
        js_api=api,
        width=450,
        height=800,
        resizable=False
    )
    webview.start()