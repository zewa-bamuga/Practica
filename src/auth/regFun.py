from fastapi import Depends, HTTPException
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.auth.schemas import UserCreate, UserAuth

from src.database import get_async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

async def register_async(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="User with this email already exists!")

    user = User(email=user_data.email, hashed_password=pwd_context.hash(user_data.password), role_id=1)
    session.add(user)
    await session.commit()
    return user
