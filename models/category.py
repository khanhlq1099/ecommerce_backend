from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config.db_config import Base

class Product_Category(Base):
    __tablename__ = "product_category"

    id = Column(Integer,primary_key=True)
    name = Column(String,nullable=False)

    product_sub_category = relationship("Product_Sub_Category",back_populates="product_category")
