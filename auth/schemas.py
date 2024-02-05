import os
from typing import Optional
from fastapi_users import schemas

class UserCreate(schemas.BaseUserCreate):
    email: str
    password: str

    # Проверяем, что мы не запущены в Docker Compose
    if os.getenv("DOCKER_COMPOSE") != "true":
        is_active: Optional[bool] = True
        is_superuser: Optional[bool] = False
        is_verified: Optional[bool] = False

class UserRead(schemas.BaseUser[int]):
    id: int
    email: str

    # Проверяем, что мы не запущены в Docker Compose
    if os.getenv("DOCKER_COMPOSE") != "true":
        is_active: bool = True
        is_superuser: bool = False
        is_verified: bool = False

    class Config:
        from_attributes = True