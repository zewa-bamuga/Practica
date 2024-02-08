from fastapi import APIRouter, Depends, Body, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from src.auth import schemas
from src.auth.jwt import signJWT
from src.auth.schemas import UserAuth
from src.auth.regFun import register_async, pwd_context
from src.database import get_async_session
from src.auth.models import User

router = APIRouter(
    prefix="/protect",
    tags=["Protect"]
)

@router.post("/Registration", response_model=schemas.User, status_code=201)
async def register(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await register_async(session=session, user_data=user_data)


async def get_user_by_email(email: str, session: AsyncSession = Depends(get_async_session)):
    async with session() as async_session:
        user = await async_session.execute(select(User).where(User.email == email))
        return user.scalar()
@router.post("/Login", response_model=schemas.User, status_code=201)
async def user_login(user_auth: UserAuth = Body(...)):
    user = await get_user_by_email(user_auth.email)
    if user and pwd_context.verify(user_auth.password, user.hashed_password):
        return signJWT(user)
    else:
        raise HTTPException(status_code=400, detail="Invalid login details")
