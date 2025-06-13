from shared import database

class Api:
    def get_products(self):
        return database.get_all_products()
    
    def add_product(self, name, price, quantity, description):
        try:
            # Try to convert to numbers. If it fails, it means bad data was sent.
            price_float = float(price)
            quantity_int = int(quantity)
            if not name: # Also check if name is empty
                return {'status': 'error', 'message': 'Item name cannot be empty.'}
            database.add_product(name, price_float, quantity_int, description)
            return {'status': 'success'}
        except (ValueError, TypeError):
            # This block will catch errors if price/quantity are empty or not numbers
            return {'status': 'error', 'message': 'Please provide valid numbers for Price and Quantity.'}

    def update_product(self, product_id, name, price, quantity, description):
        try:
            price_float = float(price)
            quantity_int = int(quantity)
            if not name:
                 return {'status': 'error', 'message': 'Item name cannot be empty.'}
            database.update_product(product_id, name, price_float, quantity_int, description)
            return {'status': 'success'}
        except (ValueError, TypeError):
            return {'status': 'error', 'message': 'Please provide valid numbers for Price and Quantity.'}

    def delete_product(self, product_id):
        database.delete_product(product_id)
        return {'status': 'success'}