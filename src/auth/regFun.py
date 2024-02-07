#тут функция для регистрации, если всё норм с регистрацией, то надо будет перенести
from fastapi import Depends, HTTPException
from passlib.context import CryptContext
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_400_BAD_REQUEST

from src.auth.models import User
from src.auth.schemas import UserCreate
from src.database import get_async_session

pwd_context = CryptContext(["bcrypt"], deprecated="auto")

async def register_async(user_data: UserCreate, session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.scalar(select(User).where(User.email == user_data.email))
    if existing_user:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail="User with this email already exists!"
        )

    user = User(email=user_data.email, role_id=1)
    user.hashed_password = pwd_context.hash(user_data.password)
    session.add(user)
    await session.commit()

    return {"id": user.id, "email": user.email, "role_id": user.role_id}
    #не знаю почему если не выводить role_id, то выдаёт ошибку, но пользователя записывает в бд
    # return {"id": user.id, "email": user.email}