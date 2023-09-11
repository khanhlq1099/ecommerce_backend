from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from config.db_config import Base


class Product_Sub_Category(Base):
    __tablename__ = "product_sub_category"

    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)

    product_category_id = Column(Integer, ForeignKey("product_category.id"))

    product_category = relationship("Product_Category",back_populates="product_sub_category")
    product = relationship("Product",back_populates="product_sub_category")
  