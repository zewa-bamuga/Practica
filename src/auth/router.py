from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import schemas
from src.auth.jwt import verify_jwt_token
from src.auth.functions import register_async, authenticate_async, apikey_scheme, change_password_async
from src.database import get_async_session

router = APIRouter(
    prefix="/Authentication",
    tags=["Authentication"]
)

@router.post("/Registration", response_model=schemas.User, status_code=201)
async def register_user_route(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await register_async(session=session, user_data=user_data)

@router.post("/Authentification")
async def authenticate_user_route(user_email: str, user_password: str, session: AsyncSession = Depends(get_async_session)):
    return await authenticate_async(user_email, user_password, session=session)

@router.get("/Get_me", response_model=schemas.User)
async def get_user(access_token: str = Depends(apikey_scheme), session: AsyncSession = Depends(get_async_session)):
    decoded_token, user = await verify_jwt_token(access_token, session)
    if user is None:
        raise HTTPException(status_code=404, detail="Пользователь не найден")
    return user

@router.post("/Change_Password")
async def change_password(user_email: str, old_password: str, new_password: str, session: AsyncSession = Depends(get_async_session)):
    return await change_password_async(user_email, old_password, new_password, session=session)