from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import schemas
from src.auth.functions import register_async, authenticate_async, change_password_async, \
    is_user_authenticated
from src.auth.models import User
from src.database import get_async_session

router = APIRouter(
    prefix="/Authentication",
    tags=["Authentication"]
)


@router.post("/Registration", response_model=schemas.User, status_code=201)
async def register_user_route(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await register_async(session=session, user_data=user_data)


@router.post("/Authentification")
async def authenticate_user_route(user_email: str, user_password: str,
                                  session: AsyncSession = Depends(get_async_session)):
    return await authenticate_async(user_email, user_password, session=session)


@router.get("/Get_me")
async def get_user_info(user: User = Depends(is_user_authenticated)):
    return user


@router.post("/Change_Password")
async def change_password(user_email: str, old_password: str, new_password: str,
                          session: AsyncSession = Depends(get_async_session)):
    return await change_password_async(user_email, old_password, new_password, session=session)
