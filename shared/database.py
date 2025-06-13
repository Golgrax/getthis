import sqlite3
import hashlib

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
    
    # Create tables
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS products (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        description TEXT,
        price REAL NOT NULL,
        image_url TEXT,
        stock INTEGER NOT NULL DEFAULT 0
    )
    ''')

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS cart (
        user_id INTEGER,
        product_id INTEGER,
        quantity INTEGER NOT NULL,
        FOREIGN KEY (user_id) REFERENCES users (id),
        FOREIGN KEY (product_id) REFERENCES products (id),
        PRIMARY KEY (user_id, product_id)
    )
    ''')
    
    # Check if products exist before inserting
    cursor.execute("SELECT COUNT(*) FROM products")
    if cursor.fetchone()[0] == 0:
        # Add sample products
        sample_products = [
            ('PUP Baybayin Lanyard', 'Classic Edition Lanyard', 140.00, '/static/images/lanyard.png', 50),
            ('PUP STUDY WITH STYLE T-Shirt', 'Classic University T-Shirt', 450.00, '/static/images/tshirt.png', 30),
            ('PUP Iskolar TOTE BAG', 'Eco-friendly and durable tote bag', 400.00, '/static/images/totebag.png', 40),
            ('PUP Jeepney Signage', 'Collectible decorative item for Iskolars', 250.00, '/static/images/jeepney.png', 100)
        ]
        cursor.executemany(
            'INSERT INTO products (name, description, price, image_url, stock) VALUES (?, ?, ?, ?, ?)',
            sample_products
        )

    conn.commit()
    conn.close()
    print("Database initialized.")

# --- Product Functions ---
def get_all_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return [dict(p) for p in products]

def add_product(name, price, quantity, description):
    conn = get_db_connection()
    conn.execute(
        'INSERT INTO products (name, price, stock, description) VALUES (?, ?, ?, ?)',
        (name, float(price), int(quantity), description)
    )
    conn.commit()
    conn.close()

def update_product(product_id, name, price, quantity, description):
    conn = get_db_connection()
    conn.execute(
        'UPDATE products SET name = ?, price = ?, stock = ?, description = ? WHERE id = ?',
        (name, float(price), int(quantity), description, product_id)
    )
    conn.commit()
    conn.close()

def delete_product(product_id):
    conn = get_db_connection()
    conn.execute('DELETE FROM products WHERE id = ?', (product_id,))
    conn.commit()
    conn.close()

# --- Cart Functions ---
def get_cart_items(user_id=1): # Using user_id 1 as a default for this demo
    conn = get_db_connection()
    items = conn.execute('''
        SELECT p.id, p.name, p.price, c.quantity, p.image_url
        FROM cart c
        JOIN products p ON c.product_id = p.id
        WHERE c.user_id = ?
    ''', (user_id,)).fetchall()
    conn.close()
    return [dict(item) for item in items]

def add_to_cart(product_id, quantity=1, user_id=1):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute(
        'SELECT quantity FROM cart WHERE user_id = ? AND product_id = ?',
        (user_id, product_id)
    )
    result = cursor.fetchone()
    if result:
        new_quantity = result['quantity'] + quantity
        cursor.execute(
            'UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?',
            (new_quantity, user_id, product_id)
        )
    else:
        cursor.execute(
            'INSERT INTO cart (user_id, product_id, quantity) VALUES (?, ?, ?)',
            (user_id, product_id, quantity)
        )
    conn.commit()
    conn.close()

def update_cart_quantity(product_id, quantity, user_id=1):
    conn = get_db_connection()
    if int(quantity) <= 0:
        conn.execute('DELETE FROM cart WHERE user_id = ? AND product_id = ?', (user_id, product_id))
    else:
        conn.execute(
            'UPDATE cart SET quantity = ? WHERE user_id = ? AND product_id = ?',
            (quantity, user_id, product_id)
        )
    conn.commit()
    conn.close()