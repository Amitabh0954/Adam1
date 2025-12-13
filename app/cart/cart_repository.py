import logging
from typing import Dict, Any

logger = logging.getLogger(__name__)

class CartRepository:
    """
    Repository class for managing shopping cart persistence.
    """

    def __init__(self, db):
        """
        Initialize the repository with a database connection.

        :param db: Database connection or ORM instance
        """
        self.db = db

    def save_cart(self, user_id: str, cart_data: Dict[str, Any]) -> None:
        """
        Save shopping cart details to the database.

        :param user_id: The unique identifier of the user
        :param cart_data: The shopping cart data to be saved
        :raises Exception: If database operation fails
        """
        logger.info(f"Saving cart to database for user: {user_id}")
        try:
            self.db.save("cart", {"user_id": user_id, "data": cart_data})
            logger.info("Cart saved successfully to database.")
        except Exception as e:
            logger.error(f"Error saving cart for user {user_id}: {e}")
            raise

    def get_cart(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve shopping cart details from the database.

        :param user_id: The unique identifier of the user
        :return: The shopping cart data
        :raises Exception: If database operation fails
        """
        logger.info(f"Retrieving cart from database for user: {user_id}")
        try:
            result = self.db.get("cart", {"user_id": user_id})
            return result["data"]
        except Exception as e:
            logger.error(f"Error retrieving cart for user {user_id}: {e}")
            raise