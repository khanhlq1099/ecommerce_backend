from pydantic import BaseModel,Field
from pydantic.generics import GenericModel
from typing import Optional,Generic,TypeVar

T = TypeVar('T')

class ProductBase(BaseModel):
    name: str
    description:str
    price:float
    quantity_in_stock: int
    product_sub_category_id:int

class ProductUpdate(BaseModel):
    name: Optional[str] =None
    description:Optional[str] = None
    price:Optional[float] = None
    quantity_in_stock: Optional[int] = None
    product_sub_category_id:Optional[int] = None

class ProductOut(BaseModel):
    name: str
    price: float
    quantity_in_stock: int

    class Config:
        orm_mode = True
        
class RequestProduct(BaseModel):
    parameter: ProductBase = Field(...)

class RequestProductUpdate(BaseModel):
    parameter: ProductUpdate = Field(...)

class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]