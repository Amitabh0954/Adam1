# -*- coding: utf-8 -*-
"""
Product model for handling product data.
"""
from sqlalchemy import Column, Integer, String, Float, Boolean
from database import Base

class Product(Base):
    __tablename__ = 'products'

    id = Column(Integer, primary_key=True)
    name = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    price = Column(Float, nullable=False)
    in_stock = Column(Boolean, default=True)

    def __repr__(self):
        return f'<Product {self.name}>'
