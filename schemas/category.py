from pydantic import BaseModel,Field
from pydantic.generics import GenericModel
from typing import Optional,Generic,TypeVar

T = TypeVar('T')

class CategoryBase(BaseModel):
    name:str

class CategoryUpdate(BaseModel):
    name:Optional[str] = None

class RequestCategory(BaseModel):
    parameter: CategoryBase = Field(...)

class RequestCategoryUpdate(BaseModel):
    parameter: CategoryUpdate = Field(...)

class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]