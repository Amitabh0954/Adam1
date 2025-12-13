import logging
from flask import Blueprint, request, jsonify

from app.cart.cart_service import CartService

logger = logging.getLogger(__name__)

cart_blueprint = Blueprint('cart', __name__, url_prefix='/cart')

# Dependency Injection Placeholder: Replace with actual instances
cart_service = CartService(cart_repository=None)

@cart_blueprint.route('/save', methods=['POST'])
def save_cart():
    """
    API endpoint to save the shopping cart.

    Request Body:
    {
        "user_id": "<string>",
        "cart": {"<product_id>": <product_details>, ...}
    }

    :return: JSON response with success status
    """
    data = request.json
    user_id = data.get("user_id")
    cart_data = data.get("cart")

    try:
        cart_service.save_cart(user_id, cart_data)
        return jsonify({"status": "success"}), 200
    except Exception as e:
        logger.error(f"Error in save_cart: {e}")
        return jsonify({"error": "Failed to save cart."}), 500

@cart_blueprint.route('/retrieve', methods=['GET'])
def retrieve_cart():
    """
    API endpoint to retrieve the shopping cart.

    Query Parameters:
    ?user_id=<string>

    :return: JSON response with the cart data
    """
    user_id = request.args.get("user_id")

    try:
        cart_data = cart_service.retrieve_cart(user_id)
        return jsonify({"status": "success", "cart": cart_data}), 200
    except Exception as e:
        logger.error(f"Error in retrieve_cart: {e}")
        return jsonify({"error": "Failed to retrieve cart."}), 500