from shared import database

class AdminApi:
    def get_products(self):
        return database.get_all_products()
    
    def add_product(self, name, price, quantity, description):
        database.add_product(name, price, quantity, description)
        return {'status': 'success'}

    def update_product(self, product_id, name, price, quantity, description):
        database.update_product(product_id, name, price, quantity, description)
        return {'status': 'success'}

    def delete_product(self, product_id):
        database.delete_product(product_id)
        return {'status': 'success'}