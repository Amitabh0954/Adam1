"""
Module for products-related views.
"""
from flask import Blueprint, request, jsonify
from app.common.models import Product
from app.common.extensions import db

products_bp = Blueprint('products_bp', __name__)

@products_bp.route('/add_product', methods=['POST'])
def add_product():
    data = request.get_json()
    if not data:
        return jsonify({"error": "No input data provided"}), 400
    
    name = data.get('name')
    description = data.get('description')
    price = data.get('price')

    if not name:
        return jsonify({"error": "Product name is required"}), 400

    if not description:
        return jsonify({"error": "Product description is required"}), 400

    if price is None:
        return jsonify({"error": "Product price is required"}), 400

    if price < 0:
        return jsonify({"error": "Product price must be a positive number"}), 400
    
    existing_product = Product.query.filter_by(name=name).first()
    if existing_product:
        return jsonify({"error": "Product name must be unique"}), 400
    
    new_product = Product(name=name, description=description, price=price)
    db.session.add(new_product)
    db.session.commit()
    
    return jsonify({"message": "Product added successfully", "product": new_product.to_dict()}), 201