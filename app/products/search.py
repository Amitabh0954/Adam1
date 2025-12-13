"""
Module for Product Search functionality.
Provides services for querying products based on user input.
"""

import logging
from typing import List, Dict, Optional

logger = logging.getLogger(__name__)

class ProductSearchService:
    """
    Service for searching products in the catalog.
    """

    def __init__(self, product_repository):
        self.product_repository = product_repository

    def search_products(self, query: str, page: int = 1, per_page: int = 10) -> Dict[str, Optional[List[Dict]]]:
        """
        Search products based on names, categories, or attributes.

        :param query: Search term entered by the user
        :param page: Page number for pagination
        :param per_page: Number of items per page
        :return: Dictionary containing search results and pagination details
        """
        try:
            results, total_count = self.product_repository.find_by_query(query, page, per_page)
            return {
                "results": results,
                "pagination": {
                    "current_page": page,
                    "total_pages": (total_count // per_page) + (1 if total_count % per_page > 0 else 0),
                    "per_page": per_page,
                    "total_count": total_count
                }
            }
        except Exception as e:
            logger.error("Failed to search products: %s", str(e))
            raise ProductSearchError("An error occurred during product search.")

class ProductSearchError(Exception):
    """
    Custom exception for product search errors.
    """
    pass

# Example initialization of the service:
# product_repository = SomeProductRepositoryImplementation()
# search_service = ProductSearchService(product_repository)
