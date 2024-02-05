from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
from typing import List

from sqlalchemy import insert, select
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends

from auth.base_config import auth_backend, fastapi_users
from auth.schemas import UserRead, UserCreate
from auth.router import router as router_protect

from database import async_session_maker, get_async_session

app = FastAPI(
    title="Путеводитель по необычным местам"
)

app.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
    prefix="/auth",
    tags=["Auth"],
)

app.include_router(router_protect)
app.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/auth",
    tags=["Auth"],
)