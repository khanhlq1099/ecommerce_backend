from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,Date, Float, PrimaryKeyConstraint
from sqlalchemy.orm import relationship

from config.db_config import Base

class User(Base):
    __tablename__ = "user"

    id = Column(Integer,primary_key=True)
    email = Column(String,nullable=False)
    password = Column(String,nullable=False)
    is_activate = Column(Boolean,default=True)
    is_profile = Column(Boolean,default=False)
    role = Column(Integer,default=3)

    user_detail = relationship("User_Detail",back_populates="user")
    cart = relationship("Cart",back_populates="user")
    order = relationship("Order", back_populates="user")

class User_Detail(Base):
    __tablename__ = "user_detail"
    __table_args__ = (
        PrimaryKeyConstraint('user_id'),
    )

    user_id = Column(Integer, ForeignKey("user.id"))
    full_name = Column(String,nullable=False)
    date_of_birth = Column(Date)
    class_name = Column(String,nullable=False)
    phone_number = Column(String)

    user = relationship("User",back_populates="user_detail")
