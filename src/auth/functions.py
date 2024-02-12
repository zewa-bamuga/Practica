from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth.jwt import create_jwt_token
from src.auth.models import User
from src.auth.schemas import UserCreate
from src.database import get_async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")
apikey_scheme = APIKeyHeader(name="Authorization")

async def register_async(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="Пользователь с этой электронной почтой уже существует!")

    user = User(email=user_data.email, hashed_password=pwd_context.hash(user_data.password), role_id=1)
    session.add(user)
    await session.commit()
    return user

async def authenticate_async(user_email: str, user_password: str, session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.execute(select(User).where(User.email == user_email))
    user = existing_user.scalar()

    if not user:
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

    is_password_correct = pwd_context.verify(user_password, user.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

    jwt_token = create_jwt_token({"sub": user.email})
    return {"access_token": jwt_token, "token_type": "bearer"}

async def change_password_async(user_email: str, old_password: str, new_password: str, session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.execute(select(User).where(User.email == user_email))
    user = existing_user.scalar()

    if not user:
        raise HTTPException(status_code=400, detail="Пользователь не найден")

    is_old_password_correct = pwd_context.verify(old_password, user.hashed_password)
    if not is_old_password_correct:
        raise HTTPException(status_code=400, detail="Неправильный старый пароль")

    user.hashed_password = pwd_context.hash(new_password)
    await session.commit()
    return {"message": "Пароль успешно обновлен"}
