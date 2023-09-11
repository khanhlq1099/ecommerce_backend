from sqlalchemy import Column, ForeignKey, Integer, Float
from sqlalchemy.orm import relationship

from config.db_config import Base

class Cart(Base):
    __tablename__ = "cart"

    id = Column(Integer,primary_key=True)
    user_id = Column(Integer, ForeignKey("user.id"))

    user = relationship("User",back_populates="cart") 
    cart_item = relationship("Cart_Item",back_populates="cart")

class Cart_Item(Base):
    __tablename__ = "cart_item"
    
    id = Column(Integer,primary_key=True)
    cart_id = Column(Integer, ForeignKey("cart.id"))
    product_id = Column(Integer, ForeignKey("product.id"))
    
    quantity = Column(Integer)
    amount = Column(Float)

    cart = relationship("Cart",back_populates="cart_item")
    product = relationship("Product",back_populates="cart_item")
  