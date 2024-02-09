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

#Оставил валидацию почты и пароля на будущее

# class UserCreate(schemas.BaseUserCreate):
#     @validator('email')
#     def validate_email(cls, value):
#         if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", value):
#             raise ValueError('Неверный адрес электронной почты')
#         return value
#
#     email: constr(max_length=100)
#
#     @validator('password')
#     def validate_password(cls, value):
#         if len(value) < 8:
#             raise ValueError('Длина пароля должна составлять не менее 8 символов')
#         if not re.match(r"^(?=.*[A-Za-z])(?=.*[0-9!#$%&*+\-.=>?@^_]).+$", value):
#             raise ValueError('Пароль должен содержать по крайней мере одну букву и одну цифру или специальный символ')
#         return value
#
#     password: constr(min_length=8, max_length=16)
