from pydantic import BaseModel,Field, EmailStr
from datetime import date
from pydantic.generics import GenericModel
from typing import Optional,Generic,TypeVar

T = TypeVar('T')

class UserBase(BaseModel):
    email: EmailStr
    password: str
    confirm_password:str

class UserUpdate(BaseModel):
    is_activate:Optional[bool] = None
    is_profile:Optional[bool] = None
    role:Optional[int] =None

class UserOut(BaseModel):
    id :int
    email: str
    is_activate:bool
    is_profile:bool
    role:int

class User(BaseModel):
    email: EmailStr
    is_active: bool 

class UserDetail(BaseModel):
    full_name: str
    date_of_birth: date 
    class_name: str
    phone_number: str

class UserDetailUpdate(UserDetail):
    full_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    class_name: Optional[str] = None
    phone_number: Optional[str] = None

class RequestUser(BaseModel):
    parameter: UserBase = Field(...)
    
class RequestUserUpdate(BaseModel):
    parametr: UserUpdate = Field(...)

class RequestUserDetail(BaseModel):
    parameter: UserDetail = Field(...)

class RequestUserDetailUpdate(BaseModel):
    parameter: UserDetailUpdate = Field(...)

class Response(GenericModel,Generic[T]):
    code: str
    status: str
    message: str
    result: Optional[T]


