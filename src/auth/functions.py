from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer, APIKeyHeader
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import schemas
from src.auth.jwt import create_jwt_token, verify_jwt_token
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


async def authenticate_async(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    user_email = user_data.email
    user_password = user_data.password

    existing_user = await session.execute(select(User).where(User.email == user_email))
    user = existing_user.scalar()

    if not user:
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

    is_password_correct = pwd_context.verify(user_password, user.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Неверное имя пользователя или пароль")

    jwt_token = create_jwt_token({"sub": user.email})
    return {"access_token": jwt_token, "token_type": "bearer"}


async def is_user_authenticated(access_token: str = Depends(apikey_scheme),
                                session: AsyncSession = Depends(get_async_session)):
    decoded_token, user = await verify_jwt_token(access_token, session)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user
