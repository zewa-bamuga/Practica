from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.auth import schemas
from src.auth.functions import register_async, authenticate_async
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
