from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import session

from src.auth import schemas
from src.auth.jwt import create_jwt_token, verify_jwt_token
from src.auth.models import User
from src.auth.regFun import register_async, pwd_context, oauth2_scheme
from src.auth.schemas import UserCreate
from src.database import get_async_session


router = APIRouter(
    prefix="/protect",
    tags=["Protect"]
)

@router.post("/Registration", response_model=schemas.User, status_code=201)
async def register(user_data: schemas.UserCreate, session: AsyncSession = Depends(get_async_session)):
    return await register_async(session=session, user_data=user_data)


@router.post("/Authentification")
async def authenticate_user(user_email: str, user_password: str, session: AsyncSession = Depends(get_async_session)):
    existing_user = await session.execute(select(User).where(User.email == user_email))
    user = existing_user.scalar()
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect username or password")

    is_password_correct = pwd_context.verify(user_password, user.hashed_password)

    if not is_password_correct:
        raise HTTPException(status_code=400, detail="Incorrect username or password")
    jwt_token = create_jwt_token({"sub": user.email})
    return {"access_token": jwt_token, "token_type": "bearer"}

async def get_current_user(token: str = Depends(oauth2_scheme)):
    decoded_data = verify_jwt_token(token)
    if not decoded_data:
        raise HTTPException(status_code=400, detail="Invalid token")
    user_email = decoded_data.get("sub")
    existing_user = await session.execute(select(User).where(User.email == user_email))
    user = existing_user.scalar()
    if not user:
        raise HTTPException(status_code=400, detail="User not found")
    return user

@router.get("/get_user")
def get_user(current_user: User = Depends(get_current_user)):
    return current_user