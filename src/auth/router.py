from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import schemas
from src.auth.base_config import fastapi_users
from src.auth.schemas import User
from src.auth.regFun import register_async
from src.auth.token import create_token
from src.database import get_async_session

router = APIRouter(
    prefix="/protect",
    tags=["Protect"]
)

#роутер для регистрации
@router.post("/Registration", response_model=schemas.User, status_code=201)
async def register(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await register_async(session=session, user_data=user_data)

#роутер для авторизации
@router.post("/Authentification",  response_model=schemas.Token, status_code=201)
async def token(user_data: schemas.UserAuth, session: AsyncSession = Depends(get_async_session)):
    return await create_token(session=session, user_data=user_data)


# current_user = fastapi_users.current_user()
#
# @router.get("/")
# def login_verification(user: User = Depends(current_user)):
#     return f"Hello, {user.email}"