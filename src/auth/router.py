from fastapi import APIRouter, Depends, HTTPException
from fastapi import Response
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from src.auth import schemas
from src.auth.jwt import create_jwt_token
from src.auth.models import User
from src.auth.functions import register_async, pwd_context, get_current_user
from src.database import get_async_session

router = APIRouter(
    prefix="/protect",
    tags=["Protect"]
)

@router.post("/Registration", response_model=schemas.User, status_code=201)
async def register(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await register_async(session=session, user_data=user_data)

@router.post("/Authentification")
async def authenticate_user(user_email: str, user_password: str, response: Response = Response(), session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.execute(select(User).where(User.email == user_email))
    user = existing_user.scalar()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    is_password_correct = pwd_context.verify(user_password, user.hashed_password)
    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    create_jwt_token(response, {"sub": user.email})
    return {"access_token": "Bearer"}

@router.get("/get_user") # Из-за того, что не работает get_current_user и verify_jwt_token не работает и эта ((((
def get_user(current_user: User = Depends(get_current_user)):
    return current_user