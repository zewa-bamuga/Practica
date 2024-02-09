from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import schemas
from src.auth.models import User
from src.auth.functions import register_async, get_current_user, authenticate_async
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

@router.get("/get_user") # Из-за того, что не работает get_current_user и verify_jwt_token не работает и эта ((((
def get_user(current_user: User = Depends(get_current_user)):
    return current_user