from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import schemas
from src.auth.functions import register_async, authenticate_async, change_password_async, \
    is_user_authenticated
from src.auth.models import User
from src.auth.schemas import UserGet, ChangePasswordRequest
from src.database import get_async_session




router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"]
)


@router.post("/registration", response_model=schemas.User, status_code=201)
async def register_user_route(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await register_async(session=session, user_data=user_data)


@router.post("/authentification")
async def authenticate_user_route(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await authenticate_async(user_data, session=session)


@router.get("/get-me", response_model=UserGet)
async def get_user_info(user: UserGet = Depends(is_user_authenticated)):
    return user


@router.post("/change-password")
async def change_password(request_data: ChangePasswordRequest, current_user: User = Depends(is_user_authenticated),
                          session: AsyncSession = Depends(get_async_session)):
    user_email = current_user.email
    old_password = request_data.old_password
    new_password = request_data.new_password
    return await change_password_async(user_email, old_password, new_password, session=session)
