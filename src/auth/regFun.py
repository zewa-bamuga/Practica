from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User
from src.auth.schemas import UserCreate, UserAuth

from src.database import get_async_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

async def register_async(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.execute(select(User).where(User.email == user_data.email))
    if existing_user.scalar():
        raise HTTPException(status_code=400, detail="User with this email already exists!")

    user = User(email=user_data.email, hashed_password=pwd_context.hash(user_data.password), role_id=1)
    session.add(user)
    await session.commit()

    return user

# async def authenticate_user(user_data: UserAuth, session: AsyncSession = Depends(get_async_session)):
#     user = await session.execute(select(User).where(User.email == user_data.email))
#     user = user.scalar()
#     if not user or not pwd_context.verify(user_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#     jwt_token = create_jwt_token({"sub": user.email})
#     return {"access_token": jwt_token}
#
# async def get_user_by_email(email: str):
#     async with get_async_session() as session:
#         result = await session.execute(select(User).where(User.email == email))
#         user = result.scalar()
#         return user