"""
Module for managing cart-related routes.
"""

from flask import Blueprint, request, jsonify
from app.services.cart.service import CartService

cart_bp = Blueprint('cart', __name__, url_prefix='/cart')

@cart_bp.route('/save', methods=['POST'])
def save_cart():
    """Handle cart saving on logout."""
    try:
        user_id = request.json.get('user_id')
        cart_data = request.json.get('cart')

        if not user_id or not cart_data:
            return jsonify({"error": "Missing user_id or cart data."}), 400

        CartService.save_cart(user_id, cart_data)
        return jsonify({"message": "Cart saved successfully."}), 200
    except Exception as e:
        return jsonify({"error": "Failed to save cart.", "details": str(e)}), 500

@cart_bp.route('/retrieve', methods=['GET'])
def retrieve_cart():
    """Handle cart retrieval on login."""
    try:
        user_id = request.args.get('user_id')

        if not user_id:
            return jsonify({"error": "Missing user_id."}), 400

        cart_data = CartService.retrieve_cart(user_id)
        return jsonify({"cart": cart_data}), 200
    except Exception as e:
        return jsonify({"error": "Failed to retrieve cart.", "details": str(e)}), 500