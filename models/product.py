from sqlalchemy import Column, ForeignKey, Integer, String, Float
from sqlalchemy.orm import relationship

from config.db_config import Base

class Product(Base):
    __tablename__ = "product"

    id = Column(Integer,primary_key=True)
    product_sub_category_id = Column(Integer, ForeignKey("product_sub_category.id"))

    name = Column(String,nullable=False)
    price = Column(Float,nullable=False)
    quantity_in_stock = Column(Integer,nullable=False)
    description = Column(String)

    cart_item = relationship("Cart_Item",back_populates="product")
    product_sub_category = relationship("Product_Sub_Category",back_populates="product")
    order_item = relationship("Order_Item",back_populates="product")