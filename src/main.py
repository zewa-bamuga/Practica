from fastapi import FastAPI
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))) # решение проблемs, при которой после распределения файлов по папкам не работыли импорты

from src.auth.base_config import auth_backend,fastapi_users
from src.auth.schemas import UserRead, UserCreate
from src.auth.router import router as router_protect

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