from pydantic import BaseModel,EmailStr
from typing import List

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: int | None = None

class LoginInput(BaseModel):
    email: EmailStr
    password: str

class EmailSchema(BaseModel):
    email: List[EmailStr]