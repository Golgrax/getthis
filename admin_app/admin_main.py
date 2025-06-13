import webview
import threading
from admin_app.admin_app import app
from admin_app.admin_api import AdminApi

def run_flask():
    # The admin app runs on port 5001
    app.run(host='127.0.0.1', port=5001)

if __name__ == '__main__':
    flask_thread = threading.Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()

    api = AdminApi()
    webview.create_window(
        'PUP Shop Admin',
        'http://127.0.0.1:5001',
        js_api=api,
        width=1024,
        height=768
    )
    webview.start()