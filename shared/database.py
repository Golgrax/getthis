import sqlite3
import hashlib
from datetime import datetime

DATABASE_FILE = 'shop.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE_FILE)
    conn.row_factory = sqlite3.Row
    return conn

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cursor.execute('CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, name TEXT NOT NULL, email TEXT NOT NULL UNIQUE, password_hash TEXT NOT NULL)')
    cursor.execute('CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT NOT NULL, description TEXT, price REAL NOT NULL, image_url TEXT, stock INTEGER NOT NULL DEFAULT 0)')
    cursor.execute('CREATE TABLE IF NOT EXISTS cart (user_id INTEGER, product_id INTEGER, quantity INTEGER NOT NULL, FOREIGN KEY (user_id) REFERENCES users (id), FOREIGN KEY (product_id) REFERENCES products (id), PRIMARY KEY (user_id, product_id))')
    cursor.execute('CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, user_id INTEGER NOT NULL, order_date TEXT NOT NULL, status TEXT NOT NULL, total_amount REAL NOT NULL, FOREIGN KEY (user_id) REFERENCES users(id))')
    cursor.execute('CREATE TABLE IF NOT EXISTS order_items (id INTEGER PRIMARY KEY, order_id INTEGER NOT NULL, product_id INTEGER NOT NULL, quantity INTEGER NOT NULL, price_at_purchase REAL NOT NULL, FOREIGN KEY (order_id) REFERENCES orders(id), FOREIGN KEY (product_id) REFERENCES products(id))')

    if cursor.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        sample_products = [('PUP Baybayin Lanyard', 'Polytechnic University (PUP) Lanyard', 140.00, None, 50), ('PUP STUDY WITH STYLE T-Shirt', 'Classic T-Shirt', 450.00, None, 30), ('PUP Iskolar TOTE BAG', 'Eco-friendly Bag', 400.00, None, 40)]
        cursor.executemany('INSERT INTO products (name, description, price, image_url, stock) VALUES (?, ?, ?, ?, ?)', sample_products)

    conn.commit()
    conn.close()
    print("Database initialized with order tables.")

def create_user(name, email, password):
    conn = get_db_connection()
    try:
        conn.execute('INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)', (name, email, hash_password(password)))
        conn.commit()
        return True
    except sqlite3.IntegrityError: return False
    finally: conn.close()

def check_user_credentials(email, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user and user['password_hash'] == hash_password(password): return dict(user)
    return None

def get_all_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return [dict(p) for p in products]

def get_cart_items(user_id):
    conn = get_db_connection()
    items = conn.execute('SELECT p.id, p.name, p.price, c.quantity FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = ?', (user_id,)).fetchall()
    conn.close()
    return [dict(item) for item in items]

def add_to_cart(product_id, user_id, quantity=1):
    conn = get_db_connection()
    cursor = conn.cursor()
    result = cursor.execute('SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?', (user_id, product_id)).fetchone()
    if result:
        new_quantity = result['quantity'] + quantity
        cursor.execute('UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?', (new_quantity, user_id, product_id))
    else:
        cursor.execute('INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)', (user_id, product_id, quantity))
    conn.commit()
    conn.close()


def update_cart_quantity(product_id, user_id, quantity):
    conn = get_db_connection()
    if int(quantity) <= 0:
        conn.execute('DELETE FROM cart WHERE user_id = ? AND product_id = ?', (user_id, product_id))
    else:
        conn.execute('UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?', (quantity, user_id, product_id))
    conn.commit()
    conn.close()

def create_order(user_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    
    cart_items = get_cart_items(user_id)
    if not cart_items:
        return None

    total_amount = sum(item['price'] * item['quantity'] for item in cart_items)

    order_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    cursor.execute(
        'INSERT INTO orders (user_id, order_date, status, total_amount) VALUES (?, ?, ?, ?)',
        (user_id, order_date, 'Pending', total_amount)
    )
    order_id = cursor.lastrowid

    for item in cart_items:
        cursor.execute(
            'INSERT INTO order_items (order_id, product_id, quantity, price_at_purchase) VALUES (?, ?, ?, ?)',
            (order_id, item['id'], item['quantity'], item['price'])
        )

    cursor.execute('DELETE FROM cart WHERE user_id = ?', (user_id,))
    
    conn.commit()
    conn.close()
    return order_id