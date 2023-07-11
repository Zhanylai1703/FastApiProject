from typing import List
from pydantic import BaseModel, EmailStr


class CityBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True
        allow_population_by_field_name = True
        arbitrary_types_allowed = True


class CategoryBase(BaseModel):
    id: int
    name: str

    class Config:
        orm_mode = True


class UserIn(BaseModel):
    email: EmailStr
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginModel(BaseModel):
    email: str
    password: str


class NewPassword(BaseModel):
    old_password: str
    new_password: str
