import logging
from typing import Any, Optional, Dict
from app.common.exceptions import ServiceException

logger = logging.getLogger(__name__)

class CartService:
    """
    Service for handling shopping cart functionality
    """

    def __init__(self, cart_repository: Any):
        """Initialize CartService with a repository interface"""
        self.cart_repository = cart_repository

    def save_cart_state(self, user_id: str, cart: Dict[str, Any]) -> None:
        """
        Save the current state of the user's shopping cart.

        :param user_id: Unique identifier for the user
        :param cart: Cart details to be saved
        """
        try:
            logger.debug(f"Saving cart state for user_id={user_id} with cart={cart}")
            self.cart_repository.save(user_id, cart)
        except Exception as e:
            logger.error(f"Error saving cart state for user_id={user_id}: {str(e)}")
            raise ServiceException(f"Unable to save cart state: {str(e)}")

    def retrieve_cart_state(self, user_id: str) -> Optional[Dict[str, Any]]:
        """
        Retrieve the user's saved cart state.

        :param user_id: Unique identifier for the user
        :return: Saved cart details or None
        """
        try:
            logger.debug(f"Retrieving cart state for user_id={user_id}")
            return self.cart_repository.retrieve(user_id)
        except Exception as e:
            logger.error(f"Error retrieving cart state for user_id={user_id}: {str(e)}")
            raise ServiceException(f"Unable to retrieve cart state: {str(e)}")
