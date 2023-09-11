from pydantic import BaseModel,Field, root_validator
from pydantic.generics import GenericModel
from typing import Optional,Generic,TypeVar
from schemas.product import ProductOut
from datetime import date

T = TypeVar('T')

class OrderBase(BaseModel):
    total_amount: Optional[float]
    status: Optional[str] 

    class Config:
        orm_mode = True

class OrderItemBase(BaseModel):
    quantity: Optional[int] = None
    product_id: Optional[int] = None

class OrderItemOut(BaseModel):
    id:Optional[int] = None
    quantity:Optional[int] = None
    amount:Optional[float]= None
    product_id:Optional[int] = None
    product: ProductOut

    class Config:
        orm_mode = True

class RequestOrder(BaseModel):
    parameter: OrderBase = Field(...)

class RequestOrderItem(BaseModel):
    parameter: OrderItemBase = Field(...)

class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]