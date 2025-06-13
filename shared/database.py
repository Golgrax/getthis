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
    
    # Create users table
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL UNIQUE,
        password_hash TEXT NOT NULL
    )
    ''')

    # Create products table
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

    # Create cart table
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
    
    # Add sample products if they don't exist
    if cursor.execute("SELECT COUNT(*) FROM products").fetchone()[0] == 0:
        sample_products = [
            ('PUP Baybayin Lanyard', 'Polytechnic University (PUP) Lanyard', 140.00, '/static/images/lanyard.png', 50),
            ('PUP STUDY WITH STYLE T-Shirt', 'Classic T-Shirt', 450.00, '/static/images/tshirt.png', 30),
            ('PUP Iskolar TOTE BAG', 'Eco-friendly Bag', 400.00, '/static/images/totebag.png', 40),
            ('PUP Jeepney Signage', 'Collectible Item', 250.00, '/static/images/jeepney.png', 100)
        ]
        cursor.executemany('INSERT INTO products (name, description, price, image_url, stock) VALUES (?, ?, ?, ?, ?)', sample_products)

    conn.commit()
    conn.close()
    print("Database initialized.")

# --- User Functions ---
def create_user(name, email, password):
    conn = get_db_connection()
    try:
        conn.execute(
            'INSERT INTO users (name, email, password_hash) VALUES (?, ?, ?)',
            (name, email, hash_password(password))
        )
        conn.commit()
        return True
    except sqlite3.IntegrityError: # This happens if email is not unique
        return False
    finally:
        conn.close()

def check_user_credentials(email, password):
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM users WHERE email = ?', (email,)).fetchone()
    conn.close()
    if user and user['password_hash'] == hash_password(password):
        return dict(user)
    return None

# --- Product Functions (no changes) ---
def get_all_products():
    conn = get_db_connection()
    products = conn.execute('SELECT * FROM products').fetchall()
    conn.close()
    return [dict(p) for p in products]

# --- Cart Functions (no changes) ---
def get_cart_items(user_id):
    conn = get_db_connection()
    items = conn.execute('''
        SELECT p.id, p.name, p.price, c.quantity, p.image_url
        FROM cart c JOIN products p ON c.product_id = p.id WHERE c.user_id = ?
    ''', (user_id,)).fetchall()
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