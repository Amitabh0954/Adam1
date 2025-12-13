import logging
from typing import List, Any

class ShoppingCartError(Exception):
    """Custom exception for ShoppingCart operations"""
    pass

class ShoppingCart:
    """Represents the shopping cart"""

    def __init__(self, user_id: str = None):
        self.user_id = user_id
        self.items = []
        self.total_price = 0.0
        logging.info(f"ShoppingCart initialized for user: {user_id}")

    def add_product(self, product: dict):
        """Adds a product to the shopping cart"""
        if "price" not in product or "id" not in product:
            raise ShoppingCartError("Invalid product object")

        self.items.append(product)
        self.total_price += product["price"]
        logging.info(f"Added product {product['id']} to the cart. New total: {self.total_price}")

    def remove_product(self, product_id: str):
        """Removes a product from the shopping cart"""
        removed = False

        for product in self.items:
            if product["id"] == product_id:
                self.items.remove(product)
                self.total_price -= product["price"]
                removed = True
                logging.info(f"Removed product {product_id} from the cart. New total: {self.total_price}")
                break

        if not removed:
            logging.warning(f"Product {product_id} not found in the cart")
            raise ShoppingCartError("Product not found")

    def clear_cart(self):
        """Clears all items from the shopping cart"""
        self.items = []
        self.total_price = 0.0
        logging.info("Cleared the shopping cart")

    def list_items(self) -> List[Any]:
        """Lists all products in the cart"""
        return self.items

    def get_total_price(self) -> float:
        """Returns the total price of items in the cart"""
        return self.total_price

    def persist_cart(self):
        """Placeholder method for persisting cart for logged-in users"""
        if self.user_id:
            logging.info(f"Persisting shopping cart for user: {self.user_id}")
            # Logic to persist cart into database could go here
            pass
        else:
            logging.warning("Cannot persist cart for guest users")

# Example usage (can be removed later):
if __name__ == "__main__":
    cart = ShoppingCart(user_id="12345")
    cart.add_product({"id": "101", "name": "Product A", "price": 20.0})
    cart.add_product({"id": "102", "name": "Product B", "price": 30.0})
    print(cart.list_items())
    print(cart.get_total_price())
    cart.remove_product("101")
    print(cart.list_items())
    cart.clear_cart()
    print(cart.list_items())