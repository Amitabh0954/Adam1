import logging
from typing import List, Dict

class SearchService:
    def __init__(self, product_repository):
        self.product_repository = product_repository
        self.logger = logging.getLogger(__name__)

    def search_products(self, query: str, page: int, per_page: int) -> Dict[str, any]:
        try:
            results = self.product_repository.search(query, page, per_page)
            total_results = self.product_repository.count_search_results(query)
            return {
                "results": results,
                "total": total_results,
                "page": page,
                "per_page": per_page
            }
        except Exception as e:
            self.logger.error(f"Error while searching for products: {str(e)}")
            raise e