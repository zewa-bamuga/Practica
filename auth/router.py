from fastapi import APIRouter, Depends

from auth.base_config import fastapi_users
from auth.models import User

router = APIRouter(
    prefix="/protect",
    tags=["Protect"]
)

current_user = fastapi_users.current_user()

@router.get("/")
def login_verification(user: User = Depends(current_user)):
    return f"Hello, {user.email}"