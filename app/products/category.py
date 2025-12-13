"""
Module for Product Categorization functionality.
Enables assigning and managing product categories.
"""

import logging
from typing import List

logger = logging.getLogger(__name__)

class ProductCategorizationService:
    """
    Service for categorizing products.
    """

    def __init__(self, category_repository):
        self.category_repository = category_repository

    def assign_categories_to_product(self, product_id: int, category_ids: List[int]) -> bool:
        """
        Assign categories to a product.

        :param product_id: ID of the product to categorize
        :param category_ids: List of category IDs to assign
        :return: Whether the assignment was successful
        """
        if not category_ids:
            raise ProductCategorizationError("Product must belong to at least one category.")

        try:
            self.category_repository.attach_categories(product_id, category_ids)
            return True
        except Exception as e:
            logger.error("Failed to assign categories: %s", str(e))
            raise ProductCategorizationError("An error occurred during category assignment.")

    def create_category(self, name: str, parent_category_id: int = None) -> int:
        """
        Create a new product category.

        :param name: Name of the category
        :param parent_category_id: Optional parent category ID for hierarchy
        :return: ID of the newly created category
        """
        try:
            return self.category_repository.create(name=name, parent_id=parent_category_id)
        except Exception as e:
            logger.error("Failed to create category: %s", str(e))
            raise ProductCategorizationError("An error occurred during category creation.")

class ProductCategorizationError(Exception):
    """
    Custom exception for product categorization errors.
    """
    pass

# Example initialization of the service:
# category_repository = SomeCategoryRepositoryImplementation()
# categorization_service = ProductCategorizationService(category_repository)
