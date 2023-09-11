from pydantic import BaseModel,Field
from pydantic.generics import GenericModel
from typing import Optional,Generic,TypeVar

T = TypeVar('T')

class SubCategoryBase(BaseModel):
    name:str
    product_category_id:int

class SubCategoryUpdate(BaseModel):
    name:Optional[str] = None
    product_category_id:Optional[int] = None

class RequestSubCategory(BaseModel):
    parameter: SubCategoryBase = Field(...)

class RequestSubCategoryUpdate(BaseModel):
    parameter: SubCategoryUpdate = Field(...)

class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]