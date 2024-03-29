from pydantic import BaseModel, EmailStr, constr, validator
import re


class UserBase(BaseModel):
    email: EmailStr

    @validator('email')
    def validate_email(cls, ve):
        if not re.match(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$", ve):
            raise ValueError('Введены неверные значения')
        return ve


class UserAuth(UserBase):
    password: constr(min_length=8, max_length=16)

    @validator('password')
    def validate_password(cls, v):
        if not re.match(r"^(?=.*[A-Za-z])(?=.*[0-9!#$%&*+\-.=>?@^_]).+$", v):
            raise ValueError('Пароль должен содержать по крайней мере одну букву и одну цифру или специальный символ')
        return v


class UserCreate(UserBase):
    password: constr(min_length=8, max_length=16)
    confirm_password: constr(min_length=8, max_length=16)

    @validator('confirm_password')
    def passwords_match(cls, v, values, **kwargs):
        if 'password' in values and v != values['password']:
            raise ValueError('Пароли не совпадают')
        return v

    @validator('password')
    def validate_password(cls, v):
        if not re.match(r"^(?=.*[A-Za-z])(?=.*[0-9!#$%&*+\-.=>?@^_]).+$", v):
            raise ValueError('Пароль должен содержать по крайней мере одну букву и одну цифру или специальный символ')
        return v


class UserData(UserBase):
    id: int
    role_id: int

    class Config:
        orm_mode = True


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


class PasswordResetRequest(BaseModel):
    email: EmailStr


class PasswordResetConfirm(BaseModel):
    email: EmailStr
    code: str
    new_password: str
