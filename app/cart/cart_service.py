import logging
from typing import Dict, Any

# Initialize the module logger
logger = logging.getLogger(__name__)

class CartService:
    """
    Service to handle shopping cart operations.
    """

    def __init__(self, cart_repository):
        """
        Initialize the cart service with a cart repository.

        :param cart_repository: Repository instance for handling data operations
        """
        self.cart_repository = cart_repository

    def save_cart(self, user_id: str, cart_data: Dict[str, Any]) -> None:
        """
        Save the shopping cart data to the user's profile.

        :param user_id: The unique identifier of the user
        :param cart_data: Dictionary representing shopping cart data
        :raises Exception: If saving fails
        """
        logger.info(f"Saving cart for user: {user_id}")
        try:
            self.cart_repository.save_cart(user_id, cart_data)
            logger.info("Cart saved successfully.")
        except Exception as e:
            logger.error(f"Failed to save cart for user {user_id}: {e}")
            raise

    def retrieve_cart(self, user_id: str) -> Dict[str, Any]:
        """
        Retrieve the shopping cart data for a user profile.

        :param user_id: The unique identifier of the user
        :return: Dictionary representing shopping cart data
        :raises Exception: If retrieval fails
        """
        logger.info(f"Retrieving cart for user: {user_id}")
        try:
            cart_data = self.cart_repository.get_cart(user_id)
            logger.info("Cart retrieved successfully.")
            return cart_data
        except Exception as e:
            logger.error(f"Failed to retrieve cart for user {user_id}: {e}")
            raise