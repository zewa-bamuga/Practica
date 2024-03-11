from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import schemas
from src.auth.functions import register_and_authenticate_async, authenticate_async, request_password_reset, confirm_password_reset
from src.auth.schemas import PasswordResetRequest, PasswordResetConfirm
from src.database import get_async_session

router = APIRouter(
    prefix="/authentication",
    tags=["Authentication"]
)


@router.post("/registration")
async def register_user_route(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await register_and_authenticate_async(user_data, session=session)


@router.post("/password/reset/request", status_code=200)
async def password_reset_request(password_reset_request: PasswordResetRequest,
                                 session: AsyncSession = Depends(get_async_session)):
    await request_password_reset(password_reset_request.email, session)


@router.post("/password/reset/confirm", status_code=200)
async def password_reset_confirm(password_reset_confirm: PasswordResetConfirm,
                                 session: AsyncSession = Depends(get_async_session)):
    await confirm_password_reset(password_reset_confirm.email, password_reset_confirm.code,
                                 password_reset_confirm.new_password, session)


@router.post("/authentification")
async def authenticate_user_route(user_data: schemas.UserAuth, session: AsyncSession = Depends(get_async_session)):
    return await authenticate_async(user_data, session=session)
