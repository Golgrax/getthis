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
        return {'success': False, 'message': 'Invalid email or password.'}

    def register(self, name, email, password):
        if not all([name, email, password]):
            return {'success': False, 'message': 'All fields are required.'}
        success = database.create_user(name, email, password)
        if success:
            return {'success': True}
        return {'success': False, 'message': 'Email already in use.'}

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
        if not self.current_user: return {'status': 'error', 'message': 'Please log in first.'}
        database.add_to_cart(product_id=product_id, user_id=self.current_user['id'])
        return {'status': 'success'}

    def update_cart_quantity(self, product_id, quantity):
        if not self.current_user: return {'status': 'error', 'message': 'Please log in first.'}
        database.update_cart_quantity(product_id=product_id, user_id=self.current_user['id'], quantity=quantity)
        return {'status': 'success'}