from shared import database

class Api:
    def get_products(self):
        return database.get_all_products()

    def get_cart(self):
        # In a real app, you'd get the logged-in user's ID
        return database.get_cart_items(user_id=1)

    def add_to_cart(self, product_id):
        database.add_to_cart(product_id=product_id, user_id=1)
        return {'status': 'success'}

    def update_cart_quantity(self, product_id, quantity):
        database.update_cart_quantity(product_id=product_id, quantity=quantity, user_id=1)
        return {'status': 'success'}

    # Add login/register methods here later
    # def login(self, email, password): ...