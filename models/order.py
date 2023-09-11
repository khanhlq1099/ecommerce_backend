from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date, Float
from sqlalchemy.orm import relationship
from datetime import date

from config.db_config import Base

class Order(Base):
    __tablename__ = "order"

    id = Column(Integer, primary_key=True)  
    user_id = Column(Integer, ForeignKey("user.id"))
    payment_method_id = Column(Integer, ForeignKey("payment_method.id"))
    full_name = Column(String)
    date_of_birth = Column(Date)
    # email = Column(String, unique= True)
    class_name = Column(String)
    phone_number = Column(String)
    order_date = Column(Date,default=date.today())
    total_amount = Column(Float,default=0)
    status = Column(String,default="pending") 

    user = relationship("User", back_populates="order")
    order_item = relationship("Order_Item",back_populates="order")
    payment_method = relationship("Payment_Method", back_populates="order")

class Order_Item(Base):
    __tablename__ = "order_item"

    id = Column(Integer, primary_key=True)
    order_id = Column(Integer, ForeignKey("order.id"))
    product_id = Column(Integer,ForeignKey("product.id"))
    quantity = Column(Integer)
    amount = Column(Float,default=0)

    order = relationship("Order",back_populates="order_item")
    product = relationship("Product",back_populates="order_item")
