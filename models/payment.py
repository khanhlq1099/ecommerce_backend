from sqlalchemy import Column, Integer, String,Date
from sqlalchemy.orm import relationship

from config.db_config import Base

class Payment_Method(Base):
    __tablename__ = "payment_method"

    id = Column(Integer, primary_key=True)
    provider = Column(String)
    account_number = Column(String)
    expiry_date = Column(Date)

    order = relationship("Order",back_populates="payment_method")