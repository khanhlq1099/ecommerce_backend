from pydantic import BaseModel,Field, root_validator
from pydantic.generics import GenericModel
from typing import Optional,Generic,TypeVar
from schemas.product import ProductOut

T = TypeVar('T')

class CartItemBase(BaseModel):
    quantity: Optional[int] = None
    product_id: Optional[int] = None

    @root_validator
    def quantity_must_positive(cls,v):
        quantity = v.get("quantity")
        if quantity < 0: 
            raise ValueError('Quantity must be positive!')
        elif quantity == 0:
            raise ValueError('Quantity must be different from zero!')
        return v

class CartItemOut(BaseModel):
    id:Optional[int] = None
    quantity:Optional[int] = None
    amount:Optional[float]= None
    product_id:Optional[int] = None
    product: ProductOut

    class Config:
        orm_mode = True

class RequestCartItem(BaseModel):
    parameter: CartItemBase = Field(...)

class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]