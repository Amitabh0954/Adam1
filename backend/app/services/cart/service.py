"""
Module for shopping cart-related business logic.
"""

import logging
from app.repositories.cart_repository import CartRepository

logger = logging.getLogger(__name__)

class CartService:
    @staticmethod
    def save_cart(user_id: str, cart_data: dict) -> None:
        """Save the shopping cart to the repository."""
        try:
            CartRepository.save_cart_to_profile(user_id, cart_data)
        except Exception as e:
            logger.error(f"Failed to save cart for user {user_id}: {e}")
            raise e

    @staticmethod
    def retrieve_cart(user_id: str) -> dict:
        """Retrieve the shopping cart from the repository."""
        try:
            return CartRepository.get_cart_from_profile(user_id)
        except Exception as e:
            logger.error(f"Failed to retrieve cart for user {user_id}: {e}")
            raise e