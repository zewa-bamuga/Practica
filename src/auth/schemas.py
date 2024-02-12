from pydantic import BaseModel, EmailStr, constr, validator
import re

class UserBase(BaseModel):
    email: EmailStr
    @validator('email')
    def validate_email(cls, ve):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", ve):
            raise ValueError('Введены неверные значения')
        return ve

class UserCreate(UserBase):
    password: constr(min_length=8, max_length=16)
    @validator('password')
    def validate_password(cls, v):
        if not re.match(r"^(?=.*[A-Za-z])(?=.*[0-9!#$%&*+\-.=>?@^_]).+$", v):
            raise ValueError('Пароль должен содержать по крайней мере одну букву и одну цифру или специальный символ')
        return v

class User(UserBase):
    id: int
    role_id: int

    class Config:
        orm_mode = True


class UserGet(BaseModel):
    email: EmailStr

    class Config:
        orm_mode = True

class ChangePasswordRequest(BaseModel):
    old_password: str
    new_password: str