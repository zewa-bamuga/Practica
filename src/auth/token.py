import uuid
from fastapi import Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth.models import User, Token
from src.auth.regFun import pwd_context
from src.auth.schemas import UserAuth
from src.database import get_async_session
from starlette.status import HTTP_404_NOT_FOUND

# async def create_token(user_data: UserAuth, session: AsyncSession = Depends(get_async_session)):
#     user = await session.execute(select(User).where(User.email == user_data.email))
#     user = user.scalar()
#
#     if not user:
#         raise HTTPException(status_code=HTTP_404_NOT_FOUND, detail="User not found")
#
#     if not pwd_context.verify(user_data.password, user.hashed_password):
#         raise HTTPException(status_code=400, detail="Incorrect username or password")
#
#     token = Token(user_id=user.id, access_token=str(uuid.uuid4()))
#     session.add(token)
#     await session.commit()
#
#     return {"access_token": token.access_token}