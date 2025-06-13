from shared import database

class Api:
    def __init__(self):
        self.current_user = None

    # --- Auth ---
    def login(self, email, password):
        user = database.check_user_credentials(email, password)
        if user:
            self.current_user = user
            return {'success': True, 'user': {'id': user['id'], 'name': user['name']}}
        return {'success': False, 'message': 'Invalid credentials.'}

    def register(self, name, email, password):
        success = database.create_user(name, email, password)
        return {'success': success, 'message': 'Registration successful!' if success else 'Email already in use.'}
    
    def logout(self):
        self.current_user = None
        return {'success': True}

    # --- Products ---
    def get_products(self):
        return database.get_all_products()

    # --- Cart ---
    def get_cart(self):
        if not self.current_user: return []
        return database.get_cart_items(user_id=self.current_user['id'])

    def add_to_cart(self, product_id):
        if not self.current_user: return {'status': 'error', 'message': 'Please log in.'}
        database.add_to_cart(product_id=product_id, user_id=self.current_user['id'])
        return {'status': 'success'}

    def update_cart_quantity(self, product_id, quantity):
        if not self.current_user: return {'status': 'error'}
        database.update_cart_quantity(product_id=product_id, user_id=self.current_user['id'], quantity=quantity)
        return {'status': 'success'}

    # --- Checkout (NEW) ---
    def place_order(self):
        if not self.current_user:
            return {'success': False, 'message': 'User not logged in.'}
        
        order_id = database.create_order(user_id=self.current_user['id'])
        
        if order_id:
            return {'success': True, 'order_id': order_id, 'message': f'Order #{order_id} placed successfully!'}
        else:
            return {'success': False, 'message': 'Your cart is empty.'}