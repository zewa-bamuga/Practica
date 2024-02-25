from fastapi import Depends
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

import jwt
from datetime import datetime, timedelta

from src.auth.models import User
from src.database import get_async_session

from fastapi import HTTPException

SECRET_KEY = "e95a3684b9982fcfd46eea716707f80cef515906eb49c4cb961dfde39a41ce21"
ALGORITHM = "HS256"
EXPIRATION_TIME = timedelta(minutes=30)


def create_jwt_token(data: dict):
    expiration = datetime.utcnow() + EXPIRATION_TIME
    data.update({"exp": expiration})
    token = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return token


async def verify_jwt_token(access_token: str, session: AsyncSession = Depends(get_async_session)):
    try:
        decoded_data = jwt.decode(access_token, SECRET_KEY, algorithms=[ALGORITHM])
        user_email = decoded_data.get("sub")
        existing_user = await session.execute(select(User).where(User.email == user_email))
        user = existing_user.scalar_one_or_none()
        if user:
            return decoded_data, user
    except jwt.PyJWTError as e:
        print("JWT ошибка декодирования:", e)
        raise HTTPException(status_code=401, detail="Неверный токен или истек срок действия")
    return None, None
